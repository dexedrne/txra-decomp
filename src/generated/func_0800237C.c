/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern void func_08005D9C(u32,u32,u16,u32);
void func_0800237C(u32 x,u32 y,u32 endx,u32 endy,u32 color,u32 page)
{
    s32 dx,dy,sx,sy;
    u32 octant;
    s32 error,i;
    if (y > 159 && endy > 159) return;
    if (x > 119 && endx > 119) return;
    octant=-1;
    dx=endx-x;
    dy=endy-y;
    if (dx<0 && dy<0) { if(dx<dy){octant=0;sx=-1;sy=-1;}else{octant=4;sx=-1;sy=-1;} }
    if (dx>=0 && dy<0) { if(-dx<dy){octant=1;sx=1;sy=-1;}else{octant=5;sx=1;sy=-1;} }
    if (dx<0 && dy>=0) { if(-dx>dy){octant=2;sx=-1;sy=1;}else{octant=6;sx=-1;sy=1;} }
    if (dx>=0 && dy>=0) { if(dx>dy){octant=3;sx=1;sy=1;}else{octant=7;sx=1;sy=1;} }
    if (octant<=3) {
        error=0;
        if(octant==0){dx=-dx;dy=-dy;}
        if(octant==1)dy=-dy;
        if(octant==2)dx=-dx;
        for(i=0;i<=dx;i++) {
            func_08005D9C(x,y,(u16)color,page);
            error+=dy;
            x+=sx;
            if(error>=dx) {error-=dx;y+=sy;}
        }
    }
    if (octant-4<=3) {
        error=0;
        if(octant==4){dx=-dx;dy=-dy;}
        if(octant==5)dy=-dy;
        if(octant==6)dx=-dx;
        for(i=0;i<=dy;i++) {
            func_08005D9C(x,y,(u16)color,page);
            error+=dx;
            y+=sy;
            if(error>=dy) {error-=dy;x+=sx;}
        }
    }
}
