# Recovery pass, 12 November

No exact replacement was installed. All **189 existing replacements** pass a forced full rebuild and the cartridge hash gate. The public registry remains **237 entries**, with **73,162 matched bytes including pools**, **85.492% of 85,578 mapped code bytes**. Registry, progress and current README totals agree.

| Owner | Differing bytes before → after | Output / original bytes | Frame / original bytes | Instruction edits before → after |
| --- | ---: | ---: | ---: | ---: |
| 0800421C HUD | 3,152 → 3,144 | 4,124 / 4,124 | 36 / 36 | 1,022 → 1,023 |
| 080181C0 contact rotation | 1,011 → 1,009 | 1,660 / 1,684 | 64 / 72 | 307 → 305 |
| 08002854 complete stream | 6,312 → 6,106 | 6,120 / 6,456 | 156 / 268 | 2,747 → 2,661 |
| 08016DA8 renderer | 3,251 → 3,250 | 4,268 / 4,288 | 108 / 96 | 898 → 897 |

The stream's “before” is the first complete validated draft made **this round**, not a previously retained complete owner. It now includes the internal 08003786 continuation, directional wrapped window, banks, three road strips, both wall seams, bridge panels and two scenery columns. Its first instruction check caught a swapped seam, which was fixed before freezing the baseline. Repeated field/table lookup expressions and point addressing then improve the complete comparison. Later descriptor order, scenery reload and per-case point-base combinations plateau. The HUD recovers map coefficient lifetimes and its original frame; its instruction distance worsens by one despite the byte gain. Contact caches the outer pair code, and the renderer scopes indices to each face.

Each retained candidate is pure structured C, complete through its established owner/pool end, checked with the historical profile and still a nonmatch. No padding, hand-written bytes, inline assembly, fixed registers, checker-boundary extension or compiler-family sweep is used. Full sanitized best diffs, sources, compiler profiles, structural summaries and exact next steps are in [the target folder](near-misses/decomp-1112c/SHAPE.md), with [HUD](near-misses/decomp-1112c/HUD.md), [contact](near-misses/decomp-1112c/CONTACT.md), [stream](near-misses/decomp-1112c/STREAM.md) and [renderer](near-misses/decomp-1112c/ARM.md) details.

Target-pass commits: **ad68a15** (HUD), **039e971** (contact), **3594659** (complete stream), **5761d93** (renderer). The final receipt commit adds the bounded follow-up journals, review tool, this note and marker. Work stays on **work/match-1112c** from **2e743c2**. No main changes, reset, rebase, stash, push, merge, deployment or extra session occurred.

The JDK and analysis installation described in the brief were absent on this host, as was `docs/MATCH1112B-SHIP.md`. Official Temurin JDK 21 was downloaded and verified. The current [Ghidra 12.2 release](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.2_build) archive matches its published SHA-256; its Java 25 minimum requires a second official Temurin runtime for headless launches. REA 6.7.0 doctor and its packaged skill/docs/source were read without changing client configuration. Its native provider snapshots the entire input, so direct `analyzeHeadless` reads the ignored ROM symlink instead. Private identity is verified. No standalone ROM copy or exported decompilation is committed.

The private project and views remain under `~/.cache/txra-ghidra/`; the locator alias is `~/txra-ghidra-project`. Import uses ARM:LE:32:v4t/APCS at 08000000, all 237 registry entries and their exact code spans/modes, writable uninitialized RAM and volatile hardware. HUD return and streaming continuation joins are private analysis overrides. The final database has 239 functions, not a public mapping increase. The ARM high-level view still loses a stack-array join; existing assembly and initial p-code independently establish its depth stores. That limitation is recorded rather than copied as false uninitialized C. Setup identities, private-view hashes and compressed authored headless recipes are retained.

Validation:

- Admission: **258 tests, 257 passed, one existing skip, zero failures**. All 189 installed C records are freshly compiled and the complete rebuilt cartridge SHA-1 agrees.
- Native rebuild: **237 compiled functions / 268 load-run entries**, **446 runtime assertions**, and **15 mapping tests** pass. `tools/progress.py` ran afterward. Gameplay milestones for this executable remain unset.
- HUD: unchanged **1,024** C state/call fixtures with undefined-behavior checks and six scratch aliases; additionally **192** original-instruction states and **9,194** original-helper calls agree.
- Contact: unchanged **768** prior-C cases, including 672 state changes and 428 detected narrowing-control differences; additionally **192** original-instruction states agree, including return and preserved registers.
- Stream: **480** original-instruction states and **11,998** ordered original-helper calls agree, comparing all EWRAM and IWRAM outside the stack. Both directions, wrapped positions, all scenery values and mixed columns are covered. Arch fixtures preserve their bridge/bank dependency.
- Renderer: unchanged **199** independent textual ARM memory fixtures, 20 fixed checks, three size checks and 14 offset checks pass; all **1,053** original instruction addresses are reached.

The new original-instruction runners execute in memory, write no ROM slices or emulator snapshots, and confer no installation authority. A swapped stream seam and unsigned narrowed coefficient are both rejected by those runners. These are bounded synthetic-state checks, not arbitrary-state or gameplay proof. Compiler/search counts and hashes are in `search-totals.json`; source, registry, build and log identities are in `admission.json`. The 37 unmatched registry entries under 1 KB are interfaces, enclosing-owner fragments or already covered entries; no new independent candidate is justified. That is a bounded registry review, not an exhaustive claim about unknown bytes.

Review folder: `txra-review/decomp-1112c/`. Start with `before-status.png` / `after-status.png`, then the same-view HUD and stream before/after pairs. `status.webm`, `0800421C.webm` and `08002854.webm` are each **four seconds, muted, 30 fps, 1280×800**, below 4 MB. Native figures are 1600×1000. All seven final pictures, all 24 decoded clip samples and native decoded after frames were opened and inspected. Notes and captions cover every published picture and clip. This is compiler evidence; no gameplay video is claimed. Media hashes are in `review.json`. No browser, server or browser profile was created.

Still unfinished: all four owners lack exact bytes. The stream is 336 bytes short with a frame 112 bytes smaller; contact is 24 bytes short with eight missing frame bytes; the renderer is 20 bytes short with twelve excess frame bytes. HUD allocation and pool layout remain different. The optimized ARM stack alias is annotated but not repaired in the decompiler. No new exact match, full-game behavior or performance milestone is claimed.

`OWNER-NOTES.md` was absent at every major step and the final read, so there are no appended notes left unaddressed. Final review/retained-receipt sizes are recorded in `artifact-totals.json`; long diagnostic receipts are compressed, and only each best full diff stays plain. The home filesystem retains about 291 GiB free. No archive was moved.

matches installed: none (189 exact replacements remain)
near-misses improved: 0800421C: 3152 -> 3144; 080181C0: 1011 -> 1009; 08002854: 6312 -> 6106; 08016DA8: 3251 -> 3250
decompiler view changed the picture: yes; complete streaming control flow is now recovered and checked.
