/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: unresolved control transfer
 */
/* func_08002500  0x08002500  thumb mode, 624 bytes of instructions (pools excluded)
 * callers: func_0800D630
 * callees: _call_via_r2
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_08002500(u32 r0) {
    u32 r1, r2, r3, r4;
    r4 = r0;
    r0 = *(u16 *)0x03005F60 /* IWRAM */;
    r0 -= 0xF;
    r0 = (u16)r0;
    if (r0 > 2) goto L_08002514;
    goto L_0800276A;
L_08002514:
    r1 = 0x03002E54 /* IWRAM */;
    r0 = 1;
    *(u16 *)0x03002E54 /* IWRAM */ = (u16)r0;
    if (r4 != 0xB) goto L_08002520;
    goto L_0800276A;
L_08002520:
    if (r4 != 6) goto L_08002526;
    goto L_0800276A;
L_08002526:
    if (r4 != 0x2D) goto L_0800252C;
    goto L_0800276A;
L_0800252C:
    if (r4 != 7) goto L_08002532;
    goto L_0800276A;
L_08002532:
    if (r4 != 0x34) goto L_08002538;
    goto L_0800276A;
L_08002538:
    if (r4 != 0x4E) goto L_0800253E;
    goto L_0800276A;
L_0800253E:
    if (r4 != 0x68) goto L_08002544;
    goto L_0800276A;
L_08002544:
    r0 = 0x030014B0 /* IWRAM */;
    r1 = 0;
    r0 = *(s16 *)(r0 + r1);
    r2 = 0x03001E60 /* IWRAM */;
    r1 = 0x64;
    r1 *= r0;
    r1 += r2;
    r2 = 2;
    r1 = *(s16 *)(r1 + r2);
    r2 = *(u32 *)0x080200C8 /* ROM */;
    _call_via_r2(r0, r1, r2);
    if (r4 == 0x20) goto L_0800256E;
    if (r4 == 0x47) goto L_0800256E;
    if (r4 == 0x61) goto L_0800256E;
    if (r4 != 0x7B) goto L_080025A0;
L_0800256E:
    r0 = 0x030014B4 /* IWRAM */;
    r1 = *(u32 *)0x030014B4 /* IWRAM */;
    if (r1 != 0) goto L_08002578;
    goto L_0800276A;
L_08002578:
    r1 += 0xB;
    r2 = *(u32 *)0x080200C8 /* ROM */;
    r0 = 0;
    _call_via_r2(r0, r1, r2);
    goto L_0800276A;
L_080025A0:
    r0 = 0x03000B60 /* IWRAM */;
    r2 = *(u8 *)0x03000B77 /* IWRAM */;
    r2 -= 1;
    r1 = r4;
    r1 -= 0x24;
    r3 = r0;
    if (r1 <= 0x5D) goto L_080025B2;
    goto L_08002758;
L_080025B2:
    r0 = r1 << 2;
    r1 = 0x080025C4 /* ROM */;
    r0 += r1;
    r0 = *(u32 *)r0;
    switch (index) { /* jump table 0x080025C4: 94 cases -> 0800276A, 0800276A, 0800276A, 0800273C, 08002744, 0800274C, 0800273C, 08002744, 0800274C, 08002758, 08002758, 08002758, 08002758, 08002758, 08002758, 08002758, 08002758, 08002758, 08002758, 08002758, 08002758, 08002758, 08002758, 08002758 ... */ }
    r0 = 0x03000B58 /* IWRAM */;
    goto L_0800274E;
    r0 = 0x03000AC8 /* IWRAM */;
    goto L_0800274E;
    r0 = 0x03005FD4 /* IWRAM */;
L_0800274E:
    r0 = *(u32 *)r0;
    r0 <<= 5;
    r0 += r3;
    r2 = *(u8 *)(r0 + 0x17);
    r2 -= 1;
L_08002758:
    if ((s32)r2 <= 0) goto L_0800276A;
    r1 = r2;
    r1 += 0xB;
    r2 = *(u32 *)0x080200C8 /* ROM */;
    r0 = 0;
    _call_via_r2(r0, r1, r2);
L_0800276A:
    return;
}
