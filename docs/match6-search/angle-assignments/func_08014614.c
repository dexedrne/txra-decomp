s32 func_08014614(s32 a, s32 b)
{
    if (b >= a && b <= a + 8192) return b-a;
    if (a >= b && a < b + 8192) return b-a;
    if (b > a + 8192) return b - 16384 - a;
    if (b > a - 8192) return 0;
    a-=16384; b-=a; return b;
}
