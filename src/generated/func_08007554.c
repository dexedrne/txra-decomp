/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern s32 g_03006880;
extern u8 g_083B8898[][4];
extern u16 *g_083B8A18[];
#include "types.h"
extern TxraTriple g_03007590[];
extern u32 g_03007774[][18];
void func_08007554(s32 a)
{
    s32 i;
    g_03006880=a;
    for(i=0;i<=3;i++) {
        u32 value=*(u8 *)(i+(a<<2)+(u32)g_083B8898);
        if(value!=255) {
            u16 *p=g_083B8A18[value];
            u32 index=*p++;
            g_03007590[index].field_00=(u32)p;
            g_03007590[index].field_04=-5;
            g_03007590[index].field_08=0;
            g_03007774[index][0]=0;
        }
    }
}
