/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* func_080000C0  0x080000C0  arm mode, 52 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_080000C0(void) {
    do {
        /* arm_status(1,0,9,0|0) */
        sp = *(u32 *)(pc + 0x28);
        /* arm_status(1,0,9,0|0) */
        sp = *(u32 *)(pc + 0x18);
        r1 = *(u32 *)(pc + 0x1E0);
        r0 = pc + 0x18;
        *(u32 *)r1 = r0;
        r1 = *(u32 *)(pc + 0x1D8);
        lr = pc;
        ((void (*)(void))r1)(); return; /* indirect tail jump */
    } while (1);
}
