"""Compare actual candidate C with the prior HUD C on valid synthetic states.

The previous draft is a regression reference, never an original-code oracle.
All six transform globals intentionally alias scratch records 8 and 9.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'recomp')]
from llm_match import PRELUDE

def check(candidate):
    candidate=Path(candidate)
    text=candidate.read_text()
    reference=(HERE.parent/'hand-20261103/func_0800421C.c').read_text()
    registry=(ROOT/'tools/rom.cfg').read_bytes()
    with tempfile.TemporaryDirectory(prefix='hud-source-1109-') as td:
        directory=Path(td)
        (directory/'candidate.c').write_text(PRELUDE+text)
        (directory/'reference.c').write_text(PRELUDE+reference.replace('func_0800421C(void)','reference_hud(void)'))
        (directory/'candidate_declarations.h').write_text(PRELUDE+text[:text.index('void func_0800421C(void)')])
        (directory/'test.c').write_text((HERE/'test_hud.c').read_text())
        aliases=['-Wl,--defsym,g_%08X=g_030057A0+%d'%(address,address-0x030057A0)
                 for address in range(0x03005800,0x03005818,4)]
        command=['cc','-std=c11','-O0','-Wall','-Wextra','-Werror','-Wno-sign-compare','-fno-strict-aliasing',
                 '-fsanitize=undefined','-fno-sanitize-recover=all','-I'+str(ROOT/'src'),
                 directory/'candidate.c',directory/'reference.c',directory/'test.c',*aliases,'-o',directory/'check']
        try:
            subprocess.run(command,check=True,capture_output=True,text=True)
            result=subprocess.run([directory/'check'],check=True,capture_output=True,text=True)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(exc.stderr.replace(str(directory),'temporary-check')) from None
    assert (ROOT/'tools/rom.cfg').read_bytes()==registry
    return dict(candidate=candidate.name,source_sha256=hashlib.sha256(text.encode()).hexdigest(),
                reference_sha256=hashlib.sha256(reference.encode()).hexdigest(),fixtures=1024,
                comparison='prior C draft state and ordered helper calls; not original instructions',
                undefined_behavior_sanitizer=True,transform_aliases=6,registry_unchanged=True,
                rom_used=False,output=result.stdout.strip())

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',type=Path,default=HERE/'func_0800421C.c')
    print(json.dumps(check(parser.parse_args().candidate),indent=2))
