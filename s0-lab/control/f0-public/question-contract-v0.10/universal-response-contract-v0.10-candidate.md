# Universal Response Contract v0.10 candidate

- status: **public CONTROL redesign proposal; not independently reviewed or executed**
- design ID: `URC-0.10-CANDIDATE`
- gate: `F0-PUBLIC QUESTION CONTRACT V0.10 REDESIGN OPEN`
- predecessor evidence: authenticated URC-0.7, URC-0.9, and v0.9 independent review v0.1
- excluded: schema, bank/fixture/oracle authoring, implementation, simulation, model calls, scoring, sealed work, and S0 conclusions

## 1. Bounded outcome

This candidate changes only effective-document construction and record-ID ordering needed to answer v0.9 findings V9-B02 and V9-B03. It preserves the authenticated v0.9 proposal-text repairs for C4, finite catalogs, cause bounds, target typing, T/F/U evaluation, consumption, rollback, and claim limits.

Nothing here establishes CONTROL integration, implementation, feasibility, public validation, sealed compatibility, representation superiority, S0 success, or any central-system result.

## 2. Facts, inferences, and proposals

### 2.1 Authenticated facts

- The v0.9 independent review reconstructed the 31-slot effective contract at SHA-256 `54e731edd895db001c3e89da25e06e7c86f1563c297184be3e6cb570fff83f01`.
- That reconstruction passed source authentication, heading resolution, preamble slicing, slot completeness, and nonrecursive sidecar use.
- V0.9 defines an unsigned byte order for already serialized `cause_ref` values but does not define the order used inside multi-member record-ID arrays before serialization.
- V0.9 contract-side C4 scope, catalog arithmetic, 28-cause bound, and eight availability axes passed the independent textual review.

### 2.2 CONTROL inferences

- The v0.9 contract construction can be retained while replacing only the cause-construction slices and publishing one complete successor record grammar.
- One comparator must govern every record-ID array before a cause key is serialized; otherwise equal sets can produce different obligation or correlation bytes.
- Hashing exact heading text in record metadata avoids making metadata character repertoire depend on punctuation in future headings while preserving exact source lookup in the public slot table.

### 2.3 Proposals

Every construction, comparator, mapping, and mutation rule below is an unvalidated proposal. A fresh public-only reviewer must independently reconstruct the effective contract and attack all record-ID order boundaries.

## 3. Complete effective-contract construction

### 3.1 Authenticated source identities

Only these source files contribute bytes to the effective v0.10 contract:

| Source ID | Exact file | SHA-256 source |
|---|---|---|
| `U7` | `question-contract-v0.7/universal-response-contract-v0.7-candidate.md` | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` |
| `U9` | `question-contract-v0.9/universal-response-contract-v0.9-candidate.md` | `2cc20e4afe84fead2a28b85a9fe4c77ae0ce3e69155a18eec5278924b936fe47` |
| `U10` | this `universal-response-contract-v0.10-candidate.md` | its matching same-basename sidecar after this file freezes |

The reviewed v0.9 effective hash is evidence, not a byte source and not a substitute for reconstruction.

### 3.2 Total successor slot map

Every effective v0.9 slot is retained or replaced exactly once.

| Effective slot | Effective v0.9 coverage | Action | Exact effective source slice |
|---:|---|---|---|
| 1 | slot 1 | replace | full `U10` §1, heading `## 1. Bounded outcome` |
| 2 | slot 2 | replace | preamble `U10` §2, from `## 2. Facts, inferences, and proposals` to immediately before `### 2.1 Authenticated facts` |
| 3 | slot 3 | replace | full `U10` §2.1, heading `### 2.1 Authenticated facts` |
| 4 | slot 4 | replace | full `U10` §2.2, heading `### 2.2 CONTROL inferences` |
| 5 | slot 5 | replace | full `U10` §2.3, heading `### 2.3 Proposals` |
| 6 | slot 6 | retain | preamble `U7` §3, from `## 3. Universal decision semantics` to immediately before `### 3.1 Question tuple and predicates` |
| 7 | slot 7 | retain | full `U7` §3.1, heading `### 3.1 Question tuple and predicates` |
| 8 | slot 8 | retain | full `U7` §3.2, heading `### 3.2 Runner-visible decision object` |
| 9 | slot 9 | retain | full `U7` §3.3, heading `### 3.3 Twenty-four globally admissible rows` |
| 10 | slot 10 | retain | full `U7` §3.4, heading `### 3.4 Total mapping and identities` |
| 11 | slot 11 | retain | full `U7` §3.5, heading `### 3.5 Exhaustive truth-entailment classification` |
| 12 | slot 12 | retain | preamble `U7` §4, from `## 4. Response structure and consequence levels` to immediately before `### 4.1 Universal answer obligations` |
| 13 | slot 13 | retain | full `U7` §4.1, heading `### 4.1 Universal answer obligations` |
| 14 | slot 14 | retain | full `U7` §4.2, heading `### 4.2 Raw, response, answer, and field consequences` |
| 15 | slot 15 | retain | full `U9` §7.1, heading `### 7.1 Three-valued atoms and truth tables` |
| 16 | slot 16 | retain | full `U9` §4, heading `## 4. Typed target and pre-admission satisfiability` |
| 17 | slot 17 | retain | preamble `U9` §5, from `## 5. Closed metadata and cause bounds` to immediately before `### 5.1 Closed component bounds` |
| 18 | slot 18 | retain | full `U9` §5.1, heading `### 5.1 Closed component bounds` |
| 19 | slot 19 | retain | full `U9` §5.2, heading `### 5.2 Identity, completeness, and admission rejection` |
| 20 | slot 20 | replace | full `U10` §4, heading `## 4. Global record-ID order and cause construction` |
| 21 | slot 21 | replace | full `U10` §5, heading `## 5. Canonical cause references and total source selectors` |
| 22 | slot 22 | retain | full `U9` §7.2, heading `### 7.2 Complete C1-C7 evaluation and consequences` |
| 23 | slot 23 | retain | preamble `U9` §8, from `## 8. Consumption and finite catalogs` to immediately before `### 8.1 Consumption equations` |
| 24 | slot 24 | retain | full `U9` §8.1, heading `### 8.1 Consumption equations` |
| 25 | slot 25 | retain | full `U9` §§8.2-8.5, from `### 8.2 Unique overlap normal form` through `### 8.5 Bank-instance projection and freeze` |
| 26 | slot 26 | retain | preamble `U7` §9, from `## 9. Canonical JSON and text` to immediately before `### 9.1 Validation order` |
| 27 | slot 27 | retain | full `U7` §9.1, heading `### 9.1 Validation order` |
| 28 | slot 28 | retain | full `U7` §9.2, heading `### 9.2 Complete member order` |
| 29 | slot 29 | retain | full `U7` §9.3, heading `### 9.3 Scalar, one-line, serialization, and limits` |
| 30 | slot 30 | retain | full `U7` §10, heading `## 10. Runner generation and leakage boundary` |
| 31 | slot 31 | replace | full `U10` §6, heading `## 6. Admissibility, rollback, and claim ceiling` |

No effective v0.9 slot or parent preamble is unclassified. U9 §§5.3, 6, and 9 are replaced in full; all other U9 slices listed above remain exact.

### 3.3 Single record grammar and effective hash

For every table row in ascending slot order:

1. Authenticate the full source file against section 3.1.
2. Decode strict UTF-8 without normalization or newline conversion.
3. Resolve each exact ATX heading text from the table. The heading line must occur exactly once and end in LF.
4. In `full` mode, a constituent slice begins at its heading's first byte and ends immediately before the next heading of equal or higher level, or at EOF. A multi-heading range concatenates every consecutive same-level constituent slice with no inserted byte.
5. In `preamble` mode, the slice begins at the named level-2 heading and ends immediately before the named first level-3 child heading, including the parent heading and intervening bytes.
6. Reject missing, duplicate, reordered, nonconsecutive, cross-source, mixed-level, or incomplete ranges and a preamble with an earlier level-3 child.
7. Compute each heading digest over the exact strict-UTF-8 heading text bytes without its final LF and without normalization.
8. Emit exactly one record in this grammar. Metadata bytes are ASCII because non-ASCII heading text is represented only by its lowercase SHA-256 digest:

```text
slot=<decimal slot>\n
source=<U7|U9|U10>\n
source_sha256=<64 lowercase hex>\n
slice_start_heading_sha256=<64 lowercase hex>\n
slice_end_heading_sha256=<64 lowercase hex>\n
slice_mode=<full|preamble>\n
length=<decimal raw-slice byte count>\n
<raw slice bytes>
```

Every field occurs exactly once. There are no transform fields in the contract grammar. The effective stream is ASCII `URC-0.10-EFFECTIVE\n` followed by the 31 records with no separator beyond the bytes shown. `effective_contract_sha256` is SHA-256 of that stream. The value freezes in a later reviewed manifest after the U10 sidecar exists; it is not embedded here.

## 4. Global record-ID order and cause construction

All record IDs remain ASCII, globally unambiguous within a block, and at most 40 bytes. Define `id_order_key(id)` as the inherited canonical JSON serialization of the scalar string `id`, encoded as UTF-8. Compare two keys by unsigned lexicographic byte order: compare the first differing byte numerically, and if one complete key is a prefix of the other, the shorter sorts first.

This comparator is global. Every contract use of `ascending`, `sorted`, `lexicographic`, `unique union`, or `first witness` over record IDs, citation IDs, affected IDs, dependent IDs, target-record IDs, required/counterexample members, correlation derivatives, or independent-basis IDs uses `id_order_key`. No natural-number, locale, case-folded, raw-display, insertion, author, or layout order is permitted. Consequently `R10` precedes `R2`; quotes, backslashes, prefixes, and ASCII punctuation follow their inherited canonical JSON escape bytes.

Authors do not supply cause references. Before constructing a cause key, every member array is sorted once by `id_order_key` and duplicate IDs reject. The comparator derives these canonical JSON-array keys:

| Family | Key |
|---|---|
| decision | `["decision","basis"]`, `["decision","responsibility"]`, `["decision","data"]` |
| prohibited submitted record | `["prohibited-record",record_id]` |
| other invalid citation | `["citation-invalid",record_id]` |
| required/counterexample obligation | `["obligation",[id_order_key-sorted member_ids]]` |
| correlation | `["correlation",[id_order_key-sorted derivative_ids],[id_order_key-sorted independent_basis_ids]]` |
| affected membership | `["affected",record_id]` |
| uncertainty | `["uncertainty"]` |
| reason | `["reason","mechanical"]` or `["reason","semantic"]` |

Two surfaces share a cause if and only if their complete canonical key bytes are identical. Required and counterexample groups with identical sorted member arrays share one obligation key; different arrays use different keys and partial overlap rejects. Correlation group member sets are disjoint and duplicate correlation keys reject. A dual-tag prohibited record has one key shared by C1/C5. Multiple closures share one affected key only for the same record ID. No other sharing exists.

The metadata registry remains at most 20 keys. A submitted answer may add at most four dynamic invalid-citation and four dynamic extra-affected keys, for an absolute maximum of 28. Dynamic extra-affected keys are M4-eligible and never C4 sources. The critical-source pool remains at most 12.

Mandatory P1 order mutations include `R10`/`R2`, strict-prefix IDs, quote and backslash escapes, every permitted ASCII punctuation boundary, identical sets presented in different input orders, obligation aliases, and correlation derivative/basis permutations. Expected bytes must be invariant to presentation order and match both independent generators and comparators.

## 5. Canonical cause references and total source selectors

There is no ordinal `cause_id`. `cause_ref` is the complete canonical JSON-array key after section 4 sorts every inner record-ID array. Sets and tables order complete `cause_ref` values by unsigned lexicographic comparison of their canonical UTF-8 bytes, with shorter-prefix-first. No locale, case folding, natural-number comparison, decoded-scalar collation, or implementation-native map order is permitted.

Selectors remain total:

- `wrong_basis`, `wrong_responsibility`, and `wrong_data` return their one decision key exactly when the available submitted coordinate is unequal to truth.
- When submitted and truth direct permission are available and unequal, `wrong_direct` returns every unequal available coordinate among basis and responsibility.
- When submitted strength is available and greater than truth, `stronger_sources` returns every unequal available coordinate among basis and responsibility.
- A prohibited record returns its prohibited-record key regardless of one or two tags; another invalid citation returns its citation-invalid key.
- Missing required/counterexample, violating correlation, and affected membership return their mechanically derived section-4 keys.
- An unavailable atom contributes no key.

No selector chooses a necessary, primary, minimal, or counterfactual explanation. A true source-requiring branch with an empty source rejects the adjudication bundle or comparator run.

## 6. Admissibility, rollback, and claim ceiling

A later question is admissible only after exact independent labels, global ID ordering, target typing, satisfiability, cause construction, C4/C6 coverage, catalog generation, package scans, semantic reviews, custody checks, and hashes all pass before exposure. One disagreement rejects the entire untouched bank version.

No predecessor is edited in place. A changed hash, post-label change, confirmatory output, leakage, role violation, contradiction, catalog mismatch, ordering mismatch, or custody mismatch requires a new reviewed contract/plan and untouched material. Failure returns to authenticated protocol and review evidence and opens no later gate.

Unknowns remain: varied synthetic authoring, independent agreement, 24-row usability, catalog affordability, packet feasibility, ACL availability, calibration/power, cost/time/storage, immutable model revision, and executor behavior.

This candidate does not establish review closure, CONTROL integration, implementation, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer. The only appropriate next action is fresh public-only independent review under a separate exact gate.
