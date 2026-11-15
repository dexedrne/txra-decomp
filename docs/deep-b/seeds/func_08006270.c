/* Unmatched source hypothesis; excluded from the build. */
extern u32 g_03006A88[],g_03006890[],g_030075E8[],g_030079D0[];
extern u32 g_03006A98,g_0300757C,g_03006A80;
extern s8 g_03007600[];
void func_08006270(u32 channel)
{
 u32 source=g_03006A88[channel];
 u32 bank;
 if(source){
  if(!g_03006890[channel]){
   if(!g_030075E8[channel]) source=g_03006A88[channel]=0;
   else {
    g_03006A88[channel]=g_083B8378[g_030079D0[channel]].field_00;
    g_03006890[channel]=g_083B8378[g_030079D0[channel]].field_04-1;
    source=g_03006A88[channel];
   }
  }else g_03006890[channel]--;
 }
 bank=(g_03006A98+1)&1;
 if(!channel){
  u32 cursor;
  s8 *dest;
  s32 left;
  if(!source)return;
  cursor=g_0300757C;
  dest=g_03007600+176*bank;
  left=175;
  do{
   *dest=*(u8 *)(source+((s32)cursor>>4));
   cursor+=g_03006A80;
   if(cursor>=((u32 *)&g_083B8378[g_030079D0[0]])[4])cursor=0;
   dest++;left--;
  }while(left>=0);
  g_0300757C=cursor;
  g_03006890[0]=4;
 }else{
  s8 *dest=g_03007600+176*bank;
  s32 left=175;
  if(source){
   do{ s32 value=*dest+*(s8 *)source;source++;*dest=value>>1;dest++;left--; }while(left>=0);
  }else{
   do{*dest=*dest>>1;dest++;left--;}while(left>=0);
  }
 }
 g_03006A88[channel]=source;
}
