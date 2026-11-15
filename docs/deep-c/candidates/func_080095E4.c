/* Unmatched source hypothesis; excluded from the ROM build. */
#include "types.h"
typedef struct Poly {u16 x[4];s16 y[4];u8 u[4],v[4];u16 field_18,field_1a;struct Poly *next;} Poly;
extern u16 g_03001B14;
extern u32 g_03005F50,g_03002E4C;
extern s32 g_083D2280[],g_083C2280[];
extern TxraTriple g_030057A0[],g_030055F0[];
extern Poly *g_030021C4,*g_03000670[];
extern void func_080164D0(s32);
void func_080095E4(void) {
 s32 i,x,z,a,c,s,dy;
 u32 bucket;
 if(g_03001B14!=2)return;
 if(g_03005F50>2 && g_03005F50<g_03002E4C-32)return;
 for(i=0;i<=6;i++) {
  switch(i) {
   case 0:
    a=(g_03006874[1].field_0c+4096)&16383;
    c=g_083D2280[a];s=g_083C2280[a];
    x=((c*3)<<8)>>12;z=((s*3)<<8)>>12;
    x+=g_03006874[1].field_00;z+=g_03006874[1].field_08;break;
   case 1:
    a=(g_03006874[1].field_0c+4096)&16383;
    c=g_083D2280[a];s=g_083C2280[a];
    x=(c<<9)>>12;z=(s<<9)>>12;
    x+=g_03006874[1].field_00;z+=g_03006874[1].field_08;break;
   case 2:
    a=(g_03006874[1].field_0c+4096)&16383;
    c=g_083D2280[a];s=g_083C2280[a];
    x=(c<<8)>>12;z=(s<<8)>>12;
    x+=g_03006874[1].field_00;z+=g_03006874[1].field_08;break;
   case 3:x=g_03006874[1].field_00;z=g_03006874[1].field_08;break;
   case 4:
    a=(g_03006874[1].field_0c+12288)&16383;
    c=g_083D2280[a];s=g_083C2280[a];
    x=(c<<8)>>12;z=(s<<8)>>12;
    x+=g_03006874[1].field_00;z+=g_03006874[1].field_08;break;
   case 5:
    a=(g_03006874[1].field_0c+12288)&16383;
    c=g_083D2280[a];s=g_083C2280[a];
    x=(c<<9)>>12;z=(s<<9)>>12;
    x+=g_03006874[1].field_00;z+=g_03006874[1].field_08;break;
   case 6:
    a=(g_03006874[1].field_0c+12288)&16383;
    c=g_083D2280[a];s=g_083C2280[a];
    x=((c*3)<<8)>>12;z=((s*3)<<8)>>12;
    x+=g_03006874[1].field_00;z+=g_03006874[1].field_08;break;
  }
  g_030057A0[0].field_00=x;g_030057A0[0].field_04=g_03006874[1].field_04+64;g_030057A0[0].field_08=z;func_080164D0(0);
  g_030057A0[1].field_00=x;g_030057A0[1].field_04=g_03006874[1].field_04;g_030057A0[1].field_08=z;func_080164D0(1);
  dy=(g_030055F0[1].field_04-g_030055F0[0].field_04)>>1;
  g_030021C4->x[0]=g_030055F0[0].field_00;g_030021C4->y[0]=g_030055F0[0].field_04;
  g_030021C4->x[1]=(u16)g_030055F0[0].field_00+dy;g_030021C4->y[1]=g_030055F0[0].field_04;
  g_030021C4->x[2]=(u16)g_030055F0[0].field_00+dy;g_030021C4->y[2]=g_030055F0[1].field_04;
  g_030021C4->x[3]=g_030055F0[0].field_00;g_030021C4->y[3]=g_030055F0[1].field_04;
  if((g_030021C4->x[0]<=119 && g_030021C4->y[0]>=0 && g_030021C4->y[0]<=159) ||
     (g_030021C4->x[1]<=119 && g_030021C4->y[1]>=0 && g_030021C4->y[1]<=159) ||
     (g_030021C4->x[2]<=119 && g_030021C4->y[2]>=0 && g_030021C4->y[2]<=159) ||
     (g_030021C4->x[3]<=119 && g_030021C4->y[3]>=0 && g_030021C4->y[3]<=159)) {
   g_030021C4->u[0]=24;g_030021C4->v[0]=0;g_030021C4->u[1]=32;g_030021C4->v[1]=0;
   g_030021C4->u[2]=32;g_030021C4->v[2]=15;g_030021C4->u[3]=24;g_030021C4->v[3]=15;
   bucket=(g_030055F0[0].field_08>>6)+8;
   if(bucket<=255) {
    Poly *head;
    g_030021C4->field_18=8;g_030021C4->field_1a=1;
    head=g_03000670[bucket];
    if(!head){g_030021C4->next=0;g_03000670[bucket]=g_030021C4;g_030021C4++;}
    else{g_030021C4->next=head;g_03000670[bucket]=g_030021C4;g_030021C4++;}
   }
  }
 }
}
