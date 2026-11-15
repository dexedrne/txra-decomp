/* Unmatched diagnostic source; not installed or accepted as behavior-correct. */
extern TxraRecord g_03001E60[];
extern s16 g_03005F54,g_030001BC,g_030021CC,g_03002330,g_03002A1C;
extern u16 g_030014BC,g_0300218C;
extern s32 g_03001B1C,g_03001E88[];
extern s32 func_08014614(s32,s32);
extern void func_0801604C(s32,s32);
#define DEEP_HALF(i,off) (*(s16 *)((u8 *)&g_03001E60[i]+(off)))
#define DEEP_FLAGS(i) (*(u16 *)((u8 *)&g_03001E60[i]+68))
void func_0800BDC0(s32 index)
{
    s32 angle,delta,i;
    u32 small=index-1;
    if((u16)DEEP_HALF(index,76)==2 || (!index && g_03005F54) || (g_030001BC&32)) {
        if(small<=2) {
            DEEP_HALF(index,74)=(DEEP_HALF(index,74)+1)&511;
            if(!(u16)DEEP_HALF(index,74)) {
                switch(g_03001E60[index].field_48) {
                case 48:
                    if(g_03001B1C&1)g_03001E60[index].field_48=10;
                    else g_03001E60[index].field_48=84;
                    break;
                case 10: case 84:g_03001E60[index].field_48=48;break;
                }
            }
        }
        if(!index && (g_030014BC&1)) {
            if((u16)g_03005F54==32)g_03005F54=31;
            DEEP_HALF(0,76)=0;
        }
        angle=(g_03006874[g_03001E60[index].field_38].field_0c+4096)&16383;
        delta=DEEP_HALF(index,66)-g_03001E60[index].field_48;
        if((u32)(delta+11)<=22)angle+=delta<<3;
        angle&=16383;
        angle=func_08014614((g_03001E60[index].field_34>>3)&16383,angle);
        if(angle>8191)angle-=16384;
        DEEP_FLAGS(index)=0;
        if(!index) {
            if(!g_030001BC && g_03005F54) {
                if(g_03001E60[0].field_28<=2559)DEEP_FLAGS(0)|=1;
            } else if(g_03001E60[index].field_28<=2239)DEEP_FLAGS(index)|=1;
        } else if(index<=3) {
            if(g_03001E60[index].field_28<=2559)DEEP_FLAGS(index)=1;
        } else if(!g_030001BC) {
            if(g_03001E60[index].field_28<=1919)DEEP_FLAGS(index)=1;
        } else if(g_030001BC==index)DEEP_FLAGS(index)=1;
        else if(g_03001E60[index].field_28<=2239)DEEP_FLAGS(index)=1;
        if((g_030001BC&32) && index==(g_030001BC&7) && !g_030021CC && g_03001E60[index].field_38>g_03001E60[0].field_38+2 && g_03001E60[index].field_28>1280)DEEP_FLAGS(index)=(DEEP_FLAGS(index)&~1)|2;
        if(!index && (g_030001BC&32) && g_03001E60[0].field_38>g_03001E60[g_030001BC&7].field_38-4 && g_03001E60[0].field_28>960 && !g_030021CC)DEEP_FLAGS(0)|=2;
        if(DEEP_HALF(index,66)<g_03001E60[index].field_48-10 && angle<=199 && !g_030021CC) {
            DEEP_FLAGS(index)|=16;
            if(g_03001E88[index*25]>1600 && angle<=349 && index<=3)DEEP_FLAGS(index)|=2;
        }
        if(DEEP_HALF(index,66)>g_03001E60[index].field_48+10 && angle>-200 && !g_030021CC) {
            DEEP_FLAGS(index)|=32;
            if(g_03001E88[index*25]>1600 && angle>-350 && index<=3)DEEP_FLAGS(index)|=2;
        }
        if(DEEP_HALF(index,66)>=g_03001E60[index].field_48-10 && DEEP_HALF(index,66)<=g_03001E60[index].field_48+10) {
            if(angle<-4) {
                if(small<=2) {if(g_03001E88[index*25]>600)DEEP_FLAGS(index)|=16;}
                else DEEP_FLAGS(index)|=16;
            }
            if(angle>4) {
                if(small<=2) {if(g_03001E88[index*25]>600)DEEP_FLAGS(index)|=32;}
                else DEEP_FLAGS(index)|=32;
            }
        }
        for(i=0;i<=7;i++) {
            if(g_03001E60[i].field_00 && i!=index && g_03001E60[i].field_38<g_03001E60[index].field_38+6 && g_03001E60[i].field_38>g_03001E60[index].field_38-1 && g_03001E60[index].field_48>=g_03001E60[i].field_48-8 && g_03001E60[index].field_48<=g_03001E60[i].field_48+8) {
                if(g_030001BC && !index && i==(g_030001BC&7))continue;
                if(g_03001E60[index].field_48<=44)g_03001E60[index].field_48=48;
                else if(g_03001E60[index].field_48>51)g_03001E60[index].field_48=48;
                else if(g_03001B1C&1)g_03001E60[index].field_48=10;
                else g_03001E60[index].field_48=84;
            }
        }
        if(small<=2)for(i=0;i<=7;i++) {
            if(i!=index && g_03001E60[i].field_00 && DEEP_HALF(i,66)>DEEP_HALF(index,66)-18 && DEEP_HALF(i,66)<DEEP_HALF(index,66)+18 && g_03001E60[i].field_38<g_03001E60[index].field_38+3 && g_03001E60[i].field_38>g_03001E60[index].field_38-1) {
                if(g_03001E88[index*25]>0)DEEP_FLAGS(index)=2;else DEEP_FLAGS(index)=0;
            }
        }
    }
    if(!DEEP_HALF(index,76) && !g_030021CC && !g_03005F54 && !g_03002330) {
        DEEP_FLAGS(index)=g_030014BC;
        if((!g_03002A1C && (g_0300218C&256)) || (g_03002A1C==1 && (g_0300218C&64))) {
            if(!g_030001BC)func_0801604C(17,1);
            else func_0801604C(17,1);
        }
    }
}
