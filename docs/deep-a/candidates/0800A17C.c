/* Unmatched diagnostic source; not installed or accepted as behavior-correct. */
extern s16 g_030001BC, g_03000AC0, g_030021CC;
extern TxraRecord g_03001E60[];
extern s16 g_03002A20[], g_03002E4C, g_03005F7C, g_03004DD4;
extern u32 g_03005FC0, g_03005F48;
extern u8 g_081BDB84[];
extern s16 g_03002330, g_03001B14, g_03004780, g_030001E0[];
extern s32 g_030014AC, g_030021D4, g_030014C0, g_03005B38, g_030014A4;
extern u8 g_03005680[];
extern u16 g_08020904[];
extern void func_08016078(s32);
extern s32 func_0800D490(void);
#define DEEP_STATE (*(s16 *)((u8 *)g_03001E60+76))
#define DEEP_COPY_ROW() { u32 *from=(u32 *)src; u32 *to=(u32 *)dst; s32 left; for(left=55;left>=0;left--) *to++=*from++; }
#define DEEP_AWARD(slot,kind) \
    if(!g_030001E0[slot] && (u16)g_03001E60[g_030001BC&7].field_62==(kind)) { g_030001E0[slot]=1;g_030014AC=1; }
void func_0800A17C(void)
{
    u8 *src,*dst,*initial_src,*initial_dst;
    s32 row,i;
    if(!g_030001BC || g_03000AC0) return;
    if((u16)(g_030001BC-4)<=3) {
        if(!g_030021CC) {
            g_03005F7C=g_03001E60[0].field_38-g_03002A20[0];
            if(g_03005F7C<0) g_03005F7C+=g_03002E4C;
            if(g_03005F7C>1280) g_03005F7C=0;
            if(g_03005F7C>864) g_03005F7C=864;
            g_03005F7C>>=4;
            g_03004DD4=g_03001E60[g_030001BC].field_38-g_03002A20[2];
            if(g_03004DD4<0) g_03004DD4+=g_03002E4C;
            if(g_03004DD4>1280) g_03004DD4=0;
            if(g_03004DD4>864) g_03004DD4=864;
            g_03004DD4>>=4;
        }
    } else { g_03005F7C=0; g_03004DD4=0; }
    initial_src=g_081BDB84;
    initial_dst=(u8 *)0x06000788;
    if(!g_03005FC0) initial_dst=(u8 *)0x0600A788;
    src=initial_src;dst=initial_dst;
    DEEP_COPY_ROW();src+=256;dst+=240;
    DEEP_COPY_ROW();src+=256;dst+=240;
    for(row=0;row<4;row++) {
        u16 *from=(u16 *)src,*to=(u16 *)dst;
        *to++=*from++;
        for(i=0;i<g_03005F7C;i++) *to++=*from++;
        for(i=0;i<54-g_03005F7C;i++) { *to++=g_03005F48;from++; }
        *to++=*from++; *to++=*from++;
        for(i=0;i<54-g_03004DD4;i++) { *to++=g_03005F48;from++; }
        for(i=0;i<g_03004DD4;i++) *to++=*from++;
        *to=*from;
        src+=256;dst+=240;
    }
    DEEP_COPY_ROW();src+=256;dst+=240;
    DEEP_COPY_ROW();
    if((u16)(g_030001BC-4)>3 || g_03002330 || g_030021CC) return;
    if((u16)g_03005F7C==54) {
        g_030014AC=0; DEEP_STATE=2; g_030021D4=1; g_030021CC=64;
        func_08016078(7);
        g_030014C0=0;
        if(!g_03001B14) {
            if(!g_03005680[g_03001E60[g_030001BC&7].field_62*2] && func_0800D490()==127 && !g_03005B38) g_03005B38=1;
            g_03005680[g_03001E60[g_030001BC&7].field_62*2]=1;
            DEEP_AWARD(1,10);
            DEEP_AWARD(2,24);
            DEEP_AWARD(3,41);
            DEEP_AWARD(4,59);
            DEEP_AWARD(5,71);
            g_030014C0=g_08020904[g_03001E60[g_03004780].field_62];
            g_030014A4+=g_030014C0;
        }
    }
    if((u16)g_03004DD4==54) {
        g_030014C0=0; DEEP_STATE=2; g_030021D4=1; g_030021CC=64;
        func_08016078(6);
    }
}
