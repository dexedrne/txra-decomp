/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: unresolved control transfer
 */
/* func_08007B28  0x08007B28  thumb mode, 24 bytes of instructions (pools excluded)
 * callers: func_080020B8
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
u32 func_08007B28(void) {
    u32 r0;
    r0 = 0;
    *(u16 *)0x030066D0 /* IWRAM */ = (u16)r0;
    r0 = 0x3C;
    *(u32 *)0x030001C4 /* IWRAM */ = r0;
}
