#!/usr/bin/env python3
"""Measure alternate historical compiler flags; never modify emitted assembly."""
import concurrent.futures as futures
import itertools
import json
import os
from pathlib import Path
import sys
import variant_search as vs

FLAGS=['-fno-thread-jumps','-fno-gcse','-fno-cse-follow-jumps','-fno-cse-skip-blocks','-fno-expensive-optimizations','-fno-branch-count-reg','-fno-strength-reduce','-fno-force-mem','-fno-function-cse','-fno-rerun-cse-after-loop','-fno-rerun-loop-opt','-fno-schedule-insns','-fno-schedule-insns2','-fno-regmove','-fno-caller-saves','-fno-peephole','-fno-defer-pop','-fno-crossjumping','-fno-loop-optimize','-fno-guess-branch-probability','-fno-omit-frame-pointer','-fno-unroll-loops','-fno-inline','-fno-strict-aliasing']
BASE_RUN=vs.judge.run
EXTRA=()

def run(args,**kw):
    if Path(str(args[0])).name in ('old_agbcc','agbcc'):args=[*args[:-2],*EXTRA,*args[-2:]]
    return BASE_RUN(args,**kw)

def worker(job):
    global EXTRA
    address,end,source,profile,flags=job
    EXTRA=flags
    vs.judge.run=run
    sc,size,got,error=vs.compile_job((address,end,source,profile))
    return {'flags':flags,'compiler':profile,'score':sc,'size':size,'error':error},got

def main():
    import argparse
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('address');ap.add_argument('source',type=Path);args=ap.parse_args()
    a=int(args.address,16);p=vs.draft.Program();end=vs.comparison_end(p,a);s=args.source.read_text()
    flags=[()]+[(f,) for f in FLAGS]+list(itertools.combinations(FLAGS,2))
    jobs=[(a,end,s,profile,f) for profile in ('old','standard') for f in flags]
    dest=Path('docs/match7-search')/('flags-'+args.address);dest.mkdir(parents=True,exist_ok=True)
    results=[];best=None
    with futures.ProcessPoolExecutor(max_workers=6,initializer=vs.init_worker,initargs=(vs.reloc.symbols(p),)) as pool:
        for row,got in pool.map(worker,jobs):
            row['exact']=bool(got and got==p.rom[a-vs.draft.BASE:end-vs.draft.BASE]);results.append(row)
            if row['score'] and (best is None or row['score']<best['score']):
                best=row;print(row,flush=True)
                (dest/'best.diff.txt').write_text(vs.source_diff(p.rom[a-vs.draft.BASE:end-vs.draft.BASE],got,a)+'\n')
    (dest/'results.json').write_text(json.dumps({'source':str(args.source),'records':results},indent=2)+'\n')

if __name__=='__main__':main()
