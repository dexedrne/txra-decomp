extern u16 *g_03007B50;
extern void func_08018AA4(void *, void *, u16);
u16 func_08018BE8(u16 address, u16 *source, u8 wait)
{
    u16 buffer[82];
    volatile u16 ready, previous, current;
    volatile u32 elapsed;
    u16 *p;
    u8 i, j;
    u16 value;
    u16 status;
    u32 offset;
    if (address >= g_03007B50[2]) return 0x80FF;
    offset = *((u8 *)g_03007B50 + 8) * 2;
    p = (u16 *)(offset + (u32)buffer);
    p += 66;
    *p-- = 0;
    for (i = 0; i < 4; i++) {
        value = *source++;
        for (j = 0; j < 16; j++) {
            *p-- = value;
            value >>= 1;
        }
    }
    for (i = 0; i < *((u8 *)g_03007B50 + 8); i++) {
        *p-- = address;
        address >>= 1;
    }
    *p-- = 0;
    *p = 1;
    func_08018AA4(buffer, (void *)0x0D000000, *((u8 *)g_03007B50 + 8) + 67);
    status = 0;
    ready = 0;
    previous = *(vu16 *)0x04000006;
    elapsed = 0;
    for (;;) {
        while (ready || !(*(vu16 *)0x0D000000 & 1)) {
            current = *(vu16 *)0x04000006;
            if (current != previous) {
                if (current > previous) elapsed += current - previous;
                else elapsed += current + 228 - previous;
                if (elapsed > 136) {
                    if (!ready && !(*(vu16 *)0x0D000000 & 1)) status = 0xC001;
                    goto done;
                }
                previous = current;
            }
        }
        ready++;
        if (!wait) break;
    }
done:
    return status;
}
