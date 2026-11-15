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
 u8 gap54[6];
 s16 field_5a;
 s16 field_5c;
 s16 field_5e,field_60;
 s16 field_62;
} Record100;
typedef struct {s16 field_00,field_02;} Pair4;
extern Record100 g_03001E60[];
extern Pair4 g_030046E0[][5];
extern s16 g_03002A1C,g_03005F54;
extern u16 g_030001BC,g_0300218C;
extern s32 g_083D2280[],g_083C2280[];
extern s32 func_08014614(s32,s32);
void func_0800CB5C(s32 slot) {
 Record100 *p=&g_03001E60[slot];
 s32 old_x=g_03001E60[slot].field_04,old_z=g_03001E60[slot].field_0c;
 s32 gear,heading,step,diff;
 g_03001E60[slot].field_2c=0;
 if((p->field_44&1) && !(p->field_44&2))g_03001E60[slot].field_2c=g_030046E0[slot][p->field_52].field_00;
 if(p->field_44&2)g_03001E60[slot].field_2c=-512;
 g_03001E60[slot].field_28+=g_03001E60[slot].field_2c>>3;
 if(slot!=0 || !g_03002A1C || g_03005F54 || (g_030001BC&32)) {
  gear=p->field_52;
  if(g_03001E60[slot].field_28>g_030046E0[slot][gear].field_02) {
   if(gear<=3) {
    if(p->field_5c>p->field_5a){p->field_52++;p->field_5c=0;}
    else{p->field_5c++;g_03001E60[slot].field_28-=64;}
   }
  } else if(gear>0 && g_03001E60[slot].field_28<g_030046E0[slot][gear-1].field_02-8)p->field_52--;
 } else {
  if(g_03001E60[0].field_28>g_030046E0[0][g_03001E60[0].field_52].field_02+g_030046E0[0][g_03001E60[0].field_52].field_00 && g_03001E60[0].field_52<=3)g_03001E60[0].field_28-=g_030046E0[0][g_03001E60[0].field_52].field_00;
  if((g_0300218C&256) && p->field_52<=3)p->field_52++;
  if((g_0300218C&512) && p->field_52>0)p->field_52--;
 }
 if(g_03001E60[slot].field_28 < -512)g_03001E60[slot].field_28=-512;
 if(g_03001E60[slot].field_28 > p->field_60)g_03001E60[slot].field_28=p->field_60;
 step=g_03001E60[slot].field_28>>3;
 heading=((g_03001E60[slot].field_34>>3)+12288)&16383;
 g_03001E60[slot].field_04=old_x+(g_083D2280[heading]*step>>12);
 g_03001E60[slot].field_0c=old_z+(g_083C2280[heading]*step>>12);
 step=p->field_3c>>3;
 heading=(p->field_3a+12288)&16383;
 g_03001E60[slot].field_04+=g_083D2280[heading]*step>>12;
 g_03001E60[slot].field_0c+=g_083C2280[heading]*step>>12;
 if(p->field_3c>0){p->field_3c-=256;if(p->field_3c<0)p->field_3c=0;}
 if(p->field_3c<0){p->field_3c+=256;if(p->field_3c>0)p->field_3c=0;}
 if(p->field_3c) {
  diff=func_08014614(g_03001E60[slot].field_20,p->field_3e);
  if(diff>8191)diff-=16384;
  g_03001E60[slot].field_20=(g_03001E60[slot].field_20+(diff>>1))&16383;
 }
 if(p->field_3c>192 && g_03001E60[slot].field_28>1600)g_03001E60[slot].field_28-=64;
 if(g_03001E60[slot].field_28>6)g_03001E60[slot].field_28-=6;
 else if(g_03001E60[slot].field_28>0)g_03001E60[slot].field_28--;
 else if(g_03001E60[slot].field_28 < -4)g_03001E60[slot].field_28+=4;
 else if(g_03001E60[slot].field_28<0)g_03001E60[slot].field_28++;
}
