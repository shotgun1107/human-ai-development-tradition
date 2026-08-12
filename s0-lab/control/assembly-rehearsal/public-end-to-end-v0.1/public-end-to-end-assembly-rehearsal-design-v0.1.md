# S0 v0.14 public end-to-end assembly rehearsal design v0.1

- `status`: public design candidate; independent review required
- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN OPEN`
- `design_base_commit`: `f7048e919ab0e698d78ca4ff4cc4eb31ca6f612c`
- `design_base_tree`: `92745e5f7a5f61c24e47501f1a0147c8f889bd61`
- `active_baseline`: `central-system-v2.1-s0-preparation`
- `execution_status`: not executed
- `F0_content_access`: none

## 1. Purpose

This design closes one narrow composition gap identified by the authenticated
I0-I3 integration-readiness audit. I0 through I3 each have accepted public,
model-free evidence, but no accepted entry point currently demonstrates a
single public-practice flow from transformation through one-shot response
capture, answer validation, and a deterministic run record.

The rehearsal answers only this question:

> Can the accepted public components be wired into one deterministic,
> fail-closed, model-free public-practice flow without widening their existing
> input or authority boundaries?

It does not run S0, estimate S0 effects, exercise F0, create an oracle, call a
provider or model, create an executor or judge, or implement the central
system or Project Brain.

## 2. Authenticated design inputs

| Input | SHA-256 | Use |
|---|---|---|
| I0-I3 integration-readiness audit v0.1 | `0ca3e51e8a566a94ed168325d18f5fe6196a132de5c4c6979c8ab7348483ffbf` | composition decision and scope |
| I0 implementation manifest | `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae` | transformation and answer-validation implementation |
| I1 implementation manifest | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` | authenticated input and one-shot runner implementation |
| I2 v0.4 implementation manifest | `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6` | public import-event contract baseline |
| I3 v0.2 implementation manifest | `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648` | public import-decision contract baseline |
| I2 public contract | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` | exact I2 preflight |
| I3 public contract | `ae834becfc393e4f525265aff473ae32d12f349713fb48b2e0bb60ea39fc7ac8` | exact I3 preflight |
| frozen public-practice bundle manifest | `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637` | public input file authentication |

The future implementation verifier must receive the implementation-manifest
digests as external pins. Discovering nearby hashes and immediately trusting
them is not sufficient.

## 3. One fixed public practice case

The first rehearsal has exactly one case. There is no case selection during a
run.

| Item | Exact value |
|---|---|
| block | `BLK-PRACTICE0002` |
| representation | `P01` |
| canonical input | `s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/canonical-input.json` |
| canonical SHA-256 | `bf8e48e1bed4c061df7de896aa14848cdeab6692288a2eda5b445c1a87557863` |
| transformed package | `s0-lab/public-practice/v0.1/packages/P01B2EMBR001/input.json` |
| package SHA-256 | `15bace158828b8a16a4fd9d76dddfa7b5870bdb580198f0da308c4fa575e03b7` |
| questions | `s0-lab/public-practice/v0.1/runner/BLK-PRACTICE0002/questions.json` |
| questions SHA-256 | `661c09dfb20ea933f521370f9e3f94e2512f49e67020101d3767a6a92a07fe90` |
| public stub response | `s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/expected-answer-P01.json` |
| response SHA-256 | `c2f824c6483b625e2fa50d0016443632809471f32ebb235e09f454cf04981bdf` |
| answer schema | `s0-lab/control/sm0/answer.schema.json` |
| answer schema SHA-256 | `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` |

Every path above is public and already within I0's authenticated allowlist.
No path under an F0 content family is an input to this design or rehearsal.

## 4. Component disposition

### 4.1 I0: active data-path component

The controller must call `verify_public_bundle(workspace_root)`. It then reads
only the fixed canonical input, questions, transformed package, public answer,
and answer schema named in section 3.

It must call:

1. `transform_canonical(canonical_object, "P01")`;
2. compare the returned bytes exactly with the frozen package bytes; and
3. after the one-shot response, call
   `validate_answer_candidate_bytes(...)` with the exact schema, questions,
   and package paths.

Any transform-byte mismatch or non-empty validation-error list fails the
rehearsal.

### 4.2 I1: active data-path component

The controller must use I1's existing public authentication functions to bind
one exact rehearsal request manifest and one exact request file. It then calls
`run_one_shot` exactly once with an injected public stub transport.

The fixed I1 policy remains unchanged:

- invocation limit: 1;
- retry limit: 0;
- tool count: 0;
- state mode: none;
- response selection: first final response only;
- maximum response bytes: 8,192; and
- maximum response frames: 256.

The public stub emits exactly one `ResponseFrame`, containing the authenticated
public answer bytes, with one fixed response ID and `final=true`. It performs no
network, provider, model, tool, browser, or filesystem lookup during
`invoke_once`.

### 4.3 I2 and I3: authenticated public-baseline preflight only

I2 and I3 describe signer-media import records. This rehearsal reads an
already authenticated public-practice bundle from the repository; no signer
media, appliance, registry activation, or import attempt occurs.

Creating a synthetic `accepted` signer-import route merely to claim that I2
and I3 were exercised would give unrelated public data false signer-state
semantics. The design therefore requires only these exact calls during
preflight:

1. I2 `verify_contract_file` on
   `s0-lab/i2/spec/trust-root-role-isolation-contract-v0.4.json`; and
2. I3 `verify_contract_file` on
   `s0-lab/i3/spec/import-decision-contract-v0.1.json`.

The run record must state:

- `i2_disposition=contract-authenticated-no-import-route`; and
- `i3_disposition=contract-authenticated-no-import-attempt`.

No I2 route context, event, ledger, witness, or identifier is created. No I3
admission, outcome, classification, completion event, or destination authority
is created. This is an explicit non-applicability decision, not a PASS claim
about runtime isolation or signer import.

## 5. The one permitted adapter

The smallest missing component is one public assembly controller. It may be
implemented in a successor gate under a new rehearsal namespace, but must not
modify I0, I1, I2, I3, their manifests, or their frozen contracts.

The controller has five responsibilities only:

1. authenticate the fixed public inputs and component pins;
2. deterministically assemble the request envelope;
3. bind that exact request through I1's manifest-grant path;
4. reserve, invoke once, validate, and commit one run record; and
5. expose stable, independently testable failure labels.

It must not become an I4 security subsystem, provider adapter, generalized
workflow engine, database, ledger, signer, executor provisioner, or S0 runner.

## 6. Deterministic request envelope

The implementation gate must materialize one frozen request artifact and one
same-directory manifest. The request artifact is reconstructed at runtime and
must compare byte-for-byte with the frozen artifact before I1 authentication.

The logical object has exactly these keys:

1. `schema_id`: `S0-PUBLIC-ASSEMBLY-REQUEST-1`
2. `rehearsal_id`: `S0-PUBLIC-AR-B2-P01-001`
3. `block_id`: `BLK-PRACTICE0002`
4. `representation_id`: `P01`
5. `input_package_sha256`: the exact section 3 package hash
6. `questions_sha256`: the exact section 3 questions hash
7. `input_package`: the parsed frozen package object
8. `questions`: the parsed frozen questions object

Serialization is UTF-8 without BOM, JSON object keys recursively sorted,
`ensure_ascii=true`, separators `,` and `:`, no insignificant whitespace, and
exactly one final LF. Duplicate JSON keys in either source object reject before
serialization.

The manifest contains exactly one lowercase SHA-256 row for the request file,
uses ASCII/LF, has one final LF, and is externally pinned by the controller's
reviewed configuration. The I1 grant has exactly that one allowed path and the
purpose `s0-public-assembly-rehearsal-v01`.

## 7. Run state machine

The controller implements exactly this state progression:

1. `NEW`
2. `PREFLIGHT_AUTHENTICATED`
3. `REQUEST_RECONSTRUCTED`
4. `OUTPUT_RESERVED`
5. `INVOKED_ONCE`
6. `RESPONSE_CAPTURED`
7. `ANSWER_VALIDATED`
8. `RECORD_COMMITTED`
9. `COMPLETE`

The transition rules are:

- `NEW -> PREFLIGHT_AUTHENTICATED` only after all component manifests,
  public-input hashes, I2 contract, and I3 contract match.
- `PREFLIGHT_AUTHENTICATED -> REQUEST_RECONSTRUCTED` only after I0 transform
  bytes match the frozen P01 package and the reconstructed request matches the
  frozen request artifact.
- `REQUEST_RECONSTRUCTED -> OUTPUT_RESERVED` uses exclusive creation. An
  existing output is a pre-invocation failure and produces zero transport
  calls.
- `OUTPUT_RESERVED -> INVOKED_ONCE` is the sole call to I1 `run_one_shot`.
- `INVOKED_ONCE -> RESPONSE_CAPTURED` requires one response identity, one final
  frame, non-empty strict JSON object bytes, and clean iterator close.
- `RESPONSE_CAPTURED -> ANSWER_VALIDATED` requires zero I0 answer-validation
  errors.
- `ANSWER_VALIDATED -> RECORD_COMMITTED` writes and fsyncs the canonical run
  record into the already reserved output.
- `RECORD_COMMITTED -> COMPLETE` requires close success and a final hash of the
  persisted record.

There is no transition back to an earlier state and no retry transition.

## 8. Failure and cleanup rules

Every failure is assigned to one of these stable classes:

- `AR-AUTH`: component, manifest, source, or request authentication failure;
- `AR-TRANSFORM`: I0 transform bytes differ from the frozen package;
- `AR-RESERVE`: output reservation fails or collides;
- `AR-INVOKE`: transport construction, call, stream, bound, or cleanup fails;
- `AR-RESPONSE`: response is incomplete, noncanonical, or not the fixed public
  response;
- `AR-ANSWER`: I0 returns one or more answer-validation errors;
- `AR-RECORD`: canonical record write, fsync, close, or final read-back fails;
- `AR-BOUNDARY`: a denied path, provider/model, tool, network, F0, executor,
  judge, oracle, key, signer, ledger, or unsupported I2/I3 action is requested.

On any failure after reservation and before committed close, the controller
closes the descriptor and removes the incomplete reservation. Cleanup failure
replaces any success claim with `AR-RECORD`. The original operational error is
retained as the primary diagnostic when cleanup also fails. A failed execution
is never resumed and is never retried under the same execution identity.

## 9. Canonical run record

The successful record is one strict JSON object serialized with the same JSON
rules as the request envelope. It contains exactly the logical field set
specified in `assembly-rehearsal-interface-map-v0.1.json`; the canonical
serializer orders those keys recursively. It contains no timestamp,
random identifier, host path, username, provider metadata, or environment
secret.

Important values include:

- the fixed rehearsal and case identity;
- baseline commit and four implementation-manifest hashes;
- bundle, canonical, package, questions, request-manifest, request, expected
  response, and actual response hashes;
- `transport_calls=1`, `retry_count=0`, `response_frames=1`,
  `final_frames=1`;
- `answer_validation_error_count=0`;
- the exact I2 and I3 non-applicability dispositions;
- `denied_input_access_count=0` within the verifier-observed allowlist; and
- `result=public-assembly-rehearsal-pass-not-s0`.

The record is structural evidence only. It does not contain answer scoring,
condition identity, model quality, a signer decision, or an S0 result.

## 10. Deterministic repeat

The implementation review runs the controller twice in two newly created,
empty, ephemeral output roots using the same authenticated public inputs and
the same stub transport.

Each execution has exactly one transport call and zero retries. The second
execution is an independent repeat, not a retry of the first. The two canonical
run-record byte streams and SHA-256 values must be identical. Only one record
is retained as the candidate evidence artifact; the verifier reports both
digests and equality.

Any nondeterministic field, different byte, second call inside one execution,
or cleanup residue fails the rehearsal.

## 11. Denied boundaries

The design and future first rehearsal deny all of the following:

- the three F0 content families and any hidden oracle;
- synthetic or canonical sealed fixtures;
- provider, model, network, browser, MCP, tool, or conversation session;
- executor A-D, judge, scoring, condition map, and S0 decision logic;
- keys, signatures, trust-root activation, signer media, durable ledger,
  witness, VM, sandbox, ACL, or actual role isolation;
- E0, central-system, Project Brain, production, safety, economic-value, and
  model-transfer work.

The verifier may inspect only the exact public paths named by its reviewed
allowlist. It must not enumerate or open F0 contents to prove non-access.

## 12. Outputs and next gate

This gate produces design records only. It does not produce the request
artifact, controller code, transport, run record, or test result.

The next gate, after an independent review returns an acceptable verdict, may
be a bounded public implementation gate for this one controller and its public
stub. That later gate still may not invoke a provider/model or run S0.

Maximum present claim:

> A public-only, model-free I0/I1 assembly rehearsal and honest I2/I3
> contract-preflight boundary have been specified for independent review. No
> rehearsal or S0 execution has occurred.
