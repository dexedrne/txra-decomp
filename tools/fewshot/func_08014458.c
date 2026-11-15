extern u8 g_03000DE8[];
extern s16 g_03006684;
extern u32 g_03001B1C;
extern u8 g_082ADBCC[];
extern u8 func_080157A0(u32);
extern void func_08015C2C(s32,s32,u8 *);
void func_08014458(void)
{
    s32 x=76;
    register s32 y0=128;
    s32 i=0;
    register s32 y1=136;
    for(;i<=5;i++) {
        u32 ch=func_080157A0(g_03000DE8[i]);
        u8 *p;
        if (!ch) ch=93;
        p=g_082ADBCC+ch*256;
        if(g_03006684!=i || (g_03001B1C&15)>7) {
            func_08015C2C(x,y0,p);
            func_08015C2C(x+8,y0,p+64);
            func_08015C2C(x,y1,p+128);
            func_08015C2C(x+8,y1,p+192);
        }
        x+=16;
    }
}
