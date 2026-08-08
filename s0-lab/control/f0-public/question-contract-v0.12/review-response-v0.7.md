# URC-0.12 redesign response to authenticated v0.11 review v0.1

- status: **CONTROL author response; not an independent review or validation**
- source review: `urc-v0.11-independent-review-v0.1.md`
- source-review SHA-256: `f797dfe55781fb9b8c9b325a9945757076596968c8e4f9dc3e449099e8754fe1`
- proposed successors: `universal-response-contract-v0.12-candidate.md` and `public-falsification-plan-v0.9.md`
- gate: `F0-PUBLIC QUESTION CONTRACT V0.12 REDESIGN OPEN`
- excluded: implementation, public authoring, simulation, execution, scoring, sealed work, and S0 conclusions

## 1. Authenticated input record

CONTROL verified branch `codex/s0-question-contract-v06-review`, clean baseline HEAD `e7ed02b5c26d22e29e20e45a3437e9c8fdd78ff7`, and fourteen allowlisted public Markdown inputs before reliance. All thirteen available same-basename sidecars matched. `AGENTS.md` has no sidecar.

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
| URC-0.10 candidate | `650a1be0fefd3643a2d0be940669038cac1c46d5695613efdb9d5cb3c37b780b` |
| public falsification plan v0.7 | `07edb8ec3044874f39ed60f1a6952eb64e369715fc1501fd309888c9b24d09dd` |
| URC-0.11 candidate | `ae4620c1b532906538252ed503cf39211c46371d4e1eebdbe9a5ef5136528807` |
| public falsification plan v0.8 | `a35ec31efd009684cf8c96400b48b87ef50a7692402f9793ee08ce883f8450c0` |
| v0.11 author response | `6f5e2308ba33da97b231b76d621559f2b4153588a55acab698a6af4c65c2365e` |
| v0.11 independent review | `f797dfe55781fb9b8c9b325a9945757076596968c8e4f9dc3e449099e8754fe1` |

No E0 artifact, repository-wide substantive search, sealed/private/oracle material, fixture, question, answer, schema, runner, implementation, output, or web source was used.

## 2. Finding-response map

“Proposed closure” means only that v0.12 contains a deterministic written response. It does not mean correct, feasible, implemented, tested, or independently accepted.

| Authenticated finding | V0.12 response | Author assessment |
|---|---|---|
| V11-M01: status transition and digest/signature bytes are non-unique | Plan section 4 publishes one ASCII/LF record grammar, SHA-256 rule, Ed25519 signature preimage/envelope, role-bound public-key registry, 14-bit evidence order, 15 allowed prefix-mask statuses, genesis/append/timestamp rules, and fixed-role E43/E45 comparison records. No free status label or alternate concatenation remains. | proposed closure; independent byte reconstruction, transition mutations, and cryptographic-scope audit required |
| V11-M02: final public publisher is outside role/ACL model | Plan sections 2, 3, and 5 add public record publisher and terminal reader roles, `public-decision-store`, E53 exact vault read, E54 atomic publication/receipt write, E55 public read, E56 receipt-digest return, and complete role-index cells. | proposed closure; fresh matrix/store/edge/index and ACL audit required |

## 3. Authenticated passes intentionally preserved

The v0.12 effective maps retain or republish:

- the 31-slot contract and 25-slot plan construction grammars, exact heading digests, and slot-10 transforms;
- the complete v0.11 semantic slice, including availability, semantic atoms, strength, direct permission, causes, selectors, consumption, and P3 consequences;
- global canonical record-ID and cause ordering, target typing, satisfiability, C1-C7, corrected C4, and T/F/U handling;
- 28-cause, eight-axis, 921,600 abstract, 1,792 availability, 407 cause-key, and maximum 2,949,120 instance counts;
- exact N/24 balance, development-example exclusion, duplicate controls, P2/P3 mappings and schedules, and non-circular seeds;
- A-D equality, scans, leakage review, transport, no retry, drift invalidation, blinded analysis, and release-after-analysis;
- the 960-call/token arithmetic, 240-hour ledger, resource stops, rollback, sealed/oracle and S0-E0 boundaries; and
- noncompensatory P0-P4 and the bounded synthetic-experiment claim ceiling.

These are proposal-text preservation claims only, not implementation or empirical results.

## 4. New v0.12 invariants

1. Status records have one exact unsigned grammar, hash, role/key-bound Ed25519 preimage, and envelope.
2. Status is a custody-receipt prefix mask only; the registrar cannot choose a pass/reject narrative for the same edge and prior state.
3. Genesis and 14 evidence transitions have one sequence, previous-record digest, edge, mask, status, and strictly increasing time rule.
4. E43 and E45 fix left/right roles, field order, hashes, agreed-table hash, comparison result, digest, signer role, and signature scope.
5. The public decision record moves only through E50 and E53-E56; publication must be byte-identical and atomically accompanied by one signed receipt.
6. Public status and public decision reading are distinct terminal roles with distinct stores and no experimental outputs.
7. The plan contains exactly eight E00 grants, 56 E01-E56 operational edge types, 26 named stores, 32 role-matrix rows, and 32 role-index rows.

## 5. Author-side construction self-test

One in-memory author-side reconstruction using strict UTF-8, exact heading lookup, the published slice rules, and the published record grammars produced:

```text
effective_contract_slots=31
effective_contract_raw_slice_bytes=33758
effective_contract_stream_bytes=43291
effective_contract_sha256=d44a73a6cd494d1e081be434ebed3d8d52f22fe49f3eed4009ed75c169a753a2

effective_plan_slots=25
effective_plan_raw_slice_bytes=60656
effective_plan_transformed_slice_bytes=60658
effective_plan_stream_bytes=68999
effective_plan_sha256=d6796b581822deb9e8dedfa21d59adeb16331418a71342cf5fa2ad81955fdfc8
```

The same check executed both slot-10 transforms once and found exact E00A-H, E01-E56, 26-store, 32-matrix-row, and 32-index-row inventories. These are nonauthoritative author self-tests, not independent reconstruction, frozen manifests, implementation, or validation results.

## 6. Remaining unknowns and risks

- A fresh reviewer may find a status transition, byte boundary, signature scope, key grant, comparison preimage, or publication receipt still ambiguous or inconsistent.
- Ed25519 key custody, revocation, atomic writes, monotonic timestamps, ACL stores, and durable public delivery may not be operationally available.
- The future duplicate-key specification, varied 24-row bank, catalogs, generators, comparators, scanners, judges, and maps remain unauthored and untested.
- Calibration, power, model availability, costs, drift, executor behavior, and every empirical effect remain unknown.

## 7. Bounded status and exact next action

The v0.12 package is an unimplemented public CONTROL redesign proposal. It does not establish review closure, CONTROL integration, executable schema, bank, fixture, oracle, generator, comparator, runner, simulation, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

The only appropriate next gate is:

`F0-PUBLIC QUESTION CONTRACT V0.12 INDEPENDENT REVIEW OPEN`

That review must authenticate and reconstruct both effective documents, re-evaluate V11-M01 and V11-M02, and test non-regression of every authenticated pass using public inputs only. No later gate opens automatically.
