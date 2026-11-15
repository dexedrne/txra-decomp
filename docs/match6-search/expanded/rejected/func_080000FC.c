/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* func_080000FC  0x080000FC  arm mode, 248 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_080000FC(u32 r0) {
    r3 = 0x04000200 /* REG_IE */;
    r2 = *(vu32 *)0x04000200 /* REG_IE */;
    r1 = r2 << 16;
    r1 = r1 >> 16;
    /* arm_status(0,1,0,0) */
    r1 = r2 & (r2 >> 16);
    r2 = 0;
    r0 = r1 & 8;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 1;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 2;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 4;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 0x10;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 0x20;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 0x40;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 0x80;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 0x100;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 0x200;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 0x400;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 0x800;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 0x1000;
    if (r0 != 0) goto L_080001C0;
    r2 += 4;
    r0 = r1 & 0x2000;
L_080001C0:
    *(u16 *)(r3 + 2) = (u16)r0;
    r1 = 8;
    *(u16 *)r3 = (u16)r1;
    /* arm_status(0,0,3,0) */
    r3 = r3 & ~0xDF;
    r3 |= 0x1F;
    /* arm_status(1,0,9,3|0) */
    r1 = *(u32 *)(pc + 0xE4);
    r1 += r2;
    r0 = *(u32 *)r1;
    lr = pc + 0;
    ((void (*)(void))r0)(); return; /* indirect tail jump */
}
