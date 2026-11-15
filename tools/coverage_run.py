#!/usr/bin/env python3
"""Run deterministic private coverage sessions, with isolated save files."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

SCENARIOS = [('save',3700,'save-input.txt','roundtrip'),
             ('reload',2200,'reload-input.txt','roundtrip'),
             ('options',3200,'options-input.txt','options'),
             ('options-all',3600,'options-all-input.txt','options-all'),
             ('sweep',7900,'menu-sweep-input.txt','sweep')]

ROUND4 = [('results-next',14000,'results-next-input.txt','results-next'),
          ('pause-third',7000,'pause-third-input.txt','pause-third')]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--snapshots',action='store_true')
    parser.add_argument('--round3',action='store_true',help='also probe course choices and pause/replay paths')
    parser.add_argument('--round4',action='store_true',help='include results and third pause-choice probes')
    parser.add_argument('--scenario',action='append',choices=[s[0] for s in ROUND4],
                        help='run only the selected round-four probe; repeat to select both')
    args=parser.parse_args()
    scenarios=SCENARIOS+([(name,6500,name+'-input.txt',name) for name in ('course-next','course-third','course-last','pause-next','pause-side')] if args.round3 or args.round4 else [])
    if args.round4:scenarios += ROUND4
    if args.scenario:scenarios = [s for s in ROUND4 if s[0] in args.scenario]
    root=args.directory;root.mkdir(parents=True,exist_ok=True)
    # Refuse old test saves instead of silently altering a previous run.
    for save in {s[3] for s in scenarios}:
        if (root/(save+'.sav')).exists():raise SystemExit('Use a fresh coverage directory')
    manifest=[]
    for name,frames,script,save in scenarios:
        path=root/(save+'.sav')
        prior=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        command=['build/txra-pc','--headless','--mute','--benchmark','--frames',str(frames),
                 '--input-script','tests/'+script,'--save',str(path),'--stats',str(root/(name+'.json')),
                 '--coverage',str(root/(name+'-coverage.json')),'--unknown-log',str(root/(name+'-unknown.log'))]
        if args.snapshots:
            snapshots=root/(name+'-snapshots');snapshots.mkdir(exist_ok=True)
            command+=['--snapshots',str(snapshots)]
        with (root/(name+'.log')).open('w') as log:
            subprocess.run(command,stdout=log,stderr=log,check=True)
        stats=json.loads((root/(name+'.json')).read_text())
        assert stats['frames']==frames and not stats['stopped']
        assert stats['fallback_steps']==stats['unknown_targets']==stats['unsupported']==0
        if name=='save':assert stats['save_writes']>0 and path.exists()
        if name=='reload':assert stats['save_writes']==0 and hashlib.sha256(path.read_bytes()).hexdigest()==prior
        manifest.append({'scenario':name,'input_sha256':hashlib.sha256(Path('tests/'+script).read_bytes()).hexdigest(),
                         'stats':stats})
        print(name,'passed',flush=True)
    (root/'sessions.json').write_text(json.dumps({'build_sha256':hashlib.sha256(Path('build/txra-pc').read_bytes()).hexdigest(),
                                                'scenarios':manifest},indent=2)+'\n')

if __name__=='__main__':main()
