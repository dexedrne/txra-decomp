import sys, re
base = open('../../near-misses/finish2-1115-sound/func_080064A4.c').read()
OLD = """                    if (command == 0x67) {
                        piece = commands[cidx + 1] << 8;
                        gMasterVolume = (piece += gFadeLevel) + (gFadeLevel << 4);
                        REG(0x04000080) = gMasterVolume;
                        gVoices[i].command = cidx + 2;
                    }"""
assert base.count(OLD) == 1
V = {}
V['v01_blockpiece'] = (OLD, """                    if (command == 0x67) {
                        u32 piece = commands[cidx + 1] << 8;
                        piece += gFadeLevel;
                        gMasterVolume = piece + (gFadeLevel << 4);
                        REG(0x04000080) = gMasterVolume;
                        gVoices[i].command = cidx + 2;
                    }""")
V['v02_twostmt'] = (OLD, OLD.replace("gMasterVolume = (piece += gFadeLevel) + (gFadeLevel << 4);", "piece += gFadeLevel;\n                        gMasterVolume = piece + (gFadeLevel << 4);"))
V['v03_index'] = (OLD, OLD.replace("piece", "index"))
V['v04_s32'] = ("    u32 piece;\n", "    s32 piece;\n")
V['v05_declafter'] = ("    u32 piece;\n", "")
V['v06_nocidx'] = (OLD, """                    if (command == 0x67) {
                        piece = commands[gVoices[i].command + 1] << 8;
                        gMasterVolume = (piece += gFadeLevel) + (gFadeLevel << 4);
                        REG(0x04000080) = gMasterVolume;
                        gVoices[i].command += 2;
                    }""")
V['v07_blockpiece_s32'] = (OLD, V['v01_blockpiece'][1].replace("u32 piece", "s32 piece"))
V['v08_regfrompiece'] = (OLD, """                    if (command == 0x67) {
                        piece = commands[cidx + 1] << 8;
                        piece += gFadeLevel;
                        piece += gFadeLevel << 4;
                        gMasterVolume = piece;
                        REG(0x04000080) = piece;
                        gVoices[i].command = cidx + 2;
                    }""")
V['v09_fl'] = (OLD, """                    if (command == 0x67) {
                        s32 fl;
                        piece = commands[cidx + 1] << 8;
                        fl = gFadeLevel;
                        piece += fl;
                        gMasterVolume = piece + (fl << 4);
                        REG(0x04000080) = gMasterVolume;
                        gVoices[i].command = cidx + 2;
                    }""")
for k, (a, b) in V.items():
    t = base
    assert t.count(a) == 1, k
    t = t.replace(a, b)
    if k == 'v05_declafter':
        t = t.replace("    s16 *slide;\n", "    s16 *slide;\n    u32 piece;\n", 1)
    open('var/%s.c' % k, 'w').write(t)
print(len(V))
