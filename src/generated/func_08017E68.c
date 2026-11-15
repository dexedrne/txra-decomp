/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
typedef struct DeepPending { u8 unknown_00[26]; u16 kind; struct DeepPending *next; } DeepPending;
extern u32 g_03005F4C;
extern DeepPending *g_03000670[], *g_030021C4;
extern void (*g_083E2284)(void), (*g_083E2288)(void), (*g_083E228C)(void), (*g_083E2290)(void);
void func_08017E68(void)
{
    s32 i;
    g_03005F4C = 0;
    for (i = 255; i >= 0; ) {
        DeepPending *pending = g_03000670[i];
        s32 next = i - 1;
        if (pending) {
            g_03000670[i] = 0;
            do {
                g_030021C4 = pending;
                g_03005F4C++;
                if (pending->kind == 0) g_083E2284();
                else if (pending->kind == 1) g_083E2288();
                else if (pending->kind == 2) g_083E228C();
                else g_083E2290();
                pending = g_030021C4->next;
            } while (pending);
        }
        i = next;
    }
}
