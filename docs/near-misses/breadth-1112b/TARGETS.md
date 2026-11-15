# Breadth round two targets, 12 November

Refreshed from the 189-match / 237-entry starting registry. The eight new small standalone functions from round one are already installed and are removed from this pending table. Extent sizes exclude trailing pools; no internal window can be installed separately. Sort order is size, historical byte distance, then address.

| Entry | Extent bytes | Mode | Earlier best byte diff | Disposition |
| --- | ---: | --- | ---: | --- |
| 08018E84 | 2 | thumb | 1 | instruction-state veneer; paired ARM tail already installed |
| 08018DE0 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018DE4 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018DE8 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018DEC | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018DF0 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018DF4 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018DF8 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018DFC | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018E00 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018E04 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018E08 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018E0C | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018E10 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018E14 | 2 | thumb | — | register-call veneer; no standalone ordinary C ABI |
| 08018E7C | 2 | thumb | — | instruction-state veneer; paired ARM tail already installed |
| 08018A54 | 4 | thumb | — | BIOS wrapper; structured C cannot issue SWI |
| 08018A58 | 4 | thumb | — | BIOS wrapper; structured C cannot issue SWI |
| 0800D960 | 8 | thumb | 2 | covered by installed func_0800D51C |
| 0800735C | 12 | thumb | — | internal block/shared tail; needs whole enclosing owner |
| 080095C4 | 14 | thumb | 10 | covered by installed func_08008A88 |
| 08007368 | 16 | thumb | 15 | internal block/shared tail; needs whole enclosing owner |
| 080051FE | 16 | thumb | 16 | internal block/shared tail; needs whole enclosing owner |
| 080001F4 | 36 | arm | — | startup, IRQ, division or private renderer ABI; see docs/asm-only.md |
| 08006712 | 46 | thumb | — | internal block/shared tail; needs whole enclosing owner |
| 080000C0 | 52 | arm | — | startup, IRQ, division or private renderer ABI; see docs/asm-only.md |
| 08006740 | 54 | thumb | 53 | internal block/shared tail; needs whole enclosing owner |
| 0800027C | 68 | arm | — | startup, IRQ, division or private renderer ABI; see docs/asm-only.md |
| 080002CC | 88 | arm | — | startup, IRQ, division or private renderer ABI; see docs/asm-only.md |
| 08000218 | 100 | arm | — | startup, IRQ, division or private renderer ABI; see docs/asm-only.md |
| 0800D570 | 192 | thumb | — | covered by installed func_0800D51C |
| 080000FC | 248 | arm | — | startup, IRQ, division or private renderer ABI; see docs/asm-only.md |
| 08000AA0 | 320 | arm | — | startup, IRQ, division or private renderer ABI; see docs/asm-only.md |
| 080010B8 | 336 | arm | — | startup, IRQ, division or private renderer ABI; see docs/asm-only.md |
| 080016E0 | 452 | arm | — | startup, IRQ, division or private renderer ABI; see docs/asm-only.md |

## Next eligible complete owners

| Entry | Complete bytes | Previous best byte diff | Work order |
| --- | ---: | ---: | --- |
| 080181C0 | 1,684 | 1,011 | Recover rotation setup and index lifetimes; 64 / 72-byte local frame. |
| 08002854 | 6,456 | no complete retained structured draft | Recover streaming owner through its continuation and balanced return. |

The 08003786 registry entry is an internal continuation of 08002854, not another function. The 0800421C, 080064A4 and 08016DA8 owners and their interior labels are excluded throughout this round. Their region search remains separate and running. The naming results cover installed functions only; they provide no additional standalone candidate.

## Small recovery windows

| Owner | Window | Bytes |
| --- | --- | ---: |
| 08002854 | 08002854–080028BC | 104 |
| 08002854 | 080028CC–080029A6 | 218 |
| 08002854 | 08002EB8–08002F62 | 170 |
| 08002854 | 08002F70–08002FBA | 74 |
| 08002854 | 080036FC–08003786 | 138 |
| 08002854 | 08003A50–08003B48 | 248 |
| 08002854 | 08003F78–0800417E | 518 |
| 080181C0 | 080185E0–080187C4 | 484 |
| 080181C0 | 080187DC–08018848 | 108 |
| 080181C0 | 0801884C–08018854 | 8 |

The broader Thumb gap scan begins at 080000C0 rather than round one's 08002000, blocks every established instruction and pool, and yields zero candidates from seventeen checks. No ordinary ARM save/frame prologue occurs in the unclassified pre-program gap. Pointer/call proposals and semantic boundaries require separate review; no map entry is invented to increase the total.

## Round-two result

No new standalone code entry passed review or matching. The early gap is a validated 2,050-byte raster reciprocal table, which classifies 1,548 more data bytes and leaves 719,822 bytes unknown. The broad LR-saving Thumb-prologue diagnostic rejects all 331 tested candidates and finds no ARM frame-start signature. The full-ROM edge/prologue leaf scan also yields zero candidates from 5,732 checks in 334.81 seconds. No new map entry is inferred from those negative searches.

The retained 080181C0 candidate improves **1,011 → 919 differing bytes**, **307 → 254 instruction edits** and **64 → 68 / 72 local frame bytes**. Its output remains **1,660 / 1,684 bytes**. All 403 original instruction addresses are exercised by the independent bounded-state check, but the source is still a nonmatch. Three finite source neighborhoods measured 1,566 complete-owner alternatives, including repeated identities across neighborhoods; the ledger records the unique total separately. The 199-edit structural diagnostic has a worse byte score and is not the retained candidate.

08002854 now has a typed opening hypothesis through 080029F0 and independent original-Thumb checks. The complete geometry owner is still unfinished; preserve the fifth argument of every 08005F48 call. The larger internal labels 08007B40 and 0800D630 are already covered by installed 08007B28 and 0800D51C owners.
