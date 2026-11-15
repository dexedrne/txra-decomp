extern vu32 g_040000D4[];
extern void func_08005EE0(void);
extern u32 func_08005EF8(void);
extern void func_0801251C(u32,u32,u32);
extern void func_08013DB4(void);
extern void func_08013E74(void);
extern void func_08015200(void);
extern void func_080154AC(u32);
extern void func_08015D78(void);
extern void func_08015E20(void);
extern void func_08015E34(void);
extern void func_0801604C(u32,u32);
extern void func_08016134(u32);
extern void func_080161E8(void);
extern void func_08018854(void);
/* func_08012A50  0x08012A50  thumb mode, 614 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: func_08005EE0, func_08005EF8, func_0801251C, func_08013DB4, func_08013E74, func_08015200, func_080154AC, func_08015D78, func_08015E20, func_08015E34, func_0801604C, func_08016134, func_080161E8, func_08018854
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_08012A50(void) {
    u32 r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10;
    u32 sp00; /* stack slots */
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
    {u32 fill=r5;
    r0 = (u32)&fill;
    g_040000D4[0] /* REG_DMA3SAD */ = (u32)&fill;
    r1 = 0x03002A30 /* IWRAM */;
    r9 = r1;
    g_040000D4[1] /* REG_DMA3DAD */ = r1;
    r6 = 0x85000080;
    g_040000D4[2] /* REG_DMA3CNT */ = r6;
    r0 = g_040000D4[2] /* REG_DMA3CNT */;
}
    {u32 fill=r5;
    r2 = (u32)&fill;
    g_040000D4[0] /* REG_DMA3SAD */ = (u32)&fill;
    r3 = 0x03000BE0 /* IWRAM */;
    r8 = r3;
    g_040000D4[1] /* REG_DMA3DAD */ = r3;
    g_040000D4[2] /* REG_DMA3CNT */ = r6;
    r0 = g_040000D4[2] /* REG_DMA3CNT */;
}
    func_08015E20();
    func_08015E20();
    *(vu16 *)0x04000000 /* REG_DISPCNT */ = (u16)r5;
    r2 = 0xC083;
    r0 = r2;
    *(vu16 *)0x0400000C /* REG_BG2CNT */ = (u16)r0;
    func_08018854();
    *(u32 *)0x030014A8 /* IWRAM */ = r5;
    {u32 fill=r5;
    r3 = (u32)&fill;
    g_040000D4[0] /* REG_DMA3SAD */ = (u32)&fill;
    r0 = r9;
    g_040000D4[1] /* REG_DMA3DAD */ = r0;
    g_040000D4[2] /* REG_DMA3CNT */ = r6;
    r0 = g_040000D4[2] /* REG_DMA3CNT */;
}
    {u32 fill=r5;
    g_040000D4[0] /* REG_DMA3SAD */ = (u32)&fill;
    r1 = r8;
    g_040000D4[1] /* REG_DMA3DAD */ = r1;
    g_040000D4[2] /* REG_DMA3CNT */ = r6;
    r0 = g_040000D4[2] /* REG_DMA3CNT */;
}
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
    r4 = 0x03005FC0 /* IWRAM */;
    *(u32 *)0x03005FC0 /* IWRAM */ = r5;
    func_08015200();
    r1 = 0x03005788 /* IWRAM */;
    r0 = 0x1F;
    *(u16 *)0x03005788 /* IWRAM */ = (u16)r0;
    r6 = 0;
    r2 = 0x02000000;
    r10 = r2;
    r3 = 0x03002E58 /* IWRAM */;
    r9 = r3;
    r8 = r6;
    r7 = r4;
L_08012B1A:
    func_08015D78();
    func_08015E20();
    func_080161E8();
    func_08013DB4();
    r0 = 0x02019EF0 /* EWRAM */;
    *(u32 *)0x030021C4 /* IWRAM */ = r0;
    r0 = r10;
    func_08016134(r0);
    r0 = r8;
    r1 = r9;
    *(u32 *)r1 = r0;
    r5 = 0x030066D4 /* IWRAM */;
    r0 = 4;
    *(u32 *)0x030066D4 /* IWRAM */ = r0;
    r4 = 0x03001B18 /* IWRAM */;
    r0 = 2;
    *(u32 *)0x03001B18 /* IWRAM */ = r0;
    r0 = 0x080257D4 /* ROM */;
    func_080154AC(r0);
    r2 = r8;
    r3 = r9;
    *(u32 *)r3 = r2;
    r0 = 0x8C;
    *(u32 *)0x030066D4 /* IWRAM */ = r0;
    *(u32 *)0x03001B18 /* IWRAM */ = r2;
    r0 = 0x0802578C /* ROM */;
    func_080154AC(r0);
    func_08013E74();
    r2 = 0x03000DFC /* IWRAM */;
    r0 = *(u32 *)r7;
    r1 = 0x06000000;
    if (r0 == 0) {
        r1 = 0x0600A000 /* VRAM */;
    }
    *(u32 *)r2 = r1;
    r0 = func_08005EF8();
    if (r6 == 0) {
        r0 = 0x083186E0 /* ROM */;
        r1 = r10;
        r2 = 0x9600;
        func_0801251C(r0, r1, r2);
    }
    r0 = 0x03005788 /* IWRAM */;
    r1 = 0;
    r0 = *(s16 *)(r0 + r1);
    if (r0 != 0) goto L_08012BEE;
    r0 = 0x20;
    r1 = *(u16 *)0x0300218C /* IWRAM */;
    r0 &= r1;
    if (r0 != 0) {
        r2 = 0x030021D8 /* IWRAM */;
        r1 = *(u32 *)0x030021D8 /* IWRAM */;
        r0 = r1 - 1;
        *(u32 *)0x030021D8 /* IWRAM */ = r0;
        if (r0 > 5) {
            r0 = r1 + 5;
            *(u32 *)0x030021D8 /* IWRAM */ = r0;
        }
        r0 = 1;
        r1 = 1;
        func_0801604C(r0, r1);
    }
    r0 = 0x10;
    r1 = *(u16 *)0x0300218C /* IWRAM */;
    r0 &= r1;
    if (r0 != 0) {
        r2 = 0x030021D8 /* IWRAM */;
        r1 = *(u32 *)0x030021D8 /* IWRAM */;
        r0 = r1 + 1;
        *(u32 *)0x030021D8 /* IWRAM */ = r0;
        if (r0 > 5) {
            r0 = r1 - 5;
            *(u32 *)0x030021D8 /* IWRAM */ = r0;
        }
        r0 = 1;
        r1 = 1;
        func_0801604C(r0, r1);
    }
    r1 = *(u16 *)0x0300218C /* IWRAM */;
    r0 = 1;
    r0 &= r1;
    if (r0 != 0) goto L_08012C78;
    r0 = 8;
    r0 &= r1;
    if (r0 != 0) goto L_08012C78;
L_08012BEE:
    r0 = *(u32 *)r7;
    r0 += 1;
    r1 = 1;
    r0 &= r1;
    *(u32 *)r7 = r0;
    r6 += 1;
    if ((s32)r6 <= 0xFF) goto L_08012B1A;
    r6 = 0x40;
    goto L_08012B1A;
L_08012C78:
    r0 = 2;
    r1 = 1;
    func_0801604C(r0, r1);
    r3 = 0;
    {u32 fill=r3;
    r2 = (u32)&fill;
    g_040000D4[0] /* REG_DMA3SAD */ = (u32)&fill;
    r1 = 0x03002A30 /* IWRAM */;
    g_040000D4[1] /* REG_DMA3DAD */ = r1;
    r2 = 0x85000080;
    g_040000D4[2] /* REG_DMA3CNT */ = r2;
    r1 = g_040000D4[2] /* REG_DMA3CNT */;
}
    {u32 fill=r3;
    r3 = (u32)&fill;
    g_040000D4[0] /* REG_DMA3SAD */ = (u32)&fill;
    r1 = 0x03000BE0 /* IWRAM */;
    g_040000D4[1] /* REG_DMA3DAD */ = r1;
    g_040000D4[2] /* REG_DMA3CNT */ = r2;
    r0 = g_040000D4[2] /* REG_DMA3CNT */;
}
    func_08015E20();
    return;
}
