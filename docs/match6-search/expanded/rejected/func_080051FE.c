/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: invalid stack depth
 */
/* func_080051FE  0x080051FE  thumb mode, 16 bytes of instructions (pools excluded)
 * callers: func_0800421C
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_080051FE(void) {
    u32 r0;
    ((void (*)(void))r0)(); return; /* indirect tail jump */
}
