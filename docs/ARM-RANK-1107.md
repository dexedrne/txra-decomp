# ARM search admission

Baseline: c2ea36c4192f94e5cefd0a1ff18a103e80f0c02f. The ranker rejected every ARM entry as lacking a compiler path, although both ARM profiles already worked. It now admits a narrow class of compiler-generated APCS leaf frames to bounded searches. The Thumb validator and exact compilation, relocation, complete-extent, next-entry and full-ROM installation checks remain unchanged.

Admission requires a contiguous unconditional prologue, preserved stack origin, no prologue re-entry, register and condition-flag definitions through control-flow joins, protected direct saved-frame stores, and execution of the matching restore before return. Unsupported startup, IRQ, custom-register, calling, indirect-transfer and processor/user-bank contracts stay blocked. The supported instruction subset excludes later-architecture instructions such as CLZ and includes the ARMv4 LDMDA array load used by the larger candidate. This is an advisory candidate filter, not a general memory-safety or ABI proof.

Fresh current-source ranking retains 181 exact C matches and 48 unmatched entries. Only 080181C0 (1,684 bytes) and 08016DA8 (4,288 bytes) pass the new admission check. Missing dynamic counts remain unknown; static counts are not presented as runtime frequency.

Final verification runs all 23 new synthetic fixtures, including failure-first cases for skipped allocation, overwritten stack origin, bypassed restore, saved-register stores, conditional definitions and processor-state variants. The full Python suite runs 212 tests: 211 pass and one existing real-resume fixture skips because fewer than two retained unmatched drafts remain. All 181 registered replacements compile exactly, and the complete 4,194,304-byte matching ROM retains SHA-1 `4197339d4add74bb40ed02a8fba5e58096afb487`. Generated assembly and maps remain unchanged.

The bounded 080181C0 source probe now reaches both ARM compiler profiles: two trials, zero compile errors, no exact match. Its retained best remains 1,644 of 1,684 bytes, with 206 instruction edits and 1,146 byte differences. This adds no C match, mapping, runtime, audio, frame-rate or device-acceptance result. Numeric evidence is in ARM-RANK-1107.json.

Verification uses a temporary source archive on the existing private-ROM host. Its sources, objects, ROM symlink and rebuilt matching ROM are removed afterward; the original private ROM stays unchanged. No ROM transfer, additional remote checkout or model request is involved.
