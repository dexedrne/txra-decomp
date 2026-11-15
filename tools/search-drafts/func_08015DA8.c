extern TxraTransfer g_030061F0[];
extern u32 g_030067E4;
void func_08015DA8(void)
{
    u32 i = 0;
    TxraTransfer *entry = g_030061F0;
    do {
        u32 source = entry->field_00;
        if (!source) { g_030061F0[0].field_00 = source; break; }
        *(vu32 *)0x040000D4 = source;
        *(vu32 *)0x040000D8 = g_030061F0[i].field_04;
        *(vu32 *)0x040000DC = (g_030061F0[i].field_08 >> 2) | 0x84000000;
        *(vu32 *)0x040000DC;
        entry++;
        i++;
    } while (i <= 96);
    g_030061F0[0].field_00 = 0;
    g_030067E4 = 0;
}
