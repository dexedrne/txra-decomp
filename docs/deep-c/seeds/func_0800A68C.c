/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
extern s16 g_03005788;
extern u32 g_03000018;
extern void func_0800A8A0(u32,const void *,void *,s32,u32);
static inline void dma_words(u32 source,u32 dest,u32 control) {
    vu32 *dma=(vu32 *)0x040000D4;
    dma[0]=source;dma[1]=dest;dma[2]=control;(void)dma[2];
}
void func_0800A68C(void) {
    if(g_03005788==0) {
        dma_words(0x0827A384,0x03002A30,0x84000050);
        if(g_03000018==0) dma_words(0x0827A0C4,0x03002B70,0x84000010);
        if(g_03000018==1) dma_words(0x08279CC4,0x03002B70,0x84000010);
        if(g_03000018==2) dma_words(0x08279EC4,0x03002B70,0x84000010);
        if(g_03000018==3) {dma_words(0x0827A2C4,0x03002B70,0x84000010);(void)*(vu32 *)0x040000DC;}
        dma_words(0x03002DB0,0x03002BB0,0x84000014);
        dma_words(0x082B3D9C,0x03002C00,0x8400000C);
        dma_words(0x0827A584,0x03000BE0,0x84000050);
        dma_words(0x082C770C,0x03000D20,0x8400001C);
    } else {
        func_0800A8A0(3,(void *)0x0827A384,(void *)0x03002A30,0x140,32);
        if(g_03000018==0) func_0800A8A0(3,(void *)0x0827A0C4,(void *)0x03002B70,0x40,32);
        if(g_03000018==1) func_0800A8A0(3,(void *)0x08279CC4,(void *)0x03002B70,0x40,32);
        if(g_03000018==2) func_0800A8A0(3,(void *)0x08279EC4,(void *)0x03002B70,0x40,32);
        if(g_03000018==3) func_0800A8A0(3,(void *)0x0827A2C4,(void *)0x03002B70,0x40,32);
        func_0800A8A0(3,(void *)0x03002DB0,(void *)0x03002BB0,0x50,32);
        func_0800A8A0(3,(void *)0x082B3D9C,(void *)0x03002C00,0x30,32);
        func_0800A8A0(3,(void *)0x0827A584,(void *)0x03000BE0,0x140,32);
        func_0800A8A0(3,(void *)0x082C770C,(void *)0x03000D20,0x70,32);
        g_03005788--;
    }
}
