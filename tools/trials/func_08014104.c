extern volatile u32 g_03005FC0;
extern u16 g_02003C00[],g_0832F29C[];
void func_08014104(void){
 u32 unused=g_03005FC0;u32 width=120;s32 height=48;
 u32 destbase=(u32)g_02003C00;u32 sourcebase=(u32)g_0832F29C;
 s32 y=0;
 do {s32 nextrow=y+1;
 if(width){s32 offset=y*240;u32 dest=(u32)(destbase+offset);u32 source=(u32)(sourcebase+offset);u32 left=width;
 do {u32 value=*(u16 *)source;
 if(value){
 if(!(value&255)) *(u16 *)dest=(*(u16 *)dest & 255)+value;
 else if(!(value&65280)) *(u16 *)dest=(*(u16 *)dest & 65280)+value;
 else *(u16 *)dest=value;
 }
 dest+=2;source+=2;left--;
 }while(left);}
 y=nextrow;
 }while(y<height);
}
