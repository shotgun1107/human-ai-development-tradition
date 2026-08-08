# URC-0.11 redesign response to authenticated v0.10 review v0.1

- status: **CONTROL author response; not an independent review or validation**
- source review: `urc-v0.10-independent-review-v0.1.md`
- source-review SHA-256: `b20855eca2efb59fc51768d581a815ef26934ed524c3fbc2197db6407c621c8a`
- proposed successors: `universal-response-contract-v0.11-candidate.md` and `public-falsification-plan-v0.8.md`
- gate: `F0-PUBLIC QUESTION CONTRACT V0.11 REDESIGN OPEN`
- excluded: implementation, public authoring, simulation, execution, scoring, sealed work, and S0 conclusions

## 1. Authenticated input record

CONTROL verified branch `codex/s0-question-contract-v06-review`, clean baseline HEAD `e19f1588f23038414b73ead530e028e0ef22550c`, and twelve allowlisted public Markdown inputs before reliance. All eleven available same-basename sidecars matched. `AGENTS.md` has no sidecar.

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
| v0.10 author response | `a15484c1f55ee388b2f6b49c25f67f549af6560b620a9b1ae128a080eedfd1d1` |
| v0.10 independent review | `b20855eca2efb59fc51768d581a815ef26934ed524c3fbc2197db6407c621c8a` |

No E0 artifact, repository-wide substantive search, sealed/private/oracle material, fixture, question, answer, schema, runner, implementation, output, or web source was used.

## 2. Finding-response map

“Proposed closure” means only that v0.11 contains a deterministic written response. It does not mean correct, feasible, implemented, tested, or independently accepted.

| Authenticated finding | V0.11 response | Author assessment |
|---|---|---|
| V10-B01: effective contract omits semantic atoms and strength | Candidate section 4 is the sole mapped replacement for slot 21. It explicitly defines field and judge availability, every semantic atom, all T/F/U conditions, the complete strength table, `stronger`, `permits_direct`, false-atom cause mapping, every source selector, and exact P3 Y handling. The map states that omitted U7 section 6 is not inherited. | proposed closure; independent reconstruction and hostile semantic mutations required |
| V10-M01: unmatched registrar and comparison outputs | Plan sections 2-4 add a terminal public status-reader role, literal E51 registrar-store write, literal E52 read, digest-chained status records, and role-index cells. E43 now carries the judgment equality digest with the agreed semantic table; E45 carries the adjudication equality digest with the agreed derived table. | proposed closure; fresh matrix-ledger and ACL audit required |

## 3. Authenticated passes intentionally preserved

The v0.11 effective maps retain or republish:

- the 31-slot contract and 25-slot plan record grammars with exact heading digests and no duplicate fields;
- the two exact slot-10 transforms, now from v0.8 to v0.11 under separate count-one preconditions;
- global canonical scalar-JSON byte ordering for every inner record-ID set and complete cause reference;
- all 24 admissible rows, typed human/Brain owners, and direct operation only for `authorized; none`;
- target typing, satisfiability, C1-C7 branches, corrected C4 scope, T/F/U tables, consumption, and response/answer/field consequences;
- 28-cause, eight-axis, 921,600 abstract, 1,792 availability, 407 cause-key, and maximum 2,949,120 instance counts;
- exact N/24 balance, divisibility, development-example exclusion, and duplicate-key controls;
- P2/P3 mappings, schedules, non-circular seeds, fit/audit separation, scans, leakage reviews, transport, no retry, and drift invalidation;
- blinded analysis, release-after-analysis, 960-call/token arithmetic, the 240-hour ledger, and resource stops; and
- rollback, sealed/oracle and S0-E0 boundaries, noncompensatory P0-P4, and the bounded synthetic-experiment claim ceiling.

These are proposal-text preservation claims only, not implementation or empirical results.

## 4. New v0.11 invariants

1. Effective slot 21 contains every semantic predicate consumed by P3, C1-C7, and later cause consumption; no omitted semantic definition is inherited.
2. A field is U only from its exact response/field availability dependency, while an available unequal or prohibited value is F.
3. Submitted operational strength and direct permission are U unless both basis and responsibility are available; otherwise their tables are total.
4. Every false available semantic atom maps to one canonical cause family before consumption, and every true source-requiring branch must return a nonempty set.
5. P3 semantic success means every enumerated atom is T; an unavailable atom invalidates adjudication rather than becoming F.
6. `registrar-store` has one writer edge E51 and one read edge E52, with a signed digest chain and a terminal reader.
7. E43 and E45 transfer their declared comparison digests together with their agreed tables; neither digest may be silently discarded.

## 5. Author-side construction self-test

One in-memory author-side reconstruction using strict UTF-8, exact heading lookup, the published slice rules, and the published record grammars produced:

```text
effective_contract_slots=31
effective_contract_raw_slice_bytes=34069
effective_contract_stream_bytes=43602
effective_contract_sha256=45d9526b4c48d199acbcf3659befab18ba1cd55e08fdaac45ea11e02f95ef88c

effective_plan_slots=25
effective_plan_raw_slice_bytes=51897
effective_plan_transformed_slice_bytes=51899
effective_plan_stream_bytes=60240
effective_plan_sha256=2c7043400030506a6d19029139869f49ac8689e95c853e2a15dde3f60fd3dc8f
```

The same check found exactly E01-E52 once each and executed both slot-10 transforms at their required count. These are nonauthoritative author self-tests, not independent reconstruction, frozen manifests, implementation, or validation results.

## 6. Remaining unknowns and risks

- A fresh reviewer may find an availability dependency, atom domain, selector, or P3 consequence still ambiguous or contradictory.
- Independent serializers may disagree on a heading, byte boundary, escape, prefix, or set-order mutation.
- The registrar status chain and comparison-digest routes may not correspond to deployable ACL stores or signing infrastructure.
- The duplicate-key specification, varied 24-row bank, catalogs, generators, comparators, scanners, judges, and map builders remain unauthored and untested.
- Calibration, power, exact model availability, costs, drift, executor behavior, and all empirical effects remain unknown.

## 7. Bounded status and exact next action

The v0.11 package is an unimplemented public CONTROL redesign proposal. It does not establish review closure, CONTROL integration, executable schema, bank, fixture, oracle, generator, comparator, runner, simulation, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

The only appropriate next gate is:

`F0-PUBLIC QUESTION CONTRACT V0.11 INDEPENDENT REVIEW OPEN`

That review must authenticate and reconstruct both effective documents, re-evaluate V10-B01 and V10-M01, and test non-regression of every authenticated pass using public inputs only. No later gate opens automatically.
