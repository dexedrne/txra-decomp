# 080064A4: sequence cursors and shorter tone-field lifetimes

Complete structured-C **nonmatches**, uninstalled and uncounted. The unchanged
historical `old -O2 -mthumb-interwork` profile compares 080064A4..08007398,
including the full shared return and pools. No admission boundary was enlarged.

| Source | Output bytes | Frame | Instruction edits | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Retained round-2 primary | 3,656 | 100 | 1,452 | 3,395 |
| `func_080064A4.c` | 3,692 | 100 | 1,415 | 3,353 |
| Round-2 six-field control | 3,668 | 100 | 1,380 | 3,542 |
| `preparation-control.c` | 3,692 | 100 | 1,338 | 3,542 |
| Original owner | 3,828 | 108 | — | 0 |

The primary improves by **42 differing bytes** and 37 instruction edits. The
corrected six-field control improves by **42 instruction edits**, with unchanged
byte distance. It remains a separate, promising source hypothesis rather than
the byte winner. Both still have an eight-byte frame deficit.

The recorded sequence-to-voice base/counter step was tried first. Sharing a base
through every envelope macro over-collapsed the field captures; narrower entry
base and counter variants also failed to beat the prior primary. The retained
six-field control uses mixed sequence record/byte-offset/cursor identities and a
captured event-stream address, then gives tone instrument/sequence and noise
arguments their own scopes. It preserves the corrected volume-cursor field at
voice offset 48 and the explicit command-stream reload.

The primary instead narrows the tone instrument scope, addresses the clear-buffer
start through its actual countdown, and addresses pitch cursor, volume delay and
output through their existing independent field bases instead of carrying three
extra pointer captures across phases. The existing field aliases and two-stage
global-volume write remain. No new state object, padding, register binding,
assembly, compiler-family sweep or hardware-access reordering was added.

## Structural diff of the best candidate

[structural.json](structural.json) aligns instruction shapes separately from its
original-address windows. Counts describe layout and syntax; they are **not an
additive allocation/scheduling byte attribution** or a semantic proof.

| Cause | Remaining region / evidence |
| --- | --- |
| Allocation | 746 aligned instruction pairs differ in register operands. Sequence-to-voice setup 080065C2..0800677A still places the counter/base and preparation fields differently; the primary captures more than the original six fields. |
| Scheduling / selection | 378 original and 287 compiled rows are unpaired by shape alignment. Envelope updates 0800677A..08006D62 span 97 original blocks and 1,319 positional differing bytes, the largest remaining window. Cursor reloads and hardware-value construction remain differently ordered or selected. |
| Control-flow layout | 74 aligned branch pairs have different destinations. Envelope exits, command dispatch, stream restart and the shared return move. The original restart at 08007358 targets 08006776; all source restart paths still pass the existing fixture checks. |
| Literal pools | 86 original versus 98 compiled referenced pool words; 72 aligned PC-reference pairs differ. Independent field bases and displaced envelope/command pools account for many literal-reference differences. Pool contents are omitted. |
| Frame | 100 versus 108 local bytes, with a 136-byte output deficit. Original sp+36 holds the stream marker, sp+88 the next voice index and sp+92 the scaled index; the candidates still keep some of those roles or field pointers in registers. |

Next concrete step: continue from `preparation-control.c` in the first tone's
pitch/volume envelope region, original 0800681C..08006918. Recover the separate
sequence-cursor address, sequence-value address and 16-bit hardware-result
lifetimes. In particular the original retains both the field address used to
advance the cursor and the address of its current sequence pair through the
sentinel tests. Preserve the six-field preparation, mixed sequence loop and
current command reload; compare the complete owner, frame and pools after each
change. Broad base sharing, explicit next-counter/marker shapes, extra pointer
phase placement and the clear-buffer/fade alternatives were measured here.

Both retained actual-C files pass the unchanged **seven synthetic fixture
groups**, strict warnings and undefined-behavior sanitization. They are not an
independent original-instruction oracle, device/audio playback, or proof for
malformed streams and arbitrary aliases. The primary was remeasured after
removing unused pointer declarations/assignments: its compiled hash changes,
while its full byte distance, instruction distance, output length and frame
remain the same. Final profiles and fixture hashes refer to that cleaned C.
Rejected historical-C and macro-member declaration hypotheses remain diagnostics
in the compressed manifest, not successful semantic checks or matches.

```
python tools/measure_candidate.py docs/near-misses/sound-owner-1109c/func_080064A4.c 080064A4 08007398 old build/sound-1109c-check
python3 docs/near-misses/sound-owner-1109/check_source.py --candidate docs/near-misses/sound-owner-1109c/func_080064A4.c
python3 docs/near-misses/sound-owner-1109/check_source.py --candidate docs/near-misses/sound-owner-1109c/preparation-control.c
```

Only the primary full sanitized diff is uncompressed. The control diff and long
search manifest are gzip files; no ROM slice, extracted binary, raw instruction
encoding or literal-pool content is retained.
