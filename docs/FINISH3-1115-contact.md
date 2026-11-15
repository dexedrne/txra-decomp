# Finish pass 3, 15 November: 080181C0 contact owner installed (label: contact)

Branch `work/finish3-contact` from main 77ab890. Every compile, measurement,
build and check ran on worker A (`agbcc_arm` sha256 `34268789…`). Nothing was built
on the laptop. No ROM bytes were copied, printed or committed.

**The contact owner 080181C0..08018854 is now exact C and installed** as
`src/generated/func_080181C0.c`, registered in `tools/rom.cfg` (offset 0x181C0,
size 1,684, compiler `arm`). It went from **158 differing bytes to 0**. Exact C goes
from 191 to 192, and `progress.json → completion` from 225 to **226 of 228**.
**2 C owners remain**: 080064A4 (sound) and 08016DA8 (renderer).

| Step (receipts in `finish3-1115-contact/progression.json`) | Bytes | Frame | Edits | Differing |
| --- | ---: | ---: | ---: | ---: |
| finish2 candidate | 1684 | 72 | 74 | 158 |
| + function-scope probe pointer `p = g_030057A0` | 1672 | 64 | 243 | 1161 |
| + raw heading before the loop, `a & 0x3FFF` inside it | 1680 | 68 | 128 | 982 |
| + mask written `a << 18 >> 18` (`u32 a`) | 1684 | 72 | 39 | 118 |
| + box tables through function-scope byte pointers, `model` scaled to a byte offset | 1684 | 72 | 0 | **0** |
| installed (unused locals removed, `model = field_02 * 8`, re-indented) | 1684 | 72 | 0 | **0** |

The installed source is plain structured C: no padding, inline assembly, fixed
registers or hand bytes. Measurement receipt: [measure.json](finish3-1115-contact/measure.json)
(exact, compiled sha256 `960f722b…`, source sha256 `af185e89…`).

## How the allocator's decisions were found

A private copy of the same `gcc_arm` sources was rebuilt with debug prints
([alloc_patch.py](finish3-1115-contact/alloc_patch.py), applied to a copy on worker A,
then `make cc1`). With no override set, its assembly was identical to the official
compiler for every source checked (the finish2 candidate, the 118-byte step and the
installed source). It prints local qty decisions (`TXDBG=L`), global `find_reg`
results (`G`) and every live-length doubling in `update_equiv_regs` (`U`). Two
what-if overrides were used for diagnosis only: `TXLEN` (set one pseudo's global
live length) and `TXSPILL` (keep a pseudo out of allocation).

### 1. The pointer giv against k: both live lengths were doubled

`update_equiv_regs` doubles a pseudo's live length when the first set it meets has
a constant REG_EQUAL note, even if a later set removes the equivalence. The 11/15
note found this for the strength-reduced probe pointer (giv). The trace shows it
also happens to the loop counter k: its first set is the reversed `k = 5`, with
REG_EQUAL 5. So the priorities in the finish2 candidate were k 5·62/142 = 2.18
(doubled from 71) and giv 4·27/108 = 1.0 (doubled from 54). Removing only the giv's
doubling gives 2.0, still behind k, which is why the earlier diagnostic failed.
`TXLEN` showed that the giv must reach live length 49 or less, undoubled, to come
first; that alone gives 118 bytes.

The giv's initial-value note comes from cse2: the rotate loop's own probe base is
hoisted into the preheader as `reg = g_030057A0`, so cse2 knows the constant. With
the probe array reached through a **function-scope pointer** (`p = g_030057A0`
before the loops, used by the probe stores and the rotate loop), the giv starts as
a copy of a register that is set outside the extended block. It gets no constant
note, is not doubled, and its init stays close to the loop: giv 4·27/45 = **2.4**
against k **2.18**. The rotate loop then takes the original's registers: giv r6,
k r7, c2 r8, c1 sl, angle*4 sb. The k/giv swap also fixes the test loop, the
collision body and the k<=3 loop.

### 2. Keeping the loop-pass budget with the pointer

The pointer removes two pass-1 movables (the probe base and probe+8), so the
threshold is 6 higher at the j index and pass 1 moves `j*4` and `j*5` (step 2,
1161 bytes). Reading the raw heading `a = field_20` before the loop and masking it
inside the loop puts movables back before the record base:
- `a & 0x3FFF` adds three (16320, +63, and). That is one too many: record+4 slips
  to pass 2, and pass 2 then cannot afford `angle*4` (982 bytes);
- `a << 18 >> 18` with `u32 a` adds two (lsl, lsr). Pass 1 again ends with
  threshold 4 at `j*4`, and pass 2 moves the j chain, `i*4`/`i*5`, zpos and
  `angle*4`, as in the original. The combined shifts are the original's
  `lsl #18; lsr #18; lsl #2`.

### 3. The j body r0/ip and the preheader reloads: the table bases

With item 1 fixed, all 118 remaining bytes came from the preheader's local
allocation. The `g_08020B04`/`g_08020B08` base loads were block-local qtys. They
took r2, so `model` went to r1 and rec+0x20 to r0, and j*100 (global, live across
the block) had to take ip. In the original both bases are reloads into r4 and lr,
which only a spilled pseudo produces: a local qty there could not get r4 while r0
is free. `TXSPILL` of the two bases gave 47 bytes, which confirmed this.

The plain-C spelling that spills them is **function-scope byte pointers to the two
tables, with the model index scaled to a byte offset once**:

    model = g_03001E60[j].field_02 * 8;
    width = *(s32 *)(wt + model);
    height = *(s32 *)(ht + model);

The pointers are function-wide constants: long-lived, not allocated, and
rematerialized by reload. That frees r2 for `model`, r1 for rec+0x20 and r0 for
j*100. It also gives reload the original's round-robin order (B04 into r4, B08
into lr, sin base into r0), so the remaining preheader and rotate-loop reload rows
match. The byte offset matters. `s32 *` pointers with `wt[model * 2]` fold the scale
into each load (`ldr r4, [r4, r2, lsl #2]`, 3 bytes off), and writing
`wt + model * 8` in each load changes the code as well (1,680 bytes). A pre-scaled
offset used by both loads stays one `lsl r2, r2, #3`.

Behaviour is unchanged: `p`, `wt` and `ht` point at the same objects as the old
array expressions, `a << 18 >> 18` on a `u32` equals `a & 0x3FFF`, and
`*(s32 *)(wt + model*8)` is `g_08020B04[model * 2]`.

## Admission and validation (all on worker A)

- `tools/measure_candidate.py src/generated/func_080181C0.c 080181C0 08018854 arm`:
  `"exact": true`, `"different_bytes": 0`, `"instruction_distance": 0`,
  `"emitted_bytes": 1684`, `"local_frame_bytes": 72`.
- `make clean; make -j8`: rc 0, 192 `C match` lines including
  `func_080181C0: C match (1684 bytes)`, `build/txra.gba: OK`, SHA-1
  `4197339d4add74bb40ed02a8fba5e58096afb487`.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`.
- `make recomp`: `Emitted 228 functions, 258 load/run entries`.
- `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`: `Accuracy: 4300 framebuffer hashes, every PCM byte, final state and sample clock passed` (`fallback=0 unknown=0 unsupported=0`).
- `tools/map_completeness.py`, then `tools/asm_interfaces.py --completeness`
  (`"failures": []`, C-candidate 2), then `tools/progress.py` (completion 226 of
  228; `functions_matched_c` 192 functions, 85,426 bytes with pools).

## Files

- `src/generated/func_080181C0.c` (new) and its `tools/rom.cfg` match entry.
- `tools/asm_interfaces.py`: the 080181C0 C-candidate row and its `OWNER_END`
  entry are gone.
- Regenerated on worker A and copied back (metadata only): `asm/program.s` (the owner
  is now an `.incbin` of the verified leaf), `docs/map/finish.json`, `progress.json`.
- README and `docs/FINISH.md` counts: 192 exact C, 226 of 228. In instruction bytes,
  exact owners hold 71,804 of 85,578 (83.9%), and the two remaining owners 7,682
  (9.0%).
- Diagnostic tools (no admission authority): `tools/contact_try1115c.py` (parallel
  scoring, optional private compiler and sanitized diff rows),
  `tools/contact_alloc1115c.py` (allocation order with priorities),
  `tools/contact_passes1115c.py` (rotate-loop movables for both passes),
  `tools/contact_rtlgrep1115c.py` and `tools/contact_rtlrange1115c.py` (RTL dump
  filters for our own C).

## Notes for the renderer and sound owners

- Check whether a priority loser is losing because of a **doubled live length**
  (`TXDBG=U`). Both bivs and givs with a constant first set are doubled.
- A constant base that the original reloads into a high register (r4/lr) is a
  spilled function-wide pseudo, not a local qty. A function-scope pointer with a
  pre-scaled byte offset reproduces it without changing the address form.

The worker copies (`~/txra-contact3`, the admission logs and both private compiler
copies) were removed. No process was left running. Work stayed on
`work/finish3-contact`, with no push or merge.

matches installed: 080181C0 (owner 080181C0..08018854, 1,684 bytes, ARM profile; full-ROM SHA-1 4197339d…afb487)
near-misses improved: 080181C0: 158 -> 0 (installed exact; 118 intermediate after the probe-pointer step)
what blocks the rest: nothing for 080181C0. The two remaining owners, 08016DA8 (renderer, 880) and 080064A4 (sound, 1,598), are register-allocation gaps outside this lane.
