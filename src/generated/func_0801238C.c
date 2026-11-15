/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_03000B60[], g_03001E60[];
void func_0801238C(void)
{
    u8 *p = g_03000B60;
    u32 i = 0;
    u8 *base = p;
    u8 *record = g_03001E60;
    u16 *value;
    for (; i <= 31; i++) *p++ = 0;
    base[0] = 1;
    value = (u16 *)(record + 0x2BE);
    base[2] = *value;
    base[3] = 1; base[14] = 1;
    base[4] = 1; base[15] = 1;
    base[5] = 1; base[16] = 1;
    base[6] = 1; base[17] = 1;
    base[7] = 1; base[18] = 1;
    base[8] = 1; base[19] = 1;
    base[9] = 1; base[20] = 1;
    base[10] = 1; base[21] = 1;
    base[11] = 1; base[22] = 1;
    base[12] = 1; base[23] = 1;
    base[13] = 1; base[24] = 1;
    *(u16 *)(record + 2) = *value;
}
