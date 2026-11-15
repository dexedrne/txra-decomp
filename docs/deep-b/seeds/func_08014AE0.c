/* Unmatched source hypothesis; excluded from the build. */
void func_08014AE0(void)
{
 unsigned long long incoming=*(volatile unsigned long long *)0x04000120;
 TxraLinkState *state=&g_03007A30;
 s32 phase=state->field_14;
 s32 *count;
 u16 *input;
 s32 i;
 u32 offset;
 if(phase==-1){
  u8 *swap;
  *(vu16 *)0x0400012A=0xFEFE;
  swap=state->field_2c;
  state->field_2c=state->field_28;
  state->field_28=swap;
 }else if(phase>=0){
  *(vu16 *)0x0400012A=((u16 *)state->field_2c)[phase];
 }
 if(state->field_14<=10) state->field_14++;
 i=0;offset=0;
 count=(s32 *)((u8 *)state+24);
 input=(u16 *)&incoming;
 do {
  u32 index=i<<2;
  if(*input==0xFEFE && *count>9){*count=-1;}
  else{
   u8 **slot=(u8 **)(offset+(u32)state+48);
   s32 at=*count;
   u8 *buffer=*slot;
   ((u16 *)buffer)[at]=*input;
   if(at==9){
    u8 **other=(u8 **)(index+(u32)state+64);
    u8 *swap=*other;
    *other=buffer;
    *slot=swap;
    *((u8 *)state+4+i)=1;
   }
  }
  if(*count<=10) ++*count;
  offset+=4;count++;input++;i++;
 }while(i<=1);
 if(state->field_00==8){
  *(vu16 *)0x0400010E=0;
  *(vu16 *)0x04000128|=128;
  *(vu16 *)0x0400010E=192;
 }
}
