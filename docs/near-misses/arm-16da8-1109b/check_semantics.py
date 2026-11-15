"""Run the existing independent 199-fixture ARM comparison for this candidate."""
import argparse
import importlib.util
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'arm_semantics_1107', HERE.parent / 'arm-16da8-1107/check_semantics.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.HERE = HERE
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--control', action='store_true', help='check the single-cursor nonmatch')
    selected = 'func_08016DA8_match.c' if parser.parse_args().control else 'func_08016DA8.c'
    sys.argv = [sys.argv[0], '--candidate', selected]
    module.main()
