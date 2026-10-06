# Cypriot syllabic Greek research corpus

**Version 1.0.0 — attributed source snapshot and reproducible research toolkit.**

Built directly from BBAW / TELOTA's digital edition of *Inscriptiones Graecae*
XV 1. Original XML, source links, editorial uncertainty and classifications are
preserved. This is **not an exhaustive corpus of Cypriot syllabic Greek or an
independently reviewed critical edition**.

## AI research skill

This corpus project includes a vendor-neutral, evidence-first AI research skill in [`ai-skill/`](ai-skill/). The corpus remains the scholarly source of truth; the skill is an interface to it, not a second corpus and not an independent authority.

Researchers using ChatGPT, Claude, Gemini, or another capable model can provide the repository (or its AI-ready bundle) together with [`ai-skill/SKILL.md`](ai-skill/SKILL.md). The skill requires the model to preserve provenance, uncertainty, exclusions, source dependence, rights, and this project's scientific gates. Before substantive use, check [`ai-skill/generated/source-state.json`](ai-skill/generated/source-state.json) and the generated research-bundle index for the corpus commit represented by the AI package.

For questions spanning multiple corpus projects, use the **Combined Corpus Research AI** documented in the Linear A repository under [`combined-ai-skill/`](https://github.com/hawkinsnick/Linear-A/tree/ai-skill-v0.1/combined-ai-skill). It orchestrates the registered individual skills while keeping their evidence models and rights separate. Membership in the combined system does **not** imply linguistic relationship, sign equivalence, chronology, decipherment, or independent replication.

## Coverage

| Measure | 1.0.0 snapshot |
|---|---:|
| Digital source index entries | 593 |
| Source responses retrieved | 593 |
| Parsed digital edition records | 592 |
| Malformed source responses quarantined unchanged | 1 |
| Source-interpreted Greek records | 170 |
| Eteocypriot-labelled records outside the Greek subset | 18 |
| Uncertain-language records outside the Greek subset | 7 |
| Unclassified records outside the Greek subset | 397 |
| Unicode interoperability characters | 55 |
| Independently reviewed project records | 0 |

These are digital **entry** counts. Numbered subentries are not automatically
distinct objects or independent witnesses. Whole-corpus coverage is unknown.
The source index covers IG XV 1's advertised 1–410 catalogue range, with
parenthesized subentries; it does not include all Cypriot sites or all published
inscriptions. The Idalion tablet is outside this snapshot's scope.

IG XV 1, 150 has a malformed translation element in the original source XML.
Its response is retained unchanged in raw sources and export quarantine, with
an explicit defect report. It is excluded from parsed records and statistics.

## Download and use

Download the ZIP from [the 1.0.0 release](https://github.com/hawkinsnick/Cypriot-syllabic-Greek/releases/tag/v1.0.0)
and extract it. No Python installation is needed to read the JSON, CSV, XML or
documentation. Start with:

- [Greek subset](exports/greek-subset.json): admitted source-interpreted Greek entries.
- [Catalogue CSV](exports/catalogue.csv): searchable catalogue view.
- [Audit](exports/audit.json): coverage and research gates.
- [Method](docs/METHOD.md): admission, uncertainty and analytical limits.
- [Original source XML](data/raw/ig): unchanged source responses.

For commands, install Python 3.10 or later, open a terminal in the extracted
folder, then run the following. All normal commands work offline and require
no third-party Python packages.

```sh
python -m csg validate
python -m unittest discover -s tests -v
python -m csg audit
python -m csg search "Kurion" --greek-only
python -m csg frequency
python -m csg export --output my-snapshot
python -m csg verify-export my-snapshot
```

On Windows, `py` may replace `python`; on macOS/Linux, `python3` may replace it.
`python scripts/release_check.py` runs the release validation suite. To rebuild
derived records from saved XML, use `python -m csg build`. Online reacquisition
is an explicit maintenance task: `python scripts/acquire.py`. Changed source
responses require review and a new version; do not silently overwrite a release.

## Research controls

The Greek subset requires an attributed GRC interpretation and a syllabic
transliteration in the source. Eteocypriot labels override admission, including
bilingual records. Other entries remain unclassified. Greek alphabetic
interpretations, modern translations and ancient syllabic transliterations
remain distinct representations.

The frequency command describes only conservative clear tokens in the admitted
Greek subset: 1,341 sign tokens on 149 digital entries. It excludes damaged,
supplied, unparsed and metadata spans. These counts are not object-deduplicated
or representative of the whole ancient corpus. Passing software checks proves
structural/source fidelity, not epigraphic correctness or peer review.

## Attribution and reuse

Primary source: **Inscriptiones Graecae, Berlin-Brandenburg Academy of Sciences
and Humanities (BBAW), TELOTA digital edition**. Scholarly editors: **Artemis
Karnava and Massimo Perna, with Markus Egetmeyer (2020)**. Individual digital
translation responsibility is retained, including **Klaus Hallof** where supplied.

Raw XML and adapted IG edition content retain upstream **CC BY 4.0**, with links back to every original page. Current project-original software is **PolyForm Noncommercial 1.0.0** and project-owned documentation/annotations are **CC BY-NC 4.0**. Unicode data retain their own licence. See [NOTICE](NOTICE) and [LICENSE](LICENSE).
No museum images, plate drawings or printed-volume scans are bundled.

## Next milestones

Priority 2 is Eteocypriot, followed by source-pinned cross-references to the prior
corpus projects. This release follows their general separation of provenance,
rights, uncertainty, native sampling units and research gates. No cross-project
schema conformance or linguistic equivalence is claimed yet. See the
[roadmap](docs/ROADMAP.md) and [data model](docs/DATA_MODEL.md).


## Fleet admission

This corpus participates in the Combined Corpus Research AI fleet. Fleet admission requires the repository's component-specific licensing architecture, its individual `ai-skill` research contract and generated bundle, explicit master-registry membership, and passing member/master validation. Third-party material retains its upstream rights.


## Offline corpus browser
Run `python scripts/build_corpus_browser.py` to generate `workbench/corpus-browser.html`. It searches only files explicitly admitted by `research/browser-sources.json`. Browser admission requires rights/provenance review; never recursively ingest restricted or raw upstream material. Display does not establish decipherment, source independence, or expert validation.
