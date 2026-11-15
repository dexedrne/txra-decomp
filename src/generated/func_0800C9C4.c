/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern TxraRecord g_03001E60[];
extern s32 g_03002E4C,g_030021D4;
extern s16 g_030021CC;
extern TxraRow28 *g_03006874;
extern s32 g_083D2280[],g_083C2280[],g_083C1A80[];
extern s32 func_08014614(s32,s32);
void func_0800C9C4(s32 index)
{
    s32 at=g_03001E60[index].field_38;
    s32 next=at+1;
    s32 after;
    TxraRow28 *base,*a,*b; s32 *xaddr;
    s32 x,z,angle,fraction,height,nextheight,slope,result;
    if (next >= g_03002E4C) next=0;
    after=next+1;
    if (after >= g_03002E4C) after=0;
    xaddr=&g_03001E60[index].field_04;
    base=g_03006874;
    a=&base[at];
    x=*xaddr-a->field_00;
    z=g_03001E60[index].field_0c-a->field_08;
    angle=(4096-a->field_0c)&16383;
    { s32 sine=g_083D2280[angle]; s32 cosine=g_083C2280[angle]; fraction=(x*cosine+z*sine)>>12; }
    b=&base[next];
    height=a->field_04+(((b->field_04-a->field_04)*fraction)>>9);
    g_03001E60[index].field_08=-height;
    nextheight=b->field_04+(((base[after].field_04-b->field_04)*fraction)>>9);
    slope=g_083C1A80[((nextheight-height)>>1)+256]-4096;
    angle=func_08014614(slope,g_03001E60[index].field_20-a->field_0c)&16383;
    result=g_03001E60[index].field_24=((g_083C2280[angle]*slope)/4096)&16383;
    if (g_030021D4==0) {
        slope=result; if (slope>8191) slope-=16384;
        g_03002E40.field_08=slope+12192;
    }
    if (g_030021D4==1) {
        slope=g_03001E60[index].field_24;
        if (slope>8191) slope-=16384;
        if (g_030021CC==0) g_03002E40.field_08=11992;
    }
}
