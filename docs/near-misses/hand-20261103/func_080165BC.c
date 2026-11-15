/* Unmatched 11/3 draft (21 instruction lines, same 1628 bytes and frame; ARM profile): only the vertex-loop tail differs. With z <<= 3 inline (as here) the registers match but sched2 puts the sy chain before sx; with z <<= 3 in place the order matches but global-alloc swaps y and z (ip/lr). Excluded from the build. */
typedef struct Quad {
    s16 x[4];
    s16 y[4];
    u8 u[4], v[4];
    u16 count, kind;
    struct Quad *next;
} Quad;
typedef struct { s32 x, y, z; } Vertex;
typedef struct { s32 sx, sy, depth, pad[4]; } Projected;
typedef struct { s32 index[4]; s32 shade[4]; s32 tex[4]; s32 unused; s32 bias; } Face;
typedef struct { s32 vertices, faces, count; } ModelInfo;
typedef struct { Face *faces; ModelInfo *info; Vertex *lod[9]; } Model;
extern TxraRecord g_03001E60[];
extern void *g_08020E24[][11];
extern s32 g_083D2280[], g_083C2280[], g_0804F330[];
extern s32 g_03005FC8, g_03005B30, g_03002E5C, g_030061E0;
extern s32 g_03002A18, g_03001B28, g_03000DF8, g_03005F58;
extern TxraTriple g_03005F70, g_03005F80;
extern s32 g_030001C4;
extern s16 g_03002E54;
extern Quad *g_030021C4, *g_03000670[];
void func_080165BC(s32 slot, s32 model)
{
    s32 d[4];
    s32 lod, i;
    Vertex *vertex;
    Face *face;
    ModelInfo *info;
    s32 nvertices, nfaces, count;
    s32 ox, oy, oz, dx, dy, dz;
    Projected *out;
    dx = g_03005F70.field_00 - g_03001E60[slot].field_04;
    dy = g_03005F70.field_04 - g_03001E60[slot].field_08;
    dz = g_03005F70.field_08 - g_03001E60[slot].field_0c;
    face = g_08020E24[model][0];
    info = g_08020E24[model][1];
    nvertices = info->vertices;
    nfaces = info->faces;
    count = info->count;
    lod = (g_03001E60[slot].field_4e >> 1) + 6;
    if (lod < 2) lod = 2;
    if (lod > 10) lod = 10;
    vertex = g_08020E24[model][lod];
    g_03005FC8 = g_083D2280[g_03001E60[slot].field_24];
    g_03005B30 = g_083C2280[g_03001E60[slot].field_24];
    g_03002E5C = g_083D2280[g_03001E60[slot].field_20];
    g_030061E0 = g_083C2280[g_03001E60[slot].field_20];
    ox = g_03005F80.field_00;
    oy = g_03005F80.field_04;
    oz = g_03005F80.field_08;
    out = (Projected *)0x02019400;
    for (i = 0; i < nvertices; i++) {
        s32 x, y, z, xx, zz, saved_x, saved_y, factor;
        x = vertex->x;
        y = -vertex->y;
        z = vertex->z;
        xx = x;
        saved_y = (y * g_03005FC8 - z * g_03005B30) >> 12;
        zz = (y * g_03005B30 + z * g_03005FC8) >> 12;
        x = (xx * g_03002E5C - zz * g_030061E0) >> 12;
        z = (xx * g_030061E0 + zz * g_03002E5C) >> 12;
        x -= dx;
        y = saved_y - dy;
        z -= dz;
        xx = (x * g_03002A18 - z * g_03001B28) >> 12;
        saved_y = y;
        zz = (x * g_03001B28 + z * g_03002A18) >> 12;
        y = (saved_y * g_03000DF8 - zz * g_03005F58) >> 12;
        z = (saved_y * g_03005F58 + zz * g_03000DF8) >> 12;
        x = xx + ox;
        z += oy;
        y += oz;
        out->depth = y;
        x <<= 3;
        y >>= 1;
        factor = g_0804F330[y + 0x10000];
        out->sx = g_030001C4 + ((x * factor) >> 16);
        out->sy = (((z << 3) * factor) >> 15) + 80;
        vertex++;
        out++;
    }
    out = (Projected *)0x02019400;
    for (i = 0; i < nfaces; i++) {
        Projected *p0 = (Projected *)(face->index[0] * sizeof(Projected) + (u32)out);
        Projected *p1 = (Projected *)(face->index[1] * sizeof(Projected) + (u32)out);
        Projected *p3 = (Projected *)(face->index[2] * sizeof(Projected) + (u32)out);
        Projected *p2 = (Projected *)(face->index[3] * sizeof(Projected) + (u32)out);
        d[0] = p0->depth;
        d[1] = p1->depth;
        d[2] = p2->depth;
        d[3] = p3->depth;
        if (d[0] > 63 && d[1] > 63 && d[2] > 63 && d[3] > 63) {
            { Quad *q = g_030021C4;
            q->x[0] = p0->sx;
            q->y[0] = p0->sy;
            q->x[1] = p1->sx;
            q->y[1] = p1->sy;
            q->x[2] = p2->sx;
            q->y[2] = p2->sy;
            q->x[3] = p3->sx;
            q->y[3] = p3->sy;
            }
            if ((g_030021C4->x[3] - g_030021C4->x[0]) * (g_030021C4->y[1] - g_030021C4->y[0]) - (g_030021C4->x[1] - g_030021C4->x[0]) * (g_030021C4->y[3] - g_030021C4->y[0]) <= 0
             && ((u16)g_030021C4->x[0] <= 119 || (u16)g_030021C4->x[1] <= 119 || (u16)g_030021C4->x[2] <= 119 || (u16)g_030021C4->x[3] <= 119)
             && ((u16)g_030021C4->y[0] <= 159 || (u16)g_030021C4->y[1] <= 159 || (u16)g_030021C4->y[2] <= 159 || (u16)g_030021C4->y[3] <= 159)) {
                s32 depth;
                g_030021C4->u[0] = 127 - (face->shade[0] >> 1);
                g_030021C4->v[0] = face->tex[0];
                g_030021C4->u[1] = 127 - (face->shade[1] >> 1);
                g_030021C4->v[1] = face->tex[1];
                g_030021C4->u[2] = 127 - (face->shade[2] >> 1);
                g_030021C4->v[2] = face->tex[2];
                g_030021C4->u[3] = 127 - (face->shade[3] >> 1);
                g_030021C4->v[3] = face->tex[3];
                if (g_030021C4->x[0] <= -67) g_030021C4->x[0] = -66;
                if (g_030021C4->x[1] <= -67) g_030021C4->x[1] = -66;
                if (g_030021C4->x[2] <= -67) g_030021C4->x[2] = -66;
                if (g_030021C4->x[3] <= -67) g_030021C4->x[3] = -66;
                if (g_030021C4->x[0] > 186) g_030021C4->x[0] = 186;
                if (g_030021C4->x[1] > 186) g_030021C4->x[1] = 186;
                if (g_030021C4->x[2] > 186) g_030021C4->x[2] = 186;
                if (g_030021C4->x[3] > 186) g_030021C4->x[3] = 186;
                depth = face->bias + ((d[0] + d[1] + d[2] + d[3]) >> 7);
                depth -= 8;
                g_030021C4->count = count;
                if (depth < 0) depth = 0;
                if (depth > 240) depth = 240;
                if (g_03002E54 == 0) g_030021C4->kind = 0;
                else g_030021C4->kind = 3;
                if (!g_03000670[depth]) {
                    g_030021C4->next = 0;
                    g_030021C4++;
                    g_03000670[depth] = g_030021C4 - 1;
                } else {
                    g_030021C4->next = g_03000670[depth];
                    g_030021C4++;
                    g_03000670[depth] = g_030021C4 - 1;
                }
            }
        }
        face++;
    }
}
