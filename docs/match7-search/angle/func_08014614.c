s32 func_08014614(s32 a, s32 b)
{
    s32 result;
    if (b >= a) {
        if (b <= a + 8192) {
 return b - a;
 }
    }
    if (a >= b) {
        if (a < b + 8192) {
 return b - a;
 }
    }
    if (b > a + 8192) result = b - (a + 16384);
    else if (b > a - 8192) result = 0;
    else result = b + 16384 - a;
done:
    return result;
}
