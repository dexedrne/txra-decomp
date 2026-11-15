/* Unregistered projection-loop hypothesis derived from func_08016DA8_match.c.
 * Separate induction variables only; no target compile or byte match verified. */
/* Complete semantic candidate, NOT an installed or byte-verified replacement.
 * ARM profile: agbcc_arm -O2 -mthumb-interwork. See README.md for pool aliases.
 * All arithmetic words are unsigned: MUL/MLA/ADD/SUB wrap before signed ASR.
 * Address arithmetic is also ARM32 modular. No widened multiply is intended.
 */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed short s16;
typedef signed int s32;

typedef struct { u32 xyz[3], active, sx, sy, depth; } TrackPoint;
typedef struct {
    u16 kind, reserved;
    u32 index[4], u[4], v[4];
    u16 count, unknown_36;
} TrackFace;
/* Store addresses rather than native pointers: this layout is 32 bytes even
 * in the host synthetic harness. The target compiler uses 32-bit pointers. */
typedef struct {
    s16 x[4], y[4];
    u8 u[4], v[4];
    u16 count, kind;
    u32 next;
} TrackPacket;

/* Pool targets verified on the private host; see pool-target-addresses.json. */
#ifndef TXRA_SYNTHETIC
extern u8 g_030055F8[];
extern u8 g_03000AD0[];
extern u8 g_03000ADC[];
#define DEPTH_SCRATCH ((u32)g_030055F8)
#define SPECIAL_BASE ((u32)g_03000AD0)
#define SPECIAL_WIDTH ((u32)g_03000ADC)
#define MEM8(a) (*(u8 *)(u32)(a))
#define MEM16(a) (*(u16 *)(u32)(a))
#define MEM32(a) (*(u32 *)(u32)(a))
#else
/* Supplied only by the ROM-free test translation unit. */
#include "synthetic_memory.h"
#endif

#ifndef TXRA_SYNTHETIC
extern u8 g_030001B8[];
#define ADDRESS_030001B8 ((u32)g_030001B8)
extern u8 g_030021C4[];
#define ADDRESS_030021C4 ((u32)g_030021C4)
extern u8 g_03000670[];
#define ADDRESS_03000670 ((u32)g_03000670)
extern u8 g_030057A0[];
#define ADDRESS_030057A0 ((u32)g_030057A0)
extern u8 g_03005F70[];
#define ADDRESS_03005F70 ((u32)g_03005F70)
extern u8 g_03005F80[];
#define ADDRESS_03005F80 ((u32)g_03005F80)
extern u8 g_03002A18[];
#define ADDRESS_03002A18 ((u32)g_03002A18)
extern u8 g_03001B28[];
#define ADDRESS_03001B28 ((u32)g_03001B28)
extern u8 g_03005F58[];
#define ADDRESS_03005F58 ((u32)g_03005F58)
extern u8 g_03000DF8[];
#define ADDRESS_03000DF8 ((u32)g_03000DF8)
extern u8 g_03000DE0[];
#define ADDRESS_03000DE0 ((u32)g_03000DE0)
extern u8 g_0804F330[];
#define ADDRESS_0804F330 ((u32)g_0804F330)
#else
#define ADDRESS_030001B8 0x030001B8u
#define ADDRESS_030021C4 0x030021C4u
#define ADDRESS_03000670 0x03000670u
#define ADDRESS_030057A0 0x030057A0u
#define ADDRESS_03005F70 0x03005F70u
#define ADDRESS_03005F80 0x03005F80u
#define ADDRESS_03002A18 0x03002A18u
#define ADDRESS_03001B28 0x03001B28u
#define ADDRESS_03005F58 0x03005F58u
#define ADDRESS_03000DF8 0x03000DF8u
#define ADDRESS_03000DE0 0x03000DE0u
#define ADDRESS_0804F330 0x0804F330u
#endif

#define CURRENT ADDRESS_030021C4
#define BUCKETS ADDRESS_03000670
#define SCRATCH ADDRESS_030057A0
#define CAMERA ADDRESS_03005F70
#define OFFSET ADDRESS_03005F80
#define POINTS 0x02014000u
#define FACES 0x02033B70u

static __inline__ u32 asr32(u32 x, u32 shift)
{
    /* GCC ARM and the host checker both define signed right shift as ASR. */
    return (u32)((s32)x >> shift);
}

static __inline__ u32 midpoint(u32 a, u32 b)
{
    return asr32(a + b, 1);
}

static __inline__ u32 point_address(u32 index)
{
    return POINTS + ((index << 3) - index) * 4u;
}

static __inline__ s32 signed_half(u32 address)
{
    return (s16)MEM16(address);
}

/* Visibility is a single corner satisfying BOTH tests, before any clamping. */
static __inline__ int visible(u32 packet)
{
    return (MEM16(packet + 0) <= 119 && signed_half(packet + 8) >= 0 && signed_half(packet + 8) <= 159) ||
           (MEM16(packet + 2) <= 119 && signed_half(packet + 10) >= 0 && signed_half(packet + 10) <= 159) ||
           (MEM16(packet + 4) <= 119 && signed_half(packet + 12) >= 0 && signed_half(packet + 12) <= 159) ||
           (MEM16(packet + 6) <= 119 && signed_half(packet + 14) >= 0 && signed_half(packet + 14) <= 159);
}

static __inline__ u32 winding(u32 packet)
{
    u32 x0 = (u32)signed_half(packet);
    u32 y0 = (u32)signed_half(packet + 8);
    u32 dx3 = (u32)signed_half(packet + 6) - x0;
    u32 dy1 = (u32)signed_half(packet + 10) - y0;
    u32 dx1 = (u32)signed_half(packet + 2) - x0;
    u32 dy3 = (u32)signed_half(packet + 14) - y0;
    return dx3 * dy1 - dx1 * dy3;
}

static __inline__ void clamp_x(void)
{
    u32 packet;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 0) <= -67) MEM16(packet + 0) = (u16)-66;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 2) <= -67) MEM16(packet + 2) = (u16)-66;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 4) <= -67) MEM16(packet + 4) = (u16)-66;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 6) <= -67) MEM16(packet + 6) = (u16)-66;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 0) > 186) MEM16(packet + 0) = 186;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 2) > 186) MEM16(packet + 2) = 186;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 4) > 186) MEM16(packet + 4) = 186;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 6) > 186) MEM16(packet + 6) = 186;
}

static __inline__ void finish_packet(u32 face, const u32 depth[4])
{
    u32 packet = MEM32(CURRENT);
    u32 middle = depth[1] + depth[2]; /* LDMDA fp-30: fp-34 then fp-30. */
    u32 bucket = asr32((depth[0] + depth[3]) + middle, 7) + 32u;
    u32 previous;
    MEM16(packet + 24) = MEM16(face + 52);
    MEM16(packet + 26) = 0;
    if ((s32)bucket < 0) bucket = 0;
    if ((s32)bucket >= 255) bucket = 255;
    if (MEM16(face) == 2) MEM16(packet + 26) = 1;
    if (MEM16(face) == 4) MEM16(MEM32(CURRENT) + 26) = 2;
    previous = MEM32(BUCKETS + 4*bucket);
    packet = MEM32(CURRENT);
    MEM32(packet + 28) = previous;
    MEM32(CURRENT) = packet + 32;
    MEM32(BUCKETS + 4*bucket) = packet;
}

/* Subquad topology in source vertex order A B C D:
 * 0: A AB AC AD; 1: AB B BC AC; 2: AC BC C CD; 3: AD AC CD D.
 * AC is a diagonal midpoint, not an average of all four corners. */
static __inline__ void subdivide(u32 face, u32 part)
{
    u32 a = point_address(MEM32(face + 4));
    u32 b = point_address(MEM32(face + 8));
    u32 c = point_address(MEM32(face + 12));
    u32 d = point_address(MEM32(face + 16));
    if (part == 0) {
        MEM32(SCRATCH + 0) = MEM32(a + 0);
        MEM32(SCRATCH + 12) = midpoint(MEM32(a + 0), MEM32(b + 0));
        MEM32(SCRATCH + 24) = midpoint(MEM32(a + 0), MEM32(c + 0));
        MEM32(SCRATCH + 36) = midpoint(MEM32(a + 0), MEM32(d + 0));
        MEM32(SCRATCH + 4) = MEM32(a + 4);
        MEM32(SCRATCH + 16) = midpoint(MEM32(a + 4), MEM32(b + 4));
        MEM32(SCRATCH + 28) = midpoint(MEM32(a + 4), MEM32(c + 4));
        MEM32(SCRATCH + 40) = midpoint(MEM32(a + 4), MEM32(d + 4));
        MEM32(SCRATCH + 8) = MEM32(a + 8);
        MEM32(SCRATCH + 20) = midpoint(MEM32(a + 8), MEM32(b + 8));
        MEM32(SCRATCH + 32) = midpoint(MEM32(a + 8), MEM32(c + 8));
        MEM32(SCRATCH + 44) = midpoint(MEM32(a + 8), MEM32(d + 8));
    }
    if (part == 1) {
        MEM32(SCRATCH + 0) = midpoint(MEM32(a + 0), MEM32(b + 0));
        MEM32(SCRATCH + 12) = MEM32(b + 0);
        MEM32(SCRATCH + 24) = midpoint(MEM32(b + 0), MEM32(c + 0));
        MEM32(SCRATCH + 36) = midpoint(MEM32(a + 0), MEM32(c + 0));
        MEM32(SCRATCH + 4) = midpoint(MEM32(a + 4), MEM32(b + 4));
        MEM32(SCRATCH + 16) = MEM32(b + 4);
        MEM32(SCRATCH + 28) = midpoint(MEM32(b + 4), MEM32(c + 4));
        MEM32(SCRATCH + 40) = midpoint(MEM32(a + 4), MEM32(c + 4));
        MEM32(SCRATCH + 8) = midpoint(MEM32(a + 8), MEM32(b + 8));
        MEM32(SCRATCH + 20) = MEM32(b + 8);
        MEM32(SCRATCH + 32) = midpoint(MEM32(b + 8), MEM32(c + 8));
        MEM32(SCRATCH + 44) = midpoint(MEM32(a + 8), MEM32(c + 8));
    }
    if (part == 2) {
        MEM32(SCRATCH + 0) = midpoint(MEM32(a + 0), MEM32(c + 0));
        MEM32(SCRATCH + 12) = midpoint(MEM32(b + 0), MEM32(c + 0));
        MEM32(SCRATCH + 24) = MEM32(c + 0);
        MEM32(SCRATCH + 36) = midpoint(MEM32(d + 0), MEM32(c + 0));
        MEM32(SCRATCH + 4) = midpoint(MEM32(a + 4), MEM32(c + 4));
        MEM32(SCRATCH + 16) = midpoint(MEM32(b + 4), MEM32(c + 4));
        MEM32(SCRATCH + 28) = MEM32(c + 4);
        MEM32(SCRATCH + 40) = midpoint(MEM32(d + 4), MEM32(c + 4));
        MEM32(SCRATCH + 8) = midpoint(MEM32(a + 8), MEM32(c + 8));
        MEM32(SCRATCH + 20) = midpoint(MEM32(b + 8), MEM32(c + 8));
        MEM32(SCRATCH + 32) = MEM32(c + 8);
        MEM32(SCRATCH + 44) = midpoint(MEM32(d + 8), MEM32(c + 8));
    }
    if (part == 3) {
        MEM32(SCRATCH + 0) = midpoint(MEM32(a + 0), MEM32(d + 0));
        MEM32(SCRATCH + 12) = midpoint(MEM32(a + 0), MEM32(c + 0));
        MEM32(SCRATCH + 24) = midpoint(MEM32(d + 0), MEM32(c + 0));
        MEM32(SCRATCH + 36) = MEM32(d + 0);
        MEM32(SCRATCH + 4) = midpoint(MEM32(a + 4), MEM32(d + 4));
        MEM32(SCRATCH + 16) = midpoint(MEM32(a + 4), MEM32(c + 4));
        MEM32(SCRATCH + 28) = midpoint(MEM32(d + 4), MEM32(c + 4));
        MEM32(SCRATCH + 40) = MEM32(d + 4);
        MEM32(SCRATCH + 8) = midpoint(MEM32(a + 8), MEM32(d + 8));
        MEM32(SCRATCH + 20) = midpoint(MEM32(a + 8), MEM32(c + 8));
        MEM32(SCRATCH + 32) = midpoint(MEM32(d + 8), MEM32(c + 8));
        MEM32(SCRATCH + 44) = MEM32(d + 8);
    }
}

static __inline__ void project_subquad(void)
{
    s32 vertex = 0;
    u32 word_offset = 0, byte_offset = 0, z_cursor = SCRATCH + 8u;
    u32 x, z, y, px, pz, py, depth, factor, packet;
    u32 camera_z = MEM32(CAMERA + 8), offset_z = MEM32(OFFSET + 8);
    /* Original loop retains separate word/byte offsets and a scratch-Z cursor. */
    do {
        x = MEM32(SCRATCH + word_offset*4u) - MEM32(CAMERA);
        z = MEM32(z_cursor) - camera_z;
        px = MEM32(ADDRESS_03002A18)*x - MEM32(ADDRESS_03001B28)*z;
        pz = asr32(MEM32(ADDRESS_03001B28)*x + MEM32(ADDRESS_03002A18)*z, 12);
        y = 0u - MEM32(SCRATCH + 4u + byte_offset) - MEM32(CAMERA + 4);
        py = MEM32(ADDRESS_03005F58)*y + MEM32(ADDRESS_03000DF8)*pz;
        depth = offset_z + asr32(MEM32(ADDRESS_03000DF8)*y - MEM32(ADDRESS_03005F58)*pz, 12);
        MEM32(DEPTH_SCRATCH + byte_offset) = depth;
        factor = MEM32(ADDRESS_0804F330 + (asr32(depth, 1) + 65536u)*4u);
        x = MEM32(OFFSET) + asr32(px, 12);
        z = MEM32(OFFSET + 4) + asr32(py, 12);
        z_cursor += 12u;
        word_offset += 3u;
        packet = MEM32(CURRENT);
        MEM16(packet + (u32)vertex*2u) = (u16)(asr32(factor*(x << 3), 16) + 60u);
        MEM16(packet + 8u + (u32)vertex*2u) = (u16)(asr32(factor*(z << 3), 15) + 80u);
        ++vertex;
        byte_offset += 12u;
    } while (vertex <= 3);
}

static __inline__ void near_expand_and_clamp(void)
{
    u32 packet = MEM32(CURRENT);
    MEM16(packet + 8) = (u16)(MEM16(packet + 8) - 1u);
    MEM16(packet) = (u16)(MEM16(packet) - 1u);
    MEM16(packet + 2) = (u16)(MEM16(packet + 2) + 1u);
    MEM16(packet + 10) = (u16)(MEM16(packet + 10) - 1u);
    packet = MEM32(CURRENT);
    if (signed_half(packet + 8) < -175) MEM16(packet + 8) = (u16)-174;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 10) < -175) MEM16(packet + 10) = (u16)-174;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 12) < -175) MEM16(packet + 12) = (u16)-174;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 14) < -175) MEM16(packet + 14) = (u16)-174;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 8) > 335) MEM16(packet + 8) = 334;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 10) > 335) MEM16(packet + 10) = 334;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 12) > 335) MEM16(packet + 12) = 334;
    packet = MEM32(CURRENT);
    if (signed_half(packet + 14) > 335) MEM16(packet + 14) = 334;
    clamp_x();
}

static __inline__ void texture_subquad(u32 face, u32 part)
{
    if (part == 0) {
        MEM8(MEM32(CURRENT) + 16) = MEM8(face + 20);
        MEM8(MEM32(CURRENT) + 20) = MEM8(face + 36);
        MEM8(MEM32(CURRENT) + 17) = (u8)midpoint(MEM32(face + 20), MEM32(face + 24));
        MEM8(MEM32(CURRENT) + 21) = (u8)midpoint(MEM32(face + 36), MEM32(face + 40));
        MEM8(MEM32(CURRENT) + 18) = (u8)midpoint(MEM32(face + 24), MEM32(face + 32));
        MEM8(MEM32(CURRENT) + 22) = (u8)midpoint(MEM32(face + 40), MEM32(face + 48));
        MEM8(MEM32(CURRENT) + 19) = (u8)midpoint(MEM32(face + 20), MEM32(face + 32));
        MEM8(MEM32(CURRENT) + 23) = (u8)midpoint(MEM32(face + 36), MEM32(face + 48));
    }
    if (part == 1) {
        MEM8(MEM32(CURRENT) + 16) = (u8)midpoint(MEM32(face + 20), MEM32(face + 24));
        MEM8(MEM32(CURRENT) + 20) = (u8)midpoint(MEM32(face + 36), MEM32(face + 40));
        MEM8(MEM32(CURRENT) + 17) = MEM8(face + 24);
        MEM8(MEM32(CURRENT) + 21) = MEM8(face + 40);
        MEM8(MEM32(CURRENT) + 18) = (u8)midpoint(MEM32(face + 24), MEM32(face + 28));
        MEM8(MEM32(CURRENT) + 22) = (u8)midpoint(MEM32(face + 40), MEM32(face + 44));
        MEM8(MEM32(CURRENT) + 19) = (u8)midpoint(MEM32(face + 24), MEM32(face + 32));
        MEM8(MEM32(CURRENT) + 23) = (u8)midpoint(MEM32(face + 40), MEM32(face + 48));
    }
    if (part == 2) {
        MEM8(MEM32(CURRENT) + 16) = (u8)midpoint(MEM32(face + 24), MEM32(face + 32));
        MEM8(MEM32(CURRENT) + 20) = (u8)midpoint(MEM32(face + 40), MEM32(face + 48));
        MEM8(MEM32(CURRENT) + 17) = (u8)midpoint(MEM32(face + 24), MEM32(face + 28));
        MEM8(MEM32(CURRENT) + 21) = (u8)midpoint(MEM32(face + 40), MEM32(face + 44));
        MEM8(MEM32(CURRENT) + 18) = MEM8(face + 28);
        MEM8(MEM32(CURRENT) + 22) = MEM8(face + 44);
        MEM8(MEM32(CURRENT) + 19) = (u8)midpoint(MEM32(face + 28), MEM32(face + 32));
        MEM8(MEM32(CURRENT) + 23) = (u8)midpoint(MEM32(face + 44), MEM32(face + 48));
    }
    if (part == 3) {
        MEM8(MEM32(CURRENT) + 16) = (u8)midpoint(MEM32(face + 20), MEM32(face + 32));
        MEM8(MEM32(CURRENT) + 20) = (u8)midpoint(MEM32(face + 36), MEM32(face + 48));
        MEM8(MEM32(CURRENT) + 17) = (u8)midpoint(MEM32(face + 24), MEM32(face + 32));
        MEM8(MEM32(CURRENT) + 21) = (u8)midpoint(MEM32(face + 40), MEM32(face + 48));
        MEM8(MEM32(CURRENT) + 18) = (u8)midpoint(MEM32(face + 28), MEM32(face + 32));
        MEM8(MEM32(CURRENT) + 22) = (u8)midpoint(MEM32(face + 44), MEM32(face + 48));
        MEM8(MEM32(CURRENT) + 19) = MEM8(face + 32);
        MEM8(MEM32(CURRENT) + 23) = MEM8(face + 48);
    }
}

void func_08016DA8(void)
{
    u32 tick = MEM32(ADDRESS_030001B8);
    u32 ring = (tick - 29u) & 31u, end = (tick - 6u) & 31u;
    u32 face, next_ring, point[4], depth[4], part, packet;
    do {
        face = FACES + ring*1344u;
        next_ring = ring + 1u;
        while (MEM16(face) != 0) {
            point[0] = point_address(MEM32(face + 4));
            depth[0] = MEM32(point[0] + 24);
            point[1] = point_address(MEM32(face + 8));
            depth[1] = MEM32(point[1] + 24);
            point[2] = point_address(MEM32(face + 12));
            depth[2] = MEM32(point[2] + 24);
            point[3] = point_address(MEM32(face + 16));
            depth[3] = MEM32(point[3] + 24);
            if ((s32)depth[0] > 767 && (s32)depth[1] > 767 &&
                (s32)depth[2] > 767 && (s32)depth[3] > 767) {
                packet = MEM32(CURRENT);
                MEM16(packet + 0) = MEM16(point[0] + 16);
                MEM16(packet + 8) = MEM16(point[0] + 20);
                MEM16(packet + 2) = MEM16(point[1] + 16);
                MEM16(packet + 10) = MEM16(point[1] + 20);
                MEM16(packet + 4) = MEM16(point[2] + 16);
                MEM16(packet + 12) = MEM16(point[2] + 20);
                MEM16(packet + 6) = MEM16(point[3] + 16);
                MEM16(packet + 14) = MEM16(point[3] + 20);
                if (visible(MEM32(CURRENT)) && (s32)winding(MEM32(CURRENT)) <= 0) {
                    if (MEM16(face) == 3) {
                        u32 slot = MEM32(ADDRESS_03000DE0), offset = slot << 4;
                        MEM32(SPECIAL_BASE + offset) = 1;
                        MEM32(SPECIAL_BASE + 4 + offset) = MEM32(point[1] + 16) + MEM32(point[0] + 16);
                        MEM32(SPECIAL_BASE + 8 + offset) = midpoint(MEM32(point[2] + 20), MEM32(point[0] + 20));
                        MEM32(SPECIAL_WIDTH + offset) = (MEM32(point[1] + 16) - MEM32(point[0] + 16)) << 1;
                        MEM32(ADDRESS_03000DE0) = slot + 1u;
                    }
                    clamp_x();
                    MEM8(MEM32(CURRENT) + 16) = MEM8(face + 20);
                    MEM8(MEM32(CURRENT) + 20) = MEM8(face + 36);
                    MEM8(MEM32(CURRENT) + 17) = MEM8(face + 24);
                    MEM8(MEM32(CURRENT) + 21) = MEM8(face + 40);
                    MEM8(MEM32(CURRENT) + 18) = MEM8(face + 28);
                    MEM8(MEM32(CURRENT) + 22) = MEM8(face + 44);
                    MEM8(MEM32(CURRENT) + 19) = MEM8(face + 32);
                    MEM8(MEM32(CURRENT) + 23) = MEM8(face + 48);
                    finish_packet(face, depth);
                }
            } else {
                for (part = 0; part != 4; ++part) {
                    if ((s32)depth[part] < 0) continue;
                    subdivide(face, part);
                    project_subquad();
                    if (!visible(MEM32(CURRENT))) continue;
                    near_expand_and_clamp();
                    if ((s32)winding(MEM32(CURRENT)) > 0) continue;
                    texture_subquad(face, part);
                    finish_packet(face, depth);
                }
            }
            face += 56u;
        }
        ring = next_ring & 31u;
    } while (ring != end);
}
