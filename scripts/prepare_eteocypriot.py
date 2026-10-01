"""Generate a source-linked acquisition ledger for the Eteocypriot project."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from csg.core import ROOT, read_json, sha256, validate, write_json

def main():
    errors = validate()
    if errors:
        raise ValueError(errors)
    rows = []
    for record in read_json(ROOT / 'data/records.json'):
        if record['language']['code'] not in {'eteocypriot', 'uncertain'}:
            continue
        source = record['source']
        rows.append({
            'candidate_id': record['id'].replace('CSG-', 'ETEC-'),
            'shared_source_identity': {'authority': source['authority'], 'source_id': record['source_id']},
            'source_title': record['title'],
            'admission_status': 'source_labelled_candidate' if record['language']['code'] == 'eteocypriot' else 'uncertain_candidate',
            'classification_basis': 'Whole-entry source title; component-level language assignment pending',
            'record_unit': 'digital_edition_entry',
            'source_url': source['url'], 'source_xml_url': source['xml_url'],
            'snapshot_reference': 'https://github.com/hawkinsnick/Cypriot-syllabic-Greek/blob/e3d9e027e9c61e742e4a82fee07e2266595e6a69/' + source['raw_path'],
            'raw_sha256': source['sha256'], 'license': source['license'],
            'source_parts': [{'n': p['n'], 'subtype': p['subtype'], 'language_assignment': None} for p in record['edition']['parts']],
            'object_id': None, 'independent_witness_id': None,
            'analysis_eligible': False,
            'independent_epigraphic_review': False,
        })
    acquisition = read_json(ROOT / 'data/acquisition.json')
    for defect in read_json(ROOT / 'data/source-defects.json'):
        row = next(r for r in acquisition if r['id'] == defect['id'])
        if sha256(ROOT / row['path']) != defect['sha256']:
            raise ValueError('Quarantined source hash mismatch')
        rows.append({
            'candidate_id': 'ETEC-IGXV1-' + defect['id'].removeprefix('IG XV 1, '),
            'shared_source_identity': {'authority': 'Inscriptiones Graecae, BBAW / TELOTA', 'source_id': defect['id']},
            'admission_status': 'quarantined_mixed_language_candidate',
            'classification_basis': 'Source header title and documented malformed body; no parsed component assignment',
            'record_unit': 'digital_edition_entry',
            'source_xml_url': row['url'],
            'snapshot_reference': 'https://github.com/hawkinsnick/Cypriot-syllabic-Greek/blob/e3d9e027e9c61e742e4a82fee07e2266595e6a69/' + row['path'],
            'raw_sha256': defect['sha256'], 'license': row['license'],
            'parse_error': defect['parse_error'],
            'object_id': None, 'independent_witness_id': None,
            'analysis_eligible': False, 'independent_epigraphic_review': False,
        })
    if len({r['candidate_id'] for r in rows}) != len(rows):
        raise ValueError('Duplicate candidate IDs')
    report = {
        'stage': '0.1 acquisition preparation, not an Eteocypriot corpus release',
        'source_snapshot_commit': 'e3d9e027e9c61e742e4a82fee07e2266595e6a69',
        'scope': 'Eteocypriot-labelled and uncertain entries in the frozen IG XV 1 snapshot only',
        'candidate_entries': len(rows),
        'source_labelled_entries': sum(r['admission_status'] == 'source_labelled_candidate' for r in rows),
        'uncertain_entries': sum(r['admission_status'] == 'uncertain_candidate' for r in rows),
        'quarantined_entries': sum(r['admission_status'] == 'quarantined_mixed_language_candidate' for r in rows),
        'component_language_assignments_verified': 0,
        'whole_corpus_coverage': None,
        'cross_project_identity_rule': 'The same authority/source_id in two projects is the same source entry, not an independent witness.',
        'candidates': rows,
    }
    write_json(ROOT / 'research/eteocypriot/candidates.json', report)
    print(f'Prepared {len(rows)} source-linked candidates; no analytical admission claimed.')

if __name__ == '__main__':
    main()
