/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern void func_08016078(u32 r0);

void func_0800D290(void) {
    u32 r0;
    s16 r1;
    u32 r4;
    u32 r5;

    r0 = 0x030021D0;
    r1 = *(s16 *)r0;
    if (r1 == 1) goto L_0800D2E4;
    if (r1 == 3) goto L_0800D2E4;
    if (r1 == 4) goto L_0800D2E4;
    if (r1 == 8) goto L_0800D2E4;
    r5 = 0x03001B1C;
    r4 = *(u32 *)r5;
    r4 &= 3;
    if (r4 != 0) goto L_0800D2BA;
    func_08016078(1);
L_0800D2BA:
    r4 = *(u32 *)r5;
    r4 &= 3;
    if (r4 != 1) goto L_0800D2C8;
    func_08016078(3);
L_0800D2C8:
    r4 = *(u32 *)r5;
    r4 &= 3;
    if (r4 != 2) goto L_0800D2D6;
    func_08016078(4);
L_0800D2D6:
    r4 = *(u32 *)r5;
    r4 &= 3;
    if (r4 != 3) goto L_0800D2E4;
    func_08016078(8);
L_0800D2E4:
    return;
}
