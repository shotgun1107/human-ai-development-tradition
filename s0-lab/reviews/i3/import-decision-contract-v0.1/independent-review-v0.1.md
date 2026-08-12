# S0 v0.14 I3 public import-decision contract independent review v0.1

- `review_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT INDEPENDENT REVIEW OPEN`
- `review_role`: fresh independent public design reviewer
- `baseline_branch`: `codex/s0-i3-public-import-decision-contract-independent-review`
- `baseline_head`: `c1af996699287c86d5142a96873eedfd78815d4e`
- `baseline_tree`: `8698ed0b1488085a7bb0e8fa39cb96e3188c6e28`
- `baseline_parent`: `620f3afaa8dd7c35a55f73465df885f8f4e8d6d7`
- `initial_status_count`: `0`
- `verdict`: `REVISE-AND-REVIEW`

## 1. Review boundary and method

I did not author or advise on the I3 design and did not treat its conclusions
as an answer key. I read only the 25 authenticated inputs listed below. I did
not search or enumerate the repository, read any F0 path or prior I3 review,
use outside sources, implement code, create fixtures or an oracle, or run a
platform, provider, model, import, E0, or S0 operation.

I independently reconstructed the two new byte grammars, raw-medium scan,
ordered classification, `H/Z` choice, event-state mapping, and completion
finalizer. I then traced hostile cases against the authenticated v0.3 text and
the exact I2 v0.4 machine-readable contract.

## 2. Authenticated inputs

All supplied SHA-256 values matched before substantive reading:

| Input | SHA-256 |
|---|---|
| `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` |
| `verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |
| I3 boundary Markdown | `9a638245f57fe49b4e3557748f0b37d097d794acc9d9650bac7fc7ea2af50aae` |
| I3 boundary sidecar | `8f0f71e1f2887463d17ba46fba7f8c53c4bcc638c631c200354cc044c1cae5fc` |
| I3 main contract Markdown | `1786b97b36988894d0fcd5083e9657502cb9ba2443fcde4909f2f261c6a1bd83` |
| I3 main contract sidecar | `753eb01f7d57f0371ac01c5d4babfbddbbd3f4af89b971d0a1afb86ae5e851bd` |
| I3 field/binding table Markdown | `e19156d4ce73be157649213e8f90fbd05ea9d3b59b6c346acba61a409cdb2ab3` |
| I3 field/binding table sidecar | `4e06b27075e545c59bbbfe0e337da43875401f13dbf6c1611f7c1f7c720ce6bf` |
| I3 classification table Markdown | `3251273da2c9f7f05968a4b1bf08ef4808dc9387682ba8b7b0c84977454003b3` |
| I3 classification table sidecar | `6a4ef7b0148647c4ee9b0de6b6b04e3afc061de0fe977f60f87a0fa950863ffc` |
| I3 implementation/test brief Markdown | `694efd7a93080d1d536d9005db5bcd9859fcf86f6ed7748d947eb14f78aac101` |
| I3 implementation/test brief sidecar | `1d5095d9af73ad724c9e663f57ee4c73c9c95b15a48f756476abae679923adf7` |
| v0.3 design Markdown | `a6fd2575052b6cbc4ae9b3a29f27f1b2338a4e6a7044285e89725eeee215b66b` |
| v0.3 design sidecar | `90b2643bd2128339261ea0eae6c334ae757d5fa096cae3e9d73b8ff7ae606757` |
| v0.3 authority matrix Markdown | `5553758d0a4bdab2dd8e747b931830287e3f522437f944b838bf87f037dc7d5a` |
| v0.3 authority matrix sidecar | `14ad4440f996f6b637b8adb667b3975a9040ee70d8da503d5be700646438d72b` |
| v0.3 acceptance addendum Markdown | `bd14249f524f37444cc4a82b676505f640492b5244d920a78fcd2820a71cebe3` |
| v0.3 acceptance addendum sidecar | `d2bac18a3bef1ec769e9f97149fa6d74bd4536b7454151ec6113fe355f9a86d7` |
| v0.4 design Markdown | `5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3` |
| v0.4 design sidecar | `8332a01452c3207321e48b6fde5736ed2ecccda493474ae05cd51f5723fad545` |
| v0.4 authority matrix Markdown | `19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8` |
| v0.4 authority matrix sidecar | `22333a6d80cd32ddd60947c6ade212331eece9b1e067958fc2264d1882f20f9a` |
| v0.4 acceptance addendum Markdown | `f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73` |
| v0.4 acceptance addendum sidecar | `3765f11d814d1fbacb55b3a3600f642c51d4d2a16d5012bfaa7ba9680fe9f03d` |
| I2 v0.4 JSON contract | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` |

The authenticated validator self-test returned `SELF_TEST=PASS`. Each of the
11 admitted Markdown/sidecar pairs returned every independently labeled check
as `PASS` and `OVERALL=PASS`. The I2 JSON passed strict UTF-8 decoding, strict
JSON parsing with duplicate-member rejection, and semantic checks for schema
and version, the unique 31-field event order, the 21 non-root signer IDs, the
three route mappings, and the predecessor's three I3-unsupported boundaries.

## 3. Independent reconstruction

### 3.1 Admission

The authenticated v0.3 ordered block has exactly 21 emitted `name=value`
lines: the displayed sequence continues through `admission_event_id` and
`decision`, so there is no alternate 19-line interpretation. I3 freezes the
same order and lexical form without changing v0.3. Every line, including line
21, ends in LF. The record hash covers all 21 lines and the final LF.

The three route maps reconstruct uniquely as:

| Class | `SRC` | `DST` |
|---|---|---|
| `preactivation-context-v1` | `key-generated` | `pop-context-bound` |
| `registry-binding-v1` | `pop-issued` | `registry-bound` |
| `activation-binding-v1` | `registry-bound` | `active` |

The admission binds campaign, ceremony, one of the 21 non-root signer IDs,
class and mapped states, package hash and object, capability, result-medium
kind and ID, distinct `R/A/P/C`, outcome schema and 2,048-byte limit. Its
`admission_event_id` is byte-equal to `A`, not a sixth event ID.

### 3.2 Outcome and medium

The outcome has one unique 26-line strict ASCII/LF grammar. The body hash is
SHA-256 of lines 1 through 25 including the LF after `reason`; `H` is SHA-256
of all 26 lines including the final LF. A frame begins at raw-medium byte zero,
ends within exactly one 2,048-byte medium, and all remaining bytes are zero.
Padding is excluded from `H`.

The only canonical tuples are accepted/none with `SRC -> DST` and unequal
nonzero configuration hashes; parse or validation rejection with `SRC -> SRC`
and equal nonzero hashes; and state-commit failure with
`SRC -> indeterminate`, nonzero before hash, and zero after hash.

### 3.3 I2 state and finalization mapping

The exact I2 mapping is pre-pending `none/none`, accepted `SRC/DST`, parse and
validation rejection `SRC/SRC`, and state-commit failure, crash, missing,
duplicate, or disagreement `SRC/indeterminate`. Pre-pending routes use the
exact direct terminal from `reserved` or `admission-frozen` and cannot infer a
post-pending outcome.

Classification and finalization are separate. Only an `accepted`
classification plus the exact matching I2 `consumed/accepted` completion using
`C` and `H`, plus append status `persisted`, makes `DST` available. Every
non-accepted class requires the matching terminal variant for a terminal
claim; missing, conflicting, unavailable, failed, or unpersisted completion
yields `no-completion-claim`. No retry, redraw, replacement event, inferred
append, event after consumed/terminal, or experimental topology expansion is
permitted.

## 4. Hostile traces

| Trace | Reconstructed result |
|---|---|
| pending, abnormal end, any apparent bytes | `crash`, `Z`; apparent frame ignored |
| normal, one 2,048-byte all-zero medium | `missing`, `Z` |
| normal, one partial LF-terminated write | `missing`, `Z` |
| normal, one complete malformed frame at zero | `disagreement`, `Z` |
| normal, one candidate only at nonzero offset | `disagreement`, `Z` |
| more than one medium, prefix, or candidate | `duplicate`, `Z`; no selection |
| canonical frame with a nonzero tail | `duplicate`, `Z` |
| unique canonical frame with a bad external binding | `disagreement`, `H` |
| bad body hash or illegal tuple | `disagreement`, `Z` |
| accepted tuple and all classification bindings exact | `accepted`, `H`, but destination still unavailable |
| accepted plus exact consumed event and persisted append | `consumed-accepted`; `DST` becomes available |
| any class plus missing, mismatching, or unpersisted completion | `no-completion-claim`; destination unavailable |
| reserved or admission-frozen | `none`, `Z`, exact direct terminal only; no retry |

Two additional traces expose substantive contradictions and are findings
below.

## 5. Findings

### `I3-IR-B01` — blocking — unique canonical frame has contradictory `H/Z` under uncertain end evidence

Take a well-typed pending fact set with exactly one 2,048-byte medium, exactly
one internally canonical outcome frame at byte zero, zero tail, canonical
admission and matching identities, and all status fields `exact`. Set only
`end_observation=unknown` (the same defect exists for `not-started`).

The main contract section 8.4 says disagreement uses `H` whenever exactly one
internally canonical frame is uniquely selectable but an external admission,
host, state, event, anti-replay, ledger, or witness fact is not exact. The
authenticated I2 v0.4 rule likewise requires `H` for disagreement with one
uniquely selectable internally canonical frame that conflicts with host
evidence. But classification row `P-DISAGREE-BYTES` includes `unknown` and
`not-started` and mandates `Z`; the representative and test lists repeat that
choice.

Thus the same admitted bytes and facts select one class but two exact frame
hashes. The finalizer consequently cannot construct one exact I2 terminal
event: its `outcome_frame_sha256` is either `H` or `Z`. This is an exact I2
event incompatibility, not a presentation issue. Freeze one rule consistent
with the unchanged I2 unique-frame rule, update every table and test, and
rereview.

### `I3-IR-M01` — major — the media count/bytes contradiction is both an API input error and a classified attempt

The classification table's typed-input gate requires bytes only when count is
one and no bytes otherwise. Violating that relationship is therefore a
malformed fact-set object and must yield only `I3_INPUT_ERROR`; the main
contract also excludes malformed fact-set objects from experimental
classification. Yet the raw-medium rules and `P-DISAGREE-BYTES` explicitly
admit a media count/bytes contradiction and classify it as `disagreement` with
`Z`.

For example, `outcome_media_count=0` with present bytes, or count one with
absent bytes, is either outside the well-typed domain or inside the ordered
classification domain. Both cannot be normative. A conforming implementation
may therefore return an API error or an I2-bound terminal classification for
the same call. Define one typed representation and one outcome for every
count/bytes combination, then align the interface, table, and tests.

### `I3-IR-M02` — major — a required outcome-to-event configuration-hash binding names event fields that do not exist

The field/binding table says the outcome's
`before_configuration_state_sha256` and `after_configuration_state_sha256`
bind the post-pending event before/after configuration hashes, and `I3-B09`
requires outcome-to-completion matching of states and configuration hashes.
The authenticated I2 v0.4 event grammar has exactly 31 fields and contains no
configuration-hash field. I3 correctly forbids adding to or competing with
that grammar. Therefore this required event binding has no destination field
and cannot be implemented or tested without either dropping the binding or
changing I2.

This is not repaired by comparing the outcome tuple internally: that is a
different check and does not satisfy the stated cross-object event binding.
Revise the binding table and test brief to identify the actual authenticated
object, if any, that supplies these hashes, or remove the impossible event
binding while preserving the exact I2 event grammar.

## 6. Disposition

Substantive finding count: three — one blocking and two major. No minor finding
is reported. The package is fail-closed with respect to acceptance, but it is
not one deterministic byte-compatible contract because the required I2 event
hash differs on an admitted hostile trace, the API/classification domain is
contradictory, and one mandatory cross-binding is unimplementable.

`REVISE-AND-REVIEW`

## 7. Evidence limits and next permissible gate

This review establishes only a public design finding disposition within the
I3 boundary. It does not validate an implementation, durable ledger or
witness, project-lifetime uniqueness, atomic append, real authority, VM or
platform enforcement, provider/model behavior, protected material, F0, E0,
S0, the central system, Project Brain, operational safety, economic value, or
model-to-model transfer.

The exact next permissible gate is a separately opened fresh independent I3
design rereview after CONTROL revises and freezes the four public design
artifacts and sidecars for these findings. This review does not open CONTROL
integration, implementation, fixtures, execution, commit, push, merge, or any
later experimental gate.
