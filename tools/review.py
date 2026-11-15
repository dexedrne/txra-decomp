#!/usr/bin/env python3
"""Record the native build, never a browser or a recreated game screen."""
import argparse,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('--frames',type=int,default=4000)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
(a.output/'NOTES.md').write_text('TXRA now boots in its own PC build, reaches the title, and accepts input through name entry and car purchase. The clips follow startup, animated menus, race entry, and a short acceleration and steering test. Compare before-boot.png with title.png when the earlier picture is present. Sound fidelity, a full race, and in-game save loading still need verification.\n')
work=Path('build/review');work.mkdir(parents=True,exist_ok=True)
save=work/'fresh.sav'
# This is an isolated disposable review save, never the player's default file.
save.unlink(missing_ok=True)

def run(args):subprocess.run(args,check=True)
def shot(frames,name,extra=()):
    ppm=work/(name+'.ppm')
    run(['build/txra-pc','--headless','--mute','--benchmark','--save',str(save),'--frames',str(frames),'--screenshot',str(ppm),'--stats',str(work/(name+'.json')),*extra])
    run(['ffmpeg','-loglevel','error','-y','-i',str(ppm),'-vf','scale=960:640:flags=neighbor',str(a.output/(name+'.png'))])
shot(300,'startup')
shot(900,'title')
shot(1080,'name-entry',('--auto-start','900'))
shot(2080,'main-menu',('--input-script','tests/boot-input.txt'))
raw=work/'session.bgra'
run(['build/txra-pc','--headless','--mute','--benchmark','--save',str(save),'--frames',str(a.frames),'--input-script','tests/boot-input.txt','--video',str(raw),'--screenshot',str(work/'latest.ppm'),'--stats',str(work/'session.json')])
clips=[('boot',0,6),('title-and-name',11,8),('name-and-car-menu',20,8),('purchase-and-menu',30,8)]
if a.frames>=2850:clips.append(('race-start',40,7))
if a.frames>=4000:clips.append(('driving-attempt',a.frames/60-8,8))
for name,start,duration in clips:
    output=a.output/(name+'.webm')
    run(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pixel_format','bgra','-video_size','240x160','-framerate','30','-ss',str(start),'-i',str(raw),'-t',str(duration),'-vf','scale=720:480:flags=neighbor','-c:v','libvpx-vp9','-crf','34','-b:v','0','-deadline','good','-cpu-used','4','-row-mt','1','-an',str(output)])
    if output.stat().st_size>4_000_000:raise RuntimeError(f'{name} exceeds review size limit')
run(['ffmpeg','-loglevel','error','-y','-i',str(work/'latest.ppm'),'-vf','scale=960:640:flags=neighbor',str(a.output/'latest.png')])
# Preserve captions for already reviewed earlier-attempt pictures.
caption_path=a.output/'captions.json';captions=json.loads(caption_path.read_text()) if caption_path.exists() else {}
captions.update({'startup.png':'After: the PC build renders the startup screen.','title.png':'After: the native title screen and Press Start prompt.','name-entry.png':'After: Start opens the name-entry screen.','main-menu.png':'After: a car purchase reaches the main menu.','latest.png':'After: the last frame of the scripted native boot and menu test.','boot.webm':'After: six seconds of actual PC startup.','title-and-name.webm':'After: the title animation and Start opening name entry.','name-and-car-menu.webm':'After: name confirmation and the animated car-selection menu.','purchase-and-menu.webm':'After: purchasing a car and navigating the main menu.','race-start.webm':'After: the PC build enters a race and renders its starting countdown.','driving-attempt.webm':'After: held acceleration and two steering inputs in the native race test.'})
caption_path.write_text(json.dumps(captions,indent=2)+'\n')
