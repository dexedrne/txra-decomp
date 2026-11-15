"""Run the unchanged independent ARM fixtures against either retained source."""
import argparse
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'arm_semantics_1107', HERE.parent / 'arm-16da8-1107/check_semantics.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--control', action='store_true')
    selected = 'frame-control.c' if parser.parse_args().control else 'func_08016DA8.c'
    # The original runner accepts fixed fixture filenames. A temporary source
    # link selects the actual C without modifying its fixtures or instruction oracle.
    with tempfile.TemporaryDirectory(prefix='arm-source-1109c-') as folder:
        module.HERE = Path(folder)
        (module.HERE / 'func_08016DA8.c').symlink_to(HERE / selected)
        sys.argv = [sys.argv[0], '--candidate', 'func_08016DA8.c']
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            module.main()
        result = json.loads(output.getvalue())
    result['candidate'] = selected
    print(json.dumps(result, indent=2))
