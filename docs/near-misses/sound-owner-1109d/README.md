# 080064A4: tone field views and envelope cursor lifetimes

Complete structured-C **nonmatches**, uninstalled and uncounted. The historical
`old -O2 -mthumb-interwork` profile and complete owner/pool boundary
080064A4..08007398 are unchanged.

| Source | Output bytes | Local frame | Instruction edits | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Retained round-3 primary | 3,692 | 100 | 1,415 | 3,353 |
| `func_080064A4.c` | 3,808 | 100 | 1,472 | 3,227 |
| Round-3 preparation control | 3,692 | 100 | 1,338 | 3,542 |
| `frame-control.c` | 3,792 | 108 | 1,328 | 3,335 |
| `instruction-control.c` | 3,776 | 104 | 1,308 | 3,405 |
| Original owner | 3,828 | 108 | — | 0 |

The primary improves by **126 differing bytes**, while instruction distance
regresses by 57. Its output deficit shrinks from 136 to 20 bytes; the eight-byte
frame deficit remains. These are explicit tradeoffs, not an exact match.
The frame control improves both distances over the prior byte primary and has
the original frame. The instruction control improves the prior control by 30
instruction edits and 137 differing bytes, with a four-byte frame deficit.
Matching a frame or length does not establish recovered original allocation.

The recorded first-tone pitch/volume step was attempted first from the six-field
preparation control. Separate cursor and sequence-pair addresses and a 16-bit
hardware result alone did not beat that control's instruction score. Explicit
unsigned word packing of hardware fields and live-index arpeggio/pitch accesses
then improved it. Independent byte-offset views for the tone instrument and
note/pitch fields, and the note-start output/volume-delay fields, produced the
retained byte candidates. A first-pitch cursor/delay/pair capture with an actual
16-bit hardware-result local gives the final primary improvement.

The six-field preparation, mixed sequence loop, stream reload and global-volume
write order remain intact in the controls. The primary retains its existing
preparation identities. Cursor values and sequence elements are re-read at the
same required updates; no envelope element is cached across cursor changes.
Hardware access order and stored field widths are preserved. The native checks
still bind all 17 existing voice-field aliases to their actual record offsets.

Further hand passes cover hardware packing, live-index versus byte-offset field
views, pointer/pair construction, and next-voice/index/marker lifetimes. The
focused sweeps preserve the original narrow declarations and casts, operate on
macro bodies with their continuations restored, and separately explore the byte
winner and the original-frame source. Each sweep completed its 6,000-candidate
bound without another retained improvement. A follow-up with the original
independent delay/pitch bases and separate first/value/add pair addresses also
stalled. Rejected diagnostics have no admission
standing. Only fixture-approved improvements are retained.

## Structural differences of the byte winner

[structural.json](structural.json) separates original-address windows from
instruction-shape alignment. Counts are heuristic layout evidence, not additive
causal byte attributions or a semantic proof.

| Cause | Remaining evidence |
| --- | --- |
| Allocation | 757 aligned instruction pairs differ in register operands. Voice preparation still assigns next-index, byte-index, marker and field addresses differently. Cursor/delay address construction is closer locally, but this is not recovered full-owner allocation. |
| Scheduling / selection | 388 original and 338 compiled instruction rows remain unpaired. Envelopes are still the largest positional window: 1,369 differing bytes in 1,512, including earlier shifts. Command and note-start windows are positionally closer despite the worse global instruction distance. |
| Control-flow layout | 90 aligned branch pairs differ in destinations. The explicit pair/cursor scopes change envelope joins; restart, command dispatch and the shared return still move. |
| Literal pools | 86 original versus 106 compiled referenced words; 75 aligned PC references differ. More independent field views retain additional literal identities. Stored values are omitted. |
| Frame | Primary 100 versus original 108 bytes. The frame control reaches 108; the instruction control is 104. Original marker sp+36, next voice sp+88 and scaled index sp+92 remain unresolved as a complete assignment. |

Next concrete step: continue from the original-frame control in the command
loop, original 08006D62..08006E00. Recover the current command index and command
stream base as distinct identities through the volume/control commands, keeping
the explicit command-stream reload and the original restart through voice
preparation. Compare the same scope change on the byte primary afterward.
The three pair-address lifetimes, independent pitch/delay bases, next-voice
capture forms and envelope-local expression neighborhoods have now stalled.

All three retained actual-C files pass the unchanged **seven synthetic fixture
groups** apiece with strict warnings and undefined-behavior sanitization. These
are C regression fixtures, not an independent original-instruction oracle or
real-device audio playback. Malformed streams and arbitrary aliasing are not
claimed. Each profile and fixture receipt pins its actual source hash.

Only the primary full sanitized diff is uncompressed. Alternate and baseline
diffs, the measured sweep manifest and experiment recipes are gzip files.
No original binary slice, raw encoding column or pool contents are retained.

```
python tools/measure_candidate.py docs/near-misses/sound-owner-1109d/func_080064A4.c 080064A4 08007398 old build/sound-d-check
python docs/near-misses/sound-owner-1109/check_source.py --candidate docs/near-misses/sound-owner-1109d/func_080064A4.c
```

The schema-2 search archive interns repeated source/output identities and
measurements. Its tables declare every trial column; full 32-byte SHA-256
digests use lossless base64 encoding, while profiles retain hexadecimal hashes.
Every identity, metric and outcome is round-trip checked before packing. Only
random temporary-directory names are normalized in rejected diagnostics.
