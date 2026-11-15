/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
#include "types.h"
/* Local 400-byte spacing hypothesis; only the addressed fields are recovered. */
typedef struct {
 s16 field_00,field_02;
 u32 field_04,field_08,field_0c;
 u8 gap10[16];
 s32 field_20,field_24,field_28;
 u8 gap2c[8];
 s32 field_34;
 s16 field_38;
 u8 gap3a[8];
 s16 field_42,field_44;
 u8 gap46[2];
 s16 field_48;
 u8 gap4a[2];
 s16 field_4c,field_4e,field_50,field_52;
 u8 gap54[8];
 s16 field_5c;
 u8 gap5e[4];
 s16 field_62;
 u8 gap64[300];
} Record400;
extern Record400 g_03001E60[2];
extern s16 g_030066D0;
extern s32 g_03002E4C;
extern u32 g_03002E50;
extern void func_0800AF4C(u32);
void func_0800B254(void) {
 s32 key=g_030066D0;
 s32 n=g_03001E60[0].field_38+6;
 TxraRow28 *row,*next;
 u32 scale,delta;
 u32 *x;
 Record400 *dest;
 if(n>=g_03002E4C)n-=g_03002E4C;
 dest=&g_03001E60[1];
 dest->field_00=1;
 x=&g_03001E60[1].field_04;
 {u32 base=(u32)g_03006874;
 row=(TxraRow28*)(n*28+base);}
 next=row+1;
 delta=next->field_00-row->field_00;
 scale=g_03002E50;
 *x=row->field_00+(delta*scale>>4);
 g_03001E60[1].field_08=-(row->field_04+((u32)(next->field_04-row->field_04)*scale>>4));
 g_03001E60[1].field_0c=row->field_08+((u32)(next->field_08-row->field_08)*scale>>4);
 {s32 *angle=&g_03001E60[1].field_34;
 row+=3;
 *angle=((row->field_0c+4096)&16383)<<3;}
 g_03001E60[1].field_20=g_03001E60[1].field_34>>3;
 g_03001E60[1].field_24=0;
 dest->field_38=n;
 g_03001E60[1].field_4c=2;
 g_03001E60[1].field_48=48;
 g_03001E60[1].field_28=1600;
 g_03001E60[1].field_52=3;
 g_03001E60[1].field_44=0;
 g_03001E60[1].field_4e=0;
 g_03001E60[1].field_42=48;
 dest->field_02=6;
 g_03001E60[1].field_50=4;
 g_03001E60[1].field_62=key;
 g_03001E60[1].field_5c=0;
 func_0800AF4C(4);
}
