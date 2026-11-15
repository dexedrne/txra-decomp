/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: call without saved LR or outside ROM
 */
/* func_08006740  0x08006740  thumb mode, 54 bytes of instructions (pools excluded)
 * callers: func_08006776
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_08006740(void) {
    u32 r0, r1, r2, r3, r5, r6, r7, r9, r10;
    u32 sp28, sp2C, sp30, sp34, sp44, sp48, sp4C, sp50, sp5C; /* stack slots */
    r5 = 0x03007770 /* IWRAM */;
    r9 = r5;
    r6 = sp5C;
    r6 += r10;
    sp28 = r6;
    r7 = r6 << 3;
    sp2C = r7;
    r0 = r9;
    r0 += 0x10;
    r0 = r7 + r0;
    sp30 = r0;
    r0 = 0x03007794 /* IWRAM */;
    r0 = r7 + r0;
    sp34 = r0;
    r0 = r9;
    r0 += 0x14;
    r0 = r7 + r0;
    sp44 = r0;
    r1 = 0x03007788 /* IWRAM */;
    r1 = r7 + r1;
    sp48 = r1;
    r2 = 0x030077A0 /* IWRAM */;
    r2 = r7 + r2;
    sp4C = r2;
    r3 = 0x030077AC /* IWRAM */;
    r3 = r7 + r3;
    sp50 = r3;
}
