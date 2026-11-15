# Matching pass, 10 November

**No replacement was installed.** The HUD improves by 67 differing bytes;
the renderer has a clearer source shape but exactly the same compiler output
as its previous candidate. Both remain substantial complete-owner nonmatches.
The exact registry stays at **181 functions, 72,524 bytes including pools,
85.19% of 85,132 mapped code bytes, and 229 mapped functions**. Registry,
README and `progress.json` agree.

Work stayed on `work/match-1109`, starting at 9e61059. Main was not changed.
There was no reset, rebase, stash, push, merge, deployment or extra session.

| Owner | Differing bytes before -> after | Instruction edits before -> after | Output / original | Local frame / original |
| --- | ---: | ---: | ---: | ---: |
| 0800421C | 3,235 -> 3,168 | 1,013 -> 989 | 4,124 / 4,124 bytes | 36 / 36 bytes |
| 08016DA8 | 3,251 -> 3,251 | 898 -> 898 | 4,268 / 4,288 bytes | 108 / 96 bytes |

The brief's HUD baseline was superseded by the retained 11/9d source. The ARM
baseline available on this branch is 3,251; no retained 3,249-byte source/profile
was found. The comparison helpers reproduced the checked-in baselines before
the new work, rather than substituting the brief's numbers.

## What changed

HUD commit **9ed77d5**, `Recover HUD selection order and record comparisons`,
retains two ordinary branch-order changes: the model sprite selection takes
the low-ID path first, and the gear icon takes nonnegative speed first. Those
forms follow the decompiler view and improve the complete owner by 67 differing
bytes and 24 instruction edits. Helper arguments, call order, scratch aliases,
complete owner end and compiler profile remain unchanged. See the
[HUD source, shape comparison and exact next step](near-misses/hud-owner-1110/README.md).

The renderer pass is the commit containing this note, titled
`Record renderer control flow and admission results`. Its near path now nests
the three positive predicates shown by the view: nonnegative depth, visible
corner and nonpositive winding. The source passes the independent fixtures and
reproduces the starting compiled hash. This is explicitly a **tie**, not a
byte-distance improvement. See the
[renderer source, shape limitation and next step](near-misses/arm-16da8-1110/README.md).

The HUD trials measured 661 source identities and 252 compiled outputs, covering
temporary sharing, mixed flash/smoke traversal, nested exits, projected point
and coordinate lifetimes, source-base joins and gauge scopes. Four scope
hypotheses were compiler rejections and 316 outputs exceeded the strict owner
boundary; none was admitted. The renderer trials measured 317 sources and 131
outputs across mixed projection traversal, texture ladders/tails, bucket links,
next-part/next-face captures and signed loop/depth roles; 167 outputs exceeded
the boundary. The manifests distinguish diagnostics from retained candidates.
No compiler-family sweep, padding, handwritten bytes, inline assembly, fixed
register or volatile spill was introduced. Only the retained sources receive
semantic approval; all final comparisons use the unmodified complete-owner
checker. No boundary was enlarged.

Each target has its own full retained C, sanitized best diff, pinned compiler
profile, fixture receipt, structural comparison, compressed baseline diff,
compressed measured-trial manifest and authored recipes. The structural counts
separate original-address windows from instruction-shape alignment; they are
layout aids, not additive causal byte counts or a proof of semantics.

## Decompiler setup and findings

The required official JDK 21 download was installed and verified. The current
Ghidra release was installed locally and its archive checksum verified against
the release's published SHA-256. Ghidra 12.2 itself requires Java 25, so a second
official Temurin runtime was installed locally for headless launches. No sudo
or client configuration change was used.

REA 6.7.0 doctor and its bundled skill/docs/source were read. Its raw-image
provider supports a base address, but makes a separate immutable copy of the
input. The task prohibits that ROM copy, so **direct `analyzeHeadless`** read the
ignored symlink instead. REA's native provider was not used. Exact versions,
checksums, memory flags, seed checks and a metadata-only project audit are in
the [headless analysis record](near-misses/DECOMPILER1110.md) and its linked
receipts.

The ROM identity was checked privately. The raw image maps file offset zero at
08000000 with `ARM:LE:32:v4t`; 229 registry entries and their instruction spans
were seeded with explicit ARM/Thumb context, and all 13 configuration seeds
were checked. Pools are excluded from decompiler bodies; compiler comparison
still includes them. Cartridge data is non-executable and read-only, RAM is
uninitialized/writable and hardware is volatile. The independent raw-loader
image-base property remains zero; the memory mapping and owner addresses are
correct, and no rebasing was performed. The project and all exported views
remain owner-only under `~/.cache/txra-ghidra/`. A home-directory symlink works
around Ghidra's rejection of dot-prefixed project path components. All final
temporary/cache paths are under that home cache; the three files created by
the initial default temporary cache were individually audited and removed.

The view changed the useful questions: the HUD has no missing switch table,
and 080051FE is its common restored-stack return rather than a normal callee.
The corrected analysis joins that epilogue without altering ROM bytes. Counted
loops, independent mode tests, record strides and helper sequence largely agree
with the retained C. The changed selection order produces the measurable gain.
The view's mixed pointer/index traversals and scalar lifetimes did not yield a
further admitted improvement.

For ARM, control flow and layouts are useful, but the printed high-level view
loses the join between four corner-depth stores and their later indexed stack
load. The stores are present in the repository assembly and initial p-code.
APCS, explicit array naming, disabled array splitting/alias blocking and corrected
memory permissions did not resolve that high-level stack alias. This is a
decompiler limitation, not an uninitialized cartridge variable. No exported C
was pasted into the repo, and no missing assignments were copied into a source
candidate. The renderer's next step starts by repairing/annotating that join
before another allocation rewrite.

## Validation

One forced whole-ROM rebuild recompiled and byte-verified **all 181 installed
replacements** and passed the pinned full-ROM SHA-1 gate. The registry is
byte-identical to the starting commit. Final admission ran **223 tests:
222 passed, one skipped, zero failures**. The existing skip reports fewer than
two unmatched retained drafts for its resumable-search fixture. The retained
sources were frozen before admission. `tools/progress.py` ran afterward and
preserved the exact-match counts. No native execution milestone is claimed for
this checkout. The [admission receipt](near-misses/admission-1110.json) pins
registry, build, source and log hashes.

The HUD passes **1,024 state and ordered-call fixtures**, strict warnings,
undefined-behavior sanitization and six transform aliases. Its reference is
prior semantic C, not independently executed original instructions. The ARM
source passes **199 independent memory fixtures**, 20 fixed expected checks,
three size checks and 14 field-offset checks, reaching all **1,053** original
instruction addresses in the synthetic textual executor. These fixtures do not
establish arbitrary malformed-state behavior, real-game execution, performance
or original byte equality. All fixture/profile source hashes agree.

## Review and remaining work

Finished review folder: `txra-review/match-1110-rea/`.

Key pictures are `before-0800421C.png` / `after-0800421C.png`, at the changed
model selection, and `before-08016DA8.png` / `after-08016DA8.png`, at the same
near-path code view. The ARM captions explicitly say its generated code is
unchanged. `arm-source-flow.png` shows what changed in our renderer source.
All five native pictures were opened and inspected, along with the decoded
clip overview and its smaller final retake. There is no cropped text, blank
scene or exported decompiler text in these pictures.

`0800421C.webm` and `08016DA8.webm` are each **four seconds, muted, 30 fps,
1600x1000 and video-only**, at **451,840 and 404,398 bytes**. Both are below
4 MB. Frames at 0.25 through 3.75 seconds, every half second, were inspected
in `clip-overview.png` (1000x660). These are compiler-comparison clips, not new
gameplay footage. No browser, server or browser profile was needed or left
running; no vehicle, world or road change was installed. The folder includes
five plain sentences in `NOTES.md` and captions for every picture and clip.
[review-1110.json](near-misses/review-1110.json) pins all eight media hashes,
sizes and dimensions. Source and build hashes are in their respective profiles
and admission receipt. These are the finished artifact references for archival;
no archive was moved.

Media and receipts together remain below 2 MiB. Only the best full sanitized
diffs exceed 500 plain-text lines; other long receipts are gzip files. No ROM
slice, raw encoding column, pool content, extracted binary, project database or
decompiler export is committed. Local ignored build/search scratch, the local
software installations and the private analysis project remain available for
continuation. Disk remained about 184 GiB free, above the 20 GiB reserve.

Still unresolved: HUD allocation and pool shifts, especially the gauge digit
join and projected effects; ARM's 12-byte frame excess, 20-byte output deficit
and corner-depth decompiler join. Neither owner is ready for installation.
Concrete next steps and completed negative neighborhoods are in each target
README. `OWNER-NOTES.md` was absent at the initial, per-target, capture,
validation and final reads; there are no appended owner notes to list or leave
unaddressed. Marker: `MATCH1110-REA-DONE`.

matches installed: none
near-misses improved: 0800421C: 3,235 -> 3,168; 08016DA8: 3,251 -> 3,251 (unchanged)
decompiler view: clarified HUD branch order and the common return, but did not resolve the ARM frame mismatch.
