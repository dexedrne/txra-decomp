Round four audited the requested pointer/call evidence but established no additional function or executable byte. Function recovery remains incomplete; the count is deliberately not inflated by internal switch labels or coincidental pointers in data.

Implementation commit: `2dd9674` — candidate audit, rejection journal, coverage probes, metadata partition and review renderer. This note and `MAP4-DONE` are recorded in the following handoff commit. No push, merge, deployment or stash was performed.

- Functions: **229 → 229** (205 THUMB, 24 ARM); all 229 emitted and compiled.
- Code bytes: **85,132 → 85,132**; the complete code classification and function inventory are unchanged.
- Unknown bytes: **723,196 → 721,992**, down 1,204.
- Data including fill: **3,385,976 → 3,387,180**. Only 948 unknown bytes became exact read data and 256 became graphics-transfer data; no previously mapped byte reverted to unknown.
- All 20 `progress.json` keys remain. Execution milestones now refer to the tested executable.

The audit checks 2,093,759 source bytes in the round-three table/data/unknown partition at every byte alignment, including packed slots crossing classification boundaries. It follows 2,031 odd ROM-pointer references, 1,078 direct ARM/THUMB calls and 200 resolved indirect references. The resulting 927 distinct targets are 193 existing function entries, 167 internal bounded-switch targets and 567 rejected or unproven candidates. There are zero additional validated proposals. `docs/map/code-audit.json` retains every target's references, classification and reason, plus a digest identifying the baseline partition.

The new validator follows conditional paths, allows stores and checks ARMv4T support, reachable decoding, instruction boundaries, literal conflicts, stack balance and the saved return address. Rejections include undecodable paths, instruction-mode conflicts, unsupported instructions, invalid returns and unresolved transfers. All 101 budget-limited targets are inside the independently proved reciprocal lookup table. A rejected candidate is not proof that its unknown neighboring bytes are data. New ARM call targets would need a separate validator; none appeared in this scan.

Validation completed:

- **90 unit tests passed**, including **33 candidate-audit tests** with synthetic instructions, packed pointers, call/BX resolution, alias ambiguity, stack-return corruption, decoder bounds, random data and command/fingerprint checks.
- **118 runtime assertions** and the controller suite passed.
- Matching C replacements and the full rebuilt ROM passed byte identity and SHA-1 verification.
- **13 normal-input coverage sessions** passed with zero fallback steps, unknown execution targets or unsupported instructions; no executed PC falls outside the static instruction spans after unique copied-code alias translation.
- The full race ran **12,500 frames / 1,170,372,096 native instructions**. Every recorded final machine/audio field matches the preceding race summary except elapsed host time. Current 12,500 frame hashes were recorded privately; prior raw hashes were unavailable, so a new frame-by-frame comparison against them is not claimed.
- Isolated save/reload checks passed, including unchanged EEPROM hash on reload. No gameplay, save format or runtime source was changed.

Two new probes select another results choice and a third pause choice through ordinary keypad input. The pause probe adds **35 executed PCs and 13,412 read bytes** over the eleven reproduced prior routes; those PCs were already statically mapped. The results probe adds neither new PCs nor read bytes. Neither probe executes replay entries `08012CC8` or `08012EB8`. Sixty-three mapped function entries and eleven unresolved register-call veneer sites remain unexecuted. Advanced career progression, unlocked courses and replay still need broader coverage; unreferenced code and unresolved transfers are not ruled out.

Review artifacts are in `txra-review/map4/`:

- `before/rom-heat-strip.png` and `after/rom-heat-strip.png`: identical viewpoints; use printed counts because the data gain is tiny at full-ROM scale.
- `functions-found.png`: unchanged function counts and current race/coverage totals.
- `candidate-audit.png`: actual candidate dispositions, including zero additional functions.
- `audit-status.webm`: six seconds, 30 fps, muted VP9, **572,097 bytes**; no audio stream.

All four pictures and representative before/after clip frames were visually inspected. The earlier clipped subtitle and a mixed-label transition were corrected. Every review folder has plain owner notes and a caption for every picture/clip. The review contains only our metadata tool output. ROM bytes, decoded assets, game images, generated recompiler source and raw execution captures are not committed or included in the review.

The private ROM was absent initially and became available locally during the job; that blocker was resolved. This worker also needed SDL headers and local ARM build tools. Verification used the system ARM assembler/linker and the repository's pinned legacy C compiler, with local overrides:

```sh
PYTHONPATH="$PWD/build/audit-deps" make recomp check check-runtime check-controller \
  TOOL_ROOT="$PWD/build/toolroot" ARM_BIN=arm-none-eabi- PYTHON=python3
```

`docs/MAP.md` gives the audit/capture reproduction commands and current partition totals. `docs/map/round4-audit.json` records the session deltas, remaining unexecuted entries, unchanged code classification, final-race comparison and classification transitions. Local compiler wrappers, dependencies, saves and captures stay ignored under `build/`.

Owner-note check: `OWNER-NOTES.md` was absent at the final read; no appended owner notes were present to address. Review notes/captions and the short muted clip requested in the brief are present. No vehicle, map or model work was performed.

Next work should target normal-input advanced-career/replay reachability and unresolved indirect values, followed by semantic bounds for the remaining 721,992 unknown bytes. Finding more functions still requires new executable evidence, not relabeling known data.
