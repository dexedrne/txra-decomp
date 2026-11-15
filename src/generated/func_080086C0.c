/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u16 g_08179784[][32];
extern void func_08008914(u32,u32,u32,u32,u32,u32,u32,u32,u32);
void func_080086C0(u32 a,s32 b)
{
    if(b) {
        s32 x=((b-1)&1)*96;
        s32 y=((b>>1)&1)*56;
        func_08008914(0,128,74,18,g_08179784[a][0],g_08179784[a][1],0,x,y);
        func_08008914(80,152,16,16,g_08179784[a][2],g_08179784[a][3],0,x,y);
        func_08008914(80,152,16,16,g_08179784[a][4],g_08179784[a][5],1,x,y);
    }
}
