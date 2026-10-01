"""Refresh the frozen BBAW index's XML, without silently swallowing failures."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def filename(identifier):
    return identifier.removeprefix('IG XV 1, ').replace('(', '_').replace(')', '') + '.xml'

def fetch(identifier):
    path = ROOT / 'data/raw/ig' / filename(identifier)
    url = 'https://telota.bbaw.de/ig/api/xml/' + urllib.parse.quote(identifier, safe='')
    error = None
    for attempt in range(3):
        try:
            if path.exists():
                raw = path.read_bytes()
            else:
                req = urllib.request.Request(url, headers={'User-Agent': 'Cypriot-syllabic-Greek/1.0 (research source snapshot)'})
                with urllib.request.urlopen(req, timeout=40) as response:
                    raw = response.read()
            # Validate identity/licence from the well-formed header even if the
            # source's edition/translation body contains a documented XML defect.
            parse_error = None
            try:
                root = ET.fromstring(raw)
            except ET.ParseError as exc:
                parse_error = str(exc)
                header_end = raw.index(b'</teiHeader>') + len(b'</teiHeader>')
                root = ET.fromstring(raw[:header_end] + b'</TEI>')
            ns = {'t': 'http://www.tei-c.org/ns/1.0'}
            if root.tag != '{http://www.tei-c.org/ns/1.0}TEI':
                raise ValueError('Not TEI XML')
            local = root.find('.//t:idno[@type="localId"]', ns)
            if local is None or (local.text or '').strip() != identifier:
                raise ValueError('Source identifier mismatch')
            licence = root.find('.//t:licence', ns)
            if licence is None or licence.get('target') != 'https://creativecommons.org/licenses/by/4.0/legalcode':
                raise ValueError('Unapproved source licence')
            path.write_bytes(raw)
            result = {'id': identifier, 'url': url, 'path': path.relative_to(ROOT).as_posix(),
                      'sha256': hashlib.sha256(raw).hexdigest(), 'status': 'quarantined' if parse_error else 'acquired',
                      'accessed': datetime.now(timezone.utc).date().isoformat(), 'license': 'CC-BY-4.0'}
            if parse_error:
                result['parse_error'] = parse_error
            return result
        except Exception as exc:
            error = str(exc)
            time.sleep(0.5 * (attempt + 1))
    return {'id': identifier, 'url': url, 'status': 'failed', 'error': error}

def main():
    ids = json.loads((ROOT / 'data/source-index.json').read_text())
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch, identifier): identifier for identifier in ids}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            if len(results) % 25 == 0:
                print(f'{len(results)}/{len(ids)} acquired={sum(x["status"] == "acquired" for x in results)}', flush=True)
    order = {identifier: i for i, identifier in enumerate(ids)}
    results.sort(key=lambda row: order[row['id']])
    (ROOT / 'data/acquisition.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    failures = sum(row['status'] == 'failed' for row in results)
    quarantined = sum(row['status'] == 'quarantined' for row in results)
    print(f'Finished: {len(results) - failures} retrieved; {quarantined} quarantined; {failures} failures', flush=True)
    return bool(failures)

if __name__ == '__main__':
    raise SystemExit(main())
