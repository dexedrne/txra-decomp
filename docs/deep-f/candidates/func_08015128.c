/* Unmatched deep-f hypothesis; excluded from the ROM build. */
extern u16 g_03002A30[];
void func_08015128(s32 t)
{
    s32 i;
    vu16 *target;
    if(t<=127 && (t&3)==0) {
        for(i=0;i<256;i++) {
            s32 r,g,b,tr,tg,tb;
            u16 c=g_03002A30[i];
            u16 d;
            r=c&31; g=(c>>5)&31; b=(c>>10)&31;
            d=*target;
            tr=d&31; tg=(d>>5)&31; tb=(d>>10)&31;
            if(r<tr) r++;
            if(g<tg) g++;
            if(b<tb) b++;
            g_03002A30[i]=r+(g<<5)+(b<<10);
            target++;
        }
    }
    if((u32)(t-256)<=127) {
        for(i=0;i<256;i++) {
            s32 r,g,b;
            u16 c=g_03002A30[i];
            r=c&31; g=(c>>5)&31; b=(c>>10)&31;
            if(r>0) r--;
            if(g>0) g--;
            if(b>0) b--;
            g_03002A30[i]=r+(g<<5)+(b<<10);
        }
    }
}
