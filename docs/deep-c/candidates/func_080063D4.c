/* Unmatched source hypothesis; excluded from the ROM build. */
extern u32 g_03006A98;
extern u32 g_03007410[2][44],g_03007600[2][44];
void func_080063D4(void) {
 u16 active;
 s32 i,j;
 u32 *p,*q;
 active=g_03006A98;
 active+=1;
 active&=1;
 g_03006A98=active;
 *(vu32*)0x04000100=0;
 *(vu32*)0x040000C4=0;
 *(vu32*)0x040000C0=0x040000A0;
 *(vu32*)0x040000BC=(u32)g_03007410[active];
 *(vu32*)0x04000100=0x0080F9C4;
 *(vu32*)0x040000C4=0xBE400000;
 *(vu32*)0x040000C4;
 *(vu32*)0x04000104=0;
 *(vu32*)0x040000D0=0;
 *(vu32*)0x040000CC=0x040000A4;
 *(vu32*)0x040000C8=(u32)g_03007600[active];
 *(vu32*)0x04000104=0x0080F99D;
 *(vu32*)0x040000D0=0xBE400000;
 *(vu32*)0x040000D0;
 active=(active+1)&1;
 p=g_03007410[active];
 for(i=43;i>=0;i--) *p++=0;
 q=g_03007600[active];
 for(j=43;j>=0;j--) *q++=0;
}
