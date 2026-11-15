/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
#include "types.h"
/* Local 100-byte record layout; names denote recovered field offsets. */
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
} Record100;
extern Record100 g_03001E60[];
extern s16 g_03001E50;
extern s32 g_03002E4C;
extern u32 g_03002E50;
/* This call site supplies the selector in r1; the mapped callee also reads it globally. */
extern s32 func_0800D3F8(s32,s32);
extern void func_0800AF4C(u32);
void func_0800A00C(void) {
 s32 n,slot,search,left,found;
 Record100 *dest;
 u32 *x,*angle;
 TxraRow28 *row,*next;
 u32 delta,scale;
 slot=4; search=0; n=100;
 for(left=0;left<=3;left++) {
  found=func_0800D3F8(search,g_03001E50);
  if(found>=search) {
   dest=&g_03001E60[slot];
   dest->field_00=1;
   x=&g_03001E60[slot].field_04;
   {u32 base=(u32)g_03006874;row=(TxraRow28*)(n*28+base);}
   next=row+1;
   delta=next->field_00-row->field_00;
   scale=g_03002E50;
   *x=row->field_00+(delta*scale>>4);
   g_03001E60[slot].field_08=-(row->field_04+((u32)(next->field_04-row->field_04)*scale>>4));
   g_03001E60[slot].field_0c=row->field_08+((u32)(next->field_08-row->field_08)*scale>>4);
   angle=(u32*)&g_03001E60[slot].field_34;
   row+=3;
   *angle=((row->field_0c+4096)&16383)<<3;
   g_03001E60[slot].field_20=(s32)*angle>>3;
   g_03001E60[slot].field_24=0;
   dest->field_38=n;
   dest->field_4c=2;
   dest->field_48=48;
   g_03001E60[slot].field_28=0;
   dest->field_52=0;
   dest->field_44=0;
   dest->field_4e=0;
   dest->field_42=48;
   dest->field_02=6;
   dest->field_50=4;
   dest->field_62=found;
   dest->field_5c=0;
   func_0800AF4C(slot);
   search=found+1;
   n+=g_03002E4C>>3;
   slot++;
  }
 }
}
