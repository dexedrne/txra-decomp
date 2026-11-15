#!/usr/bin/env python3
"""Render same-view contact and mapping evidence, with short muted clips."""
import argparse
import hashlib
import io
import json
import re
from pathlib import Path
import subprocess
import sys
from PIL import Image,ImageDraw,ImageFont

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'recomp'))
import draft,reloc
from measure_candidate import diagnostic_compile
import review_match1109c as review
from review_match1110 import media_record

ROOT=Path('docs/near-misses/breadth-1112b')


def font(size,bold=False,mono=False):
    name='DejaVuSansMono' if mono else 'DejaVuSans'
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+name+('-Bold' if bold else '')+'.ttf',size)


review.font=font


def line(draw,xy,text,size=26,color=review.FG,bold=False,mono=False,width=1510):
    f=font(size,bold,mono)
    assert draw.textbbox(xy,text,font=f)[2]<=xy[0]+width,text
    draw.text(xy,text,font=f,fill=color)


def mapping(after):
    r=json.loads((ROOT/'raster-mapping.json').read_text())
    im=Image.new('RGB',(1600,1000),review.BG);d=ImageDraw.Draw(im)
    line(d,(42,25),'TXRA / 12 NOVEMBER / SECOND BREADTH REVIEW',23,review.MUTED,True)
    line(d,(42,79),'Early code-gap review / reciprocal table',40,bold=True)
    line(d,(42,143),'AFTER: complete shared raster table validated' if after else 'BEFORE: observed reads amid unclassified bytes',26,review.AMBER)
    values=[('unknown bytes',r['after' if after else 'before']['unknown_bytes']),('known bytes in this table',2050 if after else 502),('new functions',0)]
    for x,(name,value) in zip((42,562,1082),values):
        line(d,(x,215),f'{value:,}',48,review.AMBER,True,width=470)
        line(d,(x,280),name,25,width=470)
    rows=[('table extent','080018B4 - 080020B6'),('complete table shape','1,025 halfwords validated' if after else 'not yet structurally classified'),
          ('newly classified data','1,548 bytes' if after else '0 bytes'),('mapped function entries','237'),('exact C replacements','189'),('new game execution claim','none')]
    for i,(label,value) in enumerate(rows):
        y=392+i*76
        d.rectangle((35,y-4,1565,y+58),fill=review.AGREE)
        line(d,(50,y+8),label,25,width=620)
        line(d,(735,y+8),value,25,review.AMBER if after and i<3 else review.FG,width=810)
    line(d,(42,880),'The following alignment halfword stays outside the validated table.',25)
    line(d,(42,925),'Data classification adds no function and no replacement to the exact registry.',24,review.MUTED)
    line(d,(42,967),'The original game bytes stay private. This is a mapping review.',20,review.MUTED)
    return im


def contact(program,after):
    p=ROOT/'contact-final/candidate.json' if after else ROOT/'contact-baseline.json'
    r=json.loads(p.read_text());source=Path(r['source']).read_text()
    assert hashlib.sha256(source.encode()).hexdigest()==r['source_sha256']
    actual,_=diagnostic_compile(source,'func_080181C0',0x080181C0,reloc.symbols(program),'arm')
    assert hashlib.sha256(actual).hexdigest()==r['compiled_sha256']
    expected=program.rom[0x181C0:0x18854]
    rows=review.compare(expected,actual,0x080181C0,'arm')
    im=review.picture('080181C0','Contact rotation and record lifetimes',rows,0x08018460,r,after,72)
    d=ImageDraw.Draw(im)
    left=[row for row in review.listing(expected,0x080181C0,'arm') if row[0]>=0x08018460 and not row[1].startswith('.word ')][:23]
    emitted=review.listing(actual,0x080181C0,'arm')
    loops=[int(m[1],16) for row in emitted for m in [re.match(r'bpl 0x([0-9A-Fa-f]+)$',row[1])] if m and 0x08018400<=int(m[1],16)<0x08018500]
    assert len(loops)==1
    right=[row for row in emitted if row[0]>=loops[0] and not row[1].startswith('.word ')][:23]
    assert len(left)==len(right)==23
    for index,(lrow,rrow) in enumerate(zip(left,right)):
        y=316+index*24
        d.rectangle((36,y-2,1564,y+22),fill=review.AGREE if lrow==rrow else review.BAD)
        for x,row in ((45,lrow),(823,rrow)):
            line(d,(x,y),'%08X  %s'%row[:2],18,mono=True,width=740)
    d.rectangle((35,18,1565,65),fill=review.BG)
    line(d,(42,25),'TXRA / 12 NOVEMBER / SECOND BREADTH REVIEW',23,review.MUTED,True)
    d.rectangle((35,915,1565,999),fill=review.BG)
    line(d,(42,922),'919 bytes still differ after recovery. No replacement was installed.' if after else
         '1,011 bytes differ in the round-one retained source. No replacement was installed.',24)
    line(d,(42,965),'The retained source passes original-instruction fixtures; this is not gameplay footage.' if after else
         'Same original rotation view as the after picture. Encodings and stored data are hidden.',20,review.MUTED)
    return im


def clip(path,before,after,status):
    process=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1600x1000','-r','30','-i','-',
                              '-an','-frames:v','120','-c:v','libvpx-vp9','-b:v','0','-crf','39','-deadline','good','-cpu-used','4',
                              '-row-mt','1','-threads','2',str(path)],stdin=subprocess.PIPE)
    try:
        for frame in range(120):
            im=(before if frame<60 else after).copy();d=ImageDraw.Draw(im)
            if status:
                y=392+(frame%60)*6//60*76
                d.rectangle((35,y-4,1565,y+58),outline=review.AMBER,width=2)
            else:
                y=316+(frame%60)*23//60*24
                d.rectangle((36,y-2,1564,y+22),outline=review.AMBER,width=2)
            process.stdin.write(im.tobytes())
        process.stdin.close();assert process.wait()==0
    finally:
        if process.poll() is None:process.kill();process.wait()
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    assert len(info['streams'])==1
    s=info['streams'][0]
    assert s['codec_type']=='video' and s['r_frame_rate']=='30/1' and (s['width'],s['height'])==(1600,1000)
    assert 3.9<float(info['format']['duration'])<4.1 and path.stat().st_size<4_000_000
    return media_record(path,seconds=float(info['format']['duration']),fps=30,width=1600,height=1000,audio_streams=0)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('directory',type=Path)
    ap.add_argument('--contact-only',action='store_true',help='retain the valid mapping pictures and clip')
    args=ap.parse_args();dest=args.directory.expanduser();dest.mkdir(parents=True,exist_ok=True)
    prior=json.loads((ROOT/'review.json').read_text())['artifacts'] if args.contact_only else {}
    captions={};artifacts={};program=draft.Program();overview=Image.new('RGB',(1000,660),review.BG)
    for group,(stem,maker,status) in enumerate([('raster-table',mapping,True),('080181C0',lambda after:contact(program,after),False)]):
        images=[]
        for after in (False,True):
            name=('after-' if after else 'before-')+stem+'.png'
            im=Image.open(dest/name).convert('RGB') if status and args.contact_only else maker(after)
            assert im.size==(1600,1000)
            if not (status and args.contact_only):im.save(dest/name)
            images.append(im);artifacts[name]=media_record(dest/name,width=1600,height=1000)
            captions[name]=('After: ' if after else 'Before: ')+('early-gap table classification, same metrics view; no new function.' if status else
                f"contact rotation, same original view; {919 if after else 1011:,} bytes still differ.")
        name=stem+'.webm';artifacts[name]=prior[name] if status and args.contact_only else clip(dest/name,*images,status)
        captions[name]='Four seconds, muted, 30 fps: before then after '+('table classification.' if status else 'contact compiler comparison; still uninstalled.')
        ImageDraw.Draw(overview).text((8,group*330),stem+' / decoded frames',font=font(17,True),fill=review.FG)
        for index in range(8):
            data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(.25+index*.5),'-i',str(dest/name),'-frames:v','1','-f','image2pipe','-vcodec','png','-'])
            frame=Image.open(io.BytesIO(data)).convert('RGB');assert frame.size==(1600,1000)
            assert max(frame.getextrema()[0])-min(frame.getextrema()[0])>100
            overview.paste(frame.resize((250,156)),((index%4)*250,group*330+18+(index//4)*156))
    name='clip-overview.png';overview.save(dest/name);artifacts[name]=media_record(dest/name,width=1000,height=660)
    captions[name]='Decoded half-second samples from both four-second muted comparison clips.'
    (dest/'NOTES.md').write_text('This is TXRA code recovery and map review for the second breadth pass. '
        'The contact routine is closer to the cartridge, with differing bytes reduced from 1,011 to 919, but it remains uninstalled. '
        'The early gap is now recognized as a complete table, accounting for 1,548 formerly unknown bytes; the exact total stays at 189. '
        'Compare each before and after pair at the same view, then use the short muted clips to replay the changes. '
        'These are code and mapping comparisons, not gameplay footage.\n')
    (dest/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
    (ROOT/'review.json').write_text(json.dumps(dict(directory='txra-review/breadth-1112b',artifacts=artifacts,gameplay_claimed=False,comparisons_only=True),indent=2)+'\n')
    print('Rendered %d review artifacts; %d bytes total.'%(len(artifacts),sum(r['bytes'] for r in artifacts.values())))


if __name__=='__main__':main()
