#!/bin/bash
# measure_all.sh FILE... : official agbcc_arm measurement (tools/measure_candidate.py) of each candidate, one JSON line each (worker only)
mkdir -p build
for f in "$@"; do
  python3 tools/measure_candidate.py "$f" 08016DA8 08017E68 arm build/ms-$(basename $f .c) 2>/dev/null | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(json.dumps({k: d[k] for k in ('source','source_sha256','emitted_bytes','local_frame_bytes','instruction_distance','different_bytes','exact','compiled_sha256')}))"
done
