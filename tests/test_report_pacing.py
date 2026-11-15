import importlib.util
import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('report_pacing', Path(__file__).parents[1]/'tools/report_pacing.py')
pacing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pacing)

class PhaseTimings(unittest.TestCase):
    def rows(self):
        return [dict(interval_ms='16.7', work_ms='12', host_guest_ms='2', present_ms='1',
                     capture_ms='1', audio_ms='8', pace_ms='4.7'),
                dict(interval_ms='18', work_ms='16', host_guest_ms='4', present_ms='2',
                     capture_ms='0', audio_ms='10', pace_ms='2')]

    def test_legacy_recordings_remain_unattributed(self):
        result = pacing.summary([dict(interval_ms='16.7',work_ms='12')])
        self.assertNotIn('phase_ms', result)
        self.assertEqual(result['frames'], 1)
        self.assertEqual(result['work_p95_ms'], 12)

    def test_each_phase_is_reported_separately(self):
        result = pacing.summary(self.rows())
        self.assertEqual(result['phase_ms']['audio'], {'p50': 9, 'p95': 10})
        self.assertEqual(result['phase_ms']['host_guest'], {'p50': 3, 'p95': 4})
        self.assertAlmostEqual(result['phase_ms']['pace']['p50'], 3.35)

    def test_partial_phase_capture_is_rejected(self):
        rows = self.rows()
        del rows[1]['audio_ms']
        with self.assertRaisesRegex(ValueError, 'Incomplete phase'):
            pacing.summary(rows)

    def test_nonfinite_totals_are_rejected(self):
        for field in ['work_ms', 'interval_ms']:
            with self.subTest(field=field):
                rows = self.rows()
                rows[0][field] = 'nan'
                with self.assertRaises(ValueError):
                    pacing.summary(rows)

    def test_negative_nonfinite_and_nonpartitioning_phases_are_rejected(self):
        for value in ['-1', 'nan', 'inf', '7']:
            with self.subTest(audio=value):
                rows = self.rows()
                rows[0]['audio_ms'] = value
                with self.assertRaises(ValueError):
                    pacing.summary(rows)


class AudioFrameEvents(unittest.TestCase):
    def rows(self):
        return [dict(row, frame=str(frame), audio_underruns=str(total),
                     audio_underruns_delta=str(delta), audio_backpressure_ms=str(wait))
                for row, frame, total, delta, wait in zip(
                    PhaseTimings().rows()*2, (2800, 2801, 22900, 22901),
                    (7, 8, 12, 12), (0, 1, 0, 0), (1, 2, 3, 4))]

    def test_old_eight_column_capture_has_no_invented_audio_events(self):
        result = pacing.summary([dict(row, frame=str(i+1))
                                 for i, row in enumerate(PhaseTimings().rows())])
        self.assertNotIn('audio_queue_zero_events', result)
        self.assertNotIn('audio_backpressure_ms', result)

    def test_partial_race_sections_report_only_observed_events_and_actual_neighbors(self):
        result = pacing.summary(self.rows())
        self.assertEqual(result['audio_queue_zero_count'], 1)
        self.assertEqual(result['audio_backpressure_ms'], 10)
        event, = result['audio_queue_zero_events']
        self.assertEqual((event['frame'], event['cumulative'], event['delta']), (2801, 8, 1))
        self.assertEqual([int(row['frame']) for row in event['neighbors']], [2800, 2801])
        self.assertEqual(event['neighbors'][1]['audio_ms'], '10')
        self.assertEqual(event['neighbors'][0]['host_guest_ms'], '2')

    def test_new_columns_are_all_or_none_and_require_phase_capture(self):
        for field in ('audio_underruns', 'audio_underruns_delta', 'audio_backpressure_ms'):
            for missing in ('one', 'all', 'blank'):
                with self.subTest(field=field, missing=missing):
                    rows = self.rows()
                    if missing == 'blank':
                        rows[1][field] = ''
                    else:
                        for row in rows if missing == 'all' else rows[:1]:
                            del row[field]
                    with self.assertRaisesRegex(ValueError, 'Incomplete audio event'):
                        pacing.summary(rows)
        rows = self.rows()
        for row in rows:
            for phase in ('host_guest', 'present', 'capture', 'audio', 'pace'):
                del row[phase+'_ms']
        with self.assertRaisesRegex(ValueError, 'require.*phase'):
            pacing.summary(rows)

    def test_counter_and_frame_values_must_be_nonnegative_integers_in_order(self):
        for field, value in [('audio_underruns', '-1'), ('audio_underruns', 'nan'),
                             ('audio_underruns_delta', '1.5'), ('audio_underruns_delta', '-1'),
                             ('frame', '0'), ('frame', '2800.5')]:
            with self.subTest(field=field, value=value):
                rows = self.rows()
                rows[0][field] = value
                with self.assertRaises(ValueError):
                    pacing.summary(rows)
        for frame in ('2800', '2799'):
            rows = self.rows()
            rows[1]['frame'] = frame
            with self.assertRaises(ValueError):
                pacing.summary(rows)

    def test_counter_monotonicity_and_consecutive_deltas_are_coherent(self):
        for index, field, value in [(1, 'audio_underruns', '6'),
                                    (2, 'audio_underruns', '7'),
                                    (1, 'audio_underruns_delta', '0'),
                                    (2, 'audio_underruns_delta', '5'),
                                    (0, 'audio_underruns_delta', '8')]:
            with self.subTest(index=index, field=field):
                rows = self.rows()
                rows[index][field] = value
                with self.assertRaises(ValueError):
                    pacing.summary(rows)

    def test_backpressure_is_finite_nonnegative_and_bounded_by_audio_phase(self):
        for value in ('-1', 'nan', 'inf', '8.01'):
            with self.subTest(value=value):
                rows = self.rows()
                rows[0]['audio_backpressure_ms'] = value
                with self.assertRaises(ValueError):
                    pacing.summary(rows)

    def cli(self, rows, total):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (root/'frames.csv').open('w') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            (root/'run.json').write_text(json.dumps(dict(
                frames=len(rows), elapsed_seconds=sum(float(r['interval_ms']) for r in rows)/1000,
                audio_underruns=total, audio_max_queue_ms=60)))
            output = io.StringIO()
            with patch('sys.argv', ['report_pacing.py', directory]), contextlib.redirect_stdout(output):
                pacing.main()
            return json.loads(output.getvalue())

    def full_rows(self):
        rows = self.rows()[:2]
        for i, row in enumerate(rows):
            row.update(frame=str(i+1), audio_underruns=str(i))
        return rows

    def test_full_route_cli_checks_stats_and_supports_a_short_reload_without_race_sections(self):
        result = self.cli(self.full_rows(), 1)
        self.assertEqual(result['whole_route']['audio_queue_zero_events'][0]['frame'], 2)
        self.assertIsNone(result['race_sections'])

    def test_full_route_cli_rejects_stats_disagreement_and_hidden_initial_events(self):
        with self.assertRaisesRegex(ValueError, 'audio event totals'):
            self.cli(self.full_rows(), 2)
        rows = self.full_rows()
        for row in rows:
            row['audio_underruns'] = str(int(row['audio_underruns'])+7)
        with self.assertRaisesRegex(ValueError, 'audio event totals'):
            self.cli(rows, 1)

if __name__ == '__main__':
    unittest.main()
