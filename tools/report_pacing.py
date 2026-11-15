#!/usr/bin/env python3
"""Summarize measured frame intervals from one complete paced career replay."""
import argparse
import csv
import json
import math
from pathlib import Path
import statistics


def summary(rows):
    intervals = sorted(float(r['interval_ms']) for r in rows)
    work = sorted(float(r['work_ms']) for r in rows)
    result = {'frames': len(rows), 'interval_p50_ms': statistics.median(intervals),
            'interval_p95_ms': intervals[math.ceil(len(intervals)*.95)-1],
            'work_p50_ms': statistics.median(work),
            'work_p95_ms': work[math.ceil(len(work)*.95)-1]}
    phases = ('host_guest', 'present', 'capture', 'audio', 'pace')
    if any(name+'_ms' in row for row in rows for name in phases):
        for row in rows:
            if not all(row.get(name+'_ms') not in (None, '') for name in phases):
                raise ValueError('Incomplete phase timing capture')
            values = [float(row[name+'_ms']) for name in phases]
            work_ms, interval_ms = float(row['work_ms']), float(row['interval_ms'])
            if not all(math.isfinite(v) and v >= 0 for v in [*values, work_ms, interval_ms]):
                raise ValueError('Invalid phase timing value')
            if (abs(sum(values[:-1])-work_ms) > .00001 or
                    abs(sum(values)-interval_ms) > .00001):
                raise ValueError('Phase timings do not partition the recorded frame')
        result['phase_ms'] = {}
        for name in phases:
            values = sorted(float(row[name+'_ms']) for row in rows)
            result['phase_ms'][name] = {'p50': statistics.median(values),
                                       'p95': values[math.ceil(len(values)*.95)-1]}
    audio_columns = ('audio_underruns', 'audio_underruns_delta', 'audio_backpressure_ms')
    if any(name in row for row in rows for name in audio_columns):
        if not all(row.get(name) not in (None, '') for row in rows for name in audio_columns):
            raise ValueError('Incomplete audio event capture')
        if 'phase_ms' not in result:
            raise ValueError('Audio events require complete phase timing capture')
        previous = None
        events, observed, backpressure = [], 0, 0.0
        for i, row in enumerate(rows):
            try:
                frame, total, delta = (int(row[name]) for name in
                                       ('frame', 'audio_underruns', 'audio_underruns_delta'))
            except (KeyError, TypeError, ValueError):
                raise ValueError('Invalid audio event counter or frame') from None
            if frame < 1 or total < 0 or delta < 0 or delta > total:
                raise ValueError('Invalid audio event counter or frame')
            if previous:
                old_frame, old_total = previous
                increase = total-old_total
                if frame <= old_frame or increase < delta or (frame == old_frame+1 and increase != delta):
                    raise ValueError('Incoherent audio event counter/delta')
            wait = float(row['audio_backpressure_ms'])
            if not math.isfinite(wait) or wait < 0 or wait > float(row['audio_ms'])+.00001:
                raise ValueError('Invalid audio backpressure duration')
            previous = frame, total
            observed += delta
            backpressure += wait
            if delta:
                events.append({'frame': frame, 'cumulative': total, 'delta': delta,
                               'neighbors': [r for r in rows[max(0, i-1):i+2]
                                             if abs(int(r['frame'])-frame) <= 1]})
        result.update(audio_queue_zero_count=observed, audio_queue_zero_events=events,
                      audio_backpressure_ms=backpressure)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--audio-driver', choices=('dummy', 'pulseaudio'),
                   help='Recorded SDL backend; omit when unknown')
    a = p.parse_args()
    with (a.directory/'frames.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    stats = json.loads((a.directory/'run.json').read_text())
    assert [int(r['frame']) for r in rows] == list(range(1, stats['frames']+1)), 'Missing frame samples'
    assert all(0 <= float(r['work_ms']) <= float(r['interval_ms']) + .000001 for r in rows)
    assert abs(sum(float(r['interval_ms']) for r in rows)/1000-stats['elapsed_seconds']) < .25
    race = [r for r in rows if 2800 <= int(r['frame']) < 17100 or 22900 <= int(r['frame']) < 34500]
    whole = summary(rows)
    if 'audio_queue_zero_count' in whole and (whole['audio_queue_zero_count'] != stats['audio_underruns'] or
                                             int(rows[-1]['audio_underruns']) != stats['audio_underruns']):
        raise ValueError('Full-route audio event totals disagree with run stats')
    result = {'target_fps': 16777216/280896, 'target_interval_ms': 280896/16777216*1000,
              'elapsed_seconds': stats['elapsed_seconds'], 'actual_fps': stats['frames']/stats['elapsed_seconds'],
              'whole_route': whole, 'race_sections': summary(race) if race else None,
              'audio_underruns': stats['audio_underruns'], 'audio_max_queue_ms': stats['audio_max_queue_ms'],
              'audio_driver': a.audio_driver or 'unknown',
              'dummy_audio': a.audio_driver == 'dummy' if a.audio_driver else None,
              'headless_software_output': '960x640'}
    if a.output:
        a.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
