/* Compare structural decoding with guest instructions; print metadata hashes only. */
#include "gba.h"
#include <stdlib.h>
#include <string.h>
bool generated_dispatch(GBA *g) {(void)g;return false;}
int main(int argc, char **argv) {
    if(argc!=2)return 2;
    GBA *g=calloc(1,sizeof(*g));
    FILE *f=fopen(argv[1],"rb");
    if(!f || fread(g->rom,1,sizeof(g->rom),f)!=sizeof(g->rom))return 2;
    fclose(f);
    unsigned offset,size;
    while(scanf("%u %u",&offset,&size)==2) {
        memset(g->ewram,0,sizeof(g->ewram));memset(g->iwram,0,sizeof(g->iwram));
        memset(g->r,0,sizeof(g->r));
        g->cpsr=0x3f;g->stopped=false;g->r[0]=0x08000000+offset;
        g->r[1]=0x02000000;g->r[2]=size;g->r[13]=0x03007f00;
        g->r[14]=0x02030001;g->r[15]=0x0801251c;
        unsigned steps=0;
        while(g->r[15]!=0x02030000 && !g->stopped && steps++<10000000) {
            g->quota=1000;fallback(g);
        }
        if(g->stopped || steps>=10000000 || g->unsupported)return 3;
        unsigned hash=2166136261u;
        for(unsigned i=0;i<size;i++)hash=(hash^g->ewram[i])*16777619u;
        printf("%u %u\n",offset,hash);
    }
    free(g);return 0;
}
