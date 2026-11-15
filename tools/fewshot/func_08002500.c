extern u16 g_03005F60,g_03002E54;
extern s16 g_030014B0;
extern TxraRecord g_03001E60[];
extern void (*g_080200C8)(s32,s32);
extern s32 g_030014B4,g_03000B58,g_03000AC8,g_03005FD4;
typedef struct {u8 pad[23],field_17,tail[8];} Slot;
extern Slot g_03000B60[];
void func_08002500(u32 id)
{
 s32 count,slot;
 if((u16)(g_03005F60-15)<=2)return;
 g_03002E54=1;
 if(id==11)return;
 if(id==6)return;
 if(id==45)return;
 if(id==7)return;
 if(id==52)return;
 if(id==78)return;
 if(id==104)return;
 g_080200C8(g_030014B0,g_03001E60[g_030014B0].field_02);
 if(id==32 || id==71 || id==97 || id==123){
  if(g_030014B4)g_080200C8(0,g_030014B4+11);
  return;
 }
 count=g_03000B60[0].field_17;
 count--;
 switch(id){
 case 36:case 37:case 38:return;
 case 39:case 42:case 75:case 101:case 127:
  slot=g_03000B58;goto from_slot;
 case 40:case 43:case 76:case 102:case 128:
  slot=g_03000AC8;goto from_slot;
 case 41:case 44:case 77:case 103:case 129:
  slot=g_03005FD4;
 from_slot:
  count=g_03000B60[slot].field_17;
  count--;
  break;
 }
 if(count>0)g_080200C8(0,count+11);
}
