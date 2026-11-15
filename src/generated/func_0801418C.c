/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
#include "types.h"
extern TxraSlot32 g_03000B60[4];
s32 func_0801418C(s32 group,s32 current)
{
    s32 slot=(current+1)&3;
    s32 tries=0;
    for(;tries<=3;tries++){
        if (g_03000B60[slot].field_00) {
            if (group==0 && g_03000B60[slot].field_02>15 && g_03000B60[slot].field_02<=21) break;
            if (group==1 && g_03000B60[slot].field_02>21 && g_03000B60[slot].field_02<=26) break;
            if (group==2 && g_03000B60[slot].field_02>26 && g_03000B60[slot].field_02<=31) break;
        }
        slot=(slot+1)&3;
        
    }
    return slot;
}
