#!/usr/bin/env python3
"""Exercise user-folder migration, reset confirmation and ROM failure paths."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

binary=Path('build/txra-pc').resolve()
rom=Path('baserom.gba').resolve()
checks=0

def check(value, message):
    global checks
    checks+=1
    assert value,message

with tempfile.TemporaryDirectory(prefix='desktop-flow-',dir='build') as temp:
    root=Path(temp).resolve()
    env=dict(os.environ,XDG_DATA_HOME=str(root/'data'),SDL_AUDIODRIVER='dummy')
    def run(*args, expected=0):
        result=subprocess.run([str(binary),'--rom',str(rom),'--headless','--mute','--benchmark',
            '--frames','2',*args],cwd=root,env=env,capture_output=True,text=True,timeout=15)
        check(result.returncode==expected,result.stderr)
        return result
    legacy=root/'txra.sav';legacy_bytes=bytes(range(256))*2;legacy.write_bytes(legacy_bytes)
    profile=root/'data/dexedrne/TXRA/txra.sav'
    run()
    check(profile.read_bytes()==legacy_bytes,'512-byte save migration changed bytes')
    check(legacy.read_bytes()==legacy_bytes,'Migration changed the original')
    bindings=profile.with_name('bindings.ini')
    check(bindings.exists(),'No first-launch rebinding file')
    data=bytes(reversed(range(256)))*32;profile.write_bytes(data)
    run()
    check(profile.read_bytes()==data,'Existing user profile was overwritten by import')
    run('--reset-save')
    check(not profile.exists(),'Reset retained the active EEPROM')
    backups=list(profile.parent.glob('txra.sav.reset-*.bak'))
    check(len(backups)==1 and backups[0].read_bytes()==data,'Reset lost the original save')
    check(legacy.read_bytes()==legacy_bytes,'Reset changed the legacy source')
    # Menu reset, including confirmation, uses the actual host command path.
    profile.write_bytes(data)
    script=root/'ui.txt'
    script.write_text('0 pause\n'+'0 down\n'*5+'0 accept\n0 cancel\n0 quit\n')
    run('--ui-script',str(script))
    check(profile.read_bytes()==data,'Cancelled reset changed EEPROM')
    script.write_text('0 pause\n'+'0 down\n'*5+'0 accept\n0 accept\n0 quit\n')
    run('--ui-script',str(script))
    check(not profile.exists(),'Confirmed menu reset did not clear the active save')
    backups=list(profile.parent.glob('txra.sav.reset-*.bak'))
    check(len(backups)==2 and all(p.read_bytes()==data for p in backups),'Menu reset backup damaged bytes')
    bad='key.a=not-a-key\n';bindings.write_text(bad)
    run(expected=2)
    check(bindings.read_text()==bad,'Invalid binding file was overwritten')
    bindings.unlink()
    run('--rom',str(root/'missing.gba'),expected=1)
    wrong=root/'wrong.gba';wrong.write_bytes(b'wrong')
    run('--rom',str(wrong),expected=1)
    wrong.write_bytes(bytes(4*1024*1024))
    run('--rom',str(wrong),expected=1)
    wrong.write_bytes(rom.read_bytes()+b'extra')
    run('--rom',str(wrong),expected=1)
    stats=json.loads(profile.with_name('last-run.json').read_text())
    check(not stats['unsupported'],'Host reset led to unsupported instructions')
print(f'{checks} desktop flow checks passed')
