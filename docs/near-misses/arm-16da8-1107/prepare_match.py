#!/usr/bin/env python3
"""One deterministic source-shape change, not a permutation/search family.

Expand only repeats that the original function spells out in instructions;
leave its actual ring, face, projection and four-part loops intact.
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def replace_function(source, name, replacement):
    # Locate the named definition, then its balanced-brace body.
    position = source.index(' '+name+'(')
    start = source.rfind('static __inline__ ', 0, position)
    opening = source.index('{', position)
    depth, closing = 1, opening+1
    while depth:
        if source[closing] == '{': depth += 1
        if source[closing] == '}': depth -= 1
        closing += 1
    return source[:start]+replacement+source[closing:]


def prepare():
    source = (HERE/'func_08016DA8.c').read_text()
    source = ('/* Matching-shape candidate: deterministic expansion of instruction-level\n'
              ' * repeats by prepare_match.py; still NOT an exact replacement. */\n'+source)
    visible = 'static __inline__ int visible(u32 packet)\n{\n    return '
    visible += ' ||\n           '.join(
        f'(MEM16(packet + {2*i}) <= 119 && signed_half(packet + {8+2*i}) >= 0 && signed_half(packet + {8+2*i}) <= 159)'
        for i in range(4))+';\n}'
    source = replace_function(source, 'visible', visible)
    clamp = 'static __inline__ void clamp_x(void)\n{\n    u32 packet;\n'
    for condition, value in [('<= -67', '(u16)-66'), ('> 186', '186')]:
        for i in range(4):
            clamp += (f'    packet = MEM32(CURRENT);\n'
                      f'    if (signed_half(packet + {2*i}) {condition}) MEM16(packet + {2*i}) = {value};\n')
    source = replace_function(source, 'clamp_x', clamp+'}')
    sub = ('static __inline__ void subdivide(u32 face, u32 part)\n{\n'
           '    u32 a = point_address(MEM32(face + 4));\n'
           '    u32 b = point_address(MEM32(face + 8));\n'
           '    u32 c = point_address(MEM32(face + 12));\n'
           '    u32 d = point_address(MEM32(face + 16));\n')
    topology = [('a', 'ab', 'ac', 'ad'), ('ab', 'b', 'bc', 'ac'),
                ('ac', 'bc', 'c', 'dc'), ('ad', 'ac', 'dc', 'd')]
    for part, corners in enumerate(topology):
        sub += f'    if (part == {part}) {{\n'
        for component in (0, 4, 8):
            for corner, expression in enumerate(corners):
                value = f'MEM32({expression} + {component})' if len(expression) == 1 else (
                    f'midpoint(MEM32({expression[0]} + {component}), MEM32({expression[1]} + {component}))')
                sub += f'        MEM32(SCRATCH + {corner*12+component}) = {value};\n'
        sub += '    }\n'
    source = replace_function(source, 'subdivide', sub+'}')
    texture = 'static __inline__ void texture_subquad(u32 face, u32 part)\n{\n'
    topology = [('a', 'ab', 'bd', 'ad'), ('ab', 'b', 'bc', 'bd'),
                ('bd', 'bc', 'c', 'cd'), ('ad', 'bd', 'cd', 'd')]
    for part, corners in enumerate(topology):
        texture += f'    if (part == {part}) {{\n'
        for corner, expression in enumerate(corners):
            for axis in (0, 1):
                base = 20+axis*16
                if len(expression) == 1:
                    value = f'MEM8(face + {base+4*(ord(expression)-ord("a"))})'
                else:
                    a, b = [base+4*(ord(c)-ord('a')) for c in expression]
                    value = f'(u8)midpoint(MEM32(face + {a}), MEM32(face + {b}))'
                texture += f'        MEM8(MEM32(CURRENT) + {16+axis*4+corner}) = {value};\n'
        texture += '    }\n'
    source = replace_function(source, 'texture_subquad', texture+'}')
    near = ('static __inline__ void near_expand_and_clamp(void)\n{\n'
            '    u32 packet = MEM32(CURRENT);\n'
            '    MEM16(packet + 8) = (u16)(MEM16(packet + 8) - 1u);\n'
            '    MEM16(packet) = (u16)(MEM16(packet) - 1u);\n'
            '    MEM16(packet + 2) = (u16)(MEM16(packet + 2) + 1u);\n'
            '    MEM16(packet + 10) = (u16)(MEM16(packet + 10) - 1u);\n')
    for condition, value in [('< -175', '(u16)-174'), ('> 335', '334')]:
        for i in range(4):
            near += (f'    packet = MEM32(CURRENT);\n'
                     f'    if (signed_half(packet + {8+2*i}) {condition}) MEM16(packet + {8+2*i}) = {value};\n')
    source = replace_function(source, 'near_expand_and_clamp', near+'    clamp_x();\n}')
    old = '''            for (i = 0; i != 4; ++i) {
                point[i] = point_address(MEM32(face + 4 + i*4));
                depth[i] = MEM32(point[i] + 24);
            }'''
    new = '\n'.join(f'            point[{i}] = point_address(MEM32(face + {4+4*i}));\n'
                    f'            depth[{i}] = MEM32(point[{i}] + 24);' for i in range(4))
    assert old in source
    source = source.replace(old, new)
    old = '''                for (i = 0; i != 4; ++i) {
                    MEM16(packet + i*2) = MEM16(point[i] + 16);
                    MEM16(packet + 8 + i*2) = MEM16(point[i] + 20);
                }'''
    new = '\n'.join(f'                MEM16(packet + {i*2}) = MEM16(point[{i}] + 16);\n'
                    f'                MEM16(packet + {8+i*2}) = MEM16(point[{i}] + 20);' for i in range(4))
    assert old in source
    source = source.replace(old, new)
    old = '''                    for (i = 0; i != 4; ++i) {
                        MEM8(MEM32(CURRENT) + 16 + i) = MEM8(face + 20 + i*4);
                        MEM8(MEM32(CURRENT) + 20 + i) = MEM8(face + 36 + i*4);
                    }'''
    new = '\n'.join(f'                    MEM8(MEM32(CURRENT) + {16+i}) = MEM8(face + {20+i*4});\n'
                    f'                    MEM8(MEM32(CURRENT) + {20+i}) = MEM8(face + {36+i*4});' for i in range(4))
    assert old in source
    source = source.replace(old, new).replace('u32 face, next_ring, i, point[4]', 'u32 face, next_ring, point[4]')
    # Accepted neighboring ARM C uses external address identities, rather than
    # synthesizing known RAM addresses with MOV/ADD. Keep the immediate point
    # and face bases: the original constructs those as immediate arithmetic.
    globals_ = [0x030001B8, 0x030021C4, 0x03000670, 0x030057A0,
                0x03005F70, 0x03005F80, 0x03002A18, 0x03001B28,
                0x03005F58, 0x03000DF8, 0x03000DE0, 0x0804F330]
    definitions = '#ifndef TXRA_SYNTHETIC\n'
    for address in globals_:
        definitions += f'extern u8 g_{address:08X}[];\n#define ADDRESS_{address:08X} ((u32)g_{address:08X})\n'
    definitions += '#else\n'
    for address in globals_:
        definitions += f'#define ADDRESS_{address:08X} 0x{address:08X}u\n'
    definitions += '#endif\n\n'
    for address in globals_:
        source = source.replace(f'0x{address:08X}u', f'ADDRESS_{address:08X}')
    insertion = source.index('#define CURRENT')
    source = source[:insertion]+definitions+source[insertion:]
    return source


if __name__ == '__main__':
    destination = HERE/'func_08016DA8_match.c'
    result = prepare()
    if '--check' in sys.argv:
        assert destination.read_text() == result, 'matching-shape source is stale'
    else:
        destination.write_text(result)
