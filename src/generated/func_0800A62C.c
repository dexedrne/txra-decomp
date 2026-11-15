/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_03001E60[];
extern s32 g_03006A80;
void func_0800A62C(void)
{
    u8 *p=g_03001E60;
    if (*(s16 *)(p+82)<=1) g_03006A80=(*(s32 *)(p+40)>>6)+40;
    if (*(s16 *)(p+82)==2) g_03006A80=(*(s32 *)(p+40)>>6)+32;
    if (*(s16 *)(p+82)==3) g_03006A80=(*(s32 *)(p+40)>>6)+24;
    if (*(s16 *)(p+82)==4) g_03006A80=(*(s32 *)(p+40)>>6)+16;
    if (*(s16 *)(p+82)==5) g_03006A80=(*(s32 *)(p+40)>>6)+8;
}
