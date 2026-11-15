# 080064A4 sound owner, 15 November finish4 round (label: sound)

Uninstalled near-miss for the complete owner 080064A4..08007398 (pool included). It is not
byte-exact and is not counted as a match.

| `tools/measure_candidate.py`, `old`, strict end 08007398 | finish3 (11/15) | this round |
| --- | ---: | ---: |
| Differing bytes | 159 | **90** |
| Instruction edit distance | 134 | **87** |
| Emitted / target bytes | 3,828 / 3,828 | 3,828 / 3,828 |
| Local frame / target | 108 / 108 | 108 / 108 |
| Aligned identical rows (of 1,725) | 1,592 | **1,638** |
| Register-only rows / shape rows | 131 / 10 | 87 / 7 |

Source sha256 and compiled sha256 are in `candidate.json`. The full sanitized instruction diff
is in `candidate.diff.txt` (pool words shown as `<literal pool>`, no encodings). Plain
structured C: no padding, inline assembly, fixed registers or widened checker. The 7 shape
rows are literal-pool alignment halfwords only; every instruction shape, the length and every
sp offset match.

## What changed from the finish3 source

Each step was compiled and measured on worker A with the official compiler.

| Change | Differing bytes | Distance | Register rows A / B / D |
| --- | ---: | ---: | --- |
| finish3 source | 159 | 134 | 12 / 22 / 97 |
| Noise channel: its slide and volume envelopes use the function-level `slide` pointer (shared with the three tone slide sections) instead of a block-local `seq` | 116 | 104 | 12 / 22 / 67 |
| Clear loop: `s8 *b = gMixBuffer; s8 z = 0; for (i = 175; i >= 0; i--) b[idx * 176 + i] = z;` | 97 | 94 | 7 / 20 / 67 |
| Scale loop: `s8 *b = gMixBuffer; buffer = b + idx * 176;` | **90** | **87** | **0** / 20 / 67 |

Why each one works (private debug build, `docs/finish4-1115/sound/`):

- **Shared envelope pointer.** With the noise channel on the same pseudo, the pointer has
  refs 72 / live length 193 (priority 2.24). It now outranks the three `&pitch_cursor`
  temporaries (1.96), which then take r5 as in the original. Region D drops from 97 to 67
  register rows. What remains in D is one decision: the pointer must get r2 before the
  slide sum `p` (8.33) and the three B5/B6 `&slide[cursor]` temporaries (3.86). A what-if
  r2 preference on the pointer alone (`TXPREF=38:2`) makes all of region D exact.
- **Clear loop.** The original's pointer is a strength-reduced giv: its start value is
  computed as `(idx * 176 + base) + 175` after `i = 175`. The zero (`movs r3, #0`) comes
  before `i = 175`, so it is not a loop movable (those land after the init) but a value set
  in the source before the loop. The indexed loop with `b` and `z` gives that exact order.
- **Scale loop.** The base is now its own local (r2, dies in the add), so `buffer` is born
  at the add, takes r1, and the counter `j` takes r2, as in the original. Region A is exact.

## What still differs (90 bytes, all register choice)

- **Envelope tick, region D, 67 register rows.** One allocator decision: the shared pointer
  needs r2 before `p` and the `&slide[cursor]` temporaries are allocated. In the debug build
  only a preference on the pointer itself does this (a scan of single r2 preferences on every
  allocno that conflicts with `p` or the temporaries finds nothing else). No preference for
  r2 exists in this function: in the whole trace only one allocno prefers r2 or r4.
- **Effect loop, 15 register rows.** `events16` (refs 10 / live length 54, priority 0.556) is
  allocated before the base copy (0.533) and `stop` (0.414, whose live length is doubled by
  its constant first set) and takes r2. A live length of 74 or more for `events16`
  (`TXLEN=133:74`) makes the loop exact (`stop` r3, base copy r2, `events16` r4). The plain-C
  ways to double it (a dead `= 0` initialiser, folding the load into the test, `effect->events`)
  either vanish or change the shapes.
- **Tempo counter, 5 register rows.** Local allocation puts the `gTempo` address and its
  loaded value both in r0, so the global `gTempoCounter` address takes r2. The original has
  the `gTempo` address in r2 and the counter address in r3. With this RTL (three local
  quantities; the address quantity never overlaps another quantity in r0) local-alloc cannot
  choose r2. `gTempoCounter += gTempo` gives the original load order but the same address
  registers (6 rows). Sixteen spellings of the statement were measured, and a what-if with no
  hard registers for the four tempo pseudos (all loads become reloads) changes the frame.

With the two what-if decisions together (`TXPREF=38:2,133:4`), the debug build reaches 5
differing bytes: only the tempo block.

## Behaviour check

`docs/near-misses/finish2-1115-sound/diff32.py`, with the finish3 source as reference and
this source as candidate, both compiled unchanged for i386 and run on seeded synthetic states:
**1000/1000** identical with seed 1115 and **1000/1000** with seed 2026. This is a C-to-C
regression check, not an original-instruction oracle.

Reproduce on a worker: `python3 tools/measure_candidate.py docs/near-misses/finish4-1115-sound/func_080064A4.c 080064A4 08007398 old build/x`
and `python3 docs/finish4-1115/sound/align.py docs/near-misses/finish4-1115-sound/func_080064A4.c`.
