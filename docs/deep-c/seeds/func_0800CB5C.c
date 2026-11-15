/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
extern TxraRecord g_03001E60[];
typedef struct { s16 acceleration,limit; } GearPair;
extern GearPair g_030046E0[][5];
extern s16 g_03002A1C,g_03005F54;
extern u16 g_030001BC,g_0300218C;
extern s32 g_083D2280[],g_083C2280[];
extern s32 func_08014614(s32,s32);
#define R g_03001E60[slot]
#define H(off) (*(s16 *)((u8 *)&R+(off)))
#define W(off) (*(s32 *)((u8 *)&R+(off)))
void func_0800CB5C(s32 slot) {
    s32 oldx=R.field_04, oldz=R.field_0c,angle,velocity,dx,dz,turn;
    W(0x2c)=0;
    if(H(0x44)&1) {
        if(H(0x44)&2) W(0x2c)=-512;
        else W(0x2c)=g_030046E0[slot][R.field_52].acceleration;
    }
    if(H(0x44)&2) W(0x2c)=-512;
    R.field_28+=W(0x2c)>>3;
    if(slot!=0 || g_03002A1C==0 || g_03005F54!=0 || (g_030001BC&32)) {
        s16 gear=R.field_52;
        s32 limit=g_030046E0[slot][gear].limit;
        if(R.field_28>limit) {
            if(gear<=3) {
                if(H(0x5c)>H(0x5a)) {R.field_52++;H(0x5c)=0;}
                else {H(0x5c)++;R.field_28-=64;}
            }
        } else if(gear>0 && R.field_28<g_030046E0[slot][gear-1].limit-8) R.field_52--;
    } else {
        s32 accel=g_030046E0[0][R.field_52].acceleration;
        s32 limit=g_030046E0[0][R.field_52].limit;
        if(R.field_28>limit+accel && R.field_52<=3) R.field_28-=accel;
        if((g_0300218C&256) && R.field_52<=3) R.field_52++;
        if((g_0300218C&512) && R.field_52>0) R.field_52--;
    }
    if(R.field_28 < -512) R.field_28=-512;
    if(R.field_28>H(0x60)) R.field_28=H(0x60);
    velocity=R.field_28>>3;
    angle=((R.field_34>>3)+12288)&16383;
    R.field_04=oldx+((g_083D2280[angle]*velocity)>>12);
    R.field_0c=oldz+((g_083C2280[angle]*velocity)>>12);
    velocity=R.field_3c>>3;
    angle=(H(0x3a)+12288)&16383;
    R.field_04+=(g_083D2280[angle]*velocity)>>12;
    R.field_0c+=(g_083C2280[angle]*velocity)>>12;
    if(R.field_3c>0) {
        R.field_3c-=256;
        if(R.field_3c<0) R.field_3c=0;
    }
    if(R.field_3c<0) {
        R.field_3c+=256;
        if(R.field_3c>0) R.field_3c=0;
    }
    if(R.field_3c) {
        turn=func_08014614(R.field_20,H(0x3e));
        if(turn>8191) turn-=16384;
        R.field_20=(R.field_20+(turn>>1))&16383;
    }
    if(R.field_3c>192 && R.field_28>1600) R.field_28-=64;
    if(R.field_28>6) R.field_28-=6;
    else if(R.field_28>0) R.field_28--;
    else if(R.field_28 < -4) R.field_28+=4;
    else if(R.field_28<0) R.field_28++;
}
