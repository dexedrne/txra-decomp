/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
void func_080063D4(void) {
    u32 bank, offset, *p;
    s32 i;
    bank = (*(u32 *)0x03006A98 + 1) & 1;
    *(u32 *)0x03006A98 = bank;
    *(vu32 *)0x04000100 = 0;
    *(vu32 *)0x040000C4 = 0;
    *(vu32 *)0x040000C0 = 0x040000A0;
    offset = 176 * bank;
    *(vu32 *)0x040000BC = 0x03007410 + offset;
    *(vu32 *)0x04000100 = 0x80F9C4;
    *(vu32 *)0x040000C4 = 0xBE400000;
    *(vu32 *)0x040000C4;
    *(vu32 *)0x04000104 = 0;
    *(vu32 *)0x040000D0 = 0;
    *(vu32 *)0x040000CC = 0x040000A4;
    *(vu32 *)0x040000C8 = 0x03007600 + offset;
    *(vu32 *)0x04000104 = 0x80F99D;
    *(vu32 *)0x040000D0 = 0xBE400000;
    *(vu32 *)0x040000D0;
    bank = (bank + 1) & 1;
    p = (u32 *)(0x03007410 + 176 * bank);
    for (i=43;i>=0;i--) *p++ = 0;
    p = (u32 *)(0x03007600 + 176 * bank);
    for (i=43;i>=0;i--) *p++ = 0;
}
