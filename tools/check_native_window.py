#!/usr/bin/env python3
"""Private Xvfb-only SDL window review. Raw evidence must stay under build/."""
import argparse
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess as S
import time


def layout(width, height, integer=True):
    scale = min(width / 240, height / 160)
    if integer and scale >= 1:
        scale = int(scale)
    w, h = int(240 * scale), int(160 * scale)
    return (width - w) // 2, (height - h) // 2, w, h


def selfcheck():
    assert layout(960, 640) == (0, 0, 960, 640)
    assert layout(800, 600) == (40, 60, 720, 480)
    assert layout(1024, 768) == (32, 64, 960, 640)
    assert layout(240, 160) == (0, 0, 240, 160)
    assert layout(800, 600, False) == (0, 33, 800, 533)
    keys = ('DISPLAY','WINDOW_OWNER_DISPLAY','WINDOW_PRIVATE_X')
    saved = {key:os.environ.get(key) for key in keys}
    try:
        for owner, private in ((':0',':0'),(':1',':98')):
            os.environ.update(DISPLAY=':0',WINDOW_OWNER_DISPLAY=owner,WINDOW_PRIVATE_X=private)
            try:
                private_server()
            except AssertionError:
                pass
            else:
                raise AssertionError('Unsafe display accepted')
    finally:
        for key,value in saved.items():
            if value is None:
                os.environ.pop(key,None)
            else:
                os.environ[key] = value


def private_server():
    display = os.environ['DISPLAY']
    assert display != os.environ.get('WINDOW_OWNER_DISPLAY')
    assert os.environ.get('WINDOW_PRIVATE_X') == display
    assert display.startswith(':') and int(display[1:].split('.')[0]) >= 90
    server = int(Path('/tmp/.X' + display[1:].split('.')[0] + '-lock').read_text().strip())
    server_args = Path(f'/proc/{server}/cmdline').read_bytes().split(b'\0')
    assert server_args[0].endswith(b'Xvfb') and display.encode() in server_args
    assert b'-nolisten' in server_args and b'tcp' in server_args
    authority = Path(os.environ['XAUTHORITY']).resolve()
    assert authority.is_relative_to(Path('build').resolve())
    assert str(authority).encode() in server_args
    return server


class X11:
    def __init__(self, child_pid):
        display = os.environ['DISPLAY']
        self.server_pid = private_server()
        self.x = C.CDLL('libX11.so.6')
        self.t = C.CDLL('libXtst.so.6')
        class Error(C.Structure):
            _fields_ = [('type',C.c_int),('display',C.c_void_p),('resource',C.c_ulong),
                        ('serial',C.c_ulong),('code',C.c_ubyte),('request',C.c_ubyte),('minor',C.c_ubyte)]
        callback_type = C.CFUNCTYPE(C.c_int,C.c_void_p,C.POINTER(Error))
        self.errors = []
        def error_handler(display, error):
            self.errors.append([error.contents.code,error.contents.request])
            return 0
        self.error_callback = callback_type(error_handler)
        self.x.XSetErrorHandler.argtypes = [callback_type]
        self.x.XSetErrorHandler(self.error_callback)
        signatures = {
            'XOpenDisplay': (C.c_void_p, [C.c_char_p]),
            'XDefaultRootWindow': (C.c_ulong, [C.c_void_p]),
            'XQueryTree': (C.c_int, [C.c_void_p, C.c_ulong, C.POINTER(C.c_ulong), C.POINTER(C.c_ulong), C.POINTER(C.POINTER(C.c_ulong)), C.POINTER(C.c_uint)]),
            'XFetchName': (C.c_int, [C.c_void_p, C.c_ulong, C.POINTER(C.c_void_p)]),
            'XFree': (C.c_int, [C.c_void_p]),
            'XGetGeometry': (C.c_int, [C.c_void_p, C.c_ulong, C.POINTER(C.c_ulong), C.POINTER(C.c_int), C.POINTER(C.c_int), C.POINTER(C.c_uint), C.POINTER(C.c_uint), C.POINTER(C.c_uint), C.POINTER(C.c_uint)]),
            'XTranslateCoordinates': (C.c_int, [C.c_void_p, C.c_ulong, C.c_ulong, C.c_int, C.c_int, C.POINTER(C.c_int), C.POINTER(C.c_int), C.POINTER(C.c_ulong)]),
            'XSetInputFocus': (C.c_int, [C.c_void_p, C.c_ulong, C.c_int, C.c_ulong]),
            'XStringToKeysym': (C.c_ulong, [C.c_char_p]),
            'XKeysymToKeycode': (C.c_uint, [C.c_void_p, C.c_ulong]),
            'XResizeWindow': (C.c_int, [C.c_void_p, C.c_ulong, C.c_uint, C.c_uint]),
            'XMoveWindow': (C.c_int, [C.c_void_p, C.c_ulong, C.c_int, C.c_int]),
            'XSync': (C.c_int, [C.c_void_p, C.c_int]),
            'XCloseDisplay': (C.c_int, [C.c_void_p]),
        }
        for name, (result, args) in signatures.items():
            f = getattr(self.x, name)
            f.restype, f.argtypes = result, args
        self.t.XTestFakeKeyEvent.argtypes = [C.c_void_p, C.c_uint, C.c_int, C.c_ulong]
        self.d = self.x.XOpenDisplay(display.encode())
        assert self.d
        self.root = self.x.XDefaultRootWindow(self.d)
        self.window = 0
        deadline = time.monotonic() + 20
        def find(window):
            root, parent, count = C.c_ulong(), C.c_ulong(), C.c_uint()
            children = C.POINTER(C.c_ulong)()
            self.x.XQueryTree(self.d, window, C.byref(root), C.byref(parent), C.byref(children), C.byref(count))
            for i in range(count.value):
                name = C.c_void_p()
                if self.x.XFetchName(self.d, children[i], C.byref(name)) and name.value:
                    title = C.string_at(name)
                    self.x.XFree(name)
                    if title == b'TXRA':
                        self.window = children[i]
                if not self.window:
                    find(children[i])
            if children:
                self.x.XFree(children)
        while time.monotonic() < deadline and not self.window:
            find(self.root)
            time.sleep(.1)
        assert self.window, 'No actual TXRA X11 window'
        # Xvfb belongs to this harness, and the only native child is pinned below.
        assert Path(f'/proc/{child_pid}').exists()
        self.x.XSetInputFocus(self.d, self.window, 1, 0)
        self.x.XSync(self.d, 0)
        assert not self.errors, self.errors

    def minimum(self):
        class Hints(C.Structure):
            _fields_ = [('flags', C.c_long), ('values', C.c_int * 16), ('gravity', C.c_int)]
        hints, supplied = Hints(), C.c_long()
        self.x.XGetWMNormalHints.argtypes = [C.c_void_p, C.c_ulong, C.POINTER(Hints), C.POINTER(C.c_long)]
        assert self.x.XGetWMNormalHints(self.d, self.window, C.byref(hints), C.byref(supplied))
        assert hints.flags & (1 << 4)
        return list(hints.values)[4:6]

    def geometry(self):
        root, x, y, w, h, border, depth = C.c_ulong(), C.c_int(), C.c_int(), C.c_uint(), C.c_uint(), C.c_uint(), C.c_uint()
        assert self.x.XGetGeometry(self.d, self.window, C.byref(root), C.byref(x), C.byref(y), C.byref(w), C.byref(h), C.byref(border), C.byref(depth))
        child = C.c_ulong()
        assert self.x.XTranslateCoordinates(self.d, self.window, self.root, 0, 0, C.byref(x), C.byref(y), C.byref(child))
        return [x.value, y.value, w.value, h.value, depth.value]

    def key(self, name, duration=.08):
        code = self.x.XKeysymToKeycode(self.d, self.x.XStringToKeysym(name.encode()))
        assert code, name
        self.t.XTestFakeKeyEvent(self.d, code, 1, 0)
        self.x.XSync(self.d, 0)
        time.sleep(duration)
        self.t.XTestFakeKeyEvent(self.d, code, 0, 0)
        self.x.XSync(self.d, 0)
        time.sleep(.2)

    def resize(self, w, h):
        self.x.XMoveWindow(self.d, self.window, 0, 0)
        self.x.XResizeWindow(self.d, self.window, w, h)
        self.x.XSync(self.d, 0)
        time.sleep(.4)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selfcheck', action='store_true')
    p.add_argument('--output', type=Path, default=Path('build/window-review'))
    p.add_argument('--scenario', choices=('interactive','race','rebind'), default='interactive')
    p.add_argument('--profile', type=Path)
    a = p.parse_args()
    if not __debug__:
        p.error('Window checks require assertions; do not use optimized Python')
    selfcheck()
    if a.selfcheck:
        print('5 layout and 2 private-display rejection selfchecks passed')
        return
    def interrupted(signum, frame):
        raise TimeoutError('Private window review interrupted')
    signal.signal(signal.SIGTERM, interrupted)
    out = a.output.resolve()
    assert out.is_relative_to(Path('build').resolve())
    out.mkdir(parents=True, exist_ok=True)
    data = a.profile.resolve() if a.profile else out / 'profile'
    assert data.is_relative_to(Path('build').resolve())
    env = dict(os.environ, XDG_DATA_HOME=str(data), SDL_VIDEODRIVER='x11', SDL_RENDER_DRIVER='software', SDL_AUDIODRIVER='dummy')
    for key in ('WAYLAND_DISPLAY', 'DBUS_SESSION_BUS_ADDRESS', 'PULSE_SERVER', 'SESSION_MANAGER', 'AT_SPI_BUS_ADDRESS'):
        env.pop(key, None)
    runtime = out/'runtime'
    runtime.mkdir(mode=0o700, exist_ok=True)
    env.update(XDG_CONFIG_HOME=str(out/'config'), XDG_CACHE_HOME=str(out/'cache'),
               XDG_RUNTIME_DIR=str(runtime), NO_AT_BRIDGE='1', GTK_IM_MODULE='none',
               GSETTINGS_BACKEND='memory', DBUS_SESSION_BUS_ADDRESS='unix:path='+str(out/'no-session-bus'))
    private_server()  # Validate before launching any client on this server.
    wm_log = (out/'wm.log').open('w')
    wm = S.Popen(['metacity','--sm-disable','--no-composite'],env=env,stdout=wm_log,stderr=wm_log)
    time.sleep(1)
    assert wm.poll() is None, 'Private window manager failed'
    log = (out / 'native.log').open('w')
    command = [str(Path('build/txra-pc').resolve()), '--rom', str(Path('baserom.gba').resolve()), '--mute', '--frames', '12000', '--stats', str(out/'window.json'), '--screenshot', str(out/'guest.ppm')]
    if a.scenario == 'race':
        command[command.index('12000')] = '4300'
        command += ['--input-script',str(Path('tests/race-input.txt').resolve()),
                    '--frame-hashes',str(out/'frames.txt'),'--audio-dump',str(out/'audio.pcm'),
                    '--save',str(out/'window.sav')]
    child = S.Popen(command, env=env, stdout=log, stderr=log)
    receipts = {'native_pid': child.pid, 'wm_pid':wm.pid, 'display': env['DISPLAY'], 'captures': {}, 'events': []}
    captions = {}
    x = None
    recording = None
    def key(name):
        x.key(name)
        receipts['events'].append(name)
    def capture(name, match=True):
        assert child.poll() is None
        if match:
            key('F8')
            time.sleep(2.7)  # Let the screenshot notice expire; guest remains paused.
        g = x.geometry()
        target = out / (name + '.png')
        S.run(['ffmpeg','-v','error','-y','-f','x11grab','-draw_mouse','0','-video_size',f'{g[2]}x{g[3]}','-i',f"{env['DISPLAY']}+{g[0]},{g[1]}",'-frames:v','1',str(target)], check=True, timeout=15)
        rgb = S.check_output(['ffmpeg','-v','error','-i',str(target),'-f','rawvideo','-pix_fmt','rgb24','-'], timeout=10)
        assert len(set(zip(rgb[::3],rgb[1::3],rgb[2::3]))) > 8, 'Blank display'
        r = {'geometry':g, 'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
        if match:
            bmp = max(data.rglob('shot-*.bmp'), key=lambda f:f.stat().st_mtime_ns)
            native = S.check_output(['ffmpeg','-v','error','-i',str(bmp),'-f','rawvideo','-pix_fmt','rgb24','-'], timeout=10)
            dx,dy,w,h = layout(g[2],g[3])
            errors = 0
            for yy in range(g[3]):
                for xx in range(g[2]):
                    expected = b'\0\0\0'
                    if dx <= xx < dx+w and dy <= yy < dy+h:
                        n = (((yy-dy)*160//h)*240 + (xx-dx)*240//w)*3
                        expected = native[n:n+3]
                    n = (yy*g[2]+xx)*3
                    errors += rgb[n:n+3] != expected
            assert errors == 0, (name, errors)
            r['native_scaled_pixel_mismatches'] = errors
        receipts['captures'][name] = r
        captions[target.name] = name.replace('-', ' ') + ' — actual private SDL window'
    try:
        deadline = time.monotonic()+20
        while 'Renderer:' not in (out/'native.log').read_text():
            assert child.poll() is None and time.monotonic() < deadline, 'Native SDL setup failed'
            time.sleep(.1)
        time.sleep(.5)  # SDL renderer probing can create and destroy temporary X windows.
        x = X11(child.pid)
        receipts['xvfb_pid'] = x.server_pid
        assert x.geometry()[2:4] == [960,640]
        receipts['minimum_size_hint'] = x.minimum()
        assert receipts['minimum_size_hint'] == [240,160]
        if a.scenario == 'race':
            deadline = time.monotonic()+110
            while len((out/'frames.txt').read_text().splitlines()) < 3200:
                assert child.poll() is None and time.monotonic() < deadline, 'Race capture timeout'
                time.sleep(.25)
            capture('race-running', False)
            clip = out/'race-motion.webm'
            g = x.geometry()
            S.run(['ffmpeg','-v','error','-y','-f','x11grab','-draw_mouse','0','-framerate','30',
                   '-video_size',f'{g[2]}x{g[3]}','-i',f"{env['DISPLAY']}+{g[0]},{g[1]}",
                   '-t','5','-an','-c:v','libvpx-vp9','-deadline','realtime','-cpu-used','8',
                   '-r','30','-fps_mode','cfr','-b:v','900k','-threads','1',str(clip)],check=True,timeout=20)
            assert clip.stat().st_size < 4*1024*1024
            captions[clip.name] = 'Actual SDL race motion with the existing deterministic guest input'
            assert child.wait(timeout=40) == 0
            stats = json.loads((out/'window.json').read_text())
            assert stats['functions_compiled'] == 229
            receipts['stats'] = stats
            import check_accuracy
            golden = json.loads(Path('tests/runtime-golden.json').read_text())
            (out/'run.json').write_text(json.dumps(stats)+'\n')
            check_accuracy.check(out, golden)
            reference = out/'headless'
            reference.mkdir()
            with (reference/'native.log').open('w') as ref_log:
                S.run([command[0],'--rom',command[2],'--headless','--mute','--benchmark',
                       '--frames','4300','--input-script',str(Path('tests/race-input.txt').resolve()),
                       '--save',str(reference/'fresh.sav'),'--stats',str(reference/'run.json'),
                       '--frame-hashes',str(reference/'frames.txt'),'--audio-dump',str(reference/'audio.pcm')],
                      env=env,stdout=ref_log,stderr=ref_log,check=True,timeout=60)
            check_accuracy.check(reference, golden)
            receipts['visible_and_headless_golden_passed'] = True
            print('4300 actual-window and 4300 headless frames match every golden hash, PCM byte and state')
            return
        if a.scenario == 'rebind':
            bindings = data/'dexedrne/TXRA/bindings.ini'
            before_bindings = bindings.read_bytes()
            assert b'key.start=Q\n' in before_bindings
            time.sleep(17)
            key('Escape')
            capture('rebound-before-start')
            g = x.geometry()
            clip = out/'rebound-menu.webm'
            recording = S.Popen(['ffmpeg','-v','error','-y','-f','x11grab','-draw_mouse','0',
                '-framerate','30','-video_size',f'{g[2]}x{g[3]}','-i',f"{env['DISPLAY']}+{g[0]},{g[1]}",
                '-t','5','-an','-c:v','libvpx-vp9','-deadline','realtime','-cpu-used','8',
                '-r','30','-fps_mode','cfr','-b:v','900k','-threads','1',str(clip)])
            time.sleep(.5)
            key('Escape')
            key('q')
            time.sleep(1)
            key('Escape')
            try:
                assert recording.wait(timeout=15) == 0
            finally:
                if recording.poll() is None:
                    recording.terminate()
                    recording.wait(timeout=5)
            assert clip.stat().st_size < 4*1024*1024
            captions[clip.name] = 'Actual Q binding advances the guest title menu after restart'
            capture('rebound-after-start')
            key('Up')
            key('Return')
            assert child.wait(timeout=10) == 0
            assert bindings.read_bytes() == before_bindings
            receipts['persisted_binding_unchanged'] = True
            receipts['stats'] = json.loads((out/'window.json').read_text())
            assert receipts['stats']['functions_compiled'] == 229
            assert all(receipts['stats'][k] == 0 for k in ('fallback_steps','unknown_targets','unsupported'))
            print('Persisted Start=Q loaded on restart; actual Q sent and menu quit completed')
            return
        time.sleep(7)
        capture('default-running', False)
        key('Escape')
        capture('default-paused')
        x.resize(800,600)
        capture('resized-letterbox')
        x.resize(240,160)
        capture('minimum-paused')
        x.resize(120,80)
        assert x.geometry()[2:4] == [240,160], x.geometry()
        receipts['below_minimum_clamped'] = True
        x.resize(800,600)
        key('F11')
        time.sleep(.6)
        assert x.geometry()[2:4] == [1024,768], x.geometry()
        capture('fullscreen-paused')
        key('F11')
        time.sleep(.6)
        assert x.geometry()[2:4] == [800,600], x.geometry()
        key('Escape')
        clip = out/'resume-motion.webm'
        g = x.geometry()
        S.run(['ffmpeg','-v','error','-y','-f','x11grab','-draw_mouse','0','-framerate','30','-video_size',f'{g[2]}x{g[3]}','-i',f"{env['DISPLAY']}+{g[0]},{g[1]}",'-t','5','-an','-c:v','libvpx-vp9','-deadline','realtime','-cpu-used','8','-r','30','-fps_mode','cfr','-b:v','600k','-threads','1',str(clip)],check=True,timeout=20)
        assert clip.stat().st_size < 4*1024*1024
        captions[clip.name] = 'Resumed guest motion in the resized SDL window, muted'
        key('Escape')
        key('Up')  # Wrap from Resume to Quit.
        capture('quit-selected')
        key('Return')
        assert child.wait(timeout=10) == 0
        text = (out/'native.log').read_text()
        assert text.count('Host menu paused') == 2 and text.count('Host menu resumed') == 1
        transitions = re.findall(r'Host menu (paused|resumed) at frame (\d+)',text)
        assert transitions[0][1] == transitions[1][1]
        assert int(transitions[2][1]) > int(transitions[1][1])
        receipts['menu_transitions'] = transitions
        stats = json.loads((out/'window.json').read_text())
        assert stats['functions_compiled'] == 229
        assert all(stats[k] == 0 for k in ('fallback_steps','unknown_targets','unsupported'))
        receipts['stats'] = stats
    finally:
        if recording is not None and recording.poll() is None:
            recording.terminate()
            recording.wait(timeout=5)
        if child.poll() is None:
            child.terminate()
            child.wait(timeout=10)
        if x:
            x.x.XCloseDisplay(x.d)
        wm.terminate()
        wm.wait(timeout=10)
        wm_log.close()
        log.close()
        receipts['native_closed'] = not Path(f'/proc/{child.pid}').exists()
        receipts['wm_closed'] = not Path(f'/proc/{wm.pid}').exists()
        (out/'receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
        (out/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
    print('Actual X11 window, keyboard menu, resize, fullscreen, pixel scaling and quit passed')


if __name__ == '__main__':
    main()
