/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u16 gKeysHeld,g_03007FF8;
extern s32 g_03005F44,g_03002184,g_030014A8;
extern u32 g_030001B4,g_03001B1C,g_03000B50;
extern u8 gOamShadow[],g_030021E0[];
extern void func_08007510(s32),func_08015D78(void),func_08005E14(void),func_080063D4(void),func_08015D08(void);
void func_08014E8C(void)
{
 if((gKeysHeld&1) && (gKeysHeld&14)==14 && g_03005F44==1){
 vu16 zero;
 *(vu32 *)0x040000b8=0;*(vu16 *)0x04000208=0;*(vu32 *)0x040000b8=0;*(vu16 *)0x04000000=0;
 func_08007510(0);func_08007510(1);
 *(vu16 *)0x04000080=0;*(vu16 *)0x04000084=0;*(vu16 *)0x04000082=0;
 zero=0;
 {vu32 *dma=(vu32 *)0x040000d4;
 dma[0]=(u32)&zero;dma[1]=0x05000000;dma[2]=0x81000100;dma[2];
 zero=0;dma[0]=(u32)&zero;dma[1]=0x05000200;dma[2]=0x81000100;dma[2];}
 for(;;){do {func_08015D78();}while((gKeysHeld&1)&&(gKeysHeld&14)==14);func_08005E14();}
 }
 if(!g_03002184)func_080063D4();
 func_08015D08();
 {vu32 *dma=(vu32 *)0x040000d4;
 dma[0]=(u32)gOamShadow;dma[1]=0x07000000;dma[2]=0x84000100;dma[2];}
 *(vu32 *)0x040000b8=0;
 if(g_030014A8){*(vu32 *)0x040000b0=(u32)g_030021E0;*(vu32 *)0x040000b4=0x05000000;*(vu32 *)0x040000b8=0xa2400001;}
 *(vu16 *)0x04000000|=4096;
 g_030001B4++;g_03001B1C++;g_03000B50++;g_03007FF8=1;
 *(vu16 *)0x04000004=(*(vu16 *)0x04000004&255)|0x2720;
}
