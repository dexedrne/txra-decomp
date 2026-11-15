/* Byte-verified C; address name retained pending semantic review.
 * Verified as part of unit_08005C7C.c (compiled after the earlier sound routines). */
#ifndef TXRA_BASIC_TYPES
#define TXRA_BASIC_TYPES
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#endif
#include "types.h"
extern TxraSoundVoice g_03007770[];
extern u32 g_03007404,g_03007574,g_03007578,g_03007570;
extern u32 g_03007590[];
extern u32 g_030075E8[],g_030075D8[],g_03006A88[],g_030079B0,g_030079B4;
extern u8 g_080076F4[],g_03006AA0[],g_08006271[],g_030068A0[];
void func_08007398(void) {
 s32 i; u32 offset; vu16 *wave,*p; vu32 *dma;
 g_03007770[0].field_00=0;
 g_03007770[1].field_00=0;
 g_03007770[2].field_00=0;
 g_03007770[3].field_00=0;
 g_03007770[4].field_00=0;
 g_03007770[5].field_00=0;
 g_03007770[6].field_00=0;
 g_03007770[7].field_00=0;
 g_03007404=256;
 g_03007574=0;
 g_03007578=7;
 g_03007570=0;
 wave=(vu16*)0x04000090;
 for(i=0;i<=3;i++) ((u16*)wave)[i]=0xFFFF;
 for(i=4;i<=7;i++) wave[i]=0;
 *(vu16*)0x04000080=0xFF0E;
 *(vu16*)0x04000084=0x008F;
 *(vu16*)0x04000082=0xFB0E;
 *(vu16*)0x04000070=0x00C0;
 wave=(vu16*)0x04000090;
 for(i=0;i<=3;i++) ((u16*)wave)[i]=0xFFFF;
 for(i=4;i<=7;i++) wave[i]=0;
 *(vu16*)0x04000060=8;
 g_03007590[0]=0;
 g_03007590[3]=0;
 g_03007590[6]=0;
 g_03007590[9]=0;
 g_03007590[12]=0;
 g_03007590[15]=0;
 for(i=0;i<=1;i++) { g_03006A88[i]=0; g_030075D8[i]=0; g_030075E8[i]=0; }
 dma=(vu32*)0x040000D4;
 dma[0]=(u32)g_080076F4; dma[1]=(u32)g_03006AA0; dma[2]=0x84000258; dma[2];
 dma[0]=(u32)g_08006271; dma[1]=(u32)g_030068A0; dma[2]=0x84000078; dma[2];
 g_030079B0=7;
 g_030079B4=0;
}
