/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* func_080016E0  0x080016E0  arm mode, 452 bytes of instructions (pools excluded)
 * callers: func_08001218
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_080016E0(u32 r0, u32 r1, u32 r2, u32 r3) {
    u32 r4, r5, r6, r7, r8, r9, r10, r11, r12;
    u32 sp0C, sp10; /* stack slots */
    lr = *(u32 *)(pc + 0x1BC);
    r9 = r11;
    r7 += (r8 << 16);
L_080016F8:
    r5 = sp0C;
    if ((s32)r5 >= 0xA0) goto L_08001894;
    r5 += 1;
    sp0C = r5;
    if (r5 >= 0xA0) goto L_08001878;
    lr = sp10;
    r8 = r6 << 16;
    r8 = (s32)r8 >> 23;
    r10 = (s32)r6 >> 23;
    if ((s32)r8 < (s32)-(0x88)) { r8 += 0x200; }
    if ((s32)r10 < (s32)-(0x88)) { r10 += 0x200; }
    r11 = r10 - r8;
    r11 = r11 << 1;
    r11 = *(u16 *)(lr + r11);
    r5 = 0xFF;
    r3 = r5 & (r2 >> 8);
    r5 &= (r0 >> 8);
    r3 -= r5;
    r3 = r11 * r3;
    r3 += 0x40;
    r3 = (s32)r3 >> 7;
    r1 = r2 >> 24;
    r1 -= (r0 >> 24);
    r1 = r11 * r1;
    r1 += 0x40;
    r1 = (s32)r1 >> 7;
    r3 += (r1 << 16);
    r1 = r0;
    if (r8 < 0xF0) goto L_0800178C;
    if ((s32)r8 >= 0xF0) goto L_08001878;
    r11 = r3 * r8;
    r1 -= r11;
    r8 = 0;
L_0800178C:
    r10 += 1;
    if ((s32)r10 > 0xF0) { r10 = 0xF0; }
    r10 -= r8;
    if ((s32)r10 <= 0) goto L_08001878;
    r8 = r4 + r8;
    if ((r8 & 1) != 0) {
        /* ldrh r5, [r8, -#1] */
        r5 &= 0xFF;
        r7 = r1 >> 24;
        r11 = r1 << 16;
        r11 = r12 + (r11 >> 24);
        r11 = *(u8 *)(r11 + r7 << 8);
        r5 |= (r11 << 8);
        /* strh r5, [r8, #2] */
        r10 -= 1;
        r1 += r3;
    }
    r10 = r10 >> 1;
    if (FLAGS_CS /* from 080017D4 */) {
        r8 += (r10 << 1);
        r5 = *(u16 *)r8;
        r5 &= 0xFF00;
        r7 = r2 >> 24;
        r11 = r2 << 16;
        r11 = r12 + (r11 >> 24);
        r11 = *(u8 *)(r11 + r7 << 8);
        r5 |= r11;
        *(u16 *)r8 = (u16)r5;
        r8 -= (r10 << 1);
    }
    if ((s32)r10 <= 0) goto L_08001878;
L_08001808:
    r7 = r1 >> 24;
    r11 = r1 << 16;
    r11 = r12 + (r11 >> 24);
    r5 = *(u8 *)(r11 + r7 << 8);
    r1 += r3;
    r7 = r1 >> 24;
    r11 = r1 << 16;
    r11 = r12 + (r11 >> 24);
    r11 = *(u8 *)(r11 + r7 << 8);
    r1 += r3;
    r5 += (r11 << 8);
    if (r10 != 0) { /* strhne r5, [r8, #2] */ }
    r10 -= 1;
    if ((s32)r10 <= 0) goto L_08001878;
    r7 = r1 >> 24;
    r11 = r1 << 16;
    r11 = r12 + (r11 >> 24);
    r5 = *(u8 *)(r11 + r7 << 8);
    r1 += r3;
    r7 = r1 >> 24;
    r11 = r1 << 16;
    r11 = r12 + (r11 >> 24);
    r11 = *(u8 *)(r11 + r7 << 8);
    r1 += r3;
    r5 += (r11 << 8);
    /* strh r5, [r8, #2] */
    r10 -= 1;
    if ((s32)r10 > 0) goto L_08001808;
L_08001878:
    r1 = *(u32 *)(sp + 0); r3 = *(u32 *)(sp + 4); r7 = *(u32 *)(sp + 8); sp += 12;
    r4 += 0xF0;
    r6 += r7;
    r0 += r1;
    r2 += r3;
    r9 -= 1;
    if ((s32)r9 > 0) goto L_080016F8;
L_08001894:
    return;
}
