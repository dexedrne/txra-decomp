#!/usr/bin/env python3
"""Draw the three complete-owner compiler comparisons and short muted review clips."""
import argparse
import difflib
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'recomp'))
import draft
import diffhint
import reloc
from measure_candidate import diagnostic_compile

W,H=1600,1000
BG,FG,MUTED,AMBER,BORDER='#0b1220','#f2e4c8','#b8c4d6','#ffb12a','#43536b'
BAD,AGREE='#44232d','#172238'
FONT=Path('/usr/share/fonts/gsfonts')

def font(size,bold=False,mono=False):
    name=('NimbusMonoPS' if mono else 'NimbusSans')+('-Bold.otf' if bold else '-Regular.otf')
    return ImageFont.truetype(str(FONT/name),size)

TARGETS=[
    ('arm-16da8-1109','08016DA8','Track-face renderer',0x08016E70,96),
    ('sound-owner-1109','080064A4','Sound owner',0x08006740,108),
    ('hud-owner-1109','0800421C','HUD drawer',0x08005004,36),
]

def listing(data,start,mode):
    lines=[]
    for row in diffhint.listing(data,start,mode):
        match=re.match(r'(\w{8}):\s*(.*)',row)
        address=int(match[1],16);text=match[2]
        text=re.sub(r'^[0-9A-Fa-f]{4,8}\s+','',text)
        text=re.sub(r'\.word 0x[0-9A-Fa-f]+ \(literal pool\)', '.word <literal pool>',text)
        offset=address-start
        width=4 if mode=='arm' or '.word ' in text or text.startswith('bl ') else 2
        # Keep equality sensitive to hidden pool contents as well as operands;
        # only the sanitized text is ever rendered or written.
        lines.append((address,text,hashlib.sha256(data[offset:offset+width]).digest()))
    return lines

def normalize(row):
    text=re.sub(r'\[pc, #[^]]+\]','[pc, pool]',row[1])
    text=re.sub(r'@ =0x[0-9A-Fa-f]+','@ pool',text)
    return re.sub(r'(?<=\s)0x08[0-9A-Fa-f]{6}\b','<branch>',text)

def compare(want,got,start,mode):
    left,right=listing(want,start,mode),listing(got,start,mode)
    matcher=difflib.SequenceMatcher(None,list(map(normalize,left)),list(map(normalize,right)),autojunk=False)
    rows=[]
    for tag,a,b,c,d in matcher.get_opcodes():
        aa,bb=left[a:b],right[c:d]
        for i in range(max(len(aa),len(bb))):
            x=aa[i] if i<len(aa) else None;y=bb[i] if i<len(bb) else None
            rows.append((x,y,bool(x and y and x==y)))
    return rows

def picture(address,name,rows,focus,record,after,original_frame):
    im=Image.new('RGB',(W,H),BG);draw=ImageDraw.Draw(im)
    draw.text((42,28),'TXRA  /  MATCHING C  /  11.09',font=font(22,True),fill=MUTED)
    draw.text((42,73),address+'  '+name,font=font(38,True),fill=FG)
    state='after: retained candidate' if after else 'before: prior candidate'
    draw.text((42,126),state+'  /  same original code view  /  complete owner remains a nonmatch',font=font(23),fill=MUTED)
    draw.text((42,170),f"{record['different_bytes']:,} bytes differ",font=font(39,True),fill=AMBER)
    draw.text((630,181),f"{record['emitted_bytes']:,} / {record['target_bytes']:,} bytes",font=font(28,True),fill=FG)
    frame=record.get('local_frame_bytes')
    draw.text((1120,182),f'frame {frame} / {original_frame}',font=font(26),fill=FG)
    draw.text((42,229),f"Instruction edit distance: {record['instruction_distance']:,}",font=font(23),fill=MUTED)
    draw.text((42,274),'original instructions',font=font(23,True),fill=AMBER)
    draw.text((820,274),'compiled structured C',font=font(23,True),fill=AMBER)
    top=next(i for i,(x,y,equal) in enumerate(rows) if x and x[0]>=focus)
    # Show consecutive instructions in each column. Large moved blocks create
    # long alignment gaps, which otherwise leave most of a review panel empty.
    left_rows=[x for x,y,equal in rows[top:] if x][:23]
    right_top=next((i for i in range(top,len(rows)) if rows[i][1]),None)
    if right_top is None:
        right_top=max(i for i in range(top+1) if rows[i][1])
    right_rows=[y for x,y,equal in rows[right_top:] if y][:23]
    assert len(left_rows)==len(right_rows)==23
    for j,(left,right) in enumerate(zip(left_rows,right_rows)):
        equal=left==right
        y=316+j*24
        draw.rectangle((36,y-2,W-36,y+22),fill=AGREE if equal else BAD)
        for x,item in ((45,left),(823,right)):
            if item:
                text=f'{item[0]:08X}  {item[1]}'
                # Keep the native-size view honest: fail rather than crop code.
                assert draw.textbbox((x,y),text,font=font(18,mono=True))[2] < x+744,text
                draw.text((x,y),text,font=font(18,mono=True),fill=FG)
    draw.line((42,904,W-42,904),fill=BORDER,width=2)
    draw.text((42,922),'Red rows still differ. No replacement was installed or counted as an exact match.',font=font(23),fill=FG)
    draw.text((42,960),'Compiler evidence only; this review does not show a new gameplay or performance milestone.',font=font(20),fill=MUTED)
    return im

def clip(path,before,after):
    command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
             '-s',f'{W}x{H}','-r','30','-i','-','-an','-frames:v','240','-c:v','libvpx-vp9',
             '-b:v','700k','-crf','34','-deadline','realtime','-cpu-used','6','-row-mt','1','-threads','2',str(path)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for frame in range(240):
            im=(before if frame<120 else after).copy();draw=ImageDraw.Draw(im)
            row=(frame%120)*23//120;y=316+row*24
            draw.rectangle((36,y-2,W-36,y+22),outline=AMBER,width=2)
            process.stdin.write(im.tobytes())
        process.stdin.close()
        assert process.wait()==0
    finally:
        if process.poll() is None:
            process.kill();process.wait()
    assert path.stat().st_size <= 4*1024*1024
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    assert len(info['streams'])==1 and info['streams'][0]['codec_type']=='video'
    assert info['streams'][0]['r_frame_rate']=='30/1'
    assert (info['streams'][0]['width'],info['streams'][0]['height'])==(W,H)
    assert 7.9<float(info['format']['duration'])<8.1
    return {'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'seconds':float(info['format']['duration']),'fps':30,'width':W,'height':H,'audio_streams':0}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    output=parser.parse_args().directory;output.mkdir(parents=True,exist_ok=True)
    program=draft.Program();symbols=reloc.symbols(program)
    captions={};artifacts={}
    notes=('TXRA renderer, sound update and HUD code are the three pieces reviewed here. '
        'The new C uses the original path order, sound field pointers and shared HUD addresses, bringing the compiled code closer. '
        'Compare each before and after pair at the same original code view; the captions say how many bytes still differ. '
        'The short muted clips replay those comparisons, and the overview shows decoded frames from all three. '
        'All three remain nonmatches, so the total stays at 181 and there is no new game footage.\n')
    (output/'NOTES.md').write_text(notes)
    (output/'captions.json').write_text('{}\n')
    overview=Image.new('RGB',(1600,1590),BG)
    overview_draw=ImageDraw.Draw(overview)
    for folder,address,name,focus,frame in TARGETS:
        root=Path('docs/near-misses')/folder;images=[]
        for after,label in ((False,'baseline'),(True,'candidate')):
            record=json.loads((root/(label+'.json')).read_text())
            start=int(address,16);end=int(record['target_end'],16)
            source=Path(record['source']);code=source.read_text()
            assert hashlib.sha256(code.encode()).hexdigest()==record['source_sha256']
            actual,_=diagnostic_compile(code,'func_'+address,start,symbols,record['compiler'])
            assert hashlib.sha256(actual).hexdigest()==record['compiled_sha256']
            want=program.rom[start-0x08000000:end-0x08000000]
            rows=compare(want,actual,start,'arm' if record['compiler']=='arm' else 'thumb')
            im=picture(address,name,rows,focus,record,after,frame);images.append(im)
            filename=('after-' if after else 'before-')+address+'.png';im.save(output/filename)
            captions[filename]=('After: ' if after else 'Before: ')+name.lower()+f", {record['different_bytes']:,} bytes still differ; same code view."
            (output/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
            artifacts[filename]={'sha256':hashlib.sha256((output/filename).read_bytes()).hexdigest(),'bytes':(output/filename).stat().st_size,'width':W,'height':H}
        filename=address+'.webm';artifacts[filename]=clip(output/filename,*images)
        captions[filename]='Eight seconds, muted, 30 fps: before then after '+name.lower()+' compiler comparison; still a nonmatch.'
        (output/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
        group=next(i for i,row in enumerate(TARGETS) if row[1]==address)
        overview_draw.text((12,group*530+3),address+'  '+name+'  /  decoded frames every second',font=font(21,True),fill=FG)
        for index in range(8):
            timestamp=index+0.5
            frame_bytes=subprocess.check_output(['ffmpeg','-v','error','-ss',str(timestamp),
                '-i',str(output/filename),'-frames:v','1','-f','image2pipe','-vcodec','png','-'])
            decoded=Image.open(io.BytesIO(frame_bytes)).convert('RGB')
            assert decoded.size==(W,H)
            assert max(decoded.getextrema()[0])-min(decoded.getextrema()[0])>100
            overview.paste(decoded.resize((400,250)),((index%4)*400,group*530+30+(index//4)*250))
    overview.save(output/'clip-overview.png')
    captions['clip-overview.png']='Decoded frames at 0.5 through 7.5 seconds: renderer, sound owner, then HUD; before and after in each row pair.'
    artifacts['clip-overview.png']={'sha256':hashlib.sha256((output/'clip-overview.png').read_bytes()).hexdigest(),
        'bytes':(output/'clip-overview.png').stat().st_size,'width':overview.width,'height':overview.height}
    (output/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
    Path('docs/near-misses/review-1109.json').write_text(json.dumps(artifacts,indent=2)+'\n')
    print(json.dumps(artifacts,indent=2))

if __name__=='__main__':main()
