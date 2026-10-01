import copy
import json
from pathlib import Path
import tempfile
import unittest
import shutil

from csg.core import ROOT, classification, parse_record, read_json, render, signs, validate
from csg.__main__ import frequency, verify_export, create_exports
import xml.etree.ElementTree as ET

class ResearchSemantics(unittest.TestCase):
    def test_shared_script_does_not_establish_greek(self):
        self.assertFalse(classification('Graffito, syllabisch', [], 'a-na')['greek_analysis_eligible'])

    def test_bilingual_eteocypriot_not_greek_syllabic(self):
        c = classification('Weihinschrift, eteokyprisch und griechisch', [{'text': 'Greek'}], 'a-na')
        self.assertEqual(c['code'], 'eteocypriot')
        self.assertFalse(c['greek_analysis_eligible'])

    def test_uncertain_eteocypriot_is_not_promoted(self):
        self.assertEqual(classification('Graffito, eteokyprisch?', [], 'a-na')['code'], 'uncertain')

    def test_greek_interpretation_allows_scoped_admission(self):
        self.assertTrue(classification('Grabinschrift, syllabisch', [{'text': 'Greek'}], 'a-na')['greek_analysis_eligible'])

    def test_alphabetic_greek_not_admitted_as_syllabic(self):
        self.assertFalse(classification('Greek', [{'text': 'Greek'}], 'Ἀφροδίτη')['greek_analysis_eligible'])

    def test_empty_interpretation_is_not_admitted(self):
        self.assertFalse(classification('syllabisch', [{'text': ''}], 'a-na')['greek_analysis_eligible'])

    def test_inventory_holes_not_filled(self):
        inventory = signs()
        self.assertEqual(len(inventory), 55)
        self.assertNotIn('U+10806', {row['codepoint'] for row in inventory})

    def test_nested_parts_and_breaks_preserved(self):
        el = ET.fromstring('<div><div type="textpart" n="I"><lb n="1"/>a-na<lb n="2"/>sa</div><div type="textpart" n="II"><lb n="1"/>ko</div></div>')
        self.assertEqual(render(el), 'a-na\nsa\nko')

    def test_only_admitted_clear_tokens_contribute(self):
        def row(eligible, status, values):
            return {'language': {'greek_analysis_eligible': eligible}, 'edition': {'tokens': [{'status': status, 'values': values}]}}
        result = frequency([row(True, 'conservative_clear', ['a', 'na']), row(False, 'conservative_clear', ['ko']), row(True, 'excluded_editorial_or_unparsed', ['sa'])])
        self.assertEqual(result['counts'], {'a': 1, 'na': 1})
        self.assertEqual(result['contributing_entries'], 1)

class SnapshotIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = read_json(ROOT / 'data/records.json')
        cls.acquisition = read_json(ROOT / 'data/acquisition.json')

    def test_source_replay(self):
        self.assertEqual(validate(), [])

    def test_editorial_uncertainty_not_indexed(self):
        for row in self.records:
            for token in row['edition']['tokens']:
                self.assertEqual(row['edition']['text'][token['start']:token['end']], token['raw'])
                if token['status'] == 'conservative_clear':
                    self.assertNotIn('[', token['raw'])
                    self.assertNotIn(']', token['raw'])
                    self.assertNotIn('\u0323', token['raw'])

    def test_unknown_objects_not_fabricated(self):
        self.assertTrue(all(row['object_id'] is None and row['independent_witness_id'] is None for row in self.records))

    def test_tampered_source_identifier_rejected(self):
        row = copy.deepcopy(self.acquisition[0])
        row['id'] = 'WRONG'
        with self.assertRaises(ValueError):
            parse_record(ROOT / row['path'], row)

    def test_full_export_roundtrip_and_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'export'
            create_exports(self.records, path)
            self.assertEqual(read_json(path / 'corpus.json')['records'], self.records)
            self.assertEqual(verify_export(path), [])
            (path / 'catalogue.csv').write_text('tampered')
            self.assertTrue(verify_export(path))

    def test_unlisted_export_file_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'manifest.json').write_text('{"files": {}}')
            (path / 'extra.txt').write_text('extra')
            self.assertTrue(verify_export(path))

    def test_quarantine_is_counted_as_retrieved_not_parsed(self):
        defects = read_json(ROOT / 'data/source-defects.json')
        quarantined = [r for r in self.acquisition if r['status'] == 'quarantined']
        self.assertEqual({d['id'] for d in defects}, {r['id'] for r in quarantined})
        self.assertFalse({r['source_id'] for r in self.records} & {r['id'] for r in quarantined})

    def test_manifest_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'manifest.json').write_text('{"files": {"../outside.txt": "bad"}}')
            self.assertTrue(verify_export(path))

    def test_modified_record_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / 'data', root / 'data')
            rows = read_json(root / 'data/records.json')
            rows[0]['language']['greek_analysis_eligible'] = not rows[0]['language']['greek_analysis_eligible']
            (root / 'data/records.json').write_text(json.dumps(rows))
            self.assertIn('Records differ from deterministic source replay', validate(root))

    def test_modified_raw_source_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / 'data', root / 'data')
            row = self.acquisition[0]
            path = root / row['path']
            path.write_bytes(path.read_bytes() + b'\n')
            self.assertTrue(any('hash mismatch' in e for e in validate(root)))

    def test_truncated_frozen_index_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / 'data', root / 'data')
            index = read_json(root / 'data/source-index.json')
            (root / 'data/source-index.json').write_text(json.dumps(index[:-1]))
            self.assertIn('Frozen index differs from listing evidence', validate(root))

    def test_unregistered_quarantine_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / 'data', root / 'data')
            (root / 'data/source-defects.json').write_text('[]')
            self.assertTrue(any('Unregistered source quarantine' in e for e in validate(root)))

if __name__ == '__main__':
    unittest.main()
