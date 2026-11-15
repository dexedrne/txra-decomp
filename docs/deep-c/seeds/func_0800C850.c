/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
extern TxraRecord g_03001E60[];
extern s32 g_03002E4C,g_030001B8,g_03002334,g_03005F50;
extern s16 g_030021CC;
extern s32 g_083D2280[],g_083C2280[];
extern void func_08002854(void);
void func_0800C850(s32 slot) {
    s32 current=g_03001E60[slot].field_38, previous=current-1, next=current+1;
    TxraRow28 *row;
    s32 dx,dz,a,c,s,side,forward;
    if(previous<0) previous+=g_03002E4C;
    if(next>=g_03002E4C) next=0;
    row=&g_03006874[current];
    dx=g_03001E60[slot].field_04-row->field_00;
    dz=g_03001E60[slot].field_0c-row->field_08;
    a=(4096-row->field_0c)&16383;
    c=g_083D2280[a]; s=g_083C2280[a];
    side=(dx*c-dz*s)>>12;
    forward=(dx*s+dz*c)>>12;
    *(s16 *)((u8 *)&g_03001E60[slot]+0x42)=(side+768)>>4;
    if(forward>511) {
        current=next;
        if(slot==0 && g_030021CC==0) {
            g_030001B8=(g_030001B8+1)&31;
            g_03002334=0;
            g_03005F50=current;
            func_08002854();
        }
    }
    if(forward<0) {
        if(slot==0 && g_030021CC==0) {
            if(current==next) g_030001B8-=2;
            else g_030001B8--;
            g_030001B8 &=31;
            g_03002334=1;
        }
        current=previous;
        if(slot==0 && g_030021CC==0) {
            g_03005F50=current;
            func_08002854();
        }
    }
    g_03001E60[slot].field_38=current;
}
