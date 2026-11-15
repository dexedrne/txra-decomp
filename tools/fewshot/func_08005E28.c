#include "types.h"
extern u8 g_03005FE0[];
extern u16 func_08018BD4(u16,u8 *),func_08018D48(u16,u8 *);
u32 func_08005E28(void)
{
    u32 result=0;
    s32 failures=0;
    u8 *p=g_03005FE0;
    s32 block;
    for(block=0;(s32)block<=63;block++) {
retry:
        if((s32)failures>512) {result=1;break;}
        if(func_08018BD4(block,p)) {failures++;goto retry;}
        if(func_08018D48(block,p)) {failures++;goto retry;}
        p+=8;
    }
    return result;
}
