/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: non-argument register sb read before definition; review enclosing function
 */
/* func_08014FF4  0x08014FF4  thumb mode, 302 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_08014FF4(u32 r0) {
    u32 r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r12;
    u32 sp00, sp04; /* stack slots */
    sp00 = r0;
    if ((s32)r0 > 0x7F) goto L_08015072;
    r0 = 3;
    r1 = sp00;
    r0 &= r1;
    if (r0 != 0) goto L_08015072;
    r2 = 0x1F;
    r8 = r2;
    r0 = 0x03002A30 /* IWRAM */;
    r12 = r0;
    r1 = 0xFF;
    r10 = r1;
    do {
        r2 = r12;
        r0 = *(u16 *)r2;
        r7 = 0x1F;
        r7 &= r0;
        r0 <<= 16;
        r6 = r0 >> 21;
        r1 = r8;
        r6 &= r1;
        r5 = r0 >> 26;
        r5 &= r1;
        r2 = r9;
        r0 = *(u16 *)r2;
        r4 = 0x1F;
        r4 &= r0;
        r0 <<= 16;
        r3 = r0 >> 21;
        r3 &= r1;
        r2 = r0 >> 26;
        r2 &= r1;
        if ((s32)r7 < (s32)r4) {
            r7 += 1;
        }
        if ((s32)r6 < (s32)r3) {
            r6 += 1;
        }
        if ((s32)r5 < (s32)r2) {
            r5 += 1;
        }
        r0 = r6 << 5;
        r0 = r7 + r0;
        r1 = r5 << 10;
        r0 += r1;
        r1 = r12;
        *(u16 *)r1 = (u16)r0;
        r2 = 2;
        r9 += r2;
        r12 += r2;
        r0 = 1;
        r0 = -r0;
        r10 += r0;
        r1 = r10;
    } while ((s32)r1 >= 0);
L_08015072:
    r0 = sp00;
    r0 -= 0xA0;
    if (r0 <= 0x1F) {
        r2 = 0;
        r10 = r2;
        r0 = 0x1F;
        r8 = r0;
        r1 = 0x1F;
        r12 = r1;
        do {
            r2 = r10;
            r0 = r2 << 1;
            r1 = 0x03002A30 /* IWRAM */;
            r0 += r1;
            sp04 = r0;
            r0 = *(u16 *)r0;
            r7 = r12;
            r7 &= r0;
            r0 <<= 16;
            r6 = r0 >> 21;
            r2 = r8;
            r6 &= r2;
            r5 = r0 >> 26;
            r5 &= r2;
            r0 = r9;
            r1 = *(u16 *)r0;
            r0 = r1 << 16;
            r3 = r0 >> 21;
            r3 &= r2;
            r2 = r0 >> 26;
            r0 = r8;
            r2 &= r0;
            r4 = r12;
            r4 = r4 & ~r1;
            r1 = r12;
            r3 = r1 - r3;
            r2 = r1 - r2;
            r4 <<= 1;
            r0 = r4;
            r4 = (s32)r0 >> 3;
            r3 <<= 2;
            r0 = r3;
            if ((s32)r3 < 0) {
                r0 = r3 + 7;
            }
            r3 = (s32)r0 >> 3;
            r0 = r2 << 1;
            r0 += r2;
            r2 = r0 << 1;
            r0 = r2;
            if ((s32)r2 < 0) {
                r0 = r2 + 7;
            }
            r2 = (s32)r0 >> 3;
            r0 = r12;
            r4 = r0 - r4;
            r3 = r0 - r3;
            r2 = r0 - r2;
            if ((s32)r7 < (s32)r4) {
                r7 += 1;
            }
            if ((s32)r6 < (s32)r3) {
                r6 += 1;
            }
            if ((s32)r5 < (s32)r2) {
                r5 += 1;
            }
            r0 = r6 << 5;
            r0 = r7 + r0;
            r1 = r5 << 10;
            r0 += r1;
            r1 = sp04;
            *(u16 *)r1 = (u16)r0;
            r2 = 2;
            r9 += r2;
            r0 = 1;
            r10 += r0;
            r1 = r10;
        } while ((s32)r1 <= 0xFF);
    }
    return;
}
