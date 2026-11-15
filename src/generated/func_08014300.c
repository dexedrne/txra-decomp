/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_03000B60[4][32];
void func_08014300(void)
{
    s32 pass,i;
    u32 j;
    for(pass=0;pass<=3;pass++) {
        for(i=0;i<=2;i++) {
            if (!g_03000B60[i][0] && g_03000B60[i+1][0]) {
                u8 *b=g_03000B60[i+1],*a=g_03000B60[i];
                for(j=0;j<=31;j++) {
                    u8 t=*b;
                    *b=*a;
                    *a=t;
                    a++;b++;
                }
            }
        }
    }
}
