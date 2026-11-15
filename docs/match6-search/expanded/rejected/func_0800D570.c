/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: call without saved LR or outside ROM
 */
/* func_0800D570  0x0800D570  thumb mode, 192 bytes of instructions (pools excluded)
 * callers: func_0800D630
 * callees: func_080141EC, func_08015200, func_08015E20, func_08015E34, func_08018854
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
u32 func_0800D570(void) {
    u32 r0, r1, r2, r3, r4;
    u32 sp04; /* stack slots */
    func_08015E20();
    r1 = 0x04000000 /* REG_DISPCNT */;
    r0 = 0;
    *(vu16 *)0x04000000 /* REG_DISPCNT */ = (u16)r0;
    r1 += 0xC;
    r2 = 0xC083;
    r0 = r2;
    *(vu16 *)0x0400000C /* REG_BG2CNT */ = (u16)r0;
    func_08018854();
    r4 = 0;
    *(u32 *)0x030014A8 /* IWRAM */ = r4;
    sp04 = r4;
    r3 = (u32)&sp04;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r1 = 0x03002A30 /* IWRAM */;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r2 = 0x85000080;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r2;
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    sp04 = r4;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r1 = 0x03000BE0 /* IWRAM */;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r2;
    r0 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    func_08015E20();
    r0 = 0;
    func_080141EC(r0);
    *(u32 *)0x03005FC0 /* IWRAM */ = r4;
    func_08015E34();
    *(u32 *)0x03002188 /* IWRAM */ = r4;
    r0 = 0x40;
    *(u32 *)0x030061E4 /* IWRAM */ = r0;
    *(u32 *)0x030067E4 /* IWRAM */ = r4;
    *(u32 *)0x030061F0 /* IWRAM */ = r4;
    *(u32 *)0x03001B24 /* IWRAM */ = r4;
    *(u32 *)0x03000DF0 /* IWRAM */ = r4;
    *(u32 *)0x03006680 /* IWRAM */ = r4;
    func_08015200();
    *(u32 *)0x03002320 /* IWRAM */ = r4;
    *(u32 *)0x03002324 /* IWRAM */ = r4;
    r1 = 0x3E8;
    *(u32 *)0x03002328 /* IWRAM */ = r1;
    *(u32 *)0x03005F70 /* IWRAM */ = r4;
    *(u32 *)0x03005F78 /* IWRAM */ = r4;
    *(u32 *)0x03002E44 /* IWRAM */ = r4;
    *(u32 *)0x03005784 /* IWRAM */ = r4;
    r0 = 0x2A28;
    *(u32 *)0x03002E48 /* IWRAM */ = r0;
    *(u32 *)0x03005FC4 /* IWRAM */ = r0;
    r1 = 0x03001E60 /* IWRAM */;
    r2 = 0x2C0;
    r0 = r1 + r2;
    *(u32 *)0x03001E64 /* IWRAM */ = r4;
    *(u32 *)0x03002120 /* IWRAM */ = r4;
    r3 = 0x2C4;
    r0 = r1 + r3;
    *(u32 *)0x03001E68 /* IWRAM */ = r4;
    *(u32 *)0x03002124 /* IWRAM */ = r4;
    r2 += 8;
    r0 = r1 + r2;
    *(u32 *)0x03001E6C /* IWRAM */ = r4;
    *(u32 *)0x03002128 /* IWRAM */ = r4;
    r3 += 0x18;
    r0 = r1 + r3;
    *(u32 *)0x03001E80 /* IWRAM */ = r4;
    *(u32 *)0x0300213C /* IWRAM */ = r4;
    r2 += 0x18;
    r0 = r1 + r2;
    *(u32 *)0x03001E84 /* IWRAM */ = r4;
    *(u32 *)0x03002140 /* IWRAM */ = r4;
}
