/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* __divsi3  0x08000218  arm mode, 100 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
u32 func_08000218(u32 r0, u32 r1) {
    u32 r4;
    if (r1 == 0) return r0;
    /* str r4, [sp, -#4]! */
    r4 = r0 & 0x80000000;
    if ((s32)r4 < 0) { r0 = -r0; }
    r4 ^= ((s32)r1 >> 32);
    if (FLAGS_CS /* from 0800022C */) { r1 = -r1; }
    r3 = 1;
    do {
        if (r1 < r0) { r1 = r1 << 1; }
        if (r1 < r0) { r3 = r3 << 1; }
    } while (r1 < r0);
    r2 = 0;
    do {
        if (r0 >= r1) { r0 -= r1; }
        if (r0 >= r1) { r2 += r3; }
        r3 = r3 >> 1;
        if (r3 != 0) { r1 = r1 >> 1; }
    } while (r3 != 0);
    if ((s32)(r4 & r4) < 0) { r0 = -r2; }
    if ((s32)(r4 & r4) >= 0) { r0 = r2; }
    /* ldr r4, [sp], #4 */
    return r0;
}
