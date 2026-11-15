/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
extern TxraRecord g_03001E60[];
extern s16 g_03002A1C,g_030021CC,g_030014B0;
extern u16 g_0300218C;
extern s32 g_030021D4;
extern TxraTriple g_03005F70;
extern s32 g_03002328,g_083D2280[],g_083C2280[];
extern u32 (*g_083E2280)(void);
extern void func_0800BDC0(s32),func_0800C3C4(s32),func_0800CB5C(s32),func_0800C850(s32),func_0800C9C4(s32),func_0800CEEC(s32);
extern void func_0801604C(u32,u32);
void func_0800BBD4(void) {
    s32 i;
    if(((g_03002A1C==0 && (g_0300218C&512)) || (g_03002A1C==1 && (g_0300218C&4))) && g_030021CC==0) {
        if(g_030021D4==0) g_030021D4=1;
        else g_030021D4=0;
    }
    for(i=7;i>=0;i--) {
        s32 saved1,saved2;
        if(g_03001E60[i].field_00) {
            *(s32 *)((u8 *)&g_03001E60[i]+0x10)=g_03001E60[i].field_04;
            *(s32 *)((u8 *)&g_03001E60[i]+0x14)=g_03001E60[i].field_08;
            *(s32 *)((u8 *)&g_03001E60[i]+0x18)=g_03001E60[i].field_0c;
            if(i!=g_030014B0) { saved1=g_03002E40.field_04;saved2=g_03002E40.field_08; }
            func_0800BDC0(i);func_0800C3C4(i);func_0800CB5C(i);
            func_0800C850(i);func_0800C9C4(i);func_0800CEEC(i);
            if(i!=g_030014B0) {g_03002E40.field_04=saved1;g_03002E40.field_08=saved2;}
        }
    }
    if(g_083E2280()==1) func_0801604C(22,1);
    if(g_030021D4==0) {
        s32 a=((g_03001E60[0].field_34>>3)+4096)&16383;
        s32 x=(g_083D2280[a]*-640)>>12;
        s32 z=(g_083C2280[a]*-640)>>12;
        g_03005F70.field_00=g_03001E60[0].field_04+x;
        g_03005F70.field_04=g_03001E60[0].field_08+120;
        g_03005F70.field_08=g_03001E60[0].field_0c+z;
        g_03002328=1000;
    }
    if(g_030021D4==1) {
        s32 scale=g_03001E60[0].field_28>>3;
        s32 a=(12288-g_03002E40.field_04)&16383;
        s32 x,z;
        if(scale>128) scale=128;
        x=(g_083D2280[a]*scale)>>12;
        z=(g_083C2280[a]*scale)>>12;
        if(g_030021CC==0) {
            g_03005F70.field_00=g_03001E60[0].field_04+x;
            g_03005F70.field_04=g_03001E60[0].field_08+180;
            g_03005F70.field_08=g_03001E60[0].field_0c+z;
        }
        g_03002328=900;
    }
}
