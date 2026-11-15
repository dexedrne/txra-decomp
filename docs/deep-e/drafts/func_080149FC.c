/* Unmatched source hypothesis from deep slice e; excluded from the ROM build. */
extern void func_08018A58(const void *, void *, u32);
u32 func_080149FC(u8 *out)
{
    vu32 unused;
    u32 received;
    u32 zero;
    s32 i;
    u32 *w;
    TxraLinkState *s;
    unused = 0;
    *(vu16 *)0x04000208 = 0;
    w = &g_03007A30.field_04;
    {
        u8 **q = (u8 **)(w + 15);
        for (i = 0; i < 4; i++) {
            u8 *t = q[4];
            q[4] = q[0];
            *q++ = t;
        }
    }
    received = *w;
    *w = 0;
    *(vu16 *)0x04000208 = 1;
    s = (TxraLinkState *)(w - 1);
    s->field_03 = 0;
    for (i = 0; i <= 1; i++) {
        u32 sum = 0;
        u32 j = 0;
        u16 *p = (u16 *)s->field_50[i];
        do { sum += *p++; j++; } while (j <= 9);
        if (((u8 *)&received)[i] && (s16)sum == -1) {
            func_08018A58(s->field_50[i] + 4, out + (i << 4), 0x04000004);
            s->field_03 |= 1 << i;
        }
        zero = 0;
        func_08018A58(&zero, s->field_50[i] + 4, 0x05000004);
    }
    g_03007A30.field_02 |= g_03007A30.field_03;
    return g_03007A30.field_03;
}
