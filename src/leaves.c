/* Small independently matched routines. Addresses are temporary names. */
typedef unsigned int u32;
#define WORD(address) (*(volatile u32 *)(address))
void func_08014518(void) { WORD(0x03002184) = 0; }
u32 func_080147C0(void) { return (WORD(0x04000128) & 0x30) >> 4; }
void func_08015DA4(void) { }
void func_0800D188(u32 value) {
    WORD(0x030014c0) = value;
    WORD(0x030014a4) += value;
}
