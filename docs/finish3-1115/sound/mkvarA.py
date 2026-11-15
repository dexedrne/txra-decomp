base = open('../../near-misses/finish2-1115-sound/func_080064A4.c').read()
OLD = """                        piece = commands[cidx + 1] << 8;
                        gMasterVolume = (piece += gFadeLevel) + (gFadeLevel << 4);
                        REG(0x04000080) = gMasterVolume;"""
assert base.count(OLD) == 1
P = "                        "
V = {
 'A2_twice': ["piece = commands[cidx + 1] << 8;", "piece += gFadeLevel;", "gMasterVolume = piece + (gFadeLevel << 4);", "REG(0x04000080) = piece + (gFadeLevel << 4);"],
 'A3_chain': ["piece = commands[cidx + 1] << 8;", "piece += gFadeLevel;", "REG(0x04000080) = gMasterVolume = piece + (gFadeLevel << 4);"],
 'A4_inplace': ["piece = commands[cidx + 1] << 8;", "piece += gFadeLevel;", "piece += gFadeLevel << 4;", "gMasterVolume = piece;", "REG(0x04000080) = piece;"],
 'A6_mul16': ["piece = commands[cidx + 1] << 8;", "piece += gFadeLevel;", "gMasterVolume = piece + gFadeLevel * 16;", "REG(0x04000080) = gMasterVolume;"],
 'A7_regpiece': ["piece = commands[cidx + 1] << 8;", "piece += gFadeLevel;", "gMasterVolume = piece + (gFadeLevel << 4);", "REG(0x04000080) = piece + (gFadeLevel << 4);"],
 'A8_mul256': ["piece = commands[cidx + 1] * 256;", "piece += gFadeLevel;", "gMasterVolume = piece + (gFadeLevel << 4);", "REG(0x04000080) = gMasterVolume;"],
 'A9_regfirst': ["piece = commands[cidx + 1] << 8;", "piece += gFadeLevel;", "REG(0x04000080) = piece + (gFadeLevel << 4);", "gMasterVolume = piece + (gFadeLevel << 4);"],
 'A10_shift_after': ["piece = commands[cidx + 1];", "piece <<= 8;", "piece += gFadeLevel;", "gMasterVolume = piece + (gFadeLevel << 4);", "REG(0x04000080) = gMasterVolume;"],
 'A11_or': ["piece = commands[cidx + 1] << 8;", "piece += gFadeLevel;", "gMasterVolume = piece | (gFadeLevel << 4);", "REG(0x04000080) = gMasterVolume;"],
}
for k, lines in V.items():
    open('varA/%s.c' % k, 'w').write(base.replace(OLD, '\n'.join(P + l for l in lines)))
