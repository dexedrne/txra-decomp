/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Camera projection of the 32x24 point grid (ARM, runs from RAM): each
 * active point is moved into camera space, rotated by the two camera
 * angle pairs, written back with its depth and its screen x/y from the
 * perspective table. Written like the Thumb sibling 080164D0 (saved_y,
 * in-place offsets); x and z are loaded and then offset in place so each
 * load shares its register with the result, and only x keeps its <<3
 * inside the expression. The outer pass is a goto loop so the 0x02014000
 * base is not hoisted. The unused pad array stands for the three spill
 * slots the original reload left untouched (frame 0x18). */
typedef struct { s32 x,y,z,active,sx,sy,depth; } Point;
extern s32 g_030001B8;
extern s32 g_03002A18,g_03001B28,g_03000DF8,g_03005F58;
extern TxraTriple g_03005F70,g_03005F80;
extern Point g_02014000[32][24];
extern s32 g_0804F330[];
void func_08016C18(void)
{
 s32 pad[3];
 s32 index=(g_030001B8-30)&31;
 s32 end=(g_030001B8-4)&31;
 loop: {
  u32 base=0x02014000;
  Point *point=(Point *)(base+index*672);
  s32 count=0;
  s32 next=index+1;
  while(point->active==1){
   s32 x,y,z,xx,zz,saved_y,factor;
   x=point->x;
   y=-point->y;
   z=point->z;
   x-=g_03005F70.field_00;
   y-=g_03005F70.field_04;
   z-=g_03005F70.field_08;
   xx=(x*g_03002A18-z*g_03001B28)>>12;
   saved_y=y;
   zz=(x*g_03001B28+z*g_03002A18)>>12;
   y=(saved_y*g_03000DF8-zz*g_03005F58)>>12;
   z=(saved_y*g_03005F58+zz*g_03000DF8)>>12;
   x=xx+g_03005F80.field_00;
   z+=g_03005F80.field_04;
   y+=g_03005F80.field_08;
   point->depth=y;
   z<<=3;
   y>>=1;
   factor=g_0804F330[y+0x10000];
   point->sx=(((x<<3)*factor)>>16)+60;
   point->sy=((z*factor)>>15)+80;
   count++;point++;
   if(count>23)break;
  }
  index=next&31;
 }
 if(index!=end) goto loop;
}
