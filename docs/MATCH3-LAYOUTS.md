# Layout evidence

These are provisional access layouts, with offset names rather than game meanings.
`TxraRecord` at `g_03001E60` has a 100-byte array stride: 0800D214
indexes it by the signed halfword at `g_03004780`, reads a signed halfword
at offset 62, and uses that as a 16-byte table index. 080085E0 independently
uses the same stride and reads offset 02. 0800A5C4 writes words at 04, 08,
0c, 20, 28 and 34 and halfwords at 38, 3c, 48 and 52. 0800A62C independently
reads signed offset 52 and signed word 28. Existing matched users establish
02 and 38. Unobserved gaps retain byte-array padding.

`TxraRow28`, referenced through `g_03006874`, uses a 28-byte stride in
0800A5C4 and 08009F84. Both copy its initial three words; 0800A5C4 also
loads a halfword at offset 0c. No coordinate meaning is assigned.

`TxraRow20` at `g_083B8378` has a 20-byte stride in 0800761C. The first
three words feed three parallel arrays; the second is decremented by one.
The remaining eight bytes remain unknown. This is a single-routine layout,
so its field names deliberately remain offsets.

Function names remain address-based: no new behavior name has yet passed
the requirement for agreement from two independent call sites. Global
names identify addresses only. The volatile local word in 08016210 is the
DMA fill source: it must be written anew for each chunk, and its address
must remain valid while the transfer is started.

The paired slot code uses 16-byte rows at `g_03007A10` and 32-byte rows at
`g_03000B60`. 0801466C reads bytes 00/01 and clears byte 00 of the 16-byte
rows; 080146F4 clears both whole rows. 0801418C reads bytes 00/02 of the
32-byte rows and 08014300 swaps all 32 bytes. `TxraTransfer` records the
three unsigned words consumed at a 12-byte stride by 08015DA8. These
layouts are retained as evidence-backed declarations while those sources
are being trialled; a layout declaration alone is not a matched function.

Two matching details are established by exact comparisons. In 08014458,
register-qualified constant locals preserve the two repeated vertical
arguments in high registers. In 0800ED28, shifting the delta in a separate
assignment preserves the original register allocation; folding the shift
into the following subtraction changes the output. Signed temporary
coordinates and a typed 64-byte halfword table recover the three related
call wrappers at 0800D2F4, 08008780 and 080086C0.

08007698 copies a nine-word table into a local aggregate before indexing it.
The declaration at 0801FF00 refers to the existing table; no table contents are
copied into source. The selected value scales 176 signed bytes in one of two
alternating buffers. The buffer count and stride follow the generated loads,
signed byte multiply and loop bounds.

Additional provisional layouts record the six-byte prefix of the 512-byte
save staging buffer and the communication state at 03007A30. The latter has a
packet pointer at 28, status bytes at 00/01/02/03/08/0b, signed word 14, pointer
arrays at 30/40/50 and buffer regions beginning at 60. 080147D0 writes these
pointers and 08014988 consumes 28 and the status fields. These routines remain
unmatched: these declarations establish observed access layout only. Qualifiers
on trial packet access are provisional and do not establish original source
qualifiers. No save serialization replacement was installed.

The existing 0800D37C replacement now casts the shared typed row pointer to a
byte pointer at its offset-22 access. The declaration moved into `types.h`; the
complete 56-byte compiler comparison remains exact.

08002778 independently uses the same 100-byte record stride, reads signed 00,
02 and 38, and increments/clamps a signed halfword at 50. That newly identified
halfword now occupies the corresponding former padding in `TxraRecord`.
0801084C fills a 12-byte text descriptor: byte fields 00/01/08/09 and a pointer
at 04. It passes the descriptor to 080154AC. `TxraTextRecord` preserves that
layout without assigning meanings to the small control fields.

08005E28/08005E84 match with separate retry checks; combining the checks using
logical OR changes allocation. 0801418C matches as a bounded for loop, whereas
the equivalent do/while shape rotates the body and changes bytes. In 080160C4,
the scoped wait and count-before-pointer updates preserve the observed scheduling.
080146F4 is complete under the recorded `old-no-gcse` compiler option. This choice
is reproducible build evidence, not proof of the original optimization settings.
