/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u16 g_0300218C, gKeysHeld;
void func_08015D78(void)
{
    u16 keys = ~*(vu16 *)0x04000130;
    g_0300218C = keys & ~gKeysHeld;
    gKeysHeld = keys;
}
