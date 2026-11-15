/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_0201A6F0[],g_0201C310[],g_0201F970[],g_02022FD0[],g_02026630[],g_02029C90[];
extern s32 g_03001B20,g_03005FCC,g_03005FC0;
extern void func_080160C4(u32,u8 *,u32,s32,u32);
void func_08015250(s32 state)
{
    u8 *p=g_0201A6F0;
    u8 *q;
    s32 amount;
    if(state==5)q=g_0201C310;
    if(state==4)q=g_0201F970;
    if(state==3)q=g_02022FD0;
    if(state==2)q=g_02026630;
    if(state==1)q=g_02029C90;
    if(g_03001B20)amount=g_03001B20&63;
    else amount=g_03005FCC;
    if(amount>55)amount=55;
    if(!g_03005FC0) {
        func_080160C4(3,p,0x0600A000,6960,32);
        if(amount<55)func_080160C4(3,q,0x0600A000+(amount+105)*240,(55-amount)*240,32);
    } else {
        func_080160C4(3,p,0x06000000,6960,32);
        if(amount<55)func_080160C4(3,q,0x06000000+(amount+105)*240,(55-amount)*240,32);
    }
}
