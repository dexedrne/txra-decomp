/* Complete HUD owner candidate; uninstalled historical Thumb compiler nonmatch.
 * Shared scratch records preserve the six transform aliases. See README.md. */
typedef struct {
    s16 a, b;
} HudPair;
typedef struct {
    TxraTriple a, b;
} HudRow;
typedef struct {
    s32 active, x, y, size;
} HudFlash;
typedef struct {
    s32 count, x, y, z;
} HudSmoke;
extern HudPair g_030046E0[];
extern s16 g_03002A28, g_03001E50;
extern s32 g_03002338, g_03000B5C, g_0804F330[], g_080213E0[], g_08021420, g_030021D4, g_03001B1C;
extern u8 g_08321C9C[], g_0832259C[], g_03005680[][2];
extern HudFlash g_03000AD0[];
extern HudSmoke g_030067F0[];
extern HudRow g_08020C24[];
extern TxraTriple g_030057A0[], g_030055F0[];
extern s32 g_03005800, g_03005804, g_03005808, g_0300580C, g_03005810, g_03005814;
extern void func_080162F8(s32, s32);
extern s16 g_03000AC0, g_03002330, g_03005F54, g_030001BC, g_03004780;
extern u16 g_03001B14;
extern TxraRecord g_03001E60[];
extern u8 g_08306DE0[], g_08309DE0[], g_083156E0[], g_082BB5CC[], g_082BF5CC[], g_08313EE0[],
    g_0833229C[], g_083118E0[], g_083130E0[];
extern u8 g_03000DE8[];
extern s8 g_03005790[];
extern s32 g_08020304[];
extern u32 g_030021D8, g_030061E4, g_03006680;
extern void func_0801604C(s32, s32);
extern void func_08005CF4(u32, s32, s32, s32, s32);
extern void func_0801533C(u8 *, u32, u32, u32, u32, u32, u32, u32, u32);
#define SPRITE(source, size, a0, a1)                                                               \
    func_0801533C(source, 0x06014000 + g_030061E4 * 32, size, 96, 0, a0, a1, g_030061E4 + 512, 0)
void func_0800421C(void) {
    u32 *g_03006680_cursor;
    s32 t, size, x, y, i, n, c, angle;
    s32 finish_x;
    s32 status_x;
    s32 text_x;
    s32 timer_x;
    s32 hy = 88;
    u8 *source;
    g_03006680_cursor = &g_03006680;
    if (g_03000AC0)
        goto done;
    {
        s32 overlay_size;
        u8 *source_overlay;
        u32 index_overlay;
        u32 overlay_attributes;
        if (g_03002330 > 0) {
            if (--g_03002330 == 0)
                func_0801604C(9, 1);
            if (g_03002330 <= 95) {
                t = g_03002330 & 31;
                if (t > 16)
                    overlay_size = 16;
                else
                    overlay_size = (16 - t) * 4 + 16;
                source_overlay = g_08306DE0 + ((g_03002330 >> 5) << 12);
                func_08005CF4(0, overlay_size, overlay_size, 0, 0);
                index_overlay = g_030061E4;
                {
                    u32 addr = 0x06014000 + index_overlay * 32;
                    overlay_attributes = (g_03006680 << 9) | 0xC000;
                    func_0801533C(source_overlay, addr, 0x1000, 96, 0,
                                  0x2128, overlay_attributes | hy, index_overlay + 512, 0);
                }
                g_03006680++;
                g_030061E4 += 128;
            }
        }
    }
    {
        u32 strip_index;
        if (g_03005F54) {
            if (g_03005F54 > 31 || (g_03005F54 & 1) || g_03002330) {
                source = g_08309DE0 + (g_030021D8 << 11);
                finish_x = 56;
                y = 140;
                i = 3;
                do {
                    SPRITE(source, 0x200, 0x6000 | (y & 0xFF), (finish_x & 0x1FF) | 0x8000);
                    g_030061E4 += 16;
                    source += 0x200;
                    finish_x += 32;
                } while (--i >= 0);
            }
            if ((u16)(g_03005F54 - 1) <= 30)
                g_03005F54--;
        }
        if ((g_030001BC & 32 && g_03002330 > 95) || (u16)(g_030001BC - 1) <= 2) {
            source = g_083156E0 + (g_030021D8 << 11);
            status_x = 56;
            y = 140;
            i = 3;
            do {
                SPRITE(source, 0x200, 0x6000 | (y & 0xFF), (status_x & 0x1FF) | 0x8000);
                g_030061E4 += 16;
                source += 0x200;
                status_x += 32;
            } while (--i >= 0);
            n = g_03001E60[g_03004780].field_62;
            if (n <= 95)
                source = g_082BB5CC + ((n / 6) << 10);
            else
                source = g_082BF5CC + ((n - 96) << 10);
            strip_index = g_030061E4;
            func_0801533C(source, 0x06014000 + strip_index * 32, 0x400, 96, 2, 0x201A, 0x8068,
                          strip_index + 512, 0);
            g_030061E4 += 32;
        }
        if (g_03001B14 <= 1 && g_030001BC) {
            source = g_08313EE0 + (g_030021D8 << 10) + 0x100;
            text_x = 0;
            y = 0;
            t = 208;
            i = 1;
            do {
                SPRITE(source + 0x200, 0x80, 0x6000, t & 0x1FF);
                g_030061E4 += 4;
                source += 0x80;
                t += 16;
            } while (--i >= 0);
            i = 0;
            do {
                c = g_03000DE8[i];
                if (c == ' ')
                    size = 0;
                if (c - 'A' <= 25u)
                    size = c - 64;
                if (c - '0' <= 9u)
                    size = c - 21;
                SPRITE(g_0833229C + size * 64, 0x40, 0x2000 | (y & 0xFF), text_x & 0x1FF);
                g_030061E4 += 2;
                text_x += g_08020304[size];
            } while (++i <= 5);
        }
        if (g_03001B14 == 2 && g_03002330 == 0) {
            source = g_083118E0 + (g_030021D8 << 10);
            timer_x = 88;
            y = 2;
            i = 1;
            do {
                SPRITE(source, 0x200, 0x6000 | (y & 0xFF), (timer_x & 0x1FF) | 0x8000);
                g_030061E4 += 16;
                source += 0x200;
                timer_x += 32;
            } while (--i >= 0);
            SPRITE(g_083130E0 + (g_03005790[0] << 8), 0x100, 0x2010, 0x4056);
            g_030061E4 += 8;
            SPRITE(g_083130E0 + (g_03005790[1] << 8), 0x100, 0x2010, 0x4062);
            g_030061E4 += 8;
            SPRITE(g_083130E0 + 0xA00, 0x100, 0x2010, 0x406E);
            g_030061E4 += 8;
            SPRITE(g_083130E0 + (g_03005790[2] << 8), 0x100, 0x2010, 0x4073);
            g_030061E4 += 8;
            SPRITE(g_083130E0 + (g_03005790[3] << 8), 0x100, 0x2010, 0x407F);
            g_030061E4 += 8;
            SPRITE(g_083130E0 + 0xA00, 0x100, 0x2010, 0x408B);
            g_030061E4 += 8;
            SPRITE(g_083130E0 + (g_03005790[4] << 8), 0x100, 0x2010, 0x4090);
            g_030061E4 += 8;
        }
    }
    c = g_03001E60[0].field_52;
    if (c == 0) {
        t = 0x1964;
        size = g_030046E0[0].b;
    }
    if (c == 1) {
        t = 0x1964;
        size = g_030046E0[1].b;
    }
    if (c == 2) {
        t = 0x1964;
        size = g_030046E0[2].b;
    }
    if (c == 3) {
        t = 0x1964;
        size = g_030046E0[3].b;
    }
    if (c == 4) {
        t = 0x1964;
        size = g_030046E0[4].b;
    }
    n = g_03001E60[0].field_28;
    if (n > 0)
        angle = n * t / size;
    else if (n < 0)
        angle = -n;
    else
        angle = 0;
    g_03002A28 += (angle - g_03002A28) >> 2;
    angle = (g_03002A28 - 5000) & 0x3FFF;
    i = 0;
    y = 98;
    do {
        t = (i << 5) + 512;
        c = (y & 0xFF) | 0x6000;
        x = 172;
        n = 1;
        do {
            {
s32 mask = x & 0x1FF;
            {
s32 arg7 = 0x400 | t;
        func_0801533C((u8 *)1, 0x06014000, 0, 96, 2, c, mask | 0x8000, arg7, 0);
        t += 16;
}
            x += 32;
}
        } while (--n >= 0);
        y += 16;
    } while (++i <= 2);
    func_08005CF4(angle, 16, 16, 0, 0);
    {
u32 tmp_arg;
tmp_arg = (((g_03000B5C >> 8) + 171) & 0x1FF) | ((*g_03006680_cursor) << 9) | 0xC000;
{
u32 mask_arg = (((g_03002338 >> 8) + 97) & 0xFF) | 0x2100;
func_0801533C((u8 *)1, 0x06014000, 0, 96, 0, mask_arg,
                  tmp_arg, 0x260, 0);
(*g_03006680_cursor)++;
}
}
    t = g_03001E60[0].field_28;
    if (t < 0)
        t = -t;
    t /= 20;
    n = t / 100;
    size = (t - n * 100) / 10;
    c = t - (size * 10 + n * 100);
    func_0801533C((u8 *)1, 0x06014000, 0, 96, 0, 0xA08C, 0xC0, (n << 2) + 0x2E0, 0);
    func_0801533C((u8 *)1, 0x06014000, 0, 96, 0, 0xA08C, 0xC8, (size << 2) + 0x2E0, 0);
    func_0801533C((u8 *)1, 0x06014000, 0, 96, 0, 0xA08C, 0xD0, (c << 2) + 0x2E0, 0);
    if (g_03001E60[0].field_28 >= 0)
        t = g_03001E60[0].field_52 + 1;
    else
        t = 6;
    SPRITE(g_08321C9C + (t << 8), 0x100, 0x2090, 0x40DF);
    g_030061E4 += 8;
    {
        s32 *map_zscale;
        {
            s32 map_scale;
            {
                s32 map_x;
                if (g_03001E50 == 0) {
                    map_scale = 0x1C20;
                    angle = 0x1C20;
                }
                if (g_03001E50 == 1) {
                    map_scale = 0x1400;
                    angle = 0x1400;
                }
                if (g_03001E50 == 2) {
                    angle = 0x1C20;
                    map_scale = 0x1400;
                }
                if (g_03001E50 == 3) {
                    angle = 0x1F40;
                    map_scale = 0x1B58;
                }
                if (g_03001E50 == 4) {
                    map_scale = 0x1B58;
                    angle = 0x1B58;
                }
                if (g_03001E50 == 5) {
                    angle = 0x1900;
                    map_scale = 0x1194;
                }
                map_zscale = &g_0804F330[map_scale + 0x10000];
                for (i = 0; i <= 7; i++) {
                    TxraRecord *car = &g_03001E60[i];
                    if (!car->field_00)
                        continue;
                    if (i != 0 && i <= 3)
                        continue;
                    map_x = (-car->field_04 * g_0804F330[angle + 0x10000]) >> 19;
                    y = (car->field_0c * *map_zscale) >> 19;
                    map_x += 1;
                    if (g_03001E50 == 2)
                        map_x -= 1;
                    if (g_03001E50 == 4)
                        map_x += 3;
                    source = g_0832259C;
                    if (i == 0)
                        source += 0x80;
                    else if (g_03005680[car->field_62][0])
                        source += 0x40;
                    SPRITE(source, 0x100, ((y + 118) & 0xFF) | 0x2000, (map_x + 30) & 0x1FF);
                    g_030061E4 += 2;
                }
            }
        }
    }
    i = 0;
    do {
        if (g_03000AD0[i].active) {
            if (g_03000AD0[i].size > 17)
                g_03000AD0[i].size = 17;
            t = g_080213E0[g_03000AD0[i].size];
            func_08005CF4(0, t, t, 0, 0);
            func_0801533C((u8 *)1, 0x06014000 + g_030061E4 * 32, 0x400, 96, 0,
                          ((g_03000AD0[i].y - 16) & 0xFF) | 0x2500,
                          ((g_03000AD0[i].x - 16) & 0x1FF) | ((*g_03006680_cursor) << 9) | 0x8000,
                          0x308, 0);
            g_03000AD0[i].active = 0;
            (*g_03006680_cursor)++;
        }
    } while (++i <= 7);
    {
        s32 c_projection;
        s32 y_projection;
        s32 t_projection;
        {
                n = g_03001E60[0].field_02 - 16;
            if (g_03001E60[0].field_44 & 2) {
                if (g_030021D4 != 1)
                    goto done;
                g_030057A0[8].field_00 = *(s32 *)&g_03001E60[0].unknown_10[12];
                g_030057A0[8].field_04 = g_03001E60[0].field_20;
                g_030057A0[8].field_08 = g_03001E60[0].field_24;
                g_030057A0[9].field_00 = g_03001E60[0].field_04;
                g_030057A0[9].field_04 = g_03001E60[0].field_08;
                g_030057A0[9].field_08 = g_03001E60[0].field_0c;
                g_030057A0[0].field_00 = g_08020C24[n].a.field_00 + 40;
                g_030057A0[0].field_04 = g_08020C24[n].a.field_04;
                g_030057A0[0].field_08 = g_08020C24[n].a.field_08;
                g_030057A0[1].field_00 = g_08020C24[n].a.field_00;
                g_030057A0[1].field_04 = g_08020C24[n].a.field_04;
                g_030057A0[1].field_08 = g_08020C24[n].a.field_08;
                g_030057A0[2].field_00 = -g_08020C24[n].a.field_00;
                g_030057A0[2].field_04 = g_08020C24[n].a.field_04;
                g_030057A0[2].field_08 = g_08020C24[n].a.field_08;
                g_030057A0[3].field_00 = -g_08020C24[n].a.field_00 - 40;
                g_030057A0[3].field_04 = g_08020C24[n].a.field_04;
                g_030057A0[3].field_08 = g_08020C24[n].a.field_08;
                func_080162F8(0, 0);
                func_080162F8(1, 0);
                func_080162F8(2, 0);
                func_080162F8(3, 0);
                angle = g_030055F0[1].field_00 - g_030055F0[0].field_00;
                size = g_030055F0[3].field_00 - g_030055F0[2].field_00;
                c_projection = 0x328;
                if (g_03001E60[0].field_28 < 0)
                    c_projection = 0x340;
                if (angle > 0) {
                    x = g_030055F0[1].field_00;
                    y_projection = g_030055F0[1].field_04;
                    t_projection = g_080213E0[angle];
                    func_08005CF4(0, t_projection, t_projection, 0, 0);
                    func_0801533C((u8 *)1, 0x06014000 + g_030061E4 * 32, 0x400, 96, 0,
                                  ((y_projection - 8) & 0xFF) | 0x2500,
                                  ((x - 8) & 0x1FF) | ((*g_03006680_cursor) << 9) | 0x4000,
                                  c_projection, 0);
                    (*g_03006680_cursor)++;
                }
                if (size > 0) {
                    x = g_030055F0[2].field_00;
                    y_projection = g_030055F0[2].field_04;
                    t_projection = g_080213E0[size];
                    func_08005CF4(0, t_projection, t_projection, 0, 0);
                    func_0801533C((u8 *)1, 0x06014000 + g_030061E4 * 32, 0x400, 96, 0,
                                  ((y_projection - 8) & 0xFF) | 0x2500,
                                  ((x - 8) & 0x1FF) | ((*g_03006680_cursor) << 9) | 0x4000,
                                  c_projection, 0);
                    (*g_03006680_cursor)++;
                }
            }
            if (g_030021D4 != 1)
                goto done;
            g_030057A0[8].field_00 = *(s32 *)&g_03001E60[0].unknown_10[12];
            g_030057A0[8].field_04 = g_03001E60[0].field_20;
            g_030057A0[8].field_08 = g_03001E60[0].field_24;
            g_030057A0[9].field_00 = g_03001E60[0].field_04;
            g_030057A0[9].field_04 = g_03001E60[0].field_08;
            g_030057A0[9].field_08 = g_03001E60[0].field_0c;
            g_030057A0[0].field_00 = -g_08020C24[n].b.field_00 - 32;
            g_030057A0[0].field_04 = g_08020C24[n].b.field_04;
            g_030057A0[0].field_08 = g_08020C24[n].b.field_08;
            g_030057A0[1].field_00 = -g_08020C24[n].b.field_00;
            g_030057A0[1].field_04 = g_08020C24[n].b.field_04;
            g_030057A0[1].field_08 = g_08020C24[n].b.field_08;
            g_030057A0[2].field_00 = g_08020C24[n].b.field_00;
            g_030057A0[2].field_04 = g_08020C24[n].b.field_04;
            g_030057A0[2].field_08 = g_08020C24[n].b.field_08;
            g_030057A0[3].field_00 = g_08020C24[n].b.field_00 + 32;
            g_030057A0[3].field_04 = g_08020C24[n].b.field_04;
            g_030057A0[3].field_08 = g_08020C24[n].b.field_08;
            func_080162F8(0, 0);
            func_080162F8(1, 0);
            func_080162F8(2, 0);
            func_080162F8(3, 0);
            angle = g_030055F0[1].field_00 - g_030055F0[0].field_00;
            size = g_030055F0[3].field_00 - g_030055F0[2].field_00;
            if (angle > 0) {
                x = g_030055F0[1].field_00;
                y_projection = g_030055F0[1].field_04;
                t_projection = g_08021420;
                func_08005CF4(0, t_projection, t_projection, 0, 0);
                func_0801533C((u8 *)1, 0x06014000 + g_030061E4 * 32, 0x400, 96, 0,
                              ((y_projection - 8) & 0xFF) | 0x2500,
                              ((x - 8) & 0x1FF) | ((*g_03006680_cursor) << 9) | 0x4000, 0x330, 0);
                (*g_03006680_cursor)++;
            }
            if (size > 0) {
                x = g_030055F0[2].field_00;
                y_projection = g_030055F0[2].field_04;
                t_projection = g_08021420;
                func_08005CF4(0, t_projection, t_projection, 0, 0);
                func_0801533C((u8 *)1, 0x06014000 + g_030061E4 * 32, 0x400, 96, 0,
                              ((y_projection - 8) & 0xFF) | 0x2500,
                              ((x - 8) & 0x1FF) | ((*g_03006680_cursor) << 9) | 0x4000, 0x330, 0);
                (*g_03006680_cursor)++;
            }
            if (g_030021D4 != 1)
                goto done;
        }
    }
    {
        s32 *smoke_y = &g_030067F0[0].y;
        s32 *smoke_x = &g_030067F0[0].x;
        s32 *smoke_count = &g_030067F0[0].count;
        s32 smoke_offset = 0;
        s32 *smoke_z = &g_030067F0[0].z;
        do {
            if (g_030067F0[smoke_offset / 16].count == 0) {
                if ((g_03001E60[0].field_44 & 2 && g_03001E60[0].field_28 > 0) ||
                    (g_03001E60[0].field_44 & 1 && g_03001E60[0].field_28 <= 799)) {
                    g_030067F0[smoke_offset / 16].count = 6;
                    (*smoke_x) = -56;
                    if (g_03001B1C & 4)
                        (*smoke_x) = 56;
                    g_030067F0[smoke_offset / 16].y = 0;
                    g_030067F0[smoke_offset / 16].z = 193;
                } else if (g_03001E60[0].field_40 > 44) {
                    if (g_03001E60[0].field_30 <= 199) {
                        (*smoke_count) = 6;
                        (*smoke_x) = -56;
                        (*smoke_y) = 0;
                        (*smoke_z) = 193;
                    }
                    if (g_03001E60[0].field_30 > 200) {
                        (*smoke_count) = 6;
                        (*smoke_x) = 56;
                        (*smoke_y) = 0;
                        (*smoke_z) = 193;
                    }
                }
                break;
            }
            smoke_y += 4;
            smoke_x += 4;
            smoke_count += 4;
            smoke_z += 4;
            smoke_offset += 16;
        } while (smoke_y <= &g_030067F0[7].y);
    }
    g_030057A0[8].field_00 = *(s32 *)&g_03001E60[0].unknown_10[12];
    g_030057A0[8].field_04 = g_03001E60[0].field_20;
    g_030057A0[8].field_08 = g_03001E60[0].field_24;
    g_030057A0[9].field_00 = g_03001E60[0].field_04;
    g_030057A0[9].field_04 = g_03001E60[0].field_08;
    g_030057A0[9].field_08 = g_03001E60[0].field_0c;
    {
        s32 c_split_smoke;
        i = 0;
        do {
            if (g_030067F0[i].count == 0)
                continue;
            g_030067F0[i].count--;
            g_030057A0[0].field_00 = g_030067F0[i].x;
            g_030057A0[0].field_04 = g_030067F0[i].y;
            g_030057A0[0].field_08 = g_030067F0[i].z;
            func_080162F8(0, 0);
            g_030055F0[0].field_08 >>= 4;
            if (g_030055F0[0].field_08 > 32) {
                t = 16 - g_030067F0[i].count * 2;
                x = g_030055F0[0].field_00;
                y = g_030055F0[0].field_04;
                c_split_smoke = g_080213E0[t];
                func_08005CF4(0, c_split_smoke, c_split_smoke, 0, 0);
                func_0801533C((u8 *)1, 0x06014000 + g_030061E4 * 32, 0x400, 96, 0,
                              ((y - 8) & 0xFF) | 0x2500,
                              ((x - 8) & 0x1FF) | ((*g_03006680_cursor) << 9) | 0x4000, 0x338, 0);
                (*g_03006680_cursor)++;
                c_split_smoke = g_03001E60[0].field_28 >> 6;
                if (c_split_smoke < 0)
                    c_split_smoke = -c_split_smoke;
                c_split_smoke += g_03001B1C & 15;
                g_030067F0[i].z += c_split_smoke;
                g_030067F0[i].y -= 2;
            }
        } while (++i <= 7);
    }
done:;
}
