# Contact rotation and record lifetimes

This complete hypothesis improves the round-one retained source from **1,011 to 919 differing bytes** and **307 to 254 instruction edits**. The output remains **1,660 / 1,684 bytes**, while the local frame rises from **64 to 68 / 72 bytes**. It is not an exact replacement, is absent from the build and does not change the match count.

The retained form keeps signed 32-bit lookup coefficients, uses a positive pair guard, reuses the loaded x/z locals across the two rotations and reads the second rotation coefficients at their uses. It is a measured allocation/aliasing hypothesis, not a claim to have found the original declarations. The finite trial groups include point pointer forms, coefficient order/cache choices, coordinate dataflow, array/byte offsets, derived indices and natural context after the adjacent installed ARM routines. The unchanged historical `arm` profile and exact 08018854 owner end are used throughout. No assembly, bound register, padding, injected instruction, output patch, compiler-family sweep or wider checker limit is introduced.

`original-fixtures.json` reports **384/384** comparisons with the actual original ARM instructions running from a read-only private ROM image in memory. They cover **all 403 original instruction addresses**, 352 state-changing cases, 38 contact results, 67 cache-clearing cases and 239 detections of the intentionally narrowed coefficient control. The original lookup tables are also read in memory; no bytes or tables are serialized. This is bounded synthetic state evidence, not gameplay, arbitrary malformed-state coverage or byte equality. The separate earlier-C fixture passes 768 cases and rejects its narrowing control in 428; its reference is C, not the original instructions.

Reproduce the two independent gates with the existing compiler environment and Unicorn 2.1.4 available to the Python environment:

```sh
python tools/measure_candidate.py docs/near-misses/breadth-1112b/contact-final/func_080181C0.c 080181C0 08018854 arm build/contact-recheck
python tools/check_contact_reference1112b.py docs/near-misses/breadth-1112b/contact-final/func_080181C0.c build/contact-original-fixtures.json
```

Next recover why the original retains both its record-index intermediates and the first sine coefficient in the frame, accounting for the remaining four frame bytes and 24 emitted bytes. The lower 199-edit diagnostic has a worse byte distance and is retained only as structural evidence. Its extra frame/byte differences do not authorize an installation.
