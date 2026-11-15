/* Unmatched 11/3 draft (87 aligned lines, 592 of 604 bytes; ARM profile): frame order fixed (width, height, source) and the row base taken once per row; the original keeps four inner-loop induction pointers, reloads the source pixel through src+col*2 plus row*200, and spills the next-row index. Excluded from the build. */
extern u32 g_03005FC0;
extern s16 g_03001E50;
extern u8 g_08327BDC[],g_08327C1C[],g_08327C5C[],g_0832BA5C[],g_0832BA9C[],g_0832BAE4[];
#define DEEP_PIXEL(offset) \
    value=*(u16 *)(source+row*200+column*2+(offset)); \
    if(value) { \
        if(!(value&255)) *(u16 *)(dest+row*240+column*2+(offset))=*(u8 *)(dest+row*240+column*2+(offset))+value; \
        else if(!(value&0xFF00)) *(u16 *)(dest+row*240+column*2+(offset))=(*(u16 *)(dest+row*240+column*2+(offset))&0xFF00)+value; \
        else *(u16 *)(dest+row*240+column*2+(offset))=value; }
void func_08017F64(void)
{
    s32 width,height;
    u8 *source;
    u8 *dest;
    s32 row,column;
    s32 mode;
    u16 value;
    if (!g_03005FC0) dest=(u8 *)0x0600A000;
    else dest=(u8 *)0x06000000;
    mode=g_03001E50;
    if(mode==0){width=25;height=72;dest+=0x4EC8;source=g_08327BDC;}
    if(mode==1){width=25;height=80;dest+=0x4B08;source=g_08327C1C;}
    if(mode==2){width=32;height=64;dest+=0x5280;source=g_08327C5C;}
    if(mode==3){width=29;height=66;dest+=0x5194;source=g_0832BA5C;}
    if(mode==4){width=34;height=48;dest+=0x5A02;source=g_0832BA9C;}
    if(mode==5){width=32;height=64;dest+=0x5282;source=g_0832BAE4;}
    for(row=0;row<height;) {
        s32 next=row+1;
        for(column=0;column<width;column+=2) {
            value=((u16 *)(source+row*200))[column];
            if(value) {
                if(!(value&255)) *(u16 *)(dest+row*240+column*2)=*(u8 *)&*(u16 *)(dest+row*240+column*2)+value;
                else if(!(value&0xFF00)) *(u16 *)(dest+row*240+column*2)=(*(u16 *)(dest+row*240+column*2)&0xFF00)+value;
                else *(u16 *)(dest+row*240+column*2)=value; }
            value=((u16 *)(source+row*200))[column+1];
            if(value) {
                if(!(value&255)) *(u16 *)(dest+row*240+column*2+2)=*(u8 *)&*(u16 *)(dest+row*240+column*2+2)+value;
                else if(!(value&0xFF00)) *(u16 *)(dest+row*240+column*2+2)=(*(u16 *)(dest+row*240+column*2+2)&0xFF00)+value;
                else *(u16 *)(dest+row*240+column*2+2)=value; }
        }
        row=next;
    }
}
