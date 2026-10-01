"""Dependency-free corpus commands. Run from a repository checkout."""
import argparse
from collections import Counter
import csv
import io
import json
from pathlib import Path
import shutil
import sys

from .core import ROOT, audit, build, read_json, sha256, validate, write_json

def frequency(records):
    counts = Counter()
    contributing = 0
    for record in records:
        if not record['language']['greek_analysis_eligible']:
            continue
        tokens = [token for token in record['edition']['tokens'] if token['status'] == 'conservative_clear']
        if tokens:
            contributing += 1
        counts.update(value for token in tokens for value in token['values'])
    return {'sampling_unit': 'digital_edition_entry', 'contributing_entries': contributing,
            'scope': 'Clear indexed signs in source-interpreted Greek entries only; editorial spans excluded conservatively. Not whole-corpus or object-deduplicated statistics.',
            'counts': dict(sorted(counts.items())), 'sign_tokens': sum(counts.values())}

def create_exports(records, output):
    output = Path(output)
    if output.resolve() == ROOT.resolve() or ROOT.resolve().is_relative_to(output.resolve()):
        raise ValueError('Export destination must not contain the repository')
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / 'corpus.json', {'version': (ROOT / 'VERSION').read_text().strip(), 'records': records})
    write_json(output / 'greek-subset.json', [r for r in records if r['language']['greek_analysis_eligible']])
    write_json(output / 'frequency.json', frequency(records))
    write_json(output / 'audit.json', audit(records, read_json(ROOT / 'data/acquisition.json'), read_json(ROOT / 'data/source-index.json')))
    write_json(output / 'signs.json', read_json(ROOT / 'data/signs.json'))
    with (output / 'catalogue.csv').open('w', encoding='utf-8', newline='') as handle:
        fields = ['id', 'source_id', 'language', 'greek_analysis_eligible', 'site', 'title', 'date_source', 'support', 'source_url', 'license']
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for r in records:
            writer.writerow({'id': r['id'], 'source_id': r['source_id'], 'language': r['language']['code'],
                             'greek_analysis_eligible': r['language']['greek_analysis_eligible'],
                             'site': r['site'], 'title': r['title'], 'date_source': r['date_source'],
                             'support': r['support'], 'source_url': r['source']['url'], 'license': r['source']['license']})
    # Original TEI is exported, with its licence and attribution, rather than invented EpiDoc.
    tei = output / 'tei'
    tei.mkdir(exist_ok=True)
    expected_xml = set()
    for r in records:
        name = r['id'] + '.xml'
        expected_xml.add(name)
        shutil.copyfile(ROOT / r['source']['raw_path'], tei / name)
    for path in tei.glob('*.xml'):
        if path.name not in expected_xml:
            path.unlink()
    write_json(output / 'source-defects.json', read_json(ROOT / 'data/source-defects.json'))
    for row in read_json(ROOT / 'data/acquisition.json'):
        if row['status'] == 'quarantined':
            target = output / 'quarantine' / Path(row['path']).name
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(ROOT / row['path'], target)
    (output / 'ATTRIBUTION.md').write_text((ROOT / 'NOTICE').read_text(), encoding='utf-8')
    paths = sorted(path for path in output.rglob('*') if path.is_file() and path.name != 'manifest.json')
    write_json(output / 'manifest.json', {'version': (ROOT / 'VERSION').read_text().strip(),
                                        'files': {path.relative_to(output).as_posix(): sha256(path) for path in paths}})

def verify_export(output):
    output = Path(output)
    errors = []
    try:
        manifest = read_json(output / 'manifest.json')
        expected = manifest['files']
        actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file() and p.name != 'manifest.json'}
        if actual != set(expected):
            errors.append('Export file membership differs from manifest')
        for name, digest in expected.items():
            path = (output / name).resolve()
            if not path.is_relative_to(output.resolve()) or not path.is_file():
                errors.append('Invalid manifest path: ' + name)
            elif sha256(path) != digest:
                errors.append('Export checksum mismatch: ' + name)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(str(exc))
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('build')
    sub.add_parser('validate')
    sub.add_parser('audit')
    sub.add_parser('frequency')
    search = sub.add_parser('search')
    search.add_argument('query')
    search.add_argument('--greek-only', action='store_true')
    export = sub.add_parser('export')
    export.add_argument('--output', default='exports')
    verify = sub.add_parser('verify-export')
    verify.add_argument('directory')
    args = parser.parse_args()
    if args.command == 'build':
        print(f'Built {len(build())} digital edition records.')
        return 0
    if args.command in {'validate', 'verify-export'}:
        errors = validate() if args.command == 'validate' else verify_export(args.directory)
        print(json.dumps({'valid': not errors, 'errors': errors}, ensure_ascii=False, indent=2))
        return int(bool(errors))
    # All analytical/export commands require deterministic replay to succeed first.
    errors = validate()
    if errors:
        print(json.dumps({'valid': False, 'errors': errors}, indent=2))
        return 1
    records = read_json(ROOT / 'data/records.json')
    if args.command == 'audit':
        result = audit(records, read_json(ROOT / 'data/acquisition.json'), read_json(ROOT / 'data/source-index.json'))
    elif args.command == 'frequency':
        result = frequency(records)
    elif args.command == 'search':
        result = [r for r in records if args.query.casefold() in json.dumps(r, ensure_ascii=False).casefold()
                  and (not args.greek_only or r['language']['greek_analysis_eligible'])]
    elif args.command == 'export':
        create_exports(records, args.output)
        print(f'Exported {len(records)} records to {args.output}')
        return 0
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
