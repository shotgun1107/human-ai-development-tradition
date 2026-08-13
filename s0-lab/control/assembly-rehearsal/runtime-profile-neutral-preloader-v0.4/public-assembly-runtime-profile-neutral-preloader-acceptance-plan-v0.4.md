# Public Assembly Runtime Profile + Neutral Preloader Acceptance Plan v0.4

Status: design-level acceptance obligations; no implementation or probe executed

## 1. Purpose and gate order

This plan defines the evidence needed to judge whether v0.4 closes
`RPNP3-RR-001` and `RPNP3-RR-002`. It authorizes no implementation, build,
runtime materialization, native call, platform probe, or rehearsal.

The gate order is:

1. authenticate the exact v0.4 design package;
2. complete a fresh independent public-design rereview;
3. require zero unresolved BLOCKING or MAJOR findings;
4. obtain a separate implementation gate;
5. authenticate source, build, imports, binaries, semantic validator, and
   runtime files before compilation or execution;
6. complete source, binary/import, schema, semantic, and mutation review;
7. obtain a separate bounded real-Windows platform-probe gate; and
8. only after all earlier gates pass, reconsider an official public assembly
   rehearsal.

No later gate follows automatically from an earlier one.

## 2. Package authentication

The v0.4 package is valid review input only if:

- all six logical artifacts match the exact package manifest;
- all Markdown and JSON sidecars match same-basename artifact bytes;
- the canonical text validator SelfTest passes before artifact validation;
- all JSON parses with duplicate-key rejection;
- `runtime-profile-v0.4.schema.json` passes Draft 2020-12 metaschema
  validation;
- package rows are exact, ASCII-sorted, unique, hash-correct, and exclude the
  manifest and sidecars;
- every externally supplied predecessor and rereview-record pin reproduces;
  and
- the reviewer reads only the literal CONTROL-supplied public allowlist.

Any mismatch, incomplete pin, unauthorized path, F0 access, or input repair is
`INVALID-REVIEW` before semantic judgment.

## 3. Finding-closure matrix

| Finding | Required v0.4 evidence | Failure condition |
|---|---|---|
| `RPNP3-RR-001` | Exact responsibility split: authenticated preloader constructs the only five-entry attribute list; pinned kernel applies it; future platform probe checks omitted decoys; guard validates only five known handles and makes no process-wide absence claim | Guard still claims unknown-handle enumeration; no exact process-creation tuple; no decoy probe; caller-controlled or unbound list |
| `RPNP3-RR-002` | Closed schema requires every predecessor/package, platform, source/build/import, binary/loaded-image, handle, guard, admission, atomic-root, terminal, and semantic-relation predicate | A schema-valid profile can omit or weaken a promised predicate, or semantic relations need no authenticated validator |

## 4. Responsibility-allocation review

The reviewer must independently classify every inheritance proposition as one
of these exact classes:

| Proposition | Responsible evidence |
|---|---|
| Five locator values identify five known live handles | v0.4 guard |
| Known handle kind, access, state, object and process identity | v0.4 guard |
| Ordered five-element inheritance request was constructed | authenticated preloader source/binary plus launch evidence |
| `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` was passed with exact count and size | authenticated preloader source/binary plus launch evidence |
| Opposite ends and unrelated handles were omitted from that list | authenticated preloader construction review |
| Omitted inheritable decoys are unusable in the child | pinned kernel semantics plus later real-platform probe |
| No unknown sixth handle exists, as a guard-side observation | explicitly not claimed |

The design fails if a proposition is assigned to an observer that lacks the
required input or API, if two owners silently assume each other's result, or
if a CONTROL/preloader assertion is mislabeled as guard observation.

## 5. Process-creation and handle-list evidence

### 5.1 Future source and binary audit

The separately gated implementation review must prove exactly one verifier
process-creation path with:

- direct authenticated `kernel32.dll!CreateProcessW` import;
- `STARTUPINFOEXW` and `EXTENDED_STARTUPINFO_PRESENT`;
- exactly one attribute-list entry;
- attribute ID `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`;
- ordered array length five and x64 byte length 40;
- `bInheritHandles=TRUE`;
- flags exactly `CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT |
  EXTENDED_STARTUPINFO_PRESENT | CREATE_NO_WINDOW`;
- `STARTF_USESTDHANDLES` clear;
- exact application, writable command-line, environment, current-directory,
  mitigation, token, security, and job inputs;
- no alternate process creation, shell, loader, callback, plugin, environment,
  or caller-selected handle-list route; and
- immutable attribute-list and handle-array storage until the call returns.

Any alternate route, dynamic resolution, extra attribute, changed count/size,
standard-handle route, or caller-controlled list rejects.

### 5.2 Required design mutations

Each mutation must be shown to violate the design/interface/schema:

- 4 or 6 handles;
- array byte length other than 40;
- reordered roles;
- wrong role, kind, or access predicate;
- extra attribute-list entry;
- wrong attribute ID;
- `bInheritHandles=false`;
- missing `EXTENDED_STARTUPINFO_PRESENT`;
- `STARTF_USESTDHANDLES` set;
- omitted `CREATE_NO_WINDOW`;
- an opposite pipe end in the list;
- an unrelated inheritable handle in the list;
- mutable or caller-provided array storage;
- unbound evidence digest or current-PID/success-policy admission binding; and
- any claim that the guard enumerates unknown handles.

## 6. Later real-Windows decoy probe

This section is a future platform-probe specification, not executed evidence.
For every admitted Windows build and exact platform profile, CONTROL must
create a bounded synthetic process-creation probe containing:

1. the five valid listed handles;
2. each omitted opposite pipe end;
3. one inheritable decoy of every admitted handle-object family;
4. a concurrent thread creating inheritable decoys immediately before,
   during, and after `CreateProcessW`;
5. no `STARTF_USESTDHANDLES`; and
6. a probe child given decoy numeric values only for negative testing.

Acceptance requires:

- all five listed handles are usable with exactly their frozen access;
- every omitted opposite end and decoy value is unusable in the child;
- repeated schedules never admit an omitted value;
- process creation fails or the probe fails closed on an unsupported platform;
  and
- no probe result is generalized beyond its exact pinned Windows build and
  binary/profile identities.

Any admitted decoy or opposite end invalidates the platform profile. The guard
is not used as evidence of decoy absence.

## 7. Launch-evidence and guard tests

Future source and mutation review must verify the exact
`S0-LAUNCH-HANDLE-SET-EVIDENCE-1` byte grammar before implementation
acceptance. The evidence must bind the five ordered locators and construction
metadata. The postcreation admission must bind the evidence hash, actual
verifier PID, and exact success policy ID. Returned process/thread handles stay
private to the preloader and are reviewed there, not reconstructed by the
guard.

Required negative cases include:

- changed nonce, image/package hash, application, bootstrap, verifier identity,
  flags, startup flags, attribute count/ID/size, role/kind/access, locator,
  actual verifier PID, or success policy ID;
- postcreation admission paired with another evidence record;
- raw handle values inserted into the admission frame;
- guard recomputation differing from the evidence digest;
- second guard call after success or failure;
- wrong known object kind, access, root identity, preloader identity, parent
  PID, job evidence, nonce, frame, or EOF; and
- an expectation that the guard reject an unknown decoy it was never given.

The last case must fail the test specification itself: unknown-decoy absence is
a platform/preloader responsibility, not a guard contract.

## 8. Schema completeness and semantic validation

### 8.1 Positive construction

CONTROL must construct one synthetic public placeholder profile containing
every required property and valid-shaped nonsecret identifiers. Draft 2020-12
validation must pass. This is a schema construction test only and provides no
runtime or platform evidence.

### 8.2 Exhaustive required-property deletion

For every object in the schema, delete each property named by that object's
`required` array one at a time. Every resulting instance must fail. This
includes nested identities for:

- package rows and runtime-files manifest;
- platform and loaded-PE manifests;
- kernel32 and ntdll identity and export bindings;
- guard source, build, compiler, linker, imports, binary, loaded image, Python
  initialization, direct imports, and PDB disposition;
- process creation and inherited handles;
- responsibility split and launch evidence;
- admission, locator, atomic-root, and terminal policies;
- semantic-relation list; and
- authenticated semantic-validator identity.

### 8.3 Constant, order, and weakening mutations

Mutate every fixed policy ID, Boolean, count, order, API, flag, role/kind/access
triple, import, ABI constant, state rule, package row, and semantic-relation
entry. Every mutation must fail. Add an unknown property at every object depth;
every case must fail.

### 8.4 Semantic-relation validator

JSON Schema presence checks do not prove cross-object equality. A later
separately reviewed validator must execute all ten named semantic relations.
Required negative cases include one mismatch for each relation:

- predecessor profile bytes/hash;
- runtime-files row path/hash;
- source/build/tool/import/binary/loaded-image chain;
- binary versus loaded-image object identity;
- system-image versus loaded-image/direct-import identity;
- launch evidence versus handle array;
- postcreation admission versus evidence/current PID/success policy;
- guard locators versus launch evidence;
- retained root versus duplicate object identity; and
- package rows versus exact five-row order.

No string identifier standing alone counts as executed relation evidence.

## 9. Atomic-root, state, and predecessor nonregression

The future evidence must reproduce all effective v0.1–v0.3 tests for:

- one-way channels, frame/EOF rules, and `COMMIT-ACKED` ordering;
- exact process/job counting and identity domains;
- sole `NtCreateFile`, relative root, flags, status and object postconditions;
- retained original and same-object reduced duplicate;
- anti-substitution and output usability;
- nonterminal invalid transition to `REJECTED`;
- immutable retries from `SPENT` and `REJECTED`;
- runtime/import/environment denial closure;
- candidate transport count zero or one and no provider/model/network call;
- receipt/publication semantics; and
- failure-routing and closed-claim precedence.

## 10. Acceptance threshold and closed gates

Design acceptance requires a valid fresh rereview with:

- BLOCKING: 0;
- MAJOR: 0; and
- explicit closure of `RPNP3-RR-001` and `RPNP3-RR-002` without regression.

MINOR findings require explicit CONTROL disposition. PASS permits only
consideration of a separate implementation gate. It does not authorize or
claim implementation, compilation, runtime materialization, platform probing,
official rehearsal, F0/oracle/executor/judge work, provider/model/network
access, S0/E0, central-system or Project Brain implementation, Git publication,
or main integration.
