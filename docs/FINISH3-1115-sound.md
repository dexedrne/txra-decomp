# Sound owner 080064A4, finish3 round, 15 November (label: sound)

Target: the sound owner **080064A4..08007378**, pool through 08007398 (3,828 bytes). Starting
point: the finish2 near-miss (1,598 differing bytes, frame 100/108, 8 bytes short).

No exact replacement was installed. `src/`, `tools/rom.cfg` and the registry are unchanged,
and the installed total stays **191**. The new uninstalled near-miss has the original
**length and frame** and cuts the distance by 90%:

| `tools/measure_candidate.py`, `old`, strict end 08007398 | finish2 | this round |
| --- | ---: | ---: |
| Differing bytes | 1,598 | **159** |
| Instruction edit distance | 283 | **134** |
| Emitted / target bytes | 3,820 / 3,828 | **3,828 / 3,828** |
| Local frame / target | 100 / 108 | **108 / 108** |
| Register-only rows | 170 | 131 |

Source and receipts: [finish3-1115-sound](near-misses/finish3-1115-sound/README.md). The
source sha256 is `8c1c656e…` and the compiled sha256 is `444d6222…`. Debug-build tools and the
allocator experiments are in [finish3-1115/sound](finish3-1115/sound/diag-1115.txt).

## How the frame was found

The stream lane's debug compiler was rebuilt on worker B with extra prints (`trace_patch2.py`):

- reload's per-register spill cost;
- spilled pseudos and the stack slot each one gets;
- deleted output reloads;
- global preferences.

It also has diagnostic overrides that change one allocator decision. Its unmodified output is
identical to the official compiler's.

What the trace showed:

1. In the finish2 source, only the command index is spilled by reload. At the `gFadeLevel`
   address reload, the index's r2 is the cheapest register, because reload's cost weights
   lower registers more heavily.
2. Forcing reload to take the master-volume temporary's register there instead gave exactly
   the original layout:
   - the temporary at sp+96;
   - `gFadeLevel << 4` at sp+100, whose store is later deleted, which is the "unused" slot;
   - the index at sp+104.
3. The plain-C spelling that makes reload choose that register by itself is
   `piece = commands[cidx + 1] * 256; piece += gFadeLevel;`. The multiply result becomes its
   own cheap pseudo, and `piece` reuses its slot, which keeps the second store. The 0x67 block
   now matches the original byte for byte, and nothing after 08006DC4 is shifted any more.

The other source changes are listed in the receipts README:

- one shared slide temporary;
- separate block-scoped noise indexes;
- direct event indexing in the effect loop;
- the function-level `val` and an `s16` stop flag in the effect loop;
- operand order in the fade level and the tempo counter.

Each was measured on its own. All are behaviour-preserving: `diff32.py` gives 1000/1000
identical states with seeds 1115 and 2026 against the finish2 source.

## What blocks an exact match

All 159 remaining bytes are register choices; the instruction shapes match.

- **Envelope tick, 08006776..08006D62.** 97 register rows. The tone slide sections and the
  noise channel have the envelope pointer in r5/r3 where the original has r2. Global
  allocation hands r2 to denser temporaries first: the slide temporary (priority #2) and the
  cursor address. In the debug build, two overrides together make the whole region exact:
  allocating the slide pointer first, and giving the noise pointer an r2 preference. None of
  the natural forms tried, including shared/split pointers, `const`, `register` and
  declaration order, produces that order or preference. 48 declaration-order permutations
  gave identical output.
- **Effect loop.** 22 register rows. `events16` / `stop` / base copy are rotated against the
  original's r4 / r3 / r2. An r4 preference on `events16` in the debug build leaves 7 rows.
- **Fade and mix buffer.** 12 register rows. The original loads `gMixBuffer` into r2 and
  computes the scale-loop pointer into a new register. It also places the clear loop's zero
  constant before `i = 175`.

With all three overrides, the debug build reaches 31 differing bytes, leaving only the
scale/clear loops and the tempo-counter addresses.

## Worker runs (worker B)

- All compiles, traces and searches ran on worker B, in the worker copy `~/txra-sound3` and the
  debug-compiler copy `~/txra-sound3-cc`.
- Two detached choice-point searches (`search.py` over `big.tpl`, JOBS 6, nice 5) found one
  small improvement and then plateaued. They ran 8 and 17 minutes and were stopped by their
  exact PIDs.
- Both worker copies were removed at the end.

## Validation (worker B, this branch)

- `make clean && make -j8`: 191 `C match` lines, `build/txra.gba: OK`, SHA-1
  4197339d4add74bb40ed02a8fba5e58096afb487.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`.
- No admission check was run, because nothing was installed.

matches installed: none (191 exact replacements unchanged; 080064A4 not exact)
near-misses improved: 080064A4: 1598 -> 159 differing bytes (instruction distance 283 -> 134; length 3,828/3,828 and frame 108/108 now match)
what blocks the rest: register choice only. Global allocation gives r2 to the dense slide/noise temporaries before the envelope pointers (97 rows in 08006776..08006D62). The effect-loop events16/stop/base registers are rotated (22 rows). The mix-buffer scale and clear loops keep the gMixBuffer base and the loop pointer in one register (12 rows). Debug-build overrides on three allocator decisions reach 31 bytes, but no natural C spelling found yet makes those decisions.
