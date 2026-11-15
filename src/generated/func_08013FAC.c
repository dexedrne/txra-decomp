/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern s16 g_03005788;
extern u8 g_0828FB84[],g_03002A30[],g_08306D60[],g_03002DB0[],g_082B3D9C[],g_03002C00[],g_0827A784[],g_03000BE0[],g_082C76CC[];
extern void func_0800A8A0(u32,void *,void *,s32,u32);
void func_08013FAC(s32 state)
{
    if(!g_03005788) {
        {
        vu32 *dma=(vu32 *)0x040000D4;
        u8 *dest;
        dma[0]=(u32)g_0828FB84;
        dest=g_03002A30;
        dma[1]=(u32)dest;
        dma[2]=0x84000060;
        dma[2];
        if(state==45) {
            dma[0]=(u32)g_08306D60;
        dma[1]=(u32)(dest+384);
        dma[2]=0x84000014;
        dma[2];
        } else {
            dma[0]=(u32)g_03002DB0;
        dma[1]=(u32)(dest+384);
        dma[2]=0x84000014;
        dma[2];
        }
        }
        {
        vu32 *dma=(vu32 *)0x040000D4;
        u8 *dest;
        dma[0]=(u32)g_082B3D9C;
        dma[1]=(u32)g_03002C00;
        dma[2]=0x8400000c;
        dma[2];
        dma[0]=(u32)g_0827A784;
        dest=g_03000BE0;
        dma[1]=(u32)dest;
        dma[2]=0x84000040;
        dma[2];
        dma[0]=(u32)g_082C76CC;
        dma[1]=(u32)(dest+256);
        dma[2]=0x84000040;
        dma[2];
        }
    } else {
        func_0800A8A0(3,g_0828FB84,g_03002A30,384,32);
        if(state==45)func_0800A8A0(3,g_08306D60,g_03002A30+384,80,32);
        else func_0800A8A0(3,g_03002DB0,g_03002A30+384,80,32);
        func_0800A8A0(3,g_082B3D9C,g_03002C00,48,32);
        func_0800A8A0(3,g_0827A784,g_03000BE0,256,32);
        func_0800A8A0(3,g_082C76CC,g_03000BE0+256,256,32);
        g_03005788--;
    }
}
