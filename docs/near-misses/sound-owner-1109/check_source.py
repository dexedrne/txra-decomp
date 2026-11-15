"""Run the existing seven sound-owner fixture groups against a selected C file."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def check(candidate):
    candidate=Path(candidate).resolve()
    registry=(ROOT/'tools/rom.cfg').read_bytes()
    config=json.loads(registry)
    assert not [m for m in config['matches'] if m['offset']<0x7398 and 0x64A4<m['offset']+m['size']]
    with tempfile.TemporaryDirectory(prefix='sound-source-1109-') as td:
        directory=Path(td)
        # Use the unchanged test body in a fresh directory so its quoted include
        # selects this pass's actual candidate instead of the older sibling file.
        tests=(HERE.parent/'sound-owner-1107/test_sound_owner.c').read_text()
        (directory/'test.c').write_text(tests.replace('#include "func_080064A4.c"','#include "candidate.c"'))
        (directory/'candidate.c').write_text(candidate.read_text())
        aliases=[]
        for name in re.findall(r'extern (?:s32|u32) (g_030077[0-9A-F]{2})\[\];',candidate.read_text()):
            offset=int(name[2:],16)-0x03007770
            assert 0 < offset < 72 and offset % 4 == 0
            aliases.append('-Wl,--defsym,'+name+'=g_03007770+'+str(offset))
        result=subprocess.run([shutil.which('cc'),'-std=c11','-O1','-Wall','-Wextra','-Werror',
                        '-fsanitize=undefined','-fno-sanitize-recover=all','-fno-pie','-no-pie',
                        directory/'test.c','-Wl,--defsym,g_08333324=test_steps+4',*aliases,
                        '-o',directory/'check'],check=True,capture_output=True,text=True)
        executed=subprocess.run([directory/'check'],check=True,capture_output=True,text=True)
    assert (ROOT/'tools/rom.cfg').read_bytes()==registry
    return {'candidate':candidate.name,'source_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),
            'fixture_groups':7,'undefined_behavior_sanitizer':True,'registry_unchanged':True,
            'voice_field_aliases':len(aliases),
            'rom_used':False,'output':executed.stdout.strip()}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',type=Path,default=HERE/'func_080064A4.c')
    print(json.dumps(check(parser.parse_args().candidate),indent=2))
