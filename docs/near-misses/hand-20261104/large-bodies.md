# Large-body recovery, 11/4

These are boundaries and source-level pieces read from the complete enclosing
routines. No piece below is an installed match. Internal mapped entries must
stay inside their enclosing frame.

## 08002854 with 08003786: track streamer

The prologue reserves 268 bytes. The entry at 08003786 reads sp+208 and
sp+4 before defining them; it is a continuation, not a callable C helper.
The initial source-level window is:

```c
if (direction == 0) {
    center = track_position + 28;
    if (center >= track_length) center -= track_length;
} else {
    center = track_position - 1;
    if (center < 0) center += track_length;
}
next = center + 1;
if (next >= track_length) next = 0;
next2 = next + 1;
if (next2 >= track_length) next2 = 0;
previous2 = center - 2;
if (previous2 < 0) previous2 += track_length;
previous = center - 1;
if (previous < 0) previous += track_length;
```

Here `direction`, `track_position` and `track_length` are the words at
03002334, 03005F50 and 03002E4C. The five window values become sp+12,
sp+16, sp+20, r10 and sp+8. The forward ring row starts at 030001B8;
the reverse row is `(tick - 29) & 31`. At 08002928 the face-row pointer
is `0x02033B70 + (row & 31) * 1344`; three point-row indices are
`((row + k) & 31) * 24` for k=0,1,2. Preserve those two different
strides when recovering the typed arrays.

The continuation's first type test is an unsigned byte range check:
`(u8)(row_data[23 + column] - 3) <= 8`. Its accepted path emits several
28-byte points with the already matched 08005DD4 and 08005F48 helpers and
writes their indices into a 56-byte face. A full draft still needs the
preceding type cases, shared arrays and all continuation paths. Copying
this prefix into a standalone function would give the wrong frame.

## 080064A4 through 08007378: sound control and mixing

This is one Thumb frame with 108 local bytes. 08006712 is the eight-voice
loop header, 08006740 prepares pointers to the selected 72-byte voice,
08006776 continues its body, 0800735C advances the voice counter, and
08007368 restores the enclosing frame. The long BLs between these entries
are far branches.

The initial fade increments the word at 03007400 modulo 16 when
030079B4 is 1. On wrap it decrements 030079B0, retains the upper byte of
the halfword at 04000080, and replaces its lower byte with `level * 17`.
When level reaches zero it calls 08005F8C with zero, clears the fade flag,
then stores level 7. Keep the clear inside that branch so CSE can reuse
the zero loop variable.

The output block is the 176-byte half of 03007410 selected by
`((g_03006A98 + 1) & 1) * 176`. A nonzero 03007570 clears it in a
descending loop. Otherwise an indirect callback is invoked unless the
fade flag is set and its level is zero. An intermediate fade level
scales all 176 signed samples by a value from a nine-word local table,
then shifts right by 8. The table comes from 0801FF00; its contents are
not copied into source or review evidence.

At 080065C2 a second indirect callback runs for arguments 0 and 1.
The following hardware-channel loop visits four **12-byte** sequence
records at 03007590, paired with fields in the 72-byte voice records.
Each sequence cursor advances by five halfwords per event; the first
halfword is a delay/control value. The 254/253 and 255 control cases
should be recovered as ordinary branches before attempting the remaining
voice switches. The later PCM voice loop has eight iterations; these
two loop bounds and strides must stay distinct. No complete C draft is
claimed for this enclosing function.

## 08016DA8: projected track-face renderer

The record stride is **56**, and each ring row occupies 1344 bytes:
24 records per row, with a zero kind marking the end. A provisional
layout is:

```c
typedef struct {
    u16 kind, padding;
    s32 index[4];
    s32 u[4], v[4];
    u16 count, unknown;
} TrackFace;
```

The point buffer at 02014000 has 28-byte records, including projected
x/y at +16/+20 and depth at +24. Row traversal starts at
`(tick - 29) & 31` and ends at `(tick - 6) & 31`.

The first face test loads four depths into a local four-word array.
If all four exceed 767 it enters the direct path at 08017AA8; otherwise
the path beginning at 08016E90 handles subdivision/clipping, including
the six-point scratch buffer at 030057A0. The output quad layout and
depth-bucket insertion are shared with the now matched 080165BC.
The common direct-path tail clamps x to [-66,186], copies four u/v
coordinates, computes the bucket from summed depths shifted by 7 plus
32, and clamps it to [0,255]. Kind 2 selects output kind 1; kind 4
selects output kind 2. Its bucket insertion advances the 32-byte output
pointer while advancing the input face by 56 bytes. The next useful
piece is the direct path and shared insertion tail; the clipping body
still requires its own full source recovery.
