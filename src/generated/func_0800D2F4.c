/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u16 g_08179784[][32];
extern void func_08008914(u32,u32,u32,u32,u32,u32,u32,u32,u32);
void func_0800D2F4(u32 a,s32 b)
{
    if (b) {
        s32 x=((b-1)&1)*96;
        s32 y=((b>>1)&1)*56;
        func_08008914(0,174,56,7,g_08179784[a][12],g_08179784[a][13],0,x,y);
        func_08008914(0,174,56,7,g_08179784[a][14],g_08179784[a][15],1,x,y);
    }
}
