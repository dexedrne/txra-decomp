/* Byte-verified ARM branch veneer; address name retained. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern void arm_func_080000C0(void);
void func_08000000(void) { arm_func_080000C0(); }
