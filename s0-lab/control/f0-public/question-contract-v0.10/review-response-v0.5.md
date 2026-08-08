# URC-0.10 redesign response to authenticated v0.9 review v0.1

- status: **CONTROL author response; not an independent review or validation**
- source review: `urc-v0.9-independent-review-v0.1.md`
- source-review SHA-256: `d88560ecad9642c743ea1cf9386623b1cc8e77cd34e12c7f5180c298acb52446`
- proposed successors: `universal-response-contract-v0.10-candidate.md` and `public-falsification-plan-v0.7.md`
- gate: `F0-PUBLIC QUESTION CONTRACT V0.10 REDESIGN OPEN`
- excluded: implementation, public authoring, simulation, execution, scoring, sealed work, and S0 conclusions

## 1. Authenticated input record

CONTROL verified branch `codex/s0-question-contract-v06-review`, clean baseline HEAD `58a01535bc4cf3d0b73ca3f812d04a02008f4b77`, and ten allowlisted public Markdown inputs before reliance. All nine available same-basename sidecars matched. `AGENTS.md` has no sidecar.

| Input | Verified SHA-256 |
|---|---|
| `AGENTS.md` | `656c84c83b78562a3210b50665f02c1200e2552fa8bd879394085c4fb626cf8d` |
| S0-E0 boundary | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` |
| protocol v0.3 | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| URC-0.7 candidate | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` |
| public falsification plan v0.4 | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` |
| public falsification plan v0.5 | `b960f6b8d39adfd07e6840f6d06f847b3269fb3bb0e9eeabe5f5a930e982ea0f` |
| URC-0.9 candidate | `2cc20e4afe84fead2a28b85a9fe4c77ae0ce3e69155a18eec5278924b936fe47` |
| public falsification plan v0.6 | `f610f7a226f3f03035b8d425079b3643e76687e19b295077ad017c84795d45ae` |
| v0.9 author response | `8d243c4435fff25012b0ec416c5b09414654edf4e1c4ee9d7e8d1ab549419597` |
| v0.9 independent review | `d88560ecad9642c743ea1cf9386623b1cc8e77cd34e12c7f5180c298acb52446` |

No E0 artifact, repository-wide search, sealed/private/oracle material, fixture, question, answer, schema, runner, implementation, output, or web source was used.

## 2. Finding-response map

“Proposed closure” means only that v0.10 contains a deterministic written response. It does not mean correct, feasible, implemented, tested, or independently accepted.

| Authenticated finding | V0.10 response | Author assessment |
|---|---|---|
| V9-B01: slot-10 transform cannot execute | Plan §1.3 inventories the authenticated P5 §8 slice as one exact ASCII `v0.8` and one exact ASCII `URC-0.8`. It publishes two ordered hex-encoded transforms with required occurrence count one each and rejects any other count. | proposed closure; independent reconstruction required |
| V9-B02: contradictory/non-unique plan record encoding | Contract §3.3 and plan §1.3 each publish one complete grammar with every field once. Heading metadata uses lowercase SHA-256 over exact UTF-8 heading text, so literal U+2014 never conflicts with ASCII metadata. Plan transforms are explicit variable blocks after one `slice_mode`. | proposed closure; byte-for-byte hostile reconstruction required |
| V9-B03: undefined inner record-ID order | Contract §4 defines `id_order_key` as canonical JSON scalar-string UTF-8 bytes and applies unsigned lexicographic order globally to every record-ID array and witness operation before cause serialization. It freezes R10/R2, prefix, escape, punctuation, and presentation-order mutations. | proposed closure; two independent serializers must agree |
| V9-M01: lost balance and duplicate controls | Plan §5 restores exact `N/24` balance across all 24 rows, divisibility by 24/12/8, pre-authoring N selection, development-example exclusion, exact duplicate rejection, and noun/entity/identifier/number-swapped duplicate-key rejection. | proposed closure; duplicate-key specification and authoring feasibility remain unimplemented |
| continuation of V8-M02: false custody bijection | Plan §§2-4 authorizes registrar receipt and routing of reviewed public specification bytes, adds transformation specification to E00C and full statistical/catalog inputs to E01, removes unproduced role/store attestations, and makes content, label, leakage, condition-map, and other vault write/read routes explicit. | proposed closure; fresh matrix-ledger and ACL audit required |

An author-side in-memory reconstruction produced 31 contract slots, 28,518 raw slice bytes, 38,051 effective-stream bytes, and SHA-256 `b110eb844e81c53ffdd3103cfbd26e57365487d89d8b19b2452f142e1e56d8a8`; and 25 plan slots, 50,309 transformed slice bytes, 58,650 effective-stream bytes, and SHA-256 `864a53f07c678ef26971f19d0338d23a8f8fff232902727aefaad01bee03ddb0`. This is a nonauthoritative author self-test, not an independent reconstruction, frozen manifest, implementation, or validation result.

## 3. Authenticated passes intentionally preserved

The v0.10 effective maps retain or republish:

- all 24 rows and 64 raw vectors, typed human/Brain owners, and direct operation only for `authorized; none`;
- citation, affected-set, answer, packet, and raw-byte satisfiability;
- strong T/F/U evaluation, multi-coordinate selectors, corrected C4 branch sources, consumption, and response/answer/field consequences;
- target typing, strict canonical JSON, duplicate member rejection, NFC and line-scalar rules, surrogate handling, and member order;
- 28-cause, eight-axis, 921,600 abstract, 1,792 availability, 407 cause-key, and maximum 2,949,120 instance counts;
- P2/P3 mappings, valid P3 grids, balance schedules, non-circular seeds, fit/audit separation, and grid-limited claims;
- scans, leakage reviews, transport timestamps, first-output-only, no retry, immutable revision/fingerprint, and drift invalidation;
- blinded analysis, release-after-analysis, no reanalysis, 960-call/token arithmetic, 240 human hours, and resource stops; and
- untouched-bank rollback, sealed/oracle and S0-E0 boundaries, noncompensatory P0-P4, and the bounded synthetic-experiment claim ceiling.

These are proposal-text preservation claims only, not implementation or empirical results.

## 4. New v0.10 invariants

1. The contract has one 31-record grammar and the plan has one 25-record grammar; a field cannot be inherited and inserted twice.
2. Exact heading text locates source slices, while its UTF-8 SHA-256 is the only heading value placed in ASCII metadata.
3. Slot 10 transforms one lowercase version phrase and one uppercase seed-domain token under separate exact counts.
4. One canonical scalar-JSON byte comparator orders every record-ID array before any cause key exists.
5. Every accepted bank is exactly balanced across 24 rows and contains no development example or frozen duplicate key.
6. Registrar may route reviewed public specifications but remains blind to bank content, labels, outputs, semantic maps, and sealed material.
7. Every required transformation/statistical/catalog specification and every named-vault write/read route has an explicit ledger cell.

## 5. Remaining unknowns and risks

- A fresh reviewer may find a slot omission, heading-digest ambiguity, transform inventory error, or inherited/replacement conflict.
- Independent serializers may disagree on an escape or prefix boundary despite the proposed comparator.
- The future duplicate-key specification may be too broad, too narrow, or infeasible for varied synthetic authoring.
- The revised registrar grants, ACL stores, condition-map staged readers, and atomic content-vault write may not be operationally available.
- Independent labels, generators, comparators, scanners, reviewers, judges, and map builders may fail exact agreement.
- The catalogs and maximum projection may exceed human, compute, storage, calendar, or monetary ceilings.
- Calibration, power, exact model availability, costs, drift, and executor behavior remain unknown.

## 6. Bounded status and exact next action

The v0.10 package is an unimplemented public CONTROL redesign proposal. It does not establish review closure, CONTROL integration, executable schema, bank, fixture, oracle, generator, comparator, runner, simulation, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

The only appropriate next gate is:

`F0-PUBLIC QUESTION CONTRACT V0.10 INDEPENDENT REVIEW OPEN`

That review must authenticate and reconstruct both effective documents, re-evaluate V9-B01 through V9-M01 and the continuing V8-M02 custody finding, and test non-regression of every authenticated pass using public inputs only. No later gate opens automatically.
