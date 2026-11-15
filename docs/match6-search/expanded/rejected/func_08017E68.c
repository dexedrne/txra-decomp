/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* func_08017E68  0x08017E68  arm mode, 252 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_08017E68(void) {
    u32 r4, r5, r6, r7, r11, r12;
    r12 = sp;
    r0 = 0xFF;
    r2 = *(u32 *)(pc + 0x98);
    r3 = 0;
    r7 = *(u32 *)(pc + 0x94);
    r11 = r12 - 4;
    *(u32 *)r2 = r3;
    do {
        r1 = r0 << 2;
        r2 = *(u32 *)(r7 + r1);
        r6 = r0 - 1;
        if (r2 != 0) {
            r3 = 0;
            *(u32 *)(r7 + r1) = r3;
            r5 = *(u32 *)(pc + 0x70);
            r4 = *(u32 *)(pc + 0x64);
            do {
                *(u32 *)r5 = r2;
                r3 = *(u32 *)r4;
                r2 = *(u16 *)(r2 + 0x1A);
                r3 += 1;
                *(u32 *)r4 = r3;
                if (r2 != 0) goto L_08017EDC;
                r3 = *(u32 *)(pc + 0x50);
                r12 = *(u32 *)r3;
                lr = pc;
                ((void (*)(void))r12)(); return; /* indirect tail jump */
                goto L_08017F3C;
L_08017EDC:
                if (r2 != 1) goto L_08017EF8;
                r3 = *(u32 *)(pc + 0x38);
                r12 = *(u32 *)r3;
                lr = pc;
                ((void (*)(void))r12)(); return; /* indirect tail jump */
                goto L_08017F3C;
L_08017EF8:
                if (r2 != 2) goto L_08017F2C;
                r3 = *(u32 *)(pc + 0x20);
                r12 = *(u32 *)r3;
                lr = pc;
                ((void (*)(void))r12)(); return; /* indirect tail jump */
                goto L_08017F3C;
L_08017F2C:
                r3 = *(u32 *)(pc + 0x20);
                r12 = *(u32 *)r3;
                lr = pc;
                ((void (*)(void))r12)(); return; /* indirect tail jump */
L_08017F3C:
                r3 = *(u32 *)r5;
                r2 = *(u32 *)(r3 + 0x1C);
            } while (r2 != 0);
        }
        r0 = r6 - 0;
        goto L_08017F58;
L_08017F58:
    } while ((s32)r0 >= 0);
    /* ldmdb r11, {r4, r5, r6, r7, r11, sp, lr} */
    return;
}
