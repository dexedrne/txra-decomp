/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* __udivsi3  0x0800027C  arm mode, 68 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
u32 func_0800027C(u32 r0, u32 r1) {
    if (r1 == 0) return r0;
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
    r0 = r2;
    return r0;
}
