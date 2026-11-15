/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern s32 g_030014B4;
extern u32 g_030061E4;
extern u8 g_08331F9C[];
extern void func_0801533C(u8 *,u32,u32,u32,u32,u32,u32,u32,u32);
void func_0800418C(void)
{
    s32 x,y;
    u32 index;
    if (g_030014B4<=12) { x=g_030014B4*16+16; y=64; }
    else if (g_030014B4<=25) { x=g_030014B4*16-192; y=80; }
    else { x=g_030014B4*16-400; y=96; }
    func_0801533C(g_08331F9C,0x06014000+(index=g_030061E4)*32,256,96,2,y|0x2401,(x&511)|0x4000,index+512,0);
    g_030061E4+=32;
}
