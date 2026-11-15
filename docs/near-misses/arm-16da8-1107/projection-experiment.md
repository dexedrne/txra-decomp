# Projection-loop induction hypothesis

Base: `17dfbfc99d311d11a3364c171473cc987344d277`.

`func_08016DA8_projection.c` is a separate, unregistered variant of
`func_08016DA8_match.c`. Only the variant header and `project_subquad` loop
shape differ. The readable reference, prepared control, generator, registry,
profiles, assembly and original comparison gates are unchanged.

The original instructions at 08017308–0801746C retain four loop roles:
vertex count in r8, word offset at fp-88 (step 3), byte offset at fp-84
(step 12), and scratch-Z cursor at fp-80 (step 12). The variant expresses
these separately and uses a signed vertex count with `do` / `<= 3` termination.
All address and arithmetic words remain unsigned; the signed counter is only
0 through 4. Memory reads/writes retain the prepared control's order and
widths. This is one source-shape hypothesis, not a profile or permutation sweep.

Run the unchanged differential fixture set with the newly allowed filename:

```sh
python3 docs/near-misses/arm-16da8-1107/check_semantics.py --candidate func_08016DA8_projection.c
```

The host-GCC synthetic run passes 199 fixtures, 20 fixed expected checks,
3 record sizes and 14 field offsets, reaching all 1,053 instruction addresses.
The exact source and assembly hashes are in `semantics-projection.json`.
The existing assumptions and coverage limits in README.md still apply;
address coverage does not prove every input or predicate outcome.
`prepare_match.py --check` still passes for the unchanged prepared control.

The bounded private-host comparison has now completed under the original historical
`arm -O2 -mthumb-interwork` profile, using the existing pinned compiler. The
prepared control reproduced 4,028 bytes and its known compiled SHA-256 before
one projection variant was compiled. The variant is 4,036 bytes versus the
complete 4,288-byte target; it remains a nonmatch. Instruction/byte difference
scores changed from 1046/3850 to 1047/3840, which is mixed evidence, not acceptance.
See `projection-private-comparison.json` for source, compiler and result hashes.

The original 4,288-byte assembly fixture matched the private ROM; all 19 pool
bindings were verified. Strict relocation, extent and next-entry checks remained
active. Registry count remains 181; source snapshot and private ROM were unchanged,
no ROM was transferred, and temporary comparison scratch was removed. An initial
run stopped before compilation because the system Python lacked Capstone; the
completed run reused the host's existing decomp-permuter environment without
installing packages.

No replacement was registered or installed. No runtime or FPS gain is established.
This bounded hypothesis is exhausted; do not repeat it as a profile sweep.
Complete target byte equality and the existing whole-ROM gates are still required.
