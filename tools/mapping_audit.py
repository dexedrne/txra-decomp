#!/usr/bin/env python3
"""Summarize structural and session evidence without emitting cartridge contents."""
import argparse
import json
from pathlib import Path
from rom_map import BASE


def audit(cfg, functions, baseline, sessions):
    prior_pcs={tuple(pc) for t in baseline for pc in t['pcs']}
    prior_reads=bytearray(cfg['size'])
    for trace in baseline:
        for offset,size in trace['reads']:prior_reads[offset:offset+size]=b'\1'*size
    executed=set();rows=[]
    blocks=json.loads(Path('docs/map/structures.json').read_text())['blocks']
    for name,trace in sessions:
        pcs={tuple(pc) for pc in trace['pcs']};executed.update(pcs)
        courses=[]
        for b in blocks:
            if b['format']!='course-records-stride28':continue
            count=sum(max(0,min(o+n,b['offset']+b['size'])-max(o,b['offset'])) for o,n in trace['reads'])
            if count:courses.append({'offset':b['offset'],'read_bytes':count})
        states=[];last=None
        for frame,state in sorted((e[3],e[1]) for e in trace.get('entries',[]) if e[0]==BASE+0x12600):
            if state!=last:states.append({'frame':frame,'screen_id':state});last=state
        rows.append(dict(name=name,new_executed_pcs_vs_round2=len(pcs-prior_pcs),
                         new_read_bytes_vs_round2=sum(n-sum(prior_reads[o:o+n]) for o,n in trace['reads']),
                         course_arrays_read=courses,screen_transitions=states,
                         decoder_calls=[e for e in trace.get('entries',[]) if e[0]==BASE+0x1251c]))
    unseen=[]
    for f in functions:
        entries={int(f['start'],16)}|{int(a['start'],16) for a in f.get('runtime_aliases',[])}
        if not any((pc,int(f['mode']=='thumb')) in executed for pc in entries):
            unseen.append({'start':f['start'],'mode':f['mode']})
    return dict(sessions=rows,new_executed_pcs_vs_round2=len(executed-prior_pcs),
                mapped_function_entries_unexecuted=unseen,
                conclusion='No new function is established merely by a new observed PC; recursive descent must validate instruction spans.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',nargs='+',required=True);p.add_argument('--sessions',nargs='+',required=True)
    p.add_argument('--output',type=Path,default=Path('docs/map/round3-audit.json'))
    p.add_argument('--baseline-label',default='round2',choices=['round2','round3'])
    args=p.parse_args();cfg=json.loads(Path('tools/rom.cfg').read_text())
    fs=json.loads(Path('docs/map/functions.json').read_text())['functions']
    old=[json.loads(Path(path).read_text()) for path in args.baseline]
    sessions=[(Path(path).stem.removesuffix('-coverage'),json.loads(Path(path).read_text())) for path in args.sessions]
    traces=old+[trace for _,trace in sessions]
    if any(trace.get('overflow') for trace in traces):raise ValueError('incomplete coverage')
    if len({trace.get('rom_crc32') for trace in traces})!=1:raise ValueError('mixed coverage fingerprints')
    result=audit(cfg,fs,old,sessions)
    if args.baseline_label != 'round2':
        result={k.replace('_vs_round2','_vs_'+args.baseline_label):v for k,v in result.items()}
        result['sessions']=[{k.replace('_vs_round2','_vs_'+args.baseline_label):v for k,v in row.items()}
                            for row in result['sessions']]
    result['baseline_label']=args.baseline_label
    args.output.write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
