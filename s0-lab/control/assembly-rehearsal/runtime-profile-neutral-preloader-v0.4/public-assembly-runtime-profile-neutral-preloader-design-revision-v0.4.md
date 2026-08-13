# Public Assembly Runtime Profile + Neutral Preloader Design Revision v0.4

Status: CONTROL design candidate for fresh independent rereview

## 1. Scope, authority, and replacement rule

This revision answers only the two MAJOR findings preserved in:

- `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/v0.3-independent-rereview-result-preservation-record-v0.1.md`;
- SHA-256:
  `9085e20666fdaa1246e47430993149f103c31c4e0e64652ad57d77bbed42675e`.

The findings are:

1. `RPNP3-RR-001`: the v0.3 guard could validate five known handles but could
   not observe verifier-wide absence of an unknown sixth handle or opposite
   pipe end; and
2. `RPNP3-RR-002`: the v0.3 runtime-profile schema did not require every
   source/build/import/platform, per-handle, atomic-root, retention, and
   package predicate promised by the design.

This document replaces only:

- v0.3 §§4.1–4.4 where responsibility for exact child inheritance and
  opposite-end absence was assigned to the guard;
- v0.3 §6 runtime-profile supplement and four-row package composition;
- the corresponding v0.3 interface-map, schema, and acceptance clauses; and
- references to v0.3 guard/module/frame identifiers superseded below.

Every unrelated v0.1, v0.2, and v0.3 clause remains authoritative. The
effective assembly design remains assembly v0.3 plus v0.4 replacements plus
v0.5 replacements, composed with runtime/preloader v0.1, v0.2, v0.3, and this
v0.4 overlay in that order. A consumer must reject selective predecessor use.

Base and predecessor identities:

- base commit:
  `f336995da41d201a9132246d7fffd0506f9a5a01`;
- base tree:
  `c3c351b2dcf2fc19364a7b5248c13343ae6345dd`;
- v0.3 design SHA-256:
  `971d15f4fe666d656973898a0aa38b92370cd4b8a89e92aaff00ecf7241e9456`;
- v0.3 interface-map SHA-256:
  `30d39aa73734173c0d7908bf97fb8a75d42eafca8997f464b3001ff22abbaf39`;
- v0.3 schema SHA-256:
  `1404f4981d3d7815e98a6c5d745596f15bb8d50a296410584d03d7ccb11ce3dd`;
- v0.3 acceptance-plan SHA-256:
  `a20d0dab51fb038ecda998dcbd8dbbd9483797b723a843e39368281e65716a13`;
- v0.3 package-manifest SHA-256:
  `c2ecd2931e15a99b68d3e669026342f59a42995268f8b4937ba96e63d731481b`.

This remains a public design artifact. It does not authorize or establish an
implementation, build, runtime capture, native binary, platform probe,
official rehearsal, F0 access, oracle, provider/model call, or S0 execution.

## 2. Public Windows API basis and trust allocation

The externally authenticated CONTROL launcher, authenticated preloader, and
the exact admitted Windows kernel build are the relevant trust components for
process creation. The verifier guard is not a process-wide handle enumerator.

The design relies on these public Microsoft API semantics, which must be
pinned into the future platform evidence set rather than fetched at runtime:

- `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` supplies the handles inherited by the
  child and requires `bInheritHandles=TRUE`:
  `https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute`;
- inherited handles refer to the same objects with the same values and access,
  and standard handles require the corresponding startup configuration:
  `https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance`;
- `CreateProcessW` requires `STARTUPINFOEXW` plus
  `EXTENDED_STARTUPINFO_PRESENT` for the attribute list:
  `https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw`; and
- `STARTF_USESTDHANDLES` controls whether the supplied `hStdInput`,
  `hStdOutput`, and `hStdError` fields are used:
  `https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfow`.

The source and binary review must prove the exact process-creation call. A
later real-Windows platform probe must demonstrate that the admitted build
actually enforces the frozen handle-list behavior under concurrent inheritable
decoy creation. If the platform contradicts the frozen assumption, the run
fails closed and the design returns to revision.

## 3. Exact inheritance responsibility

### 3.1 Authenticated preloader responsibility

Immediately before verifier creation, the authenticated preloader owns the
only authoritative construction of the child inheritance request. It must:

1. create the three child pipe endpoints, reduced-access root duplicate, and
   reduced-access preloader-process handle as inheritable;
2. keep every opposite pipe end, retained parent/root handle, job, process,
   thread, authentication, console, registry, token, network, and unrelated
   handle outside the list;
3. create opposite pipe ends and every locally retained duplicate as
   noninheritable;
4. construct one `STARTUPINFOEXW` whose attribute list has exactly one entry,
   `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`;
5. set that entry's value to an ordered five-element `HANDLE` array and
   `cbSize` to exactly `5 * sizeof(HANDLE)`, equal to 40 on the admitted x64
   ABI;
6. leave `STARTF_USESTDHANDLES` clear and use no supplied standard handles;
7. call the exact authenticated `CreateProcessW` import with
   `bInheritHandles=TRUE` and creation flags exactly
   `CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT |
   EXTENDED_STARTUPINFO_PRESENT | CREATE_NO_WINDOW`;
8. use the exact authenticated application path, writable canonical command
   line, environment block, current directory, security attributes, and
   mitigation/process/job policy inherited from the effective predecessor;
9. retain the attribute-list storage and ordered handle array unchanged until
   `CreateProcessW` returns; and
10. on success, retain the returned process/thread handles privately, bind the
    actual verifier PID and successful creation policy ID into the admission
    frame, and close local child-end duplicates only after that binding.

The ordered child array is exactly:

1. admission-read pipe endpoint, read but not write-data;
2. commit-request-write pipe endpoint, write but not read-data;
3. commit-reply-read pipe endpoint, read but not write-data;
4. output-root directory duplicate, list/read-attributes/synchronize only; and
5. preloader-process handle, query-limited-information/synchronize only.

No other handle can be added by a caller, environment value, command-line
value, admission frame, Python object, plugin, callback, or verifier request.
The exact preloader source, build, import graph, and loaded binary are part of
the authenticated runtime closure.

### 3.2 Kernel-semantics responsibility

The exact admitted Windows kernel is responsible for applying the authenticated
`PROC_THREAD_ATTRIBUTE_HANDLE_LIST` at process creation. The security claim is
limited to the public API contract on the pinned platform plus the later
platform evidence. It is not described as a theorem proved by the verifier.

The later platform probe must include:

- one inheritable decoy handle omitted from the list;
- all three opposite pipe ends omitted from the list;
- no `STARTF_USESTDHANDLES` and no console window;
- a concurrent thread creating additional inheritable decoys around the
  `CreateProcessW` call; and
- a probe child that is told each decoy numeric value only for the negative
  test and proves each value unusable while all five admitted handles remain
  usable with their exact access.

Any decoy or opposite end usable in the child rejects the platform profile.

### 3.3 Guard responsibility and explicit nonclaims

The v0.4 extension is named `s0_runtime_handle_guard_v0_4`; its only admitted
entry point is `bind_once_v4`, returning one private
`HandleBindingsV4` object. The first call consumes the process-global latch
before validation; success and failure both make later calls fail.

The guard receives the five canonical locator values and validates only facts
observable from those five live handles, the authenticated admission frame,
the current verifier process, and the inherited preloader-process handle. It
must validate:

- locator grammar, nonzero/sentinel exclusion, distinctness, liveness, and the
  expected inherited-handle flag;
- the three known pipe object types, direction-specific access, byte-stream
  mode, initial endpoint state, one-frame protocol, nonce, and EOF;
- reduced root access, object type, no reparse/write/delete authority, stable
  volume/file identity, and equality to the admitted retained-root identity;
- preloader-process access, live PID/image, current verifier PID/image,
  parent-PID relation, and preserved job evidence; and
- the v0.4 launch-evidence digest described below.

The guard does not claim to enumerate the verifier handle table, prove that no
unknown sixth handle exists, prove that an omitted opposite end is absent, or
independently prove the bytes originally supplied to
`PROC_THREAD_ATTRIBUTE_HANDLE_LIST`. Those are authenticated preloader,
kernel-semantics, source/binary-review, and platform-probe predicates.

### 3.4 Canonical launch-handle-set evidence

Before `CreateProcessW`, the authenticated preloader constructs exact ASCII,
final-LF bytes with schema ID `S0-LAUNCH-HANDLE-SET-EVIDENCE-1`. The ordered
fields bind:

- fresh run nonce;
- admitted preloader image and runtime-profile-package hashes;
- exact application, bootstrap, and verifier image identities;
- exact creation flags and `STARTUPINFOEXW.dwFlags`;
- `bInheritHandles=true`;
- attribute-list entry count, attribute identifier, array byte length, and
  handle count;
- for each of the five positions: semantic role, object kind, access-policy
  ID, and exact fixed-width lowercase numeric locator; and
- the intended verifier PID field as zero before creation.

After successful `CreateProcessW`, the preloader sends only the evidence
SHA-256, actual verifier PID, and creation-result policy ID
`createprocess-success-bound-v0.4` in admission frame v4. Raw process/thread
handles and raw locator values do not enter the frame. The guard recomputes the
evidence digest from its five locators, fixed profile metadata, and admitted
nonce, then checks that its current PID equals the admitted actual verifier
PID. Source/binary review, not the guard, proves the private returned
process/thread handle use. This proves agreement with the authenticated
preloader statement without upgrading it into guard-side process-wide
observation.

## 4. Admission-frame and locator v0.4 delta

The v0.4 admission schema ID is
`S0-PUBLIC-ASSEMBLY-RUNTIME-ADMISSION-FRAME-4`. The v0.3 canonical ASCII JSON,
one-line final-LF, maximum-8,192-byte framing remains authoritative, with these
additional required bindings:

- `launch_handle_set_evidence_sha256`;
- actual verifier PID and creation-result policy ID
  `createprocess-success-bound-v0.4`;
- preloader responsibility ID
  `authenticated-preloader-exact-handle-list-v0.4`;
- kernel-semantics policy ID
  `pinned-windows-handle-list-semantics-v0.4`;
- guard-observation policy ID
  `known-five-handles-only-v0.4`;
- v0.1, v0.2, v0.3, and v0.4 profile hashes; and
- exact effective five-row runtime-package hash.

Numeric handle values and raw locator strings remain forbidden in the frame.
The five command-line locator names and fixed-width representation remain
unchanged; their policy ID advances to
`ordered-command-line-handle-locators-v0.4` only to bind the new guard and
evidence transaction.

## 5. Complete runtime-profile v0.4 closure

The v0.4 supplemental profile conforms to the supplied closed Draft 2020-12
schema. Every top-level object uses `additionalProperties: false`. The schema
requires, rather than merely describes, the following groups.

### 5.1 Predecessor and package closure

- exact v0.1, v0.2, and v0.3 profile SHA-256 values;
- unchanged v0.2 process/job policy ID;
- exact five-row ASCII-sorted package composition:
  `runtime-files.sha256`, `runtime-profile-v0.1.json`,
  `runtime-profile-v0.2.json`, `runtime-profile-v0.3.json`, and
  `runtime-profile-v0.4.json`;
- runtime-files manifest virtual path and SHA-256; and
- required exact semantic-relation IDs that bind profile objects, runtime-file
  rows, source/build inputs, binaries, loaded images, and package rows.

### 5.2 Platform and source-to-binary closure

- exact kernel32 and ntdll virtual paths, SHA-256 values, file IDs, volume
  serials, PE machine, timestamp, image size, and required export RVAs;
- exact platform manifest and loaded-PE manifest paths and hashes;
- exact required loaded-PE families `python312.dll`, `kernel32.dll`,
  `ntdll.dll`, `ucrt-runtime`, and `vcruntime`;
- guard source and build-recipe paths and hashes;
- compiler and linker paths, hashes, file IDs, and version identities;
- import-manifest and CRT-import-manifest paths and hashes;
- guard binary path, hash, file ID, PE identity, loaded-image path/hash/file
  ID, and equality-policy ID;
- exact Python initialization symbol, semantic call list, direct-import policy,
  dynamic-loader/FFI prohibitions, and PDB disposition.

### 5.3 Handle and guard closure

- exact process-creation API, flags, attribute-list shape, handle-array size,
  five ordered role/kind/access triples, opposite-end and standard-handle
  policies, evidence schemas, and responsibility IDs;
- exact authenticated application-name, writable-command-line, environment,
  current-directory, process/thread security-attributes, token, mitigation,
  job, attribute-storage-lifetime, and numeric flag/attribute policies;
- exact locator grammar, order, scrub rule, and non-authority status;
- exact v0.4 guard module, entry point, return type, first/failure latch rules,
  known-handle observation list, and process-wide nonclaim; and
- admission-frame v4 schema, size, digest algorithms, required bindings, and
  raw-handle-value prohibition.

### 5.4 Atomic-root and terminal closure

- all eleven `NtCreateFile` ABI argument policy values and direct-import
  identity;
- exact null allocation/EA/security fields, root/name relation,
  success/status/information and thirteen returned-object postconditions;
- original-handle continuous retention, duplicate access, same-object
  equality, no pathname reopen, no second create, and quarantined-failure
  residue policies; and
- exact nonterminal rejection and immutable terminal retry policy.

Where Draft 2020-12 cannot compare two instance values directly, the schema
requires the exact closed `semantic_relations` list. A future separately
reviewed validator must execute every named equality and provenance relation;
presence of the string alone is not acceptance evidence.

## 6. Atomic root, state, and routing nonregression

The v0.3 sole parent-relative `NtCreateFile` construction, exact eleven-argument
ABI, `FILE_CREATE`, `OBJ_CASE_INSENSITIVE | OBJ_DONT_REPARSE`, returned-handle
validation, retained-original and reduced-duplicate equality, no reopen, and
quarantined-root routing remain unchanged. v0.4 only requires their complete
profile representation and semantic validation.

The v0.3 verifier states and terminal rules remain unchanged:

- invalid transition from a nonterminal state atomically enters `REJECTED`;
- attempts against `SPENT` or `REJECTED` fail without state mutation; and
- no retry creates a second authority, commit, consumer result, or upgrade.

## 7. Required later evidence

Before implementation consideration, a fresh independent design rereview must
authenticate this exact package, reconstruct the effective predecessor, and
return zero BLOCKING and zero MAJOR findings.

If the design passes, later gates must still separately cover:

1. source/build/runtime-file authentication before compilation;
2. source review proving the exact attribute-list buffer and process-creation
   call;
3. binary/import and loaded-image review;
4. schema and semantic-validator mutation testing;
5. a bounded real-Windows decoy/opposite-end inheritance probe;
6. the existing atomic-root usability and anti-substitution probe; and
7. only afterward, reconsideration of an official public assembly rehearsal.

No current statement treats a design artifact, schema acceptance, Microsoft
documentation, or future-test specification as executed platform evidence.

## 8. Closed claims

This revision establishes only a public v0.4 design candidate. It does not
claim that the preloader, native guard, runtime package, schema validator,
handle protocol, atomic root, assembly candidate, F0, oracle, executor,
provider/model, S0/E0, central system, Project Brain integration, operational
safety, economic value, or model-to-model transfer has been implemented,
executed, or validated.
