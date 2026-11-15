/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
typedef struct {u8 field_00,field_01,field_02,pad03[16],field_13,field_14,field_15,field_16,field_17,field_18,tail[7];} Slot;
extern Slot g_03000B60[];
extern TxraRecord g_03001E60[];
extern s32 g_030014B4,g_03000B58,g_03000AC8,g_03005FD4;
extern void func_080143B0(void);
extern void func_080086C0(s32,s32),func_08008780(s32,s32),func_0800D2F4(s32,s32),func_08008838(s32,s32);
void func_08012600(u32 id)
{
 s32 mode=0,car,count;
 s32 *selected;
 Slot *base;
 switch(id){
 case 39:case 42:case 75:case 101:case 127:
 mode=1;
 break;
 case 40:case 43:case 76:case 102:case 128:
 mode=2;
 break;
 case 41:case 44:case 77:case 103:case 129:
 mode=3;
 break;
 case 30:case 69:case 95:case 121:
 mode=4;
 func_080143B0();
 car=g_03001E60[0].field_02-16;
 count=g_030014B4;
 if(count)func_080086C0(car,count);
 count=g_03000B60[0].field_16-1;
 if(count)func_08008780(car,count);
 count=g_03000B60[0].field_18-1;
 if(count)func_0800D2F4(car,count);
 count=g_03000B60[0].field_13-1;
 if(count)func_08008838(car,count);
 break;
 case 31:case 70:case 96:case 122:
 mode=5;
 func_080143B0();
 car=g_03001E60[0].field_02-16;
 count=g_030014B4;
 if(count)func_08008780(car,count);
 count=g_03000B60[0].field_15-1;
 if(count)func_080086C0(car,count);
 count=g_03000B60[0].field_18-1;
 if(count)func_0800D2F4(car,count);
 count=g_03000B60[0].field_13-1;
 if(count)func_08008838(car,count);
 break;
 case 33:case 72:case 98:case 124:
 mode=6;
 func_080143B0();
 car=g_03001E60[0].field_02-16;
 count=g_030014B4;
 if(count)func_0800D2F4(car,count);
 count=g_03000B60[0].field_15-1;
 if(count)func_080086C0(car,count);
 count=g_03000B60[0].field_16-1;
 if(count)func_08008780(car,count);
 count=g_03000B60[0].field_13-1;
 if(count)func_08008838(car,count);
 break;
 case 25:case 64:case 90:case 116:
 mode=7;
 func_080143B0();
 car=g_03001E60[0].field_02-16;
 count=g_030014B4;
 if(count)func_08008838(car,count);
 count=g_03000B60[0].field_15-1;
 if(count)func_080086C0(car,count);
 count=g_03000B60[0].field_16-1;
 if(count)func_08008780(car,count);
 count=g_03000B60[0].field_18-1;
 if(count)func_0800D2F4(car,count);
 break;
 }
 switch(mode){
 case 0:
 func_080143B0();
 car=g_03000B60[0].field_02-16;
 count=g_03000B60[0].field_15-1;
 if(count)func_080086C0(car,count);
 count=g_03000B60[0].field_16-1;
 if(count)func_08008780(car,count);
 count=g_03000B60[0].field_18-1;
 if(count)func_0800D2F4(car,count);
 count=g_03000B60[0].field_13-1;
 if(count)func_08008838(car,count);
 break;
 case 1:
 func_080143B0();base=g_03000B60;selected=&g_03000B58;goto from_slot;
 case 2:
 func_080143B0();base=g_03000B60;selected=&g_03000AC8;
 from_slot:
 car=base[*selected].field_02-16;
 count=base[*selected].field_15-1;
 if(count)func_080086C0(car,count);
 count=base[*selected].field_16-1;
 if(count)func_08008780(car,count);
 count=base[*selected].field_18-1;
 if(count)func_0800D2F4(car,count);
 count=base[*selected].field_13-1;
 if(count)func_08008838(car,count);
 break;
 case 3:
 func_080143B0();base=g_03000B60;selected=&g_03005FD4;
 car=base[*selected].field_02-16;
 count=base[*selected].field_15-1;
 if(count)func_080086C0(car,count);
 count=base[*selected].field_16-1;
 if(count)func_08008780(car,count);
 count=base[*selected].field_18-1;
 if(count)func_0800D2F4(car,count);
 count=base[*selected].field_13-1;
 if(count)func_08008838(car,count);
 break;
 }
}
