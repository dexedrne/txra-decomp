/* Unmatched diagnostic source; not installed or accepted as behavior-correct. */
typedef struct { s16 f0,f1,f2,f3,f4,f5,f6,f7,f8,f9; } DeepStats;
typedef struct { s16 v[14]; } DeepCoefficients;
extern DeepStats g_030046E0[];
extern DeepCoefficients g_08020404[];
extern TxraRecord g_03001E60[];
extern void func_0800A940(s32);
extern void func_0800AC3C(s32);
#define DEEP_SET(off,value) (*(s16 *)((u8 *)car+(off))=(value))
#define DEEP_DEFAULTS() \
    *(s16 *)((u8 *)&g_030046E0[0].f0+index*20)=curve->v[0]; \
    *(s16 *)((u8 *)&g_030046E0[0].f1+index*20)=curve->v[5]*20; \
    *(s16 *)((u8 *)&g_030046E0[0].f2+index*20)=curve->v[1]; \
    *(s16 *)((u8 *)&g_030046E0[0].f3+index*20)=curve->v[6]*20; \
    *(s16 *)((u8 *)&g_030046E0[0].f4+index*20)=curve->v[2]; \
    *(s16 *)((u8 *)&g_030046E0[0].f5+index*20)=curve->v[7]*20; \
    *(s16 *)((u8 *)&g_030046E0[0].f6+index*20)=curve->v[3]; \
    *(s16 *)((u8 *)&g_030046E0[0].f7+index*20)=curve->v[8]*20; \
    *(s16 *)((u8 *)&g_030046E0[0].f8+index*20)=curve->v[4]; \
    *(s16 *)((u8 *)&g_030046E0[0].f9+index*20)=curve->v[9]*20; \
    DEEP_SET(84,curve->v[13]); \
    DEEP_SET(86,curve->v[12]); \
    DEEP_SET(88,curve->v[11]); \
    DEEP_SET(90,6); \
    DEEP_SET(94,0); \
    DEEP_SET(96,curve->v[10]*20);
void func_0800AF4C(u32 index)
{
    TxraRecord *car;
    DeepCoefficients *curve;
    s32 model, q;
    switch(index) {
    case 0:
        car=&g_03001E60[index];
        model=car->field_02-16;
        curve=&g_08020404[model];
        DEEP_DEFAULTS();
        func_0800A940(index);
        break;
    case 1: case 2: case 3:
        car=&g_03001E60[index];
        *(s16 *)((u8 *)&g_030046E0[0].f0+index*20)=256;
        *(s16 *)((u8 *)&g_030046E0[0].f1+index*20)=500;
        *(s16 *)((u8 *)&g_030046E0[0].f2+index*20)=192;
        *(s16 *)((u8 *)&g_030046E0[0].f3+index*20)=900;
        *(s16 *)((u8 *)&g_030046E0[0].f4+index*20)=128;
        *(s16 *)((u8 *)&g_030046E0[0].f5+index*20)=1500;
        *(s16 *)((u8 *)&g_030046E0[0].f6+index*20)=96;
        *(s16 *)((u8 *)&g_030046E0[0].f7+index*20)=1900;
        *(s16 *)((u8 *)&g_030046E0[0].f8+index*20)=64;
        *(s16 *)((u8 *)&g_030046E0[0].f9+index*20)=2300;
        DEEP_SET(84,150);
        DEEP_SET(86,1000);
        DEEP_SET(88,1900);
        DEEP_SET(90,32);
        DEEP_SET(94,0);
        DEEP_SET(96,2400);
        break;
    case 4: case 5: case 6: case 7:
        car=&g_03001E60[index];
        q=(s16)(car->field_62/24);
        model=0;
        if(q==1) model=1;
        if(q==2) model=2;
        if(q==3) model=3;
        if(q==4) model=4;
        if(q==5) model=5;
        curve=&g_08020404[model];
        DEEP_DEFAULTS();
        func_0800AC3C(index);
        break;
    }
}
