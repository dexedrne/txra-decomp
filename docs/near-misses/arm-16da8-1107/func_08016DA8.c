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

#define CURRENT 0x030021C4u
#define BUCKETS 0x03000670u
#define SCRATCH 0x030057A0u
#define CAMERA 0x03005F70u
#define OFFSET 0x03005F80u
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
    u32 i;
    for (i = 0; i != 4; ++i)
        if (MEM16(packet + 2*i) <= 119 &&
            signed_half(packet + 8 + 2*i) >= 0 &&
            signed_half(packet + 8 + 2*i) <= 159) return 1;
    return 0;
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
    u32 i, packet;
    for (i = 0; i != 4; ++i) {
        packet = MEM32(CURRENT);
        if (signed_half(packet + 2*i) <= -67) MEM16(packet + 2*i) = (u16)-66;
    }
    for (i = 0; i != 4; ++i) {
        packet = MEM32(CURRENT);
        if (signed_half(packet + 2*i) > 186) MEM16(packet + 2*i) = 186;
    }
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
    u32 component, a, b, c, d, base;
    for (component = 0; component != 12; component += 4) {
        a = point_address(MEM32(face + 4));
        b = point_address(MEM32(face + 8));
        c = point_address(MEM32(face + 12));
        d = point_address(MEM32(face + 16));
        base = SCRATCH + component;
        /* Each component is stored in order before loading the next component.
         * Re-read source values at their use, as the original stores do. */
        if (part == 0) {
            MEM32(base) = MEM32(a + component);
            MEM32(base + 12) = midpoint(MEM32(a + component), MEM32(b + component));
            MEM32(base + 24) = midpoint(MEM32(a + component), MEM32(c + component));
            MEM32(base + 36) = midpoint(MEM32(a + component), MEM32(d + component));
        } else if (part == 1) {
            MEM32(base) = midpoint(MEM32(a + component), MEM32(b + component));
            MEM32(base + 12) = MEM32(b + component);
            MEM32(base + 24) = midpoint(MEM32(b + component), MEM32(c + component));
            MEM32(base + 36) = midpoint(MEM32(a + component), MEM32(c + component));
        } else if (part == 2) {
            MEM32(base) = midpoint(MEM32(a + component), MEM32(c + component));
            MEM32(base + 12) = midpoint(MEM32(b + component), MEM32(c + component));
            MEM32(base + 24) = MEM32(c + component);
            MEM32(base + 36) = midpoint(MEM32(d + component), MEM32(c + component));
        } else {
            MEM32(base) = midpoint(MEM32(a + component), MEM32(d + component));
            MEM32(base + 12) = midpoint(MEM32(a + component), MEM32(c + component));
            MEM32(base + 24) = midpoint(MEM32(d + component), MEM32(c + component));
            MEM32(base + 36) = MEM32(d + component);
        }
    }
}

static __inline__ void project_subquad(void)
{
    u32 i, x, z, y, px, pz, py, depth, factor, packet;
    u32 camera_z = MEM32(CAMERA + 8), offset_z = MEM32(OFFSET + 8);
    for (i = 0; i != 4; ++i) {
        x = MEM32(SCRATCH + i*12) - MEM32(CAMERA);
        z = MEM32(SCRATCH + i*12 + 8) - camera_z;
        px = MEM32(0x03002A18u)*x - MEM32(0x03001B28u)*z;
        pz = asr32(MEM32(0x03001B28u)*x + MEM32(0x03002A18u)*z, 12);
        y = 0u - MEM32(SCRATCH + i*12 + 4) - MEM32(CAMERA + 4);
        py = MEM32(0x03005F58u)*y + MEM32(0x03000DF8u)*pz;
        depth = offset_z + asr32(MEM32(0x03000DF8u)*y - MEM32(0x03005F58u)*pz, 12);
        MEM32(DEPTH_SCRATCH + i*12) = depth;
        factor = MEM32(0x0804F330u + (asr32(depth, 1) + 65536u)*4u);
        x = MEM32(OFFSET) + asr32(px, 12);
        z = MEM32(OFFSET + 4) + asr32(py, 12);
        packet = MEM32(CURRENT);
        MEM16(packet + i*2) = (u16)(asr32(factor*(x << 3), 16) + 60u);
        MEM16(packet + 8 + i*2) = (u16)(asr32(factor*(z << 3), 15) + 80u);
    }
}

static __inline__ void near_expand_and_clamp(void)
{
    u32 packet = MEM32(CURRENT), i;
    MEM16(packet + 8) = (u16)(MEM16(packet + 8) - 1u);
    MEM16(packet) = (u16)(MEM16(packet) - 1u);
    MEM16(packet + 2) = (u16)(MEM16(packet + 2) + 1u);
    MEM16(packet + 10) = (u16)(MEM16(packet + 10) - 1u);
    for (i = 0; i != 4; ++i) {
        packet = MEM32(CURRENT);
        if (signed_half(packet + 8 + 2*i) < -175) MEM16(packet + 8 + 2*i) = (u16)-174;
    }
    for (i = 0; i != 4; ++i) {
        packet = MEM32(CURRENT);
        if (signed_half(packet + 8 + 2*i) > 335) MEM16(packet + 8 + 2*i) = 334;
    }
    clamp_x();
}

static __inline__ void texture_subquad(u32 face, u32 part)
{
    u32 axis, base, out, packet;
    /* Interleaved u/v stores follow the original corner order. */
    for (out = 0; out != 4; ++out) {
        for (axis = 0; axis != 2; ++axis) {
            u32 value = 0;
            base = face + 20 + axis*16;
            if (part == 0) {
                if (out == 0) value = MEM8(base);
                if (out == 1) value = midpoint(MEM32(base), MEM32(base + 4));
                if (out == 2) value = midpoint(MEM32(base + 4), MEM32(base + 12));
                if (out == 3) value = midpoint(MEM32(base), MEM32(base + 12));
            } else if (part == 1) {
                if (out == 0) value = midpoint(MEM32(base), MEM32(base + 4));
                if (out == 1) value = MEM8(base + 4);
                if (out == 2) value = midpoint(MEM32(base + 4), MEM32(base + 8));
                if (out == 3) value = midpoint(MEM32(base + 4), MEM32(base + 12));
            } else if (part == 2) {
                if (out == 0) value = midpoint(MEM32(base + 4), MEM32(base + 12));
                if (out == 1) value = midpoint(MEM32(base + 4), MEM32(base + 8));
                if (out == 2) value = MEM8(base + 8);
                if (out == 3) value = midpoint(MEM32(base + 8), MEM32(base + 12));
            } else {
                if (out == 0) value = midpoint(MEM32(base), MEM32(base + 12));
                if (out == 1) value = midpoint(MEM32(base + 4), MEM32(base + 12));
                if (out == 2) value = midpoint(MEM32(base + 8), MEM32(base + 12));
                if (out == 3) value = MEM8(base + 12);
            }
            packet = MEM32(CURRENT);
            MEM8(packet + 16 + axis*4 + out) = (u8)value;
        }
    }
}

void func_08016DA8(void)
{
    u32 tick = MEM32(0x030001B8u);
    u32 ring = (tick - 29u) & 31u, end = (tick - 6u) & 31u;
    u32 face, next_ring, i, point[4], depth[4], part, packet;
    do {
        face = FACES + ring*1344u;
        next_ring = ring + 1u;
        while (MEM16(face) != 0) {
            for (i = 0; i != 4; ++i) {
                point[i] = point_address(MEM32(face + 4 + i*4));
                depth[i] = MEM32(point[i] + 24);
            }
            if ((s32)depth[0] > 767 && (s32)depth[1] > 767 &&
                (s32)depth[2] > 767 && (s32)depth[3] > 767) {
                packet = MEM32(CURRENT);
                for (i = 0; i != 4; ++i) {
                    MEM16(packet + i*2) = MEM16(point[i] + 16);
                    MEM16(packet + 8 + i*2) = MEM16(point[i] + 20);
                }
                if (visible(MEM32(CURRENT)) && (s32)winding(MEM32(CURRENT)) <= 0) {
                    if (MEM16(face) == 3) {
                        u32 slot = MEM32(0x03000DE0u), offset = slot << 4;
                        MEM32(SPECIAL_BASE + offset) = 1;
                        MEM32(SPECIAL_BASE + 4 + offset) = MEM32(point[1] + 16) + MEM32(point[0] + 16);
                        MEM32(SPECIAL_BASE + 8 + offset) = midpoint(MEM32(point[2] + 20), MEM32(point[0] + 20));
                        MEM32(SPECIAL_WIDTH + offset) = (MEM32(point[1] + 16) - MEM32(point[0] + 16)) << 1;
                        MEM32(0x03000DE0u) = slot + 1u;
                    }
                    clamp_x();
                    for (i = 0; i != 4; ++i) {
                        MEM8(MEM32(CURRENT) + 16 + i) = MEM8(face + 20 + i*4);
                        MEM8(MEM32(CURRENT) + 20 + i) = MEM8(face + 36 + i*4);
                    }
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
