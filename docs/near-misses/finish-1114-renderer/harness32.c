/* Freestanding i386 harness: maps synthetic EWRAM/IWRAM/table at their GBA
 * addresses, reads the memory image from stdin, runs the candidate, writes the
 * image to stdout.  No ROM data is involved; all contents are synthetic. */
typedef unsigned int u32;
void func_08016DA8(void);
static int sys3(int n, int a, int b, int c) {
    int r;
    __asm__ volatile ("int $0x80" : "=a"(r) : "a"(n), "b"(a), "c"(b), "d"(c) : "memory");
    return r;
}
static int sys1(int n, int a) {
    int r;
    __asm__ volatile ("int $0x80" : "=a"(r) : "a"(n), "b"(a) : "memory");
    return r;
}
static void map(u32 addr, u32 len) {
    u32 args[6] = { addr, len, 3, 0x32 /* PRIVATE|ANON|FIXED */, (u32)-1, 0 };
    if ((u32)sys1(90, (int)args) != addr) sys1(1, 3);
}
static void io(int n, int fd, u32 addr, u32 len) {
    while (len) {
        int r = sys3(n, fd, (int)addr, (int)len);
        if (r <= 0) sys1(1, 4);
        addr += r; len -= r;
    }
}
void _start(void) {
    static const u32 regions[3][2] = {{0x02000000, 0x40000}, {0x03000000, 0x8000}, {0x07F00000, 0x300000}};
    int i;
    for (i = 0; i < 3; i++) map(regions[i][0], regions[i][1]);
    for (i = 0; i < 3; i++) io(3, 0, regions[i][0], regions[i][1]);
    func_08016DA8();
    for (i = 0; i < 3; i++) io(4, 1, regions[i][0], regions[i][1]);
    sys1(1, 0);
}
