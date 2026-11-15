/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
typedef struct DeepQuad {u16 x[4];s16 y[4];u8 u[4],v[4];u16 count,kind;struct DeepQuad *next;} DeepQuad;
extern TxraRecord g_03001E60[];
extern TxraTriple g_030055F0[],g_030057A0[];
extern s32 g_03005F50,g_03002E4C;
extern DeepQuad *g_030021C4,*g_03000670[];
extern u8 g_03005680[][2];
extern void func_080164D0(u32);
void func_08009D94(void)
{
    s32 i;
    for(i=4;i<=7;i++) {
        s32 distance;
        s32 width; s32 left,top;
        u32 depth;
        u32 uv;
        if (g_03001E60[i].field_00==0) continue;
        distance=g_03001E60[i].field_38-g_03005F50;
        if(distance>g_03002E4C-32)distance-=g_03002E4C;
        else if(distance<32-g_03002E4C)distance+=g_03002E4C;
        if((u32)(distance+1)>24)continue;
        g_030057A0[0].field_00=g_03001E60[i].field_04;
        g_030057A0[0].field_04=g_03001E60[i].field_08+420;
        g_030057A0[0].field_08=g_03001E60[i].field_0c;
        func_080164D0(0);
        g_030057A0[1].field_00=g_03001E60[i].field_04;
        g_030057A0[1].field_04=g_03001E60[i].field_08+292;
        g_030057A0[1].field_08=g_03001E60[i].field_0c;
        func_080164D0(1);
        distance=g_030055F0[1].field_04-g_030055F0[0].field_04;
        width=distance>>2;
        { DeepQuad *q=g_030021C4;
        left=g_030055F0[0].field_00-width; q->x[0]=left;
        top=g_030055F0[0].field_04; q->y[0]=top;
        q->x[1]=g_030055F0[0].field_00+width+1;
        q->y[1]=g_030055F0[0].field_04;
        q->x[2]=g_030055F0[0].field_00+width+1;
        q->y[2]=g_030055F0[1].field_04;
        q->x[3]=g_030055F0[0].field_00-width;
        q->y[3]=g_030055F0[1].field_04; }
        if (((u16)left<=119 && (s16)top>=0 && (s16)top<=159) ||
            (g_030021C4->x[1]<=119 && g_030021C4->y[1]>=0 && g_030021C4->y[1]<=159) ||
            (g_030021C4->x[2]<=119 && g_030021C4->y[2]>=0 && g_030021C4->y[2]<=159) ||
            (g_030021C4->x[3]<=119 && g_030021C4->y[3]>=0 && g_030021C4->y[3]<=159)) {
            uv=24;
            if(g_03005680[g_03001E60[i].field_62][0])uv=37;
            g_030021C4->u[0]=uv; g_030021C4->v[0]=16;
            g_030021C4->u[1]=uv+12; g_030021C4->v[1]=16;
            g_030021C4->u[2]=uv+12; g_030021C4->v[2]=40;
            g_030021C4->u[3]=uv; g_030021C4->v[3]=40;
            depth=g_030055F0[0].field_08>>6;
            depth+=8;
            if(depth<=255) {
                g_030021C4->count=8;
                g_030021C4->kind=1;
                if(!g_03000670[depth]) {
                    g_030021C4->next=0;
                    g_03000670[depth]=g_030021C4;
                    g_030021C4++;
                } else {
                    g_030021C4->next=g_03000670[depth];
                    g_03000670[depth]=g_030021C4;
                    g_030021C4++;
                }
            }
        }
    }
}
