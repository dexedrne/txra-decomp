/* Unmatched source hypothesis; excluded from the ROM build. */
#include "types.h"
extern u32 g_03007A34;
extern void func_08018A58(const void *,void *,u32);
u32 func_080149FC(u8 *out) {
 u32 received[2];
 u32 zero;
 s32 i;
 u32 j,sum;
 u16 *p;
 u8 **q;
 u8 *ready;
 u32 *word;
 TxraLinkState *state;
 received[0]=0;
 *(vu16*)0x04000208=0;
 word=&g_03007A34;
 ready=(u8*)&received[1];
 q=(u8**)((u8*)word+60);
 for(i=3;i>=0;i--) {
  u8 *temp=q[4];
  q[4]=*q;
  *q++=temp;
 }
 received[1]=*word;
 *word=0;
 *(vu16*)0x04000208=1;
 state=(TxraLinkState*)(word-1);
 state->field_03=0;
 for(i=0;i<=1;i++) {
  sum=0;
  j=0;
  p=(u16*)state->field_50[i];
  do{sum+=*p++; j++;}while(j<=9);
  if(ready[i] && (s16)sum==-1) {
   func_08018A58(state->field_50[i]+4,out+(i<<4),0x04000004);
   state->field_03|=1<<i;
  }
  zero=0;
  func_08018A58(&zero,state->field_50[i]+4,0x05000004);
 }
 g_03007A30.field_02|=g_03007A30.field_03;
 return g_03007A30.field_03;
}
