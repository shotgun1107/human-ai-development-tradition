# S0 I0-I3 integration readiness audit v0.1

- `status`: CONTROL public readiness audit
- `audit_base_commit`: `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`
- `audit_base_tree`: `d1ed10e2e8e5e21a510322c002b69b9cf89de848`
- `audit_kind`: evidence-to-requirement mapping; no implementation or S0 run
- `sealed_content_access`: none
- `primary_verdict`: `NOT-READY-FOR-SEALED-S0`
- `next_readiness`: `READY-FOR-PUBLIC-ASSEMBLY-REHEARSAL-DESIGN`
- `new_low_level_i_stage_required`: no

## 1. Audit question and boundary

This audit asks one practical question: after integrating I0 through I3 into
main, what is the smallest remaining step toward the first valid S0 run?

It does not ask how to make every component maximally secure. It treats a
missing item as a blocker only when it prevents a valid S0 flow or creates a
concrete path by which an evaluation participant can see or infer denied F0
information.

This audit read only public protocol, freeze, integration, README, report,
manifest, and implementation-import evidence. It did not open, enumerate, or
search within the three F0 content families. Only their required aggregate
inventory, 32/11/10, was checked during the preceding main integration. No
fixture, oracle, condition map, executor output, judge output, provider/model
session, E0, or S0 input was read or created.

No I0-I3 verifier was rerun for this audit. Their accepted review and main
integration records are historical implementation evidence; the present work
is a composition and readiness assessment.

## 2. Authenticated public baseline

| Public evidence | SHA-256 | Audit use |
|---|---|---|
| root `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` | current F0 and Git boundary |
| canonical S0 protocol v0.3-r1 | `6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60` | required S0 sequence |
| protocol final-refreeze decision | `512714d8745bb78c08b0b6fd085f978c84fb0b7d2439dbbae0138d2f92ef9b90` | current protocol authority |
| SM0 freeze record | `db29efe079e7b6548b7afb6380cb548997a061da84009c235dfd5be220a5f033` | answer/common/overlay/fixture formats |
| SM1 freeze record | `cdbd9dc560da7a41dfc57ec885def730edcdc7718f483f23c60d6868ddef5d00` | question, transformation, access, run, scoring, and pre-review formats |
| I0/F0-PUBLIC refreeze decision | `a9863be66dd848e6a0eefba3be535a2ea1ef33f938abd3b37276cd1e0a4f2063` | public practice and minimum transform/validation freeze |
| I0 implementation manifest | `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae` | 15-file I0 payload |
| I1 CONTROL integration decision | `167a0bf4e4bf408ad0a01e9ee45273ffcb0b9a0c06e3b5a22e63e19978cd2925` | public runtime construction acceptance |
| I1 implementation manifest | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` | 26-file I1 payload |
| I2 v0.4 MAIN integration decision | `e01399099bc115ece01c19a6382dac407601acd557c95270c7b484873ad3f3bd` | public lifecycle and role-event acceptance |
| I2 v0.4 implementation manifest | `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6` | 16-file I2 payload |
| I3 v0.2 MAIN integration decision | `07dbc6cf90584abb95108ff2d26c525648fdafe3cde8b5e0093b0ebcb5cd2818` | public import-decision acceptance |
| I3 v0.2 implementation manifest | `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648` | 17-file I3 payload |

The audit base is the current local and published main tip after the exact I3
fast-forward. F0 aggregate counts at that tip are 32/11/10.

## 3. What is actually complete

The word `complete` below means complete only inside the stated public,
model-free construction boundary.

| Layer | Verified public capability | Status |
|---|---|---|
| protocol | two-block, four-condition, eight-fresh-session S0 logic; neutral answer; blind judging; fixed decision table | frozen current authority |
| SM0 | answer, common, overlay, and fixture schema formats | frozen |
| SM1 | question/options, transformation, answer-validation, access, run, scoring, and pre-review formats | frozen |
| F0-PUBLIC + I0 | public practice packages, deterministic P01-P04 transformation, integrity/schema checks, neutral answer validation | frozen public development harness |
| I1 | authenticated public topology/codecs, injected one-shot runner, bounded response and output behavior | accepted on main |
| I2 | public 31-field event codec, route lifecycle and set-level collision checks, global-link structure, fixed vector binding | accepted on main |
| I3 | public 21/26-field import records, ordered classification, I2 completion/global-link finalization | accepted on main |

I0-I3 therefore cover many isolated pieces of the S0 preparation problem.
They do not collectively prove an S0 execution path.

## 4. Composition finding

### Fact

The authenticated implementation manifests expose four separate Python
packages. Direct source-import inspection found:

- I0 does not import I1, I2, or I3;
- I1 does not import I0, I2, or I3;
- I2 does not import I0, I1, or I3; and
- I3 imports I2, but not I0 or I1.

I1 deliberately accepts an injected transport and does not implement a
provider or model session. I0 validates public transformation and answer
format. I2 and I3 validate structural role/import records. No accepted public
entry point currently performs the protocol sequence from public package
selection through one-shot execution, run-record capture, neutral answer
validation, and final receipt.

### Inference

The main readiness gap is not another low-level codec, trust-root record, or
classification rule. It is the absence of one minimal composition path that
demonstrates the existing parts can be assembled without widening any input or
authority boundary.

Passing unit tests in four repositories-within-the-repository cannot substitute
for one end-to-end public assembly rehearsal.

## 5. Protocol sequence versus present evidence

| Protocol step | Present evidence | Readiness |
|---|---|---|
| canonical protocol freeze | canonical-r1 final refreeze decision | complete |
| answer and manifest formats | SM0 and SM1 freeze records | complete |
| public practice and deterministic transform | F0-PUBLIC/I0 freeze | complete |
| public runtime and bounded one-shot behavior | I1 | component complete |
| public role/import structural checks | I2 and I3 | component complete |
| one composed public-practice flow | no accepted entry point or run record | missing |
| actual common/overlay/run manifest instances for the chosen model/session | only schema formats are established in this audit | missing before live rehearsal |
| sealed canonical inputs, oracle, scoring, and condition map | outside this audit's allowed inputs | unknown, not presumed absent or valid |
| external pre-execution sealed review `S0-04` | no admissible public readiness evidence used here | unverified |
| eight fresh executor sessions | explicitly not created | missing before S0 |
| frozen answers and run records | no S0 execution | missing before S0 |
| fresh blind judge and scoring | no S0 execution | missing before S0 |
| CONTROL condition restoration and decision table | no S0 execution | missing before S0 |

The correct present conclusion is therefore not `S0 ready`. It is `public
component set ready for a bounded assembly rehearsal`.

## 6. Required, optional, and excessive work

### 6.1 Required now

1. Define one minimal public-only assembly rehearsal using the already frozen
   public practice bundle.
2. Specify exact handoffs among I0 transform/answer validation, I1 one-shot
   runner, and only the I2/I3 checks that are actually needed for a public run
   record.
3. Produce one explicit run-state machine covering reserve, invoke once,
   validate, record, and fail-closed cleanup.
4. Define deterministic success evidence: exact input/output hashes, one run
   record, no retry, no denied input, and byte-identical repeat for a stubbed
   transport path.
5. Keep provider/model use closed during the first model-free assembly check.

This work may be a very small adapter or controller. It must not duplicate the
existing I0-I3 grammars or grow into a central-system implementation.

### 6.2 Required before a sealed S0 run

1. A trusted external F0 verifier must attest, without exposing contents to
   CONTROL or executor A-D, that the exact sealed candidate, oracle, scoring,
   and access records are present, internally valid, and mutually bound.
2. `S0-04` must conduct the protocol's fresh pre-execution review and return
   only the authorized result and evidence hashes.
3. Exact model, reasoning level, time/output limits, prompts, opaque condition
   paths, common manifest, overlays, and eight run manifests must be frozen.
4. Eight fresh executor sessions must receive only their one condition/block
   package; no executor may inherit F0, CONTROL, another executor, or judge
   context.
5. Answers and run records must be frozen before a fresh blind judge receives
   its exact allowlist.
6. CONTROL must restore condition identities only after blind accuracy results
   are frozen and then apply the fixed decision table once.

These are direct S0 validity requirements. Their absence would permit
evaluation contamination or make the result uninterpretable.

### 6.3 Useful but not required for the first S0

- automated fresh-session provisioning;
- process or account isolation in addition to conversation/input isolation;
- signed public receipts and automated manifest handoffs;
- a provider adapter replacing manual session transfer;
- durable run-record storage and automated dashboarding.

They reduce operator error and improve repeatability, but the first S0 can be
valid without them if the exact role allowlists and fresh-session rules are
manually enforced and independently checked.

### 6.4 Unnecessary over-implementation for the current threat model

The following are not blockers for the first synthetic S0 merely because they
could make a larger system more secure:

- real Ed25519 key generation or private-key custody;
- a production trust-root or signer registry;
- a durable global ledger, atomic append, rollback-resistant witness, or
  project-lifetime uniqueness service;
- one VM per role, hostile same-process resistance, or OS-level ACL proof;
- production database, RAG, UI, network service, or Project Brain integration;
- actual appliance or raw-media infrastructure.

None directly improves the experiment if the evaluation AIs never receive the
denied F0 inputs and a trusted external role supplies only pass/fail and pinned
hashes. Building these before the public assembly rehearsal would continue the
component-review loop without testing the experiment's actual flow.

## 7. Complexity and maintenance risks

### Fact

Some component README and author verification reports still describe a future
review even though later independent review and integration records on main
supersede that status. Current-policy precedence makes the integration records
authoritative, but a reader who opens only a component README can infer a stale
gate state.

### Inference

The project now has stronger evidence for individual byte contracts than for
their composition. Adding I4, I5, or more cryptographic sublayers before one
public end-to-end rehearsal would increase:

- stale-status and cross-document interpretation cost;
- the chance that a later component changes an interface assumed by another;
- review time without proportional experimental evidence; and
- the risk that S0 preparation becomes an independent infrastructure project.

Stale README cleanup is useful but not a blocker for the public rehearsal.
Changing frozen or historical files merely for consistency would create more
review work and is not recommended in this gate.

## 8. Decision

### Facts accepted

- Protocol, SM0, SM1, F0-PUBLIC/I0, I1, I2, and I3 have accepted public
  evidence on the current main lineage.
- No accepted public entry point composes I0, I1, I2, and I3 into one rehearsal
  flow.
- No sealed S0 execution, eight-executor run, blind judgment, or scoring result
  exists in the evidence admitted to this audit.

### Decision

1. **Do not run sealed S0 yet.**
2. **Do not create a new low-level I4 security subsystem.**
3. **Proceed to one minimal public end-to-end assembly rehearsal design.**

The rehearsal must use only public practice data and must initially remain
model-free. Its purpose is to prove wiring, handoffs, fail-closed behavior, and
run-record production, not to compare A-D effectiveness.

## 9. Exact next gate

The recommended next exact gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN OPEN`

That gate should produce one bounded design defining component calls, exact
public inputs, outputs, state transitions, failure rules, and success evidence.
It must not read F0 content, create an oracle, invoke a provider/model, create
executors, score A-D, or run S0.

If the design cannot connect the accepted components without changing their
public contracts, it must identify the one smallest adapter change instead of
opening a new general implementation phase.

## 10. Maximum claim

The current main lineage contains individually accepted public S0 preparation
components through I3 and is ready for public-only assembly rehearsal design.
It is not ready for a sealed S0 execution, and this audit supplies no central-
system, Project Brain, operational-safety, economic-value, production, or
model-to-model-transfer evidence.
