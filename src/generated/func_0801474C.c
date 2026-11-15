/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern s32 g_030001C8;
extern u8 g_03007A04;
extern u32 g_030079E0;
extern void func_08014BF8(void);
void func_0801474C(void)
{
    if (g_030001C8 <= 1 && g_03007A04 == 0) {
        if (g_030079E0 & 128) {
            func_08014BF8();
            g_03007A04 = 1;
        } else if (g_030079E0 & 15) g_03007A04 = 1;
    }
}
