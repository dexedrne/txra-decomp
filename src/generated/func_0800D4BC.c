/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u8 g_03001E60[];
extern s32 g_03005F50,g_03002E4C;
void func_0800D4BC(void)
{
    s32 base=(s32)g_03001E60;
    s32 p=base+100;
    s32 end=base+300;
    do {
        if (*(s16 *)p) {
            s32 delta=*(s16 *)(p+56)-g_03005F50;
            s32 count=g_03002E4C;
            if(delta>count-32)delta-=count;
            else if(delta<-count+32)delta+=count;
            if((u32)(delta+10)>42)*(s16 *)p=0;
        }
        p+=100;
    } while(p<=end);
}
