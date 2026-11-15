"""Small, auditable source neighborhoods learned from accepted compiler matches."""
import json
from functools import lru_cache
from pathlib import Path
import re

TABLE = Path(__file__).with_name('matching_patterns.json')


def transformations(code):
    """Yield (pattern id, source); all acceptance still requires full byte equality."""
    for row in json.loads(TABLE.read_text()):
        operation = row['operation']
        if operation == 'integer_cursor':
            for m in re.finditer(r'\b(u8|u16|u32|s8|s16|s32)\s*\*\s*(\w+)\s*=\s*([^;\n]+);', code):
                name = m[2] + '_address'
                if re.search(r'\b' + name + r'\b', code):
                    continue
                replacement = 'u32 %s = (u32)(%s);\n%s *%s = (%s *)%s;' % (
                    name, m[3], m[1], m[2], m[1], name)
                yield row['id'], code[:m.start()] + replacement + code[m.end():]
        elif operation == 'scaled_stack_address':
            for m in re.finditer(r'\b(\w+) = (\w+) \+ ([^;\n]+) \+ 1;', code):
                if not re.search(r'\bu16\s+' + m[2] + r'\s*\[', code):
                    continue
                name = m[1] + '_byte_offset'
                if re.search(r'\b' + name + r'\b', code):
                    continue
                replacement = '{ u32 %s; %s = (%s) * 2; %s = (u16 *)(%s + (u32)%s); %s++; }' % (
                    name, name, m[3], m[1], name, m[2], m[1])
                yield row['id'], code[:m.start()] + replacement + code[m.end():]
        elif operation == 'global_cursor':
            # Restrict to one function with a void parameter list and word globals.
            function = re.search(r'\bfunc_[0-9A-F]+\(void\)\s*\{', code)
            loop = re.search(r'\b(for|while|do)\b', code)
            if not function or not loop:
                continue
            declared = set(re.findall(r'extern u32 ([^;]+);', code))
            globals_ = {part.strip() for declaration in declared for part in declaration.split(',')
                        if re.fullmatch(r'g_[0-9A-F]+', part.strip())}
            for name in sorted(globals_):
                cursor = name + '_cursor'
                if cursor in code:
                    continue
                tail = code[loop.start():]
                if name not in tail:
                    continue
                tail = re.sub(r'\b' + name + r'\b', '(*' + cursor + ')', tail)
                prefix = code[:function.end()] + '\nu32 *' + cursor + ';' + code[function.end():loop.start()]
                yield row['id'], prefix + cursor + ' = &' + name + ';\n' + tail
        elif operation == 'register_local':
            for m in re.finditer(r'(?m)^(\s*)(u32|s32|int|u16|s16|u8)\s+\w+\s*=', code):
                yield row['id'], code[:m.start(2)] + 'register ' + code[m.start(2):]
        elif operation == 'separate_postincrement':
            for m in re.finditer(r'\b(\w+)\s*(=|\+=)\s*\*(\w+)\+\+;', code):
                replacement = '%s %s *%s;\n%s++;' % (m[1], m[2], m[3], m[3])
                yield row['id'], code[:m.start()] + replacement + code[m.end():]
            for m in re.finditer(r'\*(\w+)\+\+\s*=\s*([^;]+);', code):
                replacement = '*%s = %s;\n%s++;' % (m[1], m[2], m[1])
                yield row['id'], code[:m.start()] + replacement + code[m.end():]
        elif operation == 'structured_backedge':
            ending = re.compile(r'if\s*\(([^;{}]+)\)\s*goto\s+(\w+);\s*if\s*\(([^;{}]+)\)\s*goto\s+(\w+);\s*\2:')
            for end in ending.finditer(code):
                begin = re.search(r'(?m)^\s*' + re.escape(end[4]) + r':', code[:end.start()])
                if not begin:
                    continue
                # Other jumps into or out of the proposed loop need manual work.
                middle = code[begin.end():end.start()]
                if re.search(r'\bgoto\s+(?:' + re.escape(end[2]) + '|' + re.escape(end[4]) + r')\b', middle):
                    continue
                replacement = ('while (1) {' + middle + 'if (' + end[1] + ') break;\n'
                               'if (!(' + end[3] + ')) break;\n}')
                yield row['id'], code[:begin.start()] + replacement + code[end.end():]
        elif operation == 'direct_mask_assignment':
            assignment = re.compile(r'\b(\w+) = (\w+);\s*(\w+) = (0x[0-9A-Fa-f]+|\d+);\s*\1 &= \3;')
            for m in assignment.finditer(code):
                replacement = m[1] + ' = ' + m[2] + ' & ' + m[4] + ';'
                yield row['id'], code[:m.start()] + replacement + code[m.end():]
        elif operation == 'direct_zero_test':
            for m in re.finditer(r'\b(\w+) = (\w+);\s*if \(\1 == 0\)', code):
                yield row['id'], code[:m.start()] + 'if (' + m[2] + ' == 0)' + code[m.end():]
        elif operation == 'direct_mask_test':
            test = re.compile(r'\b(\w+) = (\w+);\s*\1 &= (\w+);\s*if\s*\(\1 ([!=]=) ([^()]+)\)')
            for m in test.finditer(code):
                replacement = 'if ((' + m[2] + ' & ' + m[3] + ') ' + m[4] + ' ' + m[5] + ')'
                yield row['id'], code[:m.start()] + replacement + code[m.end():]
            copied_mask = re.compile(r'\b(\w+) = (\w+);\s*(\w+) = (\w+);\s*\1 &= \3;\s*if \(\1 ([!=]=) \4\)')
            for m in copied_mask.finditer(code):
                replacement = 'if ((' + m[2] + ' & ' + m[4] + ') ' + m[5] + ' ' + m[4] + ')'
                yield row['id'], code[:m.start()] + replacement + code[m.end():]
        elif operation == 'named_add_input':
            for m in re.finditer(r'\b(\w+) = (\w+) \+ \1;', code):
                name = m[1] + '_add_input'
                if name in code:
                    continue
                replacement = '{ u32 ' + name + ' = ' + m[1] + '; ' + m[1] + ' = ' + m[2] + ' + ' + name + '; }'
                yield row['id'], code[:m.start()] + replacement + code[m.end():]
        elif operation == 'direct_short_return':
            # The jump must lead directly to returning that one scalar. Other
            # labels, cleanup and observable effects make this inapplicable.
            for tail in re.finditer(r'(?m)^\s*(\w+):\s*return (\w+);\s*}', code):
                label, result = tail[1], tail[2]
                jump = re.compile(r'\b' + re.escape(result) + r'\s*=\s*([^;{}]+);\s*goto ' + re.escape(label) + r';')
                head = code[:tail.start()]
                if not jump.search(head):
                    continue
                head = jump.sub(lambda m: 'return ' + m[1] + ';', head)
                if re.search(r'\bgoto\s+' + re.escape(label) + r'\b', head):
                    continue
                direct = head + 'return ' + result + ';\n}' + code[tail.end():]
                yield row['id'], direct
                for typ in ('s32', 'u32'):
                    widened = re.sub(r'\b(?:u16|s16|u8|s8)\s+' + re.escape(result) + r'\s*;', typ + ' ' + result + ';', direct)
                    if widened != direct:
                        yield row['id'], widened
        elif operation == 'distributed_offset':
            # These are declaration hypotheses, including signed widths; byte
            # equality remains the only evidence that a proposal is usable.
            for m in re.finditer(r'\b(\w+) - \((\w+) ([+-]) (\d+)\)', code):
                op = '+' if m[3] == '-' else '-'
                replacement = m[1] + ' ' + op + ' ' + m[4] + ' - ' + m[2]
                yield row['id'], code[:m.start()] + replacement + code[m.end():]
            for m in re.finditer(r'\b(\w+) - (\d+) - (\w+)\b', code):
                replacement = m[1] + ' - (' + m[3] + ' + ' + m[2] + ')'
                yield row['id'], code[:m.start()] + replacement + code[m.end():]
        elif operation == 'guarded_loop':
            # Import lazily to keep the table usable independently.
            from variant_search import loop_mutations
            for source in loop_mutations(code):
                yield row['id'], source


@lru_cache(maxsize=256)
def focus_regions(code, pattern):
    """Precompute selected statement extents once per parent source and regex."""
    regions = []
    for match in re.finditer(pattern, code):
        left = max(code.rfind(c, 0, match.start()) for c in ';{}\n') + 1
        stops = [code.find(c, match.end()) for c in ';{}\n']
        right = min([at for at in stops if at >= 0] or [len(code)])
        regions.append((left, right))
    return tuple(regions)


def touches_focus(before, after, pattern):
    """Whether an edit intersects a selected source region, including insertions."""
    if not pattern:
        return True
    lo = 0
    while lo < min(len(before), len(after)) and before[lo] == after[lo]:
        lo += 1
    hi = len(before)
    tail = 0
    while tail < min(len(before), len(after)) - lo and before[-tail-1] == after[-tail-1]:
        tail += 1
    hi -= tail
    return any(left <= hi and right >= lo for left, right in focus_regions(before, pattern))
