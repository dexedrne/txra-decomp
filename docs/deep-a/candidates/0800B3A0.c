/* Unmatched diagnostic source; not installed or accepted as behavior-correct. */
extern void func_08005F0C(void);
extern u32 g_03005FC0;
extern s16 g_03001E50;
extern s32 g_03002E4C,g_0804F330[];
extern TxraRow28 *g_03006874;
void func_0800B3A0(void)
{
    u32 screen;
    s32 mode, xs,zs,shift;
    s32 i,offset;
    s32 xf,zf;
    func_08005F0C();
    screen = 0x06000000;
    if (!g_03005FC0) screen = 0x0600A000;
    mode = g_03001E50;
    if (mode == 0) { xs=7200; zs=xs; shift=1; }
    if (mode == 1) { xs=5120; zs=xs; shift=1; }
    if (mode == 2) { zs=7200; xs=5120; shift=0; }
    if (mode == 3) { zs=8000; xs=7000; shift=1; }
    if (mode == 4) { xs=7000; zs=xs; shift=4; }
    if (mode == 5) { zs=6400; xs=4500; shift=1; }
    i=0;
    if (i < g_03002E4C) {
        zf = g_0804F330[zs+0x10000];
        xf = g_0804F330[xs+0x10000];
        offset=0;
        do {
            TxraRow28 *point = (TxraRow28 *)((u32)g_03006874+offset);
            s32 x = (-point->field_00 * zf) >> 19;
            s32 y = (point->field_08 * xf) >> 19;
            x = (x+32)+shift;
            y += 120;
            if ((u32)(x-1) <= 238 && y > 0 && y <= 159) {
                if (x & 1) {
                    u32 p = screen + ((x>>1)<<1) + y*240;
                    *(u16 *)p = *(u8 *)p;
                } else {
                    u32 p = screen + ((x>>1)<<1) + y*240;
                    *(u16 *)p = *(u16 *)p & 0xFF00;
                }
            }
            offset += 224;
            i += 8;
        } while (i < g_03002E4C);
    }
}
