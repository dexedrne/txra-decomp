/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
#define DMA3SET(src,dst,ctl) { vu32 *dmaRegs=(vu32*)0x040000D4; dmaRegs[0]=(u32)(src); dmaRegs[1]=(u32)(dst); dmaRegs[2]=(u32)(ctl); dmaRegs[2]; }
extern s32 g_0300000C,g_03000004,g_03000008,g_03001E5C,g_03000018,g_03001E54;
extern u8 g_08269B84[],g_08259B84[],g_08261B84[],g_08271B84[];
void func_08014CE4(u16 page)
{
    s32 width,h,x,bytes,i;
    u32 scroll;
    u8 *src,*dst,*s;
    g_0300000C=width=120;
    g_03000004=scroll=(-g_03002E40.field_04>>6)&255;
    g_03000008=g_03001E5C+128;
    h=g_03000008+128;
    if(h>120) h=120;
    if(g_03000018==0) src=g_08269B84;
    if(g_03000018==1) src=g_08259B84;
    if(g_03000018==2) src=g_08261B84;
    if(g_03000018==3) src=g_08271B84;
    if(scroll&1) src=(u8*)0x02008000;
    dst=(u8*)0x0600A000;
    if(page) dst=(u8*)0x06000000;
    x=scroll>>1;
    {
        s=src-(g_03000008<<8);
        bytes=width-x;
        dst+=x*2;
        bytes*=2;
        if(x<=119) {
            for(i=0;i<h;i++) {
                DMA3SET(s,dst,0x80000000|(bytes/2));
                s+=256; dst+=240;
            }
        }
    }
    dst=(u8*)0x0600A000;
    if(page) dst=(u8*)0x06000000;
    x=(g_03000004>>1)&127;
    {
        s=src-(g_03000008<<8);
        s+=(128-x)*2;
        bytes=x;
        if(bytes>0) {
            bytes*=2;
            if(bytes>240) bytes=240;
            {
                    for(i=0;i<h;i++) {
                    DMA3SET(s,dst,0x80000000|(bytes/2));
                    s+=256; dst+=240;
                }
            }
        }
    }
    dst=(u8*)0x0600A000;
    if(page) dst=(u8*)0x06000000;
    if((u32)h<=159) {
        vu32 fill;
        u32 c=g_03001E54;
        fill=c+(c<<8)+(c<<16)+(c<<24);
        DMA3SET(&fill,dst+h*240,0x85000000|((160-h)*240/4));
    }
}
