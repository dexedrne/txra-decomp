/* Unmatched deep-f hypothesis; excluded from the ROM build. */
/* Unmatched source hypothesis; excluded from the ROM build. */
#include "types.h"
typedef struct {
 s16 field_00,field_02;
 u32 field_04,field_08,field_0c;
 s32 field_10,field_14,field_18,field_1c;
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
typedef struct {s32 value[4];} FourWords;
extern FourWords g_0801FF24;
extern s32 g_0801FF34[16];
extern Record100 g_03001E60[];
extern u16 g_03001B14;
extern u32 g_03005F90[4],g_03000000,g_03001B1C;
extern s32 g_03002E4C,g_083D2280[],g_083C2280[];
extern void *memcpy(void *,const void *,u32);
extern void func_0800AF4C(s32);
void func_0800B908(void) {
 FourWords lanes=g_0801FF24;
 s32 models[16];
 s32 slot,j,n,conflict,lane,angle;
 Record100 *p;
 u32 *xout;
 TxraRow28 *row;
 memcpy(models,g_0801FF34,64);
 if(g_03001B14==2 || g_03005F90[0] || g_03005F90[1] || g_03005F90[2] || g_03005F90[3])return;
 for(slot=1;slot<=2;slot++) {
  if(g_03001E60[slot].field_00)continue;
  conflict=0;
  n=g_03001E60[0].field_38+28;
  if(n>=g_03002E4C)n-=g_03002E4C;
  if(g_03001E60[0].field_28<=599) {
   n=g_03001E60[0].field_38-8;
   if(n<0)n+=g_03002E4C;
  }
  for(j=1;j<=3;j++) {
   if(g_03001E60[j].field_00) {
    if(g_03001E60[j].field_48==lanes.value[g_03000000&3] || (g_03001E60[j].field_38>n-4 && g_03001E60[j].field_38<n+4))conflict=1;
   }
  }
  if(g_03001E60[0].field_28<=599 && lanes.value[g_03000000&3]>g_03001E60[0].field_42-12 && lanes.value[g_03000000&3]<g_03001E60[0].field_42+12) {
   conflict=1;
   g_03000000=(g_03000000+1)&3;
  }
  if(conflict)continue;
  p=&g_03001E60[slot];
  p->field_00=1;
  xout=&g_03001E60[slot].field_04;
  {u32 base=(u32)g_03006874;row=(TxraRow28*)(n*28+base);}
  *xout=row->field_00;
  g_03001E60[slot].field_08=-row->field_04;
  g_03001E60[slot].field_0c=row->field_08;
  g_03001E60[slot].field_34=((row->field_0c+4096)&16383)<<3;
  g_03001E60[slot].field_20=g_03001E60[slot].field_34>>3;
  g_03001E60[slot].field_24=0;
  p->field_02=models[(g_03001B1C>>4)&15];
  p->field_38=n;p->field_4c=2;
  p->field_48=lanes.value[g_03000000&3];
  g_03001E60[slot].field_28=1800;
  p->field_52=3;p->field_50=4;p->field_5c=0;
  func_0800AF4C(slot);
  if(p->field_48<=39) {
   u16 a=g_03006874[p->field_38].field_0c;
   g_03001E60[slot].field_04+=(g_083D2280[a&16383]<<9)>>12;
   g_03001E60[slot].field_0c+=(g_083C2280[a&16383]<<9)>>12;
  }
  if(p->field_48>64) {
   angle=g_03006874[p->field_38].field_0c+8192;
   g_03001E60[slot].field_04+=(g_083D2280[angle&16383]<<9)>>12;
   g_03001E60[slot].field_0c+=(g_083C2280[angle&16383]<<9)>>12;
  }
  g_03000000++;
  break;
 }
}
