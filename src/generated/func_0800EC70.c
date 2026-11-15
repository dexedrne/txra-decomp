/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
u32 func_0800EC70(u32 r0, u32 r1)
{
    u32 r2;
    u32 r3;
    u32 r4;
    u32 r5;

    r3 = r0;
    r5 = 0;
    r4 = 0x03000B60;
L_0800EC78:
    r1 -= 1;
    r0 = 3;
    r1 &= r0;
    r0 = r1 << 5;
    r2 = r0 + r4;
    r0 = *(u8 *)r2;
    if (r0 == 0) {
        goto L_0800ECBA;
    }
    if (r3 != 0) {
        goto L_0800EC96;
    }
    r0 = *(u8 *)(r2 + 2);
    if (r0 <= 0x0F) {
        goto L_0800EC96;
    }
    if (r0 <= 0x15) {
        goto L_0800ECC0;
    }
L_0800EC96:
    if (r3 != 1) {
        goto L_0800ECA8;
    }
    r0 = r1 << 5;
    r0 += r4;
    r0 = *(u8 *)(r0 + 2);
    if (r0 <= 0x15) {
        goto L_0800ECA8;
    }
    if (r0 <= 0x1A) {
        goto L_0800ECC0;
    }
L_0800ECA8:
    if (r3 != 2) {
        goto L_0800ECBA;
    }
    r0 = r1 << 5;
    r0 += r4;
    r0 = *(u8 *)(r0 + 2);
    if (r0 <= 0x1A) {
        goto L_0800ECBA;
    }
    if (r0 <= 0x1F) {
        goto L_0800ECC0;
    }
L_0800ECBA:
    r5 += 1;
    if ((s32)r5 <= 2) {
        goto L_0800EC78;
    }
L_0800ECC0:
    r0 = r1;
    return r0;
}
