/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
extern TxraRecord g_03001E60[];
extern s16 g_030014B0;
void func_0800EDF4(s32 mode,s32 amount) {
    u32 source=0x082CA4A4;
    s16 type=g_03001E60[g_030014B0].field_02;
    s32 i,r,g,b,t;
    u16 *palette=(u16 *)0x03002C30;
    if(type==16)source+=384;
    if(type==17)source=0x082CD974;
    if(type==18)source=0x082D0B38;
    if(type==19)source=0x082D3EDC;
    if(type==20)source=0x082D7048;
    if(type==21)source=0x082DA048;
    if(type==22)source=0x082DD58C;
    if(type==23)source=0x082E0A30;
    if(type==24)source=0x082E3D54;
    if(type==25)source=0x082E72EC;
    type=g_03001E60[g_030014B0].field_02;
    if(type==26)source=0x082EA3D4;
    if(type==27)source=0x082ED1E0;
    if(type==28)source=0x082F07E0;
    if(type==29)source=0x082F39C0;
    if(type==30)source=0x082F6DD8;
    if(type==31)source=0x082F9E60;
    *(vu32 *)0x040000D4=source;
    *(vu32 *)0x040000D8=0x03002DB0;
    *(vu32 *)0x040000DC=0x84000014;
    *(vu32 *)0x040000DC;
    for(i=192;i<=239;i++) {
        u16 color=palette[i];
        r=color&31;g=(color>>5)&31;b=(color>>10)&31;
        if(i<192+amount) {
            switch(mode) {
            case 1:t=r;r=g;g=b;b=t;break;
            case 2:t=b;b=g;g=r;r=t;break;
            case 3:b=r;break;
            case 4:b=g;break;
            case 5:r=b;break;
            case 6:r=g;break;
            case 7:g=b;break;
            case 8:g=r;break;
            case 9:b=r;g=b;break;
            case 10:r=g;b=g;break;
            case 11:r=b;g=b;break;
            case 12:b=g/2;r=b;break;
            case 13:b=r/2;g=b;break;
            case 14:g=b/2;r=g;break;
            case 15:r=b/8;break;
            case 16:g=b/8;break;
            case 17:b=g/8;break;
            }
        }
        color=(r&31)+((g&31)<<5)+((b&31)<<10);
        palette[i]=color;palette[i-192]=color;
    }
}
