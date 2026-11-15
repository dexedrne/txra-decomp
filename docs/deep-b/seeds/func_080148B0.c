/* Unmatched source hypothesis; excluded from the build. */
extern void func_08014988(u32);
extern u32 func_080149FC(u32);
u32 func_080148B0(u32 source,u32 dest)
{
 TxraLinkState *state=&g_03007A30;
 u32 status,mask,work,bits;
 vu32 *serial;
 switch(state->field_01){
 case 0:
  serial=(vu32 *)0x04000128;
  status=*serial;
  bits=0x30;work=status;work&=bits;
  if(work) goto begin;
  work=0x88;mask=status;mask&=work;
  if(mask!=8) break;
  status=(u8)(status&4);
  if(status) goto begin;
  if(state->field_14!=-1) goto begin;
  *(vu16 *)0x04000208=status;
  *(vu16 *)0x04000200 &= 0xFF7F;
  *(vu16 *)0x04000200 |= 0x40;
  *(vu16 *)0x04000208=1;
  { u32 value=((vu8 *)serial)[1];u32 clear=65;clear=-clear;clear&=value;((vu8 *)serial)[1]=clear; }
  *(vu16 *)0x04000202=0xC0;
  *(vu32 *)0x0400010C=0xB1FC;
  state->field_00=mask;
 begin:
  g_03007A30.field_01=1;
 case 1:
  func_080149FC(dest);
  func_08014988(source);
 }
 g_03007A30.field_0b++;
 {
  u32 low=g_03007A30.field_03;
  u32 high=g_03007A30.field_02<<8;
  u32 result;
  if(g_03007A30.field_00==8) {result=128;result|=high;result|=low;}
  else {result=low;result|=high;}
  return result;
 }
}
