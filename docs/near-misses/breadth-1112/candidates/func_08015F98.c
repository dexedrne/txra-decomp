#define FILL(value, destination, control) { \
    fill = (value); \
    { vu32 *dma = (vu32 *)0x040000D4; \
    dma[0] = (u32)&fill; \
    dma[1] = (u32)(destination); \
    dma[2] = (control); \
    dma[2]; } \
}
void func_08015F98(s32 page)
{
    u32 fill;
    if (page == 0) {
        FILL(0, 0x0600A000, 0x850021C0);
        FILL(0, 0x06012700, 0x850003C0);
    } else {
        FILL(0, 0x06000000, 0x850021C0);
        FILL(0, 0x06008700, 0x850003C0);
    }
}
