/* Unmatched source hypothesis from deep slice e; excluded from the ROM build. */
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
extern Record100 g_03001E60[];
extern s16 g_03002A1C,g_030021CC,g_030014B0;
extern u16 g_0300218C;
extern u32 g_030021D4;
extern TxraTriple g_03002E40,g_03005F70,g_03002320;
extern s32 g_083D2280[],g_083C2280[];
extern s32 (*g_083E2280[])(void);
extern void func_0800BDC0(s32),func_0800C3C4(s32),func_0800CB5C(s32),func_0800C850(s32),func_0800C9C4(s32),func_0800CEEC(s32);
extern void func_0801604C(u32,u32);
void func_0800BBD4(void) {
 s32 i,save_a,save_b;
 Record100 *base;
 s32 *third;
 TxraTriple *angles;
 if(((g_03002A1C==0 && (g_0300218C&512)) || (g_03002A1C==1 && (g_0300218C&4))) && g_030021CC==0) {
  if(g_030021D4==0)g_030021D4=1;else g_030021D4=0;
 }
 i=7;
 do {
  if(g_03001E60[i].field_00) {
   g_03001E60[i].field_10=g_03001E60[i].field_04;
   g_03001E60[i].field_14=g_03001E60[i].field_08;
   g_03001E60[i].field_18=g_03001E60[i].field_0c;
   if(i!=g_030014B0){save_a=g_03002E40.field_04;save_b=g_03002E40.field_08;}
   func_0800BDC0(i);func_0800C3C4(i);func_0800CB5C(i);func_0800C850(i);func_0800C9C4(i);func_0800CEEC(i);
   if(i!=g_030014B0){g_03002E40.field_04=save_a;g_03002E40.field_08=save_b;}
  }
  i--;
 }while(i>=0);
 if(g_083E2280[0]()==1)func_0801604C(22,1);
 if(g_030021D4==0) {
  s32 scale=-640;
  s32 a=((g_03001E60[0].field_34>>3)+4096)&16383;
  s32 dx=g_083D2280[a]*scale>>12;
  s32 dz=g_083C2280[a]*scale>>12;
  g_03005F70.field_00=g_03001E60[0].field_04+dx;
  g_03005F70.field_04=g_03001E60[0].field_08+120;
  g_03005F70.field_08=g_03001E60[0].field_0c+dz;
  g_03002320.field_08=1000;
 }
 if(g_030021D4==1) {
  s32 scale=g_03001E60[0].field_28>>3;
  s32 a,dx,dz;
  if(scale>128)scale=128;
  a=(12288-g_03002E40.field_04)&16383;
  dx=g_083D2280[a]*scale>>12;
  dz=g_083C2280[a]*scale>>12;
  if(g_030021CC==0) {
   g_03005F70.field_00=g_03001E60[0].field_04+dx;
   g_03005F70.field_04=g_03001E60[0].field_08+180;
   g_03005F70.field_08=g_03001E60[0].field_0c+dz;
  }
  g_03002320.field_08=900;
 }
}
