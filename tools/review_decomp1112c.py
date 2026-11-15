#!/usr/bin/env python3
"""Render bounded compiler evidence and muted review clips; never export data."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

from PIL import Image,ImageDraw,ImageFont

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'recomp'))
import draft
import reloc
from measure_candidate import diagnostic_compile
import review_match1109c as review

ROOT=Path('docs/near-misses/decomp-1112c')
W,H=1600,1000
VIDEO_W,VIDEO_H=1280,800


def font(size,bold=False,mono=False):
    stem='DejaVuSansMono' if mono else 'DejaVuSans'
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+stem+('-Bold' if bold else '')+'.ttf',size)


def text(draw,xy,value,size=24,color=review.FG,bold=False,mono=False,width=1516):
    chosen=font(size,bold,mono)
    assert draw.textbbox(xy,value,font=chosen)[2]-xy[0]<=width,value
    draw.text(xy,value,font=chosen,fill=color)


def record(path,**extra):
    return dict(bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**extra)


def overview(after):
    im=Image.new('RGB',(W,H),review.BG)
    d=ImageDraw.Draw(im)
    text(d,(42,28),'TXRA / 12 NOVEMBER / COMPLETE-OWNER RECOVERY',23,review.MUTED,True)
    text(d,(42,84),'Four structured C candidates, all still uninstalled',35,bold=True)
    text(d,(42,150),'AFTER: retained sources' if after else 'BEFORE: retained baselines; stream is its first complete draft',24,review.AMBER)
    text(d,(42,218),'189 exact replacements / 237 mapped entries',36,review.AMBER,True)
    text(d,(42,282),'Exact replacement totals stay the same throughout this review.',23,review.MUTED)
    text(d,(42,349),'entry and work',24,review.MUTED,True)
    text(d,(860,349),'bytes still different',24,review.MUTED,True,width=330)
    text(d,(1230,349),'frame / original',24,review.MUTED,True,width=330)
    targets=[('hud','0800421C','map coefficient lifetimes',36),
             ('contact','080181C0','pair-code lifetime',72),
             ('arm','08016DA8','face index scopes',96),
             ('stream','08002854','complete geometry and continuation',268)]
    for i,(tag,addr,title,frame) in enumerate(targets):
        p=json.loads((ROOT/(tag+('-candidate' if after else '-baseline')+'.json')).read_text())
        y=408+i*83
        d.rectangle((35,y-7,1565,y+63),fill=review.AGREE)
        text(d,(48,y),addr+' / '+title,24,width=790)
        text(d,(872,y),f"{p['different_bytes']:,}",30,review.AMBER,True,width=280)
        text(d,(1240,y),f"{p['local_frame_bytes']} / {frame}",25,width=300)
    text(d,(42,790),'Original-instruction checks: HUD 192 states / contact 192 / stream 480',24)
    text(d,(42,840),'Renderer: 199 independent textual-instruction memory fixtures.',24)
    text(d,(42,909),'Stream includes both directions, walls, bridge panels and two scenery columns.',22,review.MUTED)
    text(d,(42,957),'Compiler and synthetic-state evidence; this is not gameplay footage.',21,review.MUTED)
    return im


def comparison(program,tag,addr,title,focus,frame,after):
    p=json.loads((ROOT/(tag+('-candidate' if after else '-baseline')+'.json')).read_text())
    source=Path(p['source']).read_text()
    assert hashlib.sha256(source.encode()).hexdigest()==p['source_sha256']
    start,end=int(addr,16),int(p['target_end'],16)
    actual,_=diagnostic_compile(source,'func_'+addr,start,reloc.symbols(program),p['compiler'])
    assert hashlib.sha256(actual).hexdigest()==p['compiled_sha256']
    want=program.rom[start-draft.BASE:end-draft.BASE]
    review.font=font
    rows=review.compare(want,actual,start,'arm' if p['compiler']=='arm' else 'thumb')
    im=review.picture(addr,title,rows,focus,p,after,frame)
    d=ImageDraw.Draw(im)
    d.rectangle((36,20,1564,65),fill=review.BG)
    text(d,(42,28),'TXRA / MATCHING C / 12 NOVEMBER / SAME ORIGINAL VIEW',22,review.MUTED,True)
    if tag=='stream' and not after:
        d.rectangle((36,120,1564,163),fill=review.BG)
        text(d,(42,126),'before: first complete validated draft, including the continuation',23,review.MUTED)
    return im


def clip(path,before,after,status=False):
    process=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24',
        '-s',f'{W}x{H}','-r','30','-i','-','-an','-frames:v','120','-c:v','libvpx-vp9',
        '-vf',f'scale={VIDEO_W}:{VIDEO_H}:flags=lanczos','-b:v','0','-crf','47','-deadline','good','-cpu-used','5','-row-mt','1','-threads','2',str(path)],stdin=subprocess.PIPE)
    try:
        for frame in range(120):
            im=(before if frame<60 else after).copy()
            d=ImageDraw.Draw(im)
            if status:
                y=408+(frame%60)*4//60*83
                d.rectangle((35,y-7,1565,y+63),outline=review.AMBER,width=2)
            else:
                y=316+(frame%60)*23//60*24
                d.rectangle((36,y-2,1564,y+22),outline=review.AMBER,width=2)
            process.stdin.write(im.tobytes())
        process.stdin.close()
        assert process.wait()==0
    finally:
        if process.poll() is None: process.kill();process.wait()
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    assert len(info['streams'])==1
    s=info['streams'][0]
    assert s['codec_type']=='video' and s['r_frame_rate']=='30/1'
    assert (s['width'],s['height'])==(VIDEO_W,VIDEO_H)
    assert 3.9<float(info['format']['duration'])<4.1 and path.stat().st_size<=4_000_000
    return record(path,seconds=4,fps=30,width=VIDEO_W,height=VIDEO_H,audio_streams=0)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory',type=Path)
    args=ap.parse_args()
    out=args.directory.expanduser()
    out.mkdir(parents=True,exist_ok=True)
    (out/'NOTES.md').write_text('This is TXRA code recovery for the HUD, contact rotation, track renderer and stream geometry. '
        'All four candidates are closer, and the stream now includes its full geometry and continuation; none is installed. '
        'Compare the same before and after code views and the four-owner table; the stream before image is the first complete draft made this round. '
        'The muted clips replay compiler evidence, with decoded samples in the overview; these are not gameplay recordings.\n')
    program=draft.Program()
    captions,artifacts={},{}
    sheet=Image.new('RGB',(1000,990),review.BG)
    groups=[('status',lambda after:overview(after)),
            ('0800421C',lambda after:comparison(program,'hud','0800421C','HUD drawer',0x08004A88,36,after)),
            ('08002854',lambda after:comparison(program,'stream','08002854','Track streamer',0x08002854,268,after))]
    for row,(name,maker) in enumerate(groups):
        images=[]
        for after in (False,True):
            filename=('after-' if after else 'before-')+name+'.png'
            im=maker(after)
            assert im.size==(W,H) and im.getbbox()==(0,0,W,H)
            im.quantize(colors=192).save(out/filename,optimize=True)
            images.append(im)
            captions[filename]=('After: retained candidate; ' if after else 'Before: baseline; ')+('all four owner measurements.' if name=='status' else 'same original code view, '+('first complete stream draft.' if name=='08002854' and not after else 'still a complete nonmatch.'))
            artifacts[filename]=record(out/filename,width=W,height=H)
            (out/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
        filename=name+'.webm'
        artifacts[filename]=clip(out/filename,*images,status=name=='status')
        captions[filename]='Four seconds, muted, 30 fps: before then after '+name+' compiler evidence.'
        (out/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
        d=ImageDraw.Draw(sheet)
        text(d,(8,row*330),name+' / decoded half-second samples',17,review.MUTED,True,width=980)
        for index in range(8):
            data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(.25+index*.5),'-i',str(out/filename),'-frames:v','1','-f','image2pipe','-vcodec','png','-'])
            decoded=Image.open(io.BytesIO(data)).convert('RGB')
            assert decoded.size==(VIDEO_W,VIDEO_H)
            assert decoded.getextrema()[0][1]-decoded.getextrema()[0][0]>100
            sheet.paste(decoded.resize((250,156)),((index%4)*250,row*330+18+(index//4)*156))
    sheet.quantize(colors=192).save(out/'clip-overview.png',optimize=True)
    artifacts['clip-overview.png']=record(out/'clip-overview.png',width=1000,height=990)
    captions['clip-overview.png']='Decoded frames from all three four-second clips, before then after.'
    (out/'NOTES.md').write_text('This is TXRA code recovery for the HUD, contact rotation, track renderer and stream geometry. '
        'All four candidates are closer, and the stream now includes its full geometry and continuation; none is installed. '
        'Compare the same before and after code views and the four-owner table; the stream before image is the first complete draft made this round. '
        'The muted clips replay compiler evidence, with decoded samples in the overview; these are not gameplay recordings.\n')
    (out/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
    receipt=dict(directory='txra-review/decomp-1112c',artifacts=artifacts,
        comparisons_only=True,gameplay_claimed=False,browser_or_server_started=False)
    (ROOT/'review.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
