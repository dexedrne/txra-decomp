/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Blend a mode-selected sprite into the alternate VRAM page. A zero byte
 * of each source halfword preserves that destination byte. The two source
 * expressions and the second pixel's two destination expressions retain
 * the original induction pointers and address-addition order. */
extern u32 g_03005FC0;
extern s16 g_03001E50;
extern u8 g_08327BDC[],g_08327C1C[],g_08327C5C[],g_0832BA5C[],g_0832BA9C[],g_0832BAE4[];
void func_08017F64(void)
{
    u32 temp;
    s32 width,height;
    u8 *source;
    u8 *dest;
    s32 row,column;
    s32 mode;

    if (!g_03005FC0) dest=(u8 *)0x0600A000;
    else dest=(u8 *)0x06000000;
    mode=g_03001E50;
    if(mode==0){width=25;height=72;dest+=0x4EC8;source=g_08327BDC;}
    if(mode==1){width=25;height=80;dest+=0x4B08;source=g_08327C1C;}
    if(mode==2){width=32;height=64;dest+=0x5280;source=g_08327C5C;}
    if(mode==3){width=29;height=66;dest+=0x5194;source=g_0832BA5C;}
    if(mode==4){width=34;height=48;dest+=0x5A02;source=g_0832BA9C;}
    if(mode==5){width=32;height=64;dest+=0x5282;source=g_0832BAE4;}
    for(row=0;row<height;) {
        s32 next=row+1;
        for(column=0;column<width;column+=2) {
            u16 *d=(u16 *)(dest+row*240);
            u32 value;
            value=*(u16 *)(source+column*2+row*200);
            if (value) {
                if (!(value & 255)) {
                    temp = *(u8 *)&(*(u16 *)(dest + column * 2 + row * 240));
                    *(u16 *)(dest + column * 2 + row * 240) = temp + value;
                } else if (!(value & 0xFF00)) {
                    temp = *(u16 *)(dest + column * 2 + row * 240) & 0xFF00;
                    *(u16 *)(dest + column * 2 + row * 240) = temp + value;
                } else {
                    *(u16 *)(dest + column * 2 + row * 240) = value;
                }
            }
            value=((u16 *)(source+column*2))[row*100+1];
            if (value) {
                if (!(value & 255)) {
                    temp = *(u8 *)&d[column + 1];
                    d[column + 1] = temp + value;
                } else if (!(value & 0xFF00)) {
                    temp = ((u16 *)(dest + column * 2))[row * 120 + 1] & 0xFF00;
                    ((u16 *)(dest + column * 2))[row * 120 + 1] = temp + value;
                } else {
                    ((u16 *)(dest + column * 2))[row * 120 + 1] = value;
                }
            }
        }
        row=next;
    }
}
