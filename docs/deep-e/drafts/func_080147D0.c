/* Unmatched source hypothesis from deep slice e; excluded from the ROM build. */
typedef struct { u8 a[24], b[24], c[24]; } LinkBuf;
typedef struct {
    u8 field_00,field_01,field_02,field_03;
    u32 field_04;
    u8 field_08,field_09,field_0a,field_0b;
    u8 unknown_0c[8];
    s32 field_14;
    u8 unknown_18[16];
    u8 * volatile field_28;
    u8 *field_2c;
    u8 *field_30[4],*field_40[4],*field_50[4];
    u8 field_60[24], field_78[24];
    LinkBuf field_90[2];
    u8 unknown_120[48];
} LS;
extern LS g_03007A30x __asm__("g_03007A30");
extern void func_08018A58(void *, void *, u32);
void func_080147D0(void)
{
    u32 zero;
    s32 i;
    LS *s;
    *(vu16 *)0x04000208 = 0;
    *(vu16 *)0x04000200 &= 0xFF3F;
    *(vu16 *)0x04000208 = 1;
    *(vu16 *)0x04000134 = 0;
    *(vu32 *)0x04000128 = 0x2000;
    *(vu16 *)0x04000128 |= 0x4003;
    zero = 0;
    s = &g_03007A30x;
    func_08018A58(&zero, s, 0x05000048);
    s->field_14 = -1;
    s->field_28 = s->field_60;
    s->field_2c = s->field_78;
    for (i = 0; i < 2; i++) {
        s->field_30[i] = s->field_90[i].a;
        s->field_40[i] = s->field_90[i].b;
        s->field_50[i] = s->field_90[i].c;
    }
    *(vu16 *)0x04000208 = 0;
    *(vu16 *)0x04000200 |= 0x80;
    *(vu16 *)0x04000208 = 1;
}
