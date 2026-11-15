/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern TxraRecord g_03001E60[];
extern s16 g_030014B0;
extern void func_0801251C(u8 *,u32,u32);
extern u8 g_082C77CC[];
extern u8 g_082CA6A4[];
extern u8 g_082CD9F4[];
extern u8 g_082D0BB8[];
extern u8 g_082D3F5C[];
extern u8 g_082D70C8[];
extern u8 g_082DA0C8[];
extern u8 g_082DD60C[];
extern u8 g_082E0AB0[];
extern u8 g_082E3DD4[];
extern u8 g_082E736C[];
extern u8 g_082EA454[];
extern u8 g_082ED260[];
extern u8 g_082F0860[];
extern u8 g_082F3A40[];
extern u8 g_082F6E58[];
void func_080085E0(void)
{
    u8 *p;
    if(g_03001E60[g_030014B0].field_02==16) p=g_082C77CC;
    if(g_03001E60[g_030014B0].field_02==17) p=g_082CA6A4;
    if(g_03001E60[g_030014B0].field_02==18) p=g_082CD9F4;
    if(g_03001E60[g_030014B0].field_02==19) p=g_082D0BB8;
    if(g_03001E60[g_030014B0].field_02==20) p=g_082D3F5C;
    if(g_03001E60[g_030014B0].field_02==21) p=g_082D70C8;
    if(g_03001E60[g_030014B0].field_02==22) p=g_082DA0C8;
    if(g_03001E60[g_030014B0].field_02==23) p=g_082DD60C;
    if(g_03001E60[g_030014B0].field_02==24) p=g_082E0AB0;
    if(g_03001E60[g_030014B0].field_02==25) p=g_082E3DD4;
    if(g_03001E60[g_030014B0].field_02==26) p=g_082E736C;
    if(g_03001E60[g_030014B0].field_02==27) p=g_082EA454;
    if(g_03001E60[g_030014B0].field_02==28) p=g_082ED260;
    if(g_03001E60[g_030014B0].field_02==29) p=g_082F0860;
    if(g_03001E60[g_030014B0].field_02==30) p=g_082F3A40;
    if(g_03001E60[g_030014B0].field_02==31) p=g_082F6E58;
    func_0801251C(p,0x02000000,0x10000);
}
