# Method and research limits

## Source and scope

The primary input is BBAW/TELOTA's IG XV 1 digital edition. Its public index,
retrieved on 2026-10-01, lists 593 entry identifiers in the advertised 1–410
range, including parenthesized subentries. The project uses the actual listed
identifiers, never a guessed numeric range. Index evidence and its retrieved
HTML checksum are in data/listing-evidence.json. Every retrieved XML is saved
unchanged, hashed, and checked for the requested identifier and source licence.
A transport failure is a failure, never an empty inscription or evidence that
an inscription does not exist. A retrieved but malformed response is preserved
unchanged in explicit quarantine. Its well-formed header establishes source
identity and licence; the documented body defect prevents parsed admission. Reacquisition is an explicit online operation;
all normal commands work offline against the frozen snapshot.

This digitizes a specific published digital resource, not all Cypriot syllabic
inscriptions. Important material outside this fascicle, including the Idalion
tablet, is not silently represented by an invented record. The primary source
describes its online texts/translations as supplements to the printed volumes:
https://ig.bbaw.de/de/uebersetzungen/texte
The digital edition does not replace consultation of the critical apparatus,
plates, physical objects or specialist assessment.

## Units and uncertainty

The native unit is a digital edition entry. Parenthetical entries may represent
subdivisions, fragments, instances or related material; no physical-object or
independent-witness equivalence is inferred. object_id and independent_witness_id
are null throughout this release. Counting entries never establishes a count of
independent ancient inscriptions. Date wording is preserved verbatim; normalized
dates are null because source notation has not been adjudicated.

Raw XML is authoritative. The JSON contains a serialized edition subtree and a
readable view that preserves arrows, visible editorial marks, line breaks and
text-part boundaries. The readable view is not a diplomatic rendering engine.
Line labels may repeat across source parts. Source direction markers are retained;
the software does not reverse text or assume the same direction for all entries.
No Cypriot Unicode strings are manufactured from syllabic transliterations.

## Greek subset admission

1. A title labelled eteokyprisch is excluded even if Greek appears elsewhere in
   the same source record. A Greek parallel in a bilingual does not make the
   Eteocypriot syllabic component Greek.
2. A title labelled eteokyprisch? remains uncertain and excluded.
3. Other records are admitted only if BBAW supplies a nonempty GRC-tagged
   interpretation and the edition has a multi-syllable Latin transliteration
   sequence. This is source-interpreted Greek, not independent project review.
4. Everything else is unclassified and excluded. This conservative policy can
   omit genuine Greek inscriptions, especially short or damaged ones.

The source uses a div labelled translation for GRC interpretations; the project
records these in greek_interpretations, separate from modern-language translations.
Source interpretations are not automatically independent linguistic gold.

## Token analysis

Whitespace spans are indexed with exact character offsets in the readable edition.
They are source display units, not verified linguistic word boundaries. Only
unannotated spans whose complete hyphen-separated components match the Cypriot
Unicode syllable names enter conservative sign counts. Spans with supplied text,
brackets, underdots or unparsed material are excluded. If semantic TEI editorial
elements occur in an edition, that entire edition is conservatively withheld
from token counts. This can exclude clearly surviving portions too.

These statistics describe the admitted subset in its digital-entry unit. They
are not object-deduplicated, unbiased corpus frequencies, decipherment evidence,
or comparisons with Linear A, Linear B, Cypro-Minoan or other scripts.

## Validation means

Validation checks index/ledger reconciliation, identifiers, licence admission,
source checksums, deterministic extraction and Unicode inventory identity.
It does not prove the ancient reading correct, establish exhaustive coverage,
or substitute for peer review. Negative tests exercise misclassification,
tampering, unsafe paths, unlisted files and uncertainty exclusion.
