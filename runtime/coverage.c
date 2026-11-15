/* Optional metadata-only coverage. No ROM contents are serialized. */
#include "gba.h"
#include <stdlib.h>
#include <string.h>
#define SLOTS 262144u
typedef struct { u32 pc, target, size, destination, kind; bool used; } Record;
struct Coverage { uint8_t reads[0x400000], executed[0x448000]; Record *records; bool overflow; };
bool coverage_start(GBA *g) {
    g->coverage = calloc(1, sizeof(*g->coverage));
    if (!g->coverage) return false;
    g->coverage->records = calloc(SLOTS, sizeof(Record));
    if (!g->coverage->records) { free(g->coverage); g->coverage = NULL; return false; }
    return true;
}
static void record(GBA *g, u32 kind, u32 pc, u32 target, u32 size, u32 destination) {
    if (!g->coverage) return;
    u32 h = (pc * 2654435761u ^ target * 2246822519u ^ size * 3266489917u ^ destination ^ kind) & (SLOTS-1);
    for (unsigned i=0; i<SLOTS; i++, h=(h+1)&(SLOTS-1)) {
        Record *r=&g->coverage->records[h];
        if (!r->used) { *r=(Record){pc,target,size,destination,kind,true}; return; }
        if (r->pc==pc && r->target==target && r->size==size && r->destination==destination && r->kind==kind) return;
    }
    g->coverage->overflow=true;
}
void coverage_pc(GBA *g) {
    u32 pc=g->r[15], slot=~0u, mode=(g->cpsr&32)?1:2;
    /* Selected semantic entries carry addresses/counts only, never asset data. */
    if(pc==0x0801251c)record(g,256,pc,g->r[0],g->r[2],g->r[1]);
    if(pc==0x0800d51c)record(g,257,pc,g->r[0],0,0);
    if(pc==0x08012600)record(g,258,pc,g->r[0],g->frame,0);
    if ((pc>>24)>=8 && (pc>>24)<=12) slot=pc&0x3fffff;
    else if ((pc>>24)==2) slot=0x400000+(pc&0x3ffff);
    else if ((pc>>24)==3) slot=0x440000+(pc&0x7fff);
    if (slot!=~0u) {
        if(g->coverage->executed[slot]&mode)return;
        g->coverage->executed[slot]|=mode;
    }
    record(g, 0, pc, !!(g->cpsr&32), 0, 0);
}
void coverage_branch(GBA *g, u32 target, bool thumb) {
    record(g, 1, g->r[15] | !!(g->cpsr&32), (target & ~(thumb?1u:3u)) | thumb, 0, 0);
}
void coverage_read(GBA *g, u32 a) {
    if (g->coverage && (a>>24)>=8 && (a>>24)<=12) g->coverage->reads[a&0x3fffff]=1;
}
void coverage_transfer(GBA *g, unsigned kind, u32 src, u32 dst, u32 size) {
    record(g, kind, g->r[15] | !!(g->cpsr&32), src, size, dst);
}
bool coverage_finish(GBA *g, const char *path) {
    if (!g->coverage) return true;
    FILE *f=fopen(path,"w"); bool ok=false;
    if (f) {
        u32 crc=~0u;
        for(unsigned i=0;i<sizeof(g->rom);i++) {
            crc^=g->rom[i];
            for(unsigned bit=0;bit<8;bit++)crc=(crc>>1)^(0xedb88320u&(0u-(crc&1)));
        }
        fprintf(f,"{\"rom_crc32\":\"%08x\",",~crc);
        fprintf(f,"\"version\":1,\"overflow\":%s,\"pcs\":[",g->coverage->overflow?"true":"false");
        bool comma=false;
        for(unsigned i=0;i<SLOTS;i++) {Record *r=&g->coverage->records[i]; if(r->used && r->kind==0) {
            fprintf(f,"%s[%u,%u]",comma?",":"",r->pc,r->target); comma=true;
        }}
        fprintf(f,"],\"branches\":["); comma=false;
        for(unsigned i=0;i<SLOTS;i++) {Record *r=&g->coverage->records[i]; if(r->used && r->kind==1) {
            fprintf(f,"%s[%u,%u]",comma?",":"",r->pc,r->target); comma=true;
        }}
        fprintf(f,"],\"entries\":["); comma=false;
        for(unsigned i=0;i<SLOTS;i++) {Record *r=&g->coverage->records[i]; if(r->used && r->kind>=256) {
            fprintf(f,"%s[%u,%u,%u,%u]",comma?",":"",r->pc,r->target,r->destination,r->size); comma=true;
        }}
        fprintf(f,"],\"transfers\":["); comma=false;
        for(unsigned i=0;i<SLOTS;i++) {Record *r=&g->coverage->records[i]; if(r->used && r->kind>=2 && r->kind<256) {
            fprintf(f,"%s[%u,%u,%u,%u,%u]",comma?",":"",r->kind,r->pc,r->target,r->destination,r->size); comma=true;
        }}
        fprintf(f,"],\"reads\":["); comma=false;
        for(unsigned a=0;a<0x400000;) {
            if(!g->coverage->reads[a]) {a++;continue;}
            unsigned end=a+1; while(end<0x400000 && g->coverage->reads[end])end++;
            fprintf(f,"%s[%u,%u]",comma?",":"",a,end-a);comma=true;a=end;
        }
        fprintf(f,"]}\n"); ok=!ferror(f); if(fclose(f))ok=false;
    }
    ok=ok&&!g->coverage->overflow;
    free(g->coverage->records); free(g->coverage); g->coverage=NULL;
    return ok;
}
/* Size BIOS-compressed ROM sources without serializing or changing their data.
   Services not implemented by bios() still stop explicitly after this logging. */
void coverage_bios_source(GBA *g, unsigned service) {
    if (!g->coverage || service<0x11 || service>0x15) return;
    u32 src=g->r[0], start=src&0x3fffff, p=start+4, produced=0;
    if ((src>>24)<8 || (src>>24)>12 || start>0x3ffffb) return;
    const uint8_t *rom=g->rom;
    unsigned type=rom[start];
    u32 total=rom[start+1]|rom[start+2]<<8|rom[start+3]<<16;
    if (!total || total>0x400000) return;
    if ((service==0x11 || service==0x12) && type==0x10) {
        while (produced<total) {
            if(p>=0x400000)return;
            unsigned flags=rom[p++];
            for(int bit=7;bit>=0 && produced<total;bit--) {
                if(flags&(1u<<bit)) {
                    if(p+2>0x400000)return;
                    unsigned a=rom[p++], b=rom[p++], n=(a>>4)+3, back=((a&15)<<8|b)+1;
                    if(back>produced || produced+n>total)return;
                    produced+=n;
                } else {if(p>=0x400000)return; p++;produced++;}
            }
        }
    } else if ((service==0x14 || service==0x15) && type==0x30) {
        while(produced<total) {
            if(p>=0x400000)return;
            unsigned c=rom[p++], n=(c&127)+((c&128)?3:1);
            if(produced+n>total)return;
            p+=(c&128)?1:n;
            if(p>0x400000)return;
            produced+=n;
        }
    } else if (service==0x13 && (type==0x24 || type==0x28)) {
        unsigned tree=p, end=tree+(rom[p]+1)*2, node=tree+1, bits=0, word=0;
        if(end>0x400000)return;
        p=end;
        u32 wanted=total*(type==0x24?2:1);
        while(produced<wanted) {
            if(!bits) {
                if(p+4>0x400000)return;
                word=rom[p]|(u32)rom[p+1]<<8|(u32)rom[p+2]<<16|(u32)rom[p+3]<<24;
                p+=4;bits=32;
            }
            unsigned side=(word>>(--bits))&1, value=rom[node];
            unsigned child=(node&~1u)+((value&63)+1)*2+side;
            if(child<=tree || child>=end)return;
            if(value&(side?0x40:0x80)) {
                if(type==0x24 && rom[child]>15)return;
                produced++;node=tree+1;
            } else node=child;
        }
    } else return;
    coverage_transfer(g,service,src,g->r[1],p-start);
}
