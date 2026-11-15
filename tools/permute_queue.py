#!/usr/bin/env python3
"""Build a metadata-only mutation-search queue from current, unmatched entries.

The night runner should regenerate this queue before each round. Candidate JSON
is a list of addresses or records with an ``address`` field. Score JSON is either
an address-to-score object or a list of ``address`` / ``best_score`` records.
Multiple score snapshots are allowed; the lowest score for each entry wins.
No compiler, ROM, or search result is modified.
"""
import argparse
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BASE = 0x08000000


def address(value):
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        text = value.removeprefix('func_')
        if re.fullmatch(r'(?:0x)?[0-9a-fA-F]{8}', text):
            return int(text, 16)
    raise ValueError('expected a ROM address, got %r' % value)


def score_value(value):
    if isinstance(value, dict):
        value = value.get('best_score', value.get('score'))
    # Some searches retain a primary instruction score and a byte tie-breaker.
    if isinstance(value, (list, tuple)):
        if not value:
            return None
        parts = [score_value(x) for x in value]
        if any(part is None or len(part) != 1 for part in parts):
            raise ValueError('invalid search score: %r' % value)
        return tuple(part[0] for part in parts)
    if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0:
        return (value,)
    if value is None:
        return None
    raise ValueError('invalid search score: %r' % value)


def best_scores(snapshots):
    scores = {}
    for snapshot in snapshots:
        rows = (snapshot.items() if isinstance(snapshot, dict) else
                ((row['address'], row) for row in snapshot))
        for key, value in rows:
            a, score = address(key), score_value(value)
            if score is not None and (a not in scores or score < scores[a]):
                scores[a] = score
    return scores


def queue(config, functions, candidates=None, scores=None):
    """Filter exact matches AND internal entries covered by complete matches.

    The authoritative match list is rom.cfg, never a copied progress count or a
    source filename. Unknown/stale inventory addresses are rejected explicitly.
    """
    inventory = {address(f['start']): f for f in functions}
    matched = {BASE + m['offset'] for m in config['matches']}
    covered = [(BASE + m['offset'], BASE + m['offset'] + m['size'])
               for m in config['matches']]
    scores = scores or {}
    selected = inventory if candidates is None else {
        address(c['address'] if isinstance(c, dict) else c) for c in candidates}
    out = []
    for a in selected:
        if a in matched or any(start <= a < end for start, end in covered):
            continue
        if a not in inventory:
            raise ValueError('candidate %08X is absent from the function inventory' % a)
        f = inventory[a]
        out.append({'address': '%08X' % a, 'mode': f['mode'],
                    'bytes': address(f['end']) - a,
                    'best_score': list(scores[a]) if a in scores else None})
    return sorted(out, key=lambda row: (row['best_score'] is None,
                  tuple(row['best_score'] or ()), row['bytes'], row['address']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'tools/rom.cfg')
    parser.add_argument('--inventory', type=Path, default=ROOT / 'docs/map/functions.json')
    parser.add_argument('--targets', type=Path, help='optional existing target list; defaults to all mapped entries')
    parser.add_argument('--scores', type=Path, action='append', default=[], help='score snapshot; may be repeated')
    parser.add_argument('--plain', action='store_true', help='emit addresses, one per line, for a shell runner')
    args = parser.parse_args()
    try:
        rows = queue(json.loads(args.config.read_text()),
                     json.loads(args.inventory.read_text())['functions'],
                     json.loads(args.targets.read_text()) if args.targets else None,
                     best_scores(json.loads(p.read_text()) for p in args.scores))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    if args.plain:
        print('\n'.join(row['address'] for row in rows))
    else:
        print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
