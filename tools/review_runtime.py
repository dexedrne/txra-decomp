#!/usr/bin/env python3
"""Capture the native window on a private local virtual display (no browser)."""
import argparse
import ctypes as C
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output', type=Path)
    p.add_argument('--xvfb', default=shutil.which('Xvfb') or str(Path.home() / 'opt/txra-capture/usr/bin/Xvfb'))
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    output = a.output.resolve()
    captions = json.loads((output / 'captions.json').read_text()) if (output / 'captions.json').exists() else {}
    x = C.CDLL('libX11.so.6'); xt = C.CDLL('libXtst.so.6')
    x.XOpenDisplay.argtypes = [C.c_char_p]; x.XOpenDisplay.restype = C.c_void_p
    x.XDefaultRootWindow.argtypes = [C.c_void_p]; x.XDefaultRootWindow.restype = C.c_ulong
    x.XQueryTree.argtypes = [C.c_void_p,C.c_ulong,C.POINTER(C.c_ulong),C.POINTER(C.c_ulong),C.POINTER(C.POINTER(C.c_ulong)),C.POINTER(C.c_uint)]
    x.XSetInputFocus.argtypes = [C.c_void_p,C.c_ulong,C.c_int,C.c_ulong]
    x.XKeysymToKeycode.argtypes = [C.c_void_p,C.c_ulong];x.XKeysymToKeycode.restype = C.c_uint
    x.XStringToKeysym.argtypes = [C.c_char_p]; x.XStringToKeysym.restype = C.c_ulong
    x.XFlush.argtypes = [C.c_void_p];x.XCloseDisplay.argtypes = [C.c_void_p]
    x.XFree.argtypes = [C.c_void_p]
    x.XFetchName.argtypes = [C.c_void_p,C.c_ulong,C.POINTER(C.c_char_p)]
    x.XResizeWindow.argtypes = [C.c_void_p,C.c_ulong,C.c_uint,C.c_uint]
    xt.XTestFakeKeyEvent.argtypes = [C.c_void_p,C.c_uint,C.c_int,C.c_ulong]
    with tempfile.TemporaryDirectory(prefix='txra-window-',dir=Path.home()/'.cache') as temp:
        root = Path(temp);display=None;game=None;rec=None
        log = (output / 'window-test.log').open('w')
        server = subprocess.Popen([a.xvfb,'-displayfd','1','-screen','0','1280x800x24','-nolisten','tcp'],stdout=subprocess.PIPE,stderr=log,text=True)
        try:
            number = server.stdout.readline().strip()
            if not number: raise RuntimeError('Virtual display failed to start')
            env = dict(os.environ,DISPLAY=':'+number,SDL_AUDIODRIVER='dummy',SDL_RENDER_DRIVER='software',XDG_DATA_HOME=str(root/'data'))
            display = x.XOpenDisplay(env['DISPLAY'].encode());assert display
            script = root/'ui.txt';script.write_text('900 pause\n')
            game = subprocess.Popen([str(Path('build/txra-pc').resolve()),'--rom',str(Path('baserom.gba').resolve()),
                '--mute','--no-focus-pause','--save',str(root/'review.sav'),'--ui-script',str(script),'--stats',str(root/'stats.json')],env=env,stdout=log,stderr=log)
            until=time.monotonic()+90
            while 'Host menu paused at frame 900' not in (output/'window-test.log').read_text():
                assert game.poll() is None, 'Game exited before capture'
                if time.monotonic()>until: raise RuntimeError('Game did not reach the scripted pause')
                time.sleep(.1)
            time.sleep(.3)
            parent=C.c_ulong();rt=C.c_ulong();children=C.POINTER(C.c_ulong)();count=C.c_uint()
            assert x.XQueryTree(display,x.XDefaultRootWindow(display),C.byref(rt),C.byref(parent),C.byref(children),C.byref(count))
            assert count.value
            window=None
            for i in range(count.value):
                name=C.c_char_p()
                if x.XFetchName(display,children[i],C.byref(name)) and name.value:
                    if name.value==b'TXRA': window=children[i]
                    x.XFree(name)
            x.XFree(children)
            assert window, 'Native window not found'
            x.XSetInputFocus(display,window,1,0);x.XFlush(display)
            def down(key):
                code=x.XKeysymToKeycode(display,x.XStringToKeysym(key.encode()))
                xt.XTestFakeKeyEvent(display,code,1,0);x.XFlush(display)
            def up(key):
                code=x.XKeysymToKeycode(display,x.XStringToKeysym(key.encode()))
                xt.XTestFakeKeyEvent(display,code,0,0);x.XFlush(display)
            def tap(key):
                down(key);time.sleep(.1);up(key);time.sleep(.3)
            def picture(name,caption):
                subprocess.run(['ffmpeg','-v','error','-y','-f','x11grab','-video_size','1280x800','-i',env['DISPLAY'],
                                '-frames:v','1',str(output/name)],check=True)
                captions[name]=caption
            picture('pause-window.png','After: native PC pause menu over the original title, in a real window.')
            rec=subprocess.Popen(['ffmpeg','-v','error','-y','-f','x11grab','-framerate','30','-video_size','1280x800',
                '-i',env['DISPLAY'],'-t','10','-c:v','libvpx-vp9','-crf','36','-b:v','0','-cpu-used','4','-an',str(output/'desktop-menu.webm')])
            time.sleep(.4);tap('F11');time.sleep(.35)
            picture('fullscreen.png','After: fullscreen integer scaling preserves 3:2 pixels and side borders.')
            tap('Down');tap('Down');tap('Return');time.sleep(.25)
            picture('aspect-fit.png','After: aspect-fit selected from the pause menu.')
            tap('F8');time.sleep(.2)
            tap('Escape');down('Tab');time.sleep(.7)
            picture('speed-up.png','After: hold Tab for 3x debug speed; the speed badge is host-only.')
            up('Tab');down('grave');time.sleep(.7)
            picture('slow-motion.png','After: hold grave for half speed; release restores normal pacing.')
            up('grave');tap('Escape');time.sleep(.25)
            # Return to a normal window, then resize to a deliberately awkward aspect ratio.
            tap('F11');x.XResizeWindow(display,window,1030,700);x.XFlush(display);time.sleep(.3)
            picture('resized-aspect.png','After: a wide resized window keeps the original picture aspect ratio.')
            tap('Return')  # selected scale row: back to integer
            picture('resized-integer.png','After: the same window uses whole-pixel scaling with centered black borders.')
            # Select reset and capture its confirmation before cancelling.
            tap('Down');tap('Down');tap('Down');tap('Return')
            picture('reset-confirm.png','After: reset asks for confirmation and retains the old save as a backup.')
            tap('z')
            rec.wait(timeout=30);rec=None
            assert (output/'desktop-menu.webm').stat().st_size<=4_000_000
            captions['desktop-menu.webm']='After: native pause menu, fullscreen, scaling, screenshot and debug-speed controls in motion.'
            # Exit using the menu and verify F8 actually wrote a bitmap in the user folder.
            tap('Down');tap('Return');game.wait(timeout=10)
            assert game.returncode==0
            assert list((root/'data').rglob('shot-*.bmp')), 'Screenshot hotkey did not write a user-folder image'
            (output/'window-stats.json').write_bytes((root/'stats.json').read_bytes())
        finally:
            if rec and rec.poll() is None: rec.terminate();rec.wait(timeout=10)
            if game and game.poll() is None: game.terminate();game.wait(timeout=10)
            if display: x.XCloseDisplay(display)
            server.terminate();server.wait(timeout=10);log.close()
    (output/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
    (output/'NOTES.md').write_text('TXRA now has a PC pause menu, fullscreen and two scaling choices, configurable controls, user-folder saves, screenshots and debug speed keys. Compare the before and after garage and race pictures; the original game picture stays the same. The desktop clip shows the new controls, while the other clips show the moving garage and a short drive. The performance chart measures this worker; a physical controller and listening on real speakers still need a hands-on check.\n')


if __name__=='__main__': main()
