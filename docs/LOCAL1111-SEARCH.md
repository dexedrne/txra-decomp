# Resumable region search

`tools/llm_blocks.py` searches small C regions in the complete HUD, sound and
renderer owners. It is pinned to `work/local-1111`, the private cartridge hash,
and the historical `old` / `arm` profiles. It does not need a browser.

The baseline owners are retained from `hud-owner-1110`, `sound-owner-1109d`
and `arm-16da8-1110`: **3,168**, **3,227** and **3,251** differing bytes.
These are reproduced measurements, including the complete owner and pools.
They supersede the approximate sound and renderer numbers in the task brief.

For each request, a debug compilation must reproduce the pinned non-debug
output exactly. Its source-line map attributes positional byte differences to
complete C statements and sibling groups. The search visits the worst unvisited
region that fits the context allowance. Original regions normally contain at
most 16 lines; replacements have a hard 40-line limit. This leaves room for four
actual alternatives. Referenced declarations, types, helpers and macro dependencies,
both complete region listings, matching patterns and nearby examples accompany
the region. Positional attribution is a layout aid, not semantic alignment.

A proposed region beginning with new local declarations receives a C89 compound
scope before splicing. Its expressions and statement order stay exactly as
proposed. This normalization is logged and still must fit the 40-line cap.

`--context-tokens 8192` halves the normal 16,384-token allowance and uses smaller
complete region windows. It also shortens naming excerpts and the generation
allowance. This is a client-side diagnostic for an unstable or memory-constrained
service; it does not establish the cause of connection failures or alter any
compiler or semantic gate. The chosen allowance is recorded in the checkpoint.

Requests are serial and use the existing shared service lock. The primary is
`kat-coder-v2.5:iq3s`; every ninth block request uses
`qwen3.6-35b-a3b:iq3s` as a second opinion. Only an already loaded permitted
model can be unloaded during a switch. Unrelated models and outages are waited
out, without pulling anything. Complete alternatives from a truncated reply can
still be judged; missing C is never reconstructed. Unusable replies also advance
region selection. Response diagnostics remain in ignored build scratch.

Every alternative is logged, including safety rejections, duplicates, compiler
failures, boundary failures, semantic failures, ties and regressions. Only
distinct alternatives that receive a whole-function measurement count toward
the **200 measured HUD attempts**. Synthetic unit-test proposals never enter
these counters. After the proof, the loop rotates through sound, ARM and HUD.
The default visit is 40 measurements; this run uses `--rotation-attempts 12`
to reach both secondary owners sooner. The ARM owner always uses
`agbcc_arm -O2 -mthumb-interwork`.

Each compiled alternative also runs the unchanged semantic fixtures in a bounded
worker. These cover 1,024 prior-C HUD state/call fixtures, seven synthetic sound
groups, and 199 independent ARM memory fixtures with 20 fixed checks and layout
checks. They are regression gates, not proof of arbitrary game-state behavior.
An improvement requires a strictly smaller whole-owner differing-byte count,
successful fixtures and the original owner boundary. Nothing can widen that
boundary. The full retained C, sanitized diff, compiler profile and fixture receipt
live under:

- `docs/near-misses/hud-owner-1111/`
- `docs/near-misses/sound-owner-1111/`
- `docs/near-misses/arm-16da8-1111/`

Their `improvements/` subdirectories retain accepted source revisions. Baseline
profiles point to the immutable previous sources. No object or original binary
slice is retained there. A replacement can install only after exact complete-owner
equality and the existing forced rebuild, every installed C comparison and full-ROM
hash gate. Exact counts are then refreshed. There are no automatic commits or pushes.

Naming requests use one matched function at a time to avoid confusing callees
with their caller. Four serial naming requests follow each block batch until
all address-named matches have proposals. `docs/names-1111.md` is a review table;
it never changes source identifiers. Larger evidence excerpts are marked and
their confidence is reduced. Camel-case suggestions are formatted as snake case.

Read the live status and recent attempts from this checkout:

```sh
"$HOME/opt/txra-venv/bin/python" tools/llm_blocks.py --status
tail -n 20 build/llm-blocks.log
systemctl --user status txra-blocks-local-1111 --no-pager
```

Stop through the checkpoint, which verifies the exact PID and its start time
before sending SIGTERM:

```sh
"$HOME/opt/txra-venv/bin/python" tools/llm_blocks.py --stop
```

If the process has already failed and a restart is scheduled, cancel that retry
with `systemctl --user stop txra-blocks-local-1111`. The unit uses
`KillMode=process`, so its stop signal targets only its owned main process.

The candidate adoption transaction finishes before a signal takes effect.
Pending alternatives and their cursor survive a stop. A new owner-note hash
pauses the loop for operator review; read and apply those notes before updating
the reviewed hash in the checkpoint. An external candidate edit is refused.

Resume after a clean stop with the same user service command. The transient unit
can be collected after it exits, so create it again rather than assuming its old
definition remains available:

```sh
systemd-run --user --unit=txra-blocks-local-1111 \
  --working-directory="$PWD" --setenv="TXRA_TOOLS=$HOME/opt" \
  --property="StandardOutput=append:$PWD/build/llm-blocks.log" \
  --property=StandardError=inherit --property=KillMode=process \
  --property=TimeoutStopSec=120 --property=Restart=on-failure \
  --property=RestartSec=60 \
  "$HOME/opt/txra-venv/bin/python" -u tools/llm_blocks.py --names-every 1 \
  --context-tokens 8192 --rotation-attempts 12
```

`--prepare` verifies baselines without service requests. `--max-judged N`
stops after N total measured alternatives across the resumed checkpoint.
`--names-only` resumes just the proposal table. The checkpoint is
`build/llm-blocks-status.json`; the in-flight batch is
`build/llm-blocks-pending.json`. Leave these in place when resuming.
