void func_0801251C(u8 *base, u8 *dest, u32 size)
{
    u8 *out = dest + size - 1;
    u32 start = ((base[5] << 8) | base[4]) + 3;
    u32 mask = 192;
    u32 lengthmask = 63;
    u8 *in = base + start;
    do {
        u32 tag = *in;
        if ((tag & mask) == 192) {
            u32 count = tag & lengthmask;
            u32 offset;
            u8 *copy;
            in--;
            offset = *in << 8;
            in--;
            offset |= *in;
            in--;
            copy = dest + offset;
            if (count) do {
                *out = *copy;
                out--;
                copy++;
                count--;
            } while (count);
        }
        if ((tag & mask) == 128) {
            u32 count = tag & lengthmask;
            u32 offset;
            u8 *copy;
            in--;
            offset = *in << 8;
            in--;
            offset |= *in;
            in--;
            copy = dest + offset + count - 1;
            if (count) do {
                *out = *copy;
                out--;
                copy--;
                count--;
            } while (count);
        }
        if ((tag & mask) == 64) {
            u32 count = tag & lengthmask;
            u32 value;
            in--;
            value = *in;
            in--;
            if (count) do {
                *out = value;
                out--;
                count--;
            } while (count);
        }
        if ((tag & mask) == 0) {
            u32 count = tag;
            in--;
            if (count) do {
                *out = *in;
                in--;
                out--;
                count--;
            } while (count);
        }
    } while ((s32)in > (s32)base && (s32)out > (s32)dest);
}
