"""Replay attributed squeeze identifiers without admitting readings or object joins."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://ig.bbaw.de/de/abklatsche/ig-xv-cyprus'
SNAPSHOT = 'research/bbaw-squeeze-identifier-snapshot.json'
OUTPUT = 'research/geographic-expansion-register.json'


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


class IdentifierParser(HTMLParser):
    """Read only the legacy syllabic section, stopping before alphabetic material."""
    def __init__(self):
        super().__init__()
        self.capture = None
        self.parts = []
        self.active = False
        self.section_seen = 0
        self.region = None
        self.site = None
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag in {'h2', 'h3', 'h4'} or (tag == 'li' and self.active):
            if self.capture is not None:
                raise ValueError('nested identifier/heading markup')
            self.capture, self.parts = tag, []

    def handle_data(self, data):
        if self.capture:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag != self.capture:
            return
        text = ' '.join(''.join(self.parts).split())
        self.capture = None
        if tag == 'h2':
            self.active = text == 'Tituli syllabici'
            if self.active:
                self.section_seen += 1
            self.region = self.site = None
        elif self.active and tag == 'h3':
            self.region, self.site = text, None
        elif self.active and tag == 'h4':
            self.site = text
        elif self.active and tag == 'li':
            if not self.region or not text:
                raise ValueError('identifier lacks geographic heading')
            self.rows.append({'region_as_supplied': self.region,
                              'site_as_supplied': self.site,
                              'reference_as_supplied': text})


def extract(raw):
    parser = IdentifierParser()
    parser.feed(raw.decode('utf-8'))
    if parser.section_seen != 1 or not parser.rows:
        raise ValueError('syllabic section missing or ambiguous')
    return parser.rows


def construct(snapshot):
    if snapshot['source_url'] != SOURCE:
        raise ValueError('unapproved source')
    if len(snapshot['response_sha256']) != 64 or any(c not in '0123456789abcdef' for c in snapshot['response_sha256']):
        raise ValueError('invalid response receipt')
    rows = snapshot['rows']
    seen = set()
    records = []
    for row in rows:
        if set(row) != {'region_as_supplied', 'site_as_supplied', 'reference_as_supplied'}:
            raise ValueError('snapshot field leakage')
        if not all(isinstance(row[k], str) and row[k].strip() for k in ('region_as_supplied', 'reference_as_supplied')) or (row['site_as_supplied'] is not None and (not isinstance(row['site_as_supplied'], str) or not row['site_as_supplied'].strip())):
            raise ValueError('missing identifier context')
        key = tuple(row[k] for k in sorted(row))
        if key in seen:
            raise ValueError('duplicate source catalogue row')
        seen.add(key)
        identity = hashlib.sha256(encode([row[k] for k in sorted(row)]).encode()).hexdigest()[:20]
        records.append({'id': 'BBAW-SQUEEZE-' + identity, **row,
                        'source_url': SOURCE, 'source_response_sha256': snapshot['response_sha256'],
                        'source_row_index': len(records), 'unit': 'SOURCE_CATALOGUE_IDENTIFIER',
                        'source_section': 'Tituli syllabici',
                        'language': 'UNADJUDICATED', 'reading_admitted': False,
                        'physical_object_count': None, 'independent_witness': False,
                        'ig_xv1_object_join': 'UNRESOLVED',
                        'components_and_casts': 'RETAIN_LABEL; DO_NOT_SPLIT_OR_MERGE',
                        'rights': 'PROJECT_AUTHORED_FACTUAL_IDENTIFIER_REGISTER; NO_IMAGES_OR_TRANSCRIPTIONS'})
    if len(rows) != snapshot['identifier_rows']:
        raise ValueError('source denominator drift')
    return {'schema_version': '1.0', 'source_url': SOURCE,
            'observed_at': snapshot['observed_at'], 'snapshot_sha256': hashlib.sha256(encode(snapshot).encode()).hexdigest(),
            'records': records, 'summary': {'source_identifier_rows': len(records),
                'sites': dict(Counter(r['site_as_supplied'] or 'UNKNOWN' for r in records)),
                'admitted_new_readings': 0, 'unique_physical_objects': None},
            'boundary': 'A squeeze catalogue identifier is neither a reading nor a unique ancient object. Greek-language membership and IG/ICS/object concordances require evidence. Casts, fragments, ranges and AB labels remain intact. This snapshot is not exhaustive discovery.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    content = encode(construct(json.loads((ROOT / SNAPSHOT).read_text())))
    if args.write:
        (ROOT / OUTPUT).write_text(content)
    elif (ROOT / OUTPUT).read_text() != content:
        raise ValueError('expansion register stale')
    print('Source-attributed expansion identifier replay PASS; no reading admission')


if __name__ == '__main__':
    main()
