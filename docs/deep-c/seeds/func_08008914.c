/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
static inline void copy_pixel(s32 x, s32 dx, u32 source_row, u32 dest_row) {
    u16 *p=(u16 *)(source_row+((x>>1)<<1));
    u32 value=*p;
    if(x&1) value>>=8;
    value &=255;
    if(!(dx&1)) {
        if(value) {
            p=(u16 *)(dest_row+((dx>>1)<<1));
            *p=(*p&0xff00)|value;
        }
    } else {
        if(value) {
            p=(u16 *)(dest_row+((dx>>1)<<1));
            *p=(*p&255)|(value<<8);
        }
    }
}
void func_08008914(s32 sx,s32 sy,s32 width,s32 height,s32 dx,s32 dy,s32 flip,s32 ox,s32 oy) {
    s32 y,x;
    sx+=ox;sy+=oy;
    if(!flip) {
        for(y=sy;y<sy+height;y++) {
            for(x=sx;x<sx+width;x++) {
                copy_pixel(x,dx,0x02000000+(y<<8),0x02000000+(dy<<8));
                dx++;
            }
            dx-=width;
            dy++;
        }
    } else {
        for(y=sy;y<sy+height;y++) {
            for(x=sx+width-1;x>=sx;x--) {
                copy_pixel(x,dx,0x02000000+(y<<8),0x02000000+(dy<<8));
                dx++;
            }
            dx-=width;
            dy++;
        }
    }
}
