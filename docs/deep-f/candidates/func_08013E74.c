/* Unmatched deep-f hypothesis; excluded from the ROM build. */
typedef struct DeepQuad {u16 x[4];s16 y[4];u8 u[4],v[4];u16 count,kind;struct DeepQuad *next;} DeepQuad;
extern u32 g_03001B1C;
extern s32 g_030021D8;
extern s32 g_08020784[];
extern DeepQuad *g_030021C4,*g_03000670[];
void func_08013E74(void)
{
    s32 row,u,t,y,y2,v,top;
    u32 k,k4;
    y=44;
    k=g_03001B1C&31;
    for(row=0;row<=2;row++) {
        if(row==0) y=-12;
        if(row==1) y=44;
        if(row==2) y=100;
        for(u=0;u<=31;u+=2) {
            s32 *a,*b;
            top=64;
            g_030021C4->x[0]=y;
            a=&g_08020784[k];
            g_030021C4->y[0]=(*a>>1)+top;
            y2=y+2;
            g_030021C4->x[1]=y2;
            k4=k+4;
            b=&g_08020784[k4&31];
            g_030021C4->y[1]=(*b>>1)+top;
            g_030021C4->x[2]=y2;
            g_030021C4->y[2]=(*b>>1)+39+top;
            g_030021C4->x[3]=y;
            g_030021C4->y[3]=(*a>>1)+39+top;
            v=0;
            t=g_030021D8+(row-1);
            if(t<0) t+=6;
            if(t>5) t-=6;
            if(t>2) { v=40; t-=3; }
            t=t*36+u;
            g_030021C4->u[0]=t; g_030021C4->v[0]=v;
            g_030021C4->u[1]=t+2; g_030021C4->v[1]=v;
            g_030021C4->u[2]=t+2; g_030021C4->v[2]=v+39;
            g_030021C4->u[3]=t; g_030021C4->v[3]=v+39;
            g_030021C4->count=11;
            g_030021C4->kind=3;
            if(!g_03000670[0]) {
                g_030021C4->next=0;
                g_03000670[0]=g_030021C4;
            } else {
                g_030021C4->next=g_03000670[0];
                g_03000670[0]=g_030021C4;
            }
            g_030021C4++;
            y=y2;
            k=k4&31;
        }
    }
}
