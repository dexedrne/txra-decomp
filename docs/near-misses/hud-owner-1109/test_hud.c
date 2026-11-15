/* Synthetic baseline-versus-candidate state and ordered-call comparison.
 * The older C is a regression reference, not an original-instruction oracle. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "candidate_declarations.h"
void func_0800421C(void);
void reference_hud(void);
HudPair g_030046E0[8];
s16 g_03002A28, g_03001E50;
s32 g_03002338, g_03000B5C, g_0804F330[131072], g_080213E0[256], g_08021420, g_030021D4, g_03001B1C;
u8 g_08321C9C[65536], g_0832259C[65536], g_03005680[128][2];
HudFlash g_03000AD0[8];
HudSmoke g_030067F0[8];
HudRow g_08020C24[8];
TxraTriple g_030057A0[16], g_030055F0[16];
s16 g_03000AC0, g_03002330, g_03005F54, g_030001BC, g_03004780;
u16 g_03001B14;
TxraRecord g_03001E60[8];
u8 g_08306DE0[65536], g_08309DE0[65536], g_083156E0[65536], g_082BB5CC[65536], g_082BF5CC[65536], g_08313EE0[65536], g_0833229C[65536], g_083118E0[65536], g_083130E0[65536];
u8 g_03000DE8[8];
s8 g_03005790[8];
s32 g_08020304[128];
u32 g_030021D8, g_030061E4, g_03006680;
static unsigned current_seed, call_count;
static uint64_t calls[256][10];
static uint64_t *record(unsigned kind) {
    uint64_t *row;
    assert(call_count < 256);
    row=calls[call_count++]; memset(row,0,10*sizeof(*row)); row[0]=kind; return row;
}
void func_0801604C(s32 a,s32 b) {
    uint64_t *row=record(1); row[1]=(u32)a;row[2]=(u32)b;
}
void func_08005CF4(u32 a,s32 b,s32 c,s32 d,s32 e) {
    uint64_t *row=record(2);row[1]=a;row[2]=(u32)b;row[3]=(u32)c;row[4]=(u32)d;row[5]=(u32)e;
}
void func_0801533C(u8 *p,u32 a,u32 b,u32 c,u32 d,u32 e,u32 f,u32 g,u32 h) {
    uint64_t *row=record(3);row[1]=(uintptr_t)p;row[2]=a;row[3]=b;row[4]=c;row[5]=d;row[6]=e;row[7]=f;row[8]=g;row[9]=h;
}
void func_080162F8(s32 index,s32 mode) {
    uint64_t *row=record(4);int sign=(current_seed&1)?1:-1;
    assert(index>=0&&index<4);row[1]=(u32)index;row[2]=(u32)mode;
    g_030055F0[index].field_00=120+sign*g_030057A0[index].field_00/8;
    g_030055F0[index].field_04=80+g_030057A0[index].field_04/8;
    g_030055F0[index].field_08=512+g_030057A0[index].field_08;
}
typedef struct {
    s16 smooth, countdown, overlay;
    u32 tiles, affine, count;
    s32 transform[6];
    TxraTriple scratch[16],projected[16];
    HudFlash flash[8];HudSmoke smoke[8];
    uint64_t trace[256][10];
} Snapshot;
static void snapshot(Snapshot *s) {
    memset(s,0,sizeof(*s));s->smooth=g_03002A28;s->countdown=g_03002330;s->overlay=g_03005F54;
    s->tiles=g_030061E4;s->affine=g_03006680;s->count=call_count;
    s->transform[0]=g_03005800;s->transform[1]=g_03005804;s->transform[2]=g_03005808;
    s->transform[3]=g_0300580C;s->transform[4]=g_03005810;s->transform[5]=g_03005814;
    memcpy(s->scratch,g_030057A0,sizeof(s->scratch));memcpy(s->projected,g_030055F0,sizeof(s->projected));
    memcpy(s->flash,g_03000AD0,sizeof(s->flash));memcpy(s->smoke,g_030067F0,sizeof(s->smoke));
    memcpy(s->trace,calls,call_count*sizeof(calls[0]));
}
static void initialize(unsigned seed) {
    static const s16 timers[]={0,1,2,31,32,63,64,95,96,127,150};
    static const s16 modes[]={0,1,2,3,32,33};
    unsigned i,j; s32 rotation;
    current_seed=seed;call_count=0;memset(calls,0,sizeof(calls));
    memset(g_03001E60,0,sizeof(g_03001E60));
    memset(g_030057A0,0xa5,sizeof(g_030057A0));memset(g_030055F0,0x5a,sizeof(g_030055F0));
    g_03005800=1;g_03005804=2;g_03005808=3;g_0300580C=4;g_03005810=5;g_03005814=6;
    g_03000AC0=(seed%29==0);g_03002330=timers[seed%11];g_03005F54=timers[(seed/3)%11];
    g_030001BC=modes[(seed/7)%6];g_03004780=seed%8;g_03001B14=(seed/5)%3;
    g_03002A28=(seed*31)%12000;g_03001E50=(seed/11)%6;
    g_03002338=(s32)(seed%16)*128;g_03000B5C=(s32)(seed%32)*64;
    g_08021420=64;g_030021D4=(seed%7==0)?2:1;g_03001B1C=seed&15;
    g_030021D8=seed&1;g_030061E4=seed%16;g_03006680=seed%8;
    for(i=0;i<131072;i++)g_0804F330[i]=4096+(i%8);
    for(i=0;i<256;i++)g_080213E0[i]=32+i;
    for(i=0;i<128;i++){g_08020304[i]=6+i%3;g_03005680[i][0]=i&1;g_03005680[i][1]=0;}
    for(i=0;i<8;i++) {
        g_030046E0[i].a=0;g_030046E0[i].b=100+i*16;
        g_03001E60[i].field_00=((seed+i)%5!=0);g_03001E60[i].field_02=16+i%4;
        g_03001E60[i].field_04=(s32)((seed*3+i*17)%1024)-512;
        g_03001E60[i].field_08=(s32)((seed+i*11)%128)-64;
        g_03001E60[i].field_0c=(s32)((seed*5+i*23)%1024)-512;
        g_03001E60[i].field_20=seed%256;g_03001E60[i].field_24=(seed*7)%256;
        g_03001E60[i].field_28=(s32)((seed*47+i*211)%8000)-2000;
        g_03001E60[i].field_30=198+(seed+i)%5;
        g_03001E60[i].field_40=43+(seed+i)%4;g_03001E60[i].field_44=(seed/13)&3;
        g_03001E60[i].field_52=seed%5;g_03001E60[i].field_62=(seed*3+i*7)%100;
        rotation=(s32)(seed+i);memcpy(g_03001E60[i].unknown_10+12,&rotation,sizeof(rotation));
        g_03000AD0[i].active=(seed+i)%3==0;g_03000AD0[i].size=(seed+i)%23;
        g_03000AD0[i].x=100+(seed+i)%40;g_03000AD0[i].y=70+(seed+i)%30;
        g_030067F0[i].count=(seed%9==0)?1:((seed+i)%7);
        g_030067F0[i].x=(s32)(i*8)-32;g_030067F0[i].y=0;g_030067F0[i].z=193+i*3;
        g_03005790[i]=(seed+i)%10;
        for(j=0;j<3;j++) {
            ((s32 *)&g_08020C24[i].a)[j]=(s32)(20+i*8+j*4);
            ((s32 *)&g_08020C24[i].b)[j]=(s32)(24+i*4+j*8);
        }
    }
    memcpy(g_03000DE8,"A1 B2C",6);
}
int main(void) {
    static Snapshot before,after;unsigned seed;
    for(seed=0;seed<1024;seed++) {
        initialize(seed);reference_hud();snapshot(&before);
        initialize(seed);func_0800421C();snapshot(&after);
        if(memcmp(&before,&after,sizeof(before))) {
            fprintf(stderr,"HUD regression seed %u: calls %u / %u\n",seed,before.count,after.count);return 1;
        }
    }
    puts("1024 HUD state and ordered-call fixtures passed against the prior C draft; no ROM oracle");
    return 0;
}
