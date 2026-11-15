"""Reproduce the retained near-first, explicit-expression and scope candidate."""
from pathlib import Path
HERE=Path(__file__).resolve().parent

def prepare():
    s=(HERE.parent/'arm-16da8-1107/func_08016DA8_match.c').read_text()
    condition='''            if ((s32)depth[0] > 767 && (s32)depth[1] > 767 &&
                (s32)depth[2] > 767 && (s32)depth[3] > 767) {'''
    begin=s.index(condition)
    middle=s.index('            } else {',begin)
    tail=s.index('            face += 56u;',middle)
    direct=s[begin+len(condition):middle]
    near=s[middle+len('            } else {'):tail-len('            }\n')]
    inverted='''            if ((s32)depth[0] <= 767 || (s32)depth[1] <= 767 ||
                (s32)depth[2] <= 767 || (s32)depth[3] <= 767) {'''
    s=s[:begin]+inverted+near+'            } else {'+direct+'            }\n'+s[tail:]
    s=s.replace('    u32 face, next_ring, point[4], depth[4], part, packet;',
                '    u32 depth[4];\n    u32 face, next_ring, point[4], part, packet;')
    def body(name):
        p = s.index(' '+name+'(')
        opening = s.index('{', p)
        level = 1
        end = opening + 1
        while level:
            level += (s[end] == '{') - (s[end] == '}')
            end += 1
        return s[opening+1:end-1]
    expression = body('visible').strip().removeprefix('return ').removesuffix(';')
    import re
    s = s.replace('visible(MEM32(CURRENT))',
                  '('+re.sub(r'\bpacket\b', 'MEM32(CURRENT)', expression)+')')
    s = s.replace('project_subquad();', '{'+body('project_subquad')+'}')
    begin = s.index('{', s.index('void func_08016DA8(void)')) + 1
    end = s.index('    do {', begin)
    s = s[:begin]+'\n    u32 next_ring;\n    u32 depth[4];\n    u32 part;\n    u32 face;\n    u32 packet;\n    u32 point[4];\n\n    u32 tick = MEM32(ADDRESS_030001B8);\n    u32 ring = (tick - 29u) & 31u, end = (tick - 6u) & 31u;\n'+s[end:]
    return s

if __name__=='__main__':
    import sys
    target = HERE/'func_08016DA8.c'
    result = prepare()
    if '--check' in sys.argv:
        assert target.read_text() == result, 'retained candidate differs'
    else:
        target.write_text(result)
