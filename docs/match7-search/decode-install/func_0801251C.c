
void func_0801251C(u32 r0, u32 r1, u32 r2) {
    u32 r3;
    u32 r4;
    u32 r5;
    u32 r6;
    u32 r7;
    u32 r8;
    u32 r12;
    r12 = r0;
    r6 = r1;
    r1 = *(u8 *)(r0 + 5);
    r0 = r1 << 8;
    r3 = r12;
    r3 = *(u8 *)(r3 + 4);
    r0 |= r3;
    r0 += 3;
    r2 -= 1;
    r7 = 0xC0;
    r1 = 0x3F;
    r8 = r1;
    r4 = r2 + r6;
    r3 = r12;
    r2 = r0 + r3;
while (1) {
    r5 = *(u8 *)r2;
    if ((r5 & r7) != 0xC0) goto L_08012574;
    r3 = r5;
    r0 = r8;
    r3 &= r0;
    r2 -= 1;
    r1 = *(u8 *)r2;
    r0 = r1 << 8;
    r2 -= 1;
    r1 = *(u8 *)r2;
    r0 |= r1;
    r2 -= 1;
    r1 = r6 + r0;
    if (r3 == 0) goto L_08012574;
    r0 = r3;
    do {
        r3 = *(u8 *)r1;
        *(u8 *)r4 = (u8)r3;
        r4 -= 1;
        r1 += 1;
        r0 -= 1;
    }
 while (r0 != 0);
L_08012574:
    r0 = r5;
    r0 &= r7;
    if (r0 != 0x80) goto L_080125AA;
    r3 = r5;
    r0 = r8;
    r3 &= r0;
    r2 -= 1;
    r1 = *(u8 *)r2;
    r0 = r1 << 8;
    r2 -= 1;
    r1 = *(u8 *)r2;
    r0 |= r1;
    r2 -= 1;
    r1 = r0;
 r0 = r6 + r1;
    r0 += r3;
    r1 = r0 - 1;
    if (r3 == 0) goto L_080125AA;
    r0 = r3;
    do {
        r3 = *(u8 *)r1;
        *(u8 *)r4 = (u8)r3;
        r4 -= 1;
        r1 -= 1;
        r0 -= 1;
    }
 while (r0 != 0);
L_080125AA:
    r0 = r5;
    r0 &= r7;
    if (r0 != 0x40) goto L_080125CE;
    r3 = r5;
    r0 = r8;
    r3 &= r0;
    r2 -= 1;
    r1 = *(u8 *)r2;
    r2 -= 1;
    if (r3 == 0) goto L_080125CE;
    r0 = r3;
    do {
        *(u8 *)r4 = (u8)r1;
        r4 -= 1;
        r0 -= 1;
    }
 while (r0 != 0);
L_080125CE:
    r0 = r5;
    r0 &= r7;
    if (r0 != 0) goto L_080125EC;
    r2 -= 1;
    if (r5 == 0) goto L_080125EC;
    r0 = r5;
    do {
        r3 = *(u8 *)r2;
        *(u8 *)r4 = (u8)r3;
        r2 -= 1;
        r4 -= 1;
        r0 -= 1;
    }
 while (r0 != 0);
L_080125EC:
if ((s32)r2 <= (s32)r12) break;
 if ((s32)r4 <= (s32)r6) break;
 }
    return;
}
