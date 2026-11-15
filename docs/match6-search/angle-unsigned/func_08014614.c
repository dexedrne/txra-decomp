u16 func_08014614(u32 a, u32 b)
{
    s16 result;
    if ((s32)b >= (s32)a) {
        if ((s32)b <= (s32)(a + 8192)) {
 result = b - a;
 goto done;
 }
    }
    if ((s32)a >= (s32)b) {
        if ((s32)a < (s32)(b + 8192)) {
 result = b - a;
 goto done;
 }
    }
    if ((s32)b > (s32)(a + 8192)) result = b - 16384 - a;
    else if ((s32)b > (s32)(a - 8192)) result = 0;
    else result = b - (a - 16384);
done:
    return result;
}
