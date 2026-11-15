#include "gba.h"
#include <assert.h>
#include <stdlib.h>
#include <string.h>
bool generated_dispatch(GBA *g) {(void)g;return false;}
const unsigned recompiled_function_count=0;
int main(int argc,char **argv) {
    assert(argc==2 || argc==3);
    GBA *g=calloc(1,sizeof(*g));assert(g);
    assert(coverage_start(g));
    if (argc==3) {
        for(u32 i=0;i<=262144;i++)coverage_transfer(g,2,i,0,0);
        assert(!coverage_finish(g,argv[1]));free(g);return 0;
    }
    g->r[15]=0x080000c0;g->cpsr=0x1f;g->quota=10;
    assert(tick(g));assert(tick(g)); /* deduplicated executed PC */
    rd32(g,0x0a000100); /* mirror canonicalized; aligned read size */
    branch(g,0x08002001,true);
    assert(tick(g));
    g->r[0]=0x08000100;g->r[1]=0x02000000;g->r[2]=4;
    bios(g,0x0b);
    /* DMA decrement and fixed source extents. */
    wr32(g,0x040000d4,0x08000206);wr32(g,0x040000d8,0x02000020);
    wr32(g,0x040000dc,0x80800004);
    wr32(g,0x040000d4,0x08000300);wr32(g,0x040000d8,0x02000040);
    wr32(g,0x040000dc,0x81000004);
    const uint8_t lz[]={0x10,6,0,0,0x10,65,66,67,0,2};
    const uint8_t rle[]={0x30,6,0,0,0x83,77};
    const uint8_t huff[]={0x28,4,0,0,1,0xc0,65,66,0,0,0,0x50};
    memcpy(g->rom+0x400,lz,sizeof(lz));memcpy(g->rom+0x500,rle,sizeof(rle));
    memcpy(g->rom+0x600,huff,sizeof(huff));
    g->r[0]=0x08000400;coverage_bios_source(g,0x11);
    g->r[0]=0x08000500;coverage_bios_source(g,0x14);
    g->r[0]=0x08000600;coverage_bios_source(g,0x13);
    g->r[15]=0x0801251c;g->r[0]=0x08001000;g->r[1]=0x02000000;g->r[2]=65536;
    coverage_pc(g);coverage_pc(g);
    g->r[15]=0x0800d51c;g->r[0]=4;coverage_pc(g);
    assert(coverage_finish(g,argv[1]));assert(!g->coverage);
    assert(coverage_finish(g,"build/unused.json")); /* disabled is no-op */
    assert(coverage_start(g));assert(!coverage_finish(g,"build/no-such-dir/coverage.json"));
    free(g);return 0;
}
