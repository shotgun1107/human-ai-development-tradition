# Universal Response Contract v0.13 candidate

- status: **public CONTROL redesign proposal; not independently reviewed or executed**
- design ID: `URC-0.13-CANDIDATE`
- gate: `F0-PUBLIC QUESTION CONTRACT V0.13 REDESIGN OPEN`
- predecessor evidence: authenticated URC-0.7, URC-0.9, URC-0.10, URC-0.11, URC-0.12, and v0.12 independent review v0.1
- excluded: schema, bank/fixture/oracle authoring, implementation, simulation, model calls, scoring, sealed work, and S0 conclusions

## 1. Bounded outcome

This candidate preserves the independently reconstructed v0.12 contract semantics byte-for-byte and changes only successor construction and version identity needed to pair them with the v0.13 custody redesign. Effective slot 21 remains authenticated U11 section 4; no semantic atom, strength relation, direct-permission rule, cause, selector, response consequence, or P3 consequence changes here.

The companion plan proposes exact edge-evidence bundles, a noncircular CONTROL root for the signing-key registry, and recipient-verifiable E43/E45 source delivery. These are unimplemented design corrections. Nothing here establishes independent-review closure, CONTROL integration, implementation, feasibility, public validation, sealed compatibility, representation superiority, S0 success, or any central-system result.

## 2. Facts, inferences, and proposals

### 2.1 Authenticated facts

- The v0.12 independent review reconstructed the 31-slot effective contract at SHA-256 `d44a73a6cd494d1e081be434ebed3d8d52f22fe49f3eed4009ed75c169a753a2`.
- That review found no contract-side blocking or major semantic regression. Its three findings, V12-M01 through V12-M03, are plan-side custody and verification defects.
- The authenticated U11 semantic slice passed again at proposal-text level in the v0.12 review.

### 2.2 CONTROL inferences

- Rewriting the semantic slice would create unrelated regression risk, so U11 section 4 must remain byte-identical.
- A direct five-source successor map can advance the package identity while classifying every one of the 31 effective slots exactly once.
- Custody repair cannot silently redefine answer truth, atom availability, strength, causes, selectors, or score consequences.

### 2.3 Proposals

The successor construction below is an unvalidated proposal. A fresh public-only reviewer must independently reconstruct it, authenticate all named inputs, and recheck v0.12 semantic and construction passes for non-regression.

## 3. Complete effective-contract construction

### 3.1 Authenticated source identities

Only these files contribute bytes to the effective v0.13 contract:

| Source ID | Exact file | SHA-256 source |
|---|---|---|
| `U7` | `question-contract-v0.7/universal-response-contract-v0.7-candidate.md` | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` |
| `U9` | `question-contract-v0.9/universal-response-contract-v0.9-candidate.md` | `2cc20e4afe84fead2a28b85a9fe4c77ae0ce3e69155a18eec5278924b936fe47` |
| `U10` | `question-contract-v0.10/universal-response-contract-v0.10-candidate.md` | `650a1be0fefd3643a2d0be940669038cac1c46d5695613efdb9d5cb3c37b780b` |
| `U11` | `question-contract-v0.11/universal-response-contract-v0.11-candidate.md` | `ae4620c1b532906538252ed503cf39211c46371d4e1eebdbe9a5ef5136528807` |
| `U13` | this `universal-response-contract-v0.13-candidate.md` | its matching same-basename sidecar after this file freezes |

U12 and its review are authenticated evidence, not byte sources and not substitutes for reconstruction.

### 3.2 Total successor slot map

Every effective v0.12 slot is retained or replaced exactly once.

| Effective slot | Effective v0.12 coverage | Action | Exact effective source slice |
|---:|---|---|---|
| 1 | slot 1 | replace | full `U13` section 1, heading `## 1. Bounded outcome` |
| 2 | slot 2 | replace | preamble `U13` section 2, from `## 2. Facts, inferences, and proposals` to immediately before `### 2.1 Authenticated facts` |
| 3 | slot 3 | replace | full `U13` section 2.1, heading `### 2.1 Authenticated facts` |
| 4 | slot 4 | replace | full `U13` section 2.2, heading `### 2.2 CONTROL inferences` |
| 5 | slot 5 | replace | full `U13` section 2.3, heading `### 2.3 Proposals` |
| 6 | slot 6 | retain | preamble `U7` section 3, from `## 3. Universal decision semantics` to immediately before `### 3.1 Question tuple and predicates` |
| 7 | slot 7 | retain | full `U7` section 3.1, heading `### 3.1 Question tuple and predicates` |
| 8 | slot 8 | retain | full `U7` section 3.2, heading `### 3.2 Runner-visible decision object` |
| 9 | slot 9 | retain | full `U7` section 3.3, heading `### 3.3 Twenty-four globally admissible rows` |
| 10 | slot 10 | retain | full `U7` section 3.4, heading `### 3.4 Total mapping and identities` |
| 11 | slot 11 | retain | full `U7` section 3.5, heading `### 3.5 Exhaustive truth-entailment classification` |
| 12 | slot 12 | retain | preamble `U7` section 4, from `## 4. Response structure and consequence levels` to immediately before `### 4.1 Universal answer obligations` |
| 13 | slot 13 | retain | full `U7` section 4.1, heading `### 4.1 Universal answer obligations` |
| 14 | slot 14 | retain | full `U7` section 4.2, heading `### 4.2 Raw, response, answer, and field consequences` |
| 15 | slot 15 | retain | full `U9` section 7.1, heading `### 7.1 Three-valued atoms and truth tables` |
| 16 | slot 16 | retain | full `U9` section 4, heading `## 4. Typed target and pre-admission satisfiability` |
| 17 | slot 17 | retain | preamble `U9` section 5, from `## 5. Closed metadata and cause bounds` to immediately before `### 5.1 Closed component bounds` |
| 18 | slot 18 | retain | full `U9` section 5.1, heading `### 5.1 Closed component bounds` |
| 19 | slot 19 | retain | full `U9` section 5.2, heading `### 5.2 Identity, completeness, and admission rejection` |
| 20 | slot 20 | retain | full `U10` section 4, heading `## 4. Global record-ID order and cause construction` |
| 21 | slot 21 | retain | full `U11` section 4, heading `## 4. Complete semantic atoms, strength, causes, and selectors` |
| 22 | slot 22 | retain | full `U9` section 7.2, heading `### 7.2 Complete C1-C7 evaluation and consequences` |
| 23 | slot 23 | retain | preamble `U9` section 8, from `## 8. Consumption and finite catalogs` to immediately before `### 8.1 Consumption equations` |
| 24 | slot 24 | retain | full `U9` section 8.1, heading `### 8.1 Consumption equations` |
| 25 | slot 25 | retain | full `U9` sections 8.2-8.5, from `### 8.2 Unique overlap normal form` through `### 8.5 Bank-instance projection and freeze` |
| 26 | slot 26 | retain | preamble `U7` section 9, from `## 9. Canonical JSON and text` to immediately before `### 9.1 Validation order` |
| 27 | slot 27 | retain | full `U7` section 9.1, heading `### 9.1 Validation order` |
| 28 | slot 28 | retain | full `U7` section 9.2, heading `### 9.2 Complete member order` |
| 29 | slot 29 | retain | full `U7` section 9.3, heading `### 9.3 Scalar, one-line, serialization, and limits` |
| 30 | slot 30 | retain | full `U7` section 10, heading `## 10. Runner generation and leakage boundary` |
| 31 | slot 31 | replace | full `U13` section 4, heading `## 4. Admissibility, rollback, and claim ceiling` |

No effective v0.12 slot or parent preamble is unclassified. U11 sections 1-3 and 5 are replaced; its authenticated section 4 remains exact.

### 3.3 Single record grammar and effective hash

For every table row in ascending slot order:

1. Authenticate the full source file against section 3.1.
2. Decode strict UTF-8 without normalization or newline conversion.
3. Resolve each exact ATX heading text from the table. The heading line must occur exactly once and end in LF.
4. In `full` mode, a constituent slice begins at its heading's first byte and ends immediately before the next heading of equal or higher level, or at EOF. A multi-heading range concatenates every consecutive same-level constituent slice with no inserted byte.
5. In `preamble` mode, the slice begins at the named level-2 heading and ends immediately before the named first level-3 child heading, including the parent heading and intervening bytes.
6. Reject missing, duplicate, reordered, nonconsecutive, cross-source, mixed-level, or incomplete ranges and a preamble with an earlier level-3 child.
7. Compute each heading digest over the exact strict-UTF-8 heading text bytes without its final LF and without normalization.
8. Emit exactly one record in this grammar:

```text
slot=<decimal slot>\n
source=<U7|U9|U10|U11|U13>\n
source_sha256=<64 lowercase hex>\n
slice_start_heading_sha256=<64 lowercase hex>\n
slice_end_heading_sha256=<64 lowercase hex>\n
slice_mode=<full|preamble>\n
length=<decimal raw-slice byte count>\n
<raw slice bytes>
```

Every field occurs exactly once. There are no transform fields in the contract grammar. The effective stream is ASCII `URC-0.13-EFFECTIVE\n` followed by the 31 records with no separator beyond the bytes shown. `effective_contract_sha256` is SHA-256 of that stream. The value freezes in a later reviewed manifest after the U13 sidecar exists; it is not embedded here.

## 4. Admissibility, rollback, and claim ceiling

A later question is admissible only after exact independent labels, semantic-atom and strength tables, global ID ordering, target typing, satisfiability, cause construction, C4/C6 coverage, catalog generation, package scans, semantic reviews, custody checks, and hashes all pass before exposure. One disagreement rejects the entire untouched bank version.

No predecessor is edited in place. A changed hash, post-label change, confirmatory output, leakage, role violation, contradiction, semantic-atom disagreement, catalog mismatch, ordering mismatch, evidence-bundle mismatch, root/registry mismatch, source-envelope mismatch, or custody mismatch requires a new reviewed contract/plan and untouched material. Failure returns to authenticated protocol and review evidence and opens no later gate.

Unknowns remain: varied synthetic authoring, independent agreement, 24-row usability, catalog affordability, packet feasibility, ACL availability, cryptographic-key custody, calibration/power, cost/time/storage, immutable model revision, and executor behavior.

This candidate does not establish review closure, CONTROL integration, implementation, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer. The only appropriate next action is fresh public-only independent review under a separate exact gate.
