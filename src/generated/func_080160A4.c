/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
void func_080160A4(u8 *source, u8 *dest, s32 length)
{
    s32 i;
    for (i = 0; i < length; i++) dest[i] = source[i];
}
