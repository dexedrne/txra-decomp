#!/usr/bin/env python3
"""Measured, reproducible hand-designed source grids for the seventh matching pass."""
import argparse
import concurrent.futures as futures
import itertools
import json
import os
from pathlib import Path
import re
import time
import variant_search as vs

ROOT = Path(__file__).resolve().parents[1]


def packet():
    s=(ROOT/'docs/near-misses/func_08014988.c').read_text()
    for init, qual, access, inv in itertools.product(
        ['&g_03007A30','state','(TxraLinkState *)(u32)state','(TxraLinkState *)((u32)p - 20)','(TxraLinkState *)((u32)p - 20 - 0)'],
        ['', 'register ', 'const '],
        ['original','state','integer','packet','separate'],
        ['u32 inverted = ~sum;', 'u16 inverted = ~sum;', 's32 inverted = ~sum;']):
        c=s.replace('TxraLinkState *tail = &g_03007A30;',qual+'TxraLinkState *tail = '+init+';').replace('u32 inverted = ~sum;',inv)
        if access=='state': c=c.replace('tail->','state->')
        if access=='integer': c=c.replace('(u16 *)tail->field_28','*(u16 **)((u32)tail + 40)')
        if access=='packet': c=c.replace('packet[1] = inverted;', '*((u16 *)tail->field_28 + 1) = inverted;')
        if access=='separate': c=c.replace('u16 *packet = (u16 *)tail->field_28;', 'u16 *packet;\npacket = (u16 *)tail->field_28;')
        yield c


def blit():
    s=(ROOT/'tools/search-drafts/func_08014104.c').read_text()
    # Initializer use order determines pseudo-register creation; declaration
    # order and register qualifiers independently influence old allocation.
    setup=['width=120;','height=48;','destbase=(u32)g_02003C00;','sourcebase=(u32)g_0832F29C;','y=0;']
    old='width=120;height=48;\n destbase=(u32)g_02003C00;sourcebase=(u32)g_0832F29C;\n y=0;'
    inner=['u32 dest=(u32)(destbase+offset);','u32 source=(u32)(sourcebase+offset);','u32 left=width;']
    for order, ins, hint in itertools.product(itertools.permutations(setup),itertools.permutations(inner),['','height','destbase','sourcebase','width','y']):
        c=s.replace(old,'\n'.join(order)).replace(''.join(inner),''.join(ins))
        if hint:
            c=c.replace('u32 unused,width,destbase,sourcebase;\n s32 height,y;', '\n'.join(('register ' if n==hint else '')+t+' '+n+';' for t,n in [('u32','unused'),('u32','width'),('u32','destbase'),('u32','sourcebase'),('s32','height'),('s32','y')]))
        yield c


def angle():
    s=(ROOT/'docs/near-misses/func_08014614.c').read_text()
    # Separate the common first return from the wide wraparound tail. The
    # target shares a halfword narrowing only between the first two branches.
    for typ,first,tail,end in itertools.product(['s32','u32','int'],['(u16)(b - a)','(s16)(b - a)','b - a'],['b - 16384 - a','b - (a + 16384)','(b - a) - 16384'],['b - (a - 16384)','b + 16384 - a','(b - a) + 16384']):
        c=s.replace('u16 result;',typ+' result;').replace('result = b - a;', 'result = '+first+';').replace('b - 16384 - a',tail).replace('b - (a - 16384)',end)
        yield c
        yield c.replace('result = '+first+';\n goto done;', 'return '+first+';')


def queue():
    s=(ROOT/'tools/search-drafts/func_08015DA8_offsets.c').read_text()
    setup=['u32 i = 0;','u32 base = (u32)g_030061F0;','u32 endmarker = (u32)&g_030067E4;','vu32 *dma = (vu32 *)0x040000D4;','u32 cursor = base;','u32 offset = 0;','u32 destbase = base + 4;']
    old='\n    '.join(setup)
    assert old in s
    # Permute independent initialization groups without invalid use-before-init.
    for order in itertools.permutations(setup[:4]):
        for last in itertools.permutations(setup[4:]):
            for expr,hint in itertools.product(['base + 8 + offset','offset + (base + 8)','(base + 8) + offset'],['','base','i','destbase','endmarker']):
                c=s.replace(old,'\n    '.join(order+last)).replace('base + 8 + offset',expr)
                if hint: c=re.sub(r'\bu32 '+hint+r' =', 'register u32 '+hint+' =',c)
                yield c


def packet_aliases():
    s=(ROOT/'docs/near-misses/func_08014988.c').read_text()
    for q1,q2,base,loop,scope in itertools.product(
        ['', 'volatile ', 'register ', 'register volatile '],
        ['', 'volatile ', 'register ', 'const ', 'register volatile '],
        ['state','&g_03007A30','(TxraLinkState *)(u32)state'],
        ['original','separate','for','while','signed'],
        ['original','outer','global']):
        c=s.replace('TxraLinkState *state =',q1+'TxraLinkState *state =').replace('TxraLinkState *tail = &g_03007A30;',q2+'TxraLinkState *tail = '+base+';')
        if loop=='separate':c=c.replace('sum += *p++;','sum += *p; p++;')
        if loop=='for':c=c.replace('do {\n sum += *p++;\n i++;\n }\n while (i <= 9);','for (i = 0; i < 10; i++) { sum += *p++; }')
        if loop=='while':c=c.replace('do {\n sum += *p++;\n i++;\n }\n while (i <= 9);','while (i < 10) { sum += *p++; i++; }')
        if loop=='signed':c=c.replace('u32 i;','s32 i;')
        if scope=='outer':c=c.replace('    {\n        '+q2+'TxraLinkState *tail = '+base+';', '    '+q2+'TxraLinkState *tail = '+base+';\n    {')
        if scope=='global':c=c.replace('tail->','g_03007A30.')
        yield c


def blit_loops():
    s=(ROOT/'tools/search-drafts/func_08014104.c').read_text()
    for outer,inner,dtyp,htyp,expr in itertools.product(
        ['original','for','while','guard','increment'],
        ['original','post','for','pre'],
        ['u32','s32','u16 *','u8 *'],['s32','u32','u16','s16'],
        ['y*240','(y*15)*16','(y<<8)-(y<<4)','(y*120)*2']):
        c=s.replace('offset=y*240','offset='+expr).replace('s32 height,y;',htyp+' height; s32 y;')
        if dtyp in ['u32','s32']:c=c.replace('u32 unused,width,destbase,sourcebase;', 'u32 unused,width; '+dtyp+' destbase,sourcebase;')
        else:
            c=c.replace('u32 unused,width,destbase,sourcebase;','u32 unused,width; '+dtyp+'destbase, *sourcebase;').replace('destbase=(u32)g_02003C00','destbase=('+dtyp+')g_02003C00').replace('sourcebase=(u32)g_0832F29C','sourcebase=('+dtyp+')g_0832F29C')
            c=c.replace('destbase+offset','(u32)destbase+offset').replace('sourcebase+offset','(u32)sourcebase+offset')
        if outer=='for':c=c.replace('do {s32 nextrow=y+1;','for (;y<height;) {s32 nextrow=y+1;').replace('}while(y<height);','}')
        if outer=='while':c=c.replace('do {s32 nextrow=y+1;','while(y<height) {s32 nextrow=y+1;').replace('}while(y<height);','}')
        if outer=='guard':c=c.replace('do {s32 nextrow=y+1;','if(y<height) do {s32 nextrow=y+1;')
        if outer=='increment':c=c.replace('s32 nextrow=y+1;','').replace('y=nextrow;','y++;')
        if inner=='post':c=c.replace('left--;\n }while(left);','\n }while(--left);')
        if inner=='pre':c=c.replace('left--;','--left;')
        if inner=='for':c=c.replace('do {u32 value=', 'for (;left;left--) {u32 value=').replace('left--;\n }while(left);','\n }')
        yield c


def queue_loop():
    s=(ROOT/'tools/search-drafts/func_08015DA8_offsets.c').read_text()
    for mode,base,dest,offset,shape,cast in itertools.product(
        ['old','direct'],['u32','s32','u8 *','u32 *'],
        ['base + 4','4 + base'],['base + 8 + offset','offset + (base + 8)'],
        ['original','for','while','goto','pre'],['u32','s32']):
        c=s.replace('u32 base = (u32)g_030061F0;',base+' base = ('+base+')g_030061F0;').replace('base + 4',dest).replace('base + 8 + offset',offset).replace('u32 i =',cast+' i =')
        if '*' in base:
            c=c.replace('u32 cursor = base;','u32 cursor = (u32)base;').replace('u32 destbase = '+dest+';','u32 destbase = (u32)base + 4;').replace('*(u32 *)('+offset+')','*(u32 *)((u32)base + 8 + offset)')
        if mode=='direct':c=c.replace('dma[0] = source;','*(vu32 *)0x040000D4 = source;').replace('dma[1] = dest;','*(vu32 *)0x040000D8 = dest;').replace('dma[2] =','*(vu32 *)0x040000DC =').replace('dma[2];','*(vu32 *)0x040000DC;')
        if shape=='for':c=c.replace('do {','for (;i<=96;) {').replace('} while (i <= 96);','}')
        if shape=='while':c=c.replace('do {','while (i<=96) {').replace('} while (i <= 96);','}')
        if shape=='goto':c=c.replace('do {','loop: {').replace('} while (i <= 96);','} if (i<=96) goto loop;')
        if shape=='pre':c=c.replace('i++;','').replace('while (i <= 96)','while (++i <= 96)')
        yield c


def queue_memory():
    s=(ROOT/'tools/search-drafts/func_08015DA8_offsets.c').read_text()
    for volatile,source,ctrl,dest,init,body in itertools.product(
        ['none','all','source','count','dest'],['u32','s32','int'],
        ['inline','local','split','signed'],['destbase + offset','offset + destbase'],
        ['original','basefirst'],['original','else','goto']):
        c=s.replace('u32 source =',source+' source =').replace('destbase + offset',dest)
        if volatile=='all':c=c.replace('*(u32 *)cursor','*(vu32 *)cursor').replace('*(u32 *)(', '*(vu32 *)(')
        if volatile=='source':c=c.replace('*(u32 *)cursor','*(vu32 *)cursor')
        if volatile=='count':c=c.replace('count = *(u32 *)','count = *(vu32 *)')
        if volatile=='dest':c=c.replace('dest = *(u32 *)','dest = *(vu32 *)')
        if ctrl=='local':c=c.replace('dma[2] = (count >> 2) | 0x84000000;', '{ u32 mask = 0x84000000; dma[2] = (count >> 2) | mask; }')
        if ctrl=='split':c=c.replace('dma[2] = (count >> 2) | 0x84000000;', 'count >>= 2; count |= 0x84000000; dma[2] = count;')
        if ctrl=='signed':c=c.replace('dma[2] = (count >> 2) | 0x84000000;', 'dma[2] = (count >> 2) | -2080374784;')
        if init=='basefirst':c=c.replace('u32 i = 0;\n    u32 base = (u32)g_030061F0;', 'u32 base = (u32)g_030061F0;\n    u32 i = 0;')
        if body=='goto':c=c.replace('break;', 'goto done;').replace('    *(u32 *)base = 0;','done:    *(u32 *)base = 0;').replace('    *(vu32 *)base = 0;','done:    *(vu32 *)base = 0;')
        if body=='else':
            c=c.replace('break; }','break; } else {').replace('        i++;','        i++; }')
        yield c


def packet_raw():
    s=(ROOT/'docs/near-misses/func_08014988.c').read_text()
    original=s[s.index('    {\n        TxraLinkState *tail'):s.index('    state->field_14')]
    for typ,base,inlined,decls in itertools.product(
        ['u32','s32','u8 *','u32 *','TxraLinkState *','void *'],
        ['state','&g_03007A30'],['no','yes','register'],['original','before']):
        cast='('+typ+')'+base
        if typ=='TxraLinkState *': ptr='tail->field_28';cond='tail->field_00'
        else:ptr='(*(u8 * volatile *)((u32)tail + 40))';cond='(*(u8 *)tail)'
        body='u16 *packet = (u16 *)'+ptr+'; u32 inverted = ~sum; packet[1] = inverted; if ('+cond+') *(vu16 *)0x0400010E = 0;'
        if decls=='before':body='u32 inverted; u16 *packet; packet = (u16 *)'+ptr+'; inverted = ~sum; packet[1] = inverted; if ('+cond+') *(vu16 *)0x0400010E = 0;'
        if inlined!='no':
            helper='static inline void packet_tail('+('register ' if inlined=='register' else '')+typ+' tail, u32 sum) {'+body+'}\n'
            c=helper+s.replace(original,'    packet_tail('+cast+',sum);\n')
        else:c=s.replace(original,'    { '+typ+' tail = '+cast+'; '+body+' }\n')
        yield c


def literal_bases():
    # Address spelling can change CSE's equivalence notes: a symbolic pool load
    # and an integer constant are distinct RTL even when relocation agrees.
    a=LITERAL_ADDRESS
    s=(ROOT/('docs/near-misses/func_%08X.c'%a)).read_text()
    symbols=sorted(set(re.findall(r'&?g_[0-9A-F]+',s)))
    for mask in range(1<<len(symbols)):
        c=s
        for i,name in enumerate(symbols):
            if mask&(1<<i):
                address=int(name.split('_')[-1],16)
                value='0x%08X'%address
                if name.startswith('&'):value='(TxraLinkState *)'+value if address==0x03007A30 else '(u32 *)'+value
                c=re.sub(re.escape(name)+r'\b',value,c)
        yield c
        if a==0x08014988:
            yield c.replace('TxraLinkState *tail = &g_03007A30;', 'TxraLinkState *tail = state;')
            yield c.replace('u32 i;', 's32 i;')


def control_flow():
    a=CONTROL_ADDRESS
    s=(ROOT/('docs/near-misses/func_%08X.c'%a)).read_text()
    if a==0x08015DA8:
        s=(ROOT/'tools/search-drafts/func_08015DA8_offsets.c').read_text()
        s=s.replace('break;', 'goto done;').replace('    *(u32 *)base = 0;', 'done:    *(u32 *)base = 0;')
    # Compare explicit backedges with lexical loops. Goto loops carry different
    # loop notes into the historical optimizer, changing invariant movement.
    import variant_search as search
    s=search.split_declarations(s)
    for outer in ['original','goto']:
        c=s
        if outer=='goto':
            c=re.sub(r'\bdo\s*{','loop: {',c,count=1)
            c=re.sub(r'}\s*while\s*\(([^()]*)\);', r'} if (\1) goto loop;',c,count=1)
        yield c
        if a==0x08014988:
            yield c.replace('TxraLinkState *tail = &g_03007A30;', 'TxraLinkState *tail = state;')
        if a==0x08014104:
            yield c.replace('u32 left=width;', 'u32 left; left=width;')
        if a==0x08015DA8:
            for source in ['u32','s32']:
                for base in ['base + 8 + offset','offset + (base + 8)']:
                    yield c.replace('u32 source =',source+' source =').replace('base + 8 + offset',base)


def blit_declarations():
    s=(ROOT/'tools/search-drafts/func_08014104.c').read_text()
    outer='u32 unused,width,destbase,sourcebase;\n s32 height,y;'
    declarations=['u32 unused;','u32 width;','s32 height;','u32 destbase;','u32 sourcebase;','s32 y;']
    oldinner='u32 dest=(u32)(destbase+offset);u32 source=(u32)(sourcebase+offset);u32 left=width;'
    for order in itertools.permutations(declarations):
        for inner in itertools.permutations(['u32 dest;','u32 source;','u32 left;']):
            c=s.replace(outer,'\n'.join(order)).replace(oldinner, ''.join(inner)+'dest=(u32)(destbase+offset);source=(u32)(sourcebase+offset);left=width;')
            yield c


def packet_storage():
    s=(ROOT/'docs/near-misses/func_08014988.c').read_text()
    for qual,base,placement in itertools.product(
        ['const','volatile','const volatile','restrict','__restrict',''],
        ['state','&g_03007A30'],['tail','state','both']):
        c=s.replace('TxraLinkState *tail = &g_03007A30;', 'TxraLinkState *tail = '+base+';')
        if placement in ('tail','both'):c=c.replace('TxraLinkState *tail =', 'register TxraLinkState * '+qual+' tail =')
        if placement in ('state','both'):c=c.replace('TxraLinkState *state =', 'register TxraLinkState * '+qual+' state =')
        yield c
    for base,wrapper in itertools.product(['state','&g_03007A30'],['struct','union']):
        c=s.replace('TxraLinkState *tail = &g_03007A30;', wrapper+' { TxraLinkState *ptr; } holder = { '+base+' };')
        c=c.replace('tail->','holder.ptr->')
        yield c


def blit_indexed():
    body = """u32 value = *source;
if(value) {
 if(!(value&255)) *dest=(*dest & 255)+value;
 else if(!(value&65280)) *dest=(*dest & 65280)+value;
 else *dest=value;
}
dest++; source++;"""
    for row, col, types, offset, declarations in itertools.product(
        ['for','do','nextrow'],['for','decrement','countdown','dowhile'],
        ['u32','s32'],['y*120','y*width','(y*240)/2'],['before','after']):
        setup='u32 unused=g_03005FC0; u32 width=120; s32 height=48; s32 y;'
        if declarations=='before':setup+='u16 *destbase=g_02003C00; u16 *sourcebase=g_0832F29C;'
        setup+='y=0;'
        if declarations=='after':setup+='u16 *sourcebase=g_0832F29C; u16 *destbase=g_02003C00;'
        loop='u16 *dest=destbase+('+offset+'); u16 *source=sourcebase+('+offset+'); '+types+' x;'
        if col=='for':loop+='for(x=0;x<width;x++){'+body+'}'
        if col=='decrement':loop+='for(x=width;x;x--){'+body+'}'
        if col=='countdown':loop+='x=width;if(x)while(x){'+body+'x--;}'
        if col=='dowhile':loop+='x=width;if(x)do{'+body+'x--;}while(x);'
        if row=='for':outer='for(;y<height;y++){'+loop+'}'
        if row=='do':outer='do{'+loop+'y++;}while(y<height);'
        if row=='nextrow':outer='do{s32 nextrow=y+1;'+loop+'y=nextrow;}while(y<height);'
        yield 'extern volatile u32 g_03005FC0; extern u16 g_02003C00[],g_0832F29C[]; void func_08014104(void){'+setup+outer+'}'


def decode_control():
    s=(ROOT/'docs/match6-search/expanded/func_0801251C.c').read_text()
    finish='    if ((s32)r2 <= (s32)r12) goto L_080125F4;\n    if ((s32)r4 > (s32)r6) goto L_08012540;\nL_080125F4:'
    options=[
        ('for (;;) {','if ((s32)r2 <= (s32)r12) break; if ((s32)r4 <= (s32)r6) break; }'),
        ('while (1) {','if ((s32)r2 <= (s32)r12) break; if ((s32)r4 <= (s32)r6) break; }'),
        ('do {','if ((s32)r2 <= (s32)r12) return; } while ((s32)r4 > (s32)r6);'),
        ('do {','if ((s32)r2 <= (s32)r12) goto finish; } while ((s32)r4 > (s32)r6); finish:'),
        ('do {','} while ((s32)r2 > (s32)r12 && (s32)r4 > (s32)r6);'),
        ('L_08012540:','if ((s32)r2 <= (s32)r12) goto L_080125F4; if ((s32)r4 > (s32)r6) goto L_08012540; L_080125F4:')]
    for begin,end in options:
        for tag,mask,hint,add in itertools.product(['u32','u8','s32'],['u32','u8','s32'],['none','r5','r7','r12'],['original','separate','compound']):
            c=s.replace('L_08012540:',begin).replace(finish,end).replace('u32 r5;',tag+' r5;').replace('u32 r7;',mask+' r7;')
            if hint!='none':c=c.replace('u32 '+hint+';', 'register u32 '+hint+';')
            if add=='separate':c=c.replace('r0 = r6 + r0;', 'r1 = r0; r0 = r6 + r1;')
            if add=='compound':c=c.replace('r0 = r6 + r0;', 'r0 += r6;')
            yield c


def decode_tag():
    s=(ROOT/'docs/match7-search/decode_control/func_0801251C.c').read_text()
    old='r5 = *(u8 *)r2;\n    r0 = r5;\n    r0 &= r7;\n    if (r0 != 0xC0)'
    assert old in s
    for tag,condition,load in itertools.product(
        ['u32','s32','u8','s8','u16','s16'],
        ['direct','local','block','original'],['plain','volatile','index','cast']):
        c=s.replace('u32 r5;',tag+' r5;')
        expr={'plain':'*(u8 *)r2','volatile':'*(vu8 *)r2','index':'((u8 *)r2)[0]','cast':'(u32)*(u8 *)r2'}[load]
        if condition=='direct':new='r5 = '+expr+';\n    if ((r5 & r7) != 0xC0)'
        if condition=='local':new='r5 = '+expr+'; u32 masked = r5 & r7;\n    if (masked != 0xC0)'
        if condition=='block':new='r5 = '+expr+'; u32 masked; masked = r5; masked &= r7;\n    if (masked != 0xC0)'
        if condition=='original':new='r5 = '+expr+';\n    r0 = r5;\n    r0 &= r7;\n    if (r0 != 0xC0)'
        # Replace before changing the tag declaration so each edit is independent.
        c=c.replace(old,new)
        yield c


def packet_induction():
    s=(ROOT/'docs/near-misses/func_08014988.c').read_text()
    for typ,loop,expr in itertools.product(['u32','s32','u16','u8'],['original','for','while'],[
        '(TxraLinkState *)((u32)state + i - 10)',
        '(TxraLinkState *)((u32)state + (i - 10))',
        'state + (i - 10)',
        '(TxraLinkState *)((u32)&g_03007A30 + i - 10)',
        '(i == 10 ? state : &g_03007A30)',
        '(TxraLinkState *)((u32)state + ((i - 10) & 0))']):
        c=s.replace('u32 i;',typ+' i;').replace('TxraLinkState *tail = &g_03007A30;', 'TxraLinkState *tail = '+expr+';')
        if loop=='for':c=c.replace('do {\n sum += *p++;\n i++;\n }\n while (i <= 9);','for (i = 0; i < 10; i++) { sum += *p++; }')
        if loop=='while':c=c.replace('do {\n sum += *p++;\n i++;\n }\n while (i <= 9);','while (i < 10) { sum += *p++; i++; }')
        yield c


def packet_representation():
    s=(ROOT/'docs/near-misses/func_08014988.c').read_text()
    for typ,tail,source,timing in itertools.product(
        ['u32','s32','u8 *','void *','TxraLinkState *'],
        ['state','&g_03007A30'],['u32','void *','u16 *'],
        ['original','shift','afterinvert','separate']):
        c=s.replace('u32 source)',source+' source)').replace('TxraLinkState *state = &g_03007A30;',typ+' state = ('+typ+')&g_03007A30;')
        c=c.replace('state->','((TxraLinkState *)state)->').replace('TxraLinkState *tail = &g_03007A30;', 'TxraLinkState *tail = (TxraLinkState *)'+tail+';')
        if timing=='shift':c=c.replace('((TxraLinkState *)state)->field_14 = -1;', 'state = ('+typ+')((u32)state + 20); *(s32 *)state = -1; state = ('+typ+')((u32)state - 20);')
        if timing=='afterinvert':c=c.replace('u16 *packet = (u16 *)tail->field_28;\n        u32 inverted = ~sum;', 'u32 inverted = ~sum;\n        u16 *packet = (u16 *)tail->field_28;')
        if timing=='separate':c=c.replace('u32 inverted = ~sum;', 'u32 inverted; inverted = ~sum;')
        yield c


def queue_address():
    s=(ROOT/'tools/search-drafts/func_08015DA8_offsets.c').read_text()
    countforms=[
        'u32 countbase = base; countbase += 8; count = *(u32 *)(offset + countbase);',
        'u32 countbase = base + 8; count = *(u32 *)(offset + countbase);',
        'u32 countbase = base; countbase += 8; countbase = offset + countbase; count = *(u32 *)countbase;',
        'u32 work = base; work += 8; { u32 addend = work; work = offset + addend; } count = *(u32 *)work;']
    for shape,form,init,mask,decl in itertools.product(['do','goto'],countforms,
        ['original','basefirst'],['inline','split','local'],['before','inside']):
        c=s.replace('count = *(u32 *)(base + 8 + offset);','{ '+form+' }')
        if shape=='goto':c=c.replace('do {','loop: {').replace('break;', 'goto done;').replace('} while (i <= 96);','} if (i <= 96) goto loop;').replace('    *(u32 *)base = 0;','done:    *(u32 *)base = 0;')
        if init=='basefirst':c=c.replace('u32 i = 0;\n    u32 base = (u32)g_030061F0;', 'u32 base = (u32)g_030061F0;\n    u32 i = 0;')
        if mask=='split':c=c.replace('dma[2] = (count >> 2) | 0x84000000;', 'count >>= 2; count |= 0x84000000; dma[2] = count;')
        if mask=='local':c=c.replace('dma[2] = (count >> 2) | 0x84000000;', '{ register u32 mask = 0x84000000; count >>= 2; count |= mask; dma[2] = count; }')
        if decl=='before':c=c.replace('u32 dest, count;', 'u32 dest; u32 count;')
        yield c


def packet_helpers():
    s=(ROOT/'docs/near-misses/func_08014988.c').read_text()
    original=s[s.index('    {\n        TxraLinkState *tail'):s.index('    state->field_14')]
    params={'tail':'TxraLinkState *tail','sum':'u32 sum','zero':'u32 zero'}
    args={'tail':'state','sum':'sum','zero':'0'}
    for order in itertools.permutations(['tail','sum','zero']):
        for returns,invert,base in itertools.product(['void','TxraLinkState *'],['local','inline'],['state','&g_03007A30']):
            decl=', '.join(params[x] for x in order)
            arguments=', '.join(base if x=='tail' else args[x] for x in order)
            body='u16 *packet = (u16 *)tail->field_28; u32 inverted = ~sum; packet[1] = inverted; if (tail->field_00) *(vu16 *)0x0400010E = zero;'
            if invert=='inline':body='u16 *packet = (u16 *)tail->field_28; packet[1] = ~sum; if (tail->field_00) *(vu16 *)0x0400010E = zero;'
            if returns!='void':body+=' return tail;'
            helper='static inline '+returns+' apply_packet_tail('+decl+') { '+body+' }\n'
            call=('state = ' if returns!='void' else '')+'apply_packet_tail('+arguments+');'
            yield helper+s.replace(original,'    '+call+'\n')


def queue_work():
    s=(ROOT/'tools/search-drafts/func_08015DA8_offsets.c').read_text()
    for dest,add,mask,order,decl in itertools.product(['expression','work'],['simple','named'],
        ['shiftfirst','maskfirst'],['sourcefirst','countfirst'],['top','loop']):
        c=s.replace('    do {', '    u32 work;\n    do {' if decl=='top' else '    do { u32 work;')
        address='work = base; work += 8; '
        address+=('work = offset + work;' if add=='simple' else '{ u32 addend = work; work = offset + addend; }')
        address+=' count = *(u32 *)work;'
        c=c.replace('count = *(u32 *)(base + 8 + offset);',address)
        if dest=='work':c=c.replace('dest = *(u32 *)(destbase + offset);', 'work = offset + destbase; dest = *(u32 *)work;')
        control='count >>= 2; work = 0x84000000; count |= work; dma[2] = count;'
        if mask=='maskfirst':control='work = 0x84000000; count >>= 2; count |= work; dma[2] = count;'
        c=c.replace('dma[2] = (count >> 2) | 0x84000000;',control)
        if order=='countfirst':c=c.replace('u32 dest, count;', 'u32 count, dest;')
        yield c


def queue_registers():
    s=(ROOT/'docs/match7-search/queue_work/func_08015DA8.c').read_text()
    old='work = offset + destbase; dest = *(u32 *)work;'
    destforms=[old,
        '{ u32 saved_dest = destbase; work = offset + saved_dest; } dest = *(u32 *)work;',
        'work = destbase; { u32 saved_dest = work; work = offset + saved_dest; } dest = *(u32 *)work;',
        'work = destbase; work = offset + work; dest = *(u32 *)work;']
    for form,qual,typ,decl,dma in itertools.product(destforms,['','register '],['u32','s32'],
        ['original','swap','outer','separate'],['original','assign']):
        c=s.replace(old,form).replace('u32 work;',qual+typ+' work;')
        if decl=='swap':c=c.replace('u32 dest, count;', 'u32 count, dest;')
        if decl=='outer':c=c.replace('u32 dest, count;', '').replace('    u32 work;', '    u32 dest, count; u32 work;')
        if decl=='separate':c=c.replace('u32 dest, count;', 'u32 dest; u32 count;')
        if dma=='assign':c=c.replace('        dma[2];','        work = dma[2];')
        yield c


def queue_return():
    s=(ROOT/'docs/match7-search/queue_work/func_08015DA8.c').read_text()
    tail='*(u32 *)base = 0;\n    *(u32 *)endmarker = 0;'
    for typ,zero,ret,dest in itertools.product(['u32','s32','u16'],['work','count','zero'],['return','void'],['original','split']):
        c=s.replace('void func_08015DA8',typ+' func_08015DA8' if ret=='return' else 'void func_08015DA8')
        final=(('u32 zero = 0;' if zero=='zero' else zero+' = 0;')+' *(u32 *)base = '+zero+'; *(u32 *)endmarker = '+zero+';'+(' return '+zero+';' if ret=='return' else ''))
        c=c.replace(tail, '{ '+final+' }')
        if zero=='count':c=c.replace('    u32 work;', '    u32 work, count;').replace('u32 dest, count;', 'u32 dest;')
        if dest=='split':c=c.replace('work = offset + destbase; dest = *(u32 *)work;', 'dest = *(u32 *)(offset + destbase);')
        yield c


def queue_io():
    s=(ROOT/'docs/match7-search/queue_work/func_08015DA8.c').read_text()
    for io,vol,source,control in itertools.product(['array','direct','struct'],
        ['none','all','source','count','dest'],['u32','s32'],['original','invert']):
        c=s.replace('u32 source =',source+' source =')
        if vol in ['all','source']:c=c.replace('*(u32 *)cursor','*(vu32 *)cursor')
        if vol in ['all','count']:c=c.replace('count = *(u32 *)work','count = *(vu32 *)work')
        if vol in ['all','dest']:c=c.replace('dest = *(u32 *)work','dest = *(vu32 *)work')
        if io=='direct':
            for i,addr in enumerate([0x040000D4,0x040000D8,0x040000DC]):c=c.replace('dma['+str(i)+']','(*(vu32 *)0x%08X)'%addr)
        if io=='struct':
            c='typedef struct { vu32 src, dst, control; } TransferPort;\n'+c.replace('vu32 *dma = (vu32 *)0x040000D4;', 'TransferPort *dma = (TransferPort *)0x040000D4;')
            for i,name in enumerate(['src','dst','control']):c=c.replace('dma['+str(i)+']','dma->'+name)
        if control=='invert':c=c.replace('count |= work;', 'count = work | count;')
        yield c


def halfword_decoder():
    s=(ROOT/'docs/match7-search/expanded/func_080123F0.c').read_text()
    for loop,tag,first,mask,literal in itertools.product(['goto','while'],['u32','u16','s32'],
        ['original','direct','temp'],['original','expression','separate'],['original','direct','cast']):
        c=re.sub(r'\b(?:u32|u16|s32) r12;',tag+' r12;',s)
        if loop=='while':
            c=c.replace('L_0801241A:','while (1) {').replace('if ((s32)r7 <= 0) goto L_08012508;\n    if ((s32)r6 > 0) goto L_0801241A;\nL_08012508:','if ((s32)r7 <= 0) break; if ((s32)r6 <= 0) break; }')
        old='r0 = r12;\n    r1 = r9;\n    r0 &= r1;\n    if (r0 != r9)'
        if first=='direct':c=c.replace(old,'if ((r12 & r9) != r9)')
        if first=='temp':c=c.replace(old,'r0 = r12 & r9; if (r0 != r9)')
        oldmask='r3 = r12;\n    r0 = 0x3FFF;\n    r3 &= r0;'
        if mask=='expression':c=c.replace(oldmask,'r3 = r12 & 0x3FFF;')
        if mask=='separate':c=c.replace(oldmask,'r3 = r12; { u32 mask = 0x3FFF; r3 &= mask; }')
        if literal=='direct':c=c.replace('r3 = r12;\n    if (r3 == 0)', 'if (r12 == 0)')
        if literal=='cast':c=c.replace('r1 = r12;', 'r1 = (u16)r12;')
        yield c


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('grid',choices=['packet','blit','angle','queue','packet_aliases','blit_loops','queue_loop','queue_memory','packet_raw','literal_bases','control_flow','blit_declarations','packet_storage','blit_indexed','decode_control','decode_tag','packet_induction','packet_representation','queue_address','packet_helpers','queue_work','queue_registers','queue_return','queue_io','halfword_decoder'])
    ap.add_argument('--profiles',nargs='+',default=['old'])
    ap.add_argument('--jobs',type=int,default=os.cpu_count())
    args=ap.parse_args()
    global CONTROL_ADDRESS
    CONTROL_ADDRESS=int(os.environ.get('MATCH_ADDRESS','08014988'),16)
    global LITERAL_ADDRESS
    LITERAL_ADDRESS=int(os.environ.get('MATCH_ADDRESS','08014988'),16)
    a={'packet':0x08014988,'blit':0x08014104,'angle':0x08014614,'queue':0x08015DA8,'packet_aliases':0x08014988,'blit_loops':0x08014104,'queue_loop':0x08015DA8,'queue_memory':0x08015DA8,'packet_raw':0x08014988,'literal_bases':LITERAL_ADDRESS,'control_flow':CONTROL_ADDRESS,'blit_declarations':0x08014104,'packet_storage':0x08014988,'blit_indexed':0x08014104,'decode_control':0x0801251C,'decode_tag':0x0801251C,'packet_induction':0x08014988,'packet_representation':0x08014988,'queue_address':0x08015DA8,'packet_helpers':0x08014988,'queue_work':0x08015DA8,'queue_registers':0x08015DA8,'queue_return':0x08015DA8,'queue_io':0x08015DA8,'halfword_decoder':0x080123F0}[args.grid]
    prog=vs.draft.Program(); end=vs.comparison_end(prog,a)
    output=ROOT/'docs/match7-search'/(args.grid+('-'+f'{a:08X}' if args.grid in ('control_flow','literal_bases') else ''));output.mkdir(parents=True,exist_ok=True)
    sources=list(dict.fromkeys(globals()[args.grid]()))
    jobs=[(a,end,s,p) for s in sources for p in args.profiles]
    best=None; tried=errors=0; started=time.monotonic()
    os.nice(max(0,10-os.getpriority(os.PRIO_PROCESS,0)))
    with futures.ProcessPoolExecutor(max_workers=args.jobs,initializer=vs.init_worker,initargs=(vs.reloc.symbols(prog),)) as pool:
        for lo in range(0,len(jobs),args.jobs*2):
            wave=jobs[lo:lo+args.jobs*2]
            for job,result in zip(wave,pool.map(vs.compile_job,wave)):
                tried+=1
                sc,size,got,error=result
                if error: errors+=1;continue
                if best is None or sc<best[0]:
                    best=(sc,size,job[2],job[3],got)
                    print(f'{args.grid} trials={tried} score={sc} profile={job[3]}',flush=True)
                    (output/f'func_{a:08X}.c').write_text(job[2])
                if got==prog.rom[a-vs.draft.BASE:end-vs.draft.BASE]: break
            if best and best[0]==(0,0):break
    record={'address':f'{a:08X}','planned_jobs':len(jobs),'attempts':tried,'compile_errors':errors,'seconds':round(time.monotonic()-started,2),'exact':bool(best and best[0]==(0,0))}
    if best:
        sc,size,s,p,got=best
        record.update(score=sc,size=size,compiler=p)
        (output/f'func_{a:08X}.diff.txt').write_text(vs.source_diff(prog.rom[a-vs.draft.BASE:end-vs.draft.BASE],got,a)+'\n')
    (output/'results.json').write_text(json.dumps(record,indent=2)+'\n')

if __name__=='__main__':main()
