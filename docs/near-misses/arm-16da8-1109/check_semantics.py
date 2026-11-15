"""Run the existing 199-fixture ARM executor comparison against this candidate."""
import importlib.util
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
prior=HERE.parent/'arm-16da8-1107/check_semantics.py'
spec=importlib.util.spec_from_file_location('arm_semantics_1107',prior)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
# Keep its original assembly root and fixture implementation; select this folder's
# candidate through the original accepted filename and include-search location.
module.HERE=HERE
if __name__=='__main__':
    sys.argv=[sys.argv[0],'--candidate','func_08016DA8.c']
    module.main()
