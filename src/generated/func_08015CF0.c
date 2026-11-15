/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern void func_08014AE0(void);

void func_08015CF0(void) {
    u32 r0;
    r0 = *(u32 *)0x030001C8;
    if ((s32)r0 > 1) {
        goto skip;
    }
    func_08014AE0();
skip:
    return;
}
