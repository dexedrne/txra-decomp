/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern void func_080144F4(void),func_08014518(void),func_0801443C(void *,void *,u32);
extern u32 func_08005E28(void);
extern u8 g_03000DE8[],g_03005F64[],g_030014A4[],g_030001E0[],g_03005FA0[],g_03000B60[],g_03005680[],g_03001E60[];
extern u32 g_030021D4,g_03000DE4,g_03006870;
u32 func_08013C08(void) {
 u32 result; u8 *p,*q;  s32 i;
 func_080144F4();
 { u32 header=(u32)&gSaveStaging;
 for(i=0;i<512;i++) *(u8 *)(header+i)=i;
 *(u8 *)header++='T';*(u8 *)header++='X';*(u8 *)header++='R';*(u8 *)header='C'; header+=3;p=(u8 *)header; }
 func_0801443C(p,g_03000DE8,8);p+=8;
 func_0801443C(p,g_03005F64,2);p+=2;
 func_0801443C(p,g_030014A4,4);p+=4;
 func_0801443C(p,g_030001E0,12);p+=12;
 func_0801443C(p,g_03005FA0,30);p+=30;
 func_0801443C(p,g_03000B60,128);p+=128;
 q=g_03005680;
 for(i=127;i>=0;i--) {*p++=*q; q+=2;}
 *p++=((TxraRecord *)g_03001E60)->field_02;
 *p++=g_030021D4;*p=g_03000DE4;p[1]=g_03006870;
 result=func_08005E28();func_08014518();return result;
}
