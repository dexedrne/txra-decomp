# Renderer finish pass 2, 15 November (label: renderer)

Target: **08016DA8** (ARM renderer, 4,288 bytes, owner end 08017E68). No exact
match was installed. The registry, `src/` and every installed replacement are
unchanged. Nothing was installed, so the admission gate did not run. A forced
rebuild on worker C (`rm -rf build && make -j8`) still ends with `build/txra.gba: OK`
(SHA-1 4197339d4add74bb40ed02a8fba5e58096afb487). All builds, measurements,
dumps and searches ran on worker C. Nothing ROM-derived left the worker except the
sanitized diff listing that previous rounds also kept (encodings and pool words
removed).

## Result

| Candidate | Differing bytes | Instruction distance | Emitted / target | Frame | Shape rows / register rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| 11/14 natural (`finish-1114-renderer/func_08016DA8.c`) | 2,446 | 622 | 4,288 / 4,288 | 96 | 95 / 552 |
| + scratch-store weighting only (`milestones/yz1.c`) | 2,430 | 597 | 4,288 | 96 | 107 / 525 |
| + face-row fix (`milestones/f1.c`) | 3,290 | 614 | 4,284 | 96 | 98 / 546 |
| hoist-order line (`func_08016DA8_order.c`) | 3,294 | 558 | 4,292 | 96 | 68 / 508 |
| **best (`func_08016DA8.c`)** | **880** | **367** | **4,288 / 4,288** | **96** | 113 / 295 |

The columns are measured as in the 11/14 note: `tools/measure_candidate.py`
(`arm` profile, strict end 08017E68) for bytes and distance, and
`finish-1114-renderer/sbs.py --score` for shape and register rows. The byte
count is positional, so a candidate that is 4 bytes long or short (f1, the
hoist-order line) scores badly even when its instruction shapes are closer.

The best candidate passes the same **199 synthetic differential fixtures** as
11/14 (`check32.py`, all 1,053 original instruction addresses reached, no ROM
used); see `checks.json`.

## Three source facts established this round

Each one was confirmed by compiling and measuring, and by GCC 2.9 RTL dumps
(`-dL -dl -dg`) from the worker C `agbcc_arm`.

1. **The sb/sl swap is an allocation-order effect, and it is fixed.** ARM's
   `REG_ALLOC_ORDER` lists r10 before r9 (`… 8, 10, 9, 11`). Global allocation
   takes allocnos in priority order (`floor_log2(refs) * refs / live_length`),
   so whichever of the points base and the scratch pointer is allocated first
   gets sl. In the 11/14 source the points base wins (12,037 against 10,680,
   because loop.c hoists the scratch symbol load with a `REG_EQUIV` note and
   `update_equiv_regs` doubles its live length). The cartridge has the points
   base in sb, so its scratch pointer was allocated first. Wrapping the y and z
   midpoint stores of each part block in `do { … } while (0);` adds one loop level to
   those 32 scratch references (195 to 227 weighted refs) and no points-base
   references: 12,433 against 12,037. The scratch pointer then takes sl, the points base
   takes sb, and the `a` index shares sl as in the cartridge. The wrapper is plain C
   with no effect on behaviour; GCC 2.9 emits loop notes for it, and flow.c
   weights references by loop depth.
2. **The face-row constant is fixed.** Writing the row pointer in two
   statements, `face = gFaces; face += ring * 24;`, gives the cartridge's seven
   instructions exactly (`add r7, r3, #0x33800; add r7, r7, #0x370;
   add r7, r7, #0x2000000; ldrh r3, [r7]`). The likely mechanism (consistent with the
   output; no CSE dump was taken) is that the pointer is now set twice, so CSE
   knows it only as `ring*1344 + K` with K a constant. That address is not
   legitimate for `ldrh`, so CSE leaves the exit test on `[r7]` (in the one-statement form it
   rewrote the test to `[ring*1344 + Kreg]`, which kept the forced constant
   register alive). The constant register then has one use, and combine folds it back
   into the add.
3. **The 11/14 structural projection order belongs in the same candidate.**
   With facts 1 and 2 in place, the x, y, z delta order (screen sums before the
   depth) reproduces the cartridge's hoisted camera.z/offset.z, the z-component
   pointer induction variable and the projection loop's exact length. `v-ref.c`
   is still 4 bytes long, but those bytes are part-block reloads, and the search
   removed them.

## Search

`perm.py` is a small permuter written for this owner (the repository still has
no decomp-permuter adapter, and decomp-permuter is not installed on worker C).
Each candidate goes through the repository's own diagnostic compile and scorer.
The search applies only edits that preserve behaviour, aimed at allocation and
reload choices:

- wrap a run of sibling statements in `do { … } while (0);`, or unwrap one (a
  bare `continue`/`break` is never wrapped);
- swap or move independent assignments (an identifier and lvalue dependency check);
- swap the operands of a commutative `+` or `*`;
- reorder declarations.

Scoring is `3 × distance + bytes / 3`, with heavy penalties for a wrong length or
frame. Acceptance is annealed. Runs on worker C (8–10 worker processes, nice 5), each with a
fixed time limit, about 1 h 50 min of wall time in total and about 45,000 candidates
(`search-logs.txt` has the score logs; perm4 was a two-minute false start):

| Run | Start | Evaluated | Best (bytes / distance) |
| --- | --- | ---: | --- |
| perm1 | yz1 | ≥2.9k | 1,837 / 573 (frame 100, rejected) |
| perm2, perm3 | f1, then perm2 best + structural projection | ≥2.7k | 1,577 / 473 (length 4,292) |
| perm5, perm7 | m3 = perm2 best + structural projection, uv wrappers removed (1,070 / 444) | ≥12.9k | 905 / 380 |
| perm6 | hoist-order line | ≥4k | 1,517 / 498 |
| perm8, perm9 | perm7 best | ≥22.6k | **880 / 367** |

`clean.py` then reverted every search edit that did not change the compiled bytes
(the best keeps 36 edits relative to `v-ref.c`, which is the 11/14 source plus
the face-row fix and the structural projection). The best still carries many
`do { } while (0)` wrappers. They are honest C, but they make no claim about how the
original was written. A cleaner equivalent (for example macros with
`do/while(0)` bodies) was not searched for.

## What blocks the rest

1. **First real divergence: 08016E44, the face header.** (In the best
   candidate the search also reordered the declarations, which swaps the stack
   slots of b and c, fp-68 and fp-72, at 08016E10/08016E1C. That keeps the later
   b-first hoist lined up with the cartridge's slot use, so it is a compensating
   error, not progress. The hoist-order line has the right slots and first differs at
   08016E44, and every byte before that matches.) depth[1]'s value and the
   `&pts[c]`/`&pts[d]` pointers have their registers permuted: cartridge
   r4/lr/r12, ours r12/r4/lr. All three are global allocnos. In ours depth[1] has
   the higher priority (floor_log2(refs)·refs/live: 1.8 against 1.39 and 1.24), so it
   takes r12 first. In the cartridge both pointers must have been allocated before it.
   Tried without success: all 2,520 dependency-respecting orders of the eight
   header statements (1,207 measured before the run was stopped; the source order
   was best), `do/while(0)` weighting of the direct-path loads (adds a reload, +4
   bytes), and face-loop nesting variants.
2. **Reload registers rotate through the whole function.** reload1.c's
   `allocate_reload_reg` hands out spill registers round-robin from
   `last_spill_reg`, so one extra or missing reload anywhere shifts the reload
   registers of all later code. The part blocks fit this: the cartridge reloads the
   a*28 offset into r0 and keeps it for three statements, while ours lands two
   places later in the rotation (r2), clobbers it and reloads. Most of the
   remaining 295 register rows probably follow from the few shape differences
   upstream of them.
3. **Loop-invariant hoist order (b and c offsets).** loop.c's `move_movables`
   lowers its threshold by 3 for every moved register. In the clean
   source the b offset is "not desirable" and the c offset is moved in the first
   loop pass, so c's offsets are computed before b's, as in the cartridge.
   The best candidate's extra recomputations raise the savings from 8/6/8 to
   10/8/10, so b moves first. The hoist-order line keeps the cartridge order
   (`func_08016DA8_order.c`, 68 shape rows, the fewest of any candidate) but is 4 bytes
   long because of reload inheritance in the part blocks.
4. **Projection-loop scheduling.** sched1 places dy's multiply and the
   `g_030055F8[i].x` store differently. The loop is at the register-pressure limit:
   nine hand reorderings and a separate tz temporary all spill the points base.
5. **Smaller scheduling choices** in the near-path finish block (z sum, then the
   tex/mode stores), in the bucket insertion and in the direct path's special entry.

Because of item 2, the register rows cannot be fixed one region at a time. An
exact match needs items 1, 3 and 4 right at once. The best candidate trades item 3
(and the b/c slots) for fewer reload differences. The hoist-order line has items 1
and 4 still open.

## Receipts (`docs/near-misses/finish2-1115-renderer/`)

- `func_08016DA8.c` (best), `func_08016DA8_order.c` (hoist-order line),
  `v-ref.c` (cleaning reference), `milestones/yz1.c`, `milestones/f1.c`;
- `candidate.json` and `candidate.diff.txt.gz` (measure output for the best),
  `order.json`, `checks.json` (check32 result), `search-logs.txt` (score logs only);
- tools: `perm.py` (search), `fm.py` and `fq.py` (batch scoring; `fm.py` also prints the
  points-base/scratch priorities and hard registers), `clean.py`, `dump.sh`,
  `loopinfo.sh` (first-pass part-loop movable decisions), `offsets.py`,
  `hunks.py`, `permtest.py`.

## Reproduce (on a worker, never the laptop)

```sh
D=docs/near-misses/finish2-1115-renderer
python3 tools/measure_candidate.py $D/func_08016DA8.c 08016DA8 08017E68 arm /tmp/r
python3 docs/near-misses/finish-1114-renderer/sbs.py /tmp/r.diff.txt --score
python3 docs/near-misses/finish-1114-renderer/check32.py $D/func_08016DA8.c
python3 $D/fm.py $D/func_08016DA8.c $D/func_08016DA8_order.c
bash $D/loopinfo.sh $D/func_08016DA8.c
python3 $D/perm.py $D/func_08016DA8.c /tmp/perm 600 8 1
```

The worker copies (`~/txra-renderer`, `~/txra-renderer-perm`, `~/txra-renderer-out`)
were deleted after the receipts were copied.

matches installed: none (189 exact replacements remain)
near-misses improved: 08016DA8: 2446 -> 880 differing bytes (instruction distance 622 -> 367; length and frame still exact)
what blocks the rest: the first real divergence (08016E44) is a global-allocation priority inversion between depth[1] and the c/d point pointers, and reload1.c hands out spill registers round-robin across the whole function, so it cascades into most later register rows; the b/c loop-invariant hoist order and the projection-loop schedule are also still open, and no source form found so far gets all three right together.
