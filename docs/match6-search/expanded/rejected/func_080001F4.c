/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* func_080001F4  0x080001F4  arm mode, 36 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_080001F4(u32 r0, u32 r1, u32 r2, u32 r3) {
    /* arm_status(0,0,3,0) */
    r3 = r3 & ~0xDF;
    r3 |= 0x92;
    /* arm_status(1,0,9,3|0) */
    *(u16 *)r3 = (u16)r1;
    /* arm_status(1,1,9,0|0) */
    return;
}
