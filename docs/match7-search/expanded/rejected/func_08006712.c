/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: call without saved LR or outside ROM
 */
/* func_08006712  0x08006712  thumb mode, 46 bytes of instructions (pools excluded)
 * callers: func_0800735C
 * callees: func_0800735C
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_08006712(void) {
    u32 r0, r1, r2, r3, r4, r10, r12;
    u32 sp58, sp5C; /* stack slots */
    r2 = r10;
    r1 = r2 << 3;
    r0 = r1 + r2;
    r2 = r0 << 3;
    r3 = r12;
    r0 = r2 + r3;
    r0 = *(u32 *)r0;
    r4 = r10;
    r4 += 1;
    sp58 = r4;
    sp5C = r1;
    if (r0 != 1) {
        func_0800735C();
    }
    r0 = r12;
    r0 += 0x20;
    r0 = r2 + r0;
    r0 = *(u32 *)r0;
    if (r0 != 0) { func_08006740(); return; /* tail call */ }
    func_0800735C();
}
