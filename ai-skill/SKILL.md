---
name: cypriot-syllabic-greek-research
description: Evidence-first AI research skill for the Cypriot syllabic Greek corpus.
version: 0.3.1
---

## Load and validate this repository-bound skill

Use this file as the canonical individual skill. Load the complete matching
repository checkout or give the AI access to its files; this Markdown file alone
contains instructions, not the corpus. Do not claim that supplying a GitHub URL
installs a skill or makes private/local files available to an AI platform.
Resolve the paths below from the repository root. With Python 3.10+ available,
run `python scripts/validate_ai_skill.py` before describing this skill as
operational on the supplied checkout. Read `docs/AI-SKILL-VALIDATION.md` for the
exact workflow, examples, dependencies, validation scope and limitations.
If execution or source access is unavailable, say which step was not run and
make no fresh validation claim. Preserve all native source/rights restrictions.

Discover exact IDs with `python scripts/evidence_query.py --coverage` and
`python scripts/evidence_query.py --list COLLECTION`. Retrieve evidence with
`python scripts/evidence_query.py --record ID --collection COLLECTION`;
use `python scripts/research_delivery.py --dossier ID --collection COLLECTION`
for its evidence-only answer frame. Return the exact source path/hash/pointer,
attribution, uncertainty and native evidence unit. A missing ID means absent
from the selected view; never invent a replacement or infer global absence.


# Cypriot syllabic Greek Research Skill

This skill is an interface to the corpus in this repository. The corpus remains the canonical source of truth. Never maintain an independent scholarly dataset inside the skill.

## Governing rules
1. Separate physical/epigraphic observation, source transcription, normalization, computational derivation, scholarly interpretation, and AI-derived analysis.
2. Prefer canonical machine-readable corpus records over prose summaries for record-level questions.
3. Preserve identifiers, provenance, uncertainty, disagreements, corrections, negative results, and superseded analyses.
4. Never invent missing signs, readings, restorations, provenience, bibliography, source independence, or rights.
5. Label calculations performed by the AI and state enough method for reproduction.
6. Respect record/source-specific licensing and attribution. Repository-level licensing must not erase upstream restrictions.
7. For cross-corpus claims, establish comparability and source independence before interpreting similarity.
8. Report blocked or missing evidence rather than filling gaps.

## Corpus-specific caution
Deciphered script used for Greek and related evidence: distinguish attested transcription from normalization, restoration, linguistic analysis, and cross-script comparison.

## Default research response
Give the direct answer, followed as relevant by Evidence; Evidentiary status; Uncertainty/limitations; Reproducibility; Rights/attribution.

## Synchronization
Read `ai-skill/generated/source-state.json` before substantive work. It records the corpus commit from which the AI-facing package was synchronized. Generated files are rebuildable views; canonical corpus files govern if a discrepancy is found.

## Academic-scrutiny gates
- Digital edition entries are not automatically distinct objects or independent witnesses
- The Greek subset is source-interpreted, not independent linguistic gold
- Whole-corpus frequency and cross-script phonetic inference remain blocked
- IG XV 1, 150 remains quarantined and excluded from parsed statistics
- Greek interpretation, syllabic transliteration and modern translation remain distinct


## Offline corpus browser
Run `python scripts/build_corpus_browser.py` to generate `workbench/corpus-browser.html`. It searches only files explicitly admitted by `research/browser-sources.json`. Browser admission requires rights/provenance review; never recursively ingest restricted or raw upstream material. Display does not establish decipherment, source independence, or expert validation.


## >9 collection gate
The current IG XV 1,1 layer has method-parity provenance, lineage, disagreement, rights, browser/API/export and validation controls. It does **not** yet represent the whole Cypriot syllabic Greek corpus: the official scholarly program extends through Paphos and other geographic fascicles. A >9 evidence-depth assessment therefore depends on broader authoritative coverage and object/edition concordance, not additional cosmetic engineering. See `docs/GT9-READINESS.md`.

## Enforced assertion, dependency and bundle integrity

Read `docs/AI-INTEGRITY.md` and the required `research/cross-corpus-dependencies.json` before source counts or cross-corpus analysis. Use qualified assertion views when provided; original source literals must travel with their reconciliation, uncertainty and identity context. The dependency register does not certify physical identity or linguistic affinity. Shared catalogue references and duplicated digital sources are not independent witnesses. Missing links mean unknown, not independent. `scripts/check_cross_corpus_dependencies.py` screens declared record selections and rejects pooled physical/witness counts and phonetic transfer. Native AI bundle validation checks the dependency projection and local evidence hashes. Bundle publication validates the exact source parent and never rebases or force-pushes the validated artifact. Software and packaging checks do not establish expert or model-behavior acceptance.

## Expanded evidence access

Use the geographic expansion register for squeeze catalogue discovery beyond IG XV 1. Keep its 210 source identifiers separate from parsed inscriptions and Greek subset statistics. Retain AB/fragment/cast labels and uncertain sites. Leave IG/object joins and Greek-language membership unresolved until source-supported; do not infer a reading from a catalogue heading.
Read `docs/GEOGRAPHIC-EXPANSION.md` for acquisition, scope and rights boundaries.

## Corpus-native evidence and alternatives

Read `docs/EVIDENCE-AND-ALTERNATIVES.md`, `research/evidence-query-profile.json` and `analysis/evidence-query-coverage.json` for evidence or competing-reading questions. Use `scripts/evidence_query.py` with exact native IDs and an explicit collection when ambiguous. Preserve `native_record`, every uncertainty/editorial mark, source attribution, locator, inspection status and rights. Cite artifact path, JSON pointer and SHA-256; hashes certify bytes only. Treat explicitly linked records as declared ID associations, not physical certification or independent witnesses. Context resources have corpus-level scope and are not automatically about the queried record. Distinguish a named source reading from a legacy queue label, uninspected bibliographic lead, count convention or hypothesis. Do not infer a count of collated alternative pairs or independent witnesses from searchable rows; those metrics remain unknown. Report the native units and scope of each view separately, and defer to the corpus-specific limits. No new readings, expert acceptance or decipherment follows from this interface.

## Bounded attribution review (2026-10-15)

Read `docs/ATTRIBUTION-REVIEW.md` and `research/attribution-review.json` before describing a dispute or source comparison. Run `python scripts/attribution_review.py --case ID` with the referenced evidence available. Preserve complete native evidence and distinguish reading, interpretation, classification, count, identity and representation questions. This checkpoint reviews pinned repository packets; it does not repeat their primary consultation or grant independent review. Inherit the exact author/publication, locator, consultation limits and dependence from each pointer; missing fields remain unknown. Use the case-specific remaining work. Do not count register entries or apparatus notes as fully attributed pairs, physical objects or independent witnesses.

All four controls distinguish language attribution, expected revisions without encoded pairs, coin units and fascicle coverage. Shared IG data remain dependent evidence.

## Research delivery, evidence answers and feedback

Read `docs/RESEARCH-DELIVERY.md` and verify `analysis/research-delivery.json`
with `python scripts/research_delivery.py --check` before using delivery claims.
Use `--dossier ID --collection COLLECTION` for exact evidence-bound answers;
preserve the complete native payload, citations, categories and limitations.
Use `--search TEXT` for source-record retrieval. Do not convert file pointers
into missing primary-edition citations, catalogue rows into unique objects,
source dependence into independent confirmation, or review forms into acceptance.
Prepare bounded review drafts with `--review-template`; validate submissions with
`--validate-review`, then require native human-maintainer acceptance. Treat delivery
and deterministic answer tests as engineering checks, not empirical LLM validation
or completion of scholarly/source-permission work. Local packaging grants no new
redistribution rights. Label any model-generated analysis separately and cite it.

## Combine Cypriot views without adding duplicate evidence

Read `docs/SOURCE-VIEW-UNION.md` before combining the broader Cypriot and Eteocypriot views. Their 25 shared source-entry IDs are the same digital-edition units, not independent witnesses. Use the master's frozen `scripts/prepare_source_union.py` only for its declared digital-entry source union; preserve both view-specific assertions under shared source-ID groups. It yields 592 groups from 617 incoming view rows and cannot supply Greek/Eteocypriot language frequencies, physical-object totals, sign equivalence or independent corroboration. Other corpus pairings and unit changes require separate admissible evidence.

## Preserve review provenance

Reject malformed JSON-pointer escapes and negative or leading-zero array indices
when verifying source citations; literal object keys retain their own spelling.
Read the [master hostile-review report](https://github.com/hawkinsnick/Master-Corpus-AI-Skill/blob/main/references/hostile-review-2026-10-25.md)
for this member's pinned retrieval scope and the limits of the source-fidelity
and development checks. Complete retrieval-view traversal does not certify
corpus completeness, accepted readings, independent witnesses or expert review.
