#!/usr/bin/env python3
"""Review count and percent over accepted commit times; metadata only."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import datetime as dt
from review_map import base, font, FG, MUTED, COLORS


def main(default_target=40):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory',type=Path)
    ap.add_argument('--baseline',required=True)
    ap.add_argument('--target-additions',type=int,default=default_target)
    args=ap.parse_args()
    subprocess.run([sys.executable,'tools/review_match3.py',str(args.directory),
        '--baseline',args.baseline,'--target-additions',str(args.target_additions)],check=True)
    rows=json.loads((args.directory/'batch-history.json').read_text())
    mapped=json.loads(Path('progress.json').read_text())['code_bytes_mapped']
    times=[dt.datetime.fromisoformat(r['time']).timestamp() for r in rows]
    elapsed=max(1,times[-1]-times[0])
    values=[100*r['bytes']/mapped for r in rows]
    im,d=base('Matched mapped code over time','Accepted source replacements / metadata from our matching tools')
    left,right,top,bottom=160,1460,280,790
    # Fixed zero baseline prevents small gains looking like a completed project.
    ceiling=20
    for pct in range(0,ceiling+1,5):
        y=bottom-int((bottom-top)*pct/ceiling)
        d.line((left,y,right,y),fill='#344258',width=2)
        d.text((40,y-15),f'{pct}%',font=font(24),fill=MUTED)
    points=[(left+int((t-times[0])/elapsed*(right-left)),bottom-int(v/ceiling*(bottom-top))) for t,v in zip(times,values)]
    steps=[points[0]]
    for old,new in zip(points,points[1:]): steps.extend([(new[0],old[1]),new])
    d.line(steps,fill=COLORS['code'],width=6)
    for index in (0,len(rows)-1):
        x,y=points[index]
        d.ellipse((x-6,y-6,x+6,y+6),fill=FG)
        d.text((max(left,min(x-55,right-180)),y-52),f'{values[index]:.3f}%',font=font(30,True),fill=FG)
        d.text((left if index==0 else right-280,bottom+32),dt.datetime.fromisoformat(rows[index]['time']).strftime('%m-%d %H:%M UTC'),font=font(22),fill=MUTED)
    d.text((80,900),f'Unchanged denominator: {mapped:,} mapped instruction bytes. Pools are included in matched totals.',font=font(23),fill=MUTED)
    d.text((80,945),'Steps show accepted batches, not search speed or newly mapped code.',font=font(23),fill=MUTED)
    im.save(args.directory/'matched-percent.png')
    notes=args.directory/'NOTES.md'
    notes.write_text(notes.read_text().replace('the two charts', 'the three charts'))
    captions=args.directory/'captions.json'; data=json.loads(captions.read_text())
    data['matched-percent.png']=f'Accepted matched code: {values[0]:.3f}% before, {values[-1]:.3f}% after; fixed denominator.'
    captions.write_text(json.dumps(data,indent=2)+'\n')
    return 0

if __name__=='__main__': raise SystemExit(main())
