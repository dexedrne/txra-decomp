/* Unmatched source hypothesis from deep slice e; excluded from the ROM build. */
typedef struct {
    u16 baud:2, si:1, sd:1, id:2, error:1, enable:1, unused8:4, mode:2, irq:1, unused15:1;
    u16 data;
} SioMultiCnt;
typedef struct { u16 data[4]; } SioMultiRecv;
void func_08014AE0(void)
{
    SioMultiRecv recv = *(SioMultiRecv *)0x04000120;
    TxraLinkState *s = &g_03007A30;
    s32 i;
    if (s->field_14 == -1) {
        u8 *t;
        ((SioMultiCnt *)0x04000128)->data = 0xFEFE;
        t = s->field_2c;
        s->field_2c = s->field_28;
        s->field_28 = t;
    } else if (s->field_14 >= 0) {
        ((SioMultiCnt *)0x04000128)->data = ((u16 *)s->field_2c)[s->field_14];
    }
    if (s->field_14 <= 10) s->field_14++;
    for (i = 0; i <= 1; i++) {
        s32 *count = &((s32 *)s->unknown_18)[i];
        if (recv.data[i] == 0xFEFE && *count > 9) {
            *count = -1;
        } else {
            u8 *buf = s->field_30[i];
            ((u16 *)buf)[*count] = recv.data[i];
            if (*count == 9) {
                s->field_30[i] = s->field_40[i];
                s->field_40[i] = buf;
                ((u8 *)&s->field_04)[i] = 1;
            }
        }
        if (*count <= 10) ++*count;
    }
    if (s->field_00 == 8) {
        *(vu16 *)0x0400010E = 0;
        *(vu16 *)0x04000128 |= 0x80;
        *(vu16 *)0x0400010E = 0xC0;
    }
}
