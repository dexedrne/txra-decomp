/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Distinct range-end symbols intentionally resolve to the next range starts.
 * Keeping their source identities separate preserves the original copy setup. */
extern u8 gUnk_08000BF0[],gUnk_08001218[],gUnk_080005D8[],gUnk_080018B4[];
extern u8 g_080005D8[],g_08000BF0[],g_08001218[],g_080002CC[],g_080018B4[];
extern u8 g_03004790[],g_030014D0[],g_03001B30[],g_03002E60[];
extern u8 g_080165BC[],g_03002340[],g_08016C18[],g_03000020[],g_08016DA8[],g_03003540[];
extern u8 g_08017E68[],g_030066E0[],g_08017F64[],g_03005830[],g_080181C0[],g_03000E00[];
#define DEEP_COPY(source,destination,count) \
    dma[0]=(u32)(source); dma[1]=(u32)(destination); dma[2]=(count)|0x84000000; dma[2]
void func_08018854(void)
{
    vu32 *dma=(vu32 *)0x040000D4;
    DEEP_COPY(g_080005D8,g_03004790,(gUnk_08000BF0-g_080005D8)/4);
    DEEP_COPY(g_08000BF0,g_030014D0,(gUnk_08001218-g_08000BF0)/4);
    DEEP_COPY(g_080002CC,g_03001B30,(gUnk_080005D8-g_080002CC)/4);
    DEEP_COPY(g_08001218,g_03002E60,(gUnk_080018B4-g_08001218)/4);
    DEEP_COPY(g_080165BC,g_03002340,0x1B5);
    DEEP_COPY(g_08016C18,g_03000020,0x64);
    DEEP_COPY(g_08016DA8,g_03003540,0x465);
    DEEP_COPY(g_08017E68,g_030066E0,0x40);
    DEEP_COPY(g_08017F64,g_03005830,0xC0);
    DEEP_COPY(g_080181C0,g_03000E00,0x1A9);
}
