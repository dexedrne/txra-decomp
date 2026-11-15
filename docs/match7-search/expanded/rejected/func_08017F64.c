/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* func_08017F64  0x08017F64  arm mode, 604 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_08017F64(void) {
    u32 r4, r5, r6, r7, r8, r9, r10, r11, r12;
    r12 = sp;
    r3 = *(u32 *)(pc + 0x1E8);
    sp -= 0x10;
    r2 = *(u32 *)r3;
    r11 = r12 - 4;
    if (r2 == 0) { r4 = 0x06000000; }
    if (r2 == 0) { r4 += 0xA000; }
    if (r2 != 0) { r4 = 0x06000000; }
    r3 = *(u32 *)(pc + 0x1CC);
    r3 = *(s16 *)r3;
    if (r3 == 0) {
        r2 = 0x19;
        *(u32 *)(r11 + -0x2C) = r2;
        r2 += 0x2F;
        *(u32 *)(r11 + -0x30) = r2;
        r4 += 0x4E00;
        r2 = *(u32 *)(pc + 0x1AC);
        r4 += 0xC8;
        *(u32 *)(r11 + -0x34) = r2;
    }
    if (r3 == 1) {
        r2 = 0x19;
        *(u32 *)(r11 + -0x2C) = r2;
        r2 += 0x37;
        *(u32 *)(r11 + -0x30) = r2;
        r4 += 0x4B00;
        r2 = *(u32 *)(pc + 0x188);
        r4 += 8;
        *(u32 *)(r11 + -0x34) = r2;
    }
    if (r3 == 2) {
        r2 = 0x20;
        *(u32 *)(r11 + -0x2C) = r2;
        r2 += r2;
        *(u32 *)(r11 + -0x30) = r2;
        r4 += 0x5200;
        r2 = *(u32 *)(pc + 0x164);
        r4 += 0x80;
        *(u32 *)(r11 + -0x34) = r2;
    }
    if (r3 == 3) {
        r2 = 0x1D;
        *(u32 *)(r11 + -0x2C) = r2;
        r2 += 0x25;
        *(u32 *)(r11 + -0x30) = r2;
        r4 += 0x5100;
        r2 = *(u32 *)(pc + 0x140);
        r4 += 0x94;
        *(u32 *)(r11 + -0x34) = r2;
    }
    if (r3 == 4) {
        r2 = 0x22;
        *(u32 *)(r11 + -0x2C) = r2;
        r2 += 0xE;
        *(u32 *)(r11 + -0x30) = r2;
        r4 += 0x5A00;
        r2 = *(u32 *)(pc + 0x11C);
        r4 += 2;
        *(u32 *)(r11 + -0x34) = r2;
    }
    if (r3 == 5) {
        r3 = 0x20;
        *(u32 *)(r11 + -0x2C) = r3;
        r2 = 0x40;
        *(u32 *)(r11 + -0x30) = r2;
        r4 += 0x5200;
        r3 = *(u32 *)(pc + 0xF8);
        r4 += 0x82;
        *(u32 *)(r11 + -0x34) = r3;
    }
    r3 = *(u32 *)(r11 + -0x30);
    r2 = 0;
    if ((s32)r2 < (s32)r3) {
        do {
            r3 = *(u32 *)(r11 + -0x2C);
            r10 = 0;
            r3 = r2 + 1;
            *(u32 *)(r11 + -0x38) = r3;
            if ((s32)r10 < (s32)r3) {
                r3 = r2 << 4 - r2;
                r7 = r3 << 4;
                r12 = r4 + r7;
                r3 = r2 + (r2 << 2);
                r3 += (r3 << 2);
                r9 = r3 << 3;
                r2 = *(u32 *)(r11 + -0x34);
                r8 = r10;
                r6 = r2 + r9;
                r5 = r2;
                do {
                    r0 = *(u16 *)(r5 + r9);
                    if (r0 == 0) goto L_08018114;
                    if ((r0 & 0xFF) == 0) { r1 = *(u8 *)r12; }
                    if ((r0 & 0xFF) == 0) { r3 = r1 + r0; }
                    if ((r0 & 0xFF) == 0) { *(u16 *)r12 = (u16)r3; }
                    if ((r0 & 0xFF) == 0) goto L_08018114;
                    if ((r0 & 0xFF00) != 0) goto L_08018110;
                    r3 = *(u16 *)r12;
                    r1 = r3 & 0xFF00;
                    r2 = r1 + r0;
                    *(u16 *)r12 = (u16)r2;
                    goto L_08018114;
L_08018110:
                    *(u16 *)r12 = (u16)r0;
L_08018114:
                    lr = 2;
                    r0 = *(u16 *)(r6 + lr);
                    if (r0 == 0) goto L_08018188;
                    if ((r0 & 0xFF) == 0) { r1 = *(u8 *)(r12 + lr); }
                    if ((r0 & 0xFF) == 0) { r3 = r1 + r0; }
                    if ((r0 & 0xFF) == 0) { *(u16 *)(r12 + lr) = (u16)r3; }
                    if ((r0 & 0xFF) == 0) goto L_08018188;
                    if ((r0 & 0xFF00) != 0) goto L_0801817C;
                    r3 = r8 + r4;
                    r3 = r7 + r3;
                    r2 = *(u16 *)(r3 + lr);
                    r1 = r2 & 0xFF00;
                    r1 += r0;
                    *(u16 *)(r3 + lr) = (u16)r1;
                    goto L_08018188;
L_0801817C:
                    r3 = r8 + r4;
                    r3 = r7 + r3;
                    *(u16 *)(r3 + lr) = (u16)r0;
L_08018188:
                    r12 += 4;
                    r6 += 4;
                    r5 += 4;
                    r8 += 4;
                    r3 = *(u32 *)(r11 + -0x2C);
                    r10 += 2;
                } while ((s32)r10 < (s32)r3);
            }
            r2 = *(u32 *)(r11 + -0x38);
            r3 = *(u32 *)(r11 + -0x30);
        } while ((s32)r2 < (s32)r3);
    }
    /* ldmdb r11, {r4, r5, r6, r7, r8, r9, r10, r11, sp, lr} */
    return;
}
