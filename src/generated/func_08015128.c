/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u16 g_03002A30[];
void func_08015128(s32 t)
{
    s32 i;
    s32 r,g,b;
    u16 *target;
    if(t<=127 && (t&3)==0) {
        for(i=0;i<256;i++) {
            s32 tr,tg,tb;
            r=g_03002A30[i]&31; g=(g_03002A30[i]>>5)&31; b=(g_03002A30[i]>>10)&31;
            tr=*target&31; tg=(*target>>5)&31; tb=(*target>>10)&31;
            if(r<tr) r++;
            if(g<tg) g++;
            if(b<tb) b++;
            g_03002A30[i]=r+(g<<5)+(b<<10);
            target++;
        }
    }
    if((u32)(t-256)<=127) {
        for(i=0;i<256;i++) {
            r=g_03002A30[i]&31; g=(g_03002A30[i]>>5)&31; b=(g_03002A30[i]>>10)&31;
            if(r>0) r--;
            if(g>0) g--;
            if(b>0) b--;
            g_03002A30[i]=r+(g<<5)+(b<<10);
        }
    }
}
