/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern s16 g_03005788;
extern u32 g_03000018;
extern u8 g_0827A384[],g_03002A30[],g_0827A0C4[],g_08279CC4[],g_08279EC4[],g_0827A2C4[],g_03002DB0[],g_082B3D9C[],g_0827A584[],g_03000BE0[],g_082C770C[];
extern void func_0800A8A0(u32,void *,void *,s32,u32);
void func_0800A68C(void) {
 if(!g_03005788) {
  vu32 *dma=(vu32*)0x040000D4;
  u8 *dest;
  dma[0]=(u32)g_0827A384;dest=g_03002A30;dma[1]=(u32)dest;dma[2]=0x84000050;dma[2];
  if(g_03000018==0){dma[0]=(u32)g_0827A0C4;dma[1]=(u32)(dest+320);dma[2]=0x84000010;dma[2];}
  if(g_03000018==1){dma[0]=(u32)g_08279CC4;dma[1]=(u32)(dest+320);dma[2]=0x84000010;dma[2];}
  if(g_03000018==2){dma[0]=(u32)g_08279EC4;dma[1]=(u32)(dest+320);dma[2]=0x84000010;dma[2];}
  if(g_03000018==3){dma[0]=(u32)g_0827A2C4;dma[1]=(u32)(dest+320);dma[2]=0x84000010;dma[2];}
  dma[0]=(u32)g_03002DB0;dma[1]=(u32)(dest+384);dma[2]=0x84000014;dma[2];
  dma[0]=(u32)g_082B3D9C;dma[1]=(u32)(dest+464);dma[2]=0x8400000C;dma[2];
  /* A separate destination lifetime is required for the second region. */
  {u8 *dest;dma[0]=(u32)g_0827A584;dest=g_03000BE0;dma[1]=(u32)dest;dma[2]=0x84000050;dma[2];
  dma[0]=(u32)g_082C770C;dma[1]=(u32)(dest+320);dma[2]=0x8400001C;dma[2];
 }
 } else {
  func_0800A8A0(3,g_0827A384,g_03002A30,320,32);
  if(g_03000018==0)func_0800A8A0(3,g_0827A0C4,g_03002A30+320,64,32);
  if(g_03000018==1)func_0800A8A0(3,g_08279CC4,g_03002A30+320,64,32);
  if(g_03000018==2)func_0800A8A0(3,g_08279EC4,g_03002A30+320,64,32);
  if(g_03000018==3)func_0800A8A0(3,g_0827A2C4,g_03002A30+320,64,32);
  func_0800A8A0(3,g_03002DB0,g_03002A30+384,80,32);
  func_0800A8A0(3,g_082B3D9C,g_03002A30+464,48,32);
  func_0800A8A0(3,g_0827A584,g_03000BE0,320,32);
  func_0800A8A0(3,g_082C770C,g_03000BE0+320,112,32);
  g_03005788--;
 }
}
