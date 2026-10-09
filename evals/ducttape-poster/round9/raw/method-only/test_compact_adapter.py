"""Synthetic in-memory metadata only; no images, cases, jobs, or CLI provenance produced."""
import copy
import hashlib
import importlib.util
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
import compact_critic_adapter as adapter

FROZEN = Path('/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round8/summarize.py')
spec = importlib.util.spec_from_file_location('frozen_summary_read_only', FROZEN)
v4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v4)


def fixture():
    packet = {'case_id': 'SYNTHETIC-METADATA-ONLY', 'wave': 'synthetic', 'expected_count': 5,
              'normalization': adapter.NORMALIZATION, 'critic_profiles': ['A', 'B', 'C'],
              'requirements': {'style': 'synthetic literal style', 'ratio': [16, 9], 'no_type_only': True},
              'copy': [{'text': '가 나·다', 'kind': 'text', 'fixed_newlines': False},
                       {'text': 'https://example.invalid/a/b', 'kind': 'url', 'fixed_newlines': False},
                       {'text': '첫 줄\n둘째 줄', 'kind': 'text', 'fixed_newlines': True}],
              'images': [], 'source_assets': [], 'protected_layouts': []}
    raw = {'schema_version': 1, 'kind': 'compact_critic_observations', 'case_id': packet['case_id'],
           'wave': packet['wave'], 'profile': 'A', 'session_id': None,
           'procedure': {'fresh_session': True, 'all_views_before_scoring': True, 'order_compliant': True,
                         'method': 'SYNTHETIC declaration only; no assets exist and no viewing occurred in this test.',
                         'source_assets_viewed': [], 'protected_layouts_read': []}, 'viewed': [], 'images': {}}
    for i in range(5):
        iid = f'SYNTHETIC-{i}'
        views = {name: {'path': f'/synthetic-does-not-exist/{iid}/{name}.png', 'sha256': '0' * 64,
                        'width': size[0], 'height': size[1]}
                 for name, size in zip(adapter.VIEWS, [(1600, 900), (720, 405), (320, 180)])}
        packet['images'].append({'image_id': iid, 'role': iid, 'stage': 'initial', 'views': views,
                                 'ratio_requirement': [16, 9], 'style_requirement': 'synthetic per-image style'})
        raw['viewed'] += [{'image_id': iid, 'view': name, 'path': row['path'], 'sha256': row['sha256'], 'viewed': True}
                         for name, row in views.items()]
        ev = [['native', 'synthetic upper-left region', 'Synthetic schema evidence; not an observation of any image.']]
        raw['images'][iid] = {'copy': [{'raw': text, 'layout': {'status': 'PASS', 'observations': 'Synthetic layout metadata.'},
                                        'ambiguity': None, 'revisit': None}
                                       for text in ['가 나 · 다', 'https://example.invalid/a/b', '첫 줄\n둘째 줄']],
                             'mandatory': {'text': {'status': 'PASS', 'issues': []},
                                           'style': {'status': 'PASS', 'evidence': copy.deepcopy(ev), 'issues': []},
                                           'ratio': {'status': 'PASS', 'issues': []},
                                           'no_type_only': {'status': 'PASS', 'evidence': copy.deepcopy(ev), 'issues': []},
                                           'substantive_visual': {'status': 'PASS', 'evidence': copy.deepcopy(ev), 'issues': []}},
                             'ratings': {d: {'score': 4, 'evidence': copy.deepcopy(ev)} for d in adapter.DIMENSIONS},
                             'source_fidelity': [], 'residuals': []}
    ids = list(raw['images'])
    raw['set'] = {'members': ids, 'count_fidelity': {'status': 'PASS', 'observed_count': 5, 'issues': []},
                  'diversity': 4, 'evidence': [[iid, 'thumbnail320', 'synthetic full composition', 'Synthetic relationship metadata.'] for iid in ids],
                  'residuals': []}
    return packet, raw


class AdapterTest(unittest.TestCase):
    def test_frozen_source_identity(self):
        self.assertEqual(hashlib.sha256(FROZEN.read_bytes()).hexdigest(), adapter.SUMMARY_SHA256)

    def test_normalization_matches_frozen(self):
        strings = ['가 나 · 다', '가나·다', 'a / b', 'a/b', 'https://example.invalid/a/b',
                   'https: / / example.invalid/a/b', '첫 줄\r\n둘째 줄', '  첫  줄\n 둘째 줄 ', '\u1100\u1161 나·다', '']
        for kind in ('text', 'url'):
            for fixed in (False, True):
                for raw in strings:
                    entry = {'text': 'synthetic', 'kind': kind, 'fixed_newlines': fixed}
                    self.assertEqual(adapter.normalize(raw, entry), v4.normalize(raw, entry))

    def test_landscape_complete_schema_and_raw_immutability(self):
        packet, raw = fixture()
        before = copy.deepcopy(raw)
        result = adapter.export(packet, raw)
        self.assertEqual(raw, before)
        self.assertEqual(len(result['viewed']), 15)
        self.assertEqual(sum(len(i['scores']) for i in result['images'].values()), 35)
        for image in packet['images']:
            row = result['images'][image['image_id']]
            check = v4.image_record(row, image, 'A', packet, {'views': image['views']})
            self.assertEqual(check['errors'], [])
            self.assertEqual(row['mandatory']['ratio']['observed_dimensions'], [1600, 900])
        self.assertEqual(result['images']['SYNTHETIC-0']['mandatory']['text']['transcriptions'][0]['raw_observed'], '가 나 · 다')
        self.assertIn('가 나 · 다', adapter.markdown(result))

    def test_low_score_and_copy_error_are_not_rewritten(self):
        packet, raw = fixture()
        row = raw['images']['SYNTHETIC-0']
        row['ratings']['space']['score'] = 2
        row['copy'][0]['raw'] = '가나·다'
        row['mandatory']['text']['status'] = 'FAIL'
        result = adapter.export(packet, raw)['images']['SYNTHETIC-0']
        self.assertEqual(result['scores']['space'], 2)
        self.assertFalse(result['mandatory']['text']['transcriptions'][0]['equal'])
        self.assertEqual(v4.image_record(result, packet['images'][0], 'A', packet, {'views': packet['images'][0]['views']})['gate'], 'FAIL')

    def test_revisit_preserves_first_read(self):
        packet, raw = fixture()
        reading = raw['images']['SYNTHETIC-0']['copy'][0]
        reading.update(raw='가 나?다', ambiguity='Synthetic uncertain punctuation')
        target = packet['images'][0]['views']['native']
        reading['revisit'] = {'view': 'native', 'path': target['path'], 'sha256': target['sha256'],
                              'raw_observed': '가 나·다', 'resolved': True, 'reason': 'One synthetic revisit.',
                              'resolution': 'Synthetic punctuation resolution.'}
        record = adapter.export(packet, raw)['images']['SYNTHETIC-0']
        self.assertEqual(record['mandatory']['text']['transcriptions'][0]['raw_observed'], '가 나?다')
        self.assertTrue(record['mandatory']['text']['transcriptions'][0]['equal'])
        self.assertEqual(v4.image_record(record, packet['images'][0], 'A', packet, {'views': packet['images'][0]['views']})['errors'], [])

    def test_unresolved_ambiguity_and_null_score_remain_na(self):
        packet, raw = fixture()
        row = raw['images']['SYNTHETIC-0']
        row['copy'][0]['ambiguity'] = 'Synthetic unresolved glyph.'
        row['mandatory']['text']['status'] = 'NA'
        row['ratings']['ai_slop'].update(score=None, reason='Synthetic unavailable native detail.')
        result = adapter.export(packet, raw)['images']['SYNTHETIC-0']
        self.assertIsNone(result['scores']['ai_slop'])
        self.assertEqual(result['mandatory']['text']['status'], 'NA')
        self.assertEqual(v4.image_record(result, packet['images'][0], 'A', packet, {'views': packet['images'][0]['views']})['gate'], 'NA')

    def test_missing_read_score_view_or_member_is_rejected(self):
        for mutation in (lambda r: r['images']['SYNTHETIC-0']['copy'][0].pop('raw'),
                         lambda r: r['images']['SYNTHETIC-0']['ratings'].pop('space'),
                         lambda r: r['viewed'].pop(), lambda r: r['images'].pop('SYNTHETIC-4'),
                         lambda r: r['images']['SYNTHETIC-0']['ratings']['space'].update(score=True),
                         lambda r: r['set']['evidence'].pop()):
            packet, raw = fixture()
            mutation(raw)
            with self.assertRaises(ValueError):
                adapter.export(packet, raw)

    def test_unknown_view_path_is_preserved_and_invalidates_order(self):
        packet, raw = fixture()
        raw['viewed'][0]['path'] = '/unknown-raw-path.png'
        result = adapter.export(packet, raw)
        self.assertEqual(result['viewed'][0]['path'], '/unknown-raw-path.png')
        self.assertFalse(result['procedure']['order_compliant'])
        self.assertTrue(result['procedure']['adapter_binding_errors'])

    def test_unavailable_source_geometry_cannot_pass(self):
        packet, raw = fixture()
        packet['source_assets'] = [{'asset_id': 'SYNTHETIC-SOURCE', 'actual_path': '/synthetic-source.png', 'sha256': '1' * 64}]
        manifest = {'path': '/synthetic-layout.json', 'sha256': '2' * 64}
        packet['protected_layouts'] = [{'asset_id': 'SYNTHETIC-SOURCE', 'manifest': manifest}]
        raw['procedure']['source_assets_viewed'] = [{'asset_id': 'SYNTHETIC-SOURCE', 'path': '/unknown-source.png', 'sha256': '1' * 64,
                                                    'viewed': False, 'reason': 'Synthetic unavailable source.'}]
        raw['procedure']['protected_layouts_read'] = [{'manifest': manifest, 'read': False, 'reason': 'Synthetic unavailable geometry.'}]
        for row in raw['images'].values():
            row['mandatory']['style']['status'] = 'NA'
            row['source_fidelity'] = [{'asset_id': 'SYNTHETIC-SOURCE', 'status': 'NA', 'observations': 'Identity/protected geometry unavailable.'}]
        result = adapter.export(packet, raw)
        self.assertEqual(result['images']['SYNTHETIC-0']['mandatory']['style']['status'], 'NA')
        raw['images']['SYNTHETIC-0']['source_fidelity'][0]['status'] = 'PASS'
        with self.assertRaises(ValueError):
            adapter.export(packet, raw)


if __name__ == '__main__':
    unittest.main()
