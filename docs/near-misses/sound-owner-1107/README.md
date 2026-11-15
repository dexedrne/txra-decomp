# Complete Thumb sound-owner source recovery

Base: `8c850d72cca4f83c9a246190c79edbccfa713e89`.

`func_080064A4.c` is a complete, **uninstalled** structured-C candidate for
`080064A4..08007398`, 3,828 original bytes including pools. It reuses the
11/4b prefix's recovered behavior and adds the complete eight-voice command,
byte-event, envelope and sample-state body. It is not an exact-match claim.
The registry remains at 181 C matches. No ROM, table contents, native binary,
object file or replacement instruction stream is included here.

## Owner and exits

The tracked entry at `asm/program.s:5093` saves r4-r7/LR and r8-r10 and
allocates 108 local bytes. The exact caller `func_08015D08` calls the owner
when `g_03002184 == 0`; tracked pre-replacement assembly also shows its
BL at `08015D40`. The only external calls in this owner are `08005F8C` and
the retained r1 callback veneer `08018DE4`. Ordinary indirect function-pointer
calls express the latter; the owner itself has no private-register arguments.

These mapped labels are parts of the same frame:

| Label | Source role |
| --- | --- |
| `08006712` | Eight-voice loop header; selected voice has 72-byte stride |
| `08006740` | Refresh selected-voice field pointers before command/event work |
| `08006776` | Event/delay processing; also the immediate retry after an end marker |
| `0800735C` | Advance saved voice index; loop through index 7 |
| `08007368` | Shared return; release 108 bytes, restore r8-r10/r4-r7 and original LR |

The early transfers at `080066EC` and `08006700` enter that shared return.
They are represented by the muted gate and unsigned accumulator gate returns.
All later paths either advance the voice, restart its command/event processing,
or reach the same final return. No internal label becomes a C callee.

`docs/map/functions.json` retains six separate candidate entries for this
owner; they are not six independently callable functions. Current `rom.cfg`
contains no installed match overlapping `064A4..07398`. Future acceptance must
compare one whole owner with explicit limit and target end `08007398`, retaining
the strict byte/size checks. Default next-candidate limit `08006712` is an
internal label. No checker defaults or map boundaries were changed.

## State, widths and source ownership

The 72-byte voice layout is the existing `TxraSoundVoice` layout, with provisional
names in the candidate rather than a production header change. Stored addresses
remain 32-bit on both ARM and the host test build. Instrument descriptors are
nine words; sample descriptors four words; hardware sequence records three words.

| Offset | Role |
| --- | --- |
| `00 / 04` | Enabled (`==1`) / hardware-output permission |
| `08 / 0c / 10` | Word-command index / byte-event index / note delay |
| `14 / 18 / 1c` | Note / hardware pitch / instrument or sample index |
| `20 / 24` | Word-command stream / byte-event stream addresses |
| `28 / 2c` | Byte-note transposition / stream repeat count |
| `30 / 34` | Volume cursor / delay; `34` becomes PCM sample-enabled state |
| `38 / 3c` | Pitch-envelope cursor / delay; PCM sample position / length |
| `40 / 44` | Arpeggio cursor / delay; `40` becomes PCM fixed-point step |

The enclosing stack has a copied nine-word fade table in its first 36 bytes.
Other recovered slots are semantic locals/pointers, not incoming C arguments:

| Stack offset | Meaning in the eight-voice body |
| --- | --- |
| `24` | Original byte-stream marker, distinct from the transposed note |
| `28 / 2c` | Voice index times 9 / index times 72 |
| `30 / 34` | Pointers to selected delay / byte-event address |
| `38 / 3c / 40` | Pointers to selected sample position / transpose / delay |
| `44 / 48` | Pointers to selected note / pitch |
| `4c / 50` | Pointers to selected sample step / sample length |
| `54` | Unsigned `voice - 4`, used by the two/four PCM-channel range checks |
| `58 / 5c` | Next voice index / voice index times 8 |
| `60 / 68` | Temporary global-volume arithmetic / original command index |

The callback and four hardware sequences always run before the PCM tick gate.
The unsigned accumulator adds the tempo word with 32-bit wrap, returns at values
0..255, otherwise subtracts **one** 256 and processes one tick. It does not run a
catch-up loop. Fade multiplication also preserves the low 32-bit product before
the signed right shift; signed sample loads remain signed bytes.

Word commands preserve the independent tests and their original order:

| Command | Operation |
| --- | --- |
| `60` | Advance three command words |
| `61` | Stop output; zero the selected hardware register pair, or set PCM position -1 for voices 4/5 only |
| `62` | Assign the next word as an absolute command index |
| `64` | Select byte-event stream, transposition and repeats; clear cursor/delay; advance four words |
| `66` | Store global word `030079C0`; advance two words |
| `67` | Set global volume `(next << 8) + fade_level * 17`, store low halfword to sound control; advance two words |
| `69` | Set tempo accumulator increment; advance two words |

The original loops until command `61` or `64`; malformed/unrecognized command
cycles can therefore still fail to terminate. No invented escape or validation
changes the original state machine. A byte marker `65` handles stream repeats or
clears the stream and immediately resumes word commands in this same tick.
The marker is distinct from a transposed **note** whose value happens to be 65.
Notes truncate to eight bits after transposition. Rest 96 becomes note 96 for
voices 4/5 and note 48 for every other voice. All notes still consume the
instrument and duration bytes. PCM voices 4..7 get table step `95-note`, enabled
state 1, position 0, and `(sample_length-4)<<14`; rest note 96 then sets position
-1. This routine prepares PCM state; the separate ARM `080076F4` mixes samples.

For a voice whose delay starts nonzero, `08006784..08006796` decrements the
delay, then tests the output flag. Output zero skips all continuation envelope
state and hardware writes. With output enabled, hardware voices 0..2 update
arpeggio, pitch slide and volume envelopes even on the final decrement from
1 to 0. Only afterward does `08006D58` test the remaining delay: zero continues
to commands/events in this same tick, nonzero advances the voice. Signed
halfwords are compared to 253; 254 redirects the cursor, while 255 backs it up
to hold the last event. Noise voice 3 uses this same output/delay control flow,
but treats 254 as data and
only 255 as a hold. Its volume change retriggers the frequency register with
bit 15. Initial note programming is output-gated. Channel 0/noise initial pitch
arithmetic adds **-32768**, while channels 1/2 use OR bit 15; these are kept
separate even though ordinary small envelope values produce the same halfword.

## Literal identities

All 112 PC-relative loads reference 86 unique words in eleven in-owner pool
blocks. The first referenced word is `08006574`, the last `08007394`; the last
pool ends at the independent entry `08007398`. Pointer-only reviewed metadata
resolved the additional extern identities used by the recovered body:

- `083C19C0`: instrument-address table (word load, then descriptor dereference).
- `083C100D / 083C0FAC`: high/low frequency bytes (byte-indexed reads).
- `08333324`: PCM step words indexed by `95-note`, including the preceding word for rest 96.
- `083B8698`: 16-byte sample descriptors; length word at offset 4.

No array values were exported or embedded. The address at `03007818` is already
voice 2's pitch field; it stays an access through that voice, not a separate
host object. The three arithmetic pool words were separately confirmed:
`08006A28` is -256, and `08007088 / 08007388` are -32768. Pointer-like values
were used only after the corresponding operand's dereference/index semantics
was checked. The metadata source assembly SHA256 was
`013f6f4982c413494122f6565c5e0f3e662bd9fd6fc232b76596b1f773b132d6`.

## Checks and limits

Run from the repository root:

```
python3 docs/near-misses/sound-owner-1107/check_source.py
```

Seven synthetic groups compile and execute the **actual candidate** with host
`cc`, `-Wall -Wextra -Werror`, and undefined-behavior sanitization. They exercise
output-zero envelope suppression and final-delay envelope-before-command order
for all four hardware voices, hardware sequence redirects/stops,
fade/mute/gate/overflow, all four hardware
note initializations, signed envelope steps/redirects/holds, noise's distinct 254
handling, command chaining/jumps/repeats, transposition truncation, note-65 versus
marker-65, PCM state for all four sample voices, and output-gated stop behavior.
They assert the 12/16/36/72-byte state layouts. Synthetic event/descriptor memory
and hardware words live in fresh low-address mappings; a linker alias supplies
the real rest-note `step[-1]` position. Mapping collisions fail rather than
replacing existing process memory. No ROM or audio process is used.

The two output/delay regressions each failed against the prior candidate
before the shared control-flow fix; all seven groups pass afterward.
The scalar expected values were derived from the tracked instruction paths;
this is not an independent ARM execution comparison. The callbacks and fade
stop callee are synthetic stubs. Arbitrary malformed streams, data aliasing,
every sample/envelope combination and hardware side effects are not established.
The C candidate also passes a separate strict C89 syntax check. These local
source checks do not perform a ROM comparison; the private compiler result below
is separate evidence. No native/ARM execution of this candidate was performed.
Arbitrary malformed streams, aliasing and hardware behavior remain outside these
checks. Macros retain blocks inside one owner, but their source shape has not
reproduced the original bytes.

## One historical-compiler comparison: NONMATCH

Independent source review found and corrected the continuation envelope's
output gate and final-delay ordering in `ed92865`; the two actual-C regressions
failed before that correction and all seven source groups passed afterward.
That corrected source received exactly **one** pinned historical-default `old`
compiler invocation. `compiler-comparison.json` is the sanitized actual receipt;
its source SHA256 matches the committed C candidate. Toolchain pin keys retain
only executable basenames. No instruction listings, original bytes or table
contents are included.

| Measurement | Actual result |
| --- | --- |
| Source commit | `ed92865f5b6399778cb8ae9d74bad551c9d970de` |
| Full target | `080064A4..08007398`, 3,828 bytes including pools |
| Compiled C | 2,996 bytes |
| Exact equality | **false — NONMATCH** |
| Registered C matches | 181 before and after |
| Installed | false |
| Compiler invocations / model calls | 1 / 0 |

Compiled SHA256:
`e274ed409767128ee9eaa0c2021818c038d4af7843104741a226ba9ad024ae1a`.
Full-target SHA256:
`e391678273de8dae8b0f0c4f845dbb86674af3f8b97b7ca015632cc17cf8f301`.
The candidate is shorter by 832 bytes; that is a length difference, not an
instruction or byte-distance score. No matching prefix, frame-size agreement,
whole-owner equality or performance improvement is claimed. Emitted frame and
pool-layout differences have not been diagnosed here.

The actual receipt records unchanged registry, ROM and toolchain, removed
scratch files, zero model calls and no ROM transfer. This was a compiler
comparison, not a native execution, gameplay or audio acceptance run. No
compiler/profile retry followed the nonmatch. The strict whole-owner acceptance
rule was retained; the candidate remains uninstalled and unregistered.

Next: retain the complete source and honest nonmatch evidence for review.
Any later source-shape work needs a separately chosen bounded hypothesis;
this result does not justify another compiler-family sweep. Existing audio
diagnostics and native goldens remain unchanged and do not validate this C.
