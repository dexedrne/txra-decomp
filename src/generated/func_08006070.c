/* Byte-verified C inside unit_08005C7C.c only; address name retained pending semantic review.
 * Compiled alone, global CSE visits the hoisted address constants in a different
 * order and two of them swap registers: see docs/COMPILER.md. */
#ifndef TXRA_BASIC_TYPES
#define TXRA_BASIC_TYPES
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#endif
extern u32 g_03007570;
extern u32 g_03007590[];
extern u32 g_030075D8[],g_03007408[],g_030075E8[],g_03006898[],g_03006A88[],g_030075E0[],g_030079D0[],g_03006888[],g_03006890[],g_03006A90[],g_03007760[],g_030079B8[];
extern u32 g_030079C8,g_030079B0,g_030079C4,g_030079B4;
void func_08006070(void)
{
    s32 i;
    g_03007570=1;
    if(g_03007590[0]==0) { *(vu16*)0x04000062=0; *(vu16*)0x04000064=0; }
    if(g_03007590[3]==0) { *(vu16*)0x04000068=0; *(vu16*)0x0400006C=0; }
    if(g_03007590[6]==0) { *(vu16*)0x04000072=0; *(vu16*)0x04000074=0; }
    if(g_03007590[9]==0) { *(vu16*)0x04000078=0; *(vu16*)0x0400007C=0; }
    for(i=0;i<=1;i++) {
        g_03007408[i]=g_030075D8[i];
        g_03006898[i]=g_030075E8[i];
        g_030075E0[i]=g_03006A88[i];
        g_03006888[i]=g_030079D0[i];
        g_03006A90[i]=g_03006890[i];
        g_030079B8[i]=g_03007760[i];
        g_03006A88[i]=0;
    }
    g_030079C8=g_030079B0;
    g_030079C4=g_030079B4;
    g_030079B0=7;
    g_030079B4=0;
}
