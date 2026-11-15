typedef unsigned long long u64;
typedef struct {
    u16 baud:2, si:1, sd:1, id:2, error:1, enable:1, unused8:4, mode:2, irq:1, unused15:1;
    u16 data;
} SioMultiCnt;
typedef struct { u16 data[4]; } SioMultiRecv;
#define G g_03007A30
#define COUNT(i) (((s32 *)G.unknown_18)[i])
void func_08014AE0(void)
{
    u64 recv = *(u64 *)0x04000120;
    s32 i;
    if (G.field_14 == -1) {
        u8 *t;
        ((SioMultiCnt *)0x04000128)->data = 0xFEFE;
        t = G.field_2c;
        G.field_2c = G.field_28;
        G.field_28 = t;
    } else if (G.field_14 >= 0) {
        ((SioMultiCnt *)0x04000128)->data = ((u16 *)G.field_2c)[G.field_14];
    }
    if (G.field_14 <= 10) G.field_14++;
    for (i = 0; i <= 1; i++) {
        if (((u16 *)&recv)[i] == 0xFEFE && COUNT(i) > 9) {
            COUNT(i) = -1;
        } else {
            ((u16 *)G.field_30[i])[COUNT(i)] = ((u16 *)&recv)[i];
            if (COUNT(i) == 9) {
                u8 *other = G.field_40[i];
                G.field_40[i] = G.field_30[i];
                G.field_30[i] = other;
                ((u8 *)&G.field_04)[i] = 1;
            }
        }
        if (COUNT(i) <= 10) COUNT(i)++;
    }
    if (G.field_00 == 8) {
        *(vu16 *)0x0400010E = 0;
        *(vu16 *)0x04000128 |= 0x80;
        *(vu16 *)0x0400010E = 0xC0;
    }
}
