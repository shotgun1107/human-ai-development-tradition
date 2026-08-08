# Universal Response Contract v0.11 candidate

- status: **public CONTROL redesign proposal; not independently reviewed or executed**
- design ID: `URC-0.11-CANDIDATE`
- gate: `F0-PUBLIC QUESTION CONTRACT V0.11 REDESIGN OPEN`
- predecessor evidence: authenticated URC-0.7, URC-0.9, URC-0.10, and v0.10 independent review v0.1
- excluded: schema, bank/fixture/oracle authoring, implementation, simulation, model calls, scoring, sealed work, and S0 conclusions

## 1. Bounded outcome

This candidate changes only the effective-contract composition needed to answer v0.10 finding V10-B01. It republishes one complete normative definition of semantic atoms, their availability, operational strength, direct permission, cause mapping, and source selectors. It preserves the authenticated v0.10 byte grammar, global record-ID order, typed target, C4, finite catalogs, cause bounds, rollback, and claim limits.

Nothing here establishes review closure, CONTROL integration, implementation, feasibility, public validation, sealed compatibility, representation superiority, S0 success, or any central-system result.

## 2. Facts, inferences, and proposals

### 2.1 Authenticated facts

- The v0.10 independent review reconstructed the 31-slot effective contract at SHA-256 `b110eb844e81c53ffdd3103cfbd26e57365487d89d8b19b2452f142e1e56d8a8`.
- V10-B01 found that effective v0.10 replaced U7 section 6 without republishing the semantic-atom, operational-strength, and truth-function definitions still consumed by retained C/P3 text.
- The same review passed the v0.10 source authentication, slice construction, record grammar, heading encoding, global record-ID order, target/C4 repair, cause/catalog arithmetic, and bounded claim at their stated proposal-text levels.

### 2.2 CONTROL inferences

- The omission can be repaired without changing the 31-slot cardinality by replacing effective v0.10 slot 21 with one self-contained normative slice.
- Availability and truth must be separate: an unavailable submitted field yields `U`, while an available unequal or prohibited value yields `F`.
- The semantic slice must define every atom used by P3, every predicate used by C1-C7, and every cause returned to consumption. A unique byte stream alone is insufficient.

### 2.3 Proposals

Every rule below remains an unimplemented proposal. A fresh public-only reviewer must independently reconstruct the effective stream and attack field unavailability, strength boundaries, direct-permission mismatches, citation groups, reason judgments, cause aliases, and P3 consequences.

## 3. Complete effective-contract construction

### 3.1 Authenticated source identities

Only these source files contribute bytes to the effective v0.11 contract:

| Source ID | Exact file | SHA-256 source |
|---|---|---|
| `U7` | `question-contract-v0.7/universal-response-contract-v0.7-candidate.md` | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` |
| `U9` | `question-contract-v0.9/universal-response-contract-v0.9-candidate.md` | `2cc20e4afe84fead2a28b85a9fe4c77ae0ce3e69155a18eec5278924b936fe47` |
| `U10` | `question-contract-v0.10/universal-response-contract-v0.10-candidate.md` | `650a1be0fefd3643a2d0be940669038cac1c46d5695613efdb9d5cb3c37b780b` |
| `U11` | this `universal-response-contract-v0.11-candidate.md` | its matching same-basename sidecar after this file freezes |

The reviewed v0.10 effective hash is evidence, not a byte source and not a substitute for reconstruction.

### 3.2 Total successor slot map

Every effective v0.10 slot is retained or replaced exactly once.

| Effective slot | Effective v0.10 coverage | Action | Exact effective source slice |
|---:|---|---|---|
| 1 | slot 1 | replace | full `U11` section 1, heading `## 1. Bounded outcome` |
| 2 | slot 2 | replace | preamble `U11` section 2, from `## 2. Facts, inferences, and proposals` to immediately before `### 2.1 Authenticated facts` |
| 3 | slot 3 | replace | full `U11` section 2.1, heading `### 2.1 Authenticated facts` |
| 4 | slot 4 | replace | full `U11` section 2.2, heading `### 2.2 CONTROL inferences` |
| 5 | slot 5 | replace | full `U11` section 2.3, heading `### 2.3 Proposals` |
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
| 21 | slot 21 | replace | full `U11` section 4, heading `## 4. Complete semantic atoms, strength, causes, and selectors` |
| 22 | slot 22 | retain | full `U9` section 7.2, heading `### 7.2 Complete C1-C7 evaluation and consequences` |
| 23 | slot 23 | retain | preamble `U9` section 8, from `## 8. Consumption and finite catalogs` to immediately before `### 8.1 Consumption equations` |
| 24 | slot 24 | retain | full `U9` section 8.1, heading `### 8.1 Consumption equations` |
| 25 | slot 25 | retain | full `U9` sections 8.2-8.5, from `### 8.2 Unique overlap normal form` through `### 8.5 Bank-instance projection and freeze` |
| 26 | slot 26 | retain | preamble `U7` section 9, from `## 9. Canonical JSON and text` to immediately before `### 9.1 Validation order` |
| 27 | slot 27 | retain | full `U7` section 9.1, heading `### 9.1 Validation order` |
| 28 | slot 28 | retain | full `U7` section 9.2, heading `### 9.2 Complete member order` |
| 29 | slot 29 | retain | full `U7` section 9.3, heading `### 9.3 Scalar, one-line, serialization, and limits` |
| 30 | slot 30 | retain | full `U7` section 10, heading `## 10. Runner generation and leakage boundary` |
| 31 | slot 31 | replace | full `U11` section 5, heading `## 5. Admissibility, rollback, and claim ceiling` |

No effective v0.10 slot or parent preamble is unclassified. U10 sections 1-3, 5, and 6 are replaced in full; only its authenticated section 4 remains exact.

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
source=<U7|U9|U10|U11>\n
source_sha256=<64 lowercase hex>\n
slice_start_heading_sha256=<64 lowercase hex>\n
slice_end_heading_sha256=<64 lowercase hex>\n
slice_mode=<full|preamble>\n
length=<decimal raw-slice byte count>\n
<raw slice bytes>
```

Every field occurs exactly once. There are no transform fields in the contract grammar. The effective stream is ASCII `URC-0.11-EFFECTIVE\n` followed by the 31 records with no separator beyond the bytes shown. `effective_contract_sha256` is SHA-256 of that stream. The value freezes in a later reviewed manifest after the U11 sidecar exists; it is not embedded here.

## 4. Complete semantic atoms, strength, causes, and selectors

This section is the only normative semantic-atom and selector definition in the effective contract. Nothing is inherited from omitted U7 section 6.

Define `response_ok` as `F-envelope=T AND F-membership=T`. A submitted field is available exactly when `response_ok` and its own inherited format atom are T. Thus basis, responsibility, data, cited IDs, affected IDs, uncertainty, and short reason depend respectively on `F-basis`, `F-responsibility`, `F-data`, `F-cited`, `F-affected`, `F-uncertainty`, and `F-reason`. `F-answer` is the aggregate answer-schema result used by the inherited consequence table; it is not an additional dependency for an otherwise valid independent field. If the expected answer object cannot expose a field, that field's own format atom is F. Therefore one malformed field can make `F-answer=F` while other fields whose own atoms are T remain available for diagnosis. Accepted metadata is always available after admission. An unavailable semantic atom is `U`, never `F`, and returns no cause.

The semantic-judge result is available only when the short-reason field is available and two fresh public judges have produced signed judgments whose comparison yields one byte-identical agreed result for that answer. Missing, malformed, or unequal judgments make `R-semantic=U` and invalidate the adjudication bundle before confirmatory scoring; they are not coerced to F.

For every answer the comparator emits exactly these semantic atoms when their dependencies are available:

| Atom | Availability | T condition; otherwise F |
|---|---|---|
| `D-basis` | submitted basis | submitted basis equals accepted basis |
| `D-responsibility` | submitted responsibility | submitted responsibility equals accepted responsibility |
| `D-data` | submitted data | submitted data equals accepted data |
| `E-cite:<id>` for every submitted citation ID | cited IDs | `<id>` belongs to `allowed_record_ids` |
| `E-required:<obligation>` for every required group | cited IDs | at least one group member is cited |
| `E-correlation:<group>` for every correlation group | cited IDs | fewer than two derivatives are cited, or at least one independent-basis member is cited |
| `E-counter:<obligation>` for every counterexample group | cited IDs and submitted strength | submitted strength is not greater than truth, or at least one counterexample member is cited |
| `A:<id>` for every ID in the unique union of submitted and accepted affected IDs | affected IDs | submitted membership for `<id>` equals accepted membership |
| `U` | submitted uncertainty | submitted uncertainty equals accepted uncertainty |
| `R-mechanical` | short reason | exact bytes satisfy inherited canonical escaped-byte, scalar, one-line, length, and prohibited-lexeme rules |
| `R-semantic` | semantic-judge result | the agreed result says that no prohibited semantic claim class appears |

If required and counterexample member arrays are identical after global ID sorting, their two surface atoms remain separate but map to the same obligation cause. Consumption permits only one later residual use of that cause.

For a complete basis/responsibility pair define:

```text
operational_strength(authorized, none) = 2
operational_strength(any barred row) = 1
operational_strength(every other admissible row) = 0
permits_direct(row) = T exactly for (authorized, none), otherwise F
```

Truth strength and `truth_direct` are always available. Submitted strength and `submitted_direct` are U if either submitted basis or responsibility is unavailable. Otherwise `stronger(answer,truth)` is T exactly when submitted operational strength is numerically greater than truth strength and F otherwise. Direct inequality is T exactly when available `submitted_direct` differs from `truth_direct`, F when equal, and U when submitted direct permission is unavailable.

False available atoms map mechanically to the effective slot-20 canonical keys:

- false `D-basis`, `D-responsibility`, and `D-data` map to their distinct decision keys;
- a false citation atom for a tagged prohibited record maps to its one prohibited-record key, while every other false citation maps to its citation-invalid key;
- false required and counterexample atoms map to their sorted-member obligation key;
- a false correlation atom maps to its sorted derivative/basis correlation key;
- false affected membership maps to the affected key for that record ID;
- false uncertainty maps to the uncertainty key; and
- false mechanical and semantic reason atoms map to their respective reason keys.

The source selectors are total:

- `wrong_basis`, `wrong_responsibility`, and `wrong_data` return their one decision key exactly when the corresponding available atom is F.
- When submitted and truth direct permission are available and unequal, `wrong_direct` returns every basis/responsibility decision key whose submitted coordinate differs from truth. The set is nonempty by construction.
- When submitted strength is available and greater than truth, `stronger_sources` returns every basis/responsibility decision key whose submitted coordinate differs from truth. The set is nonempty by construction.
- A cited prohibited record returns its one prohibited-record key regardless of whether it carries one or both tags; another invalid citation returns its citation-invalid key.
- Missing required/counterexample membership, a violating correlation, and unequal affected membership return their mechanically derived obligation, correlation, and affected keys.
- Unavailable atoms and F branches return no T-branch source. A true source-requiring branch with an empty source rejects the bundle or comparator run.

No selector chooses a primary, necessary, minimal, or counterfactual explanation. The exact P3 semantic success set is all atoms enumerated in the table for that admitted question and submitted answer. After inherited format handling, P3 `Y=1` exactly when every member of that set is T; `Y=0` when at least one available member is F. Any U member invalidates adjudication before Y and is never treated as F or T.

Mandatory P1 mutations cross every field-availability bit with equal/unequal decision coordinates; all three strength levels; every ordered submitted/truth strength pair; direct equal/different/U; allowed, prohibited, and other invalid citations; required hit/miss; correlation zero/one/two derivatives with/without basis; counterexample hit/miss under stronger and non-stronger rows; affected equal/missing/extra; uncertainty equal/different; reason mechanical T/F/U; semantic judgment T/F/U; identical required/counterexample aliases; and every C1-C7 T/F/U consequence. Both independent expected generators and comparators must agree on atom values, sources, consumption, and P3 Y.

## 5. Admissibility, rollback, and claim ceiling

A later question is admissible only after exact independent labels, semantic-atom and strength tables, global ID ordering, target typing, satisfiability, cause construction, C4/C6 coverage, catalog generation, package scans, semantic reviews, custody checks, and hashes all pass before exposure. One disagreement rejects the entire untouched bank version.

No predecessor is edited in place. A changed hash, post-label change, confirmatory output, leakage, role violation, contradiction, semantic-atom disagreement, catalog mismatch, ordering mismatch, or custody mismatch requires a new reviewed contract/plan and untouched material. Failure returns to authenticated protocol and review evidence and opens no later gate.

Unknowns remain: varied synthetic authoring, independent agreement, 24-row usability, catalog affordability, packet feasibility, ACL availability, calibration/power, cost/time/storage, immutable model revision, and executor behavior.

This candidate does not establish review closure, CONTROL integration, implementation, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer. The only appropriate next action is fresh public-only independent review under a separate exact gate.
