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
extern s16 g_030014B0;
extern u16 g_03002DB0[];
extern u8 g_082CA4A4[],g_082CD974[],g_082D0B38[],g_082D3EDC[],g_082D7048[],g_082DA048[],g_082DD58C[],g_082E0A30[],g_082E3D54[],g_082E72EC[],g_082EA3D4[],g_082ED1E0[],g_082F07E0[],g_082F39C0[],g_082F6DD8[],g_082F9E60[];
void func_0800EDF4(u32 effect,s32 count) {
 u8 *source=g_082CA4A4;
 vu32 *dma;
 u32 base;
 s32 i,red,green,blue,end;
 if(g_03001E60[g_030014B0].field_02==16)source+=384;
 if(g_03001E60[g_030014B0].field_02==17)source=g_082CD974;
 if(g_03001E60[g_030014B0].field_02==18)source=g_082D0B38;
 if(g_03001E60[g_030014B0].field_02==19)source=g_082D3EDC;
 if(g_03001E60[g_030014B0].field_02==20)source=g_082D7048;
 if(g_03001E60[g_030014B0].field_02==21)source=g_082DA048;
 if(g_03001E60[g_030014B0].field_02==22)source=g_082DD58C;
 if(g_03001E60[g_030014B0].field_02==23)source=g_082E0A30;
 if(g_03001E60[g_030014B0].field_02==24)source=g_082E3D54;
 if(g_03001E60[g_030014B0].field_02==25)source=g_082E72EC;
 if(g_03001E60[g_030014B0].field_02==26)source=g_082EA3D4;
 if(g_03001E60[g_030014B0].field_02==27)source=g_082ED1E0;
 if(g_03001E60[g_030014B0].field_02==28)source=g_082F07E0;
 if(g_03001E60[g_030014B0].field_02==29)source=g_082F39C0;
 if(g_03001E60[g_030014B0].field_02==30)source=g_082F6DD8;
 if(g_03001E60[g_030014B0].field_02==31)source=g_082F9E60;
 dma=(vu32*)0x040000D4;
 dma[0]=(u32)source;dma[1]=(u32)g_03002DB0;dma[2]=0x84000014;dma[2];
 i=192;
 base=(u32)g_03002DB0;
 base-=384;
 end=count+192;
 do {
  u32 address=i<<1;
  u32 color=*(u16*)(address+base);
  red=color&31;
  color<<=16;green=(color>>21)&31;blue=(color>>26)&31;
  if(i<end) {
   switch(effect) {
    case 1:{s32 t=red;red=green;green=blue;blue=t;}break;
    case 2:{s32 t=blue;blue=green;green=red;red=t;}break;
    case 3:blue=red;break;
    case 4:blue=green;break;
    case 5:red=blue;break;
    case 6:red=green;break;
    case 7:green=blue;break;
    case 8:green=red;break;
    case 9:blue=red;green=blue;break;
    case 10:red=green;blue=green;break;
    case 11:red=blue;green=blue;break;
    case 12:blue=green/2;red=blue;break;
    case 13:blue=red/2;green=blue;break;
    case 14:green=blue/2;red=green;break;
    case 15:red=blue/8;break;
    case 16:green=blue/8;break;
    case 17:blue=green/8;break;
   }
  }
  color=(red&31)+((green&31)<<5)+((blue&31)<<10);
  address+=base;
  *(u16*)address=color;
  *(u16*)(((i-192)<<1)+base)=color;
  i++;
 }while(i<=239);
}
