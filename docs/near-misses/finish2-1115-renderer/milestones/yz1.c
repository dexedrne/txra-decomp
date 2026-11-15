/* 08016DA8 renderer milestone (11/15), NOT an exact match: 2,430 differing bytes.
 * ARM profile: agbcc_arm -O2 -mthumb-interwork, owner end 08017E68.
 * The 11/14 natural source plus one do { } while (0) around the y/z scratch
 * stores of each part block. That raises the scratch pointer's loop-weighted
 * references (195 -> 227), so global allocation takes it before the points
 * base: points base in sb, scratch pointer (shared with a) in sl, as in the
 * cartridge. Behaviour is unchanged. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;

typedef struct { s32 x, y, z, flag, sx, sy, depth; } Point;
typedef struct { u16 kind, pad; s32 idx[4]; s32 u[4]; s32 v[4]; u16 tex, pad2; } Face;
typedef struct Packet { s16 x[4]; s16 y[4]; u8 u[4]; u8 v[4]; u16 tex, mode; struct Packet *next; } Packet;
typedef struct { s32 x, y, z; } Vec3;
typedef struct { s32 active, x, y, w; } Special;

#define gPoints ((Point *)0x02014000)
#define gFaces ((Face *)0x02033B70)

extern u32 g_030001B8;
extern Packet *g_030021C4;
extern Packet *g_03000670[];
extern Vec3 g_030057A0[];
extern Vec3 g_03005F70;
extern Vec3 g_03005F80;
extern s32 g_03002A18, g_03001B28, g_03005F58, g_03000DF8;
extern Vec3 g_030055F8[];
extern s32 g_0804F330[];
extern s32 g_03000DE0;
extern Special g_03000AD0[];

#define gCurPacket g_030021C4
#define gBuckets g_03000670
#define gScratch g_030057A0
#define gCamera g_03005F70
#define gOffset g_03005F80

void func_08016DA8(void)
{
    s32 depth[4];
    u32 tick, ring, end;
    Face *face;
    s32 part, a, b, c, d, i, z;
    Point *pts = gPoints;

    tick = g_030001B8;
    ring = (tick - 29) & 31;
    end = (tick - 6) & 31;
    do {
        for (face = &gFaces[ring * 24]; face->kind != 0; face++) {
            a = face->idx[0];
            b = face->idx[1];
            c = face->idx[2];
            d = face->idx[3];
            depth[0] = pts[a].depth;
            depth[1] = pts[b].depth;
            depth[2] = pts[c].depth;
            depth[3] = pts[d].depth;
            if (depth[0] <= 767 || depth[1] <= 767 || depth[2] <= 767 || depth[3] <= 767) {
                for (part = 0; part < 4; part++) {
                    if (depth[part] < 0) continue;
                    if (part == 0) {
                        gScratch[0].x = pts[a].x;
                        gScratch[1].x = (pts[a].x + pts[b].x) >> 1;
                        gScratch[2].x = (pts[a].x + pts[c].x) >> 1;
                        gScratch[3].x = (pts[a].x + pts[d].x) >> 1;
do {
                        gScratch[0].y = pts[a].y;
                        gScratch[1].y = (pts[a].y + pts[b].y) >> 1;
                        gScratch[2].y = (pts[a].y + pts[c].y) >> 1;
                        gScratch[3].y = (pts[a].y + pts[d].y) >> 1;
                        gScratch[0].z = pts[a].z;
                        gScratch[1].z = (pts[a].z + pts[b].z) >> 1;
                        gScratch[2].z = (pts[a].z + pts[c].z) >> 1;
                        gScratch[3].z = (pts[a].z + pts[d].z) >> 1;
} while (0);
                    }
                    if (part == 1) {
                        gScratch[0].x = (pts[a].x + pts[b].x) >> 1;
                        gScratch[1].x = pts[b].x;
                        gScratch[2].x = (pts[b].x + pts[c].x) >> 1;
                        gScratch[3].x = (pts[a].x + pts[c].x) >> 1;
do {
                        gScratch[0].y = (pts[a].y + pts[b].y) >> 1;
                        gScratch[1].y = pts[b].y;
                        gScratch[2].y = (pts[b].y + pts[c].y) >> 1;
                        gScratch[3].y = (pts[a].y + pts[c].y) >> 1;
                        gScratch[0].z = (pts[a].z + pts[b].z) >> 1;
                        gScratch[1].z = pts[b].z;
                        gScratch[2].z = (pts[b].z + pts[c].z) >> 1;
                        gScratch[3].z = (pts[a].z + pts[c].z) >> 1;
} while (0);
                    }
                    if (part == 2) {
                        gScratch[0].x = (pts[a].x + pts[c].x) >> 1;
                        gScratch[1].x = (pts[b].x + pts[c].x) >> 1;
                        gScratch[2].x = pts[c].x;
                        gScratch[3].x = (pts[d].x + pts[c].x) >> 1;
do {
                        gScratch[0].y = (pts[a].y + pts[c].y) >> 1;
                        gScratch[1].y = (pts[b].y + pts[c].y) >> 1;
                        gScratch[2].y = pts[c].y;
                        gScratch[3].y = (pts[d].y + pts[c].y) >> 1;
                        gScratch[0].z = (pts[a].z + pts[c].z) >> 1;
                        gScratch[1].z = (pts[b].z + pts[c].z) >> 1;
                        gScratch[2].z = pts[c].z;
                        gScratch[3].z = (pts[d].z + pts[c].z) >> 1;
} while (0);
                    }
                    if (part == 3) {
                        gScratch[0].x = (pts[a].x + pts[d].x) >> 1;
                        gScratch[1].x = (pts[a].x + pts[c].x) >> 1;
                        gScratch[2].x = (pts[d].x + pts[c].x) >> 1;
                        gScratch[3].x = pts[d].x;
do {
                        gScratch[0].y = (pts[a].y + pts[d].y) >> 1;
                        gScratch[1].y = (pts[a].y + pts[c].y) >> 1;
                        gScratch[2].y = (pts[d].y + pts[c].y) >> 1;
                        gScratch[3].y = pts[d].y;
                        gScratch[0].z = (pts[a].z + pts[d].z) >> 1;
                        gScratch[1].z = (pts[a].z + pts[c].z) >> 1;
                        gScratch[2].z = (pts[d].z + pts[c].z) >> 1;
                        gScratch[3].z = pts[d].z;
} while (0);
                    }
                    {
                        for (i = 0; i < 4; i++) {
                            s32 dx, dy, dz, tx, ty, tz, f;
                            dx = gScratch[i].x - gCamera.x;
                            dz = gScratch[i].z - gCamera.z;
                            tx = g_03002A18 * dx - g_03001B28 * dz;
                            tz = (g_03001B28 * dx + g_03002A18 * dz) >> 12;
                            dy = -gScratch[i].y - gCamera.y;
                            ty = g_03005F58 * dy + g_03000DF8 * tz;
                            tz = gOffset.z + ((g_03000DF8 * dy - g_03005F58 * tz) >> 12);
                            g_030055F8[i].x = tz;
                            f = g_0804F330[(tz >> 1) + 0x10000];
                            gCurPacket->x[i] = ((f * ((gOffset.x + (tx >> 12)) << 3)) >> 16) + 60;
                            gCurPacket->y[i] = ((f * ((gOffset.y + (ty >> 12)) << 3)) >> 15) + 80;
                        }
                    }
                    if (!((gCurPacket->x[0] >= 0 && gCurPacket->x[0] < 120 && gCurPacket->y[0] >= 0 && gCurPacket->y[0] < 160)
                       || (gCurPacket->x[1] >= 0 && gCurPacket->x[1] < 120 && gCurPacket->y[1] >= 0 && gCurPacket->y[1] < 160)
                       || (gCurPacket->x[2] >= 0 && gCurPacket->x[2] < 120 && gCurPacket->y[2] >= 0 && gCurPacket->y[2] < 160)
                       || (gCurPacket->x[3] >= 0 && gCurPacket->x[3] < 120 && gCurPacket->y[3] >= 0 && gCurPacket->y[3] < 160)))
                        continue;
                    gCurPacket->y[0]--;
                    gCurPacket->x[0]--;
                    gCurPacket->y[1]--;
                    gCurPacket->x[1]++;
                    if (gCurPacket->y[0] < -175) gCurPacket->y[0] = -174;
                    if (gCurPacket->y[1] < -175) gCurPacket->y[1] = -174;
                    if (gCurPacket->y[2] < -175) gCurPacket->y[2] = -174;
                    if (gCurPacket->y[3] < -175) gCurPacket->y[3] = -174;
                    if (gCurPacket->y[0] > 335) gCurPacket->y[0] = 334;
                    if (gCurPacket->y[1] > 335) gCurPacket->y[1] = 334;
                    if (gCurPacket->y[2] > 335) gCurPacket->y[2] = 334;
                    if (gCurPacket->y[3] > 335) gCurPacket->y[3] = 334;
                    if (gCurPacket->x[0] <= -67) gCurPacket->x[0] = -66;
                    if (gCurPacket->x[1] <= -67) gCurPacket->x[1] = -66;
                    if (gCurPacket->x[2] <= -67) gCurPacket->x[2] = -66;
                    if (gCurPacket->x[3] <= -67) gCurPacket->x[3] = -66;
                    if (gCurPacket->x[0] > 186) gCurPacket->x[0] = 186;
                    if (gCurPacket->x[1] > 186) gCurPacket->x[1] = 186;
                    if (gCurPacket->x[2] > 186) gCurPacket->x[2] = 186;
                    if (gCurPacket->x[3] > 186) gCurPacket->x[3] = 186;
                    if ((gCurPacket->x[3] - gCurPacket->x[0]) * (gCurPacket->y[1] - gCurPacket->y[0])
                      - (gCurPacket->x[1] - gCurPacket->x[0]) * (gCurPacket->y[3] - gCurPacket->y[0]) > 0)
                        continue;
                    if (part == 0) {
                        gCurPacket->u[0] = face->u[0];
                        gCurPacket->v[0] = face->v[0];
                        gCurPacket->u[1] = (face->u[0] + face->u[1]) >> 1;
                        gCurPacket->v[1] = (face->v[0] + face->v[1]) >> 1;
                        gCurPacket->u[2] = (face->u[1] + face->u[3]) >> 1;
                        gCurPacket->v[2] = (face->v[1] + face->v[3]) >> 1;
                        gCurPacket->u[3] = (face->u[0] + face->u[3]) >> 1;
                        gCurPacket->v[3] = (face->v[0] + face->v[3]) >> 1;
                    } else if (part == 1) {
                        gCurPacket->u[0] = (face->u[0] + face->u[1]) >> 1;
                        gCurPacket->v[0] = (face->v[0] + face->v[1]) >> 1;
                        gCurPacket->u[1] = face->u[1];
                        gCurPacket->v[1] = face->v[1];
                        gCurPacket->u[2] = (face->u[1] + face->u[2]) >> 1;
                        gCurPacket->v[2] = (face->v[1] + face->v[2]) >> 1;
                        gCurPacket->u[3] = (face->u[1] + face->u[3]) >> 1;
                        gCurPacket->v[3] = (face->v[1] + face->v[3]) >> 1;
                    } else if (part == 2) {
                        gCurPacket->u[0] = (face->u[1] + face->u[3]) >> 1;
                        gCurPacket->v[0] = (face->v[1] + face->v[3]) >> 1;
                        gCurPacket->u[1] = (face->u[1] + face->u[2]) >> 1;
                        gCurPacket->v[1] = (face->v[1] + face->v[2]) >> 1;
                        gCurPacket->u[2] = face->u[2];
                        gCurPacket->v[2] = face->v[2];
                        gCurPacket->u[3] = (face->u[2] + face->u[3]) >> 1;
                        gCurPacket->v[3] = (face->v[2] + face->v[3]) >> 1;
                    } else if (part == 3) {
                        gCurPacket->u[0] = (face->u[0] + face->u[3]) >> 1;
                        gCurPacket->v[0] = (face->v[0] + face->v[3]) >> 1;
                        gCurPacket->u[1] = (face->u[1] + face->u[3]) >> 1;
                        gCurPacket->v[1] = (face->v[1] + face->v[3]) >> 1;
                        gCurPacket->u[2] = (face->u[2] + face->u[3]) >> 1;
                        gCurPacket->v[2] = (face->v[2] + face->v[3]) >> 1;
                        gCurPacket->u[3] = face->u[3];
                        gCurPacket->v[3] = face->v[3];
                    }
                    z = depth[0] + depth[3]; z += depth[2] + depth[1]; z = (z >> 7) + 32;
                    gCurPacket->tex = face->tex;
                    gCurPacket->mode = 0;
                    if (z < 0) z = 0;
                    z = z > 255 ? 255 : z;
                    if (face->kind == 2) gCurPacket->mode = 1;
                    if (face->kind == 4) gCurPacket->mode = 2;
                    if (gBuckets[z] == 0) {
                        Packet *p = gCurPacket;
                        p->next = 0;
                        gCurPacket++;
                        gBuckets[z] = p;
                    } else {
                        Packet *p = gCurPacket;
                        p->next = gBuckets[z];
                        gCurPacket++;
                        gBuckets[z] = p;
                    }
                }
            } else {
                gCurPacket->x[0] = pts[a].sx;
                gCurPacket->y[0] = pts[a].sy;
                gCurPacket->x[1] = pts[b].sx;
                gCurPacket->y[1] = pts[b].sy;
                gCurPacket->x[2] = pts[c].sx;
                gCurPacket->y[2] = pts[c].sy;
                gCurPacket->x[3] = pts[d].sx;
                gCurPacket->y[3] = pts[d].sy;
                if ((gCurPacket->x[0] >= 0 && gCurPacket->x[0] < 120 && gCurPacket->y[0] >= 0 && gCurPacket->y[0] < 160)
                 || (gCurPacket->x[1] >= 0 && gCurPacket->x[1] < 120 && gCurPacket->y[1] >= 0 && gCurPacket->y[1] < 160)
                 || (gCurPacket->x[2] >= 0 && gCurPacket->x[2] < 120 && gCurPacket->y[2] >= 0 && gCurPacket->y[2] < 160)
                 || (gCurPacket->x[3] >= 0 && gCurPacket->x[3] < 120 && gCurPacket->y[3] >= 0 && gCurPacket->y[3] < 160)) {
                    if ((gCurPacket->x[3] - gCurPacket->x[0]) * (gCurPacket->y[1] - gCurPacket->y[0])
                      - (gCurPacket->x[1] - gCurPacket->x[0]) * (gCurPacket->y[3] - gCurPacket->y[0]) <= 0) {
                        if (face->kind == 3) {
                            s32 n = g_03000DE0;
                            g_03000AD0[n].active = 1;
                            g_03000AD0[n].x = pts[b].sx + pts[a].sx;
                            g_03000AD0[n].y = (pts[c].sy + pts[a].sy) >> 1;
                            g_03000AD0[n].w = (pts[b].sx - pts[a].sx) << 1;
                            g_03000DE0 = n + 1;
                        }
                        if (gCurPacket->x[0] <= -67) gCurPacket->x[0] = -66;
                        if (gCurPacket->x[1] <= -67) gCurPacket->x[1] = -66;
                        if (gCurPacket->x[2] <= -67) gCurPacket->x[2] = -66;
                        if (gCurPacket->x[3] <= -67) gCurPacket->x[3] = -66;
                        if (gCurPacket->x[0] > 186) gCurPacket->x[0] = 186;
                        if (gCurPacket->x[1] > 186) gCurPacket->x[1] = 186;
                        if (gCurPacket->x[2] > 186) gCurPacket->x[2] = 186;
                        if (gCurPacket->x[3] > 186) gCurPacket->x[3] = 186;
                        gCurPacket->u[0] = face->u[0];
                        gCurPacket->v[0] = face->v[0];
                        gCurPacket->u[1] = face->u[1];
                        gCurPacket->v[1] = face->v[1];
                        gCurPacket->u[2] = face->u[2];
                        gCurPacket->v[2] = face->v[2];
                        gCurPacket->u[3] = face->u[3];
                        gCurPacket->v[3] = face->v[3];
                        z = depth[0] + depth[3]; z += depth[2] + depth[1]; z = (z >> 7) + 32;
                        gCurPacket->tex = face->tex;
                        gCurPacket->mode = 0;
                        if (z < 0) z = 0;
                        z = z > 255 ? 255 : z;
                        if (face->kind == 2) gCurPacket->mode = 1;
                        if (face->kind == 4) gCurPacket->mode = 2;
                        if (gBuckets[z] == 0) {
                            Packet *p = gCurPacket;
                            p->next = 0;
                            gCurPacket++;
                            gBuckets[z] = p;
                        } else {
                            Packet *p = gCurPacket;
                            p->next = gBuckets[z];
                            gCurPacket++;
                            gBuckets[z] = p;
                        }
                    }
                }
            }
        }
        ring = (ring + 1) & 31;
    } while (ring != end);
}
