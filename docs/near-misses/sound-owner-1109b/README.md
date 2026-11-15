# 080064A4: preparation identities and command lifetimes

Complete structured-C nonmatches, uninstalled and uncounted. The unchanged
historical `old -O2 -mthumb-interwork` profile compares the complete owner
080064A4..08007398, including pools. No checker boundary was extended.

| Source | Output bytes | Local frame | Instruction edits | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Retained 11/9 primary | 3,644 | 104 | 1,467 | 3,473 |
| `func_080064A4.c` | 3,656 | 100 | 1,452 | 3,395 |
| `preparation-control.c` | 3,668 | 100 | 1,380 | 3,542 |
| Original owner | 3,828 | 108 | — | 0 |

The byte candidate shortens cursor/command-address lifetimes, captures the command
index pointer in the command block, and gives the four sequence updates separate
16-bit hardware results. The voice base is shared through the sequence/voice
phases. Source arithmetic widths and the original two-stage global-volume update
remain intact. The primary still captures more than the original six fields;
its lower byte distance does not establish the correct allocation shape.

Private-host setup review identified a mistake in the prior phased hypothesis:
the fifth preparation pointer is voice offset **48, the volume cursor**, not
offset 64, the arpeggio cursor. The control explicitly captures delay, events,
note, pitch, volume cursor and pitch delay. It uses shared-base delay/note
addresses and reloads the command stream address inside its loop. This lowers
instruction distance from the preceding phased control's 1,397 to 1,380, although
its byte distance is five bytes worse than that control's 3,537. It is retained
as a distinct source hypothesis, not advertised as the byte winner.

`search-summary.json` gives deduplicated source/output counts. `search.json.gz`
records preparation-field identities, typed/shared bases, separate 8/9/72-byte
index expressions, block captures, hardware-result scopes, bounded declaration
orders and the existing learned patterns. Compilation failures are recorded as
invalid source hypotheses; they are not semantic passes or matches. No compiler
family sweep, register binding, assembly, padding or new storage was used.

Each retained source passes the seven existing actual-C synthetic fixture groups
with strict warnings and undefined-behavior sanitization. These are state checks
from the tracked sound paths, **not an independent instruction oracle**, real
audio/device execution, or proof for malformed command streams and arbitrary
aliasing. The fixture implementation and its original limitations are unchanged.
`candidate-checks.json` and `preparation-control-checks.json` pin the tested C.

Reproduce from the repository root with the existing project Python environment:

```
python tools/measure_candidate.py docs/near-misses/sound-owner-1109b/func_080064A4.c 080064A4 08007398 old build/sound-1109b-check
python3 docs/near-misses/sound-owner-1109/check_source.py --candidate docs/near-misses/sound-owner-1109b/func_080064A4.c
python3 docs/near-misses/sound-owner-1109/check_source.py --candidate docs/near-misses/sound-owner-1109b/preparation-control.c
```

Next concrete step: continue from the corrected preparation control. Its compiler
chooses the delay-field address as a common base, keeps the volume cursor in a
high register and spills the voice counter/base differently. Recover the original
base-of-voice lifetime in the four-sequence loop and its transition into voice
preparation, before changing the envelope expressions. In the original, the
voice counter survives in the same high register and all six preparation fields
are stack captures. The explicit command reload improved instruction distance;
three/four command-pointer captures and simple base placement already measured
here did not reconcile the remaining eight-byte frame deficit. Do not repeat
those declarations as a compiler sweep.

Only the best candidate's full sanitized instruction diff is uncompressed.
Control diff and search manifests are gzip files. No raw instruction encoding,
pool contents, ROM slice or extracted binary is retained in this folder.
