# 08016DA8: typed point indexing and geometry lifetimes

Complete structured-C **nonmatch**, uninstalled and uncounted. The original
4,288-byte owner and its pools are compared under the unchanged historical
`arm -O2 -mthumb-interwork` profile and strict end 08017E68.

| Measurement | Retained 11/9 source | Retained 11/9b source |
| --- | ---: | ---: |
| Output bytes | 4,016 | 4,220 |
| Local frame bytes | 88 | 120 |
| Instruction edit distance | 855 | 859 |
| Differing bytes, including missing tail | 3,677 | 3,401 |

`func_08016DA8_match.c` is a separate **single-cursor nonmatch control**, despite
its legacy fixture-compatible filename: 4,164 output bytes, 112-byte frame,
859 instruction edits and 3,503 differing bytes. Its profile and compressed diff
are `single-cursor-control.*`. Both sources pass the independent checks below.

The claim is a **276-byte improvement in the complete comparison**. Instruction
distance regresses by four and the frame is 24 bytes above the original's 96.
Those regressions are not hidden by the closer output length. This source is
not ready for installation and is not proof of a recovered original allocation.

The source retains the near-first path and projection expressions. It captures
source vertex identities, indexes the existing 28-byte point records, and keeps
A/B/C y/z pointers outside the four-part loop while x uses point indexing. D is
addressed within its three subdivision cases. Typed face records retain the
original index loads. Unsigned midpoint/multiply/add/subtract arithmetic still
wraps before signed right shifts. The synthetic build maps those same typed
reads into the existing memory fixture; it does not substitute a second geometry
algorithm.

The bounded pass measured separate x byte offsets, typed base placement, scalar
and array source indices, signed depth/counter shapes, one/two face cursors,
branch-local D pointers, far-field scopes and declaration order. Most explicit
component spellings compile identically. A single face cursor reduces the frame
to 112 but raises byte distance to 3,503; a three-index array reaches 104 with
worse comparisons. No source padding, new storage, register binding, assembly,
compiler sweep, projection-induction rerun or car-contact trial was used.
`search-summary.json` has deduplicated counts; `search.json.gz` records every
measured source/output identity and invalid declaration hypothesis.

The unchanged independent textual ARM executor versus actual compiled C passes
199 synthetic memory fixtures, 20 fixed expected checks, three layout sizes and
14 field offsets. It reaches all 1,053 original instruction addresses. The
11/7 reference's stable-input, valid-index and alias assumptions and unproven
malformed cases still apply. This is not real-game execution or a byte match.

Reproduce from the repository root with the existing project Python environment:

```
python tools/measure_candidate.py docs/near-misses/arm-16da8-1109b/func_08016DA8.c 08016DA8 08017E68 arm build/arm-1109b-check
python3 docs/near-misses/arm-16da8-1109b/check_semantics.py
python3 docs/near-misses/arm-16da8-1109b/check_semantics.py --control
```

Next concrete step: separate the far-path point/depth values from near-path
geometry allocation without carrying a second face cursor through both. The
retained output duplicates the next-face address and spills the B depth twice;
original setup 08016E08..08016EF0 has one next-face spill, separate A/B/C x
offsets and three y/z pointers. Start with the retained single-cursor control, move the direct-screen loads into their own block, and recover
those original spills before touching projection arithmetic. Simply spelling
component offsets or branch-local D pointers was measured here and is not the
next experiment.

Only the best candidate's full sanitized diff is uncompressed. Search manifests
are gzip files; no ROM slice, extracted binary, raw instruction encoding or
literal-pool contents are retained here.
