#define FILL(value, destination, control) { \
    fill = (value); \
    { vu32 *dma = (vu32 *)0x040000D4; \
    dma[0] = (u32)&fill; \
    dma[1] = (u32)(destination); \
    dma[2] = (control); \
    dma[2]; } \
}
void func_08015F58(s32 page)
{
    u32 pattern = 0xB1B1B1B1;
    u32 fill;
    if (page == 0) {
        FILL(pattern, 0x0600A000, 0x85002580);
    } else {
        FILL(pattern, 0x06000000, 0x85002580);
    }
}
