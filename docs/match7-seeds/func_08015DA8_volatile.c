void func_08015DA8(void) {
    u32 r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r12;
    r7 = 0;
    r0 = 0x030061F0 /* IWRAM */;
    r12 = r0;
    r1 = 0x030067E4 /* IWRAM */;
    r9 = r1;
    r6 = 0x040000D4 /* REG_DMA3SAD */;
    r5 = r12;
    r4 = 0;
    r0 = 4;
    r0 += r12;
    r8 = r0;
L_08015DC6:
    r3 = *(u32 *)r5;
    if (r3 != 0) goto L_08015DE0;
    r1 = r12;
    *(u32 *)r1 = r3;
    goto L_08015E08;
L_08015DE0:
    r1 = r8;
    r0 = r4 + r1;
    r2 = *(u32 *)r0;
    r0 = r12;
    r0 += 8;
    r0 = r4 + r0;
    r1 = *(u32 *)r0;
    *(vu32 *)r6 = r3;
    *(vu32 *)(r6 + 4) = r2;
    r1 >>= 2;
    r0 = 0x84000000;
    r1 |= r0;
    *(vu32 *)(r6 + 8) = r1;
    r0 = *(vu32 *)(r6 + 8);
    r5 += 0xC;
    r4 += 0xC;
    r7 += 1;
    if (r7 <= 0x60) goto L_08015DC6;
L_08015E08:
    r0 = 0;
    r1 = r12;
    *(u32 *)r1 = r0;
    r1 = r9;
    *(u32 *)r1 = r0;
    return;
}
