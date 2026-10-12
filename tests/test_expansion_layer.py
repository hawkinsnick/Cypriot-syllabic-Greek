import importlib.util
import pathlib
import unittest

P = pathlib.Path(__file__).resolve().parents[1] / 'scripts/build_expansion_layer.py'
spec = importlib.util.spec_from_file_location('expansion', P)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ExpansionTests(unittest.TestCase):
    def test_section_boundary_and_casts(self):
        raw = b'<h2>IG XV 1, 1</h2><li>exclude</li><h2>Tituli syllabici</h2><h3>Paphus et vicinia</h3><h4>Idalium</h4><ul><li>ICS n. 217 ectt. gypsina: AB</li></ul><h2>Tituli alphabetici</h2><li>exclude</li>'
        rows = m.extract(raw)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['reference_as_supplied'], 'ICS n. 217 ectt. gypsina: AB')
        snap = dict(source_url=m.SOURCE, response_sha256='a'*64, observed_at='2026-10-12T00:00:00Z', identifier_rows=1, rows=rows)
        r = m.construct(snap)['records'][0]
        self.assertFalse(r['reading_admitted'])
        self.assertIsNone(r['physical_object_count'])

    def test_missing_heading(self):
        with self.assertRaises(ValueError):
            m.extract(b'<h2>Tituli syllabici</h2><li>ICS 17</li>')

    def test_ambiguous_section(self):
        with self.assertRaises(ValueError):
            m.extract(b'<h2>Tituli syllabici</h2><h2>Tituli syllabici</h2>')

    def test_duplicate_and_linguistic_leakage(self):
        row = dict(region_as_supplied='Paphus', site_as_supplied='Rantidi', reference_as_supplied='Meister n. 1 AB')
        snap = dict(source_url=m.SOURCE, response_sha256='a'*64, observed_at='now', identifier_rows=2, rows=[row, row])
        with self.assertRaises(ValueError):
            m.construct(snap)
        snap.update(rows=[dict(row, reading='invented')], identifier_rows=1)
        with self.assertRaises(ValueError):
            m.construct(snap)

    def test_bad_source_and_denominator(self):
        snap = dict(source_url='https://example.org', response_sha256='a'*64, observed_at='now', identifier_rows=0, rows=[])
        with self.assertRaises(ValueError):
            m.construct(snap)
        snap.update(source_url=m.SOURCE, identifier_rows=2)
        with self.assertRaises(ValueError):
            m.construct(snap)
