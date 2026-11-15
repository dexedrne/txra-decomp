# Stream owner, 15 November: exact match installed

Target: the road stream owner **08002854..0800418C** (6,456 bytes with pools, 268-byte frame). It contains the registry entry **08003786**, the second pass of its scenery loop.

**The owner is now exact C and installed** as `src/generated/func_08002854.c`, registered in `tools/rom.cfg` with offset 0x2854 and size 6,456. It went from 23 differing bytes to 0. 08003786 is covered by the installed body. The registry stays at 228 entries.

| Measure | 11/14 candidate | Installed |
| --- | ---: | ---: |
| Emitted / target bytes | 6,456 / 6,456 | 6,456 / 6,456 |
| Local frame / original | 268 / 268 | 268 / 268 |
| Instruction edit distance | 20 | **0** |
| Differing bytes | 23 | **0** |

Profile: `old`, `-O2 -mthumb-interwork`, checker end 0800418C. The source is plain structured C, with no padding, inline assembly, fixed registers or hand-written bytes. The measurement receipt is [measure.json](finish2-1115/stream/measure.json): exact, compiled sha256 `ecab29c6…`, source sha256 `55b49019…`.

## The change

Only two statements changed. The 11/14 candidate computed each index in one expression:

```c
following = ((ring + 1) & 31) * 24;
ahead = ((ring + 2) & 31) * 24;
```

The installed source builds each value in place, in its own variable:

```c
following = (ring + 1) & 31;
following *= 24;
ahead = (ring + 2) & 31;
ahead *= 24;
```

Splitting the `&` into its own statement as well (`following = ring + 1; following &= 31; …`) also gives an exact match. All nine combinations are in [variants.json](finish2-1115/stream/variants.json).

## Why it works

The 11/14 note blamed local allocation: it guessed that something kept r1 busy from `ring+2` through the `first` reload. A trace from a debug build of the compiler showed the real cause. The trace is in [reload-trace.txt](finish2-1115/stream/reload-trace.txt), and [trace_patch.py](finish2-1115/stream/trace_patch.py) adds the debug prints. The debug build's assembly output was compared with the official compiler on both sources and is identical. The real cause is reload's round-robin choice of spill register.

- `following` and `ahead` are user variables that live on the stack (sp+40 and sp+44). Written in place, `following = ring + 1` needs an output reload. Reload's round-robin picks it, so `adds r1, r4, #1` is chosen and the rotation advances past r1. The next two statements inherit r1.
- `ahead = ring + 2` uses the two-address add alternative. Ring dies here, so reload uses ring's own register for the output: `adds r4, #2; ands r4, r3`.
- The `first` reload for the point base starts after r1, finds r2 busy and takes r3. The point-base constant then takes r4, and the four GCSE spill stores take r5, r0, r1, r2. This matches the original exactly.
- The candidate kept both indices in local pseudos. Local allocation gave them r1 and left the rotation at r0, so every later choice was off by one register.

### Ruled out on the way

The variant table has the full list.

- **Updating `ring` itself in place** (`ring = (ring + 2) & 31`) gives exactly the right `adds r4, #2` but grows the output to 6,592 bytes with a 148-byte frame. The trace shows why:
  - Ring's priority rises from 5,833 to 12,857, so global allocation assigns it r4 before pseudo 4073.
  - Once a global pseudo owns r4, 4073 can no longer evict the local-alloc pseudos from r4, so it falls back to r9.
  - The cascade then spreads (11/14 numbering): 4621 evicts r8 instead of r9, then 42, which held r8, is spilled, and so on.
- `ring += 2; ahead = (ring & 31) * 24` compiles back to the candidate, because regmove renames it.
- Other forms gave 22–24 differing bytes or worse:
  - symbol versus constant bases;
  - two-dimensional face and point bases;
  - block-scope temporaries;
  - other statement orders.

## Admission and validation (all on worker A)

- `tools/measure_candidate.py src/generated/func_08002854.c 08002854 0800418C old`: `"exact": true`, `"different_bytes": 0`, `"instruction_distance": 0`, `"local_frame_bytes": 268`.
- `make clean; make -j8`:
  - 190 `C match` lines, including `func_08002854: C match (6456 bytes)`;
  - `build/txra.gba: OK`;
  - SHA-1 `4197339d4add74bb40ed02a8fba5e58096afb487`.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`. This ran on the final tree, after a second clean rebuild.
- `make recomp`: `Emitted 228 functions, 258 load/run entries`.
- `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`:
  - `Accuracy: 4300 framebuffer hashes, every PCM byte, final state and sample clock passed`;
  - `fallback=0 unknown=0 unsupported=0`.
- `tools/map_completeness.py`, then `tools/asm_interfaces.py --completeness`, then `tools/progress.py`:
  - 0 verification failures;
  - `docs/map/finish.json` reproduces byte for byte on a second run;
  - `rom_map.py --refine-diff` reports 0 changes.

The 11/14 synthetic behaviour checker (`tools/check_stream_original1112c.py`) was not re-run. The installed bytes are identical to the original, so that checker cannot tell them apart.

## Map, registry and counts

- `tools/asm_interfaces.py`: 08003786 is now `covered-by-installed-owner` (owner 08002854). The stale 08002854 `C-candidate` row and its `OWNER_END` entry are gone.
- `tests/test_match4.py` now checks that `tools/rank_targets.py` reports 08003786 as `covered by installed func_08002854`. That label stays a registry entry, because it is a native recompiler BL target.
- `progress.json → completion` now reads **224 of 228 complete**: 190 exact C, 3 labels inside installed owners (0800D570, 0800D630, 08003786) and 31 assembly interfaces. **4 C owners remain**: 0800421C, 080064A4, 08016DA8 and 080181C0, 13,924 bytes with pools. `functions_matched_c` is 190 functions, 79,618 bytes with pools.
- In instruction bytes, which come from the function spans:
  - exact C owners hold 66,470 of 85,578 (77.7%);
  - documented assembly holds 6,092 (7.1%);
  - the four remaining owners hold 13,016 (15.2%).

  README and `docs/FINISH.md` are updated to match.
- `asm/program.s` was regenerated by `make`, so the owner is now an `.incbin` of the verified leaf. `docs/map/finish.json` and `progress.json` were regenerated on worker A and copied back. All three are metadata only, with no ROM bytes.

## Notes for the other owners

The same debug trace can explain the HUD (0800421C) and sound (080064A4) whole-function allocation differences. It prints three things:

- local qty order with each qty's chosen register;
- global allocation results, including evictions of local-alloc pseudos;
- every reload register choice.

To use it, apply `trace_patch.py` to a private copy of agbcc's `gcc/` on a worker, build with `make old -j1`, and set `TXDBG=LGR`. Always compare its assembly with the official compiler first. It is a diagnostic only and is never used for matching.

Work stayed on `work/finish2-stream`, with no push or merge. Every build, measurement and check ran on worker A, and the laptop only edited files.

matches installed: 08002854 (owner 08002854..0800418C, 6,456 bytes; covers the internal entry 08003786)
near-misses improved: 08002854: 23 -> 0 differing bytes (installed exact; full-ROM SHA-1 4197339d…afb487)
what blocks the rest: four C owners remain (0800421C HUD, 080064A4 sound, 08016DA8 renderer, 080181C0 contact); this lane did not work on them, and their whole-function allocation and loop-pass differences are as described in the 11/14 notes
