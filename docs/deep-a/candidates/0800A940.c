/* Unmatched diagnostic source; not installed or accepted as behavior-correct. */
typedef struct { s16 f0,f1,f2,f3,f4,f5,f6,f7,f8,f9; } DeepStats;
typedef struct { s16 v[14]; } DeepCoefficients;
extern DeepStats g_030046E0[];
extern DeepCoefficients g_080205C4[];
extern TxraRecord g_03001E60[];
extern u8 g_03000B60[];
#define DEEP_BUMP(field,coefficient,factor) \
    { s32 change=(((s32)(field)<<5)*((coefficient)*(factor)))/100; change/=32; (field)+=change; }
void func_0800A940(s32 index)
{
    s32 model=g_03001E60[index].field_02-16;
    s32 first,second;
    DeepCoefficients *curve;
    if(g_03000B60[17]) *(s16 *)((u8 *)&g_03001E60[index]+90)=6-g_03000B60[17]*2;
    first=(g_03000B60[15]-1)+(g_03000B60[14]-1)*3;
    curve=&g_080205C4[model];
    DEEP_BUMP(g_030046E0[index].f0,curve->v[0],first);
    DEEP_BUMP(g_030046E0[index].f2,curve->v[1],first);
    DEEP_BUMP(g_030046E0[index].f4,curve->v[2],first);
    DEEP_BUMP(g_030046E0[index].f6,curve->v[3],first);
    DEEP_BUMP(g_030046E0[index].f8,curve->v[4],first);
    second=g_03000B60[16]-1;
    DEEP_BUMP(g_030046E0[index].f1,curve->v[5],second);
    DEEP_BUMP(g_030046E0[index].f3,curve->v[6],second);
    DEEP_BUMP(g_030046E0[index].f5,curve->v[7],second);
    DEEP_BUMP(g_030046E0[index].f7,curve->v[8],second);
    DEEP_BUMP(g_030046E0[index].f9,curve->v[9],second);
    DEEP_BUMP(*(s16 *)((u8 *)&g_03001E60[index]+96),g_080205C4[model].v[10],second);
    first=(g_03000B60[19]*2+g_03000B60[18]-4)+g_03000B60[20];
    DEEP_BUMP(*(s16 *)((u8 *)&g_03001E60[index]+88),g_080205C4[model].v[11],first);
    first=g_03000B60[19]-1;
    DEEP_BUMP(*(s16 *)((u8 *)&g_03001E60[index]+86),g_080205C4[model].v[12],first);
}
