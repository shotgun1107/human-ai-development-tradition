# S0 v0.14 I3 public import classification table v0.2

- `status`: bounded public design revision candidate
- `design_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT V0.2 BOUNDED DESIGN REVISION OPEN`
- `responds_to_review_sha256`: `572c9b41f4a5d6ee09f46ae5909554252f166b6aa27a78ad0f2e6ca04dfecd1c`
- `claim_kind`: total deterministic classification design only
- `implementation_status`: not opened

## 1. Decision boundary

This table is subordinate to the complete v0.2 main contract and the unchanged
I2 v0.4 contract with SHA-256
`713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da`.
It classifies supplied public facts; it does not observe reality, append an
event, or grant authority.

`Z` is 64 ASCII zeroes. `H` is SHA-256 of one uniquely selectable internally
canonical 26-line outcome frame including final LF.

## 2. Typed-input gate

A valid `ClassificationFactSet` contains:

- one `last_durable_phase` in `reserved`, `admission-frozen`, `pending`;
- one `end_observation` in `not-started`, `normal`, `abnormal`, `unknown`;
- one immutable finite `outcome_media_observations` sequence whose every
  member is exact bytes;
- exactly eight status fields in `exact`, `conflict`, `unavailable`; and
- optional admission evidence that is absent or exact bytes.

The sequence length is the only `observed_media_count`; no independent count
argument exists. Empty, one-member, and multiple-member sequences are valid
classification inputs. A wrong container, lazy/unbounded producer, non-byte
member, invalid enum, missing required member, or non-byte admission argument
returns stable `I3_INPUT_ERROR` before classification.

Noncanonical bytes are not a type error. They are well-typed evidence handled
by the ordered rows.

## 3. Pre-pending rows

| Row | Predicate | Class/hash/states | Required completion |
|---|---|---|---|
| `PRE-R` | phase `reserved` | `none`, `Z`, `none/none` | exact I2 direct terminal from reserved |
| `PRE-A` | phase `admission-frozen` | `none`, `Z`, `none/none` | exact I2 direct terminal from admission-frozen |

Outcome bytes are not interpreted. Final disposition is terminal only after
the exact event is persisted; otherwise it is `no-completion-claim`. No retry
or destination authority exists.

## 4. Pending scan derivations

| Derived value | Exact definition |
|---|---|
| `observed_media_count` | length of `outcome_media_observations` |
| `sole_medium` | the sole member only when count equals one |
| `medium_exact` | sole medium exists and length is exactly 2,048 bytes |
| `schema_prefix_count` | exact outcome-schema-prefix occurrences in sole medium; zero otherwise |
| `complete_at_zero` | byte zero begins a structurally complete 26-LF-line block |
| `complete_candidate_count` | structurally complete candidates beginning at schema prefixes |
| `candidate_end` | byte after LF terminating line 26 when one candidate begins at zero |
| `nonzero_tail` | any nonzero byte from candidate end through byte 2047 |
| `canonical_frame` | unique candidate at zero passes grammar, body hash, route, and tuple validation |
| `H` | full-frame SHA-256 of `canonical_frame` including final LF |
| `external_exact` | end is normal, admission canonical and matching, every cross-binding exact, all eight statuses exact |

`complete_at_zero` is structural only. A complete block with a bad field,
value, order, body hash, or tuple is noncanonical and cannot be missing.

## 5. Complete ordered pending rows

Earlier rows have strict precedence.

| Order | Row | Predicate after all earlier rows failed | Class | Hash | Event state pair |
|---:|---|---|---|---|---|
| 1 | `P-CRASH` | end is `abnormal` | `crash` | `Z` | `SRC/indeterminate` |
| 2 | `P-MISSING` | end normal; count one; medium exactly 2,048 bytes; no duplicate predicate; medium all zero or neither complete block at zero nor complete candidate elsewhere | `missing` | `Z` | `SRC/indeterminate` |
| 3 | `P-DUPLICATE` | count greater than one, or sole medium has more than one schema prefix, more than one complete candidate, or nonzero tail after a complete candidate at zero | `duplicate` | `Z` | `SRC/indeterminate` |
| 4 | `P-DISAGREE-H` | exactly one internally canonical frame begins at zero with zero tail, but `external_exact=false`, including end unknown/not-started | `disagreement` | `H` | `SRC/indeterminate` |
| 5 | `P-DISAGREE-Z` | `canonical_frame=false`; examples are empty sequence, wrong medium length, no unique canonical frame under unknown/not-started end, complete noncanonical block, sole nonzero-offset candidate, bad body hash, illegal tuple, or other malformed/incomplete/non-unique bytes | `disagreement` | `Z` | `SRC/indeterminate` |
| 6 | `P-PARSE-REJECTED` | `external_exact=true`; canonical tuple `rejected/parse-rejected` | `parse-rejected` | `H` | `SRC/SRC` |
| 7 | `P-VALIDATION-REJECTED` | `external_exact=true`; canonical tuple `rejected/validation-rejected` | `validation-rejected` | `H` | `SRC/SRC` |
| 8 | `P-STATE-COMMIT-FAILED` | `external_exact=true`; canonical tuple `rejected/state-commit-failed` | `state-commit-failed` | `H` | `SRC/indeterminate` |
| 9 | `P-ACCEPTED` | `external_exact=true`; canonical tuple `accepted/none` | `accepted` | `H` | `SRC/DST` |

Rows 6-9 are reachable because their frame is canonical and their external
evidence is exact. Row 4 requires non-exact external evidence; row 5 requires
no canonical frame. The predicates are therefore disjoint.

## 6. Finding-specific hostile traces

### 6.1 `I3-IR-B01`: one canonical frame under uncertain end evidence

| Input | Result |
|---|---|
| one canonical frame, zero tail, all bindings/statuses exact, end `unknown` | `P-DISAGREE-H`, `disagreement`, `H` |
| same but end `not-started` | `P-DISAGREE-H`, `disagreement`, `H` |
| one complete block with bad body hash, end `unknown` | `P-DISAGREE-Z`, `disagreement`, `Z` |
| one partial frame, end `unknown` | `P-DISAGREE-Z`, `disagreement`, `Z` |
| two canonical-looking frames, end `unknown` | `P-DUPLICATE`, `duplicate`, `Z` |

The first two rows preserve the exact I2 rule: a unique internally canonical
frame remains identified as `H` even when host-end evidence conflicts or is
unavailable.

### 6.2 `I3-IR-M01`: media representation

| Typed input | Derived count | Result |
|---|---:|---|
| empty byte-string sequence | 0 | `P-DISAGREE-Z` |
| one all-zero 2,048-byte member, normal end | 1 | `P-MISSING` |
| one canonical-frame member | 1 | later row by end/bindings/tuple |
| two byte-string members | 2 | `P-DUPLICATE` |
| count supplied separately | not admitted | `I3_INPUT_ERROR`; no count parameter exists |
| one sequence member that is not bytes | not derived | `I3_INPUT_ERROR` |

No accepted call can contain a contradictory caller-supplied count and bytes.

### 6.3 `I3-IR-M02`: configuration hashes

| Evidence | Exact check |
|---|---|
| outcome before/after configuration hashes | validate only against the four canonical outcome tuples |
| I2 completion for an H-bearing class | compare actual event field `outcome_frame_sha256` to recomputed `H` |
| direct I2 configuration-hash equality | forbidden because the 31-field event has no such field |
| Z-bearing class | no selected frame and no configuration-hash claim |

## 7. General overlap traces

| Observation | Result and reason |
|---|---|
| abnormal end plus valid-looking frame | crash/Z; abnormal evidence is first |
| normal end plus two zero media | duplicate/Z; missing requires one medium |
| normal end plus one partial 12-line write | missing/Z; no complete candidate |
| normal end plus complete block with bad body hash | disagreement/Z; complete but internally invalid |
| canonical frame plus nonzero tail | duplicate/Z; no frame selected |
| canonical accepted frame plus wrong campaign | disagreement/H; unique canonical frame, external binding conflict |
| canonical rejection plus unavailable witness snapshot | disagreement/H; unique canonical frame, external evidence unavailable |
| canonical frame only at nonzero offset | disagreement/Z; not selectable at byte zero |
| one exact accepted frame, normal end, every binding/status exact | accepted/H; destination still unavailable until finalization |

## 8. Classification result

Every successful classification returns:

| Output | Exact domain |
|---|---|
| `last_durable_phase` | copied closed phase |
| `outcome_class` | `none`, `accepted`, three named rejections, `crash`, `missing`, `duplicate`, or `disagreement` |
| `outcome_frame_sha256` | exactly tabled `H` or `Z` |
| `before_appliance_state` | `none` pre-pending; `SRC` post-pending |
| `after_appliance_state` | `none`, `DST`, `SRC`, or `indeterminate` exactly as tabled |
| `required_completion_kind` | direct-terminal-reserved, direct-terminal-admission-frozen, terminal-rejected, or consumed-accepted |
| `destination_authority` | always unavailable at classification time |

This in-memory result is not a new serialized experimental record.

## 9. Finalizer

| Order | Classification | Exact event/append | Disposition | Destination |
|---:|---|---|---|---|
| 1 | pre-pending `none` | phase-matching direct terminal; persisted | `terminal-rejected` | unavailable |
| 2 | `accepted` | consumed/accepted with `C`, `H`, `SRC/DST`; persisted | `consumed-accepted` | `DST` available |
| 3 | non-accepted pending class | terminal/rejected with `C`, required `H/Z`, tabled states; persisted | `terminal-rejected` | unavailable |
| 4 | any | missing, malformed, mismatching, conflicting, unavailable, failed, or unpersisted completion | `no-completion-claim` | unavailable |

The event comparison uses only actual I2 fields. `H` commits the whole frame,
including configuration hashes. The finalizer does not change classification,
redraw IDs, infer persistence, or retry.

## 10. Totality obligations

A later implementation must demonstrate:

1. every well-typed input selects exactly one pre-pending or pending row;
2. identical input always selects the same row;
3. missing and duplicate never overlap;
4. complete malformed bytes never become missing;
5. one canonical frame plus uncertain/conflicting external evidence always
   uses disagreement/`H`;
6. `Z` never replaces an identifiable unique canonical frame except crash,
   whose precedence explicitly ignores apparent bytes;
7. only exact accepted/consumed/persisted makes `DST` available; and
8. malformed API objects produce only `I3_INPUT_ERROR`.

No implementation or test is run under this gate.

## 11. Closed boundary

This design does not implement platform observations, persistence, actual
authority, VM/provider isolation, F0, fixture/oracle, E0, or S0.
