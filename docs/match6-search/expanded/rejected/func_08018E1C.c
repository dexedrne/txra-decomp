/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: runtime helper
 */
/* memcpy  0x08018E1C  thumb mode, 94 bytes of instructions (pools excluded)
 * callers: func_0800B908
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
u32 func_08018E1C(u32 r0, u32 r1, u32 r2) {
    u32 r3, r4, r5;
    r5 = r0;
    r4 = r5;
    r3 = r1;
    if (r2 <= 0xF) goto L_08018E5C;
    r0 = r3;
    r0 |= r5;
    r1 = 3;
    r0 &= r1;
    if (r0 != 0) goto L_08018E5C;
    r1 = r5;
    do {
        r0 = *(u32 *)(r3 + 0); r3 += 4;
        *(u32 *)(r1 + 0) = r0; r1 += 4;
        r0 = *(u32 *)(r3 + 0); r3 += 4;
        *(u32 *)(r1 + 0) = r0; r1 += 4;
        r0 = *(u32 *)(r3 + 0); r3 += 4;
        *(u32 *)(r1 + 0) = r0; r1 += 4;
        r0 = *(u32 *)(r3 + 0); r3 += 4;
        *(u32 *)(r1 + 0) = r0; r1 += 4;
        r2 -= 0x10;
    } while (r2 > 0xF);
    if (r2 > 3) {
        do {
            r0 = *(u32 *)(r3 + 0); r3 += 4;
            *(u32 *)(r1 + 0) = r0; r1 += 4;
            r2 -= 4;
        } while (r2 > 3);
    }
    r4 = r1;
L_08018E5C:
    r2 -= 1;
    r0 = 1;
    r0 = -r0;
    if (r2 != r0) {
        r1 = r0;
        do {
            r0 = *(u8 *)r3;
            *(u8 *)r4 = (u8)r0;
            r3 += 1;
            r4 += 1;
            r2 -= 1;
        } while (r2 != r1);
    }
    r0 = r5;
    return r0;
}
