/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: unresolved control transfer
 */
/* func_080157A0  0x080157A0  thumb mode, 1162 bytes of instructions (pools excluded)
 * callers: func_08014458, func_080154AC
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
u32 func_080157A0(u32 r0) {
    u32 r1, r2;
    r0 <<= 24;
    r2 = (u8)r0;
    r1 = 0xBF000000;
    r0 += r1;
    r0 >>= 24;
    if (r0 > 0x19) goto L_080157B4;
    r0 += 1;
    goto L_080157D2;
L_080157B4:
    r0 = r2;
    r0 -= 0x61;
    r0 = (u8)r0;
    if (r0 > 0x19) goto L_080157C4;
    r0 += 1;
    goto L_080157D2;
L_080157C4:
    r0 = r2;
    r0 -= 0x30;
    r0 = (u8)r0;
    if (r0 > 9) goto L_080157D8;
    r0 += 0x20;
L_080157D2:
    r0 <<= 24;
    r2 = (u8)r0;
    goto L_08015C26;
L_080157D8:
    r0 = r2;
    r0 -= 0x20;
    if (r0 <= 0xDF) goto L_080157E2;
    goto L_08015C26;
L_080157E2:
    r0 <<= 2;
    r1 = 0x080157F0 /* ROM */;
    r0 += r1;
    r0 = *(u32 *)r0;
    switch (index) { /* jump table 0x080157F0: 224 cases -> 08015B70, 08015B78, 08015C26, 08015B9C, 08015B94, 08015B90, 08015B98, 08015B7C, 08015C26, 08015C26, 08015C26, 08015C26, 08015B88, 08015B80, 08015B84, 08015C26, 08015C26, 08015C26, 08015C26, 08015C26, 08015C26, 08015C26, 08015C26, 08015C26 ... */ }
    r2 = 0;
    goto L_08015C26;
    r2 = 0x1B;
    goto L_08015C26;
    r2 = 0x1C;
    goto L_08015C26;
    r2 = 0x1D;
    goto L_08015C26;
    r2 = 0x1E;
    goto L_08015C26;
    r2 = 0x1F;
    goto L_08015C26;
    r2 = 0x2A;
    goto L_08015C26;
    r2 = 0x2B;
    goto L_08015C26;
    r2 = 0x2E;
    goto L_08015C26;
    r2 = 0x5A;
    goto L_08015C26;
    r2 = 0x2F;
    goto L_08015C26;
    r2 = 0x5F;
    goto L_08015C26;
    r2 = 0x51;
    goto L_08015C26;
    r2 = 0x52;
    goto L_08015C26;
    r2 = 0x2C;
    goto L_08015C26;
    r2 = 0x2D;
    goto L_08015C26;
    r2 = 0x30;
    goto L_08015C26;
    r2 = 0x31;
    goto L_08015C26;
    r2 = 0x32;
    goto L_08015C26;
    r2 = 0x33;
    goto L_08015C26;
    r2 = 0x34;
    goto L_08015C26;
    r2 = 0x35;
    goto L_08015C26;
    r2 = 0x36;
    goto L_08015C26;
    r2 = 0x37;
    goto L_08015C26;
    r2 = 0x38;
    goto L_08015C26;
    r2 = 0x39;
    goto L_08015C26;
    r2 = 0x3A;
    goto L_08015C26;
    r2 = 0x3B;
    goto L_08015C26;
    r2 = 0x3C;
    goto L_08015C26;
    r2 = 0x3D;
    goto L_08015C26;
    r2 = 0x3E;
    goto L_08015C26;
    r2 = 0x3F;
    goto L_08015C26;
    r2 = 0x40;
    goto L_08015C26;
    r2 = 0x41;
    goto L_08015C26;
    r2 = 0x42;
    goto L_08015C26;
    r2 = 0x43;
    goto L_08015C26;
    r2 = 0x44;
    goto L_08015C26;
    r2 = 0x45;
    goto L_08015C26;
    r2 = 0x46;
    goto L_08015C26;
    r2 = 0x47;
    goto L_08015C26;
    r2 = 0x48;
    goto L_08015C26;
    r2 = 0x4B;
    goto L_08015C26;
    r2 = 0x4C;
    goto L_08015C26;
    r2 = 0x4D;
    goto L_08015C26;
    r2 = 0x4E;
    goto L_08015C26;
    r2 = 0x4F;
L_08015C26:
    r0 = r2;
    return r0;
}
