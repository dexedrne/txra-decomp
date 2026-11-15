/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Road stream owner 08002854..0800418C. The mapped entry 08003786 is an internal
 * label: the second pass of the two-column scenery loop, reached by the far BL
 * goto at 0800416A, so it is covered by this body.
 * Written after the original statement order: faces addressed as base[faces],
 * a point cursor plus per-row counters, explicit window setup in both directions.
 * `following` and `ahead` are built in place in their own (stack) variables: the
 * reload register picked for `following = ring + 1` advances reload's round-robin,
 * and `ahead = ring + 2` reuses ring's dying register, as in the original. */
typedef struct {
    s32 x, y, z;
    u16 angle;
    u8 road[3], wall_left, unused_12, wall_right, bank_left, bank_right;
    u8 bridge, scenery[2], unused_19[3];
} StreamRow;
typedef struct {
    s32 x, y, z, active, screen_x, screen_y, depth;
} StreamPoint;
typedef struct {
    u16 kind, reserved;
    s32 index[4], u[4], v[4];
    u16 texture, untouched;
} StreamFace;
extern s32 g_03002334, g_03005F50, g_03002E4C, g_030001B8, g_03005F48;
extern StreamPoint g_02014000[];
extern StreamFace g_02033B70[];
extern s32 g_080219AC[][4], g_08021520[][3], g_0802158C[][3], g_080215F8[][3];
extern s32 g_08021718[][5];
extern void func_08005DD4(TxraTriple *, TxraTriple *, s32, u32);
extern void func_08005F48(TxraTriple *, TxraTriple *, s32, u32, s32);

#define ROWS ((StreamRow *)g_03006874)
#define R(i) ((TxraTriple *)&ROWS[i])
#define DONE p->active = 1; p++

void func_08002854(void)
{
    s32 i, previous, previous2, center, next, next2;
    s32 faces;
    StreamFace *fb;
    s32 angle, first, following, ahead;
    s32 fcount, acount, right_start, b0, b1, b2;
    s32 left_start, unused_next;
    s32 count, ring;
    StreamPoint *p;

    if (g_03002334 == 0) {
        center = g_03005F50 + 28;
        if (center >= g_03002E4C) center -= g_03002E4C;
        next = center + 1;
        if (next >= g_03002E4C) next = 0;
        next2 = next + 1;
        if (next2 >= g_03002E4C) next2 = 0;
        previous2 = center - 2;
        if (previous2 < 0) previous2 += g_03002E4C;
        previous = center - 1;
        if (previous < 0) previous += g_03002E4C;
        ring = g_030001B8;
    } else {
        center = g_03005F50 - 1;
        if (center < 0) center += g_03002E4C;
        next = center + 1;
        if (next >= g_03002E4C) next = 0;
        next2 = next + 1;
        if (next2 >= g_03002E4C) next2 = 0;
        previous2 = center - 2;
        if (previous2 < 0) previous2 += g_03002E4C;
        previous = center - 1;
        if (previous < 0) previous += g_03002E4C;
        ring = (g_030001B8 - 29) & 31;
    }
    fb = &((StreamFace *)0x02033B70)[(ring & 31) * 24];
    first = (ring & 31) * 24;
    following = (ring + 1) & 31;
    following *= 24;
    ahead = (ring + 2) & 31;
    ahead *= 24;
    p = &((StreamPoint *)0x02014000)[first];
    if (g_03002334 == 0) {
        for (i = 0; i < 24; i++) {
            p[i].active = 0;
            fb[i].kind = 0;
        }
    } else {
        for (i = 0; i < 24; i++) {
            p[i].active = 0;
            fb[i].kind = 0;
        }
    }
    angle = ROWS[center].angle;
    unused_next = ROWS[next2].bank_left;
    faces = 0;
    count = 0;
    fcount = 0;
    acount = 0;

    if ((center & 1) == 0) {
        if (ROWS[center].bank_left) {
            func_08005F48(R(center), (TxraTriple *)p, 2560, angle + 0x1000, 0);
            fb[faces].index[3] = first + count;
            fb[faces].index[2] = ahead + acount;
            DONE; count++; acount++;
            func_08005F48(R(center), (TxraTriple *)p, 2560, angle + 0x1000, g_080219AC[ROWS[center].bank_left][2]);
            fb[faces].index[0] = first + count;
            fb[faces].index[1] = ahead + acount;
            DONE; count++; acount++;
            fb[faces].kind = 1;
            fb[faces].reserved = 0;
            fb[faces].texture = g_080219AC[ROWS[center].bank_left][3];
            fb[faces].u[0] = g_080219AC[ROWS[center].bank_left][0];
            fb[faces].v[0] = g_080219AC[ROWS[center].bank_left][1];
            fb[faces].u[1] = g_080219AC[ROWS[center].bank_left][0] + 31;
            fb[faces].v[1] = g_080219AC[ROWS[center].bank_left][1];
            fb[faces].u[2] = g_080219AC[ROWS[center].bank_left][0] + 31;
            fb[faces].v[2] = g_080219AC[ROWS[center].bank_left][1] + 63;
            fb[faces].u[3] = g_080219AC[ROWS[center].bank_left][0];
            fb[faces].v[3] = g_080219AC[ROWS[center].bank_left][1] + 63;
            faces++;
            if (ROWS[previous2].bank_left == 0) {
                func_08005F48(R(center), (TxraTriple *)p, 3840, angle + 0x1000, 0);
                DONE;
                func_08005F48(R(center), (TxraTriple *)p, 3840, angle + 0x1000, g_080219AC[ROWS[center].bank_left][2]);
                DONE;
                count += 2;
                fb[faces].index[0] = first + 3;
                fb[faces].index[1] = first + 1;
                fb[faces].index[2] = first;
                fb[faces].index[3] = first + 2;
                fb[faces].kind = 1;
                fb[faces].reserved = 0;
                fb[faces].texture = g_080219AC[ROWS[center].bank_left][3];
                fb[faces].u[0] = g_080219AC[ROWS[center].bank_left][0] + 32;
                fb[faces].v[0] = g_080219AC[ROWS[center].bank_left][1];
                fb[faces].u[1] = g_080219AC[ROWS[center].bank_left][0] + 63;
                fb[faces].v[1] = g_080219AC[ROWS[center].bank_left][1];
                fb[faces].u[2] = g_080219AC[ROWS[center].bank_left][0] + 63;
                fb[faces].v[2] = g_080219AC[ROWS[center].bank_left][1] + 63;
                fb[faces].u[3] = g_080219AC[ROWS[center].bank_left][0] + 32;
                fb[faces].v[3] = g_080219AC[ROWS[center].bank_left][1] + 63;
                faces++;
            }
        } else {
            if (ROWS[previous2].bank_left) {
                func_08005F48(R(center), (TxraTriple *)p, 2560, angle + 0x1000, 0);
                DONE; count++;
                left_start = count - 1;
                func_08005F48(R(center), (TxraTriple *)p, 2560, angle + 0x1000, g_080219AC[ROWS[previous2].bank_left][2]);
                DONE; count++;
            }
            if (ROWS[next2].bank_left) acount = 4;
        }
        if (ROWS[center].bank_right) {
            func_08005F48(R(center), (TxraTriple *)p, 2560, angle - 0x1000, 0);
            fb[faces].index[2] = first + count;
            fb[faces].index[3] = ahead + acount;
            count++; acount++;
            DONE;
            func_08005F48(R(center), (TxraTriple *)p, 2560, angle - 0x1000, g_080219AC[ROWS[center].bank_right][2]);
            fb[faces].index[1] = first + count;
            fb[faces].index[0] = ahead + acount;
            DONE; count++;
            fb[faces].kind = 1;
            fb[faces].reserved = 0;
            fb[faces].texture = g_080219AC[ROWS[center].bank_right][3];
            fb[faces].u[0] = g_080219AC[ROWS[center].bank_right][0];
            fb[faces].v[0] = g_080219AC[ROWS[center].bank_right][1];
            fb[faces].u[1] = g_080219AC[ROWS[center].bank_right][0] + 31;
            fb[faces].v[1] = g_080219AC[ROWS[center].bank_right][1];
            fb[faces].u[2] = g_080219AC[ROWS[center].bank_right][0] + 31;
            fb[faces].v[2] = g_080219AC[ROWS[center].bank_right][1] + 63;
            fb[faces].u[3] = g_080219AC[ROWS[center].bank_right][0];
            fb[faces].v[3] = g_080219AC[ROWS[center].bank_right][1] + 63;
            faces++;
            if (ROWS[previous2].bank_right == 0) {
                func_08005F48(R(center), (TxraTriple *)p, 3840, angle - 0x1000, 0);
                DONE;
                func_08005F48(R(center), (TxraTriple *)p, 3840, angle - 0x1000, g_080219AC[ROWS[center].bank_right][2]);
                DONE;
                fb[faces].index[0] = first + count - 1;
                fb[faces].index[1] = first + count + 1;
                fb[faces].index[2] = first + count;
                fb[faces].index[3] = first + count - 2;
                count += 2;
                fb[faces].kind = 1;
                fb[faces].reserved = 0;
                fb[faces].texture = g_080219AC[ROWS[center].bank_right][3];
                fb[faces].u[0] = g_080219AC[ROWS[center].bank_right][0] + 32;
                fb[faces].v[0] = g_080219AC[ROWS[center].bank_right][1];
                fb[faces].u[1] = g_080219AC[ROWS[center].bank_right][0] + 63;
                fb[faces].v[1] = g_080219AC[ROWS[center].bank_right][1];
                fb[faces].u[2] = g_080219AC[ROWS[center].bank_right][0] + 63;
                fb[faces].v[2] = g_080219AC[ROWS[center].bank_right][1] + 63;
                fb[faces].u[3] = g_080219AC[ROWS[center].bank_right][0] + 32;
                fb[faces].v[3] = g_080219AC[ROWS[center].bank_right][1] + 63;
                faces++;
            }
        } else {
            if (ROWS[previous2].bank_right) {
                func_08005F48(R(center), (TxraTriple *)p, 2560, angle - 0x1000, 0);
                DONE; count++;
                right_start = count - 1;
                func_08005F48(R(center), (TxraTriple *)p, 2560, angle - 0x1000, g_080219AC[ROWS[previous2].bank_right][2]);
                DONE; count++;
                if (ROWS[next2].bank_right) acount += 4;
            }
        }
    }
    if (center & 1) {
        if (ROWS[next].bank_left) {
            if (ROWS[previous].bank_left == 0) fcount += 4;
            else fcount += 2;
        } else if (ROWS[previous].bank_left) fcount += 2;
        if (ROWS[next].bank_right) {
            if (ROWS[previous].bank_right == 0) fcount += 4;
            else fcount += 2;
        } else if (ROWS[previous].bank_right) fcount += 2;
    }
    /* three road strips */
    func_08005DD4(R(center), (TxraTriple *)p, 960, angle + 0x1000);
    fb[faces].index[3] = first + count;
    fb[faces].index[0] = following + fcount;
    DONE;
    fb[faces + 3].index[2] = following + fcount;
    fb[faces + 3].index[3] = first + count;
    count++; fcount++;
    func_08005DD4(R(center), (TxraTriple *)p, 320, angle + 0x1000);
    fb[faces].index[2] = first + count;
    fb[faces].index[1] = following + fcount;
    fb[faces].u[0] = g_08021520[ROWS[center].road[0]][0];
    fb[faces].v[0] = g_08021520[ROWS[center].road[0]][1];
    fb[faces].u[1] = g_08021520[ROWS[center].road[0]][0] + 31;
    fb[faces].v[1] = g_08021520[ROWS[center].road[0]][1];
    fb[faces].u[2] = g_08021520[ROWS[center].road[0]][0] + 31;
    fb[faces].v[2] = g_08021520[ROWS[center].road[0]][1] + 31;
    fb[faces].u[3] = g_08021520[ROWS[center].road[0]][0];
    fb[faces].v[3] = g_08021520[ROWS[center].road[0]][1] + 31;
    fb[faces].texture = g_08021520[ROWS[center].road[0]][2];
    fb[faces].reserved = 0;
    fb[faces].kind = 1;
    faces++;
    fb[faces].index[3] = first + count;
    fb[faces].index[0] = following + fcount;
    DONE; count++; fcount++;
    func_08005DD4(R(center), (TxraTriple *)p, 320, angle - 0x1000);
    fb[faces].index[2] = first + count;
    fb[faces].index[1] = following + fcount;
    fb[faces].u[0] = g_0802158C[ROWS[center].road[1]][0];
    fb[faces].v[0] = g_0802158C[ROWS[center].road[1]][1];
    fb[faces].u[1] = g_0802158C[ROWS[center].road[1]][0] + 31;
    fb[faces].v[1] = g_0802158C[ROWS[center].road[1]][1];
    fb[faces].u[2] = g_0802158C[ROWS[center].road[1]][0] + 31;
    fb[faces].v[2] = g_0802158C[ROWS[center].road[1]][1] + 31;
    fb[faces].u[3] = g_0802158C[ROWS[center].road[1]][0];
    fb[faces].v[3] = g_0802158C[ROWS[center].road[1]][1] + 31;
    fb[faces].texture = g_0802158C[ROWS[center].road[1]][2];
    fb[faces].reserved = 0;
    fb[faces].kind = 1;
    faces++;
    fb[faces].index[3] = first + count;
    fb[faces].index[0] = following + fcount;
    DONE; count++; fcount++;
    func_08005DD4(R(center), (TxraTriple *)p, 960, angle - 0x1000);
    fb[faces].index[2] = first + count;
    fb[faces].index[1] = following + fcount;
    DONE; count++; fcount++;
    fb[faces].u[0] = g_080215F8[ROWS[center].road[2]][0];
    fb[faces].v[0] = g_080215F8[ROWS[center].road[2]][1];
    fb[faces].u[1] = g_080215F8[ROWS[center].road[2]][0] + 31;
    fb[faces].v[1] = g_080215F8[ROWS[center].road[2]][1];
    fb[faces].u[2] = g_080215F8[ROWS[center].road[2]][0] + 31;
    fb[faces].v[2] = g_080215F8[ROWS[center].road[2]][1] + 31;
    fb[faces].u[3] = g_080215F8[ROWS[center].road[2]][0];
    fb[faces].v[3] = g_080215F8[ROWS[center].road[2]][1] + 31;
    fb[faces].texture = g_080215F8[ROWS[center].road[2]][2];
    fb[faces].reserved = 0;
    fb[faces].kind = 1;
    faces++;
    fb[faces + 1].index[2] = first + count - 1;
    fb[faces + 1].index[3] = following + fcount - 1;
    /* left wall */
    if (ROWS[center].wall_left != ROWS[previous].wall_left) {
        func_08005F48(R(center), (TxraTriple *)p, 960, angle + 0x1000, g_08021718[ROWS[previous].wall_left][3]);
        DONE; count++;
    }
    func_08005F48(R(center), (TxraTriple *)p, 960, angle + 0x1000, g_08021718[ROWS[center].wall_left][3]);
    fb[faces].index[0] = first + count;
    fb[faces].index[1] = following + fcount;
    DONE;
    fb[faces].kind = 1;
    fb[faces].reserved = 0;
    fb[faces].texture = g_08021718[ROWS[center].wall_left][4];
    count++; fcount++;
    fb[faces].u[0] = g_08021718[ROWS[center].wall_left][0];
    fb[faces].v[0] = g_08021718[ROWS[center].wall_left][1];
    fb[faces].u[1] = g_08021718[ROWS[center].wall_left][0] + 31;
    fb[faces].v[1] = g_08021718[ROWS[center].wall_left][1];
    fb[faces].u[2] = g_08021718[ROWS[center].wall_left][0] + 31;
    fb[faces].v[2] = g_08021718[ROWS[center].wall_left][1] + g_08021718[ROWS[center].wall_left][2] - 1;
    fb[faces].u[3] = g_08021718[ROWS[center].wall_left][0];
    fb[faces].v[3] = g_08021718[ROWS[center].wall_left][1] + g_08021718[ROWS[center].wall_left][2] - 1;
    faces++;
    if (ROWS[next].wall_left != ROWS[center].wall_left) fcount++;
    /* right wall */
    if (ROWS[center].wall_right != ROWS[previous].wall_right) {
        func_08005F48(R(center), (TxraTriple *)p, 960, angle - 0x1000, g_08021718[ROWS[previous].wall_right][3]);
        DONE; count++;
    }
    func_08005F48(R(center), (TxraTriple *)p, 960, angle - 0x1000, g_08021718[ROWS[center].wall_right][3]);
    fb[faces].index[0] = following + fcount;
    fb[faces].index[1] = first + count;
    DONE;
    fb[faces].kind = 1;
    fb[faces].reserved = 0;
    fb[faces].texture = g_08021718[ROWS[center].wall_right][4];
    count++; fcount++;
    fb[faces].u[0] = g_08021718[ROWS[center].wall_right][0];
    fb[faces].v[0] = g_08021718[ROWS[center].wall_right][1];
    fb[faces].u[1] = g_08021718[ROWS[center].wall_right][0] + 31;
    fb[faces].v[1] = g_08021718[ROWS[center].wall_right][1];
    fb[faces].u[2] = g_08021718[ROWS[center].wall_right][0] + 31;
    fb[faces].v[2] = g_08021718[ROWS[center].wall_right][1] + g_08021718[ROWS[center].wall_right][2] - 1;
    fb[faces].u[3] = g_08021718[ROWS[center].wall_right][0];
    fb[faces].v[3] = g_08021718[ROWS[center].wall_right][1] + g_08021718[ROWS[center].wall_right][2] - 1;
    faces++;
    if (ROWS[next].wall_right != ROWS[center].wall_right) fcount++;
    /* bridge panels */
    if (ROWS[center].bridge) {
        func_08005F48(R(center), (TxraTriple *)p, 960, angle + 0x1000, -600);
        fb[faces].index[0] = first + count;
        b0 = count;
        fb[faces].index[3] = following + fcount;
        DONE; count++; fcount++;
        func_08005F48(R(center), (TxraTriple *)p, 0, angle + 0x1000, -600);
        fb[faces].index[1] = first + count;
        b1 = count;
        fb[faces].index[2] = following + fcount;
        fb[faces].u[0] = 0;
        fb[faces].v[0] = 128;
        fb[faces].u[1] = 15;
        fb[faces].v[1] = 128;
        fb[faces].u[2] = 15;
        fb[faces].v[2] = 159;
        fb[faces].u[3] = 0;
        fb[faces].v[3] = 159;
        fb[faces].texture = g_03005F48;
        fb[faces].reserved = 0;
        fb[faces].kind = 4;
        faces++;
        fb[faces].index[0] = first + count;
        fb[faces].index[3] = following + fcount;
        DONE; count++; fcount++;
        func_08005F48(R(center), (TxraTriple *)p, 960, angle - 0x1000, -600);
        fb[faces].index[1] = first + count;
        b2 = count;
        fb[faces].index[2] = following + fcount;
        DONE; count++;
        fb[faces].u[0] = 16;
        fb[faces].v[0] = 128;
        fb[faces].u[1] = 31;
        fb[faces].v[1] = 128;
        fb[faces].u[2] = 31;
        fb[faces].v[2] = 159;
        fb[faces].u[3] = 16;
        fb[faces].v[3] = 159;
        fb[faces].texture = g_03005F48;
        fb[faces].reserved = 0;
        fb[faces].kind = 4;
        faces++;
    } else if (ROWS[previous].bridge) {
        func_08005F48(R(center), (TxraTriple *)p, 960, angle + 0x1000, -600);
        DONE; count++;
        func_08005F48(R(center), (TxraTriple *)p, 0, angle + 0x1000, -600);
        DONE; count++;
        func_08005F48(R(center), (TxraTriple *)p, 960, angle - 0x1000, -600);
        DONE; count++;
    }
    /* two scenery columns */
    for (i = 0; i < 2; i++) {
        if ((u8)(ROWS[center].scenery[i] - 3) <= 8) {
            fb[faces].index[3] = first + left_start;
            func_08005DD4(R(center), (TxraTriple *)p, 960, angle + 0x1000);
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 2560, angle + 0x1000, -800);
            fb[faces].index[0] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 960, angle + 0x1000, -800);
            fb[faces].index[1] = first + count;
            DONE; count++;
            fb[faces].u[0] = 48; fb[faces].v[0] = 128; fb[faces].u[1] = 63; fb[faces].v[1] = 128;
            fb[faces].u[2] = 63; fb[faces].v[2] = 191; fb[faces].u[3] = 48; fb[faces].v[3] = 191;
            fb[faces].texture = 2; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
            fb[faces].index[0] = first + count - 1;
            func_08005F48(R(center), (TxraTriple *)p, 0, angle - 0x1000, -800);
            fb[faces].index[1] = first + count;
            DONE; count++;
            fb[faces].index[3] = first + b0;
            fb[faces].index[2] = first + b1;
            fb[faces].u[0] = 32; fb[faces].v[0] = 128; fb[faces].u[1] = 47; fb[faces].v[1] = 128;
            fb[faces].u[2] = 47; fb[faces].v[2] = 145; fb[faces].u[3] = 32; fb[faces].v[3] = 145;
            fb[faces].texture = 2; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
            fb[faces].index[0] = first + count - 1;
            fb[faces].index[3] = first + b1;
            fb[faces].index[2] = first + b2;
            func_08005F48(R(center), (TxraTriple *)p, 960, angle - 0x1000, -800);
            fb[faces].index[1] = first + count;
            DONE; count++;
            fb[faces].u[0] = 48; fb[faces].v[0] = 128; fb[faces].u[1] = 63; fb[faces].v[1] = 128;
            fb[faces].u[2] = 63; fb[faces].v[2] = 145; fb[faces].u[3] = 48; fb[faces].v[3] = 145;
            fb[faces].texture = 2; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
            fb[faces].index[0] = first + count - 1;
            func_08005F48(R(center), (TxraTriple *)p, 2560, angle - 0x1000, -800);
            fb[faces].index[1] = first + count;
            DONE; count++;
            fb[faces].index[2] = first + right_start;
            func_08005DD4(R(center), (TxraTriple *)p, 960, angle - 0x1000);
            fb[faces].index[3] = first + count;
            DONE; count++;
            fb[faces].u[0] = 32; fb[faces].v[0] = 128; fb[faces].u[1] = 47; fb[faces].v[1] = 128;
            fb[faces].u[2] = 47; fb[faces].v[2] = 191; fb[faces].u[3] = 32; fb[faces].v[3] = 191;
            fb[faces].texture = 2; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
        }
        if (ROWS[center].scenery[i] == 12 || ROWS[center].scenery[i] == 14) {
            func_08005DD4(R(center), (TxraTriple *)p, 1920, angle + 0x1000);
            fb[faces].index[3] = first + count;
            DONE; count++;
            func_08005DD4(R(center), (TxraTriple *)p, 1280, angle + 0x1000);
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1920, angle + 0x1000, -600);
            fb[faces].index[0] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1280, angle + 0x1000, -600);
            fb[faces].index[1] = first + count;
            DONE; count++;
            if (ROWS[center].scenery[i] == 11) {
                fb[faces].u[0] = 0; fb[faces].v[0] = 192; fb[faces].u[1] = 31; fb[faces].v[1] = 192;
                fb[faces].u[2] = 31; fb[faces].v[2] = 255; fb[faces].u[3] = 0; fb[faces].v[3] = 255;
            } else {
                fb[faces].u[0] = 32; fb[faces].v[0] = 192; fb[faces].u[1] = 63; fb[faces].v[1] = 192;
                fb[faces].u[2] = 63; fb[faces].v[2] = 255; fb[faces].u[3] = 32; fb[faces].v[3] = 255;
            }
            fb[faces].texture = 1; fb[faces].reserved = 0; fb[faces].kind = 2;
            faces++;
        }
        if (ROWS[center].scenery[i] == 13 || ROWS[center].scenery[i] == 15) {
            func_08005DD4(R(center), (TxraTriple *)p, 1920, angle - 0x1000);
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005DD4(R(center), (TxraTriple *)p, 1280, angle - 0x1000);
            fb[faces].index[3] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1920, angle - 0x1000, -600);
            fb[faces].index[1] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1280, angle - 0x1000, -600);
            fb[faces].index[0] = first + count;
            DONE; count++;
            if (ROWS[center].scenery[i] == 12) {
                fb[faces].u[0] = 0; fb[faces].v[0] = 192; fb[faces].u[1] = 31; fb[faces].v[1] = 192;
                fb[faces].u[2] = 31; fb[faces].v[2] = 255; fb[faces].u[3] = 0; fb[faces].v[3] = 255;
            } else {
                fb[faces].u[0] = 32; fb[faces].v[0] = 192; fb[faces].u[1] = 63; fb[faces].v[1] = 192;
                fb[faces].u[2] = 63; fb[faces].v[2] = 255; fb[faces].u[3] = 32; fb[faces].v[3] = 255;
            }
            fb[faces].texture = 1; fb[faces].reserved = 0; fb[faces].kind = 2;
            faces++;
        }
        if (ROWS[center].scenery[i] == 1) {
            func_08005DD4(R(center), (TxraTriple *)p, 1280, angle + 0x1000);
            fb[faces].index[3] = first + count;
            DONE; count++;
            func_08005DD4(R(center), (TxraTriple *)p, 1232, angle + 0x1000);
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1280, angle + 0x1000, -750);
            fb[faces].index[0] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1216, angle + 0x1000, -750);
            fb[faces].index[1] = first + count;
            DONE; count++;
            fb[faces].u[0] = 0; fb[faces].v[0] = 2; fb[faces].u[1] = 3; fb[faces].v[1] = 2;
            fb[faces].u[2] = 3; fb[faces].v[2] = 61; fb[faces].u[3] = 0; fb[faces].v[3] = 61;
            fb[faces].texture = 8; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
            func_08005F48(R(center), (TxraTriple *)p, 1240, angle + 0x1000, -740);
            fb[faces].index[3] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1120, angle + 0x1000, -740);
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1240, angle + 0x1000, -800);
            fb[faces].index[0] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1120, angle + 0x1000, -800);
            fb[faces].index[1] = first + count;
            DONE; count++;
            fb[faces].u[0] = 4; fb[faces].v[0] = 0; fb[faces].u[1] = 11; fb[faces].v[1] = 0;
            fb[faces].u[2] = 11; fb[faces].v[2] = 7; fb[faces].u[3] = 4; fb[faces].v[3] = 7;
            fb[faces].texture = 8; fb[faces].reserved = 0; fb[faces].kind = 3;
            faces++;
        }
        if (ROWS[center].scenery[i] == 2) {
            func_08005DD4(R(center), (TxraTriple *)p, 1280, angle - 0x1000);
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005DD4(R(center), (TxraTriple *)p, 1232, angle - 0x1000);
            fb[faces].index[3] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1280, angle - 0x1000, -750);
            fb[faces].index[1] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1216, angle - 0x1000, -750);
            fb[faces].index[0] = first + count;
            DONE; count++;
            fb[faces].u[0] = 20; fb[faces].v[0] = 2; fb[faces].u[1] = 23; fb[faces].v[1] = 2;
            fb[faces].u[2] = 23; fb[faces].v[2] = 61; fb[faces].u[3] = 20; fb[faces].v[3] = 61;
            fb[faces].texture = 8; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
            func_08005F48(R(center), (TxraTriple *)p, 1240, angle - 0x1000, -740);
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1120, angle - 0x1000, -740);
            fb[faces].index[3] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1240, angle - 0x1000, -800);
            fb[faces].index[1] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1120, angle - 0x1000, -800);
            fb[faces].index[0] = first + count;
            DONE; count++;
            fb[faces].u[0] = 12; fb[faces].v[0] = 0; fb[faces].u[1] = 19; fb[faces].v[1] = 0;
            fb[faces].u[2] = 19; fb[faces].v[2] = 7; fb[faces].u[3] = 12; fb[faces].v[3] = 7;
            fb[faces].texture = 8; fb[faces].reserved = 0; fb[faces].kind = 3;
            faces++;
        }
        if ((u8)(ROWS[center].scenery[i] - 16) <= 3) {
            func_08005DD4(R(center), (TxraTriple *)p, 1280, angle + 0x1000);
            fb[faces].index[3] = first + count;
            DONE; count++;
            func_08005DD4(R(center), (TxraTriple *)p, 1248, angle + 0x1000);
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1280, angle + 0x1000, -600);
            fb[faces].index[0] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1248, angle + 0x1000, -600);
            fb[faces].index[1] = first + count;
            DONE; count++;
            fb[faces].u[0] = 0; fb[faces].v[0] = 192; fb[faces].u[1] = 2; fb[faces].v[1] = 192;
            fb[faces].u[2] = 2; fb[faces].v[2] = 255; fb[faces].u[3] = 0; fb[faces].v[3] = 255;
            fb[faces].texture = 2; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
            func_08005DD4(R(center), (TxraTriple *)p, 1280, angle - 0x1000);
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005DD4(R(center), (TxraTriple *)p, 1248, angle - 0x1000);
            fb[faces].index[3] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1280, angle - 0x1000, -600);
            fb[faces].index[1] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1248, angle - 0x1000, -600);
            fb[faces].index[0] = first + count;
            DONE; count++;
            fb[faces].u[0] = 3; fb[faces].v[0] = 192; fb[faces].u[1] = 5; fb[faces].v[1] = 192;
            fb[faces].u[2] = 5; fb[faces].v[2] = 255; fb[faces].u[3] = 3; fb[faces].v[3] = 255;
            fb[faces].texture = 2; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
            fb[faces].index[3] = first + count - 6;
            func_08005F48(R(center), (TxraTriple *)p, 392, angle + 0x1000, -600);
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1248, angle + 0x1000, -1000);
            fb[faces].index[0] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 392, angle + 0x1000, -1000);
            fb[faces].index[1] = first + count;
            DONE; count++;
            fb[faces].u[0] = 64; fb[faces].v[0] = 192; fb[faces].u[1] = 95; fb[faces].v[1] = 192;
            fb[faces].u[2] = 95; fb[faces].v[2] = 223; fb[faces].u[3] = 64; fb[faces].v[3] = 223;
            fb[faces].texture = 2; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
            func_08005F48(R(center), (TxraTriple *)p, 392, angle - 0x1000, -600);
            fb[faces].index[3] = first + count - 3;
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 392, angle - 0x1000, -1000);
            fb[faces].index[0] = first + count - 2;
            fb[faces].index[1] = first + count;
            DONE; count++;
            fb[faces].u[0] = 64; fb[faces].v[0] = 192; fb[faces].u[1] = 95; fb[faces].v[1] = 192;
            fb[faces].u[2] = 95; fb[faces].v[2] = 223; fb[faces].u[3] = 64; fb[faces].v[3] = 223;
            fb[faces].texture = 2; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
            func_08005F48(R(center), (TxraTriple *)p, 1280, angle - 0x1000, -600);
            fb[faces].index[3] = first + count - 2;
            fb[faces].index[2] = first + count;
            DONE; count++;
            func_08005F48(R(center), (TxraTriple *)p, 1280, angle - 0x1000, -1000);
            fb[faces].index[0] = first + count - 2;
            fb[faces].index[1] = first + count;
            DONE; count++;
            fb[faces].u[0] = 64; fb[faces].v[0] = 192; fb[faces].u[1] = 95; fb[faces].v[1] = 192;
            fb[faces].u[2] = 95; fb[faces].v[2] = 223; fb[faces].u[3] = 64; fb[faces].v[3] = 223;
            fb[faces].texture = 2; fb[faces].reserved = 0; fb[faces].kind = 1;
            faces++;
        }
    }
}

#undef ROWS
#undef R
#undef DONE
