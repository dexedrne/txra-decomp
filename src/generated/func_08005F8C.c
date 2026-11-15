/* Byte-verified C; address name retained pending semantic review. */
#ifndef TXRA_BASIC_TYPES
#define TXRA_BASIC_TYPES
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#endif
#include "types.h"
#include "types.h"
extern TxraSoundVoice g_03007770[8];
extern u32 g_083C1070[][9];
extern u32 g_03007580,g_030079C0,g_030075F0,g_030079B0,g_030079B4;
void func_08005F8C(u32 n)
{
 s32 i;
 for(i=0;i<=7;i++) {
  g_03007770[i].field_20=g_083C1070[n][i];
  g_03007770[i].field_08=0;
  g_03007770[i].field_24=0;
  g_03007770[i].field_0c=0;
  g_03007770[i].field_14=96;
  g_03007770[i].field_10=0;
  g_03007770[i].field_00=1;
  g_03007770[i].field_04=1;
  g_03007770[i].field_38=-1;
  g_03007770[i].field_30=0;
 }
 g_03007580=g_083C1070[n][8];
 g_030079C0=0;
 g_030075F0=n;
 g_030079B0=7;
 g_030079B4=0;
}
