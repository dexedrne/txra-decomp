# Two complete ARM branch veneers and retained ROM metadata

Baseline: `678a801c46732f4569c697f35989ccbeaaa77104`. The confirmed matching registry increases from 179 to 181 entries. Each addition is one complete four-byte ARM branch: `08000000` forwards to ARM startup `080000C0`; `08018E80` forwards its two signed arguments/result to ARM division `08000218`. The startup and division bodies remain unconverted. These ordinary C wrappers use the existing `modern-arm` compiler profile, with no inline assembly or output patching.

Both wrappers match their entire declared extent, including relocation, before the next mapped entry. The legacy ARM profile emits 24 bytes for the startup wrapper and is not accepted; the division wrapper is correctly rejected for crossing its four-byte boundary. Exact modern outputs have zero instruction and byte differences.

Full verification on the existing private-ROM compiler host:

- All 181 registered replacements compile and compare exactly. The complete 4,194,304-byte rebuilt ROM retains SHA-1 `4197339d4add74bb40ed02a8fba5e58096afb487`.
- Python suite: 189 run, 188 pass, one existing skip because fewer than two unmatched retained drafts remain for the real search-resume fixture. Compiler/ROM checks otherwise run.
- Generated assembly changes only the two branch sites to include their verified compiled bytes. Current mapping files remain byte-for-byte unchanged after regeneration.

The build exposed previously dropped config metadata. The existing reviewed call at `080065CC` would revert to unresolved on regeneration. Its existing `known_indirect_calls` config record is restored; the private ROM word at `08332EA0` is independently checked as `030068A1`, and the preceding Thumb load/call sequence is recorded in the numeric proof.

The missing ROM partition also caused the progress generator to report zero mapped code. The partition, dynamic seeds, observed-source list and format evidence are restored exactly from ancestor `2dd9674e79e3ce1fc13c2b92a1c52d09c558d5cf`, which produced the current coverage report. That report's complete blob matches the current report. All base addresses, sizes, seeds, regions and copied-code rules agree. The restored 17,672 spans partition all four MiB and exactly reproduce the current classification totals. Current 181 matches are retained. No new runtime coverage is claimed.

Two new regressions require a contiguous partition matching the reviewed coverage totals and a regeneratable config entry for the reviewed veneer call. The partition test fails with the dropped metadata and passes after restoration. Progress changes only the C counters: 72,516 to 72,524 bytes including pools, 179 to 181 entries, and 85.181% to 85.190% of the existing mapped-code denominator. Local native-build/milestone counters retain their existing unverified state.

Only a temporary source archive was built on the compiler host. The existing private ROM was linked there during verification; the link, compiled objects and rebuilt matching ROM were removed with the owned temporary stage. No ROM was transferred or committed, no additional Git checkout or native/audio/browser/model job was created on that host, and the original ROM remains unchanged. Numeric proof and exact source hashes are in `ARM-VENEERS-1107.json`; raw logs remain with the coordinator. This adds no native frame-rate, boot, audio or controller acceptance.
