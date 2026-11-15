/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* func_08018854  0x08018854  arm mode, 416 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: none (leaf)
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
u32 func_08018854(void) {
    u32 r11, r12;
    r12 = sp;
    r0 = *(u32 *)(pc + 0x190);
    r2 = 0xD4;
    r3 = *(u32 *)(pc + 0x18C);
    r2 += 0x4000000;
    r1 = *(u32 *)(pc + 0x188);
    r3 -= r0;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r0;
    if ((s32)r3 < 0) { r3 += 3; }
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r3 = (s32)r3 >> 2;
    r0 = *(u32 *)(pc + 0x170);
    r3 |= 0x84000000;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r3;
    r3 = *(u32 *)(pc + 0x168);
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    r3 -= r0;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r0;
    r1 = *(u32 *)(pc + 0x158);
    if ((s32)r3 < 0) { r3 += 3; }
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r3 = (s32)r3 >> 2;
    r0 = *(u32 *)(pc + 0x14C);
    r3 |= 0x84000000;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r3;
    r3 = *(u32 *)(pc + 0x144);
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    r3 -= r0;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r0;
    r1 = *(u32 *)(pc + 0x134);
    if ((s32)r3 < 0) { r3 += 3; }
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r3 = (s32)r3 >> 2;
    r0 = *(u32 *)(pc + 0x128);
    r3 |= 0x84000000;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r3;
    r3 = *(u32 *)(pc + 0x120);
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    r3 -= r0;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r0;
    if ((s32)r3 < 0) { r3 += 3; }
    r1 = *(u32 *)(pc + 0x10C);
    r3 = (s32)r3 >> 2;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r3 |= 0x84000000;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r3;
    r3 = *(u32 *)(pc + 0xFC);
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r1 = *(u32 *)(pc + 0xF4);
    r3 = 0x1B4;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r3 += 0x84000001;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r3;
    r3 = *(u32 *)(pc + 0xE4);
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r1 = *(u32 *)(pc + 0xDC);
    r3 = 0x64;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r3 += 0x84000000;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r3;
    r1 = *(u32 *)(pc + 0xCC);
    r0 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r1;
    r3 = 0x460;
    r1 = *(u32 *)(pc + 0xC0);
    r3 += 0x80000005;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r3 += 0x4000000;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r3;
    r3 = *(u32 *)(pc + 0xB0);
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r1 = *(u32 *)(pc + 0xA8);
    r3 = 0x40;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r3 += 0x84000000;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r3;
    r3 = *(u32 *)(pc + 0x98);
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r1 = *(u32 *)(pc + 0x90);
    r3 = 0xC0;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r3 += 0x84000000;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r3;
    r3 = *(u32 *)(pc + 0x80);
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    *(vu32 *)0x040000D4 /* REG_DMA3SAD */ = r3;
    r1 = *(u32 *)(pc + 0x78);
    r3 = 0x1A8;
    *(vu32 *)0x040000D8 /* REG_DMA3DAD */ = r1;
    r3 += 0x84000001;
    *(vu32 *)0x040000DC /* REG_DMA3CNT */ = r3;
    r11 = r12 - 4;
    r1 = *(vu32 *)0x040000DC /* REG_DMA3CNT */;
    /* ldmdb r11, {r11, sp, lr} */
    return r0;
}
