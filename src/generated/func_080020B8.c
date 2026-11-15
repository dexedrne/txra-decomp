/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u32 g_030067E4,g_030061F0[],g_03007FFC,g_03000DE4,g_03006870;
extern u8 g_080000FC[],g_03004DE0[],g_08020A04[],g_03005680[],g_03000B60[],g_03005FA0[],g_08020C04[],g_03002E30[];
extern u16 g_030001E0[],g_03005F64,g_03001E50,g_03001B14,g_03005F5C;
extern u32 g_030014A4,g_030021D4,g_03005F44,g_03001B1C;
extern TxraRecord g_03001E60[];
extern void func_08007398(void),func_080146F4(void),func_0800F008(u32),func_08018A5C(u32),func_08016078(u32),func_0800D51C(u32),func_08012CC8(void),func_08012EB8(void);
extern s32 func_08007B28(void);
void func_080020B8(void)
{
    volatile u32 zero;
    vu32 *dma;
    s32 i,j;
    u32 state;
    s32 choice;
    *(vu16 *)0x04000208=0;
    *(vu16 *)0x04000000=128;
    *(vu16 *)0x04000204=0x4014;
    g_030067E4=0;g_030061F0[0]=0;
    zero=0;dma=(vu32 *)0x040000D4;
    dma[0]=(u32)&zero;dma[1]=0x02000000;dma[2]=0x85010000;dma[2];
    zero=0;dma[0]=(u32)&zero;dma[1]=0x03000000;dma[2]=0x85001F80;dma[2];
    dma[0]=(u32)g_080000FC;dma[1]=(u32)g_03004DE0;dma[2]=0x84000200;dma[2];
    g_03007FFC=(u32)g_03004DE0;
    func_08007398();
    *(vu16 *)0x04000208=1;*(vu16 *)0x04000200=1;
    *(vu16 *)0x04000004=8;*(vu32 *)0x04000100=0x00C3FF00;
    func_08007398();
    g_03000DE4=1;g_03006870=1;
    func_080146F4();
    {u8 *from=g_08020A04;u8 *to=g_03005680;
    for(i=127;i>=0;i--) {*to=from[0];to[1]=from[1];from+=2;to+=2;} }
    g_03000B60[0]=1;g_03000B60[2]=16;
    g_03000B60[3]=1;g_03000B60[14]=1;
    g_03000B60[4]=1;g_03000B60[15]=1;
    g_03000B60[5]=1;g_03000B60[16]=1;
    g_03000B60[6]=1;g_03000B60[17]=1;
    g_03000B60[7]=1;g_03000B60[18]=1;
    g_03000B60[8]=1;g_03000B60[19]=1;
    g_03000B60[9]=1;g_03000B60[20]=1;
    g_03000B60[10]=1;g_03000B60[21]=1;
    g_03000B60[11]=1;g_03000B60[22]=1;
    g_03000B60[12]=1;g_03000B60[23]=1;
    g_03000B60[13]=1;g_03000B60[24]=1;
    g_03001E60[0].field_02=16;g_03001E60[7].field_02=16;
    for(i=0;i<=5;i++)
        for(j=0;j<=4;j++) g_03005FA0[i*5+j]=g_08020C04[i*5+j];
    for(i=0;i<=5;i++) g_030001E0[i]=0;
    g_030001E0[0]=1;g_030014A4=15000;g_03005F64=1;g_03001E50=0;
    state=0;g_03001B14=0;g_030021D4=1;
    func_0800F008(0);g_03005F44=1;
    *(vu16 *)0x04000208=0;
    *(vu16 *)0x04000200|=4;
    *(vu16 *)0x04000208=1;
    func_08018A5C(4);
repeat:
    g_03005F5C=0;
    for(j=0;j<=15;j++) g_03002E30[j]=0;
    func_08016078(2);func_0800D51C(state);
    if(g_03001B14==1)func_08016078(5);
    else {
        if((g_03001B1C&3)==0)func_08016078(1);
        if((g_03001B1C&3)==1)func_08016078(3);
        if((g_03001B1C&3)==2)func_08016078(4);
        if((g_03001B1C&3)==3)func_08016078(8);
    }
    choice=func_08007B28();
    if(choice==3) {
        s32 selection=(s16)g_03001B14;
        if(selection==0)state=2;
        if(selection==1)state=3;
        if(selection==2)state=4;
        if(selection==3)state=5;
        goto repeat;
    }
    if(choice==4){state=4;goto repeat;}
    if(choice==5){func_08012CC8();state=3;goto repeat;}
    if(choice==6){func_08012EB8();state=2;goto repeat;}
}
