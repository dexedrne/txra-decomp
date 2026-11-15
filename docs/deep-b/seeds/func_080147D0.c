/* Unmatched source hypothesis; excluded from the build. */
extern void func_08018A58(const void *,void *,u32);
void func_080147D0(void)
{
 u32 zero;
 u32 state;
 u32 i;
 u32 tail,offset;
 u8 **first, **second;
 u32 firstbase,secondbase;
 *(vu16 *)0x04000208=0;
 *(vu16 *)0x04000200 &= 0xFF3F;
 *(vu16 *)0x04000208=1;
 *(vu16 *)0x04000134=0;
 *(vu32 *)0x04000128=0x2000;
 *(vu16 *)0x04000128 |= 0x4003;
 zero=0;
 state=(u32)&g_03007A30;
 func_08018A58(&zero,(void *)state,0x05000048);
 *(s32 *)(state+20)=-1;
 *(u8 **)(state+40)=(u8 *)state+96;
 *(u8 **)(state+44)=(u8 *)state+120;
 i=0;
 tail=(u32)state+192;
 offset=0;
 first=(u8 **)(state+48);
 firstbase=(u32)state+144;
 secondbase=(u32)state+168;
 second=(u8 **)(state+64);
 do {
  u32 index=i<<2;
  *first++=(u8 *)(offset+firstbase);
  *second++=(u8 *)(offset+secondbase);
  *(u32 *)(index+(state+80))=tail;
  tail+=72;
  offset+=72;
  i++;
 }while((s32)i<=1);
 *(vu16 *)0x04000208=0;
 *(vu16 *)0x04000200 |= 128;
 *(vu16 *)0x04000208=1;
}
