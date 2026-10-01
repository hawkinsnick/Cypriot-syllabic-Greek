# Data model 1.0

| Field | Meaning |
|---|---|
| id | Stable project namespace for the source entry; not a physical object |
| source_id | Exact BBAW digital edition identifier |
| record_unit | Always digital_edition_entry |
| object_id / independent_witness_id | Unknown in this snapshot; null |
| script | ISO 15924 Cprt |
| language | Classification, basis, status and Greek-analysis eligibility |
| edition.text | Readable source view, with preserved uncertainty and arrows |
| edition.xml | Serialized source edition subtree, retaining semantic markup |
| edition.parts / line_labels | Source parts and labels; not globally unique lines |
| edition.tokens | Character offsets and conservative analytical status |
| greek_interpretations | GRC-labelled source interpretations, not ancient syllabic signs |
| translations | Modern-language source translations with responsibility |
| source | URLs, raw source path, SHA-256, date, licence and modifications |
| review | Automated source replay; independent epigraphic review is false |

JSON is the lossless project interchange. CSV is a catalogue convenience view;
it does not carry the complete edition or evidence. TEI exports are the unchanged
source files. The schema covers project records, not the external XML's EpiDoc
conformance. No EpiDoc validation is claimed merely because XML is well formed.

IDs are stable within this source edition. They do not resolve historical ICS,
museum or other catalogue identities. Any future concordance needs attributed
identity assertions and must not merge entries on a matching number alone.
