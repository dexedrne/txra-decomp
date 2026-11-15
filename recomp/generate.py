#!/usr/bin/env python3
"""ARMv4T -> C semantic operations. Generated ROM-dependent C stays in build/.
With --draft, lift the same per-instruction output into readable build/drafts/<func>.c."""
import argparse,hashlib,json,struct,sys,zlib
from pathlib import Path
BASE=0x08000000

def sign(v,n): return (v^(1<<(n-1)))-(1<<(n-1))
def decode(w,t,pc,direct=None):
    nxt=pc+(2 if t else 4)
    if t:
        a,b,c=(w>>8)&7,(w>>3)&7,w&7
        if w&0xf800==0xf000: return f'g->r[14]=0x{(pc+4+(sign(w&2047,11)<<12))&0xffffffff:08x}; g->r[15]={nxt}u;'
        if w&0xf800==0xf800:
            return f'{{u32 dst=g->r[14]+{(w&2047)*2}u; g->r[14]={nxt|1}u; branch(g,dst,true);}}'+(f'{direct[direct[pc,"bl"],True]}(g);' if direct and (pc,"bl") in direct and (direct[pc,"bl"],True) in direct else '')
        if w&0xf800==0xe000:return f'g->r[15]={pc+4+(sign(w&2047,11)<<1)}u;'
        if w&0xff00==0xdf00:return f'g->r[15]={nxt}u; bios(g,{w&255});'
        if w&0xf000==0xd000:return f'g->r[15]=cond(g,{(w>>8)&15})?{pc+4+(sign(w&255,8)<<1)}u:{nxt}u;'
        # Each group is decoded at build time; operands are constant in C.
        if w&0xe000==0: return f'thumb(g,0,{(w>>11)&3},{(w>>6)&31},{b},{c});'
        if w&0xe000==0x2000:return f'thumb(g,1,{(w>>11)&3},{a},{w&255},0);'
        if w&0xfc00==0x4000:return f'thumb(g,2,{(w>>6)&15},{b},{c},0);'
        if w&0xfc00==0x4400:return f'thumb(g,3,{(w>>8)&3},{(w>>3)&15},{(w&7)|((w>>4)&8)},0);'
        if w&0xf800==0x4800:return f'g->r[{a}]=rd32(g,((g->r[15]+4)&~3u)+{(w&255)*4});g->r[15]={nxt}u;'
        if w&0xf000==0x5000:return f'thumb(g,4,{(w>>9)&7},{(w>>6)&7},{b},{c});'
        if w&0xe000==0x6000:return f'thumb(g,5,{(w>>11)&3},{(w>>6)&31},{b},{c});'
        if w&0xf000==0x8000:return f'thumb(g,6,{(w>>11)&1},{(w>>6)&31},{b},{c});'
        if w&0xf000==0x9000:return f'thumb(g,7,{(w>>11)&1},{a},{(w&255)*4},0);'
        if w&0xf000==0xa000:return f'thumb(g,8,{(w>>11)&1},{a},{(w&255)*4},0);'
        if w&0xff00==0xb000:return f'thumb(g,9,{(w>>7)&1},{(w&127)*4},0,0);'
        if w&0xf600==0xb400:return f'thumb(g,10,{(w>>11)&1},{w&255},{(w>>8)&1},0);'
        if w&0xf000==0xc000:return f'thumb(g,11,{(w>>11)&1},{a},{w&255},0);'
    else:
        cc=w>>28; body=None
        if w&0x0ffffff0==0x012fff10:body=f'branch(g,reg(g,{w&15}),reg(g,{w&15})&1);'
        elif w&0x0f000000==0x0f000000:body=f'g->r[15]={nxt}u; bios(g,{(w>>16)&255});'
        elif w&0x0e000000==0x0a000000:
            dst=(pc+8+(sign(w&0xffffff,24)<<2))&0xffffffff
            body=(f'g->r[14]={nxt}u;' if w&(1<<24) else '')+f'g->r[15]={dst}u;'
            if direct and w&(1<<24) and (dst,False) in direct: body+=f'{direct[dst,False]}(g);'
        elif w&0x0e000000==0x08000000:body=f'arm_block(g,{(w>>24)&1},{(w>>23)&1},{(w>>22)&1},{(w>>21)&1},{(w>>20)&1},{(w>>16)&15},{w&65535});'
        elif w&0x0e000000==0x00000000 and w&0x0f8000f0==0x00800090:body=f'arm_mul(g,1,{(w>>22)&1},{(w>>21)&1},{(w>>20)&1},{(w>>16)&15},{(w>>12)&15},{(w>>8)&15},{w&15});'
        elif w&0x0fc000f0==0x00000090:body=f'arm_mul(g,0,0,{(w>>21)&1},{(w>>20)&1},{(w>>16)&15},{(w>>12)&15},{(w>>8)&15},{w&15});'
        elif w&0x0fb00ff0==0x01000090:body=f'{{u32 ad=reg(g,{(w>>16)&15}),v=reg(g,{w&15}),old={"rd8" if w&(1<<22) else "rd32"}(g,ad); {"wr8" if w&(1<<22) else "wr32"}(g,ad,v);g->r[{(w>>12)&15}]=old;g->r[15]={nxt}u;}}'
        elif w&0x0e000090==0x00000090:body=f'arm_half(g,{(w>>24)&1},{(w>>23)&1},{(w>>22)&1},{(w>>21)&1},{(w>>20)&1},{(w>>16)&15},{(w>>12)&15},{((w>>4)&240)|(w&15)},{(w>>5)&3});'
        elif w&0x0fbf0fff==0x010f0000:body=f'arm_status(g,0,{(w>>22)&1},{(w>>12)&15},0);'
        elif w&0x0db0f000==0x0120f000:body=f'arm_status(g,1,{(w>>22)&1},{(w>>16)&15},{w&0xfff}|{((w>>25)&1)<<16});'
        elif w&0x0c000000==0x04000000:body=f'arm_mem(g,{(w>>25)&1},{(w>>24)&1},{(w>>23)&1},{(w>>22)&1},{(w>>21)&1},{(w>>20)&1},{(w>>16)&15},{(w>>12)&15},{w&4095});'
        elif w&0x0c000000==0:body=f'arm_dp(g,{(w>>25)&1},{(w>>21)&15},{(w>>20)&1},{(w>>16)&15},{(w>>12)&15},{w&4095},0,0);'
        if body:return f'if(cond(g,{cc})){{{body}}}else g->r[15]={nxt}u;'
    return 'g->unsupported++; g->stopped=true;'

def main(rompath="baserom.gba"):
    rom=Path(rompath).read_bytes();cfg=json.loads(Path('tools/rom.cfg').read_text())
    assert hashlib.sha1(rom).hexdigest()==cfg['sha1'],'wrong ROM'
    fs=json.loads(Path('docs/map/functions.json').read_text())['functions']
    mapped_count=len(fs)
    starts={f['start'] for f in fs}
    fs += [f for f in json.loads(Path('recomp/observed.json').read_text())['functions'] if f['start'] not in starts]
    entries=[]
    for f in fs:
        start=int(f['start'],16);t=f['mode']=='thumb'
        entries.append((start,t,f,0))
        for a in f['runtime_aliases']:entries.append((int(a['start'],16),t,f,int(a['start'],16)-start))
    names={(pc,t):f'fn_{pc:08x}_{int(t)}' for pc,t,_,_ in entries}
    owners={}
    out=['#include "gba.h"']
    out += [f'static __attribute__((noinline)) void {n}(GBA*g);' for n in names.values()]
    for pc,t,f,delta in entries:
        out.append(f'static __attribute__((noinline)) void {names[pc,t]}(GBA*g){{while(g->quota>0&&!g->stopped){{switch(g->r[15]){{')
        emitted=set()
        for a,z in f['spans']:
            at=int(a,16); end=int(z,16)
            while at<end:
                w=struct.unpack_from('<H' if t else '<I',rom,at-BASE)[0];run=at+delta
                if run not in emitted:
                    emitted.add(run)
                    owners.setdefault(run|int(t),names[pc,t])
                    if t and w&0xf800==0xf800 and at>=BASE+2:
                        prev=struct.unpack_from('<H',rom,at-BASE-2)[0]
                        if prev&0xf800==0xf000:names[run,'bl']=(run+2+(sign(prev&2047,11)<<12)+(w&2047)*2)&0xffffffff
                    guard=f'if(rd{16 if t else 32}(g,{run}u)!={w}u)return;' if run<BASE else ''
                    out.append(f'case {run}u: {guard} if(!tick(g))return; g->compiled_steps++; {decode(w,t,run,names)} break;')
                at+=2 if t else 4
        out.append('default:return;} if(((g->cpsr&32)!=0)!='+str(int(t))+')return;}}')
    out.append('const unsigned recompiled_function_count='+str(mapped_count)+';')
    out.append(f'const u32 recompiled_rom_crc={zlib.crc32(rom)}u;')
    out.append('typedef struct {u32 pc; void(*fn)(GBA*);} Entry; static const Entry entries[]={')
    for key,name in sorted(owners.items()):out.append(f'{{{key}u,{name}}},')
    out.append('}; bool generated_dispatch(GBA*g){u32 key=g->r[15]|((g->cpsr&32)?1:0);unsigned lo=0,hi=sizeof(entries)/sizeof(*entries);while(lo<hi){unsigned mid=lo+(hi-lo)/2;if(entries[mid].pc<key)lo=mid+1;else hi=mid;}if(lo<sizeof(entries)/sizeof(*entries)&&entries[lo].pc==key){entries[lo].fn(g);return true;}return false;}')
    Path('build').mkdir(exist_ok=True)
    generated=Path('build/generated.c'); text='\n'.join(out)+'\n'
    if not generated.exists() or generated.read_text()!=text: generated.write_text(text)
    Path('build/emitted.json').write_text(json.dumps({'functions_emitted':len(fs),'entries':len(entries)}))
    # The fallback uses the same semantic operations, with runtime operand decode.
    print(f'Emitted {len(fs)} functions, {len(entries)} load/run entries')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom',default='baserom.gba')
    parser.add_argument('--draft',action='store_true')
    args=parser.parse_args()
    if args.draft:
        import draft
        print(f'Wrote {draft.write_drafts()} drafts to build/drafts')
    else:main(args.rom)
