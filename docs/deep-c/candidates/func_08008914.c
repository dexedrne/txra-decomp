/* Unmatched source hypothesis; excluded from the ROM build. */
void func_08008914(s32 x,s32 y,s32 width,s32 height,s32 dx,s32 dy,s32 flip,s32 ox,s32 oy) {
 s32 sy,sx;
 x+=ox;y+=oy;
 if(!flip) {
  for(sy=y;sy<y+height;sy++) {
   for(sx=x;sx<x+width;sx++) {
    u32 pixel=*(u16*)(0x02000000+(sy<<8)+((sx>>1)<<1));
    if(sx&1)pixel>>=8;
    pixel&=255;
    if(!(dx&1)) {
     if(pixel) {
      u16 *dst=(u16*)(0x02000000+(dy<<8)+((dx>>1)<<1));
      *dst=(*dst&0xFF00)|pixel;
     }
    } else {
     if(pixel) {
      u16 *dst=(u16*)(0x02000000+(dy<<8)+((dx>>1)<<1));
      *dst=(*dst&255)|(pixel<<8);
     }
    }
    dx++;
   }
   dx-=width;dy++;
  }
 } else {
  for(sy=y;sy<y+height;sy++) {
   for(sx=x+width-1;sx>=x;sx--) {
    u32 pixel=*(u16*)(0x02000000+(sy<<8)+((sx>>1)<<1));
    if(sx&1)pixel>>=8;
    pixel&=255;
    if(!(dx&1)) {
     if(pixel) {
      u16 *dst=(u16*)(0x02000000+(dy<<8)+((dx>>1)<<1));
      *dst=(*dst&0xFF00)|pixel;
     }
    } else {
     if(pixel) {
      u16 *dst=(u16*)(0x02000000+(dy<<8)+((dx>>1)<<1));
      *dst=(*dst&255)|(pixel<<8);
     }
    }
    dx++;
   }
   dx-=width;dy++;
  }
 }
}
