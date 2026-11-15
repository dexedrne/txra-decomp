#!/usr/bin/env python3
"""Persistent five-worker source search; only complete byte equality is a match.

The private result cache lives under build/. Checkpoints, sources and instruction
text diffs are safe review artifacts. No service or remote matcher is contacted.
"""
import argparse
from collections import deque
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import re
import sqlite3
import time

import variant_search as v

ROOT = v.ROOT
VERSION = 1


def splice(s, m, replacement):
    return s[:m.start()] + replacement + s[m.end():]


def extra_mutations(s):
    """Structured declaration/expression/control hypotheses, never output edits.

    Width, qualifier and layout hypotheses may change behavior. They must never
    be installed without the independent complete-byte and next-entry checks.
    Assignment reordering is restricted to declared scalar locals, pure scalar
    expressions and no read/write dependency in either direction.
    """
    atom = r'(?:[A-Za-z_]\w*|0x[\da-fA-F]+|\d+)'
    scalar = set()
    for m in v.DECL.finditer(s):
        scalar.update(x.strip() for x in m[4].split(','))
        if not m[2]:
            yield 'qualifier', s[:m.start(3)]+'const '+s[m.start(3):]
        if m[5]:
            yield 'qualifier', s[:m.start(3)]+'volatile '+s[m.start(3):]
    for m in re.finditer(r'\b(?:const|volatile|register)\s+(?=(?:u32|s32|u16|s16|u8|s8|int)\b)',s):
        yield 'qualifier-remove', splice(s,m,'')
    # Bracketed associative expressions, both groupings and constant positions.
    for m in re.finditer(r'\(('+atom+r')\s*([+*&|^])\s*('+atom+r')\)\s*\2\s*('+atom+r')',s):
        yield 'reassociate', splice(s,m,f'{m[1]} {m[2]} ({m[3]} {m[2]} {m[4]})')
    for m in re.finditer(r'('+atom+r')\s*([+*&|^])\s*\(('+atom+r')\s*\2\s*('+atom+r')\)',s):
        yield 'reassociate', splice(s,m,f'({m[1]} {m[2]} {m[3]}) {m[2]} {m[4]}')
    for m in re.finditer(r'\b('+atom+r')\s*\*\s*(2|4|8|16|32|64|128|256)\b',s):
        yield 'shift-multiply', splice(s,m,f'({m[1]} << {int(m[2]).bit_length()-1})')
    for m in re.finditer(r'\b('+atom+r')\s*<<\s*([1-8])\b',s):
        yield 'multiply-shift', splice(s,m,f'({m[1]} * {1<<int(m[2])})')
    for m in re.finditer(r'\b('+atom+r')\s*&\s*(255|65535|0xff|0xffff)\b',s,re.I):
        width='u8' if int(m[2],0) == 255 else 'u16'
        yield 'mask-cast', splice(s,m,f'({width}){m[1]}')
    # Local temp introduction and immediate copy propagation.
    assignment = re.compile(r'(?m)^([ \t]*)(\w+)\s*=\s*([^;{}\n]+);')
    for m in assignment.finditer(s):
        if m[2] not in scalar or re.search(r'\b(?:sizeof|return)\b',m[3]): continue
        if 'search_temp' not in s and len(s)<12000:
            for typ in ('u32','s32','u16','s16'):
                yield 'temporary-introduce', splice(s,m, m[1]+'{ '+typ+' search_temp = '+m[3]+'; '+m[2]+' = search_temp; }')
    copy=re.compile(r'(?m)^([ \t]*)(\w+) = (\w+);\s*\n([ \t]*)(\w+) = ([\w +<>&|^()\-]+);')
    for m in copy.finditer(s):
        if {m[2],m[3],m[5]} <= scalar and m[2] != m[5] and re.search(r'\b'+m[2]+r'\b',m[6]):
            expr=re.sub(r'\b'+m[2]+r'\b',m[3],m[6])
            # Keep the copy: it can still be live after the next assignment.
            yield 'temporary-propagate', splice(s,m,f'{m[1]}{m[2]} = {m[3]};\n{m[4]}{m[5]} = {expr};')
    pair=re.compile(r'(?m)^([ \t]*)(\w+) = ([\w +<>&|^()\-]+);\s*\n([ \t]*)(\w+) = ([\w +<>&|^()\-]+);')
    for m in pair.finditer(s):
        names=set(re.findall(r'\b[A-Za-z_]\w*\b',m[3]+' '+m[6]))
        if not {m[2],m[5]}<=scalar or not names<=scalar:continue
        if m[2]==m[5] or re.search(r'\b'+m[2]+r'\b',m[6]) or re.search(r'\b'+m[5]+r'\b',m[3]):continue
        # Parentheses are allowed for casts/grouping, never calls.
        if re.search(r'\w\s*\(',m[3]+m[6]):continue
        yield 'independent-order', splice(s,m,f'{m[1]}{m[5]} = {m[6]};\n{m[4]}{m[2]} = {m[3]};')
    for m in re.finditer(r'\b(\w+)\[('+atom+r')\]',s):
        # Exclude declarations, array fields and global extern declarations.
        line=s[max(s.rfind(';',0,m.start()),s.rfind('\n',0,m.start()))+1:m.start()]
        if re.search(r'\b(?:extern|u8|u16|u32|s8|s16|s32|int)\b|[.>]',line):continue
        yield 'array-pointer', splice(s,m,f'*({m[1]} + {m[2]})')
    for m in re.finditer(r'\*\((\w+)\s*\+\s*('+atom+r')\)',s):
        yield 'pointer-array', splice(s,m,f'{m[1]}[{m[2]}]')
    for m in re.finditer(r'\b(\w+)\s*\+=\s*(2|4|8|12);',s):
        # Integer address with equivalent explicitly scaled pointer increment.
        if m[1] in scalar:
            for typ,width in [('u8',1),('u16',2),('u32',4)]:
                if int(m[2])%width==0:
                    yield 'address-pointer', splice(s,m,f'{m[1]} = (u32)(({typ} *){m[1]} + {int(m[2])//width});')
    # The existing three-word record is a reviewed template, never a new global layout.
    for m in re.finditer(r'\*\(u32 \*\)\((\w+) \+ (0|4|8)\)',s):
        yield 'offset-field',splice(s,m,'((TxraTransfer *)'+m[1]+')->field_'+format(int(m[2]),'02x'))
    for m in re.finditer(r'\(\(TxraTransfer \*\)(\w+)\)->field_(00|04|08)',s):
        yield 'field-offset',splice(s,m,'*(u32 *)('+m[1]+' + '+str(int(m[2],16))+')')
    for m in re.finditer(r'(?m)^(\s*)(\w+) = (\w+);',s):
        if {m[2],m[3]}<=scalar:
            for typ in ('u8','u16','u32','s16','s32'):
                yield 'widen-narrow',splice(s,m,m[1]+m[2]+' = ('+typ+')'+m[3]+';')
    # Complete brace-delimited if/else, including conditions with nested parens.
    for m in re.finditer(r'\bif\s*\(',s):
        pend=v.balanced_end(s,m.end()-1,'(',')')
        if pend is None:continue
        brace=pend+1
        while brace<len(s) and s[brace].isspace():brace+=1
        if brace>=len(s) or s[brace]!='{':continue
        close=v.balanced_end(s,brace,'{','}')
        if close is None:continue
        tail=re.match(r'\s*else\s*\{',s[close+1:])
        if not tail:continue
        other=close+1+tail.end()-1; end=v.balanced_end(s,other,'{','}')
        if end is None:continue
        cond=s[m.end():pend]; yes=s[brace+1:close]; no=s[other+1:end]
        yield 'if-invert',s[:m.start()]+'if (!('+cond+')) {'+no+'} else {'+yes+'}'+s[end+1:]
        if re.search(r'\breturn\s*[^;]*;\s*$',yes):
            yield 'early-return',s[:m.start()]+'if ('+cond+') {'+yes+'}\n'+no+s[end+1:]
    # Independent constant tests on the same selector -> switch hypothesis.
    case=re.compile(r'if\s*\((\w+)\s*==\s*(0x[\da-fA-F]+|\d+)\)\s*\{([^{}]*)\}')
    matches=list(case.finditer(s))
    for i,first in enumerate(matches):
        chain=[first]
        for nxt in matches[i+1:]:
            if nxt[1]!=first[1] or s[chain[-1].end():nxt.start()].strip():break
            if re.search(r'\b'+first[1]+r'\s*(?:=|\+\+|--|[+\-*/&|^]=)',chain[-1][3]):break
            chain.append(nxt)
        if len(chain)>1:
            out='switch ('+first[1]+') {'+''.join('case '+c[2]+': {'+c[3]+'} break;\n' for c in chain)+'}'
            yield 'if-switch',s[:first.start()]+out+s[chain[-1].end():]
    for m in re.finditer(r'switch\s*\((\w+)\)\s*\{',s):
        end=v.balanced_end(s,m.end()-1,'{','}')
        if end is None:continue
        body=s[m.end():end]
        cases=list(re.finditer(r'case\s+(\d+|0x[\da-fA-F]+)\s*:\s*\{([^{}]*)\}\s*break;',body))
        if not cases or re.sub(r'case\s+(\d+|0x[\da-fA-F]+)\s*:\s*\{([^{}]*)\}\s*break;','',body).strip():continue
        out=' else '.join('if ('+m[1]+' == '+c[1]+') {'+c[2]+'}' for c in cases)
        yield 'switch-if',s[:m.start()]+out+s[end+1:]
    # Inline versus an ordinary local helper call; only existing helpers.
    for m in re.finditer(r'\bstatic\s+(inline\s+)?(u32|s32|u16|s16|void)\s+(\w+)\s*\(',s):
        yield 'helper-inline', s[:m.start()]+('static ' if m[1] else 'static inline ')+s[m.start(2):]
    # Local struct layout hypotheses only. Global reviewed types are never edited.
    for m in re.finditer(r'struct\s+\w*\s*\{([^{}]+)\}',s):
        fields=[x.strip() for x in m[1].split(';') if x.strip()]
        if len(fields)>1 and all(re.fullmatch(r'(?:u32|s32|u16|s16|u8|s8)\s+\w+',x) for x in fields):
            for i in range(len(fields)-1):
                swapped=fields[:];swapped[i],swapped[i+1]=swapped[i+1],swapped[i]
                yield 'local-struct-order',s[:m.start(1)]+'; '.join(swapped)+';'+s[m.end(1):]


def neighborhood(source,rng):
    # Learned successful transformations always enter the queue first.
    preferred=[(n,v.split_declarations(s)) for n,s in v.matching_patterns.transformations(source)]
    ordinary=[('base',v.split_declarations(s)) for s in itertools.islice(v.mutations(source,rng),1800)]
    ordinary.extend((n,v.split_declarations(s)) for n,s in extra_mutations(source))
    rng.shuffle(ordinary)
    seen={source};result=[]
    for name,s in preferred+ordinary:
        if s not in seen and len(s)<16000:
            seen.add(s);result.append((name,s))
    return result


def atomic_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');tmp.replace(path)


def fingerprint():
    h=hashlib.sha256()
    arm_cc=Path(v.judge.CC).with_name('agbcc_arm')
    h.update(b'arm-compiler\0'+(arm_cc.read_bytes() if arm_cc.is_file() else b'missing'))
    files=[Path(v.judge.CC),Path(v.judge.CC).with_name('agbcc'),*[Path(v.judge.ARM+x) for x in ('gcc','as','objcopy','objdump')],ROOT/'baserom.gba',ROOT/'tools/rom.cfg',ROOT/'src/types.h',Path(__file__),ROOT/'tools/variant_search.py',ROOT/'tools/matching_patterns.json',ROOT/'tools/matching_patterns.py',ROOT/'tools/reloc.py',ROOT/'tools/diffhint.py',ROOT/'recomp/draft.py']
    for p in files:h.update(p.read_bytes())
    h.update(v.judge.PRELUDE.encode())
    return h.hexdigest()


def choose_targets(prog,count):
    ranks={r['address']:r for r in v.rank_targets.rank(prog,*v.rank_targets.coverage_evidence(ROOT/'docs/map'))}
    candidates={}
    for folder in ('docs/near-misses','docs/match7-search','docs/match9-search'):
        for p in sorted((ROOT/folder).rglob('*.json')):
            try:r=json.loads(p.read_text())
            except (ValueError,OSError):continue
            if not isinstance(r,dict):continue
            a=str(r.get('address',p.stem.removeprefix('func_'))).upper().removeprefix('0X')
            if a not in ranks or ranks[a]['blocked_reason'] or not r.get('score'):continue
            src=p.with_name('func_'+a+'.c')
            if not src.exists():continue
            row={'address':a,'prior_score':r['score'],'source':str(src.relative_to(ROOT)),'rank':ranks[a]}
            if a not in candidates or row['prior_score']<candidates[a]['prior_score']:candidates[a]=row
    return sorted(candidates.values(),key=lambda r:r['prior_score'])[:count]


def worker_init(table):
    v.init_worker(table)
    os.nice(max(0,15-os.getpriority(os.PRIO_PROCESS,0)))


def restore_rng(value):
    return tuple(restore_rng(x) if isinstance(x,list) else x for x in value)


def search(pool,prog,target,args,db,context):
    a=int(target['address'],16); end=v.comparison_end(prog,a)
    mode=prog.by_start[a]['mode'];profiles=v.profiles_for_mode(mode)
    dest=args.output/target['address']; dest.mkdir(parents=True,exist_ok=True)
    checkpoint=dest/'checkpoint.json'
    rng=random.Random(args.seed+a)
    sources=v.seeds(prog,a,target['source'])
    # All historical hypotheses for this entry, not just the closest seed.
    for folder in ('docs/match7-search','docs/match9-search','tools/search-drafts'):
        sources.extend(p.read_text() for p in sorted((ROOT/folder).rglob('func_%08X*.c'%a)))
    sources=list(dict.fromkeys(v.split_declarations(s) for s in sources))
    state={'address':target['address'],'seed':args.seed+a,'seconds':0.,'attempts':0,'compiled':0,'cache_hits':0,'errors':0,'restarts':0,'equal_moves':0,'best':None,'elite':[],'current':None,'generation':0,'context':context,'operators':{}}
    if checkpoint.exists():
        state=json.loads(checkpoint.read_text())
        if state['context']!=context:raise ValueError('checkpoint context changed; choose a fresh output directory')
        rng.setstate(restore_rng(state['rng']))
    pending=deque((s,p,'seed') for s in sources for p in profiles)
    started=time.monotonic();previous=state['seconds'];lastlog=-1;stall=0
    history=dest/'history.jsonl'
    def save():
        state['seconds']=previous+time.monotonic()-started
        state['rng']=rng.getstate()
        atomic_json(checkpoint,state)
        public={k:val for k,val in state.items() if k not in ('elite','current','rng','context','best')}
        best=state['best']
        public['best_score']=best['score'] if best else None
        public['compiler']=best['profile'] if best else None
        public['exact']=bool(best and best['score']==[0,0])
        public['variants_per_second']=round(state['attempts']/max(.001,state['seconds']),2)
        atomic_json(dest/'result.json',public)
        with history.open('a') as f:f.write(json.dumps({k:public[k] for k in ('seconds','attempts','compiled','cache_hits','errors','restarts','equal_moves','best_score','variants_per_second')})+'\n')
        print(json.dumps({'address':target['address'],**{k:public[k] for k in ('seconds','attempts','best_score','variants_per_second')}}),flush=True)
    while previous+time.monotonic()-started<args.seconds:
        if not pending:
            state['generation']+=1
            if state['current'] and stall<20 and state['generation']%12:
                parent=state['current']
            elif state['elite'] and state['generation']%4:
                parent=rng.choice(state['elite'])
            else:
                state['restarts']+=1
                parent={'source':rng.choice(sources),'profile':rng.choice(profiles)}
            variants=neighborhood(parent['source'],rng)
            if state['generation']%4==0:
                s=parent['source']
                for _ in range(rng.randint(2,6)):
                    opts=neighborhood(s,rng)
                    if not opts:break
                    _,s=rng.choice(opts)
                variants=neighborhood(s,rng)+variants
            pending.extend((s,parent['profile'],op) for op,s in variants)
            pending.extend((parent['source'],p,'profile') for p in profiles)
            # Limit retained speculative queue to keep every parent reachable.
            if not pending:continue
        wave=[];cached=[]
        # Persistent cache prevents re-compilation of any repeated source/profile.
        for _ in range(min(30,len(pending))):
            source,profile,op=pending.popleft()
            key=hashlib.sha256((context+target['address']+profile+source).encode()).hexdigest()
            found=db.execute('SELECT result FROM cache WHERE key=?',(key,)).fetchone()
            item=(source,profile,op,key)
            if found:cached.append((item,json.loads(found[0])))
            else:wave.append(item)
        # Cached paths cannot create an unbounded CPU-only plateau loop.
        results=[]
        jobs=[(a,end,s,p) for s,p,_,_ in wave]
        for item,(score,size,got,error) in zip(wave,pool.map(v.compile_job,jobs)):
            result={'score':list(score) if score is not None else None,'size':size,'error':error}
            db.execute('INSERT OR IGNORE INTO cache VALUES (?,?)',(item[3],json.dumps(result)))
            results.append((item,result))
        db.commit();state['compiled']+=len(wave);state['cache_hits']+=len(cached)
        for (source,profile,op,key),result in results+cached:
            state['attempts']+=1;state['operators'][op]=state['operators'].get(op,0)+1
            if result['error']:state['errors']+=1;continue
            entry={'source':source,'profile':profile,'score':result['score'],'size':result['size']}
            if state['best'] is None or entry['score']<state['best']['score']:
                state['best']=entry;stall=0
                (dest/('func_%08X.c'%a)).write_text(source)
                # Full uncached comparison supplies the retained diff, never cache guesses.
                _,_,_,want,got=v.judge.compile_candidate(source,'func_%08X'%a,a,a+65536,v.reloc.symbols(prog),target_end=end,compiler=profile,rom=prog.rom)
                (dest/('func_%08X.diff.txt'%a)).write_text('Compiler: '+profile+'\n'+v.source_diff(bytes.fromhex(want)[:end-a],bytes.fromhex(got),a,mode=mode)+'\n')
                save()
            current=state['current']
            if current is None or entry['score']<current['score'] or (entry['score']==current['score'] and rng.random()<.35):
                if current and entry['score']==current['score']:state['equal_moves']+=1
                state['current']=entry
            if not any(e['source']==source and e['profile']==profile for e in state['elite']):
                state['elite'].append(entry);state['elite'].sort(key=lambda e:e['score']);state['elite']=state['elite'][:12]
        stall+=1
        # Keep spending the assigned wall budget even after a match; compilation
        # of further source variants is useful evidence, installation is separate.
        elapsed=previous+time.monotonic()-started
        if elapsed-lastlog>=30:save();lastlog=elapsed
    save()
    return json.loads((dest/'result.json').read_text())


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--seconds',type=float,default=1500)
    ap.add_argument('--count',type=int,default=12)
    ap.add_argument('--active-targets',type=int,default=5,choices=range(1,6),help='concurrent timed target windows, sharing the fixed five compiler processes')
    ap.add_argument('--seed',type=int,default=101029)
    ap.add_argument('--output',type=Path,default=Path('docs/match10-search'))
    args=ap.parse_args()
    if args.seconds<=0 or args.count<=0:ap.error('positive seconds/count required')
    os.nice(max(0,15-os.getpriority(os.PRIO_PROCESS,0)))
    prog=v.draft.Program();context=fingerprint()
    args.output.mkdir(parents=True,exist_ok=True)
    manifest=args.output/'targets.json'
    targets=json.loads(manifest.read_text()) if manifest.exists() else choose_targets(prog,args.count)
    atomic_json(manifest,targets)
    (ROOT/'build').mkdir(exist_ok=True)
    db=sqlite3.connect(ROOT/'build/search10-cache.sqlite',timeout=120)
    db.execute('PRAGMA journal_mode=WAL')
    db.execute('CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, result TEXT NOT NULL)')
    db.commit();db.close()
    results=[]
    # Target scheduling uses threads only; all compilation runs in this one fixed
    # five-process pool. Each target gets >= seconds of its own wall-clock window.
    # Time includes competition for that shared pool; it is not exclusive CPU time.
    with ProcessPoolExecutor(max_workers=5,initializer=worker_init,initargs=(v.reloc.symbols(prog),)) as pool:
        # Fork before scheduler threads exist.
        def run_target(target):
            notes=ROOT/'OWNER-NOTES.md'
            if notes.exists():print(notes.read_text(),flush=True)
            conn=sqlite3.connect(ROOT/'build/search10-cache.sqlite',timeout=120)
            try:return search(pool,prog,target,args,conn,context)
            finally:conn.close()
        # Start process workers before starting the thread scheduler.
        ready=[pool.submit(time.time) for _ in range(5)]
        for f in ready:f.result()
        with ThreadPoolExecutor(max_workers=args.active_targets) as scheduler:
            tasks=[scheduler.submit(run_target,target) for target in targets]
            for done in as_completed(tasks):
                results.append(done.result())
                atomic_json(args.output/'summary.json',sorted(results,key=lambda r:r['address']))
    return 0

if __name__=='__main__':raise SystemExit(main())
