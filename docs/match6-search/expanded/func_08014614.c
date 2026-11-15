s32 func_08014614(s32 a, s32 b)
{
    u16 result;
    if (b >= a) {
        if (b <= a + 8192) {
 result = b - a;
 goto done;
 }
    }
    if (a >= b) {
        if (a < b + 8192) {
 result = b - a;
 goto done;
 }
    }
    if (b > a + 8192) result = b - 16384 - a;
    else if (b > a - 8192) result = 0;
    else result = b - (a - 16384);
done:
    return result;
}
