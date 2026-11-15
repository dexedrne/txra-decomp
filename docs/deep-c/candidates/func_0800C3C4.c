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
 s16 field_40;
 s16 field_42,field_44;
 u8 gap46[2];
 s16 field_48;
 u8 gap4a[2];
 s16 field_4c,field_4e,field_50,field_52;
 s16 field_54,field_56,field_58;
 s16 field_5a;
 s16 field_5c;
 s16 field_5e,field_60;
 s16 field_62;
} Record100;
extern Record100 g_03001E60[];
extern s32 func_08014614(s32,s32);
extern void func_0801604C(u32,u32);
extern u32 g_030021D4;
extern s16 g_030021CC;
extern TxraTriple g_03002E40;
void func_0800C3C4(s32 slot) {
 Record100 *base=g_03001E60;
 Record100 *p=base+slot;
 s32 steer,diff,tilt;
 if(p->field_40>0)p->field_40--;
 steer=g_03001E60[slot].field_30;
 if(p->field_44&32) {
  if(steer>p->field_56)steer=p->field_56-350;
  if(steer>0)steer-=250;
  steer-=p->field_54;
  if(steer < -p->field_58 && g_03001E60[slot].field_28>1920) {
   g_03001E60[slot].field_28-=64;
   steer=-p->field_58;
   if(slot==0 && !g_03001E60[0].field_40) {
    func_0801604C(14,1);g_03001E60[0].field_40=64;
    if(!g_03001E60[0].field_3c) {
     g_03001E60[0].field_3c=16;
     g_03001E60[0].field_3a=(g_03001E60[0].field_20-4096)&16383;
     g_03001E60[0].field_3e=g_03001E60[0].field_20&16383;
    }
   }
  }
 }
 if(p->field_44&16) {
  if(steer < -p->field_56)steer=350-p->field_56;
  if(steer<0)steer+=250;
  steer+=p->field_54;
  if(steer > p->field_58 && g_03001E60[slot].field_28>1920) {
   g_03001E60[slot].field_28-=64;
   steer=p->field_58;
   if(slot==0 && !g_03001E60[0].field_40) {
    func_0801604C(14,1);g_03001E60[0].field_40=64;
    if(!g_03001E60[0].field_3c) {
     g_03001E60[0].field_3c=16;
     g_03001E60[0].field_3a=(g_03001E60[0].field_20+4096)&16383;
     g_03001E60[0].field_3e=g_03001E60[0].field_20&16383;
    }
   }
  }
 }
 if(!(p->field_44&32) && !(p->field_44&16)) {
  if(steer < -p->field_56)steer=-p->field_56;
  if(steer > p->field_56)steer=p->field_56;
  if(steer)steer-=steer>>2;
 }
 g_03001E60[slot].field_30=steer;
 if(steer < -p->field_56)steer=-p->field_56;
 if(steer > p->field_56)steer=p->field_56;
 if(g_03001E60[slot].field_28<0) {
  steer=-steer;steer>>=1;
  g_03001E60[slot].field_20=(g_03001E60[slot].field_20-(steer>>3))&16383;
 }
 if(g_03001E60[slot].field_28>0) {
  steer>>=1;
  g_03001E60[slot].field_20=(g_03001E60[slot].field_20-(steer>>3))&16383;
 }
 diff=func_08014614(g_03001E60[slot].field_20,(g_03006874[p->field_38].field_0c+4096)&16383);
 if(diff>8191)diff-=8192;
 if(diff < -3600)g_03001E60[slot].field_20=g_03006874[p->field_38].field_0c+7694;
 if(diff > 3600)g_03001E60[slot].field_20=g_03006874[p->field_38].field_0c+498;
 g_03001E60[slot].field_20&=16383;
 diff=func_08014614(g_03001E60[slot].field_34>>3,g_03001E60[slot].field_20);
 if(diff>8191)diff-=16384;
 g_03001E60[slot].field_34=(g_03001E60[slot].field_34+(diff<<3))&131071;
 tilt=0;
 if(steer>400)tilt=(((steer-400)>>1)*g_03001E60[slot].field_28)>>14;
 if(steer < -400)tilt=(((steer+400)>>1)*g_03001E60[slot].field_28)>>14;
 if(tilt>p->field_4e)p->field_4e++;
 if(tilt<p->field_4e)p->field_4e--;
 if(g_030021D4==1 && !g_030021CC) {
  diff=func_08014614((8192-(g_03001E60[slot].field_34>>3))&16383,g_03002E40.field_04)&16383;
  if(diff>8191)diff-=16384;
  if((u32)(diff+4)>8) {
   diff>>=2;if(diff < -60)diff=-60;if(diff>60)diff=60;
   g_03002E40.field_04-=diff;
  } else {if(diff<0)g_03002E40.field_04++;if(diff>0)g_03002E40.field_04--;}
  diff=func_08014614((4096-g_03002E40.field_04)&16383,g_03006874[p->field_38].field_0c&16383);
  if(diff>8191)diff-=16384;
  if(diff < -768)g_03002E40.field_04=3328-g_03006874[p->field_38].field_0c;
  if(diff >768)g_03002E40.field_04=4864-g_03006874[p->field_38].field_0c;
  g_03002E40.field_04&=16383;
 }
 if(!g_030021D4)g_03002E40.field_04=(8192-g_03001E60[slot].field_20)&16383;
}
