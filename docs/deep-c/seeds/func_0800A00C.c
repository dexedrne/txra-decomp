/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
extern TxraRecord g_03001E60[];
extern s16 g_030066D0;
extern s32 g_03002E4C;
extern u32 g_03002E50;
extern void func_0800AF4C(u32);
extern s16 g_03001E50;
extern s32 func_0800D3F8(s32, s32);
void func_0800A00C(void) {
    s32 slot=4, lower=0, index=100, tries, found;
    TxraRow28 *row;
    u32 scale, angle;
    for(tries=3;tries>=0;tries--) {
        found=func_0800D3F8(lower,g_03001E50);
        if(found<lower) continue;
    g_03001E60[slot].field_00=1;
    row=&g_03006874[index];
    scale=g_03002E50;
    g_03001E60[slot].field_04=(u32)row->field_00+(((u32)row[1].field_00-(u32)row->field_00)*scale>>4);
    g_03001E60[slot].field_08=-((u32)row->field_04+(((u32)row[1].field_04-(u32)row->field_04)*scale>>4));
    g_03001E60[slot].field_0c=(u32)row->field_08+(((u32)row[1].field_08-(u32)row->field_08)*scale>>4);
    angle=((row[3].field_0c+0x1000)&0x3fff)<<3;
    g_03001E60[slot].field_34=angle;
    g_03001E60[slot].field_20=(s32)angle>>3;
    *(u32 *)((u8 *)&g_03001E60[slot]+0x24)=0;
    g_03001E60[slot].field_38=index;
    *(u16 *)((u8 *)&g_03001E60[slot]+0x4c)=2;
    g_03001E60[slot].field_48=48;
    g_03001E60[slot].field_28=0;
    g_03001E60[slot].field_52=0;
    *(u16 *)((u8 *)&g_03001E60[slot]+0x44)=0;
    *(u16 *)((u8 *)&g_03001E60[slot]+0x4e)=0;
    *(u16 *)((u8 *)&g_03001E60[slot]+0x42)=48;
    g_03001E60[slot].field_02=6;
    g_03001E60[slot].field_50=4;
    g_03001E60[slot].field_62=found;
    *(u16 *)((u8 *)&g_03001E60[slot]+0x5c)=0;
    func_0800AF4C(slot);
        lower=found+1;
        index+=g_03002E4C>>3;
        slot++;
    }
}
