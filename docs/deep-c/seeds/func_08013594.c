/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
extern void func_08005EE0(void);
extern void func_0801251C(u32,u32,u32);
extern u32 func_08013B38(void);
extern u32 func_08013C08(void);
extern void func_08013CF4(void);
extern void func_08015200(void);
extern void func_080154AC(u32);
extern void func_08015D78(void);
extern void func_08015E20(void);
extern void func_08015E34(void);
extern void func_0801604C(u32,u32);
extern void func_08016078(u32);
extern void func_080160C4(u32,u32,u32,u32);
extern void func_08016134(u32);
extern void func_080161E8(void);
extern void func_08018854(void);
u32 func_08013594(u32 r0) {
    u32 r1,r2,r3,r4,r5,r6,r7,r8,r9,r10;
    u32 sp00,sp04,sp08;
    r10 = r0;
    sp08 = r0;
    r0 = 0;
    func_08016078(r0);
L_080135AA:
    func_08005EE0();
    r0 = 0;
    *(u32 *)0x030014A8 /* IWRAM */ = r0;
    r1 = 0x030021E0 /* IWRAM */;
    r2 = 0;
    r3 = 0x13E;
    r0 = r1 + r3;
    do {
        *(u16 *)r0 = (u16)r2;
        r0 -= 2;
    } while ((s32)r0 >= (s32)r1);
    r5 = 0;
    sp04 = r5;
    r4 = 0x040000D4 /* REG_DMA3SAD */;
    r0 = (u32)&sp04;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r0;
    r1 = 0x03002A30 /* IWRAM */;
    r9 = r1;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r6 = 0x85000080;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r6;
    r0 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    sp04 = r5;
    r2 = (u32)&sp04;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r2;
    r3 = 0x03000BE0 /* IWRAM */;
    r8 = r3;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r3;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r6;
    r0 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    func_08015E20();
    func_08015E20();
    *(vu16 *)0x04000000 /* REG_DISPCNT */ = (u16)r5;
    r1 = 0x0400000C /* REG_BG2CNT */;
    r2 = 0xC083;
    r0 = r2;
    *(vu16 *)0x0400000C /* REG_BG2CNT */ = (u16)r0;
    r1 += 0x44;
    r3 = 0x1641;
    r0 = r3;
    *(vu16 *)0x04000050 /* REG_BLDCNT */ = (u16)r0;
    r1 += 2;
    r2 = 0x808;
    r0 = r2;
    *(vu16 *)0x04000052 /* REG_BLDALPHA */ = (u16)r0;
    r1 += 2;
    r0 = 1;
    *(vu16 *)0x04000054 /* REG_BLDY */ = (u16)r0;
    func_08018854();
    *(u32 *)0x030014A8 /* IWRAM */ = r5;
    sp04 = r5;
    r3 = (u32)&sp04;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r0 = r9;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r0;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r6;
    r0 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    sp04 = r5;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r1 = r8;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r6;
    r0 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    func_08015E20();
    func_08015E34();
    *(u32 *)0x03002188 /* IWRAM */ = r5;
    r0 = 0x40;
    *(u32 *)0x030061E4 /* IWRAM */ = r0;
    *(u32 *)0x030067E4 /* IWRAM */ = r5;
    *(u32 *)0x030061F0 /* IWRAM */ = r5;
    *(u32 *)0x03001B24 /* IWRAM */ = r5;
    *(u32 *)0x03000DF0 /* IWRAM */ = r5;
    *(u32 *)0x03006680 /* IWRAM */ = r5;
    *(u32 *)0x03005FC0 /* IWRAM */ = r5;
    func_08015200();
    r1 = 0x03005788 /* IWRAM */;
    r0 = 0x1F;
    *(u16 *)0x03005788 /* IWRAM */ = (u16)r0;
    r0 = 0x030014B4 /* IWRAM */;
    *(u32 *)0x030014B4 /* IWRAM */ = r5;
    r9 = r5;
L_08013674:
    func_08015D78();
    func_08015E20();
    func_080161E8();
    func_08013CF4();
    func_08015E34();
    r2 = 0;
    *(u32 *)0x03002188 /* IWRAM */ = r2;
    r0 = 0x40;
    *(u32 *)0x030061E4 /* IWRAM */ = r0;
    *(u32 *)0x030067E4 /* IWRAM */ = r2;
    *(u32 *)0x030061F0 /* IWRAM */ = r2;
    *(u32 *)0x03001B24 /* IWRAM */ = r2;
    *(u32 *)0x03000DF0 /* IWRAM */ = r2;
    *(u32 *)0x03006680 /* IWRAM */ = r2;
    func_08015200();
    r0 = 0x02000000;
    func_08016134(r0);
    r2 = sp08;
    if (r2 <= 9) goto L_080136BC;
    goto L_08013894;
L_080136BC:
    switch (r2) { case 0: goto L_08013744; case 1: goto L_0801376C; case 2: goto L_080137F0; case 3: goto L_0801387C; case 4: goto L_08013894; case 5: goto L_08013894; case 6: goto L_08013894; case 7: goto L_08013894; case 8: goto L_08013798; case 9: goto L_080137C4; }
L_08013744:
    r6 = 0x03002E58 /* IWRAM */;
    r7 = 0;
    *(u32 *)0x03002E58 /* IWRAM */ = r7;
    r5 = 0x030066D4 /* IWRAM */;
    r0 = 0x40;
    *(u32 *)0x030066D4 /* IWRAM */ = r0;
    r4 = 0x03001B18 /* IWRAM */;
    r0 = 2;
    *(u32 *)0x03001B18 /* IWRAM */ = r0;
    r0 = 0x080258F4 /* ROM */;
    goto L_08013804;
L_0801376C:
    r0 = 0;
    *(u32 *)0x03002E58 /* IWRAM */ = r0;
    r0 = 0x40;
    *(u32 *)0x030066D4 /* IWRAM */ = r0;
    r0 = 2;
    *(u32 *)0x03001B18 /* IWRAM */ = r0;
    r0 = 0x080259CC /* ROM */;
    func_080154AC(r0);
    goto L_08013894;
L_08013798:
    r0 = 0;
    *(u32 *)0x03002E58 /* IWRAM */ = r0;
    r0 = 0x40;
    *(u32 *)0x030066D4 /* IWRAM */ = r0;
    r0 = 2;
    *(u32 *)0x03001B18 /* IWRAM */ = r0;
    r0 = 0x08025CE4 /* ROM */;
    func_080154AC(r0);
    goto L_08013894;
L_080137C4:
    r0 = 0;
    *(u32 *)0x03002E58 /* IWRAM */ = r0;
    r0 = 0x40;
    *(u32 *)0x030066D4 /* IWRAM */ = r0;
    r0 = 2;
    *(u32 *)0x03001B18 /* IWRAM */ = r0;
    r0 = 0x08025D2C /* ROM */;
    func_080154AC(r0);
    goto L_08013894;
L_080137F0:
    r6 = 0x03002E58 /* IWRAM */;
    r7 = 0;
    *(u32 *)0x03002E58 /* IWRAM */ = r7;
    r5 = 0x030066D4 /* IWRAM */;
    r0 = 0x40;
    *(u32 *)0x030066D4 /* IWRAM */ = r0;
    r4 = 0x03001B18 /* IWRAM */;
    r0 = 2;
    *(u32 *)0x03001B18 /* IWRAM */ = r0;
    r0 = 0x08025A14 /* ROM */;
L_08013804:
    func_080154AC(r0);
    r0 = *(u32 *)0x030014B4 /* IWRAM */;
    if (r0 != 0) goto L_0801381C;
    r0 = *(u32 *)0x03001B1C /* IWRAM */;
    r1 = 0xF;
    r0 &= r1;
    if (r0 > 7) goto L_0801382E;
L_0801381C:
    r0 = 0x20;
    r0 = -r0;
    *(u32 *)r6 = r0;
    r0 = 0x60;
    *(u32 *)r5 = r0;
    *(u32 *)r4 = r7;
    r0 = 0x0802593C /* ROM */;
    func_080154AC(r0);
L_0801382E:
    r0 = *(u32 *)0x030014B4 /* IWRAM */;
    if (r0 != 1) goto L_08013842;
    r0 = *(u32 *)0x03001B1C /* IWRAM */;
    r1 = 0xF;
    r0 &= r1;
    if (r0 > 7) goto L_08013894;
L_08013842:
    r0 = 0x20;
    *(u32 *)0x03002E58 /* IWRAM */ = r0;
    r0 = 0x60;
    *(u32 *)0x030066D4 /* IWRAM */ = r0;
    r0 = 0;
    *(u32 *)0x03001B18 /* IWRAM */ = r0;
    r0 = 0x08025984 /* ROM */;
    func_080154AC(r0);
    goto L_08013894;
L_0801387C:
    r0 = 0;
    *(u32 *)0x03002E58 /* IWRAM */ = r0;
    r0 = 0x40;
    *(u32 *)0x030066D4 /* IWRAM */ = r0;
    r0 = 2;
    *(u32 *)0x03001B18 /* IWRAM */ = r0;
    r0 = 0x08025A5C /* ROM */;
    func_080154AC(r0);
L_08013894:
    r3 = r9;
    if (r3 == 0) {
        r0 = 0x0828FD84 /* ROM */;
        r4 = 0x02009600 /* EWRAM */;
        r5 = 0x9600;
        r1 = r4;
        r2 = r5;
        func_0801251C(r0, r1, r2);
        r0 = 0x02000000;
        r8 = r0;
        r6 = 0x20;
        sp00 = r6;
        r0 = 3;
        r1 = r4;
        r2 = r8;
        r3 = r5;
        func_080160C4(r0, r1, r2, r3);
        r0 = 0x0828B4E8 /* ROM */;
        r2 = 0xF5A0;
        r1 = r4;
        func_0801251C(r0, r1, r2);
        r3 = 0x1B30;
        sp00 = r6;
        r0 = 3;
        r1 = r4;
        r2 = r8;
        func_080160C4(r0, r1, r2, r3);
    }
    r0 = 0x03005788 /* IWRAM */;
    r1 = 0;
    r0 = *(s16 *)(r0 + r1);
    if (r0 == 0) goto L_080138E4;
    goto L_08013A92;
L_080138E4:
    r2 = sp08;
    if (r2 <= 9) goto L_080138EC;
    goto L_08013A92;
L_080138EC:
    switch (r2) { case 0: goto L_0801394C; case 1: goto L_080139B8; case 2: goto L_08013A02; case 3: goto L_08013A74; case 4: goto L_08013A92; case 5: goto L_08013A92; case 6: goto L_08013A92; case 7: goto L_08013A92; case 8: goto L_080139EC; case 9: goto L_080139F6; }
L_0801394C:
    r0 = 0x20;
    r1 = *(u16 *)0x0300218C /* IWRAM */;
    r0 &= r1;
    if (r0 != 0) {
        r1 = 0x030014B4 /* IWRAM */;
        r0 = *(u32 *)0x030014B4 /* IWRAM */;
        if (r0 != 0) {
            r0 -= 1;
            *(u32 *)0x030014B4 /* IWRAM */ = r0;
        }
        r0 = 1;
        r1 = 1;
        func_0801604C(r0, r1);
    }
    r0 = 0x10;
    r1 = *(u16 *)0x0300218C /* IWRAM */;
    r0 &= r1;
    if (r0 != 0) {
        r1 = 0x030014B4 /* IWRAM */;
        r0 = *(u32 *)0x030014B4 /* IWRAM */;
        if (r0 != 1) {
            r0 += 1;
            *(u32 *)0x030014B4 /* IWRAM */ = r0;
        }
        r0 = 1;
        r1 = 1;
        func_0801604C(r0, r1);
    }
    r0 = 1;
    r1 = *(u16 *)0x0300218C /* IWRAM */;
    r0 &= r1;
    if (r0 != 0) goto L_0801399A;
    goto L_08013A92;
L_0801399A:
    r0 = *(u32 *)0x030014B4 /* IWRAM */;
    if (r0 == 0) {
        r3 = 1;
        r10 = r3;
    }
    if (r0 != 1) goto L_08013A62;
    r0 = 6;
    r10 = r0;
    goto L_08013A62;
L_080139B8:
    r1 = r9;
    if (r1 != 0x76) goto L_080139DA;
    r0 = func_08013B38();
    r4 = r0;
    r0 = *(u32 *)0x03006870 /* IWRAM */;
    if (r0 == 0) {
        r0 = 0;
        func_08016078(r0);
    }
    if (r4 == 0) goto L_080139DA;
    r2 = 8;
    r10 = r2;
L_080139DA:
    r3 = r9;
    if (r3 != 0x78) goto L_08013A92;
    r0 = 4;
    r10 = r0;
    goto L_08013A92;
L_080139EC:
    r1 = r9;
    if ((s32)r1 <= 0x40) goto L_08013A92;
    r2 = 6;
    goto L_08013A90;
L_080139F6:
    r3 = r9;
    if ((s32)r3 <= 0x40) goto L_08013A92;
    r0 = 7;
    r10 = r0;
    goto L_08013A92;
L_08013A02:
    r0 = 0x20;
    r1 = *(u16 *)0x0300218C /* IWRAM */;
    r0 &= r1;
    if (r0 != 0) {
        r1 = 0x030014B4 /* IWRAM */;
        r0 = *(u32 *)0x030014B4 /* IWRAM */;
        if (r0 != 0) {
            r0 -= 1;
            *(u32 *)0x030014B4 /* IWRAM */ = r0;
        }
        r0 = 1;
        r1 = 1;
        func_0801604C(r0, r1);
    }
    r0 = 0x10;
    r1 = *(u16 *)0x0300218C /* IWRAM */;
    r0 &= r1;
    if (r0 != 0) {
        r1 = 0x030014B4 /* IWRAM */;
        r0 = *(u32 *)0x030014B4 /* IWRAM */;
        if (r0 != 1) {
            r0 += 1;
            *(u32 *)0x030014B4 /* IWRAM */ = r0;
        }
        r0 = 1;
        r1 = 1;
        func_0801604C(r0, r1);
    }
    r0 = 1;
    r1 = *(u16 *)0x0300218C /* IWRAM */;
    r0 &= r1;
    if (r0 == 0) goto L_08013A92;
    r0 = *(u32 *)0x030014B4 /* IWRAM */;
    if (r0 == 0) {
        r1 = 3;
        r10 = r1;
    }
    if (r0 != 1) goto L_08013A62;
    r2 = 7;
    r10 = r2;
L_08013A62:
    r0 = 2;
    r1 = 1;
    func_0801604C(r0, r1);
    goto L_08013A92;
L_08013A74:
    r3 = r9;
    if (r3 != 0x76) goto L_08013A88;
    r0 = func_08013C08();
    r4 = r0;
    if (r4 == 0) goto L_08013A88;
    r0 = 9;
    r10 = r0;
L_08013A88:
    r1 = r9;
    if (r1 != 0x78) goto L_08013A92;
    r2 = 5;
L_08013A90:
    r10 = r2;
L_08013A92:
    r0 = 0x03005FC0 /* IWRAM */;
    r1 = *(u32 *)0x03005FC0 /* IWRAM */;
    r1 += 1;
    r2 = 1;
    r1 &= r2;
    *(u32 *)0x03005FC0 /* IWRAM */ = r1;
    r9 += r2;
    r3 = r9;
    if ((s32)r3 > 0xFF) {
        r0 = 0x40;
        r9 = r0;
    }
    r1 = sp08;
    if (r1 != r10) goto L_08013AB2;
    goto L_08013674;
L_08013AB2:
    r2 = r10;
    if (r2 != 1) goto L_08013AC4;
    r3 = 1;
    sp08 = r3;
    goto L_080135AA;
L_08013AC4:
    r0 = r10;
    if (r0 != 3) goto L_08013AD0;
    r1 = 3;
    sp08 = r1;
    goto L_080135AA;
L_08013AD0:
    r2 = r10;
    if (r2 != 8) goto L_08013ADC;
    r3 = 8;
    sp08 = r3;
    goto L_080135AA;
L_08013ADC:
    r0 = r10;
    if (r0 != 9) goto L_08013AE8;
    r1 = 9;
    sp08 = r1;
    goto L_080135AA;
L_08013AE8:
    r3 = 0;
    sp04 = r3;
    r2 = (u32)&sp04;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r2;
    r1 = 0x03002A30 /* IWRAM */;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r2 = 0x85000080;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r2;
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    sp04 = r3;
    r3 = (u32)&sp04;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r1 = 0x03000BE0 /* IWRAM */;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r2;
    r0 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    func_08015E20();
    r0 = 2;
    func_08016078(r0);
    r0 = r10;
    return r0;
}
