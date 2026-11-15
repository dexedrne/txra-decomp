/* Unmatched diagnostic source; not installed or accepted as behavior-correct. */
extern u8 g_03000A70[];
extern u32 g_03001B18,g_03002E58,g_030066D4;
extern void func_080154AC(TxraTextRecord *);
void func_08010910(u32 x, u32 y, u32 flags, s32 value)
{
    u8 *cursor = g_03000A70;
    u32 emitted = 0;
    do { g_03001B18 = flags & 7;
    g_03002190.field_00 = x;
    g_03002190.field_01 = y; } while (0);
    g_03002E58 = 0;
    g_030066D4 = y;
    g_03002190.field_04 = cursor;
    g_03002190.field_08 = 1;
    g_03002190.field_09 = 1;
    if (flags & 8) { g_03002190.field_01 = 80; g_03002190.field_00 = 8; }
    if (!(flags & 16)) *cursor = 36; else *cursor = 35;
    cursor++;
    if (value > 99999 || emitted == 1) {
        s32 digit; flags = 100000; digit = value / (s32)flags;
        value -= digit * flags;
        *cursor++ = digit + 48;
        emitted = 1;
    }
    if (value > 9999 || emitted == 1) {
        s32 digit; flags = 10000; digit = value / (s32)flags;
        value -= digit * flags;
        *cursor++ = digit + 48;
        emitted = 1;
    }
    if (value > 999 || emitted == 1) {
        s32 digit = value / 1000;
        value -= digit * 1000;
        *cursor++ = digit + 48;
        emitted = 1;
    }
    if (value > 99 || emitted == 1) {
        s32 digit; flags = 100; digit = value / (s32)flags;
        value -= digit * flags;
        *cursor++ = digit + 48;
        emitted = 1;
    }
    if (value > 9 || emitted == 1) {
        s32 digit = value / 10;
        value -= digit * 10;
        *cursor++ = digit + 48;
    }
    cursor[0] = value + 48;
    cursor[1] = 0;
    func_080154AC(&g_03002190);
}
