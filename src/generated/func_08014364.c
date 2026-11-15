/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_03000B60[];
void func_08014364(void)
{
    s32 i;
    u32 j;
    u8 *source;
    u8 *dest;
    i = 1;
    source = g_03000B60;
    for (; i <= 3; i++) {
        dest = (u8 *)(i * 32 + (u32)source);
        if (*dest == 0) {
            for (j = 0; j <= 31; j++) *dest++ = *source++;
            break;
        }
    }
}
