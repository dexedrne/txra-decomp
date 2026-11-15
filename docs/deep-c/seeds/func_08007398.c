/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
extern TxraSoundVoice g_03007770[8];
extern u32 g_03007404, g_03007574, g_03007578, g_03007570;
extern u32 g_030079B0,g_030079B4;
extern u32 g_03007590[6][3];
extern u32 g_030075E8[],g_030075D8[],g_03006A88[];
extern u8 g_03006AA0[], g_030068A0[];
extern void func_080076F4(void),func_08006270(void);
static inline void wave_clear(void) {
    u16 *base=(u16*)0x04000090;
    u16 *p=base+3;
    s32 i;
    do { *p--=0xffff; } while ((s32)p >= (s32)base);
    p=base+4;
    for(i=3;i>=0;i--) *p++=0;
}
void func_08007398(void) {
    s32 i;
    g_03007770[0].field_00=0;
    g_03007770[1].field_00=0;
    g_03007770[2].field_00=0;
    g_03007770[3].field_00=0;
    g_03007770[4].field_00=0;
    g_03007770[5].field_00=0;
    g_03007770[6].field_00=0;
    g_03007770[7].field_00=0;
    g_03007404=256;
    g_03007574=0;
    g_03007578=7;
    g_03007570=0;
    wave_clear();
    *(vu16*)0x04000080=0xff0e;
    *(vu16*)0x04000084=0x8f;
    *(vu16*)0x04000082=0xfb0e;
    *(vu16*)0x04000070=0xc0;
    wave_clear();
    *(vu16*)0x04000060=8;
    g_03007590[0][0]=0;g_03007590[1][0]=0;g_03007590[2][0]=0;
    g_03007590[3][0]=0;g_03007590[4][0]=0;g_03007590[5][0]=0;
    for(i=0;i<2;i++){g_03006A88[i]=0;g_030075D8[i]=0;g_030075E8[i]=0;}
    *(vu32*)0x040000D4=(u32)func_080076F4;
    *(vu32*)0x040000D8=(u32)g_03006AA0;
    *(vu32*)0x040000DC=0x84000258;
    *(vu32*)0x040000DC;
    *(vu32*)0x040000D4=(u32)func_08006270;
    *(vu32*)0x040000D8=(u32)g_030068A0;
    *(vu32*)0x040000DC=0x84000078;
    *(vu32*)0x040000DC;
    g_030079B0=7;g_030079B4=0;
}
