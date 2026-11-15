/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern void func_08005F8C(u32);

void func_08016078(u32 r0)
{
    u32 r4;
    u32 result;

    r4 = r0;
    r0 = *(vu32 *)0x03006870;
    if (r0 != 0) {
        if (r4 != 0) {
            result = r4;
            func_08005F8C(result);
            *(vu16 *)0x030021D0 = (u16)r4;
            return;
        }
    }
    func_08005F8C(0);
    *(vu16 *)0x030021D0 = (u16)r4;
}
