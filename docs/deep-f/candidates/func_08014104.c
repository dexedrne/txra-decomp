/* Unmatched deep-f hypothesis; excluded from the ROM build. */
extern volatile u32 g_03005FC0;
extern u16 g_02003C00[],g_0832F29C[];
// s32 s32 for 
void func_08014104(void){ u32 unused=g_03005FC0; s32 width=120; s32 height=48; u8 *db=(u8*)g_02003C00; u8 *sb=(u8*)g_0832F29C; s32 y; s32 x; for(y=0;y<height;y++){ for(x=0;x<width;x++){ u16 *d=(u16*)(db+y*240); u16 *s=(u16*)(sb+y*240); u32 value=s[x]; if(value){ if(!(value&255)) d[x]=(d[x] & 255)+value; else if(!(value&65280)) d[x]=(d[x] & 65280)+value; else d[x]=value; } } } }
