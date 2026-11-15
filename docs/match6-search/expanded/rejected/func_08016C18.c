/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* func_08016C18  0x08016C18  arm mode, 400 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_08016C18(void) {
    u32 r4, r5, r6, r7, r8, r9, r10, r11, r12;
    r12 = sp;
    r3 = *(u32 *)(pc + 0x154);
    sp -= 0x18;
    r2 = *(u32 *)r3;
    r11 = r12 - 4;
    r1 = r2 - 0x1E;
    r1 &= 0x1F;
    r2 -= 4;
    r2 &= 0x1F;
    *(u32 *)(r11 + -0x38) = r2;
    do {
        r3 = r1 + (r1 << 1);
        r3 = r3 << 3 - r3;
        r3 = r3 << 5;
        r8 = r3 + 0x2000000;
        r8 += 0x14000;
        r3 = *(u32 *)(r8 + 0xC);
        r2 = 0;
        *(u32 *)(r11 + -0x3C) = r2;
        r1 += 1;
        *(u32 *)(r11 + -0x40) = r1;
        if (r3 != 1) goto L_08016D68;
        r9 = *(u32 *)(pc + 0x104);
        r10 = *(u32 *)(pc + 0x104);
L_08016C7C:
        r12 = *(u32 *)r8;
        r3 = *(u32 *)(pc + 0x100);
        r2 = *(u32 *)r9;
        r1 = *(u32 *)r3;
        r12 -= r2;
        r5 = r1 * r12;
        r4 = *(u32 *)(r8 + 8);
        r3 = *(u32 *)(r9 + 8);
        r4 -= r3;
        r0 = r1 * r4;
        r3 = *(u32 *)(pc + 0xE0);
        r2 = *(u32 *)r3;
        r7 = r2 * r4;
        /* long multiply */
        r3 = *(u32 *)(r8 + 4);
        r0 = *(u32 *)(r9 + 4);
        r2 = *(u32 *)(pc + 0xCC);
        r4 = -r3;
        r1 = *(u32 *)r2;
        r4 -= r0;
        r0 = r1 * r4;
        r12 = (s32)r12 >> 12;
        lr = r1 * r12;
        r3 = *(u32 *)(pc + 0xB4);
        r2 = *(u32 *)r3;
        r1 = r2 * r12;
        /* long multiply */
        r3 = *(u32 *)(r10 + 8);
        r12 = *(u32 *)r10;
        r0 -= r1;
        lr = *(u32 *)(r10 + 4);
        r4 = r3 + ((s32)r0 >> 12);
        *(u32 *)(r8 + 0x18) = r4;
        r5 -= r7;
        r2 = *(u32 *)(pc + 0x8C);
        r4 = (s32)r4 >> 1;
        r3 = r4 + 0x10000;
        r1 = *(u32 *)(r2 + r3 << 2);
        r12 += ((s32)r5 >> 12);
        r2 = r12 << 3;
        r3 = r1 * r2;
        r4 = lr + ((s32)r6 >> 12);
        r4 = r4 << 3;
        r2 = r1 * r4;
        r3 = (s32)r3 >> 16;
        r1 = *(u32 *)(r11 + -0x3C);
        r3 += 0x3C;
        r1 += 1;
        *(u32 *)(r11 + -0x3C) = r1;
        r2 = (s32)r2 >> 15;
        *(u32 *)(r8 + 0x10) = r3;
        r2 += 0x50;
        *(u32 *)(r8 + 0x14) = r2;
        r8 += 0x1C;
        if ((s32)r1 > 0x17) goto L_08016D68;
        r3 = *(u32 *)(r8 + 0xC);
        if (r3 == 1) goto L_08016C7C;
L_08016D68:
        r2 = *(u32 *)(r11 + -0x40);
        r3 = *(u32 *)(r11 + -0x38);
        r1 = r2 & 0x1F;
        goto L_08016D9C;
L_08016D9C:
    } while (r1 != r3);
    /* ldmdb r11, {r4, r5, r6, r7, r8, r9, r10, r11, sp, lr} */
    return;
}
