/* Complete streaming hypothesis, including the internal 08003786 loop.
 * Uninstalled. Helper order and final memory require original-state checks.
 * Cartesian triples are in the game's existing coordinate frame. */
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

#define ROW(i) (&((StreamRow *)g_03006874)[(i)])
#define D(radius, heading) do { \
    func_08005DD4((TxraTriple *)ROW(center), (TxraTriple *)(point+emitted), radius, heading); \
    point[emitted].active = 1; ++emitted; \
} while (0)
#define P(radius, heading, elevation) do { \
    func_08005F48((TxraTriple *)ROW(center), (TxraTriple *)(point+emitted), radius, heading, elevation); \
    point[emitted].active = 1; ++emitted; \
} while (0)
#define INDICES(a,b,c,d) do { face->index[0]=(a); face->index[1]=(b); \
    face->index[2]=(c); face->index[3]=(d); } while (0)
#define RECT(u0,v0,u1,v1) do { \
    face->u[0]=(u0); face->v[0]=(v0); face->u[1]=(u1); face->v[1]=(v0); \
    face->u[2]=(u1); face->v[2]=(v1); face->u[3]=(u0); face->v[3]=(v1); \
} while (0)
#define END_FACE(k,t) do { face->texture=(t); face->reserved=0; face->kind=(k); ++face; } while (0)

void func_08002854(void)
{
    s32 center, previous, previous2, next, next2;
    s32 ring, first, following, ahead;
    s32 i, count, next_count, faces;
 s32 emitted;
    s32 next_left, next_right, this_left;
    s32 bridge_start, bridge_middle, bridge_end;
    s32 base_angle, left_angle, right_angle;
    s32 road_first, road_next;
    s32 type, bank, old_bank;
    s32 *settings;
    StreamPoint *point, *clear_point;
    StreamFace *face, *clear_face;
    if (g_03002334 == 0) {
        center = g_03005F50 + 28;
        if (center >= g_03002E4C) center -= g_03002E4C;
        ring = g_030001B8;
    } else {
        center = g_03005F50 - 1;
        if (center < 0) center += g_03002E4C;
        ring = (g_030001B8 - 29) & 31;
    }
    next = center + 1;
    if (next >= g_03002E4C) next = 0;
    next2 = next + 1;
    if (next2 >= g_03002E4C) next2 = 0;
    previous2 = center - 2;
    if (previous2 < 0) previous2 += g_03002E4C;
    previous = center - 1;
    if (previous < 0) previous += g_03002E4C;
    first = (ring & 31) * 24;
    following = ((ring + 1) & 31) * 24;
    ahead = ((ring + 2) & 31) * 24;
    face = &g_02033B70[(ring & 31) * 24];
    point = &g_02014000[first];
    clear_point = point;
    clear_face = face;
    i = 23;
    do {
        clear_point->active = 0;
        clear_face->kind = 0;
        ++clear_point;
        ++clear_face;
    } while (--i >= 0);
    emitted = 0;
    base_angle = ROW(center)->angle;
    left_angle = base_angle + 4096;
    right_angle = base_angle - 4096;
    faces = count = next_count = 0;
    next_left = next_right = this_left = 0;
    if ((center & 1) == 0) {
        bank = ROW(center)->bank_left;
        if (bank == 0) {
            old_bank = ROW(previous2)->bank_left;
            if (old_bank) {
                P(2560,left_angle,0);
                P(2560,left_angle,g_080219AC[old_bank][2]);
                count = 2;
            }
            if (ROW(next2)->bank_left) next_left = 4;
        } else {
            P(2560,left_angle,0);
            P(2560,left_angle,g_080219AC[ROW(center)->bank_left][2]);
            INDICES(first+1,ahead+1,ahead,first);
            
            RECT(g_080219AC[ROW(center)->bank_left][0],g_080219AC[ROW(center)->bank_left][1],g_080219AC[ROW(center)->bank_left][0]+31,g_080219AC[ROW(center)->bank_left][1]+63);
            END_FACE(1,g_080219AC[ROW(center)->bank_left][3]);
            ++faces;
            count = 2;
            next_left = 2;
            if (ROW(previous2)->bank_left == 0) {
                P(3840,left_angle,0);
                P(3840,left_angle,g_080219AC[ROW(center)->bank_left][2]);
                INDICES(first+3,first+1,first,first+2);
                
                RECT(g_080219AC[ROW(center)->bank_left][0]+32,g_080219AC[ROW(center)->bank_left][1],g_080219AC[ROW(center)->bank_left][0]+63,g_080219AC[ROW(center)->bank_left][1]+63);
                END_FACE(1,g_080219AC[ROW(center)->bank_left][3]);
                ++faces;
                count = 4;
            }
        }
        bank = ROW(center)->bank_right;
        if (bank == 0) {
            old_bank = ROW(previous2)->bank_right;
            if (old_bank) {
                this_left = count;
                P(2560,right_angle,0);
                P(2560,right_angle,g_080219AC[old_bank][2]);
                count += 2;
            }
        } else {
            P(2560,right_angle,0);
            P(2560,right_angle,g_080219AC[ROW(center)->bank_right][2]);
            INDICES(ahead+next_left+1,first+count+1,first+count,ahead+next_left);
            
            RECT(g_080219AC[ROW(center)->bank_right][0],g_080219AC[ROW(center)->bank_right][1],g_080219AC[ROW(center)->bank_right][0]+31,g_080219AC[ROW(center)->bank_right][1]+63);
            END_FACE(1,g_080219AC[ROW(center)->bank_right][3]);
            ++faces;
            count += 2;
            if (ROW(previous2)->bank_right == 0) {
                P(3840,right_angle,0);
                P(3840,right_angle,g_080219AC[ROW(center)->bank_right][2]);
                INDICES(first+count-1,first+count+1,first+count,first+count-2);
                
                RECT(g_080219AC[ROW(center)->bank_right][0]+32,g_080219AC[ROW(center)->bank_right][1],g_080219AC[ROW(center)->bank_right][0]+63,g_080219AC[ROW(center)->bank_right][1]+63);
                END_FACE(1,g_080219AC[ROW(center)->bank_right][3]);
                ++faces;
                count += 2;
            }
        }
    } else {
        if (ROW(next)->bank_left) next_count = ROW(previous)->bank_left ? 2 : 4;
        else if (ROW(previous)->bank_left) next_count = 2;
        if (ROW(next)->bank_right) next_count += ROW(previous)->bank_right ? 2 : 4;
        else if (ROW(previous)->bank_right) next_count += 2;
    }
    road_first = first+count;
    road_next = following+next_count;
    D(960,left_angle);
    INDICES(following+next_count,following+next_count+1,first+count+1,first+count);
    D(320,left_angle);
    
    RECT(g_08021520[ROW(center)->road[0]][0],g_08021520[ROW(center)->road[0]][1],g_08021520[ROW(center)->road[0]][0]+31,g_08021520[ROW(center)->road[0]][1]+31);
    END_FACE(1,g_08021520[ROW(center)->road[0]][2]);
    ++faces;
    INDICES(following+next_count+1,following+next_count+2,first+count+2,first+count+1);
    D(320,right_angle);
    
    RECT(g_0802158C[ROW(center)->road[1]][0],g_0802158C[ROW(center)->road[1]][1],g_0802158C[ROW(center)->road[1]][0]+31,g_0802158C[ROW(center)->road[1]][1]+31);
    END_FACE(1,g_0802158C[ROW(center)->road[1]][2]);
    ++faces;
    INDICES(following+next_count+2,following+next_count+3,first+count+3,first+count+2);
    D(960,right_angle);
    
    RECT(g_080215F8[ROW(center)->road[2]][0],g_080215F8[ROW(center)->road[2]][1],g_080215F8[ROW(center)->road[2]][0]+31,g_080215F8[ROW(center)->road[2]][1]+31);
    END_FACE(1,g_080215F8[ROW(center)->road[2]][2]);
    ++faces;
    /* The first wall establishes the cross-row seam used by the second. */
    face->index[2] = road_next;
    face->index[3] = road_first;
    count += 4;
    bank = ROW(center)->wall_left;
    if (bank != ROW(previous)->wall_left) {
        P(960,left_angle,g_08021718[ROW(previous)->wall_left][3]);
        ++count;
    }
    P(960,left_angle,g_08021718[ROW(center)->wall_left][3]);
    face->index[0] = first+count;
    face->index[1] = following+next_count+4;
    
    RECT(g_08021718[ROW(center)->wall_left][0],g_08021718[ROW(center)->wall_left][1],g_08021718[ROW(center)->wall_left][0]+31,g_08021718[ROW(center)->wall_left][1]+g_08021718[ROW(center)->wall_left][2]-1);
    END_FACE(1,g_08021718[ROW(center)->wall_left][4]);
    ++faces;
    ++count;
    next_count += ROW(next)->wall_left != ROW(center)->wall_left ? 6 : 5;
    bank = ROW(center)->wall_right;
    if (bank != ROW(previous)->wall_right) {
        P(960,right_angle,g_08021718[ROW(previous)->wall_right][3]);
        ++count;
    }
    P(960,right_angle,g_08021718[ROW(center)->wall_right][3]);
    INDICES(following+next_count,first+count,road_first+3,road_next+3);
    
    RECT(g_08021718[ROW(center)->wall_right][0],g_08021718[ROW(center)->wall_right][1],g_08021718[ROW(center)->wall_right][0]+31,g_08021718[ROW(center)->wall_right][1]+g_08021718[ROW(center)->wall_right][2]-1);
    END_FACE(1,g_08021718[ROW(center)->wall_right][4]);
    ++faces;
    ++count;
    next_count += ROW(next)->wall_right != ROW(center)->wall_right ? 2 : 1;
    if (ROW(center)->bridge == 0) {
        if (ROW(previous)->bridge) {
            P(960,left_angle,-600);
            P(0,left_angle,-600);
            P(960,right_angle,-600);
            count += 3;
        }
    } else {
        P(960,left_angle,-600);
        P(0,left_angle,-600);
        bridge_start = count;
        bridge_middle = count+1;
        bridge_end = count+2;
        INDICES(first+count,first+count+1,following+next_count+1,following+next_count);
        RECT(0,128,15,159);
        END_FACE(4,g_03005F48);
        ++faces;
        P(960,right_angle,-600);
        INDICES(first+count+1,first+count+2,following+next_count+2,following+next_count+1);
        RECT(16,128,31,159);
        END_FACE(4,g_03005F48);
        ++faces;
        count += 3;
    }
    /* Both scenery columns share the stream's point and face cursors. */
    for (i=0; i<2; ++i) {
        type = ROW(center)->scenery[i];
        if ((u8)(type-3) <= 8) {
            D(960,left_angle); P(2560,left_angle,-800); P(960,left_angle,-800);
            INDICES(first+count+1,first+count+2,first+count,first);
            RECT(48,128,63,191); END_FACE(1,2);
            P(0,right_angle,-800);
            INDICES(first+count+2,first+count+3,first+bridge_middle,first+bridge_start);
            RECT(32,128,47,145); END_FACE(1,2);
            P(960,right_angle,-800);
            INDICES(first+count+3,first+count+4,first+bridge_end,first+bridge_middle);
            RECT(48,128,63,145); END_FACE(1,2);
            P(2560,right_angle,-800); D(960,right_angle);
            INDICES(first+count+4,first+count+5,first+this_left,first+count+6);
            RECT(32,128,47,191); END_FACE(1,2);
            count += 7;
        }
        if (type==12 || type==14) {
            D(1920,left_angle); D(1280,left_angle); P(1920,left_angle,-600); P(1280,left_angle,-600);
            INDICES(first+count+2,first+count+3,first+count+1,first+count);
            if (type==11) { RECT(0,192,31,255); }
            else { RECT(32,192,63,255); }
            END_FACE(2,1); count += 4;
        }
        if (type==13 || type==15) {
            D(1920,right_angle); D(1280,right_angle); P(1920,right_angle,-600); P(1280,right_angle,-600);
            INDICES(first+count+3,first+count+2,first+count,first+count+1);
            if (type==12) { RECT(0,192,31,255); }
            else { RECT(32,192,63,255); }
            END_FACE(2,1); count += 4;
        }
        if (type==1) {
            D(1280,left_angle); D(1232,left_angle); P(1280,left_angle,-750); P(1216,left_angle,-750);
            INDICES(first+count+2,first+count+3,first+count+1,first+count);
            RECT(0,2,3,61); END_FACE(1,8);
            P(1240,left_angle,-740); P(1120,left_angle,-740); P(1240,left_angle,-800); P(1120,left_angle,-800);
            INDICES(first+count+6,first+count+7,first+count+5,first+count+4);
            RECT(4,0,11,7); END_FACE(3,8); count += 8;
        }
        if (type==2) {
            D(1280,right_angle); D(1232,right_angle); P(1280,right_angle,-750); P(1216,right_angle,-750);
            INDICES(first+count+3,first+count+2,first+count,first+count+1);
            RECT(20,2,23,61); END_FACE(1,8);
            P(1240,right_angle,-740); P(1120,right_angle,-740); P(1240,right_angle,-800); P(1120,right_angle,-800);
            INDICES(first+count+7,first+count+6,first+count+4,first+count+5);
            RECT(12,0,19,7); END_FACE(3,8); count += 8;
        }
        if ((u8)(type-16) <= 3) {
            D(1280,left_angle); D(1248,left_angle); P(1280,left_angle,-600); P(1248,left_angle,-600);
            INDICES(first+count+2,first+count+3,first+count+1,first+count);
            RECT(0,192,2,255); END_FACE(1,2);
            D(1280,right_angle); D(1248,right_angle); P(1280,right_angle,-600); P(1248,right_angle,-600);
            INDICES(first+count+7,first+count+6,first+count+4,first+count+5);
            RECT(3,192,5,255); END_FACE(1,2);
            P(392,left_angle,-600); P(1248,left_angle,-1000); P(392,left_angle,-1000);
            INDICES(first+count+9,first+count+10,first+count+8,first+count+2);
            RECT(64,192,95,223); END_FACE(1,2);
            P(392,right_angle,-600); P(392,right_angle,-1000);
            INDICES(first+count+10,first+count+12,first+count+11,first+count+8);
            RECT(64,192,95,223); END_FACE(1,2);
            P(1280,right_angle,-600); P(1280,right_angle,-1000);
            INDICES(first+count+12,first+count+14,first+count+13,first+count+11);
            RECT(64,192,95,223); END_FACE(1,2); count += 15;
        }
    }
}

#undef ROW
#undef D
#undef P
#undef INDICES
#undef RECT
#undef END_FACE
