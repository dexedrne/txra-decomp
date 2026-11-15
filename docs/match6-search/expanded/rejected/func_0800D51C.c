/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: path leaves ROM or enters established literal/data pool
 */
/* func_0800D51C  0x0800D51C  thumb mode, 84 bytes of instructions (pools excluded)
 * callers: func_080020B8
 * callees: func_08015E20
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_0800D51C(u32 r0) {
    u32 r1, r2, r3, r4, r6;
    u32 sp04; /* stack slots */
    r6 = r0;
    r4 = 0;
    *(u32 *)0x03000010 /* IWRAM */ = r4;
    r0 = 0x4C;
    *(u32 *)0x030001C4 /* IWRAM */ = r0;
    *(u32 *)0x030014A8 /* IWRAM */ = r4;
    sp04 = r4;
    r1 = (u32)&sp04;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r1;
    r1 = 0x03002A30 /* IWRAM */;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r2 = 0x85000080;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r2;
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    sp04 = r4;
    r3 = (u32)&sp04;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r1 = 0x03000BE0 /* IWRAM */;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r2;
    r0 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    func_08015E20();
    *(u32 *)0x03005FCC /* IWRAM */ = r4;
    *(u32 *)0x03001B20 /* IWRAM */ = r4;
    *(u32 *)0x030001CC /* IWRAM */ = r6;
    r0 = 0x1F;
    *(u16 *)0x03005788 /* IWRAM */ = (u16)r0;
}
