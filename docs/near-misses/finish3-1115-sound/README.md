# 080064A4 sound owner, 15 November finish3 round (label: sound)

Uninstalled near-miss for the complete owner 080064A4..08007398 (pool included). It is not
byte-exact and is not counted as a match.

| `tools/measure_candidate.py`, `old`, strict end 08007398 | finish2 (11/15) | this round |
| --- | ---: | ---: |
| Differing bytes | 1,598 | **159** |
| Instruction edit distance | 283 | **134** |
| Emitted / target bytes | 3,820 / 3,828 | **3,828 / 3,828** |
| Local frame / target | 100 / 108 | **108 / 108** |
| Aligned identical rows (of 1,725) | 1,546 | **1,592** |
| Register-only rows / shape rows | 170 / 16 | 131 / 10 |

Source sha256 `8c1c656e…`, compiled sha256 `444d6222…` (`candidate.json`; full sanitized
instruction diff in `candidate.diff.txt`, pool words shown as `<literal pool>`, no encodings).
Plain structured C: no padding, inline assembly, fixed registers or widened checker.

## What changed from the finish2 source

Each change was compiled and measured on worker B; the first one is the frame fix.

| Change | Differing bytes | Frame |
| --- | ---: | ---: |
| finish2 source | 1,598 | 100 |
| 0x67: `piece = commands[cidx + 1] * 256; piece += gFadeLevel; gMasterVolume = piece + (gFadeLevel << 4);` | 203 | **108** |
| Tone slide temporary `p` declared once at function level (shared by the three tone channels) | 198 | 108 |
| Noise channel: `index` block-scoped separately in the slide and volume parts | 182 | 108 |
| Effect loop indexes `events16[gEffects[i].cursor + k]` directly (no `event` pointer) | 175 | 108 |
| Fade: `gFadeLevel + (gFadeLevel << 4)` instead of `gFadeLevel * 17` | 174 | 108 |
| Effect loop uses the function-level `val`; `stop` is `s16` | 160 | 108 |
| `gTempoCounter = gTempo + gTempoCounter;` | **159** | 108 |

### Why the multiply form fixes the frame

The debug-build trace (`docs/finish3-1115/sound/diag-1115.txt`, item 1) shows how the
original frame arises. At the `gFadeLevel` address reload, reload must spill one low register.
Its cost per register is refs × (usable registers at or above it). With `<< 8` the cheapest is
the command index in r2, so only the index is spilled and the frame stays at 100. With
`* 256` the multiply result is a separate 2-reference pseudo in r1, and reload spills that
instead (sp+96). Then three more things follow:

- `piece` later spills from the same r1 and shares that slot, so its second store is kept.
- The next iteration spills `gFadeLevel << 4` (sp+100). Its only store is then deleted by
  `delete_output_reload`, which leaves the unused slot.
- The third iteration spills the index (sp+104).

This is exactly the original's sp+96 / unused sp+100 / sp+104 layout. With this change the
length and every sp offset match the original.

## What still differs (159 bytes, all register choice)

- **Envelope tick, 97 register rows.** The three tone slide sections and the noise channel
  have the envelope pointer in r5/r3 where the original has r2. Global allocation gives the
  denser temporaries first pick: the slide temporary `p` (#2 in priority order), the
  `pitch_cursor` address and the noise index. In the debug build, either of two overrides
  makes all of region D exact:
  - allocating the slide pointer first (or giving it an r2 preference), plus
  - an r2 preference on the noise pointer.

  No natural source variant tried creates that preference (diag items 2 and 4).
- **Effect loop, 22 register rows.** The original has `events16` in r4 and `stop` in r3; here
  they are rotated (r2/r4, with the base copy in r3). An r4 preference on `events16` in the
  debug build leaves 7 rows.
- **Fade/mix, 12 register rows.**
  - The scale loop has buffer r2 / counter r1, against r1 / r2 in the original. The original
    loads `gMixBuffer` into r2 and computes the loop pointer into a new register.
  - The clear loop places its zero constant before `i = 175` in the original.

With all three allocator overrides together, the debug build reaches 31 differing bytes.
Only those last scale/clear-loop and tempo-address rows remain.

## Behaviour check

`docs/near-misses/finish2-1115-sound/diff32.py`, with the finish2 source as reference and
this source as candidate, both compiled unchanged for i386 and run on seeded synthetic states:
**1000/1000** identical with seed 1115 and **1000/1000** with seed 2026. The finish2 source
was itself checked against the 11/11 reference (see its README). This is a C-to-C regression
check, not an original-instruction oracle.

Reproduce on a worker: `python3 tools/measure_candidate.py docs/near-misses/finish3-1115-sound/func_080064A4.c 080064A4 08007398 old build/x`
and `python3 docs/finish3-1115/sound/align.py docs/near-misses/finish3-1115-sound/func_080064A4.c`.
