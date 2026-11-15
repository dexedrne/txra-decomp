/* Unmatched deep-l draft (161 differing instructions); excluded from the ROM build. */
extern TxraRecord g_03001E60[];
extern TxraTriple g_03005F80, g_03005F70, g_030057A0[], g_030055F0[];
extern s32 g_083D2280[], g_083C2280[], g_0804F330[];
extern s32 g_03005FC8, g_03005B30, g_03002E5C, g_030061E0;
extern s32 g_03002A18, g_03001B28, g_03000DF8, g_03005F58;
void func_080162F8(s32 point, s32 slot)
{
    volatile TxraTriple v[2];
    s32 x, y, z, a, b, c, d, e, f, scale;
    v[0].field_00 = g_03005F80.field_00;
    v[0].field_04 = g_03005F80.field_04;
    v[0].field_08 = g_03005F80.field_08;
    v[1].field_00 = g_03005F70.field_00 - g_03001E60[slot].field_04;
    v[1].field_04 = g_03005F70.field_04 - g_03001E60[slot].field_08;
    v[1].field_08 = g_03005F70.field_08 - g_03001E60[slot].field_0c;
    g_03005FC8 = g_083D2280[g_03001E60[slot].field_24];
    g_03005B30 = g_083C2280[g_03001E60[slot].field_24];
    g_03002E5C = g_083D2280[g_03001E60[slot].field_20];
    g_030061E0 = g_083C2280[g_03001E60[slot].field_20];
    x = g_030057A0[point].field_00;
    y = -g_030057A0[point].field_04;
    z = g_030057A0[point].field_08;
    a = (g_03005FC8 * y - g_03005B30 * z) >> 12;
    b = (g_03005B30 * y + g_03005FC8 * z) >> 12;
    c = (x * g_03002E5C - g_030061E0 * b) >> 12;
    d = (x * g_030061E0 + b * g_03002E5C) >> 12;
    c -= v[1].field_00;
    e = a - v[1].field_04;
    d -= v[1].field_08;
    a = (g_03002A18 * c - g_03001B28 * d) >> 12;
    b = (c * g_03001B28 + g_03002A18 * d) >> 12;
    f = (e * g_03000DF8 - b * g_03005F58) >> 12;
    d = (e * g_03005F58 + b * g_03000DF8) >> 12;
    x = v[0].field_00 + a;
    y = v[0].field_04 + d;
    z = v[0].field_08 + f;
    g_030055F0[point].field_08 = z;
    x <<= 3; y <<= 3; z >>= 1;
    scale = g_0804F330[z + 65536];
    g_030055F0[point].field_00 = (x * scale >> 15) + 120;
    g_030055F0[point].field_04 = (y * scale >> 15) + 80;
}
