/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u32 g_03001B24,g_03000DF0,g_03006690[];
extern u8 g_03000BE0[];
extern s32 g_030067E4;
extern TxraTransfer g_030061F0[];
extern u16 g_030001F0[][6];
void func_0801533C(u32 source, u32 destination, u32 size, u32 a0,
                   u32 a1,u32 a2,u32 a3,u32 a4,u32 palette)
{
    u32 sprite = g_03001B24;
    u32 palette_base;
    if (palette > 15) {
        if (g_03000DF0 == 0) {
            vu32 *dma; palette_base=(u32)g_03000BE0; dma=(vu32 *)0x040000D4;
            dma[0]=palette;
            dma[1]=palette_base;
            dma[2]=0x84000008;
            dma[2];
            g_03006690[0]=palette;
            palette=0;
            g_03000DF0=1;
        } else {
            u32 found=0;
            u32 i=0;
            for (;i<g_03000DF0;i++) {
                if (g_03006690[i] == palette) { palette=i; found=1; break; }
            }
            if (!found) {
                i=g_03000DF0;
                if ((s32)i <= 15) {
                    vu32 *dma; palette_base=(u32)g_03000BE0; dma=(vu32 *)0x040000D4;
                    dma[0]=palette;
                    dma[1]=palette_base+(i<<5);
                    dma[2]=0x84000008;
                    dma[2];
                    g_03006690[i]=palette;
                    palette=i;
                    g_03000DF0++;
                }
            }
        }
    }
    a4 |= palette<<12;
    if (g_030067E4 <= 95 && destination+size <= 0x06018000) {
        if (source != 1) {
            s32 n=g_030067E4;
            g_030061F0[n].field_00=source;
            g_030061F0[n].field_04=destination;
            g_030061F0[n].field_08=size;
            g_030067E4=n+1;
            g_030061F0[n+1].field_00=0;
        }
        g_030001F0[sprite][0]=a0;
        g_030001F0[sprite][1]=a1;
        g_030001F0[sprite][2]=a2;
        g_030001F0[sprite][3]=a3;
        g_030001F0[sprite][4]=a4;
        sprite++;
    }
    g_03001B24=sprite;
}
