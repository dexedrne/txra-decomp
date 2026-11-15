/* Unmatched ARM draft (j4: 80 normalized rows, same 400-byte length; frame, base address and loop shape match, the projection arithmetic is scheduled differently); excluded from the build. Compile with the arm profile. */
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
   s32 x=point->x-g_03005F70.field_00;
   s32 z=point->z-g_03005F70.field_08;
   s32 px=g_03002A18*x-g_03001B28*z;
   s32 pz=g_03001B28*x+g_03002A18*z;
   s32 y=-point->y-g_03005F70.field_04;
   s32 depth=g_03005F80.field_08+((g_03000DF8*y-g_03005F58*(pz>>12))>>12);
   s32 py=g_03005F58*y+g_03000DF8*(pz>>12);
   s32 factor;
   point->depth=depth;
   factor=g_0804F330[(depth>>1)+65536];
   point->sx=((factor*((g_03005F80.field_00+(px>>12))<<3))>>16)+60;
   point->sy=((factor*((g_03005F80.field_04+(py>>12))<<3))>>15)+80;
   count++;point++;
   if(count>23)break;
  }
  index=next&31;
 }
 if(index!=end) goto loop;
}
