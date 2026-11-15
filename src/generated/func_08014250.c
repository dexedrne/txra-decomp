/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern void func_080085E0(void);
extern void func_0800EDF4(u32, u32);
extern void func_08014394(void);
void func_08014250(u32 a0, u32 a1)
{
    func_0800EDF4(a0, a1);
    func_080085E0();
    func_08014394();
}
