/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u32 g_03000DE4;
extern u16 g_03000B54[];
extern void func_0800761C(u32, u32);
void func_0801604C(u32 value, u32 index)
{
    if (g_03000DE4 == 1) {
        g_03000B54[index] = value;
        func_0800761C(value, index);
    }
}
