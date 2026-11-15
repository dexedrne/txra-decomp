#define FILL(value, destination, control) { \
    fill = (value); \
    dma[0] = (u32)&fill; \
    dma[1] = (u32)(destination); \
    dma[2] = (control); \
    (void)dma[2]; \
}
void func_08015F98(s32 page)
{
    u32 zero = 0;
    u32 fill;
    vu32 *dma = (vu32 *)0x040000D4;
    if (page == 0) {
        FILL(zero, 0x0600A000, 0x850021C0);
        FILL(zero, 0x06012700, 0x850003C0);
    } else {
        FILL(zero, 0x06000000, 0x850021C0);
        FILL(zero, 0x06008700, 0x850003C0);
    }
}
