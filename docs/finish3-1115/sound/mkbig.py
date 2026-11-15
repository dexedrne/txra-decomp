#!/usr/bin/env python3
"""Build the choice-point template big.tpl from the finish3 near-miss source (alternatives found in this round)."""
t = open('../../near-misses/finish3-1115-sound/func_080064A4.c').read()
def rep(old, new, cnt=1):
    global t
    assert t.count(old) == cnt, (old[:70], t.count(old))
    t = t.replace(old, new)
def opts(*o):
    return '@'.join(x.replace('\n', '\\n') for x in o)
# slide pointer / update / val forms (TICK_TONE)
head, body = t.split("void func_080064A4(void) {\n")
a = head.index('#define TICK_TONE'); b = head.index('#define ARP_DIRECT')
m = head[a:b]
m = m.replace(' slide = inst->slide;', ' SVAR = inst->slide;').replace('slide != 0', 'SVAR != 0').replace('slide[', 'SVAR[')
U0 = "p = gVoices[i].pitch; p += SVAR[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;"
assert m.count(U0) == 1
m = m.replace(U0, "«up@" + opts(U0, "{ s32 p = gVoices[i].pitch; p += SVAR[gVoices[i].pitch_cursor]; gVoices[i].pitch = p; }",
    "p = gVoices[i].pitch + SVAR[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;", "gVoices[i].pitch += SVAR[gVoices[i].pitch_cursor];") + "»")
V0 = """                val = gVoices[i].pitch;                                                              \\
                val |= inst->flags << 8;                                                             \\
                REG(frq) = val;                                                                      \\"""
assert m.count(V0) == 1
m = m.replace(V0, "                «vf@" + opts("val = gVoices[i].pitch; val |= inst->flags << 8; REG(frq) = val;",
    "val = (inst->flags << 8) | gVoices[i].pitch; REG(frq) = val;", "val = gVoices[i].pitch | (inst->flags << 8); REG(frq) = val;") + "» \\")
head = head[:a] + m + head[b:]
head = head.replace("typedef unsigned char u8;", "«sv@/*SUB:SVAR=slide*/@/*SUB:SVAR=seq*/»\ntypedef unsigned char u8;", 1)
t = head + "void func_080064A4(void) {\n" + body
# p declaration position
rep("    s32 i;\n    s32 p;\n    s32 j;\n", "    s32 i;\n    «pd1@s32 p;\\n@»    s32 j;\n")
rep("    s32 cidx;\n    s16 *slide;\n", "    s32 cidx;\n    s16 *slide;\n    «pd1@@s32 p;\\n»")
# fade level
rep("(gFadeLevel + (gFadeLevel << 4))", "«f17@(gFadeLevel + (gFadeLevel << 4))@(gFadeLevel | (gFadeLevel << 4))@(gFadeLevel + gFadeLevel * 16)»")
# tempo
rep("    gTempoCounter = gTempo + gTempoCounter;\n", "    «tmp@gTempoCounter = gTempo + gTempoCounter;@gTempoCounter += gTempo;@gTempoCounter = gTempoCounter + gTempo;»\n")
rep("        u16 *events16;\n        s16 stop;\n        u16 freq;\n", "        «d1@u16 *events16;\\n@»        «st@s16@s32@u16@u8@s8» stop;\n        «d1@@u16 *events16;\\n»«bv@@        u16 val;\\n»        u16 freq;\n")
# effect loop forms
rep("        events16 = gEffects[i].events;\n", "        events16 = «eev@gEffects[i].events@effect->events»;\n")
rep("            if (gEffects[i].delay != 0) {\n                if (--gEffects[i].delay != 0)", "            if («edl@gEffects[i].delay@effect->delay» != 0) {\n                if (--«edl@gEffects[i].delay@effect->delay» != 0)")
rep("            gEffects[i].cursor += 5;\n", "            «ecu@gEffects[i].cursor@effect->cursor» += 5;\n")
rep("                gEffects[i].events = 0;\n", "                «eclr@gEffects[i].events@effect->events» = 0;\n")
rep("                val = freq = 0;\n", "                «effz@val = freq = 0;@freq = val = 0;@val = 0;\\n                freq = 0;»\n")
rep("    for (i = 0; i <= 3; effect++, i++) {\n", "    for (i = 0; i <= 3; «einc@effect++, i++@i++, effect++») {\n")
# scale/clear forms
rep("""            for (j = 175; j >= 0; j--) {
                *buffer = (*buffer * gain) >> 8;
                buffer++;
            }""", "            «sl@" + opts("""for (j = 175; j >= 0; j--) {
                *buffer = (*buffer * gain) >> 8;
                buffer++;
            }""", """j = 175;
            do {
                *buffer = (*buffer * gain) >> 8;
                buffer++;
            } while (--j >= 0);""", """for (j = 175; j >= 0; j--, buffer++)
                *buffer = (*buffer * gain) >> 8;""") + "»")
rep("""                buffer = gMixBuffer;
                buffer += idx * 176;""", "                «sb@buffer = gMixBuffer;\\n                buffer += idx * 176;@buffer = gMixBuffer + idx * 176;@buffer = &gMixBuffer[idx * 176];»")
rep("""            buffer = gMixBuffer;
            i = 175;
            buffer += idx * 176 + i;""", "            «cb@" + opts("""buffer = gMixBuffer;
            i = 175;
            buffer += idx * 176 + i;""", """buffer = &gMixBuffer[idx * 176] + 175;
            i = 175;""", """i = 175;
            buffer = &gMixBuffer[idx * 176] + i;""", """buffer = gMixBuffer;
            buffer += idx * 176;
            i = 175;
            buffer += i;""") + "»")
# noise section forms
rep("""                        if (seq != 0 && --gVoices[3].pitch_delay == 0) {
                            s32 index;

                            index = gVoices[3].pitch_cursor;""", """                        if (seq != 0 && --gVoices[3].pitch_delay == 0) {
                            «ni1@s32 index;\\n\\n@»                            index = gVoices[3].pitch_cursor;""")
rep("""                        if (seq != 0 && --gVoices[i].volume_delay == 0) {
                            s32 index;

                            index = gVoices[i].volume_cursor;""", """                        if (seq != 0 && --gVoices[i].volume_delay == 0) {
                            «ni2@s32 index;\\n\\n@»                            index = gVoices[i].volume_cursor;""")
rep("""                                {
                                    s32 t = seq[gVoices[3].pitch_cursor];
                                    val = (inst->flags << 8) | t;
                                }""", "                                «c3c@" + opts("""{
                                    s32 t = seq[gVoices[3].pitch_cursor];
                                    val = (inst->flags << 8) | t;
                                }""", "val = (inst->flags << 8) | (u16)seq[gVoices[3].pitch_cursor];", """{
                                    s32 t = seq[gVoices[3].pitch_cursor];
                                    val = t | (inst->flags << 8);
                                }""") + "»")
open('big.tpl', 'w').write(t)
print('ok')
