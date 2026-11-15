/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: non-argument register r8 read before definition; review enclosing function
 */
/* func_08015128  0x08015128  thumb mode, 206 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_08015128(u32 r0) {
    u32 r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r12;
    r9 = r0;
    if ((s32)r0 > 0x7F) goto L_0801519E;
    r0 = 3;
    r1 = r9;
    r0 &= r1;
    if (r0 != 0) goto L_0801519E;
    r7 = 0x1F;
    r0 = 0x1F;
    r10 = r0;
    r6 = 0x03002A30 /* IWRAM */;
    r1 = 0xFF;
    r12 = r1;
    do {
        r0 = *(u16 *)r6;
        r5 = r10;
        r5 &= r0;
        r0 <<= 16;
        r4 = r0 >> 21;
        r4 &= r7;
        r2 = r0 >> 26;
        r2 &= r7;
        r1 = r8;
        r0 = *(u16 *)r1;
        r1 = r10;
        r1 &= r0;
        r0 <<= 16;
        r3 = r0 >> 21;
        r3 &= r7;
        r0 >>= 26;
        r0 &= r7;
        if ((s32)r5 < (s32)r1) {
            r5 += 1;
        }
        if ((s32)r4 < (s32)r3) {
            r4 += 1;
        }
        if ((s32)r2 < (s32)r0) {
            r2 += 1;
        }
        r0 = r4 << 5;
        r0 = r5 + r0;
        r1 = r2 << 10;
        r0 += r1;
        *(u16 *)r6 = (u16)r0;
        r0 = 2;
        r8 += r0;
        r6 += 2;
        r1 = 1;
        r1 = -r1;
        r12 += r1;
        r0 = r12;
    } while ((s32)r0 >= 0);
L_0801519E:
    r0 = 0xFFFFFF00;
    r0 += r9;
    if (r0 <= 0x7F) {
        r6 = 0x1F;
        r3 = 0x03002A30 /* IWRAM */;
        r1 = 0xFF;
        r12 = r1;
        do {
            r0 = *(u16 *)r3;
            r5 = 0x1F;
            r5 &= r0;
            r0 <<= 16;
            r4 = r0 >> 21;
            r4 &= r6;
            r2 = r0 >> 26;
            r2 &= r6;
            if ((s32)r5 > 0) {
                r5 -= 1;
            }
            if ((s32)r4 > 0) {
                r4 -= 1;
            }
            if ((s32)r2 > 0) {
                r2 -= 1;
            }
            r0 = r4 << 5;
            r0 = r5 + r0;
            r1 = r2 << 10;
            r0 += r1;
            *(u16 *)r3 = (u16)r0;
            r3 += 2;
            r0 = 1;
            r0 = -r0;
            r12 += r0;
            r1 = r12;
        } while ((s32)r1 >= 0);
    }
    return;
}
