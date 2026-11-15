extern void func_08018A58(u32, void *, u32);
void func_08014988(u32 source)
{
    u32 sum = 0;
    u32 i;
    u16 *p;
    TxraLinkState *state = &g_03007A30;
    state->field_28[0] = state->field_0b;
    state->field_28[1] = state->field_02 ^ state->field_03;
    *(u16 *)(state->field_28 + 2) = 0;
    func_08018A58(source, state->field_28 + 4, 0x04000004);
    i = 0;
    p = (u16 *)state->field_28;
    do {
 sum += *p++;
 i++;
 }
 while (i <= 9);
{
u32 tail = (u32)&g_03007A30;
 u16 *packet = *(u16 **)((u32)tail + 40);
 packet[1] = ~sum;
 if (*(u8 *)tail) *(vu16 *)0x0400010E = 0;
}
    state->field_14 = -1;
    if (state->field_00 && state->field_08) *(vu16 *)0x0400010E = 192;
}
