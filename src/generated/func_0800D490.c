/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
u32 func_0800D490(void)
{
    u32 count;
    u8 *ptr;
    s32 i;
    u8 val;

    count = 0;
    ptr = (u8 *)0x03005680;
    i = 127;
    do {
        val = *ptr;
        if (val != 0) {
            count++;
        }
        ptr += 2;
        i--;
    } while (i >= 0);
    return count;
}
