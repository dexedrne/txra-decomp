extern u32 g_03000DE4;
extern u16 g_03000B54[];
extern void func_0800761C(u32, u32);
void func_0801604C(u32 value, u32 index)
{
    if (g_03000DE4 == 1) {
        g_03000B54[index] = value;
        func_0800761C(value, index);
    }
}
