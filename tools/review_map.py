#!/usr/bin/env python3
"""Render coverage metadata only. Never opens the ROM or game framebuffers."""
import argparse
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

COLORS={'code':'#ffb12a','data':'#639ee8','graphics':'#b39afb','audio':'#ed80a5',
        'table':'#7c7ce5','text':'#e2c074','compressed':'#ed7962','fill':'#cbd2dc','unknown':'#303b4d'}
NAMES={'code':'Code','data':'Read / transfer data','graphics':'Graphics / palettes','audio':'Audio',
       'table':'Tables / literals','text':'Text','compressed':'Compressed','fill':'Fill','unknown':'Unknown'}
BG='#101725';FG='#f2eedf';MUTED='#b0bbce'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)
def base(title,subtitle):
    im=Image.new('RGB',(1600,1000),BG);d=ImageDraw.Draw(im)
    d.text((58,34),'TXRA  /  ROM MAPPING',font=font(20,True),fill=MUTED)
    d.text((58,78),title,font=font(43,True),fill=FG)
    d.text((58,143),subtitle,font=font(21),fill=MUTED)
    return im,d

def counts(spans):
    result={k:0 for k in COLORS}
    for block in spans:result[block['type']]+=block['size']
    return result

def heat(spans,label,size):
    im,d=base('The ROM, by byte classification',f'{label}  •  4 MiB image  •  Each row is 256 KiB  •  File offsets in hexadecimal')
    rowbytes=0x40000;left=155;width=1370;top=215;stride=35
    for row in range(16):
        y=top+row*stride
        d.text((58,y+3),f'{row*rowbytes:06X}',font=font(16),fill=MUTED)
        d.rectangle((left,y,left+width,y+23),fill=COLORS['unknown'])
    for block in spans:
        start=block['offset'];end=start+block['size']
        for row in range(start//rowbytes,(end-1)//rowbytes+1):
            a=max(start,row*rowbytes)-row*rowbytes;z=min(end,(row+1)*rowbytes)-row*rowbytes
            x=left+int(a*width/rowbytes);right=left+int(z*width/rowbytes)
            if right>x:d.rectangle((x,top+row*stride,right-1,top+row*stride+23),fill=COLORS[block['type']])
    c=counts(spans)
    mapped=size-c['unknown']
    d.text((58,805),f'{mapped/size:.2%} mapped',font=font(33,True),fill=FG)
    d.text((560,814),f'{mapped:,} mapped bytes   /   {c["unknown"]:,} unknown bytes',font=font(22),fill=MUTED)
    for i,kind in enumerate(COLORS):
        x=58+(i%5)*305;y=875+(i//5)*43
        d.rectangle((x,y+4,x+15,y+19),fill=COLORS[kind])
        d.text((x+26,y),NAMES[kind],font=font(17),fill=FG)
    d.text((58,967),'Metadata only. Tiny ranges are limited by picture resolution; progress counts use exact byte spans.',font=font(15),fill=MUTED)
    return im

def chart(before,after,size):
    im,d=base('Code + data coverage', 'The same 4,194,304 bytes before and after this mapping pass')
    left,width=80,1440
    for y,label,spans in ((285,'Before',before),(565,'After',after)):
        c=counts(spans);code=c['code'];data=size-code-c['unknown'];mapped=code+data
        d.text((left,y-67),label,font=font(32,True),fill=FG)
        pos=left
        for value,color in ((code,COLORS['code']),(data,COLORS['data']),(c['unknown'],COLORS['unknown'])):
            end=pos+value/size*width;d.rectangle((int(pos),y,int(end),y+84),fill=color);pos=end
        d.text((left,y+108),f'{mapped/size:.2%} mapped   •   Code {code/size:.2%}   •   Data + fill {data/size:.2%}',font=font(24,True),fill=FG)
        d.text((left,y+152),f'{mapped:,} mapped bytes   /   {c["unknown"]:,} unknown bytes',font=font(21),fill=MUTED)
    for i,(name,kind) in enumerate((('Code','code'),('Data + fill','data'),('Unknown','unknown'))):
        x=80+i*475;d.rectangle((x,805,x+25,830),fill=COLORS[kind]);d.text((x+40,803),name,font=font(23),fill=FG)
    d.text((80,895),'Observed reads establish only the bytes accessed. They do not establish complete asset boundaries.',font=font(21),fill=MUTED)
    d.text((80,934),'Static candidates and observed paths do not prove that every function or course has been found.',font=font(21),fill=MUTED)
    return im

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('review',type=Path)
    parser.add_argument('--before-config',type=Path)
    parser.add_argument('--before-splits',type=Path,default=Path('build/map2/before-splits.json'))
    args=parser.parse_args();root=args.review;root.mkdir(parents=True,exist_ok=True)
    cfg=json.loads(Path('tools/rom.cfg').read_text());size=cfg['size'];after=cfg['mapping']
    splits=json.loads(args.before_splits.read_text())['regions'] if not args.before_config else []
    before=json.loads(args.before_config.read_text())['mapping'] if args.before_config else [{'offset':int(s['start'],16)-cfg['base'],'size':int(s['end'],16)-int(s['start'],16),
             'type':'code' if s['kind'] in ('arm','thumb') else 'unknown'} for s in splits]
    images=[]
    for folder,spans,label in (('before',before,'Before: round 2'),('after',after,'After: round 3 evidence')):
        dest=root/folder;dest.mkdir(exist_ok=True)
        im=heat(spans,label,size);im.save(dest/'rom-heat-strip.png');images.append(im)
        (dest/'NOTES.md').write_text(f'TXRA ROM coverage, {folder} this mapping pass. Compare this picture with the same view in the other folder; dark areas still need evidence. Colors show metadata classifications and contain no game images or ROM content.\n')
        (dest/'captions.json').write_text(json.dumps({'rom-heat-strip.png':f'{folder.capitalize()}: the full ROM by byte classification, in the same view.'},indent=2)+'\n')
    chart(before,after,size).save(root/'mapped-progress.png')
    command=['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','1600x1000','-framerate','30','-i','-',
             '-an','-c:v','libvpx-vp9','-threads','2','-b:v','1100k','-crf','34','-r','30',str(root/'map-progress.webm')]
    encoder=subprocess.Popen(command,stdin=subprocess.PIPE)
    for frame in range(180):
        if frame<45:im=images[0]
        elif frame<105:
            im=images[0].copy();end=int(1000*(frame-44)/60);im.paste(images[1].crop((0,0,1600,end)),(0,0))
        else:im=images[1]
        encoder.stdin.write(im.tobytes())
    encoder.stdin.close()
    if encoder.wait():raise RuntimeError('video encoder failed')
    if (root/'map-progress.webm').stat().st_size>4000000:raise RuntimeError('clip exceeds review limit')
    (root/'NOTES.md').write_text('This is the TXRA ROM mapping work, shown using our coverage tools only. Compare before/ and after/ for the same full-ROM view; the chart separates code from data and fill. Course records, projection lookup values and checked compressed blocks now have mapped byte ranges, while dark areas remain unknown. The muted clip replays the change between the two metadata maps; it contains no game footage.\n')
    (root/'captions.json').write_text(json.dumps({'mapped-progress.png':'Before and after: exact mapped code, data plus fill, and unknown percentages.',
                                                 'map-progress.webm':'Six-second metadata replay: the round 2 map changes to the round 3 structural map.'},indent=2)+'\n')
    print('Rendered two heat maps, one comparison chart, and a muted 6-second 30-fps clip.')

if __name__=='__main__':main()
