/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern TxraTriple g_03002E40,g_03005F80,g_03002320;
extern s32 g_083D2280[],g_083C2280[];
extern s32 g_03002A18,g_03001B28,g_03000DF8,g_03005F58;
void func_08016264(void)
{
    TxraTriple *source=&g_03002E40;
    s32 mask=16383;
    s32 a=source->field_04&mask;
    s32 b=source->field_08&mask;
    g_03002A18=g_083D2280[a];
    g_03001B28=g_083C2280[a];
    g_03000DF8=g_083D2280[b];
    g_03005F58=g_083C2280[b];
    g_03005F80.field_00=g_03002320.field_00;
    g_03005F80.field_04=g_03002320.field_04;
    g_03005F80.field_08=g_03002320.field_08;
    g_03002A18=g_083D2280[a];
    g_03001B28=g_083C2280[a];
}
