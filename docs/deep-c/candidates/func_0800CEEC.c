/* Unmatched source hypothesis; excluded from the ROM build. */
#include "types.h"
typedef struct {
 s16 field_00,field_02;
 u32 field_04,field_08,field_0c;
 s32 field_10,field_14,field_18,field_1c;
 s32 field_20,field_24,field_28;
 s32 field_2c,field_30;
 s32 field_34;
 s16 field_38;
 s16 field_3a,field_3c,field_3e;
 u8 gap40[2];
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
extern s16 g_030021CC;
extern s32 g_083D2280[],g_083C2280[];
extern s32 func_08014614(u32,u32);
extern void func_0801604C(u32,u32);
void func_0800CEEC(s32 slot) {
 Record100 *base=g_03001E60;
 Record100 *p=base+slot;
 s32 n=p->field_38;
 TxraRow28 *row;
 s32 x,z,a,c,s,lateral,forward,diff;
 u32 *xfield;
 xfield=&g_03001E60[slot].field_04;
 {u32 base=(u32)g_03006874;row=(TxraRow28*)(n*28+base);}
 x=*xfield-row->field_00;
 z=g_03001E60[slot].field_0c-row->field_08;
 a=(4096-row->field_0c)&16383;
 c=g_083D2280[a];
 lateral=x*c;
 s=g_083C2280[a];
 lateral=(lateral-z*s)>>12;
 forward=(x*s+z*c)>>12;
 if((u32)(lateral+850)>1700) {
  if(lateral < -850) {
   lateral=-840;
   diff=func_08014614((row->field_0c+8192)&16383,g_03001E60[slot].field_20)&16383;
   if(diff>8191)diff-=8192;
   if(diff>4096)diff=8192-diff;
   p->field_3c=(4096-diff)/6+256;
   p->field_3a=g_03006874[n].field_0c&16383;
   p->field_3e=(g_03001E60[slot].field_20-(diff>>2))&16383;
   g_03001E60[slot].field_30=0;
   g_03001E60[slot].field_28=g_03001E60[slot].field_28*diff>>12;
   if(slot==0 && !g_030021CC)func_0801604C(28,1);
  }
  if(lateral >850) {
   lateral=840;
   diff=func_08014614(g_03006874[n].field_0c&16383,g_03001E60[slot].field_20)&16383;
   if(diff>8191)diff-=8192;
   if(diff>4096)diff=8192-diff;
   p->field_3c=(4096-diff)/6+256;
   p->field_3a=(g_03006874[n].field_0c+8192)&16383;
   p->field_3e=(g_03001E60[slot].field_20+(diff>>2))&16383;
   g_03001E60[slot].field_30=0;
   g_03001E60[slot].field_28=g_03001E60[slot].field_28*diff>>12;
   if(slot==0 && !g_030021CC)func_0801604C(28,1);
  }
  a=(16384-a)&16383;
  c=g_083D2280[a];
  x=lateral*c;
  s=g_083C2280[a];
  x=(x-forward*s)>>12;
  z=(lateral*s+forward*c)>>12;
  g_03001E60[slot].field_04=g_03006874[n].field_00+x;
  g_03001E60[slot].field_0c=g_03006874[n].field_08+z;
 }
}
