# 080064A4 sound owner, 15 November round (label: sound)

Uninstalled near-miss for the complete owner 080064A4..08007398 (pool included).
It is not byte-exact and is not counted as a match.

| | 11/11 retained (`sound-owner-1111`) | this round |
| --- | ---: | ---: |
| Differing bytes | 3,227 | **1,598** |
| Instruction edit distance | 1,472 | **283** |
| Emitted / target bytes | 3,808 / 3,828 | 3,820 / 3,828 |
| Local frame / target | 100 / 108 | 100 / 108 |
| Original instructions identical in a text alignment (of 1,725) | 543 | **1,546** |
| Register-only rows / shape rows | 801 / 583 | 170 / 16 |

The first four rows come from the unchanged `tools/measure_candidate.py` (`old` profile,
`-O2 -mthumb-interwork`, strict end 08007398, `checker_rejection: null`). The alignment rows come
from `batch.py`, which aligns opcode shapes first and registers second.

## Files

- `func_080064A4.c`: the source (sha256 `4765bf75…`, compiled sha256 `9320af76…`).
- `candidate.json`, `candidate.diff.txt`: measurement and full sanitized instruction diff. Pool
  words are shown as `<literal pool>`; the diff has no encodings and no ROM bytes.
- `checks.json`: alignment summary per region and the differential runs.
- `batch.py`: parallel measurement plus alignment. It rebuilds the original listing in memory from
  `recomp/draft.py` on the worker and never writes or prints it.
- `wsearch.py`, `search-template.tpl`, `search-choice.json`: the choice-point search. Every
  `«name@option0@option1…»` marker in the template is an alternative source form; markers with the
  same name move together. The final source is the template at `search-choice.json` plus two hand
  edits found afterwards (the mix-buffer index blocks at the top) and whitespace cleanup. Each edit
  was re-measured. The cleanup leaves the compiled sha256 unchanged.
- `diff32.py`, `harness32.c`: differential behaviour check (below).

Reproduce on a worker: `python3 tools/measure_candidate.py docs/near-misses/finish2-1115-sound/func_080064A4.c 080064A4 08007398 old build/x`
and `python3 docs/near-misses/finish2-1115-sound/batch.py <file.c>`.

## How the source was built

The 11/11 source was produced by automated search and carries field-pointer variables and macros
the original does not have. This round started over from the assembly in `asm/program.s`, in the
original statement order. The source alternatives were then searched on worker B. Facts each confirmed
by compile and measure:

- **Loops.** The voice body is a real `do { … } while (marker == 0x65)` loop. The `restart:` label
  sits just before it. 08006740..08006774 is that loop's preheader: loop.c hoists `9*i`, `72*i` and
  the field addresses there, and the 0x65 restart branches to the label in front of it.
- **The fade flag store.** `command` is a function-level variable initialised to 0. The fade code
  stores it (`gFadeActive = command`), which is the `r7 = 0` at 080064B0 and its store at 080064F8.
- **Block-scoped locals.** The original allocation follows a style where temporaries are declared
  in the innermost block. Each of these moved many rows to exact:
  - the tone-start envelope pointer;
  - the sound-effect loop's pointer, flag and register values;
  - the noise-channel tick pointer;
  - the slide temporary `{ s32 p = pitch; p += seq[c]; pitch = p; }`;
  - the arpeggio write temporary `{ u16 t = flags << 8; REG = t | pitch; }`;
  - `{ s32 *durations = gDurations; … }` around the note fields.

  The last one also reproduces the early duration-table load. It stops loop.c from hoisting
  `&voice[i].cursor`, which had added a stack slot and shifted every sp offset after it.
- **Expression idioms.** `val = inst->control; val |= seq[c] << 8;` gives the `ldrh` of the control
  word. `val = pitch; val |= flags << 8;` gives the `(pitch << 16 | flags << 24) >> 16` form. In the
  noise slide, `{ s32 t = seq[c]; val = (flags << 8) | t; }` gives the second `ldrh`. The tick
  arpeggio index is written inline. The slide envelope has its own pointer variable; arpeggio and
  volume share one.

## What still differs

- **Length and frame (8 bytes).** The original keeps the 0x67 master-volume temporary in memory
  (sp+96, stored and reloaded) and leaves an unused slot at sp+100. The command index goes to sp+104.
  This source keeps that temporary in r1; its command index is at sp+96 and its frame is 100 bytes.
  Every byte after 08006DC4 is therefore 6 bytes out of place. This shift accounts for most of the
  positional differing-byte count.

  Tried without effect:
  - a block-local temporary;
  - signed type;
  - operand orders;
  - a combined assignment.

  Taking its address breaks the rest of the function.
- **Envelope tick slide sections.** The slide pointer, `72*i` and the cursor address use a rotated
  register set (r5/r2/r3 against r2/r1/r5). This leaves about 105 register-only rows in
  08006776..08006D62. Sharing one pointer variable fixes the slide but breaks the arpeggio and volume
  sections.
- **Smaller differences.**
  - The mix-buffer clear hoists its zero constant after `i = 175`; the original hoists it before.
    Same length.
  - Effect-loop register roles: event pointer r3, flag r4 and value r2, against r4, r3 and r4 in
    the original.
  - The operand order of `gFadeLevel * 17`.

## Behaviour check

`diff32.py` compiles two sources unchanged for i386, so pointers are 32-bit. It links each one
freestanding with `harness32.c` and every `g_XXXXXXXX` symbol at its GBA address, then runs both
on the same seeded synthetic states:

- voices with command and event streams and repeats;
- instruments with envelopes, including jump and hold markers;
- sound effects, fade, tempo and the mix buffer.

It compares every mapped region and the ordered hook-call log. No ROM bytes are used. The reference
is the 11/11 source, which passed the seven fixture groups (`sound-owner-1109/check_source.py`).

- After one correction to that reference (`--fix-pcm-step`), 1000/1000 states with seed 1115 and
  1000/1000 with seed 2026 are byte-identical.
- Without the correction, 130/300 are identical. The rest differ in the rest-sample step field.

The correction is needed because the 11/11 source stores the sample step to voice offset 0x40. The
original stores it at 0x30: 08007314 does `str r0,[r4]` with r4 = sp+76 = 0x030077A0 + 72*i,
written at 0800676A. The new source follows the original. This is a C-to-C regression check on
synthetic states. It does not execute the original instructions and does not test gameplay.
