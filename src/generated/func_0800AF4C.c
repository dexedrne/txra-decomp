/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Per-slot car stat setup: slot 0 reads its spec from the record's model,
 * slots 1-3 get fixed values, slots 4-7 pick a spec from field_62 / 24.
 * Each case takes the record array base in its own temporary before
 * indexing, which keeps the base load ahead of the * 100. */
extern TxraRecord g_03001E60[];
extern s16 g_030046E0[][10];
typedef struct { u16 a[5]; s16 b[6]; u16 c[3]; } CarSpec;
extern CarSpec g_08020404[];
extern void func_0800A940(s32);
extern void func_0800AC3C(s32);
void func_0800AF4C(s32 slot)
{
    s32 k;
    switch (slot) {
    case 0: {
        TxraRecord *base = g_03001E60;
        TxraRecord *rec = base + slot;
        k = rec->field_02 - 16;
        g_030046E0[slot][0] = g_08020404[k].a[0];
        g_030046E0[slot][1] = g_08020404[k].b[0] * 20;
        g_030046E0[slot][2] = g_08020404[k].a[1];
        g_030046E0[slot][3] = g_08020404[k].b[1] * 20;
        g_030046E0[slot][4] = g_08020404[k].a[2];
        g_030046E0[slot][5] = g_08020404[k].b[2] * 20;
        g_030046E0[slot][6] = g_08020404[k].a[3];
        g_030046E0[slot][7] = g_08020404[k].b[3] * 20;
        g_030046E0[slot][8] = g_08020404[k].a[4];
        g_030046E0[slot][9] = g_08020404[k].b[4] * 20;
        rec->field_54 = g_08020404[k].c[2];
        rec->field_56 = g_08020404[k].c[1];
        rec->field_58 = g_08020404[k].c[0];
        rec->field_5a = 6;
        rec->field_5e = 0;
        rec->field_60 = g_08020404[k].b[5] * 20;
        func_0800A940(slot);
        break;
    }
    case 1:
    case 2:
    case 3: {
        TxraRecord *base, *rec;
        g_030046E0[slot][0] = 256;
        g_030046E0[slot][1] = 500;
        g_030046E0[slot][2] = 192;
        g_030046E0[slot][3] = 900;
        g_030046E0[slot][4] = 128;
        g_030046E0[slot][5] = 1500;
        g_030046E0[slot][6] = 96;
        g_030046E0[slot][7] = 1900;
        g_030046E0[slot][8] = 64;
        g_030046E0[slot][9] = 2300;
        base = g_03001E60;
        rec = base + slot;
        rec->field_54 = 150;
        rec->field_56 = 1000;
        rec->field_58 = 1900;
        rec->field_5a = 32;
        rec->field_5e = 0;
        rec->field_60 = 2400;
        break;
    }
    case 4:
    case 5:
    case 6:
    case 7: {
        s32 q;
        TxraRecord *base = g_03001E60;
        TxraRecord *rec = base + slot;
        q = (s16)(rec->field_62 / 24);
        k = 0;
        if (q == 1) k = 1;
        if (q == 2) k = 2;
        if (q == 3) k = 3;
        if (q == 4) k = 4;
        if (q == 5) k = 5;
        g_030046E0[slot][0] = g_08020404[k].a[0];
        g_030046E0[slot][1] = g_08020404[k].b[0] * 20;
        g_030046E0[slot][2] = g_08020404[k].a[1];
        g_030046E0[slot][3] = g_08020404[k].b[1] * 20;
        g_030046E0[slot][4] = g_08020404[k].a[2];
        g_030046E0[slot][5] = g_08020404[k].b[2] * 20;
        g_030046E0[slot][6] = g_08020404[k].a[3];
        g_030046E0[slot][7] = g_08020404[k].b[3] * 20;
        g_030046E0[slot][8] = g_08020404[k].a[4];
        g_030046E0[slot][9] = g_08020404[k].b[4] * 20;
        rec->field_54 = g_08020404[k].c[2];
        rec->field_56 = g_08020404[k].c[1];
        rec->field_58 = g_08020404[k].c[0];
        rec->field_5a = 6;
        rec->field_5e = 0;
        rec->field_60 = g_08020404[k].b[5] * 20;
        func_0800AC3C(slot);
        break;
    }
    }
}
