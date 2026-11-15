#!/bin/bash
# Full validation of the integrated finish-6 tree (worker only). One block per step, rc per step.
# Usage on the worker, from the copied tree: bash docs/finish6-1115/integrate6/validate.sh <logdir>
export PATH=$HOME/opt/txra-venv/bin:$PATH
L=${1:?logdir}; mkdir -p build "$L"
step() { echo "=== $*"; "$@" > "$L/step.log" 2>&1; rc=$?; tail -"${TAILN:-6}" "$L/step.log"; echo "rc=$rc"; }
echo "=== committed file hashes (before)"
sha256sum asm/program.s docs/map/finish.json progress.json docs/map/functions.json tools/rom.cfg
echo "=== measure (admission)"
python3 tools/measure_candidate.py src/generated/func_08016DA8.c 08016DA8 08017E68 arm build/m-install > "$L/measure.json" 2> "$L/measure.err"
echo "rc=$?"; cat "$L/measure.json"
echo "=== make clean; make -j8"
make clean > /dev/null 2>&1
make -j8 > "$L/make.log" 2>&1; rc=$?
echo "rc=$rc"; echo "C match lines: $(grep -c 'C match' "$L/make.log")"
grep 'func_08016DA8\|func_080064A4' "$L/make.log"; grep 'txra.gba' "$L/make.log" | tail -2; sha1sum build/txra.gba
TAILN=4 step make check
TAILN=3 step make recomp
TAILN=3 step make check-runtime
TAILN=4 step make check-mapping
TAILN=3 step make check-accuracy
TAILN=8 step python3 tools/map_completeness.py --output build/mc.json
TAILN=14 step python3 tools/asm_interfaces.py --completeness build/mc.json
TAILN=40 step python3 tools/progress.py
TAILN=6 step python3 tools/rom_map.py --refine-diff build/d.json
echo "=== regenerated file hashes (after)"
sha256sum asm/program.s docs/map/finish.json progress.json docs/map/functions.json tools/rom.cfg
echo VALIDATE_DONE
