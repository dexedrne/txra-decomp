/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: invalid stack depth
 */
/* func_08007368  0x08007368  thumb mode, 16 bytes of instructions (pools excluded)
 * callers: func_080064A4
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
u32 func_08007368(void) {
    u32 r0;
    ((void (*)(void))r0)(); return; /* indirect tail jump */
}
