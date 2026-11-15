s32 func_08014614(s32 a, s32 b)
{
    if (b >= a && b <= a + 8192) {return b-a;}
    if (a >= b && a < b + 8192) {b-=a; return b;}
    if (b > a + 8192) b-=a; b-=16384; return b;
    if (b > a - 8192) return 0;
    return b - (a - 16384);
}
