/* Unmatched source hypothesis; excluded from the ROM build. */
#include "types.h"
extern TxraRecord g_03001E60[];
extern TxraTriple g_03005F80,g_03005F70,g_030057A0[],g_030055F0[];
extern s32 g_083D2280[],g_083C2280[],g_0804F330[];
extern s32 g_03005FC8,g_03005B30,g_03002E5C,g_030061E0;
extern s32 g_03002A18,g_03001B28,g_03000DF8,g_03005F58;
void func_080162F8(s32 point,s32 slot) {
 TxraTriple center,delta;
 s32 cp,sp,cy,sy,x,y,z,a,b,c,d,e,f,scale;
 center.field_00=g_03005F80.field_00;
 center.field_04=g_03005F80.field_04;
 center.field_08=g_03005F80.field_08;
 delta.field_00=g_03005F70.field_00-g_03001E60[slot].field_04;
 delta.field_04=g_03005F70.field_04-g_03001E60[slot].field_08;
 delta.field_08=g_03005F70.field_08-g_03001E60[slot].field_0c;
 cp=g_083D2280[*(s32*)((u8*)&g_03001E60[slot]+36)];g_03005FC8=cp;
 sp=g_083C2280[*(s32*)((u8*)&g_03001E60[slot]+36)];g_03005B30=sp;
 cy=g_083D2280[g_03001E60[slot].field_20];g_03002E5C=cy;
 sy=g_083C2280[g_03001E60[slot].field_20];g_030061E0=sy;
 x=g_030057A0[point].field_00;
 y=-g_030057A0[point].field_04;
 z=g_030057A0[point].field_08;
 a=(cp*y-sp*z)>>12;
 b=(sp*y+cp*z)>>12;
 c=(x*cy-sy*b)>>12;
 d=(x*sy+b*cy)>>12;
 c-=delta.field_00;
 e=a-delta.field_04;
 d-=delta.field_08;
 a=(g_03002A18*c-g_03001B28*d)>>12;
 b=(c*g_03001B28+g_03002A18*d)>>12;
 f=(e*g_03000DF8-b*g_03005F58)>>12;
 d=(e*g_03005F58+b*g_03000DF8)>>12;
 x=center.field_00+a;
 y=center.field_04+d;
 z=center.field_08+f;
 g_030055F0[point].field_08=z;
 x<<=3;y<<=3;z>>=1;
 scale=g_0804F330[z+65536];
 g_030055F0[point].field_00=(x*scale>>15)+120;
 g_030055F0[point].field_04=(y*scale>>15)+80;
}
