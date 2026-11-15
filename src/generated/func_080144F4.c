/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
void func_080144F4(void)
{
    *(vu32 *)0x03002184 = 1;
    *(vu32 *)0x04000100 = 0;
    *(vu32 *)0x040000C4 = 0;
    *(vu32 *)0x04000104 = 0;
    *(vu32 *)0x040000D0 = 0;
}
