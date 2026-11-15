# Mutation-search target selection

`tools/permute_queue.py` rebuilds a queue from the current `tools/rom.cfg`
match list and `docs/map/functions.json`. It excludes installed entries and
internal entries covered by an installed body. Regenerate it before **each**
round, including after a match is accepted. A copied progress count or yesterday's
target list must never decide whether an entry is still unmatched.

An existing target list can contain address strings or records with an
`address` field. Score snapshots can be address-to-score objects or lists of
records with `address` and `best_score` fields. Repeated snapshots retain the
lowest score per entry. Scalar permuter scores and instruction/byte score pairs
are supported; only compare snapshots using the same scoring system. Entries
with scores run first, ascending; untried entries follow, smallest first.

```sh
python3 tools/permute_queue.py --targets build/night-targets.json \
  --scores build/night-scores.json --plain
```

With no `--targets`, it lists all unmatched mapped entries, including assembly
interfaces and internal fragments. That inventory is for inspection; a search
runner should supply its candidate list of complete C bodies. Missing score
snapshots should be omitted, not replaced with invented scores.

At the 178-match baseline, 080165BC, 08017F64, 08017E68 and 08018E18 are all
already installed and are automatically excluded regardless of candidate order
or score. A valid 606 score for 080076F4 ranks ahead of untried candidates.

The requested `feat/permuter-1103` branch was absent from the supplied checkout,
its origin and available local bundles during this pass. This standalone helper
and its tests are ready to import into that adapter or call from its night
runner. Until that branch or runner is available, this does **not** establish
that the live scheduled search consumes the filtered queue.
