#!/usr/bin/env python3
"""Render round-10 compiler metadata only, with a muted 30-fps review clip."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
from PIL import Image, ImageDraw
from review_map import font, BG, FG, MUTED

AMBER='#ffb12a'; BLUE='#639ee8'; GRID='#344258'
W,H=1600,1200


def canvas(title,subtitle):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.text((55,30),'TXRA  /  MATCH ROUND 10',font=font(22,True),fill=MUTED)
    d.text((55,75),title,font=font(40,True),fill=FG)
    d.text((55,135),subtitle,font=font(21),fill=MUTED)
    return im,d


def write_notes(directory,notes,captions):
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'NOTES.md').write_text(notes+'\n')
    (directory/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')


def overview(rows,baseline,current,label):
    im,d=canvas('Exact replacements and remaining differences',label+'  /  Only full byte equality counts as a match')
    a=baseline['functions_matched_c'];b=current['functions_matched_c']
    for x,name,data in [(60,'Before',a),(820,'After' if label=='Final' else 'Current',b)]:
        d.text((x,200),name,font=font(28,True),fill=MUTED)
        d.text((x,244),f"{data['count']} functions   /   {data['percent_of_mapped_code']:.3f}%",font=font(30,True),fill=FG)
        d.text((x,293),f"{data['bytes_including_pools']:,} replacement bytes, including pools",font=font(20),fill=MUTED)
    d.line((60,350,1540,350),fill=GRID,width=2)
    for x,text in [(60,'Entry'),(300,'Instruction differences'),(740,'Byte differences'),(1060,'Fresh compilations'),(1380,'Minutes')]:
        d.text((x,379),text,font=font(19,True),fill=MUTED)
    for i,row in enumerate(rows):
        y=425+i*min(47,560/max(1,len(rows)));r=row['result'];old=row['prior_score'];new=r.get('best_score') or old
        d.text((60,y),row['address'],font=font(22,True),fill=FG)
        d.text((300,y),f'{old[0]}  →  {new[0]}',font=font(22),fill=AMBER if new[0]<old[0] else FG)
        d.text((740,y),f'{old[1]}  →  {new[1]}',font=font(22),fill=FG)
        d.text((1060,y),f"{r.get('compiled',0):,}",font=font(22),fill=FG)
        d.text((1380,y),f"{r.get('seconds',0)/60:.1f}",font=font(22),fill=FG)
    total=sum(r['result'].get('compiled',0) for r in rows)
    exact=sum(bool(r['result'].get('exact')) for r in rows)
    d.text((60,1030),f'{total:,} fresh source/profile compilations   /   {exact} exact search results',font=font(27,True),fill=FG)
    d.text((60,1084),'Five compiler processes shared across active targets; elapsed minutes include queueing.',font=font(22),fill=MUTED)
    d.text((60,1127),'Mapped-code denominator stays at 85,132 bytes. A closer draft is still unfinished work.',font=font(22),fill=MUTED)
    return im


def traces(rows,fraction=1):
    im,d=canvas('Best instruction score over search time','Each panel has its own score scale  /  Lower is closer  /  Amber is the best known draft')
    stride=min(153,900/max(1,(len(rows)+1)//2))
    for i,row in enumerate(rows):
        col=i%2;rr=i//2;x=60+col*790;y=210+rr*stride
        hist=row['history'];prior=row['prior_score'][0]
        end=max(1500,row['result'].get('seconds',0));limit=end*fraction
        top=max(1,prior);left=x+55;right=x+680;upper=y+36;bottom=y+stride-30
        d.text((x,y),row['address'],font=font(21,True),fill=FG)
        best=min([prior]+[h['best_score'][0] for h in hist if h.get('best_score') and h['seconds']<=limit])
        d.text((x+210,y),f'{prior} → {best}',font=font(21,True),fill=AMBER)
        duration=row['result'].get('seconds',0)
        time_label=f'{min(limit,duration)/60:.1f} min' if duration else 'queued'
        d.text((x+450,y),time_label,font=font(18),fill=MUTED)
        for score in [0,top]:
            yy=bottom-(bottom-upper)*score/top
            d.line((left,yy,right,yy),fill=GRID,width=1)
            d.text((x,int(yy)-8),str(score),font=font(15),fill=MUTED)
        points=[(left,upper)];best=prior
        for h in hist:
            if h['seconds']>limit:break
            if h.get('best_score'):best=min(best,h['best_score'][0])
            xx=left+(right-left)*h['seconds']/end;yy=bottom-(bottom-upper)*best/top
            points.extend([(xx,points[-1][1]),(xx,yy)])
        points.append((left+(right-left)*min(limit,row['result'].get('seconds',0))/end,points[-1][1]))
        if len(points)>1:d.line(points,fill=AMBER,width=3)
        d.text((left,y+stride-25),'0',font=font(14),fill=MUTED)
        d.text((right-52,y+stride-25),'25 min',font=font(14),fill=MUTED)
    d.text((60,1161),'Flat traces are measured plateaus. These plots contain our compiler metadata only.',font=font(20),fill=MUTED)
    return im


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory',type=Path)
    ap.add_argument('--search',type=Path,default=Path('docs/match10-search'))
    ap.add_argument('--video',action='store_true')
    ap.add_argument('--final',action='store_true')
    args=ap.parse_args();root=args.directory;root.mkdir(parents=True,exist_ok=True)
    baseline=root/'baseline.json'
    if not baseline.exists():shutil.copyfile('progress.json',baseline)
    before=json.loads(baseline.read_text());current=json.loads(Path('progress.json').read_text())
    targets=json.loads((args.search/'targets.json').read_text());rows=[]
    for row in targets:
        folder=args.search/row['address'];p=folder/'result.json';h=folder/'history.jsonl'
        row['result']=json.loads(p.read_text()) if p.exists() else {}
        row['history']=[json.loads(line) for line in h.read_text().splitlines()] if h.exists() else []
        rows.append(row)
        logs=root/'logs'/row['address'];logs.mkdir(parents=True,exist_ok=True)
        for filename in ['result.json','history.jsonl','func_'+row['address']+'.diff.txt']:
            if (folder/filename).exists():shutil.copyfile(folder/filename,logs/filename)
    label='Final' if args.final else 'Search in progress'
    overview(rows,before,current,label).save(root/'search-results.png')
    traces(rows).save(root/'score-traces.png')
    # Identical framing of accepted totals, for an honest before/after view.
    for name,data in [('before',before),('after',current)]:
        folder=root/name;folder.mkdir(exist_ok=True)
        im,d=canvas('Accepted ordinary C replacements','Complete functions only  /  Same mapped-code denominator')
        r=data['functions_matched_c']
        d.text((90,290),name.capitalize(),font=font(42,True),fill=MUTED)
        d.text((90,385),f"{r['count']} functions",font=font(72,True),fill=FG)
        d.text((90,510),f"{r['percent_of_mapped_code']:.3f}% of mapped code",font=font(52,True),fill=AMBER)
        d.text((90,625),f"{r['bytes_including_pools']:,} replacement bytes, including literal pools",font=font(30),fill=FG)
        d.rectangle((90,740,1510,810),fill=GRID)
        d.rectangle((90,740,90+int(1420*r['percent_of_mapped_code']/100),810),fill=AMBER)
        d.text((90,875),'Search attempts and closer drafts do not increase this total.',font=font(27),fill=MUTED)
        im.save(folder/'matching-status.png')
        write_notes(folder,f'TXRA accepted replacement totals, {name} the round-ten search. Compare this with the same view in the other folder; unfinished drafts do not increase these numbers.',{'matching-status.png':f'{name.capitalize()}: accepted exact replacements, with a fixed mapped-code denominator.'})
    captions={'search-results.png':'Round-ten results: prior and best differences, fresh compilations and elapsed time for each target.','score-traces.png':'Best instruction differences over each target’s timed window; flat lines show plateaus.'}
    if args.video:
        path=root/'search-progress.webm'
        cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate','30','-i','-','-an','-c:v','libvpx-vp9','-threads','2','-b:v','1000k','-crf','36','-r','30',str(path)]
        encoder=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        for frame in range(180):encoder.stdin.write(traces(rows,min(1,frame/150)).tobytes())
        encoder.stdin.close()
        if encoder.wait():raise RuntimeError('video encoding failed')
        if path.stat().st_size>4000000:raise RuntimeError('video exceeds review limit')
        captions[path.name]='Six-second muted replay of our measured search scores, 30 fps; compiler metadata only.'
    write_notes(root,'This is TXRA’s tenth compiler matching search. Compare before/ and after/ for accepted totals, and use the results table to see which unfinished drafts got closer. Each score trace shows the best known instruction difference during that target’s search; lower is better, and a flat line means the search plateaued. Five compiler workers are shared across the timed windows, and only exact results can become replacements.',captions)
    return 0

if __name__=='__main__':raise SystemExit(main())
