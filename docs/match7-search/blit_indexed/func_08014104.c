extern volatile u32 g_03005FC0; extern u16 g_02003C00[],g_0832F29C[]; void func_08014104(void){u32 unused=g_03005FC0; u32 width=120; s32 height=48; s32 y;u16 *destbase=g_02003C00; u16 *sourcebase=g_0832F29C;y=0;do{s32 nextrow=y+1;u16 *dest=destbase+(y*120); u16 *source=sourcebase+(y*120); u32 x;for(x=0;x<width;x++){u32 value = *source;
if(value) {
 if(!(value&255)) *dest=(*dest & 255)+value;
 else if(!(value&65280)) *dest=(*dest & 65280)+value;
 else *dest=value;
}
dest++; source++;}y=nextrow;}while(y<height);}