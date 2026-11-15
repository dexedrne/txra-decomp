#include "types.h"
#include "types.h"
extern TxraRecord g_03001E60[];
extern u8 g_03000B60[];
extern s32 g_030021D4,g_03005F50,g_03002E4C;
extern u16 g_03002E54;
extern void (*g_080200C8)(s32,s32);
void func_08002778(u32 value)
{
 s32 i=0;
 g_03002E54=value;
 if(!g_030021D4)i=1;
 for(;i<=7;i++){
 
 if(g_03001E60[i].field_00){
 s32 delta=g_03001E60[i].field_38-g_03005F50;
 if(delta>g_03002E4C-32)delta-=g_03002E4C;
 else if(delta<32-g_03002E4C)delta+=g_03002E4C;
 if((u32)(delta+1)<=24)g_03001E60[i].field_50=0;
 else if(g_03001E60[i].field_50<=255)(g_03001E60[i].field_50)++;
 else g_03001E60[i].field_50=256;
 if(g_03001E60[i].field_50<=3)g_080200C8(i,g_03001E60[i].field_02);
 }
 }
 if(g_030021D4==1 && g_03000B60[23]>1)g_080200C8(0,g_03000B60[23]+10);
}
