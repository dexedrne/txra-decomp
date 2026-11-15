/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_03007A30[];
void func_08014C0C(void)
{
    *(vu16 *)0x04000208 = 0;
    *(vu16 *)0x04000200 &= 0xFF3F;
    *(vu16 *)0x04000208 = 1;
    *(vu16 *)0x04000128 = 0x2003;
    *(vu32 *)0x0400010C = 0xB1FC;
    *(vu16 *)0x04000202 = 0xC0;
    g_03007A30[8] = 0;
}
