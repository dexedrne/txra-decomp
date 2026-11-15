#include "types.h"
extern s32 g_03000018;
extern u8 g_08269B84[],g_08259B84[],g_08261B84[],g_08271B84[];
extern u8 g_02008000[];
void func_08014C5C(void)
{
    u8 *source;
    u8 *dest;
    s32 row,col;
    u32 value;
    if(g_03000018==0)source=(u8 *)g_08269B84;
    if(g_03000018==1)source=(u8 *)g_08259B84;
    if(g_03000018==2)source=(u8 *)g_08261B84;
    if(g_03000018==3)source=(u8 *)g_08271B84;
    dest=(u8 *)g_02008000;
    for(row=0;row<=127;row++) {
        for(col=0;col<=127;col++) {
            value=*(u8 *)((u8 *)source+(row<<8)+(col<<1));
            *(u16 *)((col<<1)+(s32)dest+(row<<8))=
                (*(u16 *)((row<<8)+((((col-1)&127)<<1)+(s32)source))>>8)|(value<<8);
        }
    }
}
