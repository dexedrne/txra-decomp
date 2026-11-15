# Sound owner 080064A4, finish4 round, 15 November (label: sound)

Target: the sound owner **080064A4..08007378**, pool through 08007398 (3,828 bytes). Starting
point: the finish3 near-miss (159 differing bytes, length and frame already exact).

No exact replacement was installed. `src/`, `tools/rom.cfg` and the registry are unchanged,
and the installed total stays **192**. The new uninstalled near-miss keeps the original
length and frame and cuts the distance by 43%:

| `tools/measure_candidate.py`, `old`, strict end 08007398 | finish3 | this round |
| --- | ---: | ---: |
| Differing bytes | 159 | **90** |
| Instruction edit distance | 134 | **87** |
| Emitted / target bytes | 3,828 / 3,828 | 3,828 / 3,828 |
| Local frame / target | 108 / 108 | 108 / 108 |
| Register-only rows (A / B / D) | 131 (12 / 22 / 97) | **87 (0 / 20 / 67)** |

Source and receipts: [finish4-1115-sound](near-misses/finish4-1115-sound/README.md). Debug-build
tools and what-if scripts: [finish4-1115/sound](finish4-1115/sound/).

## Source changes (three, each measured on its own)

1. **One envelope pointer for the tone slides and the noise channel.** The noise channel's
   slide and volume envelopes now use the function-level `slide` pointer instead of a
   block-local `seq`: 159 -> 116. The merged pointer (refs 72, live length 193, priority
   2.24) is now allocated before the three `&pitch_cursor` temporaries (1.96), which then take
   r5 as in the original.
2. **Clear loop as an indexed loop.** `s8 *b = gMixBuffer; s8 z = 0;
   for (i = 175; i >= 0; i--) b[idx * 176 + i] = z;`: 116 -> 97. The original pointer is a
   strength-reduced giv whose start is `(idx * 176 + base) + 175`, computed after `i = 175`,
   and the zero register is set before `i = 175`, which a loop movable cannot be (movables
   land after the init). The clear loop is now byte-exact.
3. **Scale loop base in its own local.** `s8 *b = gMixBuffer; buffer = b + idx * 176;`:
   97 -> 90. `buffer` is born at the add and takes r1; the counter `j` takes r2. Region A
   (fade, scale and clear loops) is now exact.

Behaviour: `diff32.py` against the finish3 source gives 1000/1000 identical states for seeds
1115 and 2026.

## Allocator diagnosis (private debug build of old_agbcc, worker A)

The stream and finish3 trace patches were reapplied, plus `trace_patch3.py`, which adds:

- `TXWATCH` (conflict and preference masks of a watched pseudo, with every conflicting
  allocno and its hard register at that moment);
- `TXDBG=A` (the full global order with priorities and pruned preferences);
- what-if overrides `TXLEN` / `TXREFS` (live length or refs of one allocno before sorting),
  `TXSPILL` (keep a pseudo out of global allocation) and `TXNOLOCAL` (keep it out of
  local allocation).

The worker's `~/opt/agbcc/gcc` objects come from the non-OLD `agbcc` build. The copy must be
`make clean`ed before `make old`, otherwise the traced compiler differs from the official one.
`buildcc.sh` does this. Every trace below was checked "traced==official" first.

What-if results on the new source:

| Override | Differing bytes | Region rows left |
| --- | ---: | --- |
| none | 90 | B 20, D 67 |
| `TXPREF=38:2` (shared envelope pointer prefers r2) | 23 | B 20 |
| `TXLEN=133:74` (`events16` live length 74) | 72 | B 5, D 67 |
| `TXPREF=38:2,133:4` | **5** | B 5 (tempo block only) |

- **Region D.** Only the pointer's own r2 preference works. A scan of single r2 preferences
  on each allocno that conflicts with the slide sum `p` (46 allocnos) or the `&slide[cursor]`
  temporaries finds nothing else. The pointer's priority cannot reach `p` (8.33) or the
  temporaries (3.86). In the whole function only one allocno has any r2 or r4 preference,
  because local-alloc rarely puts a quantity in r2. Merging the note-start `seq` pointers into
  `slide` raises its priority to 3.91, but it breaks the note-start code (frame 112). Merging
  `p` into `command` or `j` lowers `p` but not the temporaries.
- **Effect loop.** The original order is base copy (r2), `stop` (r3), `events16` (r4).
  `stop`'s live length is doubled by its constant first set (29 -> 58), and so is `freq`'s.
  `events16` needs the same treatment (any live length of 74 or more works), but its only set
  is a load. A dead `= 0` initialiser is deleted, and `effect->events` changes the loop's
  shapes.
- **Tempo block.** The gTempo address, the counter value and the gTempo value are local
  quantities. The 3-quantity sort (`qty_compare (0, 1)` compares quantity numbers, not
  order slots) never lets the address quantity see r0 occupied, so it always gets r0. The
  original's r2 needs different RTL there. No spelling tried produced it.

## Worker runs (worker A)

- All compiles, traces, what-ifs, searches and behaviour checks ran on worker A, in the worker
  copy `~/txra-sound4` and the debug-compiler copy `~/txra-sound4-cc`.
- A choice-point search over the effect-loop and tempo spellings around the new source
  (`search.py`, `srch.tpl`, 13 choice points, JOBS 10, nice 5, 30-minute limit) ran
  194 neighbourhood steps without an improvement. All 64 combinations of `srch2.tpl` (tone
  slide sum and `val` forms, noise-slide temporary forms) were also measured, and none beats
  the new source. The search ended by its own time limit; no process was left running.
- Both worker copies were removed at the end.

## Validation (worker A, this branch)

- `make clean && make -j8`: rc 0, 192 `C match` lines, `build/txra.gba: OK`, SHA-1
  4197339d4add74bb40ed02a8fba5e58096afb487.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`.
- No admission check was run, because nothing was installed.

matches installed: none (192 exact replacements unchanged; 080064A4 not exact)
near-misses improved: 080064A4: 159 -> 90 differing bytes (instruction distance 134 -> 87; length 3,828/3,828 and frame 108/108 kept; region A now exact)
what blocks the rest: register choice only, three allocator decisions. The shared envelope pointer must take r2 before the slide sum and the &slide[cursor] temporaries (67 rows in region D; only an r2 preference on the pointer does it). The effect loop's events16 must rank below stop (15 rows; needs live length of 74 or more). The tempo block's gTempo address must get r2 from local-alloc (5 rows; impossible with the current RTL). No natural C spelling found yet makes these decisions. With the first two as debug overrides, 5 bytes remain.
