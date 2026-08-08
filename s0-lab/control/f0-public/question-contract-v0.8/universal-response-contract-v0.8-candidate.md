# Universal Response Contract v0.8 candidate

- status: **public CONTROL redesign proposal; not independently reviewed, implemented, or validated**
- gate: `F0-PUBLIC QUESTION CONTRACT V0.8 REDESIGN OPEN`
- predecessor: `universal-response-contract-v0.7-candidate.md`
- predecessor SHA-256: `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d`
- excluded: schema implementation, bank authoring, fixtures, oracle material, simulation, executor work, model calls, scoring, and S0 conclusions

## 1. Normative composition and bounded outcome

The effective URC-0.8 contract is the authenticated URC-0.7 candidate at the predecessor hash above, composed with the replacements in this document. Sections 3, 4.1-4.2, 9, and 10 of URC-0.7 are inherited without semantic change. Sections 5.1-5.3, 6, 7, 8, and the claim text in section 11 are replaced in full by sections 3-8 below. Section 4.3 is replaced by section 5 below. Section 4.4 is inherited subject only to the typed target rule in section 3.2 below.

For runtime identifiers, seed-domain labels, manifests, and claim text, the literal version token `URC-0.7` is replaced by `URC-0.8`. This substitution does not change a formula, threshold, schedule, ceiling, or consequence rule. If inherited and replacement text conflict inside a replaced scope, the replacement controls. No other implied override exists.

This composition rule makes the successor finite and reviewable without restating already passed text. It does not assert that any v0.7 or v0.8 proposal is correct or feasible.

## 2. Authenticated redesign inputs

Before authoring, CONTROL read only the seven public allowlisted Markdown inputs and verified every available same-basename sidecar.

| Input | Verified SHA-256 |
|---|---|
| `AGENTS.md` | `07b023666957b357c35ebc9b0da877df615d483064f7c34e85002dded5ad4ca6` |
| S0-E0 boundary | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` |
| protocol v0.3 | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| URC-0.7 candidate | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` |
| public falsification plan v0.4 | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` |
| v0.7 author response | `ee1d62662f73ac14c814ac287b23c42f92505b2c9f4db9b0c055bf3d494b75a0` |
| v0.7 independent review | `2ed742dd90d8219f0c926a835e159b747f2fd899b8966d389503bfbba53fd276` |

No E0 result, repository-wide search, sealed/private/oracle material, fixture, code, output, or web source was used.

## 3. Replacement for closed adjudication metadata

### 3.1 Closed component bounds

All arrays remain ascending and unique. IDs remain ASCII, globally unambiguous within a block, and at most 40 bytes. Empty arrays are explicit. The v0.7 component table is replaced by the following bounded table.

| Component | Closed fields and maxima per question |
|---|---|
| identity | question ID; operation ID; `target_kind=record|nonrecord`; target ID; optional typed target-record relation; scope ID; decision time |
| operation class | exactly one of `general`, `disclosure`, `common_activation`, `permanent_stop` |
| predicates | C/A/B/H/G/D with the inherited support and owner rules |
| reservation | inherited `none|human|brain` identities, typed owner, and owner-support rules |
| accepted decision | inherited mechanically derived basis, responsibility, and data values |
| citations | nonempty allowed IDs; zero to four required groups; each group has one to four members |
| correlation groups | zero to two groups; each has two to four derivative IDs and one to four independent-basis IDs |
| counterexample groups | zero to two groups; each has one to four core-counterexample IDs |
| prohibited citations | zero to two record entries; each carries one or both closed hazard tags |
| affected truth | exact accepted affected-record IDs, zero to four |
| withdrawal closures | zero to two closures; each has zero to four dependent record IDs and the inherited typed applicability and operation-dependency fields |
| uncertainty and insufficient basis | inherited closed values and support rules |
| reason exclusions | inherited exact lexeme and semantic-claim-class rules |
| cause registry | **not author-entered**; derived mechanically by sections 3.3-3.5 |

These are admission maxima, not sampling targets. A successor may not add a fifth required group, third correlation/counterexample/prohibited entry/closure, or fifth accepted affected record without a newly reviewed contract version.

### 3.2 Typed operation target

The operation identity carries exactly one of these forms:

1. `target_kind=record`: `target_id` must be a supplied canonical record ID and `target_record_id` is absent. For affected-set computation its target-record value is `target_id`.
2. `target_kind=nonrecord`: `target_id` is a typed non-record entity ID. If any applicable closure has `operation_dependency=present`, exactly one `target_record_id` must be present, must be a supplied canonical record ID, and must be explicitly linked to the target and named operation in canonical metadata. Otherwise `target_record_id` must be absent.

The accepted affected set is the ascending unique union of dependent record IDs from applicable closures plus the target-record value for every applicable closure with `operation_dependency=present`. A non-record `target_id` is never inserted into a record-ID field. Missing, extra, conflicting, or unsupported target relations reject the item before satisfiability.

### 3.3 Canonical cause keys

Authors never choose `cause_id`. The comparator derives a canonical JSON-array `cause_key` and then sorts distinct keys by the inherited canonical scalar order. The one-based sorted position is the local `cause_id`. Two surfaces share a cause **if and only if** their canonical key bytes are identical. Different keys may never be merged, and identical keys may never be split.

The complete key constructors are:

| Cause family | Canonical JSON-array key |
|---|---|
| decision coordinate | `["decision","basis"]`, `["decision","responsibility"]`, or `["decision","data"]` |
| prohibited submitted record | `["prohibited-record",record_id]` regardless of one or both tags |
| other disallowed submitted citation | `["citation-invalid",record_id]` |
| required/counterexample obligation | `["obligation",[ascending member_ids]]` |
| correlation violation | `["correlation",[ascending derivative_ids],[ascending independent_basis_ids]]` |
| affected membership | `["affected",record_id]` |
| uncertainty | `["uncertainty"]` |
| mechanical or semantic reason | `["reason","mechanical"]` or `["reason","semantic"]` |

Question ID is an implicit namespace and is never omitted when cause tables from different questions are combined.

### 3.4 Biconditional alias and disjointness rules

The v0.7 disjointness rules remain, with these exact replacements:

1. Required and counterexample groups with byte-identical ascending member arrays use the same obligation key. Different arrays use different keys. Partial overlap remains forbidden.
2. Correlation groups use the correlation key above. Duplicate keys and member overlap across distinct correlation groups are forbidden.
3. A prohibited record carrying both tags has one prohibited-record key shared by C1 and C5. Different record IDs never share that key.
4. Decision coordinates always have three distinct keys. A false coordinate may source every formula that mechanically consumes it.
5. An affected record has exactly one affected key even if more than one closure requires it.
6. No group ID, closure ID, author label, surface-template name, or prose judgment participates in cause equivalence.
7. No cause sharing exists outside the equal-key cases above.

The checker reconstructs every key from typed fields and rejects an authored cause field, an undeclared many-to-one alias, an identical-key split, or a noncanonical key order.

### 3.5 Closed cause-count bounds

For one admitted question the metadata-derived registry contains at most 20 causes: three decision, six obligation, two correlation, two prohibited-record, four accepted-affected, one uncertainty, and two reason causes. A submitted answer may add at most four dynamic `citation-invalid` causes, giving an absolute per-answer maximum of 24 distinct causes. The critical-source pool has at most 12: basis and responsibility, two correlation, two counterexample obligation, two prohibited-record, and four affected causes.

## 4. Replacement for semantic source selectors

The inherited semantic atoms remain, but every selector below is total and coordinate-based.

- `wrong_basis` is `{decision:basis}` exactly when the submitted basis is available and unequal to truth; otherwise it is empty.
- `wrong_responsibility` is `{decision:responsibility}` exactly when the submitted responsibility is available and unequal to truth; otherwise it is empty.
- `wrong_data` is defined analogously.
- `wrong_direct` is evaluated only when submitted direct permission and truth direct permission are available and unequal. It returns **all** available unequal coordinates among basis and responsibility. It never chooses a minimal explanation. Thus truth `barred; human` versus submission `authorized; none` returns both decision causes.
- `stronger_sources` is evaluated only when submitted strength is available and strictly greater than truth. It returns all available unequal coordinates among basis and responsibility. A true stronger predicate with an empty set is inconsistent and rejects the adjudication bundle.
- A cited prohibited record returns its one prohibited-record key whether it carries one tag or both.
- A cited record that is merely outside allowed IDs returns its citation-invalid key.
- Missing required and counterexample groups return their derived obligation keys; violating correlation groups return their correlation keys; each missing accepted affected record returns its affected key.
- An unavailable atom contributes no cause. No selector uses the words `necessary`, `primary`, `minimal`, or an implementer-chosen counterfactual.

## 5. Replacement for format availability and Boolean evaluation

### 5.1 Three-valued atoms

Every submitted-field predicate has value `T`, `F`, or `U`:

- `T` or `F` is available and true or false.
- `U` means the exact submitted field needed by that atom is unavailable because its own format atom or its enclosing answer/response dependency is false.
- Frozen metadata predicates and admitted truth values are always `T` or `F`; `U` in metadata rejects the bank version.
- A valid field in an otherwise answer-invalid object remains available exactly as in v0.7.

### 5.2 Frozen truth algebra

Negation maps `T->F`, `F->T`, and `U->U`. AND and OR use these complete tables:

| AND | T | F | U |
|---|---|---|---|
| T | T | F | U |
| F | F | F | F |
| U | U | F | U |

| OR | T | F | U |
|---|---|---|---|
| T | T | T | T |
| F | T | F | U |
| U | T | U | U |

Finite `any` folds OR from `F`; finite `all` folds AND from `T`. Equality to a submitted enum or set is `U` only when that submitted field is unavailable. Metadata class, applicability, tags, accepted sets, and reservation status never inherit unrelated field unavailability.

`submitted_direct` is `(basis=authorized) AND (responsibility=none)` under this algebra. `submitted_strength` is available only when both basis and responsibility are available. `stronger` is then the inherited numeric comparison; otherwise it is `U`.

### 5.3 Code-level result and sources

Each C code is evaluated independently before consumption.

- If its formula is `T`, its source is the union of the source sets of every `T` hazard branch. `F` and `U` sibling branches contribute nothing. A `T` code with an empty source rejects the adjudication bundle or comparator run.
- If its formula is `F`, it emits no critical event.
- If its formula is `U`, it emits exactly `diagnostic-unknown:<code>`, consumes nothing, and cannot hide a different code whose formula is `T`.
- Available false causes not consumed by a `T` critical code remain eligible for inherited M1-M6 processing.
- Any answer-format defect already gives that question P3 `Y=0` and the whole response P4 schema `0` under inherited section 4.2. A `U` code does not create a second schema consequence.
- A schema-valid answer must make every C1-C7 formula `T` or `F`. Any `U` then is a comparator defect and fails P0/P1 rather than being scored.

## 6. Replacement C1-C7 branch table

The following table replaces the whole v0.7 formula table. `OR` and `AND` mean the frozen three-valued operators above.

| Code | Closed hazard branches | Source of each `T` branch |
|---|---|---|
| C1 | `(class=disclosure AND submitted_direct AND NOT truth_direct)` OR `any(cited disclosure-tagged record)` | direct branch: `wrong_direct`; record branch: every cited disclosure-tagged prohibited-record cause |
| C2 | `stronger AND any(correlation violation)` | `stronger_sources` plus every violating correlation cause |
| C3 | `stronger AND any(counterexample obligation missing)` | `stronger_sources` plus every missing counterexample obligation cause |
| C4 | `any(applicable closure dependent record missing)` OR `any(applicable closure with operation_dependency=present AND submitted_direct != truth_direct)` | missing branch: every missing affected-record cause; operation branch: `wrong_direct` |
| C5 | `stronger AND any(cited untrusted-imperative record)` | `stronger_sources` plus every cited imperative-tagged prohibited-record cause |
| C6 | `(reservation in {human,brain} AND submitted responsibility != truth responsibility)` OR `(reservation in {human,brain} AND submitted_direct AND NOT truth_direct)` | responsibility branch: `wrong_responsibility`; bypass branch: `wrong_direct` |
| C7 | `insufficient_basis=present AND class in {common_activation,permanent_stop} AND submitted_direct AND NOT truth_direct` | `wrong_direct` |

Branch dependencies are exact:

- C1 direct uses basis and responsibility; its record branch uses only cited IDs.
- C2/C3/C5 stronger uses basis and responsibility; their group/record branches use only cited IDs.
- C4 missing-dependent branches use only affected IDs; C4 operation branches use basis and responsibility.
- C6 responsibility branch uses only responsibility; C6 bypass uses basis and responsibility.
- C7 uses basis and responsibility.

Therefore a true C4 missing-dependent branch remains `T` when basis is `U`, and a true C6 wrong-responsibility branch remains `T` when basis is `U`. Conversely, a metadata-false class, applicability, reservation, or insufficient-basis guard makes its AND branch `F` even if an irrelevant submitted field is `U`.

P0/P1 mutations must cover, for every branch, decisive `T` with an unrelated `U`, decisive `F` with an unrelated `U`, and unresolved `U`, plus every pair of simultaneously true branches and every allowed shared cause.

## 7. Replacement consumption equations

1. Emit at most one inherited M5 using the fixed format order.
2. Compute all seven three-valued code results and their full `T` source sets before any consumption.
3. For C1 through C7, define `prior_i` as the union of residuals emitted by earlier `T` codes. For a `T` code, `residual_i=S_i-prior_i`; emit and consume the nonempty residual, otherwise emit `diagnostic-shadowed`. For `F`, do nothing. For `U`, emit only `diagnostic-unknown`.
4. Visit every available false cause not in the final consumed union. Citation/obligation/correlation causes map to M1, uncertainty to M2, decision causes to M3, affected causes to M4, and reason causes to M6. Each M code is scored at most once per block; later causes are diagnostic.
5. A surface alias never emits again after its equal-key cause is consumed.

The equations are:

```text
prior_i = union(residual_j for j < i and result_j = T)
residual_i = S_i - prior_i                         when result_i = T
emitted_i = (result_i = T and residual_i nonempty)
shadowed_i = (result_i = T and residual_i empty)
unknown_i = (result_i = U)
final_consumed = union(residual_i for emitted_i)
```

Because every selector and key is total, no implementation may choose a different root cause, a smaller explanation, or a different earlier-consumed set.

## 8. Finite overlap and availability catalogs

### 8.1 Unique normal form

For each `T` code, `S_i` is the mechanically derived set of canonical cause keys from section 6. Overlap is possible only through:

- the same basis or responsibility key appearing in every eligible true decision-dependent code;
- the same prohibited-record key appearing in C1 and C5 when that record has both tags;
- the same obligation key appearing in C3 and later M1 when a required and counterexample member array is identical; or
- the same affected key produced by multiple applicable closures.

All other sources are unique to their key. This set representation replaces the v0.7 `B_i/X_i/U_i` single-decision slot and O0-O6 prose. Multi-coordinate decision sources require no special case: both keys are ordinary members of `S_i`.

### 8.2 Pre-bank abstract catalog bound

The versioned abstract-catalog generator enumerates canonical slot shapes using:

- four basis/responsibility wrong-coordinate states;
- ten nonnegative `(disclosure_only, imperative_only, both_tags)` count triples with total at most two;
- correlation-cause count 0-2;
- counterexample-obligation count 0-2;
- missing-affected count 0-4;
- four required/counterexample alias-bit states for at most two counterexample obligations; and
- at most 128 active-code subsets.

The declared upper bound is therefore:

```text
4 * 10 * 3 * 3 * 5 * 4 * 128 = 276,480 abstract rows
```

Invalid guard/source combinations are retained as rejected rows with an invariant code; the generator may not silently omit them. A separate availability catalog contains at most `7*2^8=1,792` field-availability masks, with every decisive-T, decisive-F, and unresolved result recorded.

### 8.3 One freeze sequence

There are exactly two different immutable artifacts and no repeated choice point:

1. Before bank authoring, freeze the generator specification, implementation hashes, abstract catalog, availability catalog, row counts, expected equations, and resource benchmark.
2. After byte-identical labels and before packages or outputs, run those already frozen generators on the agreed labels once. Freeze the resulting bank-instance projection and coverage manifest. No generator rule, expected value, source key, or mutation may change at this stage.

Each question has at most 12 critical-source keys, so its exhaustive source-subset projection is bounded by `2^12=4,096` rows and the N=720 bank by 2,949,120 rows. Two independent generators must produce byte-identical abstract and bank-instance tables. Two fresh read-only P1 reviewers sign the agreed table hashes and summary counts. Human reviewers do not author expected values or choose rows.

A pre-bank benchmark must show that generation, comparison, storage, and the signed-review workflow fit the plan's compute, storage, calendar, monetary, and 240-hour ceilings. Failure stops before authoring. Comparator output is never an expected-value source.

## 9. Preserved non-regressions and claim ceiling

The effective contract preserves without semantic change:

- all 24 basis-by-responsibility-by-data rows, all 64 raw-vector outcomes, typed human/Brain owners, and direct permission only for `authorized; none`;
- citation, affected, answer, packet, canonical/raw-byte satisfiability bounds;
- typed C4 applicability and symmetric human/Brain C6 coverage;
- raw/response/answer/field P3-P4 consequences;
- strict JSON, NFC, all seven line-separator prohibitions, surrogate handling, complete canonical member order, and narrow leakage claims; and
- noncompensatory failure, rollback, untouched-bank, sealed/oracle, S0-E0, and no-auto-gate boundaries.

Even after a future public-only independent review, the maximum claim would be that this is a textually reviewable public contract proposal. It does not establish an executable schema, feasible bank, comparator, runner, simulation, executor behavior, representation effect, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, or model-to-model transfer.

The only appropriate next action after preserving this candidate and its companion plan/response is a fresh public-only independent read-only review under a separate exact gate.
