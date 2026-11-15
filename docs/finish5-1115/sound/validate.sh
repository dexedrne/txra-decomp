#!/bin/bash
# Full validation after the install (worker only); one log line block per step.
export PATH=$HOME/opt/txra-venv/bin:$PATH
step() { echo "=== $*"; "$@" 2>&1 | tail -${TAILN:-6}; echo "rc=${PIPESTATUS[0]}"; }
TAILN=4 step make check
TAILN=3 step make recomp
TAILN=3 step make check-runtime
TAILN=4 step make check-mapping
TAILN=3 step make check-accuracy
TAILN=8 step python3 tools/map_completeness.py
TAILN=12 step python3 tools/asm_interfaces.py --completeness
TAILN=12 step python3 tools/progress.py
TAILN=6 step python3 tools/rom_map.py --refine-diff
echo VALIDATE_DONE
