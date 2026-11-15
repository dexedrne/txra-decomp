extern u16 func_08018BD4(u16, u16 *);
extern u16 func_08018D48(u16, u16 *);
u16 func_08018DA0(u16 index, u16 *source)
{
    u8 attempt;
    u16 result;
    for (attempt = 0; attempt < 3; attempt++) {
        result = func_08018BD4(index, source);
        if (result != 0) continue;
        result = func_08018D48(index, source);
        if (result == 0) break;
    }
    return result;
}
