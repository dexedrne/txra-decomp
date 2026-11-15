/* Freestanding i386 harness: maps GBA-addressed regions at their real addresses,
   reads a synthetic state from stdin, runs func_080064A4 for N frames and writes
   the regions plus a call log back to stdout.  No libc, no ROM bytes. */
typedef unsigned int u32;
typedef int s32;
extern void func_080064A4(void);

static long sys(long n, long a, long b, long c, long d, long e, long f) {
    long r;
    __asm__ volatile("push %%ebp\n\tmov %7, %%ebp\n\tint $0x80\n\tpop %%ebp"
                     : "=a"(r) : "a"(n), "b"(a), "c"(b), "d"(c), "S"(d), "D"(e), "g"(f) : "memory");
    return r;
}
static void die(int code) { sys(1, code, 0, 0, 0, 0, 0); for (;;) {} }
static void readall(char *p, long n) {
    while (n > 0) { long r = sys(3, 0, (long)p, n, 0, 0, 0); if (r <= 0) die(3); p += r; n -= r; }
}
static void writeall(const char *p, long n) {
    while (n > 0) { long r = sys(4, 1, (long)p, n, 0, 0, 0); if (r <= 0) die(4); p += r; n -= r; }
}
struct region { u32 base, size; };
static const struct region regions[] = {
    {0x02000000, 0x10000}, {0x03000000, 0x8000}, {0x04000000, 0x1000},
    {0x0801F000, 0x1000}, {0x08332000, 0x92000},
};
#define NREG (sizeof(regions) / sizeof(regions[0]))
static u32 log_[64];
static u32 nlog;
static void note(u32 v) { if (nlog < 64) log_[nlog++] = v; }
static void hook_mix(s32 n) { note(0x1000 + (u32)n); }
static void hook_channel(s32 n) { note(0x2000 + (u32)n); }
void func_08005F8C(s32 n) { note(0x3000 + (u32)n); }

void _start(void) {
    unsigned i;
    u32 frames;
    for (i = 0; i < NREG; i++) {
        long r = sys(192, regions[i].base, regions[i].size, 3, 0x32 /* MAP_PRIVATE|FIXED|ANON */, -1, 0);
        if (r != (long)regions[i].base) die(10 + i);
    }
    readall((char *)&frames, 4);
    for (i = 0; i < NREG; i++) readall((char *)regions[i].base, regions[i].size);
    *(u32 *)0x08332E9C = (u32)hook_mix;
    *(u32 *)0x08332EA0 = (u32)hook_channel;
    for (i = 0; i < frames; i++) { note(0xF000 + i); func_080064A4(); }
    *(u32 *)0x08332E9C = 0;
    *(u32 *)0x08332EA0 = 0;
    for (i = 0; i < NREG; i++) writeall((const char *)regions[i].base, regions[i].size);
    writeall((const char *)&nlog, 4);
    writeall((const char *)log_, sizeof(log_));
    die(0);
}
