# S0 v0.14 role-position isolation matrix v0.1

- `status`: design candidate
- `design_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN OPEN`
- `source_topology`: authenticated I1 `public-runtime-v0.14.json`
- `claim_kind`: public identity and isolation design only

## 1. Identifier model

This matrix closes the identity distinction needed by a later implementation.

- `role_row_id` is one of the 32 frozen aggregated topology rows.
- `position_label` is `single`, `A`, `B`, `1`, or `2` exactly as assigned by
  the frozen row.
- `role_position_id` is the ASCII concatenation
  `<role_row_id>:<position_label>`. There are exactly 40.
- `section4_signer_id` is one of the frozen 22 registry IDs or `none`.
- `invocation_id` globally identifies one future actor instance and binds to
  exactly one role position. There is no separate serialized actor-instance
  identifier, and it does not change the 40-position count.
- `vm_id` identifies the new VM used by one invocation. It is never a role
  or signer identity.

The `control-root-authority` signer is outside the 32 rows and 40 positions.
It has no experimental edge and no invocation multiplicity.

## 2. Exact row-position-signer binding

| Row order | Role row ID | Position | Role position ID | Section-4 signer ID | Isolation notes |
|---:|---|---|---|---|---|
| 1 | `registrar` | `single` | `registrar:single` | `control-registrar` | Receipt/status infrastructure; no protected payload |
| 2 | `public-status-reader` | `single` | `public-status-reader:single` | `none` | Terminal read-only |
| 3 | `public-record-publisher` | `single` | `public-record-publisher:single` | `public-record-publisher` | Publication only; no raw/label/map input |
| 4 | `public-record-reader` | `single` | `public-record-reader:single` | `none` | Terminal read-only |
| 5 | `content-intake` | `single` | `content-intake:single` | `content-intake` | Protected future content custodian |
| 6 | `simulation-builder` | `single` | `simulation-builder:single` | `simulation-builder` | Must precede future bank contents |
| 7 | `fact-author` | `single` | `fact-author:single` | `none` | Future fresh authoring role |
| 8 | `label-authors` | `A` | `label-authors:A` | `none` | Paired; never sees B result |
| 8 | `label-authors` | `B` | `label-authors:B` | `none` | Paired; never sees A result |
| 9 | `label-comparison` | `single` | `label-comparison:single` | `label-comparison` | Separate from both label authors |
| 10 | `representation-builder` | `single` | `representation-builder:single` | `representation-builder` | Denied labels/expected values |
| 11 | `package-builder-scanner-1` | `single` | `package-builder-scanner-1:single` | `none` | Compound row is intentionally one position |
| 12 | `scanner-2` | `single` | `scanner-2:single` | `none` | Denied scanner-1 result |
| 13 | `scan-comparison` | `single` | `scan-comparison:single` | `scan-comparison` | Separate from both scanners |
| 14 | `leakage-reviewers` | `1` | `leakage-reviewers:1` | `none` | Paired; never sees reviewer 2 result |
| 14 | `leakage-reviewers` | `2` | `leakage-reviewers:2` | `none` | Paired; never sees reviewer 1 result |
| 15 | `leakage-comparison` | `single` | `leakage-comparison:single` | `leakage-comparison` | Separate from both reviewers |
| 16 | `comparator-builders` | `1` | `comparator-builders:1` | `comparator-builder-1` | Paired; own vault/key only |
| 16 | `comparator-builders` | `2` | `comparator-builders:2` | `comparator-builder-2` | Paired; own vault/key only |
| 17 | `expected-catalog-generators` | `1` | `expected-catalog-generators:1` | `none` | Paired; never sees generator 2 result |
| 17 | `expected-catalog-generators` | `2` | `expected-catalog-generators:2` | `none` | Paired; never sees generator 1 result |
| 18 | `catalog-comparison` | `single` | `catalog-comparison:single` | `catalog-comparison` | Separate from both generators |
| 19 | `p1-reviewers` | `1` | `p1-reviewers:1` | `none` | Paired; never sees review 2 |
| 19 | `p1-reviewers` | `2` | `p1-reviewers:2` | `none` | Paired; never sees review 1 |
| 20 | `p1-review-comparison` | `single` | `p1-review-comparison:single` | `p1-review-comparison` | Separate from both reviewers |
| 21 | `condition-map-schedule-custodian` | `single` | `condition-map-schedule-custodian:single` | `none` | Holds future semantic map; strongly separated |
| 22 | `blinded-map-builders` | `1` | `blinded-map-builders:1` | `none` | Paired; pre-call map access only |
| 22 | `blinded-map-builders` | `2` | `blinded-map-builders:2` | `none` | Paired; pre-call map access only |
| 23 | `analysis-map-comparison` | `single` | `analysis-map-comparison:single` | `analysis-map-comparison` | Separate from map builders and analysis |
| 24 | `dispatcher-transport-recorder` | `single` | `dispatcher-transport-recorder:single` | `none` | Future transport exception requires separate gate |
| 25 | `public-executor` | `single` | `public-executor:single` | `none` | Position template; future per-run fresh external sessions plus local custody |
| 26 | `raw-output-custodian-anonymizer` | `single` | `raw-output-custodian-anonymizer:single` | `none` | Sees raw output, not labels/map/comparator logic |
| 27 | `semantic-judges` | `1` | `semantic-judges:1` | `semantic-judge-1` | Paired; future manual Project-only Pro session plus local custody |
| 27 | `semantic-judges` | `2` | `semantic-judges:2` | `semantic-judge-2` | Paired; future manual Project-only Pro session plus local custody |
| 28 | `judgment-comparison` | `single` | `judgment-comparison:single` | `judgment-comparison` | Separate from both judges |
| 29 | `comparator-operators` | `1` | `comparator-operators:1` | `comparator-operator-1` | Paired; own comparator only |
| 29 | `comparator-operators` | `2` | `comparator-operators:2` | `comparator-operator-2` | Paired; own comparator only |
| 30 | `adjudication-comparison` | `single` | `adjudication-comparison:single` | `adjudication-comparison` | Separate from both operators |
| 31 | `analysis` | `single` | `analysis:single` | `analysis` | No semantic map; frozen anonymous analysis only |
| 32 | `final-decision-custodian` | `single` | `final-decision-custodian:single` | `final-decision-custodian` | Receives map only after authenticated E48 |
| non-row | `control-root-authority` | non-row | not a role position | `control-root-authority` | Offline registry signing only |

The table has 40 experimental positions, 21 experimental section-4 signer
bindings, 19 `none` bindings, and one non-row root signer, totaling the exact 22
registry signer IDs.

## 3. Section-4 and inherited signature scopes

The 22-entry registry governs only the exact generic-envelope scope inherited
from v0.14 section 4. It does not silently redefine every predecessor artifact
described as “signed.”

The section-4 scope includes the root registry envelope, registrar status
envelopes, the frozen evidence-receipt producer roles and artifact kinds, E42,
E43, E44, E45, E54, and E56 as specified by v0.14.

Public grants and other predecessor artifacts described as signed but outside
that generic-envelope scope retain an inherited signing specification. The
currently accepted public I1 topology does not supply a total replacement key
and preimage mechanism for those artifacts. This design records that scope as
`inherited-signature-unresolved`; it does not add signers to registry v1,
declare those artifacts unsigned, or authorize their implementation. The
execution package cannot freeze until a separately gated design resolves every
such inherited signature without changing the 22-entry section-4 registry.

## 4. Exact store ACL inventory

Writer does not imply read or list. Every reader grant is object-, edge-, and
phase-scoped. The exact inventory is 27 writers and 46 explicit reader entries.

| Store | Only writer | Explicit readers |
|---|---|---|
| `registrar-receipt-vault` | registrar, named status-evidence edges | registrar, E51 bundle construction only |
| `registrar-store` | registrar, E51 | public status reader, E52 |
| `public-decision-store` | public record publisher, E54 | public record reader, E55 full; registrar receives only the E56 publication-receipt object capability |
| `content-vault` | content intake, E04 | label A, label B, representation builder, E06 |
| `label-vault-A` | label A, E07 | label comparison, E07 |
| `label-vault-B` | label B, E07 | label comparison, E07 |
| `agreed-label-vault` | label comparison, E09 | generators 1/2 E10; leakage reviewers 1/2 E11; judges 1/2 and comparator operators 1/2 E12 |
| `representation-vault` | representation builder, E13 | package builder E15; condition-map custodian E13 |
| `signed-package-vault` | package builder, E16 | scanner 2 E18; leakage reviewers 1/2 E22; condition-map custodian E32 |
| `scan-vault-1` | package builder/scanner 1, E17 | scan comparison, E20 |
| `scan-vault-2` | scanner 2, E19 | scan comparison, E20 |
| `leakage-vault-1` | leakage reviewer 1, E23 | leakage comparison, E23 |
| `leakage-vault-2` | leakage reviewer 2, E23 | leakage comparison, E23 |
| `comparator-vault-1` | comparator builder 1, E25 | comparator operator 1, E25 |
| `comparator-vault-2` | comparator builder 2, E25 | comparator operator 2, E25 |
| `generator-vault-1` | generator 1, E26/E28 | catalog comparison, E26/E28 |
| `generator-vault-2` | generator 2, E26/E28 | catalog comparison, E26/E28 |
| `analysis-input-vault` | simulation builder, E03 | analysis, E46 after calibration freeze |
| `catalog-vault` | catalog comparison, E27/E29 | P1 reviewers 1/2 E27/E29; comparator operators 1/2 E29 |
| `p1-review-vault-1` | P1 reviewer 1, E30 | P1 comparison, E30 |
| `p1-review-vault-2` | P1 reviewer 2, E30 | P1 comparison, E30 |
| `condition-map-vault` | condition-map custodian, E33 | blinded-map builders 1/2 E33 before calls; final decision E49 only after the E48 payload/hash, producer receipt, and corresponding E51 `A-0fff` status pair all authenticate and commit |
| `analysis-map-vault` | analysis-map comparison, E35 | analysis, E47 |
| `raw-output-vault` | dispatcher, E39 | raw-output custodian, E39 |
| `judgment-vault-1` | semantic judge 1, E42 | judgment comparison, E42 |
| `judgment-vault-2` | semantic judge 2, E42 | judgment comparison, E42 |
| `final-decision-vault` | final decision, E50 | public record publisher, E53 |

The `public-decision-store` registrar entry is not a directory read and grants
no decision-record bytes. It is an E56 object capability for the exact
publication-receipt material the publisher sends to the registrar. This closes
the otherwise overbroad interpretation of `receipt-artifacts-only`.

E43 and E45 ordered deliveries and the E48 protected analysis payload are
direct recipient artifacts, not new stores. Airlock disks, temporary paths,
logs, key containers, and VM disks are security-control components, not extra
experimental stores. Input/output/staging disks are TCB-controlled temporary
replicas with frozen retention deadlines and may not retain a protected payload
after their defined transfer or quarantine period. Signer key containers are
separate campaign-lifetime custody components and never hold role vaults or
protected artifact copies beyond one signing request.

The 27 writers and 46 readers above are experimental logical ACL entries. Four
distinct least-privilege TCB principals—input route controller,
ingestion/export verifier, trusted-staging verifier, and immutable-store
committer—and the host administrator have physical byte capability, not
semantic reader authority. They do not share a wildcard credential. Any
wildcard, parent listing, cross-store search, discretionary access, recipient
choice, or human semantic inspection invalidates the campaign. Signer
appliance/provider/anti-replay components and the root are separate TCB domains,
not mediation principals or experimental readers.

## 5. Edge and phase invariants

- The edge inventory remains exactly E00A-E00H and E01-E56. A fan-out or split
  delivery does not create a new edge ID.
- E25, E27, E29, E35, E48, and E50 split protected payload from public receipt.
  The registrar receives only the receipt leg.
- Comparator vault 1 is visible only to operator 1; comparator vault 2 only to
  operator 2. No paired producer reads the other's output.
- The condition-map custodian is separated from executor, dispatcher, raw
  custodian, judges, comparator operators, analysis, and final decision.
- Analysis receives the blinded analysis map, not the semantic condition map.
  Final decision receives E49 only after the E48 payload/hash and signed
  producer receipt authenticate and the registrar's corresponding E51
  status-envelope/bundle pair commits as state `A-0fff`.
- Raw output goes only to the raw custodian through the named vault. Judges and
  comparator operators receive the E40 anonymous semantic projection; analysis
  receives the E41 anonymous timing/byte projection.
- E51 and E54 are atomic pair operations in the future backend. Partial or
  duplicate acceptance is forbidden.

## 6. Co-location prohibitions

Different role positions never share a process, interpreter, session,
conversation root, credential set, VM instance, writable root, output disk, or
role-local state. The intentionally compound
`package-builder-scanner-1:single` row is the sole intra-row combination
already frozen by v0.14.

In addition:

- the two members of every paired row have separate lineage roots, principals,
  VM instances, key containers where applicable, and human-visible results;
- the root authority shares none of those resources with an experimental
  position or registrar;
- the registrar is never co-located with a protected-payload holder;
- each comparison custodian is separate from every producer it compares;
- dispatcher and executor are separate;
- analysis and final decision are separate; and
- future executor actor instances are fresh per condition/block/run unit, do
  not fork from a fixture author or another executor, and cannot read another
  executor transcript or output.

The single `public-executor:single` topology position is a role template, not a
claim that one actor instance handles every future run. It expands to exactly
eight future invocation/external-session pairs, four conditions times two
blocks; each handles one unit and at most three run concurrently.

The external model session used by a future executor or semantic judge is not
inside the local Hyper-V trust boundary. It needs its own fresh-session,
no-memory, no-tool, exact-input controls at the later execution or manual-judge
gate. The Hyper-V environment protects local package custody, transport, and
output ingestion; it does not turn a provider project into a local VM.
This remains `external-provider-isolation-unresolved` and blocks execution-
package freeze until a provider-specific independent review closes it.

Actor VMs, campaign-lifetime signer appliances, the non-row root environment,
and TCB infrastructure are distinct domains. A signer appliance binds to one
section-4 signer ID, never runs an actor role, and exposes only its frozen
domain-restricted, anti-replay signing interface. A private key never enters an
actor VM.

## 7. Later machine-readable realization

The isolation implementation must derive and freeze machine-readable
inventories for role positions, signer bindings, store ACLs, exploded transfer
legs, isolation domains, co-location constraints, and key lifecycle. Those
files must be generated from and tested against this authenticated table and
the I1 topology; they may not become a second source of discretionary role,
store, edge, or signer semantics.
