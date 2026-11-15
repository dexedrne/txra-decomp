extern void func_08018A58(u32, void *, u32);
void func_08014988(u32 source)
{
    u32 sum = 0;
    u32 i;
    u16 *p;
    u32 state = (u32)&g_03007A30;
    ((TxraLinkState *)state)->field_28[0] = ((TxraLinkState *)state)->field_0b;
    ((TxraLinkState *)state)->field_28[1] = ((TxraLinkState *)state)->field_02 ^ ((TxraLinkState *)state)->field_03;
    *(u16 *)(((TxraLinkState *)state)->field_28 + 2) = 0;
    func_08018A58(source, ((TxraLinkState *)state)->field_28 + 4, 0x04000004);
    i = 0;
    p = (u16 *)((TxraLinkState *)state)->field_28;
    do {
 sum += *p++;
 i++;
 }
 while (i <= 9);
    {
        TxraLinkState *tail = (TxraLinkState *)&g_03007A30;
        u16 *packet = (u16 *)tail->field_28;
        u32 inverted = ~sum;
        packet[1] = inverted;
        if (tail->field_00) *(vu16 *)0x0400010E = 0;
    }
    ((TxraLinkState *)state)->field_14 = -1;
    if (((TxraLinkState *)state)->field_00 && ((TxraLinkState *)state)->field_08) *(vu16 *)0x0400010E = 192;
}
