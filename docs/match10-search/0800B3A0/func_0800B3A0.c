extern u32 func_08005F0C(void);
void func_0800B3A0(void) {
    u32 r0;
    u32 r1;
    u32 r2;
    u32 r3;
    u32 r4;
    u32 r5;
    u32 r6;
    u32 r7;
    u32 r8;
    u32 r9;
    u32 r10;
    u32 r12;
    r0 = func_08005F0C();
    r0 = *(u32 *)0x03005FC0 ;
    r1 = 0x06000000;
    r12 = r1;
    if (r0 == 0) {
        r2 = 0x0600A000 ;
        r12 = r2;
    }
    r0 = 0x03001E50 ;
    r1 = 0;
    r0 = *(s16 *)(r0 + r1);
    if (r0 == 0) {
        r4 = 0x1C20;
        r6 = r4;
        r7 = 1;
    }
    if (r0 == 1) {
        r4 = 0x1400;
        r6 = r4;
        r7 = 1;
    }
    if (r0 == 2) {
        r6 = 0x1C20;
        r4 = 0x1400;
        r7 = 0;
    }
    if (r0 == 3) {
        r6 = 0x1F40;
        r4 = 0x1B58;
        r7 = 1;
    }
    if (r0 == 4) {
        r4 = 0x1B58;
        r6 = r4;
        r7 = 4;
    }
    if (r0 == 5) {
        r6 = 0x1900;
        r4 = 0x1194;
        r7 = 1;
    }
    r5 = 0;
    r0 = 0x03002E4C ;
    r1 = *(u32 *)0x03002E4C ;
    r10 = r0;
    if ((s32)r5 < (s32)r1) {
        r2 = 0x0804F330 ;
        r1 = 0x10000;
        r0 = r6 + r1;
        r0 <<= 2;
        r0 += r2;
        r0 = *(u32 *)r0;
        r8 = r0;
        r1 = r4 + r1;
        r1 <<= 2;
        r1 += r2;
        r6 = *(u32 *)r1;
        r2 = 0x03006874 ;
        r9 = r2;
        r4 = 0;
        do {
            r0 = r9;
            r1 = *(u32 *)r0;
            {
 u32 r1_add_input = r1;
 r1 = r4 + r1_add_input;
 }
            r0 = *(u32 *)r1;
            r3 = -r0;
            r2 = *(u32 *)(r1 + 8);
            r0 = r8;
            r0 *= r3;
            r3 = (s32)r0 >> 19;
            r0 = r2;
            r0 *= r6;
            r2 = (s16)r0 >> 19;
            r0 = r3;
            r0 += 0x20;
            r3 = r0 + r7;
            r2 += 0x78;
            r0 = r3 - 1;
            if (r0 > 0xEE) goto L_0800B4BC;
            if ((s32)r2 <= 0) goto L_0800B4BC;
            if ((s32)r2 > 0x9F) goto L_0800B4BC;
            r0 = 1;
            r0 &= r3;
            if (r0 == 0) goto L_0800B4A4;
            r1 = (s32)r3 >> 1;
            r0 = r2 << 4;
            r0 -= r2;
            r0 <<= 4;
            r1 <<= 1;
            r1 += r12;
            r0 += r1;
            r1 = *(u8 *)r0;
            *(u16 *)r0 = (u16)r1;
            goto L_0800B4BC;
L_0800B4A4:
            r0 = (s32)r3 >> 1;
            r1 = r2 << 4;
            r1 -= r2;
            r1 <<= 4;
            r0 <<= 1;
            r0 += r12;
            r1 += r0;
            r0 = 0xFF00;
            r2 = *(u16 *)r1;
            r0 &= r2;
            *(u16 *)r1 = (u16)r0;
L_0800B4BC:
            r4 += 0xE0;
            r5 += 8;
            r1 = r10;
            r0 = *(u32 *)r1;
        }
 while ((s32)r5 < (s32)r0);
    }
    return;
}
