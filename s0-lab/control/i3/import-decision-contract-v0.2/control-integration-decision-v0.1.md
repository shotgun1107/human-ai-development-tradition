# S0 v0.14 I3 public import-decision contract v0.2 CONTROL integration decision v0.1

- `status`: CONTROL integration decision
- `decision_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT V0.2 CONTROL INTEGRATION DECISION OPEN`
- `decision_input_commit`: `f999454e226d075d8643a5b75a1b7fa93d27acea`
- `decision_input_tree`: `8042b9ae14f0dfd72cd5b6a1f5c884139d7a2731`
- `design_commit`: `9df5bf8ae4a834fdcb0ca0b89eb03d0e04a6e5bb`
- `independent_rereview_commit`: `f999454e226d075d8643a5b75a1b7fa93d27acea`
- `decision`: `ACCEPT-FOR-MAIN-INTEGRATION-CONSIDERATION-ONLY`
- `implementation_status`: closed

## 1. CONTROL decision

CONTROL accepts the authenticated I3 v0.2 public design package and its fresh
zero-finding independent rereview as eligible for a separate main integration
decision.

This decision does exactly three things:

1. recognizes the four v0.2 design artifacts as the current proposed I3 public
   design baseline, replacing v0.1 for future I3 interpretation;
2. records the independent closure of `I3-IR-B01`, `I3-IR-M01`, and
   `I3-IR-M02`; and
3. permits only a separately opened main integration decision gate.

It does not merge or fast-forward main, open implementation, create code or
fixtures, authorize a real import, or open any execution gate.

## 2. Authenticated decision inputs

| Artifact | SHA-256 | CONTROL use |
|---|---|---|
| root `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` | current role, publication, and F0 boundary |
| canonical text validator | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` | public artifact validation |
| I3 boundary v0.1 | `9a638245f57fe49b4e3557748f0b37d097d794acc9d9650bac7fc7ea2af50aae` | exact I3 scope and review-loop limits |
| v0.1 independent review | `572c9b41f4a5d6ee09f46ae5909554252f166b6aa27a78ad0f2e6ca04dfecd1c` | three predecessor findings |
| v0.2 main contract | `f04dae684b7373a4c613c3f0e357ef8266f0bf307e78e78d105cb04168f61594` | complete successor contract |
| v0.2 field-and-binding table | `b034fadf16e7b5d11594c6987ba714e791ef2b2d02409589c6e7b90126e2fa02` | exact field sources and bindings |
| v0.2 classification table | `82f787c737f0a255970679b4c501b93061de7b7778e10843d71c047aa69ea706` | total ordered classification and finalization |
| v0.2 implementation/test brief | `182df459eee2877d5c4710794ad7a7c86a56a44abe7ce14d09e629fc1c29ac62` | future bounded implementation target |
| v0.2 independent rereview | `e915ed191a685afe9d6cfbc905f38ab589090535f4435a88a80ddf5d093b9fac` | fresh zero-finding disposition |
| I2 v0.4 machine-readable contract | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` | unchanged 31-field event authority |

All seven admitted Markdown/sidecar pairs passed the authenticated canonical
validator after its SelfTest passed all eleven cases. Every input hash matched
the recorded bytes before this decision was written.

## 3. Git and evidence lineage

The decision input lineage is linear:

```text
d2167aebe6b295b99982bed15f5a0d79720c899d
  -> 9df5bf8ae4a834fdcb0ca0b89eb03d0e04a6e5bb
  -> f999454e226d075d8643a5b75a1b7fa93d27acea
```

- `d2167ae` contains the authenticated v0.1 independent review;
- `9df5bf8` adds exactly the four v0.2 design artifacts and sidecars; and
- `f999454` adds exactly the fresh independent rereview and sidecar.

The decision worktree began clean at `f999454`, tree
`8042b9ae14f0dfd72cd5b6a1f5c884139d7a2731`, with sole parent `9df5bf8`.
No candidate or review input was modified during CONTROL consideration.

## 4. Finding dispositions

### 4.1 `I3-IR-B01`: closed

V0.2 defines one exact rule compatible with I2:

- a uniquely selectable internally canonical frame always contributes `H`;
- normal end plus exact evidence reaches its explicit class with `H`;
- unknown or not-started end with that same unique frame reaches
  `disagreement/H`;
- malformed, incomplete, oversized, or non-unique bytes use `Z`; and
- abnormal end retains first-precedence `crash/Z` and ignores apparent bytes.

The independent rereviewer reproduced these branches and found no residual
I2-event incompatibility.

### 4.2 `I3-IR-M01`: closed

V0.2 has one media representation: an immutable finite sequence of byte
strings. Count is derived only from sequence length. Empty, one-member, and
multiple-member sequences enter the classification table; malformed outer or
member types return only `I3_INPUT_ERROR`. No separate count exists that can
contradict supplied bytes.

### 4.3 `I3-IR-M02`: closed

V0.2 does not invent configuration-hash fields in I2. The two configuration
hashes are validated inside the exact outcome tuple. The recomputed full-frame
hash `H` commits those bytes, and the actual I2 field
`outcome_frame_sha256=H` carries that commitment. Z-bearing classes make no
configuration-hash claim.

### 4.4 New findings

The fresh independent rereview reported:

- blocking: 0;
- major: 0; and
- minor: 0.

Its exact verdict was
`PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`.

## 5. Accepted I3 v0.2 design boundary

CONTROL accepts only these public deterministic claims:

- one exact 21-line admission grammar;
- one exact 26-line outcome grammar;
- the exact body hash, full `H`, final LF, and 2,048-byte zero-tail rule;
- preservation of the exact I2 v0.4 31-field event contract;
- one typed media-sequence representation;
- exact pre-pending behavior and nine total ordered pending rows;
- exact `H/Z` and I2 before/after state mapping;
- separation of classification from completion finalization; and
- destination authority only for accepted plus exact consumed event plus
  persisted append.

The v0.1 design remains historical evidence. It is not a competing current
authority and cannot be selected instead of v0.2.

## 6. Noncompensatory conditions

Main integration consideration is allowed only while all of the following
remain exact:

1. the four v0.2 design hashes and rereview hash in section 2;
2. the linear design-to-rereview ancestry in section 3;
3. finding count zero in the authenticated rereview;
4. unchanged I2 v0.4 contract hash and 31-field event;
5. no modification to the inherited PUBLIC-GIT F0 inventory; and
6. no implementation, fixture, oracle, provider/model, E0, or S0 claim.

Any mismatch blocks main integration consideration. A later commit or merge
cannot repair an input mismatch by silently replacing the reviewed bytes.

## 7. Gates that remain closed

This CONTROL decision does not authorize:

- I3 code, parser, serializer, classifier, finalizer, test harness, manifest,
  or generated cases;
- raw media, host/appliance observation, durable ledger/witness, project-
  lifetime uniqueness, or atomic append;
- registry authority, key generation, signatures, VM/platform/provider
  enforcement, or model sessions;
- F0 content access, fixture/oracle authoring, executor/judge work, E0, or S0;
- main merge, fast-forward, PR, release, or branch deletion; or
- central-system or Project Brain implementation.

The current claim remains public design acceptance only. It is not evidence
that any operational system obeys the contract.

## 8. Decision and next gate

**Decision: `ACCEPT-FOR-MAIN-INTEGRATION-CONSIDERATION-ONLY`.**

The exact next permissible gate is:

`S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT V0.2 MAIN INTEGRATION DECISION OPEN`

That gate may decide whether the authenticated I3 v0.2 design lineage should
be integrated into main. It does not itself perform a merge or fast-forward,
and it cannot open implementation automatically.

## 9. Maximum claim

CONTROL has accepted the zero-finding I3 v0.2 public design package for a
separate main integration decision. No implementation, platform behavior,
actual authority, F0/E0/S0 result, or production readiness has been validated.
