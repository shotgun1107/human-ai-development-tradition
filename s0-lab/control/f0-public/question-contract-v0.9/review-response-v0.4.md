# URC-0.9 redesign response to authenticated v0.8 review v0.1

- status: **CONTROL author response; not an independent review or validation**
- source review: `urc-v0.8-independent-review-v0.1.md`
- source-review SHA-256: `9bca8b3b2ba9e43d00e17f89ad4e5eec9c329bb8d49fccd5137e01b27034d511`
- proposed successors: `universal-response-contract-v0.9-candidate.md` and `public-falsification-plan-v0.6.md`
- gate: `F0-PUBLIC QUESTION CONTRACT V0.9 REDESIGN OPEN`
- excluded: implementation, public authoring, simulation, execution, scoring, sealed work, and S0 conclusions

## 1. Authenticated input record

CONTROL verified branch `codex/s0-question-contract-v06-review`, clean baseline HEAD `2b3546d383ecb43fdc3c7c03ef9b89b35f48f675`, and the nine allowlisted public Markdown inputs before relying on them. All eight available same-basename sidecars matched. `AGENTS.md` has no sidecar.

| Input | Verified SHA-256 |
|---|---|
| `AGENTS.md` | `656c84c83b78562a3210b50665f02c1200e2552fa8bd879394085c4fb626cf8d` |
| S0-E0 boundary | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` |
| protocol v0.3 | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| URC-0.7 candidate | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` |
| public falsification plan v0.4 | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` |
| URC-0.8 candidate | `ee9f9dd02030a79b7f28a475f18402906c0425de97eab677d50316d41676677c` |
| public falsification plan v0.5 | `b960f6b8d39adfd07e6840f6d06f847b3269fb3bb0e9eeabe5f5a930e982ea0f` |
| v0.8 author response | `b2ab90bb3862fa9b74bf656c87d92cc809b2dfa5990a555731b6c52175b6adcf` |
| v0.8 independent review | `9bca8b3b2ba9e43d00e17f89ad4e5eec9c329bb8d49fccd5137e01b27034d511` |

No E0 artifact, repository-wide search, sealed/private/oracle material, fixture, problem, answer, schema, runner, implementation, output, or web source was used.

## 2. Finding-response map

“Proposed closure” means that the successor text contains a deterministic rule aimed at the finding. It does not mean the rule is correct, feasible, implemented, tested, or independently accepted.

| Authenticated finding | V0.9 response | Author assessment |
|---|---|---|
| V8-B01: incomplete exact-hash contract composition | Candidate §3 publishes a 31-slot total map covering v0.7 §§1-11, including parent preambles and all of §11, identifies every inherited/replaced slice, defines strict byte slicing and one record stream, and defers the nonrecursive effective hash to a reviewed manifest after the v0.9 source sidecar exists. Plan §1 provides a 25-slot transitive P4/P5/P6 construction rather than treating P5 as a self-contained copy of P4. | proposed closure; hostile recomposition required |
| V8-B02: noncanonical cause ordering | Candidate §6 removes ordinal cause IDs. `cause_ref` is the canonical JSON-array key itself and ordering is unsigned lexicographic canonical UTF-8 byte order with a prefix rule. It expressly fixes `R10` before `R2` and forbids locale, natural-number, case-folded, or decoded-scalar alternatives. | proposed closure; byte-boundary mutation review required |
| V8-B03: C4 branch/source-domain mismatch | Candidate §7.3 separately defines dependent-missing, target-record-missing, and direct-mismatch branches and names only each branch's exact source. Unrelated missing accepted IDs and all extra submitted affected IDs remain M4. Alias, T/F/U, dependency, target, and unrelated-ID mutations are mandatory. | proposed closure; downstream consumption must be independently traced |
| V8-B04: impossible catalog arithmetic | Candidate §8.3 fixes the unquotiented abstract product to 921,600 and retains rejected rows. Candidate §§8.4-8.5 separately fix 1,792 availability rows, 407 cause-key rows, and the maximum 2,949,120 bank-instance projection. Plan §§5-7 propagates those counts into benchmark and resource stops. | proposed closure; resource envelope and generators remain unrun |
| V8-M01: incomplete cause and availability bounds | Candidate §§5.3 and 8.4 include 20 metadata keys, four dynamic invalid-citation keys, and four dynamic extra-affected keys for an absolute maximum of 28. It names and orders all eight availability axes and defines the 28-slot baseline/single/pair catalog. | proposed closure; completeness and storage remain unverified |
| V8-M02: unmatched operational edges | Plan §§2-4 names every store, adds assigned-package delivery, constants/formula delivery, one exact `agreed-label-vault`, generator/P1/judgment stores, 50 numbered operational edges plus eight public grant edges, and an explicit role-to-edge index. Store-mediated edges are assigned to their only writer and authorized reader. | proposed closure; an independent bijection and ACL audit is required |

## 3. Authenticated passes intentionally preserved

The effective construction retains or republishes these predecessor proposal-text controls:

- all 24 globally admissible rows and all 64 raw vectors, typed human/Brain ownership, and direct operation only for `authorized; none`;
- finite citation, affected-set, answer, packet, and raw-byte witnesses with pre-admission rejection;
- strong T/F/U algebra, multi-coordinate `wrong_direct` and `stronger_sources`, and response/answer/field-local consequences;
- strict canonical JSON, duplicate detection, NFC and prohibited-line-scalar rejection, surrogate handling, complete member order, and narrow leakage claims;
- valid P3 null grids, complete P2/P3 mappings, fit/audit separation, rotations, schedules, and grid-limited statistical claims;
- direct non-nested simulation, benchmark stops, concurrency three, immutable model revision/fingerprint, first-output-only, and no retry;
- 960-call and visible-token arithmetic at N=720, the exact 240-hour total, and noncompensatory P0-P4;
- untouched-bank rollback, sealed/oracle separation, S0-E0 separation, and the maximum synthetic-public-experiment claim ceiling.

Preservation is a document-construction proposal only. None of these controls has been implemented or empirically validated here.

## 4. New v0.9 invariants

1. Only authenticated v0.7 and v0.9 slices contribute normative contract bytes; v0.8 remains historical evidence.
2. Every predecessor section and subsection is classified once before an effective hash can exist.
3. Canonical cause bytes are identity and order; no local ordinal remapping exists.
4. Each C4 true branch returns only the cause keys that made that branch true.
5. The full abstract product is 921,600 rows with no pre-rejection quotient.
6. Availability uses one published eight-bit order, and the cause catalog covers all 28 maximum slots.
7. Every operational positive input and output has an exact ledger edge or exact named-store grant; ambient access is forbidden.
8. The dispatcher receives its assigned signed package, and analysis receives pre-call frozen selected constants plus the public formula manifest through named stores.
9. The semantic condition map remains withheld until the anonymous analysis hash freezes; final decision is a mechanical join with no reanalysis.

## 5. Remaining unknowns and risks

- A fresh reviewer may find a missing slice, heading-boundary ambiguity, or inherited/replacement contradiction in either effective construction.
- Independent serializers, generators, comparators, catalogs, role-edge audits, and ACLs do not exist and may disagree.
- The corrected 921,600-row abstract catalog and maximum projection may exceed compute, storage, signing, calendar, human, or monetary ceilings.
- The 24-row grammar and tightened metadata may be impractical for varied synthetic authoring or first-output executors.
- Independent labels, scans, leakage reviews, judgments, maps, and comparison custodians may fail exact agreement.
- Calibration, power, exact model availability, drift behavior, costs, and every P0-P4 result remain unknown.

## 6. Bounded status and exact next action

The v0.9 package is an unimplemented public CONTROL redesign proposal. It does not establish CONTROL-integration suitability, an executable schema, bank, fixture, oracle, generator, comparator, runner, simulation, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

The only appropriate next gate is:

`F0-PUBLIC QUESTION CONTRACT V0.9 INDEPENDENT REVIEW OPEN`

That review must authenticate and reconstruct both effective documents, re-evaluate V8-B01 through V8-M02, and test non-regression of every authenticated pass using public inputs only. No later gate opens automatically.
