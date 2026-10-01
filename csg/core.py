from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = {'t': 'http://www.tei-c.org/ns/1.0'}
XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'
LICENCE = 'https://creativecommons.org/licenses/by/4.0/legalcode'

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def signs():
    """Unicode names are interoperability labels, not a palaeographic signary."""
    rows = []
    for cp in range(0x10800, 0x10840):
        name = unicodedata.name(chr(cp), '')
        if name.startswith('CYPRIOT SYLLABLE '):
            rows.append({'id': f'Cprt-U{cp:05X}', 'codepoint': f'U+{cp:05X}',
                         'character': chr(cp), 'value': name.removeprefix('CYPRIOT SYLLABLE ').lower(),
                         'unicode_name': name, 'basis': 'Unicode Character Database',
                         'source': 'https://www.unicode.org/Public/14.0.0/ucd/UnicodeData.txt'})
    return rows

def local(tag):
    return tag.rsplit('}', 1)[-1]

def render(element):
    """Readable source view. Original XML remains authoritative for semantics."""
    if element is None:
        return ''
    pieces = []
    def visit(node):
        tag = local(node.tag)
        if tag == 'lb':
            pieces.append('\n')
        elif tag == 'div' and node.get('type') == 'textpart':
            pieces.append('\n')
        elif tag == 'gap':
            pieces.append('[gap]')
        if node.text:
            pieces.append(node.text)
        for child in node:
            visit(child)
            if child.tail:
                pieces.append(child.tail)
    visit(element)
    return '\n'.join(' '.join(line.split()) for line in ''.join(pieces).splitlines() if line.strip())

def text_at(root, xpath):
    element = root.find(xpath, NS)
    return ' '.join(''.join(element.itertext()).split()) if element is not None else None

def classification(title, interpretations, edition_text):
    """Do not infer language from site, script, readable sign values, or a German gloss."""
    title = title.lower()
    if 'eteokyprisch' in title:
        return {'code': 'uncertain' if 'eteokyprisch?' in title else 'eteocypriot',
                'status': 'source_label', 'basis': 'title', 'greek_analysis_eligible': False}
    has_syllabic = bool(re.search(r'\b(?:[a-z]{1,2}-)+[a-z]{1,2}\b', edition_text))
    if any(item.get('text', '').strip() for item in interpretations) and has_syllabic:
        return {'code': 'grc', 'status': 'source_interpretation',
                'basis': 'GRC interpretation supplied by BBAW for a syllabic edition',
                'greek_analysis_eligible': True}
    return {'code': 'und', 'status': 'unclassified',
            'basis': 'No unambiguous admitted Greek interpretation', 'greek_analysis_eligible': False}

def parse_record(path, acquisition):
    raw = path.read_bytes()
    root = ET.fromstring(raw)
    if root.tag != '{http://www.tei-c.org/ns/1.0}TEI':
        raise ValueError('Not a TEI document')
    identifier = text_at(root, './/t:idno[@type="localId"]')
    if identifier != acquisition['id']:
        raise ValueError('Source identifier mismatch')
    licence = root.find('.//t:licence', NS)
    if licence is None or licence.get('target') != LICENCE:
        raise ValueError('Unsupported source licence')
    title = text_at(root, './/t:title') or ''
    edition = root.find('.//t:div[@type="edition"]', NS)
    readable = render(edition)
    translations, interpretations = [], []
    for div in root.findall('.//t:div[@type="translation"]', NS):
        item = {'language': div.get(XML_LANG, '').lower(), 'responsibility': (div.get('resp') or '').strip() or None,
                'text': render(div), 'source_locator': 'div[@type="translation"]',
                'xml': ET.tostring(div, encoding='unicode')}
        (interpretations if item['language'] == 'grc' else translations).append(item)
    language = classification(title, interpretations, readable)
    # Whitespace spans remain tied to source display text, not reconstructed words.
    vocabulary = {row['value']: row['id'] for row in signs()}
    tokens = []
    for match in re.finditer(r'\S+', readable):
        raw_token = match.group()
        if re.search('[a-z]', raw_token) and not re.search('[\u0370-\u03ff\u1f00-\u1fff]', raw_token):
            candidate = raw_token[:-1] if raw_token.endswith(('.', ',', ';', ':')) else raw_token
            values = candidate.split('-')
            line_start = readable.rfind('\n', 0, match.start()) + 1
            line_end = readable.find('\n', match.end())
            source_line = readable[line_start:line_end if line_end != -1 else len(readable)]
            metadata_line = bool(re.search(r'\b(?:tit|linea|vacat|latus|supra|infra)\b', source_line))
            exact = bool(values) and all(v in vocabulary for v in values) and not metadata_line
            # Reject TEI editorial constructs even when flattened text looks clean.
            semantics = any(local(e.tag) in {'supplied', 'unclear', 'gap', 'choice', 'app', 'del', 'add'} for e in edition.iter()) if edition is not None else False
            tokens.append({'raw': raw_token, 'start': match.start(), 'end': match.end(),
                           'status': 'conservative_clear' if exact and not semantics else 'excluded_editorial_or_unparsed',
                           'values': values if exact and not semantics else [],
                           'sign_ids': [vocabulary[v] for v in values] if exact and not semantics else []})
    parts = []
    if edition is not None:
        for div in edition.findall('.//t:div[@type="textpart"]', NS):
            parts.append({'n': div.get('n'), 'subtype': div.get('subtype'), 'text': render(div)})
    directions = sorted(set(c for c in readable if c in '←→'))
    number = identifier.removeprefix('IG XV 1, ')
    return {
        'id': 'CSG-IGXV1-' + number.replace('(', '-').replace(')', ''),
        'source_id': identifier, 'record_unit': 'digital_edition_entry',
        'object_id': None, 'independent_witness_id': None,
        'script': 'Cprt', 'language': language, 'title': title,
        'site': text_at(root, './/t:origPlace'), 'date_source': text_at(root, './/t:origDate'),
        'date_normalized': None, 'support': text_at(root, './/t:support'),
        'provenance_source': text_at(root, './/t:provenance[@type="found"]'),
        'edition': {'representation': 'source_syllabic_transliteration_or_mixed_edition',
                    'text': readable, 'xml': ET.tostring(edition, encoding='unicode') if edition is not None else None,
                    'parts': parts, 'line_labels': [e.get('n') for e in edition.iter() if local(e.tag) == 'lb'] if edition is not None else [],
                    'direction_markers': directions, 'direction': 'not_normalized',
                    'tokens': tokens},
        'greek_interpretations': interpretations, 'translations': translations,
        'bibliography_source': text_at(root, './/t:div[@type="bibliography"]'),
        'source': {'authority': 'Inscriptiones Graecae, BBAW / TELOTA',
                   'url': 'https://telota.bbaw.de/ig/digitale-edition/inschrift/' + urllib.parse.quote(identifier, safe=''),
                   'xml_url': acquisition['url'], 'raw_path': acquisition['path'],
                   'sha256': hashlib.sha256(raw).hexdigest(), 'accessed': acquisition['accessed'],
                   'license': 'CC-BY-4.0', 'license_url': LICENCE,
                   'modifications': 'XML parsed into JSON; readable whitespace and part boundaries normalized; conservative token index added. Raw XML unchanged.'},
        'review': {'source_fidelity': 'automated_replay', 'independent_epigraphic_review': False},
    }

def build(root=ROOT):
    acquisition = read_json(root / 'data/acquisition.json')
    records = [parse_record(root / row['path'], row) for row in acquisition if row['status'] == 'acquired']
    write_json(root / 'data/records.json', records)
    write_json(root / 'data/signs.json', {'ucd_version': '14.0.0', 'repertoire_kind': 'Unicode_interoperability', 'signs': signs()})
    return records

def audit(records, acquisition, index):
    greek = [r for r in records if r['language']['greek_analysis_eligible']]
    return {'version': (ROOT / 'VERSION').read_text().strip(),
            'scope': 'Frozen IG XV 1 digital index; not the entire ancient corpus',
            'source_index_entries': len(index), 'acquired_entries': sum(r['status'] in {'acquired', 'quarantined'} for r in acquisition),
            'quarantined_entries': [r['id'] for r in acquisition if r['status'] == 'quarantined'],
            'failed_entries': [r['id'] for r in acquisition if r['status'] == 'failed'],
            'digital_edition_records': len(records), 'source_interpreted_greek_records': len(greek),
            'eteocypriot_labelled_records': sum(r['language']['code'] == 'eteocypriot' for r in records),
            'uncertain_language_records': sum(r['language']['code'] == 'uncertain' for r in records),
            'unclassified_records': sum(r['language']['code'] == 'und' for r in records),
            'greek_records_with_clear_tokens': sum(any(t['values'] for t in r['edition']['tokens']) for r in greek),
            'distinct_objects': None, 'independent_witnesses': None, 'whole_corpus_coverage_fraction': None,
            'independently_reviewed_records': 0,
            'gates': {'source_snapshot': ('READY_WITH_QUARANTINE' if any(r['status'] == 'quarantined' for r in acquisition) else 'READY') if not any(r['status'] == 'failed' for r in acquisition) else 'INCOMPLETE',
                      'source_interpreted_greek_subset': 'READY_SCOPED',
                      'whole_corpus_frequency': 'BLOCKED', 'linguistic_gold': 'BLOCKED',
                      'cross_script_phonetic_inference': 'BLOCKED', 'exhaustive_critical_edition': 'BLOCKED'}}

def validate(root=ROOT):
    errors = []
    try:
        index = read_json(root / 'data/source-index.json')
        acquisition = read_json(root / 'data/acquisition.json')
        records = read_json(root / 'data/records.json')
        inventory = read_json(root / 'data/signs.json')
        if len(index) != len(set(index)):
            errors.append('Duplicate index identifiers')
        evidence = read_json(root / 'data/listing-evidence.json')
        if len(index) != evidence['source_index_count'] or sha256(root / 'data/source-index.json') != evidence['source_index_sha256']:
            errors.append('Frozen index differs from listing evidence')
        if [r['id'] for r in acquisition] != index:
            errors.append('Acquisition ledger does not exactly reconcile with index')
        if len({r['id'] for r in records}) != len(records):
            errors.append('Duplicate record IDs')
        defects = read_json(root / 'data/source-defects.json')
        expected = []
        for row in acquisition:
            if row['status'] not in {'acquired', 'quarantined'}:
                errors.append('Source retrieval failed: ' + row['id'])
                continue
            path = root / row['path']
            if not path.resolve().is_relative_to((root / 'data/raw/ig').resolve()):
                errors.append('Unsafe source path: ' + row['id'])
                continue
            if sha256(path) != row['sha256']:
                errors.append('Raw source hash mismatch: ' + row['id'])
            if row['status'] == 'quarantined':
                defect = next((d for d in defects if d['id'] == row['id']), None)
                if defect is None or defect['sha256'] != row['sha256'] or defect['parse_error'] != row.get('parse_error'):
                    errors.append('Unregistered source quarantine: ' + row['id'])
                raw = path.read_bytes()
                try:
                    ET.fromstring(raw)
                    errors.append('Quarantined source unexpectedly well formed: ' + row['id'])
                except ET.ParseError as exc:
                    if str(exc) != row.get('parse_error'):
                        errors.append('Quarantine error mismatch: ' + row['id'])
                header_end = raw.index(b'</teiHeader>') + len(b'</teiHeader>')
                header = ET.fromstring(raw[:header_end] + b'</TEI>')
                licence = header.find('.//t:licence', NS)
                if text_at(header, './/t:idno[@type="localId"]') != row['id'] or licence is None or licence.get('target') != LICENCE:
                    errors.append('Quarantine identity/licence mismatch: ' + row['id'])
                continue
            expected.append(parse_record(path, row))
        if records != expected:
            errors.append('Records differ from deterministic source replay')
        if inventory != {'ucd_version': '14.0.0', 'repertoire_kind': 'Unicode_interoperability', 'signs': signs()}:
            errors.append('Unicode inventory mismatch')
        if len(inventory['signs']) != 55:
            errors.append('Unexpected Cypriot Unicode character count')
        unicode_evidence = read_json(root / 'data/unicode-evidence.json')
        if [{'codepoint': s['codepoint'], 'name': s['unicode_name']} for s in inventory['signs']] != unicode_evidence['characters']:
            errors.append('Inventory differs from pinned Unicode 14 source evidence')
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        errors.append(str(exc))
    return errors
