/* Unmatched source hypothesis; excluded from the ROM build. */
#include "types.h"
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
extern s32 g_03002E4C;
extern s32 g_083D2280[],g_083C2280[];
extern s16 g_030021CC;
extern u32 g_030001B8,g_03002334;
extern s32 g_03005F50;
extern void func_08002854(void);
void func_0800C850(s32 slot) {
 Record100 *base=g_03001E60;
 Record100 *p=base+slot;
 s32 current=p->field_38;
 s32 previous=current-1;
 s32 next;
 TxraRow28 *row;
 s32 x,z,angle,cosine,sine,lateral,forward;
 u32 *xfield;
 if(previous<0)previous+=g_03002E4C;
 next=current+1;
 if(next>=g_03002E4C)next=0;
 xfield=&g_03001E60[slot].field_04;
 {u32 base=(u32)g_03006874;row=(TxraRow28*)(current*28+base);}
 x=*xfield-row->field_00;
 z=g_03001E60[slot].field_0c-row->field_08;
 angle=(4096-row->field_0c)&16383;
 cosine=g_083D2280[angle];
 lateral=x*cosine;
 sine=g_083C2280[angle];
 lateral=(lateral-z*sine)>>12;
 forward=(x*sine+z*cosine)>>12;
 p->field_42=(lateral+768)>>4;
 if(forward>511) {
  current=next;
  if(slot==0 && g_030021CC==0) {
   g_030001B8=(g_030001B8+1)&31;
   g_03002334=slot;
   g_03005F50=current;
   func_08002854();
  }
 }
 if(forward<0) {
  if(slot==0 && g_030021CC==0) {
   if(current==next)g_030001B8-=2;
   else g_030001B8-=1;
   g_030001B8&=31;
   g_03002334=1;
  }
  current=previous;
  if(slot==0 && g_030021CC==0) {
   g_03005F50=current;
   func_08002854();
  }
 }
 g_03001E60[slot].field_38=current;
}
