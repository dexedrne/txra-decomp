# Uninstalled matching trials

These C sources are continuation material, not accepted replacements or few-shot
examples. The matching build does not consume this directory. Do not add a trial
to `rom.cfg` until its entire compiler output and complete ROM rebuild agree.
No instruction listings, original bytes or extracted tables are stored here.

`func_08014104.c` is the packed-pixel overlay. The default compiler emits 134 bytes
with the correct instruction shapes, constants and internal literal pools, but
10 bytes differ in register choices. The first difference is at offset 0x10;
the exact prefix is 16 bytes and exact suffix is 15 bytes. Saved registers 8/9
and working registers 4/5 are exchanged. Moving the width guard outside the
pointer calculations and sharing the two transparent-byte cases recovered the
control flow. Plain pointer rewrites and changed loop shapes have not fixed the
remaining allocation. The unused read is volatile because removing it changes
the target's initial global read.

`func_080123F0.c` is a lifted reverse halfword-copy decoder, retained for further
hand recovery. It compiles to the full 300-byte extent but differs in 14 bytes,
starting at offset 0x2e; its exact suffix is 55 bytes. Several moves choose a low
register instead of the saved tag, and two mask sequences exchange operands.
It needs readable local names and a complete byte match before installation.
Source values remain references and computed loads, never embedded ROM data.

Check either trial with `python3 tools/diffhint.py <address> <source>` using the
configured matching environment. These are negative comparison results, not a
claim of new matched coverage. The other hand trials remain local under `build/`.
