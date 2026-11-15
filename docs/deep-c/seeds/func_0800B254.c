/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
extern TxraRecord g_03001E60[];
extern s16 g_030066D0;
extern s32 g_03002E4C;
extern u32 g_03002E50;
extern void func_0800AF4C(u32);
void func_0800B254(void) {
    s16 saved=g_030066D0;
    s32 index=g_03001E60[0].field_38+6;
    TxraRow28 *row;
    TxraRecord *record;
    u32 scale, angle;
    if(index>=g_03002E4C) index-=g_03002E4C;
    record=&g_03001E60[4];
    g_03001E60[4].field_00=1;
    row=&g_03006874[index];
    scale=g_03002E50;
    g_03001E60[4].field_04=(u32)row->field_00+(((u32)row[1].field_00-(u32)row->field_00)*scale>>4);
    g_03001E60[4].field_08=-((u32)row->field_04+(((u32)row[1].field_04-(u32)row->field_04)*scale>>4));
    g_03001E60[4].field_0c=(u32)row->field_08+(((u32)row[1].field_08-(u32)row->field_08)*scale>>4);
    angle=((row[3].field_0c+0x1000)&0x3fff)<<3;
    g_03001E60[4].field_34=angle;
    g_03001E60[4].field_20=(s32)angle>>3;
    *(u32 *)((u8 *)&g_03001E60[4]+0x24)=0;
    g_03001E60[4].field_38=index;
    *(u16 *)((u8 *)&g_03001E60[4]+0x4c)=2;
    g_03001E60[4].field_48=48;
    g_03001E60[4].field_28=1600;
    g_03001E60[4].field_52=3;
    *(u16 *)((u8 *)&g_03001E60[4]+0x44)=0;
    *(u16 *)((u8 *)&g_03001E60[4]+0x4e)=0;
    *(u16 *)((u8 *)&g_03001E60[4]+0x42)=48;
    g_03001E60[4].field_02=6;
    g_03001E60[4].field_50=4;
    g_03001E60[4].field_62=saved;
    *(u16 *)((u8 *)&g_03001E60[4]+0x5c)=0;
    func_0800AF4C(4);
}
