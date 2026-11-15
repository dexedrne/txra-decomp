#include "gba.h"
#include <limits.h>
#define N 0x80000000u
#define Z 0x40000000u
#define C 0x20000000u
#define V 0x10000000u
static u32 ror(u32 x, unsigned s) {
    s &= 31;
    return s ? (x >> s) | (x << (32 - s)) : x;
}
static void nz(GBA *g, u32 x) {
    g->cpsr = (g->cpsr & ~(N | Z)) | (x & N) | (x ? 0 : Z);
}
static u32 add(GBA *g, u32 a, u32 b, unsigned carry, bool flags) {
    uint64_t v = (uint64_t)a + b + carry;
    u32 r = v;
    if (flags) {
        nz(g, r);
        g->cpsr = (g->cpsr & ~(C | V)) | ((v >> 32) ? C : 0) | ((~(a ^ b) & (a ^ r) & N) ? V : 0);
    }
    return r;
}
static u32 shift(GBA *g, u32 a, unsigned type, unsigned n, bool flags, bool imm) {
    unsigned c = (g->cpsr & C) != 0;
    u32 r = a;
    if (!n && imm && type) {
        if (type == 3) {
            r = (a >> 1) | (c << 31);
            c = a & 1;
            goto done;
        }
        n = 32;
    }
    if (!n)
        return a;
    switch (type) {
    case 0:
        c = n <= 32 ? ((a >> (32 - n)) & 1) : 0;
        r = n < 32 ? a << n : 0;
        break;
    case 1:
        c = n <= 32 ? ((a >> (n - 1)) & 1) : 0;
        r = n < 32 ? a >> n : 0;
        break;
    case 2:
        c = n < 32 ? ((a >> (n - 1)) & 1) : (a >> 31);
        r = n < 32 ? (u32)((int32_t)a >> n) : (a & N ? ~0u : 0);
        break;
    case 3:
        r = ror(a, n);
        c = r >> 31;
        break;
    }
done:
    if (flags)
        g->cpsr = (g->cpsr & ~C) | (c ? C : 0);
    return r;
}
void branch(GBA *g, u32 dst, bool t) {
    if (g->coverage) coverage_branch(g, dst, t);
    g->cpsr = (g->cpsr & ~32u) | (t ? 32 : 0);
    g->r[15] = dst & ~(t ? 1u : 3u);
}
void arm_dp(GBA *g, unsigned imm, unsigned op, unsigned s, unsigned rn, unsigned rd, u32 bits,
            unsigned unused, unsigned unused2) {
    (void)unused;
    (void)unused2;
    u32 a = reg(g, rn), b, r = 0;
    unsigned carry = (g->cpsr & C) != 0;
    bool logical = op == 0 || op == 1 || op == 8 || op == 9 || op >= 12;
    if (imm) {
        b = ror(bits & 255, ((bits >> 8) & 15) * 2);
        if (s && logical && (bits & 0xf00))
            g->cpsr = (g->cpsr & ~C) | (b & N ? C : 0);
    } else {
        unsigned rs = (bits >> 8) & 15;
        unsigned amount = bits & 16 ? (reg(g, rs) & 255) : ((bits >> 7) & 31);
        b = reg(g, bits & 15);
        if ((bits & 16) && (bits & 15) == 15)
            b += 4;
        b = shift(g, b, (bits >> 5) & 3, amount, s && logical, !(bits & 16));
    }
    switch (op) {
    case 0:
    case 8:
        r = a & b;
        break;
    case 1:
    case 9:
        r = a ^ b;
        break;
    case 2:
    case 10:
        r = add(g, a, ~b, 1, s);
        break;
    case 3:
        r = add(g, b, ~a, 1, s);
        break;
    case 4:
    case 11:
        r = add(g, a, b, 0, s);
        break;
    case 5:
        r = add(g, a, b, carry, s);
        break;
    case 6:
        r = add(g, a, ~b, carry, s);
        break;
    case 7:
        r = add(g, b, ~a, carry, s);
        break;
    case 12:
        r = a | b;
        break;
    case 13:
        r = b;
        break;
    case 14:
        r = a & ~b;
        break;
    case 15:
        r = ~b;
        break;
    }
    if (s && logical)
        nz(g, r);
    if (op >= 8 && op <= 11) {
        g->r[15] += 4;
        return;
    }
    if (rd == 15) {
        if (s)
            g->cpsr = g->spsr;
        branch(g, r, (g->cpsr & 32) != 0);
    } else {
        g->r[rd] = r;
        g->r[15] += 4;
    }
}
void arm_mem(GBA *g, unsigned i, unsigned p, unsigned u, unsigned b, unsigned w, unsigned l, u32 rn,
             unsigned rd, unsigned off) {
    u32 base = reg(g, rn),
        delta = i ? shift(g, reg(g, off & 15), (off >> 5) & 3, (off >> 7) & 31, false, true) : off;
    u32 next = u ? base + delta : base - delta, ad = p ? next : base;
    if (l) {
        u32 value = b ? rd8(g, ad) : rd32(g, ad);
        if ((!p || w) && rn != rd)
            g->r[rn] = next;
        if (rd == 15) {
            branch(g, value, false);
            return;
        }
        g->r[rd] = value;
    } else {
        u32 value = reg(g, rd) + (rd == 15 ? 4 : 0);
        if (b)
            wr8(g, ad, value);
        else
            wr32(g, ad, value);
        if (!p || w)
            g->r[rn] = next;
    }
    g->r[15] += 4;
}
void arm_half(GBA *g, unsigned p, unsigned u, unsigned i, unsigned w, unsigned l, unsigned rn,
              unsigned rd, u32 off, unsigned kind) {
    u32 base = reg(g, rn), delta = i ? off : reg(g, off & 15),
        next = u ? base + delta : base - delta, ad = p ? next : base;
    if (l) {
        u32 v = kind == 1   ? rd16(g, ad)
                : kind == 2 ? (u32)(int32_t)(int8_t)rd8(g, ad)
                            : (ad & 1 ? (u32)(int32_t)(int8_t)rd8(g, ad)
                                      : (u32)(int32_t)(int16_t)rd16(g, ad));
        g->r[rd] = v;
    } else
        wr16(g, ad, reg(g, rd));
    if (!p || w)
        g->r[rn] = next;
    if (rd != 15 || !l)
        g->r[15] += 4;
}
void arm_block(GBA *g, unsigned p, unsigned u, unsigned s, unsigned w, unsigned l, unsigned rn,
               unsigned list) {
    unsigned n = __builtin_popcount(list);
    u32 base = reg(g, rn);
    bool empty = !n;
    if (empty) {
        list = 1 << 15;
        n = 16;
    }
    u32 ad = u ? base + (p ? 4 : 0) : base - 4 * n + (p ? 0 : 4), dest = 0;
    bool pc = false;
    for (unsigned i = 0; i < 16; i++)
        if (list & (1u << i)) {
            if (l) {
                u32 v = rd32(g, ad & ~3u);
                if (i == 15) {
                    dest = v;
                    pc = true;
                } else
                    g->r[i] = v;
            } else
                wr32(g, ad, reg(g, i) + (i == 15 ? 4 : 0));
            ad += 4;
        }
    if (w && !(l && (list & (1u << rn))))
        g->r[rn] = u ? base + 4 * n : base - 4 * n;
    if (pc) {
        if (s)
            g->cpsr = g->spsr;
        branch(g, dest, (g->cpsr & 32) != 0);
    } else
        g->r[15] += 4;
}
void arm_mul(GBA *g, unsigned wide, unsigned sign, unsigned acc, unsigned s, unsigned hi,
             unsigned lo, unsigned rs, unsigned rm) {
    u32 a = reg(g, rm), b = reg(g, rs);
    if (wide) {
        uint64_t v = sign ? (uint64_t)((int64_t)(int32_t)a * (int64_t)(int32_t)b) : (uint64_t)a * b;
        if (acc)
            v += ((uint64_t)g->r[hi] << 32) | g->r[lo];
        g->r[lo] = v;
        g->r[hi] = v >> 32;
        if (s)
            g->cpsr = (g->cpsr & ~(N | Z)) | (g->r[hi] & N) | (v ? 0 : Z);
    } else {
        u32 r = a * b + (acc ? g->r[lo] : 0);
        g->r[hi] = r;
        if (s)
            nz(g, r);
    }
    g->r[15] += 4;
}
void arm_status(GBA *g, unsigned write, unsigned saved, unsigned field, u32 bits) {
    if (!write)
        g->r[field] = saved ? g->spsr : g->cpsr;
    else {
        u32 value = bits & (1u << 16) ? ror(bits & 255, ((bits >> 8) & 15) * 2) : reg(g, bits & 15),
            mask = 0;
        for (unsigned b = 0; b < 4; b++)
            if (field & (1u << b))
                mask |= 255u << (b * 8);
        if (saved)
            g->spsr = (g->spsr & ~mask) | (value & mask);
        else {
            u32 old = g->cpsr & 31, newmode = (mask & 255) ? value & 31 : old;
            if (old != newmode) {
                g->bank_sp[old] = g->r[13];
                g->bank_lr[old] = g->r[14];
                g->r[13] = g->bank_sp[newmode];
                g->r[14] = g->bank_lr[newmode];
            }
            g->cpsr = (g->cpsr & ~mask) | (value & mask);
        }
    }
    g->r[15] += 4;
}
void thumb(GBA *g, unsigned group, unsigned op, unsigned x, unsigned y, int z) {
    u32 a, b, r = 0, ad;
    bool wrotepc = false;
    unsigned c = (g->cpsr & C) != 0;
    switch (group) {
    case 0:
        if (op < 3) {
            g->r[z] = shift(g, g->r[y], op, x, true, true);
            nz(g, g->r[z]);
        } else {
            a = g->r[y];
            b = x & 16 ? (x & 7) : g->r[x & 7];
            g->r[z] = x & 8 ? add(g, a, ~b, 1, true) : add(g, a, b, 0, true);
        }
        break;
    case 1:
        a = g->r[x];
        if (op == 0) {
            g->r[x] = y;
            nz(g, y);
        }
        if (op == 1)
            add(g, a, ~y, 1, true);
        if (op == 2)
            g->r[x] = add(g, a, y, 0, true);
        if (op == 3)
            g->r[x] = add(g, a, ~y, 1, true);
        break;
    case 2:
        a = g->r[y];
        b = g->r[x];
        switch (op) {
        case 0:
            r = a & b;
            break;
        case 1:
            r = a ^ b;
            break;
        case 2:
        case 3:
        case 4:
            r = shift(g, a, op - 2, b & 255, true, false);
            break;
        case 5:
            r = add(g, a, b, c, true);
            break;
        case 6:
            r = add(g, a, ~b, c, true);
            break;
        case 7:
            r = shift(g, a, 3, b & 255, true, false);
            break;
        case 8:
            r = a & b;
            break;
        case 9:
            r = add(g, 0, ~b, 1, true);
            break;
        case 10:
            r = add(g, a, ~b, 1, true);
            break;
        case 11:
            r = add(g, a, b, 0, true);
            break;
        case 12:
            r = a | b;
            break;
        case 13:
            r = a * b;
            break;
        case 14:
            r = a & ~b;
            break;
        case 15:
            r = ~b;
            break;
        }
        nz(g, r);
        if (op != 8 && op != 10 && op != 11)
            g->r[y] = r;
        break;
    case 3:
        a = reg(g, y);
        b = reg(g, x);
        if (op == 0)
            r = a + b;
        if (op == 1)
            add(g, a, ~b, 1, true);
        if (op == 2)
            r = b;
        if (op == 3) {
            branch(g, b, b & 1);
            wrotepc = true;
        } else if (op != 1) {
            if (y == 15) {
                branch(g, r, true);
                wrotepc = true;
            } else
                g->r[y] = r;
        }
        break;
    case 4:
        ad = g->r[y] + g->r[x];
        switch (op) {
        case 0:
            wr32(g, ad, g->r[z]);
            break;
        case 1:
            wr16(g, ad, g->r[z]);
            break;
        case 2:
            wr8(g, ad, g->r[z]);
            break;
        case 3:
            g->r[z] = (int32_t)(int8_t)rd8(g, ad);
            break;
        case 4:
            g->r[z] = rd32(g, ad);
            break;
        case 5:
            g->r[z] = rd16(g, ad);
            break;
        case 6:
            g->r[z] = rd8(g, ad);
            break;
        case 7:
            g->r[z] = ad & 1 ? (int32_t)(int8_t)rd8(g, ad) : (int32_t)(int16_t)rd16(g, ad);
            break;
        }
        break;
    case 5:
        ad = g->r[y] + (op & 2 ? x : x * 4);
        if (op & 1)
            g->r[z] = op & 2 ? rd8(g, ad) : rd32(g, ad);
        else if (op & 2)
            wr8(g, ad, g->r[z]);
        else
            wr32(g, ad, g->r[z]);
        break;
    case 6:
        ad = g->r[y] + x * 2;
        if (op)
            g->r[z] = rd16(g, ad);
        else
            wr16(g, ad, g->r[z]);
        break;
    case 7:
        ad = g->r[13] + y;
        if (op)
            g->r[x] = rd32(g, ad);
        else
            wr32(g, ad, g->r[x]);
        break;
    case 8:
        g->r[x] = (op ? g->r[13] : (g->r[15] + 4) & ~3u) + y;
        break;
    case 9:
        g->r[13] = op ? g->r[13] - x : g->r[13] + x;
        break;
    case 10: {
        unsigned list = x | (y ? (op ? 1u << 15 : 1u << 14) : 0), n = __builtin_popcount(list);
        ad = op ? g->r[13] : g->r[13] - n * 4;
        u32 start = ad;
        for (unsigned i = 0; i < 16; i++)
            if (list & (1u << i)) {
                if (op) {
                    u32 v = rd32(g, ad);
                    if (i == 15) {
                        branch(g, v, true);
                        wrotepc = true;
                    } else
                        g->r[i] = v;
                } else
                    wr32(g, ad, g->r[i]);
                ad += 4;
            }
        g->r[13] = op ? ad : start;
        break;
    }
    case 11:
        ad = g->r[x];
        for (unsigned i = 0; i < 8; i++)
            if (y & (1u << i)) {
                if (op)
                    g->r[i] = rd32(g, ad);
                else
                    wr32(g, ad, g->r[i]);
                ad += 4;
            }
        if (!op || !(y & (1u << x)))
            g->r[x] = ad;
        break;
    }
    if (!wrotepc)
        g->r[15] += 2;
}
void fallback(GBA *g) {
    u32 pc = g->r[15], w;
    bool t = g->cpsr & 32;
    if (!tick(g))
        return;
    g->fallback_steps++;
    if (t) {
        w = rd16(g, pc);
        unsigned a = (w >> 8) & 7, b = (w >> 3) & 7, c = w & 7;
        if ((w & 0xf800) == 0xf000) {
            g->r[14] = pc + 4 + ((int32_t)(w << 21) >> 9);
            g->r[15] += 2;
        } else if ((w & 0xf800) == 0xf800) {
            u32 dst = g->r[14] + (w & 2047) * 2;
            g->r[14] = (pc + 2) | 1;
            branch(g, dst, true);
        } else if ((w & 0xf800) == 0xe000)
            g->r[15] = pc + 4 + ((int32_t)(w << 21) >> 20);
        else if ((w & 0xff00) == 0xdf00) {
            g->r[15] += 2;
            bios(g, w & 255);
        } else if ((w & 0xf000) == 0xd000)
            g->r[15] = cond(g, (w >> 8) & 15) ? pc + 4 + ((int32_t)(w << 24) >> 23) : pc + 2;
        else if ((w & 0xe000) == 0)
            thumb(g, 0, (w >> 11) & 3, (w >> 6) & 31, b, c);
        else if ((w & 0xe000) == 0x2000)
            thumb(g, 1, (w >> 11) & 3, a, w & 255, 0);
        else if ((w & 0xfc00) == 0x4000)
            thumb(g, 2, (w >> 6) & 15, b, c, 0);
        else if ((w & 0xfc00) == 0x4400)
            thumb(g, 3, (w >> 8) & 3, (w >> 3) & 15, (w & 7) | ((w >> 4) & 8), 0);
        else if ((w & 0xf800) == 0x4800) {
            g->r[a] = rd32(g, ((pc + 4) & ~3u) + (w & 255) * 4);
            g->r[15] += 2;
        } else if ((w & 0xf000) == 0x5000)
            thumb(g, 4, (w >> 9) & 7, (w >> 6) & 7, b, c);
        else if ((w & 0xe000) == 0x6000)
            thumb(g, 5, (w >> 11) & 3, (w >> 6) & 31, b, c);
        else if ((w & 0xf000) == 0x8000)
            thumb(g, 6, (w >> 11) & 1, (w >> 6) & 31, b, c);
        else if ((w & 0xf000) == 0x9000)
            thumb(g, 7, (w >> 11) & 1, a, (w & 255) * 4, 0);
        else if ((w & 0xf000) == 0xa000)
            thumb(g, 8, (w >> 11) & 1, a, (w & 255) * 4, 0);
        else if ((w & 0xff00) == 0xb000)
            thumb(g, 9, (w >> 7) & 1, (w & 127) * 4, 0, 0);
        else if ((w & 0xf600) == 0xb400)
            thumb(g, 10, (w >> 11) & 1, w & 255, (w >> 8) & 1, 0);
        else if ((w & 0xf000) == 0xc000)
            thumb(g, 11, (w >> 11) & 1, a, w & 255, 0);
        else {
            g->unsupported++;
            g->stopped = true;
        }
        return;
    }
    w = rd32(g, pc);
    if (!cond(g, w >> 28)) {
        g->r[15] += 4;
        return;
    }
    if ((w & 0x0ffffff0) == 0x012fff10) {
        u32 target = reg(g, w & 15);
        branch(g, target, target & 1);
    } else if ((w & 0x0f000000) == 0x0f000000) {
        g->r[15] += 4;
        bios(g, (w >> 16) & 255);
    } else if ((w & 0x0e000000) == 0x0a000000) {
        if (w & (1 << 24))
            g->r[14] = pc + 4;
        g->r[15] = pc + 8 + ((int32_t)(w << 8) >> 6);
    } else if ((w & 0x0e000000) == 0x08000000)
        arm_block(g, (w >> 24) & 1, (w >> 23) & 1, (w >> 22) & 1, (w >> 21) & 1, (w >> 20) & 1,
                  (w >> 16) & 15, w & 65535);
    else if ((w & 0x0f8000f0) == 0x00800090)
        arm_mul(g, 1, (w >> 22) & 1, (w >> 21) & 1, (w >> 20) & 1, (w >> 16) & 15, (w >> 12) & 15,
                (w >> 8) & 15, w & 15);
    else if ((w & 0x0fc000f0) == 0x00000090)
        arm_mul(g, 0, 0, (w >> 21) & 1, (w >> 20) & 1, (w >> 16) & 15, (w >> 12) & 15,
                (w >> 8) & 15, w & 15);
    else if ((w & 0x0fb00ff0) == 0x01000090) {
        u32 ad = reg(g, (w >> 16) & 15), v = reg(g, w & 15),
            old = w & (1 << 22) ? rd8(g, ad) : rd32(g, ad);
        if (w & (1 << 22))
            wr8(g, ad, v);
        else
            wr32(g, ad, v);
        g->r[(w >> 12) & 15] = old;
        g->r[15] += 4;
    } else if ((w & 0x0e000090) == 0x00000090)
        arm_half(g, (w >> 24) & 1, (w >> 23) & 1, (w >> 22) & 1, (w >> 21) & 1, (w >> 20) & 1,
                 (w >> 16) & 15, (w >> 12) & 15, ((w >> 4) & 240) | (w & 15), (w >> 5) & 3);
    else if ((w & 0x0fbf0fff) == 0x010f0000)
        arm_status(g, 0, (w >> 22) & 1, (w >> 12) & 15, 0);
    else if ((w & 0x0db0f000) == 0x0120f000)
        arm_status(g, 1, (w >> 22) & 1, (w >> 16) & 15, (w & 4095) | (((w >> 25) & 1) << 16));
    else if ((w & 0x0c000000) == 0x04000000)
        arm_mem(g, (w >> 25) & 1, (w >> 24) & 1, (w >> 23) & 1, (w >> 22) & 1, (w >> 21) & 1,
                (w >> 20) & 1, (w >> 16) & 15, (w >> 12) & 15, w & 4095);
    else if ((w & 0x0c000000) == 0)
        arm_dp(g, (w >> 25) & 1, (w >> 21) & 15, (w >> 20) & 1, (w >> 16) & 15, (w >> 12) & 15,
               w & 4095, 0, 0);
    else {
        g->unsupported++;
        g->stopped = true;
    }
}
void dispatch(GBA *g) {
    if (g->in_irq && g->r[15] == 0x138) {
        g->bank_sp[g->cpsr & 31] = g->r[13];
        g->bank_lr[g->cpsr & 31] = g->r[14];
        for (unsigned i = 0; i < 16; i++)
            g->r[i] = g->irq_regs[i];
        g->cpsr = g->irq_cpsr;
        g->in_irq = false;
        return;
    }
    uint64_t before = g->instructions;
    u32 entry = g->r[15];
    if (generated_dispatch(g) && (g->instructions != before || entry != g->r[15]))
        return;
    // Log unique unknown execution entries, without storing code or data.
    static u32 seen[65536];
    u32 key = g->r[15] | ((g->cpsr & 32) ? 1 : 0), slot = (key * 2654435761u) >> 16;
    unsigned probes = 0;
    while (seen[slot] && seen[slot] != key + 1 && probes++ < 65536)
        slot = (slot + 1) & 65535;
    if (!seen[slot]) {
        seen[slot] = key + 1;
        g->unknown_count++;
        if (g->unknown) {
            fprintf(g->unknown, "%08x\n", key);
        }
    }

    fallback(g);
}
bool tick(GBA *g) {
    if (g->quota <= 0 || g->stopped)
        return false;
    u32 pc = g->r[15];
    irq_check(g);
    if (g->r[15] != pc)
        return false;
    if (g->coverage) coverage_pc(g);
    g->quota--;
    g->instructions++;
    if (g->trace) {
        static FILE *f;
        if (!f)
            f = fopen("build/trace.log", "w");
        if (f) {
            fprintf(f, "%08x %08x", g->r[15], g->cpsr);
            for (unsigned i = 0; i < 15; i++)
                fprintf(f, " %08x", g->r[i]);
            fprintf(f, "\n");
        }
    }
    hardware_advance(g, 3);
    return true;
}
void bios(GBA *g, unsigned n) {
    if (g->coverage) coverage_bios_source(g, n);
    if (n == 0x0b || n == 0x0c) {
        u32 src = g->r[0], dst = g->r[1], cnt = g->r[2] & 0x1fffff;
        bool word = n == 0xc || (g->r[2] & (1 << 26)), fill = g->r[2] & (1 << 24);
        if (n == 0xc)
            cnt = (cnt + 7) & ~7u;
        unsigned stride = word ? 4 : 2;
        src &= ~(stride - 1);
        dst &= ~(stride - 1);
        if (g->coverage) coverage_transfer(g, n, src, dst, (fill ? 1 : cnt) * stride);
        for (u32 i = 0; i < cnt; i++) {
            if (word)
                wr32(g, dst, rd32(g, src));
            else
                wr16(g, dst, rd16(g, src));
            dst += stride;
            if (!fill)
                src += stride;
        }
        return;
    }
    if (n == 2 || n == 3 || n == 4 || n == 5) {
        g->halted = true;
        return;
    }
    if (n == 6 || n == 7) {
        int32_t a = g->r[n == 6 ? 0 : 1], b = g->r[n == 6 ? 1 : 0];
        if (b) {
            g->r[0] = (a == INT_MIN && b == -1) ? INT_MIN : a / b;
            g->r[1] = (a == INT_MIN && b == -1) ? 0 : a % b;
            g->r[3] = g->r[0] & N ? 0 - g->r[0] : g->r[0];
        }
        return;
    }
    if (n == 8) {
        u32 v = g->r[0], r = 0;
        for (u32 bit = 1u << 30; bit; bit >>= 2) {
            if (v >= r + bit) {
                v -= r + bit;
                r = (r >> 1) + bit;
            } else
                r >>= 1;
        }
        g->r[0] = r;
        return;
    }
    fprintf(stderr, "Unsupported BIOS service %02x at %08x\n", n, g->r[15]);
    g->unsupported++;
    g->stopped = true;
}
