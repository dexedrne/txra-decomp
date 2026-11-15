#!/usr/bin/env python3
"""Bounded, reproducible compiler search. No service requests or ROM bytes saved.

Search one draft: variant_search.py ADDRESS draft.c --budget 4000
Search ranked complete 8-60-instruction entries: variant_search.py --all
Winners remain reviewable until --install explicitly requests full-ROM validation.
"""
import argparse
import concurrent.futures as futures
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import re
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'recomp')]
import diffhint
import draft
import llm_match as judge
import rank_targets
import reloc
import matching_patterns

COMPILE_CACHE = {}
ROM = None
PROFILES = ('old', 'standard', 'old-no-gcse', 'old-o1', 'standard-o1',
            'old-no-interwork', 'arm', 'modern-arm')


def profiles_for_mode(mode):
    return tuple(p for p in PROFILES if (p in ('arm', 'modern-arm')) == (mode == 'arm'))

DECL = re.compile(r'(?m)^([ \t]*)(register\s+)?(u32|s32|int|u16|s16|u8)\s+((?:r\d+|[a-zA-Z_]\w*)(?:\s*,\s*\w+)*)(\s*=\s*[^;\n]+)?\s*;')


def instruction_tokens(code, start, mode='thumb'):
    # Include register operands, constants and pools. Ignore absolute listing
    # addresses: one inserted instruction must cost one, not every later row.
    return [re.sub(r'^\w+:\s*(?:[0-9A-F]{4,8}\s+)?', '', s).strip()
            for s in diffhint.listing(code, start, mode)]


def edit_distance(a, b):
    row = list(range(len(b)+1))
    for i, x in enumerate(a, 1):
        nxt = [i]
        for j, y in enumerate(b, 1):
            nxt.append(min(nxt[-1]+1, row[j]+1, row[j-1]+(x != y)))
        row = nxt
    return row[-1]


def score(want, got, start, mode='thumb'):
    return (edit_distance(instruction_tokens(want, start, mode), instruction_tokens(got, start, mode)),
            sum(x != y for x, y in zip(want, got)) + abs(len(want)-len(got)))


def split_declarations(code):
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)
    # Normalize compact drafts without breaking semicolons inside for headers.
    out=[]; parens=0
    for c in code:
        parens += (c == '(') - (c == ')')
        out.append(c)
        if c in '{};' and parens == 0:
            out.append('\n')
    code=re.sub(r'\n[ \t]*\n+', '\n', ''.join(out))
    return DECL.sub(lambda m: '\n'.join('%s%s%s %s%s;' %
        (m[1], m[2] or '', m[3], n.strip(), m[5] or '') for n in m[4].split(',')), code)



def balanced_end(code, start, opening, closing):
    depth=0
    for index in range(start,len(code)):
        depth += (code[index]==opening) - (code[index]==closing)
        if depth==0: return index
    return None


def loop_mutations(code):
    for m in re.finditer(r'\b(for|while)\s*\(',code):
        begin=m.end()-1
        end=balanced_end(code,begin,'(',')')
        if end is None: continue
        brace=end+1
        while brace<len(code) and code[brace].isspace(): brace+=1
        if brace>=len(code) or code[brace]!='{': continue
        close=balanced_end(code,brace,'{','}')
        if close is None: continue
        condition=code[begin+1:end]
        body=code[brace+1:close]
        if m[1]=='for':
            parts=condition.split(';')
            if len(parts)!=3 or re.search(r'\bcontinue\b',body): continue
            init,test,step=parts
            replacement='{'+init+'; while ('+(test.strip() or '1')+') {'+body+step+';}}'
        else:
            # Entry guard preserves zero-iteration behavior and IO read count.
            replacement='if ('+condition+') do {'+body+'} while ('+condition+');'
        yield code[:m.start()]+replacement+code[close+1:]


def mutations(code, rng):
    """Local neighborhoods; exact comparison, never the rewrite, proves acceptance.

    Width changes are hypotheses about original declarations; they need not be
    semantically equivalent for values outside this function's actual domain.
    No assembly, register bindings, output patches or artificial side effects.
    """
    code = split_declarations(code)
    ds = list(DECL.finditer(code))
    for m in ds:
        for typ in ('u32', 's32', 'int', 'u16', 's16', 'u8'):
            yield code[:m.start(3)] + typ + code[m.end(3):]
        yield code[:m.start()] + m[1] + ('' if m[2] else 'register ') + m[3] + ' ' + m[4] + (m[5] or '') + ';' + code[m.end():]
    # Initialization at declaration versus a following assignment can change
    # pseudo-register creation order on the historical compiler.
    for m in ds:
        if m[5] and ',' not in m[4]:
            yield code[:m.start()] + '%s%s%s %s;\n%s%s%s;' % (m[1],m[2] or '',m[3],m[4],m[1],m[4],m[5]) + code[m.end():]
    # Declaration permutation can affect allocation even for identical lifetimes.
    if len(ds) > 1 and not re.sub(DECL, '', code[ds[0].end():ds[-1].start()]).strip():
        for _ in range(min(16, len(ds)*2)):
            texts = [m.group() for m in ds]; rng.shuffle(texts)
            out = code
            for m, val in reversed(list(zip(ds, texts))):
                out = out[:m.start()] + val + out[m.end():]
            yield out
    # Pairwise declaration swaps keep close allocation alternatives reachable.
    # Restrict to a contiguous declaration run so variables never change scope.
    for i, first in enumerate(ds):
        for second in ds[i+1:]:
            middle=code[first.end():second.start()]
            if re.sub(DECL, '', middle).strip():
                break
            yield (code[:first.start()]+second.group()+middle+
                   first.group()+code[second.end():])
    # Provisional signature hypotheses; final byte equality protects the machine ABI.
    ret = re.search(r'\b(u32|s32|int|u16|s16|u8)\s+func_[0-9A-F]+\(',code)
    if ret:
        for typ in ('u32','s32','int','u16','s16','u8'):
            yield code[:ret.start(1)]+typ+code[ret.end(1):]
    sig = re.search(r'\bfunc_[0-9A-F]+\(([^)]*)\)', code)
    if sig:
        params=sig[1].split(',')
        for index in range(len(params)-1):
            reordered=params[:]
            reordered[index],reordered[index+1]=reordered[index+1],reordered[index]
            yield code[:sig.start(1)]+', '.join(p.strip() for p in reordered)+code[sig.end(1):]
        for m in re.finditer(r'\b(u32|s32|int|u16|s16|u8)\b', sig[1]):
            for typ in ('u32','s32','u16','s16','u8','int'):
                lo, hi = sig.start(1)+m.start(), sig.start(1)+m.end()
                yield code[:lo]+typ+code[hi:]
    # Expand/fold compound assignments.
    for m in re.finditer(r'\b(\w+)\s*(<<|>>|[+\-*&|^])=\s*([^;]+);', code):
        yield code[:m.start()] + '%s = %s %s (%s);' % (m[1],m[1],m[2],m[3]) + code[m.end():]
    for m in re.finditer(r'\b(\w+) = \1 ([+\-*&|^]|<<|>>) ([^;]+);', code):
        yield code[:m.start()] + '%s %s= %s;' % (m[1],m[2],m[3]) + code[m.end():]
    # Commutative arithmetic and separated temporaries affect evaluation order.
    for m in re.finditer(r'\b(\w+)\s*([+*&|^])\s*(\w+)\b',code):
        if m[1] != m[3]:
            yield code[:m.start()]+m[3]+' '+m[2]+' '+m[1]+code[m.end():]
    # Explicit scalar cast neighborhoods.
    for m in re.finditer(r'\((u32|s32|u16|s16|u8|s8)\)(\w+)', code):
        for typ in ('u32','s32','u16','s16','u8'):
            yield code[:m.start(1)] + typ + code[m.end(1):]
        yield code[:m.start()] + m[2] + code[m.end():]
    # Folded constant expressions and index vs pointer access.
    for m in re.finditer(r'\b0x[0-9A-Fa-f]+\b', code):
        v = int(m[0],16)
        if v and v & (v-1) == 0:
            yield code[:m.start()] + '(1U << %d)' % (v.bit_length()-1) + code[m.end():]
        yield code[:m.start()] + str(v) + 'U' + code[m.end():]
    for m in re.finditer(r'\*\((v?u(?:8|16|32)) \*\)\((\w+) \+ ([^()]+)\)', code):
        size={'8':1,'16':2,'32':4}[re.search(r'\d+',m[1])[0]]
        yield code[:m.start()] + '((%s *)%s)[(%s)/%d]' % (m[1],m[2],m[3],size) + code[m.end():]
    # IO volatility only; ordinary RAM/ROM reads must not acquire side effects.
    for m in re.finditer(r'\((v?u(?:8|16|32)) \*\)0x040[0-9A-Fa-f]+', code):
        typ=m[1]; typ=typ[1:] if typ.startswith('v') else 'v'+typ
        yield code[:m.start(1)]+typ+code[m.end(1):]
    # Adjacent independent scalar assignments (do not reorder loads/stores/calls).
    pat=r'(?m)^( +)(\w+) = ([\w +<>&|^()\-]+);\n\1(\w+) = ([\w +<>&|^()\-]+);'
    scalars={n.strip() for d in ds for n in d[4].split(',')}
    for m in re.finditer(pat,code):
        names=set(re.findall(r'\b[A-Za-z_]\w*\b',m[3]+' '+m[5]))
        if (not {m[2],m[4]} <= scalars or not names <= scalars
                or re.search(r'\w\s*\(',m[3]+m[5])):
            continue
        if m[2] != m[4] and not re.search(r'\b'+m[2]+r'\b',m[5]) and not re.search(r'\b'+m[4]+r'\b',m[3]):
            yield code[:m.start()]+'%s%s = %s;\n%s%s = %s;' % (m[1],m[4],m[5],m[1],m[2],m[3])+code[m.end():]
    # Structured loop and early-return shapes, conservative supported forms.
    yield from loop_mutations(code)
    for m in re.finditer(r'while\s*\(([^()]+)\)\s*\{',code):
        yield code[:m.start()]+'for (; %s;) {' % m[1]+code[m.end():]
    for m in re.finditer(r'for\s*\(\s*;\s*([^;()]+);\s*\)\s*\{',code):
        yield code[:m.start()]+'while (%s) {' % m[1]+code[m.end():]
    for m in re.finditer(r'do\s*\{([^{}]*)\}\s*while\s*\(([^()]+)\);',code):
        yield code[:m.start()]+'for (;;) {'+m[1]+'\nif (!(%s)) break;\n}' % m[2]+code[m.end():]
    for m in re.finditer(r'if\s*\(([^()]+)\)\s*return ([^;]+);\s*return ([^;]+);',code):
        yield code[:m.start()]+'if (%s) { return %s; } else { return %s; }' % (m[1],m[2],m[3])+code[m.end():]


def source_diff(want, got, address, mode='thumb'):
    # Reviewable instruction text and constants, without raw instruction words.
    return re.sub(r'(?m)^([ +-]?[0-9A-F]{8}:)\s+[0-9A-F]{4,8}\s+',
                  r'\1 ', diffhint.hint(want,got,address,rows=10000,mode=mode))


def init_worker(table):
    global SYMBOLS, ROM
    SYMBOLS = table
    ROM = (ROOT/'baserom.gba').read_bytes()
    os.nice(max(0, 10-os.getpriority(os.PRIO_PROCESS, 0)))


def compile_job(job):
    address, end, source, profile = job
    try:
        # Retain oversize near misses so search can descend toward target length.
        _, size, _, expected, actual = judge.compile_candidate(source, 'func_%08X'%address,
             address, address+65536, SYMBOLS, target_end=end, compiler=profile, cache=COMPILE_CACHE, rom=ROM)
        want, got = bytes.fromhex(expected)[:end-address], bytes.fromhex(actual)
        return score(want, got, address,mode='arm' if profile in ('arm','modern-arm') else 'thumb'), size, got, None
    except Exception as exc:
        # Never include absolute temporary paths, compiler dumps or ROM content.
        return None, 0, None, type(exc).__name__


def seeds(prog, address, supplied=None):
    if supplied:
        return [split_declarations(Path(supplied).read_text())]
    paths = [ROOT/'tools/search-drafts'/('func_%08X.c'%address), ROOT/'docs/near-misses'/('func_%08X.c'%address), ROOT/'tools/trials'/('func_%08X.c'%address)]
    paths.extend(sorted((ROOT/'tools/search-drafts').glob('func_%08X_*.c'%address)))
    out = [p.read_text() for p in paths if p.exists()]
    calls = '\n'.join('extern %s %s(%s);' % ('u32' if prog.returns(a) else 'void',prog.name(a),
                    ', '.join(['u32']*prog.params(a)) or 'void') for a in prog.callees.get(address,()))
    text = re.sub(r'^/\*.*?\*/\s*', '', draft.draft(prog,address), count=1, flags=re.S)
    out.append(calls+'\n'+text)
    try:
        out.extend(judge.leafgen.generate(prog,address))
    except judge.leafgen.Unsupported:
        pass
    return list(dict.fromkeys(split_declarations(s) for s in out))


def comparison_end(prog, address):
    return max(int(prog.by_start[address]['end'],16),
               max(draft.pool_words(prog,address),default=address-4)+4)


def search(pool, prog, row, source, budget, beam, output, focus=None, seconds=None):
    a=int(row['address'],16); end=comparison_end(prog,a)
    original=prog.rom[a-draft.BASE:end-draft.BASE]
    rng=random.Random(a); seen=set(); elite=[]; tried=errors=0; started=time.monotonic()
    profiles=profiles_for_mode(prog.by_start[a]['mode'])
    initial=seeds(prog,a,source)
    learned_counts={}
    deadline=started+seconds if seconds is not None else float("inf")
    neighborhoods={}
    def neighborhood(s):
        if time.monotonic() >= deadline:
            return []
        s=split_declarations(s)
        if len(s) > 8192:
            return []
        if s in neighborhoods:
            return neighborhoods[s]
        preferred=[]
        for pattern, candidate in matching_patterns.transformations(s):
            candidate=split_declarations(candidate)
            if matching_patterns.touches_focus(s,candidate,focus):
                preferred.append(candidate)
                learned_counts[pattern]=learned_counts.get(pattern,0)+1
        ordinary=[split_declarations(c) for c in itertools.islice(mutations(s,rng),512)]
        rng.shuffle(ordinary)
        result=list(dict.fromkeys(preferred+[c for c in ordinary
            if matching_patterns.touches_focus(s,c,focus)]))
        if len(neighborhoods)>=64: neighborhoods.pop(next(iter(neighborhoods)))
        neighborhoods[s]=result
        return result
    pending=[(s,p) for s in initial for p in profiles]
    pending.extend((candidate,p) for s in initial for candidate in neighborhood(s) for p in profiles)
    best=None; stagnant=0; escapes=0; generations=0
    while pending and tried < budget and generations < 64 and time.monotonic() < deadline:
        generations+=1
        jobs=[]
        for s,p in pending:
            h=hashlib.sha256((p+'\0'+s).encode()).hexdigest()
            if h not in seen:
                seen.add(h); jobs.append((a,end,s,p))
            if len(jobs) >= budget-tried: break
        if not jobs:
            if not elite or escapes >= 8:
                break
            escapes += 1
            pending=[]
            for e in elite:
                for _ in range(8):
                    s=e[1]
                    for depth in range(2+escapes%3):
                        opts=neighborhood(s)
                        if opts: s=rng.choice(opts)
                    pending.append((s,rng.choice(profiles)))
            continue
        improved=False
        # Bounded waves prevent a huge speculative queue surviving an exact match.
        for lo in range(0,len(jobs),max(1,os.cpu_count() or 1)*2):
            wave=jobs[lo:lo+max(1,os.cpu_count() or 1)*2]
            for job,result in zip(wave,pool.map(compile_job,wave)):
                tried+=1
                sc,size,got,error=result
                if error: errors+=1; continue
                entry=(sc,job[2],job[3],size,got)
                elite.append(entry)
                if best is None or sc < best[0]:
                    best=entry; improved=True
                    output.mkdir(parents=True,exist_ok=True)
                    (output/('func_%08X.c'%a)).write_text(job[2])
                    print('%08X trials=%d instructions=%d bytes=%d profile=%s' % (a,tried,*sc,job[3]),flush=True)
                if got == original:
                    break
            if best and best[4] == original: break
        elite=sorted(elite,key=lambda e:e[0])
        # Preserve source diversity; otherwise five identical profiles crowd beam.
        unique={}
        for e in elite:
            unique.setdefault(e[1],e)
        elite=list(unique.values())[:beam]
        if best and best[4] == original: break
        stagnant=0 if improved else stagnant+1
        pending=[]
        for e in elite:
            variants=neighborhood(e[1])
            # Include alternate flags for each improved source as well as local edits.
            pending.extend((e[1],p) for p in profiles)
            pending.extend((s,e[2]) for s in variants)
        if stagnant >= 3:
            # Multi-edit escape from a local minimum, reproducible per target.
            for e in elite:
                s=e[1]
                for _ in range(6):
                    opts=neighborhood(s)
                    if not opts: break
                    s=rng.choice(opts); pending.append((s,rng.choice(profiles)))
        # Parent-source round robin rather than letting one beam consume budget.
        # Keep learned transformations ahead of the ordinary randomized neighborhood.
    record={**row,'comparison_bytes':end-a,'attempts':tried,'compile_errors':errors,'seconds':round(time.monotonic()-started,2),
            'status':'exact' if best and best[4]==original else ('time limit' if time.monotonic()>=deadline else ('budget exhausted' if tried>=budget else 'neighborhood exhausted')),'exact':bool(best and best[4]==original),
            'focus':focus,'seconds_limit':seconds,'learned_candidates':learned_counts,'generations':generations}
    output.mkdir(parents=True,exist_ok=True)
    if best:
        sc,s,p,size,got=best
        record.update(score=list(sc),compiler=p,size=size)
        (output/('func_%08X.c'%a)).write_text(s)
        (output/('func_%08X.diff.txt'%a)).write_text('Compiler: %s\nInstruction edit distance: %d\nByte distance: %d\n' % (p,*sc)+source_diff(original,got,a,mode=prog.by_start[a]['mode'])+'\n')
    else:
        (output/('func_%08X.c'%a)).write_text(seeds(prog,a,source)[0])
        (output/('func_%08X.diff.txt'%a)).write_text('No draft compiled successfully; inspect provisional signature and body.\n')
    (output/('func_%08X.json'%a)).write_text(json.dumps(record,indent=2)+'\n')
    return record


def save_rejection(prog, row, output):
    address=int(row['address'],16)
    dest=output/'rejected'; dest.mkdir(parents=True,exist_ok=True)
    name='func_%08X'%address
    (dest/(name+'.c')).write_text('/* Diagnostic lifted draft only; not a compilable near match.\n * Rejection: '+row['blocked_reason']+'\n */\n'+draft.draft(prog,address))
    (dest/(name+'.diff.txt')).write_text('Rejected before compilation: '+row['blocked_reason']+'\nNo compiled comparison exists for this entry. See the diagnostic draft; recover the enclosing body or a suitable compiler path first.\n')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('address',nargs='?');ap.add_argument('source',nargs='?',type=Path)
    ap.add_argument('--all',action='store_true');ap.add_argument('--budget',type=int,default=4000)
    ap.add_argument('--focus',help='regex selecting the source region allowed to mutate')
    ap.add_argument('--max-instructions',type=int,default=60)
    ap.add_argument('--beam',type=int,default=6);ap.add_argument('--jobs',type=int,default=os.cpu_count())
    ap.add_argument('--seconds',type=float,help='per-target wall-clock budget; retain best comparison on expiry')
    ap.add_argument('--resume',action='store_true',help='skip finalized entries in the output manifest')
    ap.add_argument('--install',action='store_true');ap.add_argument('--output',type=Path,default=ROOT/'docs/near-misses')
    args=ap.parse_args()
    if not args.all and not args.address: ap.error('supply address and draft, or --all')
    if args.seconds is not None and args.seconds <= 0: ap.error('--seconds must be positive')
    os.nice(max(0,10-os.getpriority(os.PRIO_PROCESS,0)))
    prog=draft.Program(); rows=rank_targets.rank(prog,*rank_targets.coverage_evidence(ROOT/'docs/map'))
    rows=[r for r in rows if 8<=r['instructions']<=args.max_instructions] if args.all else [r for r in rows if r['address']==args.address.upper().removeprefix('0X')]
    if not rows: ap.error('no unmatched ranked target in the requested selection')
    previous=args.output/'search-results.json'
    records=json.loads(previous.read_text()) if args.resume and previous.exists() else []
    completed={r['address'] for r in records}
    rows=[r for r in rows if r['address'] not in completed]
    with futures.ProcessPoolExecutor(max_workers=args.jobs,initializer=init_worker,initargs=(reloc.symbols(prog),)) as pool:
        for row in rows:
            if row['blocked_reason']:
                save_rejection(prog,row,args.output)
                records.append({**row,'attempts':0,'exact':False,'status':'rejected before compilation'})
                continue
            # Owner notes may be appended while the batch is running.
            notes=ROOT/'OWNER-NOTES.md'
            if notes.exists(): print(notes.read_text(),flush=True)
            rec=search(pool,prog,row,args.source,args.budget,args.beam,args.output,args.focus,args.seconds)
            records.append(rec)
            if rec['exact'] and args.install:
                a=int(row['address'],16); name='func_%08X'%a
                source=(args.output/(name+'.c')).read_text()
                following=min((x for x in prog.by_start if x>a),default=judge.BASE+prog.cfg['scan_end'])
                exact,*_=judge.compile_candidate(source,name,a,following,reloc.symbols(prog),
                    target_end=int(prog.by_start[a]['end'],16),compiler=rec['compiler'])
                if not exact: raise ValueError('final boundary check failed')
                # Analysis can regenerate an older indirect resolver's metadata.
                # Preserve reviewed mapping files verbatim across the full build.
                mapped={p:p.read_bytes() for p in (ROOT/'docs/map').glob('*') if p.is_file()}
                try:
                    judge.install(source,name,a,rec['size'],rec['compiler'])
                finally:
                    for p,data in mapped.items():
                        if p.read_bytes()!=data: p.write_bytes(data)
                print(name+' installed; full ROM verified',flush=True)
            (args.output/'search-results.json').write_text(json.dumps(records,indent=2)+'\n')
    (args.output/'search-results.json').write_text(json.dumps(records,indent=2)+'\n')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
