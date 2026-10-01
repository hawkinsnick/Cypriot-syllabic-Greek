# Eteocypriot acquisition preparation

This continues work after the Cypriot syllabic Greek 1.0 milestone. It prepares
priority 2 without redefining the Greek corpus or pretending that a title label
is a verified language assignment for every component of a bilingual inscription.

The reproducible candidate ledger identifies 26 entries in the frozen primary
source snapshot: 18 source-labelled entries, seven uncertain candidates and
one quarantined mixed-language entry. These are acquisition candidates, not 26
independent Eteocypriot inscriptions or an exhaustive corpus.

Run `python scripts/prepare_eteocypriot.py` from the repository root to rebuild
the ledger. It first validates the source snapshot, then preserves exact source
identifiers, raw hashes, CC BY 4.0 attribution links and eligibility exclusions.
No source transcription or sound value has been invented.

## Next work

1. Establish component-level language assertions, starting with bilingual
   entries IG XV 1, 1, 2 and 7; source parts must be cited individually.
2. Keep the seven uncertain candidates separate from source-labelled entries.
3. Preserve IG XV 1, 150's malformed source without guessed repairs. A repaired
   representation would need an explicit transformation and separate source hash.
4. Add source-verified concordances and object identity evidence before treating
   entries in separate projects as different ancient witnesses.
5. Expand acquisition beyond this one digital fascicle with recorded rights and
   source consultation depth; never claim whole-corpus coverage from this ledger.

The family snapshot register pins the actual current commits of the six prior
repositories. Version strings are preserved as retrieved, including the Disc's
prerelease and Byblos's explicitly provisional research status. This register
establishes repository identity only. Native schema adapters and research gate
comparisons remain the next step; linguistic comparisons are not authorized by
metadata compatibility.

The existing 1.0 tag remains the immutable Greek source snapshot used by these
references. Eteocypriot should receive its own release identity when its corpus
and admission criteria are established.
