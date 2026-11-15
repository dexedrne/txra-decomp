# Round 4 shared names and evidence

`gSaveStaging` aliases 03005FE0 and retains the existing 512-byte
`TxraSaveBlock` layout. The newly matched 08013B38 and 08013C08 read and write
the same payload fields after six header bytes; 08005E28 and 08005E84 transfer
64 eight-byte blocks to and from EEPROM. Packing and unpacking keep their
original byte order, validation and retry behavior.

`gKeysHeld` aliases 030014BC. 08015D78 stores the complement of hardware
KEYINPUT there after calculating the newly pressed mask; 08014E8C tests a
held-button combination and polls until release. 0300218C retains its address
name because the matched consumers have not independently established its use.

`gOamShadow` aliases 03005B40. 08015200 copies three halfword attributes per
eight-byte entry, and 08014E8C transfers exactly 1024 bytes to hardware OAM.
08005CF4 writes signed affine coefficients at halfword offsets 3/7/11/15 for
each group of four entries. `TxraOamEntry` names the three attributes and the
interleaved affine parameter. Its eight-byte size and the four-entry matrix
spacing agree. The older signed-halfword alias in 08005CF4 stays valid: changing
its declaration to a byte array changes allocation despite equivalent accesses.

`gEepromGeometry` aliases 03007B50. 08018A5C selects one of two existing ROM
geometry records; 08018AA4 reads the halfword at offset 6 into WAITCNT and
08018B24 checks the halfword at 4 and emits the byte-at-8 count of address bits.
`TxraEepromGeometry` retains the unproven word at 0 and names block count at 4, wait control
at 6 and address bits at 8, with the remaining bytes unnamed. The standard
compiler choice already recorded for the selector remains necessary.

`TxraSoundVoice` records the shared 72-byte voice stride: 08005F8C initializes
eight voices, while 08006712 and 08006740 read control words and derive parallel
pointers at the same stride within the sound mixer copied during 08007398.
Only the subsystem and record are named; individual controls retain offsets.
The mixer fragments are not installed as standalone C functions.

Car and physics field meanings remain provisional. Strides and arithmetic alone
are insufficient to distinguish position, velocity, temporary transforms and
other game records. No function symbol was renamed from a guess.

The aliases resolve to the same addresses in both standalone trial comparison
and the complete build. Address-based names remain valid for existing sources.
All changed installed sources must continue to compare across their full extents.
