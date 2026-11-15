/* Isolated compiler experiment, not a replacement for the enclosing function. */
extern s32 g_03002A18,g_03001B28,g_03000DF8,g_03005F58;
void deep_rotation_probe(s32 *out,s32 x,s32 y,s32 z)
{
    s32 xx=(x*g_03002A18-z*g_03001B28)>>12;
    s32 zz=(x*g_03001B28+z*g_03002A18)>>12;
    out[0]=xx;
    out[1]=(y*g_03000DF8-zz*g_03005F58)>>12;
    out[2]=(y*g_03005F58+zz*g_03000DF8)>>12;
}
