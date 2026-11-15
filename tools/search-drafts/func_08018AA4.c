void func_08018AA4(u32 source, u32 dest, u16 count)
{
    u16 ime = *(vu16 *)0x04000208;
    u16 wait;
    *(vu16 *)0x04000208 = 0;
    wait = *(vu16 *)0x04000204;
    wait &= 0xF8FF;
    wait |= gEepromGeometry->wait_control;
    *(vu16 *)0x04000204 = wait;
    *(vu32 *)0x040000D4 = source;
    *(vu32 *)0x040000D8 = dest;
    *(vu32 *)0x040000DC = count | 0x80000000;
    while (*(vu16 *)0x040000DE & 0x8000) {}
    *(vu16 *)0x04000208 = ime;
}
