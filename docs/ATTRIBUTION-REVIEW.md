# Attribution review

All four controls distinguish language attribution, expected revisions without encoded pairs, coin units and fascicle coverage. Shared IG data remain dependent evidence.

Existing source consultation receipts and limits are inherited exactly from the referenced native packets. This pass inspects those packets, not the underlying publications afresh. No exhaustive literature search, new autopsy or independent review is claimed.

The complete selections below name the finite native collections reviewed. Other repository records and the broader literature are outside this checkpoint. Case counts are review tasks, not inscriptions, independent witnesses or fully attributed alternative pairs.

| Complete native selection | Rows |
|---|---:|
| `research/disagreement-register.json/items` | 4 |

Use the case query to read the finding together with the complete native evidence, including any named author/publication, source locator, inspection state, qualification and source dependence. Missing metadata stays missing; a source ID alone is not proof of direct consultation.

```sh
python scripts/attribution_review.py --check
python scripts/attribution_review.py --case 'CSG-DIS-001'
python scripts/evidence_query.py --list attribution-review
```

| Review ID | Type | Finding | Remaining work |
|---|---|---|---|
| CSG-DIS-001 | CLASSIFICATION | IG language labels are edition assertions; uncertain and component labels cannot be resolved from the register. | Locate each questioned component in licensed IG XML before evaluating its language. |
| CSG-DIS-002 | COVERAGE_GAP | The register predicts historical/modern revisions but supplies no aligned pair of readings or page-level ICS citation. | Acquire an exact ICS-to-IG entry and locus crosswalk; expected revision is not an established variant. |
| CSG-DIS-003 | COUNT_OR_IDENTITY | Coin types, edition parts and specimens use different units. | Establish explicit specimen concordances before any physical-object total. |
| CSG-DIS-004 | COVERAGE_GAP | The parsed first fascicle and the historical database denominator are different coverage assertions. | Geographic/fascicle scope and dated source for the broader denominator must accompany comparisons. |

`research/attribution-review.json` pins every referenced native artifact by SHA-256 and records exact JSON pointers. `analysis/attribution-review-audit.json` is replayed by the checker. Queries reject changed input bytes before returning any case. The earlier native records remain unchanged.

Pair-attribution states describe documentary limitations, not scientific acceptance. A partial located comparison can be a real scholarly alternative without full typographic, physical-position or independent collation. `NOT_APPLICABLE` marks controls and interpretations for which a two-reading pair is not the appropriate unit. No unknown pair/witness total is replaced with zero.
