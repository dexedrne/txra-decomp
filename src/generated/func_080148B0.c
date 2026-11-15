/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Multi-player serial control as two halfwords: control bits, then send data. */
typedef struct {
    u16 baud:2, si:1, sd:1, id:2, error:1, enable:1, unused8:4, mode:2, irq:1, unused15:1;
    u16 data;
} SioMultiCnt;
extern void func_08014988(u32);
extern u32 func_080149FC(u8 *);
u32 func_080148B0(u32 send, u8 *out)
{
    TxraLinkState *s = &g_03007A30;
    switch (s->field_01) {
    case 0: {
        SioMultiCnt *reg = (SioMultiCnt *)0x04000128;
        SioMultiCnt sio = *reg;
        if (sio.id == 0) {
            if (sio.sd != 1 || sio.enable != 0) goto done;
            if (sio.si == 0 && s->field_14 == -1) {
                *(vu16 *)0x04000208 = 0;
                *(vu16 *)0x04000200 &= 0xFF7F;
                *(vu16 *)0x04000200 |= 0x40;
                *(vu16 *)0x04000208 = 1;
                reg->irq = 0;
                *(vu16 *)0x04000202 = 0xC0;
                *(vu32 *)0x0400010C = 0xB1FC;
                s->field_00 = 8;
            }
        }
        g_03007A30.field_01 = 1;
    }
    case 1:
        func_080149FC(out);
        func_08014988(send);
        break;
    }
done:
    g_03007A30.field_0b++;
    {
        u16 lo = g_03007A30.field_03;
        u16 hi = g_03007A30.field_02 << 8;
        u16 result;
        if (g_03007A30.field_00 == 8) result = 0x80 | hi | lo;
        else result = lo | hi;
        return result;
    }
}
