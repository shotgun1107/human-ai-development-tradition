# S0 v0.14 public assembly build and runtime materialization design v0.1 independent review

- status: completed fresh independent PUBLIC design review
- verdict: REVISE-AND-REVIEW
- finding counts: BLOCKING 0; MAJOR 5; MINOR 0
- implementation observed: none
- compiler or build observed: none
- runtime materialization or native execution observed: none
- F0 content access: none

## 1. Role, baseline, and integrity checkpoints

I acted only as the fresh independent public-design reviewer. I did not
author, advise on, or QA the candidate package, and I did not use an author
conversation or another review conclusion.

The following CONTROL-supplied identity values matched:

- origin:
  https://github.com/shotgun1107/human-ai-development-tradition.git
- review branch:
  codex/s0-build-runtime-materialization-design-v01-review
- HEAD:
  14534507c4ad1691d18182a9cedfae4be9db4cb8
- tree:
  cfc23db91c4c6e99cae1f1b29f849eed6016af21
- sole parent:
  64077a5862aa5678a83ba2f9f48fc71493ed2808
- candidate remote-tracking ref value:
  14534507c4ad1691d18182a9cedfae4be9db4cb8
- initial worktree change count: zero
- F0 aggregate inventory: 32 / 11 / 10
- F0 worktree quiet exits: 0 / 0 / 0

The candidate package manifest SHA-256 matched
bdf3cd280c65adcb4a1a4c965a3e2512e460eb2c03f498274bddfe5879ba5e1c.
It contained exactly six unique ASCII-sorted logical target rows. Every
candidate logical artifact and same-basename sidecar matched the externally
supplied SHA-256:

| Logical artifact | SHA-256 |
|---|---|
| interface map | e0a5d539a2672cf5ac93ad1db8bc48c89a1f380e8c3430de85ef140812c43963 |
| mutation matrix | 326144bda84cfdd77c2dfaa4e6c5bd069852a8e74bc6edfc1f9e165b8a50420b |
| profile schema | 77977adfd852cae50589f68996c7e2c06fdb5b58164a469d0d87436c8761d254 |
| acceptance plan | 6838c96bbbd1eb17e5b8959f19c8bee64f00a77070c294b171fb67c1c653b3b0 |
| design | 2acbdfa35d09ba19f085f7cbff19a5c06a3605a58617e2165383f81391542c11 |
| review brief | da99792c296266e27f3eacf193d317dc83016f58c9ace6e0445444d63493522a |

The canonical validator SelfTest passed. Each admitted Markdown/sidecar pair
passed separately. Each candidate JSON and sidecar passed independently
labeled UTF-8, UTF-8 BOM absence, CR absence, final-LF, trailing-whitespace,
canonical sidecar-record, and hash checks. All three JSON files parsed with
duplicate-key rejection. The profile schema passed the Draft 2020-12
metaschema.

All externally pinned predecessor records and manifests matched. Their exact
authenticated target counts were:

| Closure | Exact targets | Sidecars explicitly admitted |
|---|---:|---:|
| bounded implementation | 3 | 0 |
| bounded verification | 4 | 0 |
| assembly design v0.5 | 5 | 5 |
| RPNP design v0.4 | 6 | 6 |
| integration design v0.1 | 5 | 5 |
| integration design v0.2 | 6 | 6 |
| assembly implementation | 32 | 0 |
| RPNP implementation | 11 | 0 |
| I0 implementation | 15 | 0 |
| I1 implementation | 26 | 0 |
| I2 implementation | 16 | 0 |
| I3 implementation | 17 | 0 |
| public-practice bundle | 90 | 0 |

Reviewer-local PowerShell execution-policy, output-capture, quoting,
manifest-anchor, and tokenization errors were corrected and rerun. They did
not change candidate bytes and are not candidate findings.

## 2. Independent reconstruction

The authenticated current bridge is bounded offline Python. Its exact success
and rejection objects keep candidate_only true, native_api_reachable false,
and rehearsal_pass false. It creates no native root, native process, handle
guard, publication witness, commit transaction, live decision, or rehearsal
authority.

The effective predecessor requires a separately authenticated native
preloader, CPython guard, source/build/import/binary/loaded-image closure,
known-five handle responsibility allocation, preloader-only atomic-root
creation, exact nested state order, and later real-Windows probes. Those
inputs and behaviors do not exist in the current candidate. The design
correctly marks the native source, toolchain, CPython distribution,
dependency closure, Windows platform, build, runtime tree, and approving
review as later inputs or evidence.

The prose also correctly requires two clean builds, complete output equality,
static inspection without loading, an unsigned certificate-table-size-zero
candidate, exact runtime rows, closed/read-back/rehash-before-publication
behavior, source-only isolated Python, quarantine, bounded resources,
diagnostic-only records, and closed live/rehearsal/F0/S0/E0 gates.

Those high-level boundaries are not enough for a PASS because the closed
machine-readable contracts and transaction order contain the five MAJOR
defects below.

## 3. Findings

### BRM-IR-001 — MAJOR — profile authority and external-pin closure is incomplete

The design requires original-byte authentication of every Section 2
predecessor. The interface map includes the bounded verification manifest and
integration v0.1 design manifest, but the schema's closed authority object
does not contain either field. Adding either field is rejected as an unknown
property. The map-only baseline commit and tree also have no stated
outer-only disposition in the schema.

The ten-class list separately requires an exact runtime-tree profile before
implementation, but the schema has no separately authenticated
runtime-tree-profile identity. The runtime_package manifest describes a
future package/output manifest and does not unambiguously bind the missing
pre-execution runtime-tree profile.

Counterexample: a schema-valid profile can bind every schema authority while
using different bounded-verification or integration-v0.1 bytes, because
there is no field or named semantic relation that can compare those omitted
pins. That leaves more than one source/provenance interpretation before any
process.

Required correction: make every retained predecessor and all ten external
pin classes exact, closed, independently authenticated fields or explicitly
outer-pinned identities, including an unambiguous pre-execution runtime-tree
profile. State one failure class and pre-process boundary for each.

### BRM-IR-002 — MAJOR — the binary profile cannot encode the promised inspection policy

The closed binary_profile requires general artifact, section, import, export,
load-config, mitigation, and a few zero-count values. It cannot encode the
guard module or PyInit_s0_runtime_handle_guard_v0_4 export, bound-import
count, CLR-header count, relocation-table identity, resource/Windows-manifest
identity, dynamic-loader or generic-FFI prohibition, or the complete
host-path/debug/PDB/CodeView disposition promised by the design and interface
map. The fourteen semantic relations contain no complete binary-policy
relation that supplies these missing predicates.

Counterexample: a schema-valid runtime_guard profile can point to an
authenticated export manifest that lacks the required PyInit symbol, and it
cannot add guard_entry_point or bound_import_count because additional
properties are rejected.

Required correction: add exact fields and semantic comparisons for every
required PE, import, export, relocation, resource, mitigation, debug,
certificate, loader, and guard predicate, all byte-bound to the inspected
image without loading it.

### BRM-IR-003 — MAJOR — the runtime package cannot encode the exact Python/import closure

The interface map fixes CPython 3.12 x64, flags -I/-S/-B, jsonschema 4.26.0,
no user site, no PYTHONPATH, no bytecode writes, no path/registry application
selection, and source-only authenticated imports. None of those fields exists
in the closed runtime_package object except the weaker
ambient_discovery_allowed false. The schema also permits one arbitrary
runtime row and does not require exact roles for the verifier application,
Python DLL, standard library, guard, dependencies, bootstrap, assembly
source, I0-I3 source, profiles, manifests, and fixed inputs.

Counterexample: an otherwise schema-valid profile with one native-executable
row, no Python flags, no source-only module map, and no jsonschema-version
binding passes. Attempts to add initial_python_flags,
source_only_authenticated_imports, or jsonschema_version are rejected as
unknown properties.

Required correction: bind the exact required runtime-role set, CPython ABI and
flags, dependency/module map, source-only resolution algorithm, no-import
dispositions, DLL/application selection, and all ambient-discovery
prohibitions in closed schema fields plus executable semantic relations.

### BRM-IR-004 — MAJOR — the mutation matrix does not have exact output-state or first-failure semantics

The 46 rows are unique and each has expected_failure, id, mutation, and
phase, but no required before/after-output bit. Several mutation texts combine
cases with different correct labels:

- BRM-BUILD-003 combines a missing output with an extra output. A command that
  creates no declared output and omits all outputs is BR-BUILD/0, while an
  extra created file is post-output BR-BUILD/1.
- BRM-BUILD-005 combines timeout, capture, memory, and process-bound failures
  without saying whether any output already exists. Either BR-BUILD/0 or
  BR-BUILD/1 can be correct.
- BRM-RETRY-001 always says BR-MATERIALIZE/1, although the preserved first
  primary class must remain an earlier BR-BUILD/1, BR-REPRO/1, or
  BR-BINARY/1 when that earlier failure caused the retry.

Required correction: split outcome-dependent rows, add an explicit
output-created boolean, and state overlap precedence so every row has exactly
one primary label without replacing an earlier failure.

### BRM-IR-005 — MAJOR — publication and record freezing are circular and the publish owner is unspecified

Section 9 requires the exact materialization record to be frozen before the
atomic rename. Section 11 requires that same record to contain the
publication transaction and final identity, facts that cannot be observed as
successful before the rename. The ordered phases end at RECORDS-FROZEN and
contain no publication-complete state.

The design also creates independent runtime staging roots from A and B and
requires one final publication, but it does not designate which identical
root is the sole rename source or how the unselected identical root is
quarantined without becoming a better-output selection or retry.

Counterexample: freeze a record that claims a final identity, then have the
same-volume rename fail because the destination appeared. The frozen record
now overclaims publication. Writing or amending the record after rename
instead violates the stated prepublication freeze rule.

Required correction: define a noncircular prepublication record, atomic
publish state, postpublication identity verification, final diagnostic record
order, one deterministic A/B staging-root owner, and exact failure/quarantine
behavior.

## 4. Ten external-pin hostile matrix

For every row below I applied the same eight conceptual counterexamples:
missing value; uppercase digest; wrong-length/malformed digest; all-zero
placeholder; predecessor digest; moving version label; candidate-selected
digest; and a lowercase 64-hex value whose bytes were not authenticated.
Every case must stop before candidate import or process creation.

| External class | Exact first failure | Action boundary |
|---|---|---|
| native source manifest | BR-SOURCE/0 | before source admission |
| materializer/static-inspector source manifest | BR-SOURCE/0 | before source admission |
| offline toolchain bundle manifest | BR-TOOLCHAIN/0 | before tool resolution |
| compiler/linker/SDK/header/library/CRT identities | BR-TOOLCHAIN/0 | before tool resolution |
| CPython 3.12 x64 distribution manifest | BR-SOURCE/0 | before runtime dependency admission |
| Python dependency manifest | BR-SOURCE/0 | before runtime dependency admission |
| Windows build/system-image manifest | BR-AUTH/0 | before platform admission |
| canonical build profile and command plan | BR-TOOLCHAIN/0 | before command interpretation |
| runtime-tree profile | BR-SOURCE/0 | before runtime mapping |
| approving independent design review | BR-AUTH/0 | before all candidate input use |

No callback, environment, PATH, registry, installer, package manager, local
newest version, prior validation object, or author-selected value may fill a
failed row.

## 5. Forty-six-row hostile reconstruction

This table supplies one concrete counterexample for every matrix row. For the
three overbroad rows identified in BRM-IR-004, the counterexample is narrowed
to the candidate's stated label; that does not repair the broader row.

| ID | Concrete counterexample | First failure | Exact action boundary |
|---|---|---|---|
| BRM-AUTH-001 | approving-review field absent | BR-AUTH/0 | before candidate input use |
| BRM-AUTH-002 | one authority digest uses uppercase A | BR-AUTH/0 | before candidate input use |
| BRM-AUTH-003 | candidate substitutes a predecessor design hash | BR-AUTH/0 | before candidate input use |
| BRM-SOURCE-001 | guard source row absent from native manifest | BR-SOURCE/0 | before source snapshot |
| BRM-SOURCE-002 | one retained Python byte is flipped | BR-SOURCE/0 | before source snapshot |
| BRM-SOURCE-003 | LF source is normalized to CRLF | BR-SOURCE/0 | before source snapshot |
| BRM-SOURCE-004 | offline RPNP Python is assigned native-preloader role | BR-SOURCE/0 | before source admission |
| BRM-TOOL-001 | compiler is found as cl.exe through PATH | BR-TOOLCHAIN/0 | before process creation |
| BRM-TOOL-002 | an imported compiler DLL is absent from the manifest | BR-TOOLCHAIN/0 | before process creation |
| BRM-TOOL-003 | dependency restore or telemetry endpoint is reachable | BR-TOOLCHAIN/0 | before process creation |
| BRM-TOOL-004 | cmd.exe command string replaces argv | BR-TOOLCHAIN/0 | before command interpretation |
| BRM-TOOL-005 | inherited USERPROFILE is added to the environment | BR-TOOLCHAIN/0 | before process creation |
| BRM-BUILD-001 | tool exits 1 before creating a declared file | BR-BUILD/0 | stop build; no admitted output |
| BRM-BUILD-002 | tool writes one object then exits 1 | BR-BUILD/1 | quarantine build root |
| BRM-BUILD-003 | tool creates undeclared junk.obj | BR-BUILD/1 | quarantine after output enumeration |
| BRM-BUILD-004 | tool creates an output outside its clean root | BR-BUILD/1 | quarantine after first created residue |
| BRM-BUILD-005 | tool creates an object then exceeds memory bound | BR-BUILD/1 | terminate and quarantine |
| BRM-REPRO-001 | only build A is run | BR-REPRO/1 | reject before comparison acceptance |
| BRM-REPRO-002 | B hard-links an object from A | BR-REPRO/1 | reject on independence check |
| BRM-REPRO-003 | one corresponding output byte differs | BR-REPRO/1 | reject complete candidate |
| BRM-REPRO-004 | B contains one extra declared path | BR-REPRO/1 | reject path-set comparison |
| BRM-REPRO-005 | B is patched and A is selected | BR-REPRO/1 | reject before runtime construction |
| BRM-PE-001 | preloader is PE32 x86 | BR-BINARY/1 | reject during static inspection |
| BRM-PE-002 | one delay-import ordinal is added | BR-BINARY/1 | reject during import inspection |
| BRM-PE-003 | guard lacks its PyInit export | BR-BINARY/1 | reject during export inspection |
| BRM-PE-004 | image imports LoadLibraryW | BR-BINARY/1 | reject during import inspection |
| BRM-PE-005 | image contains a TLS callback | BR-BINARY/1 | reject during static inspection |
| BRM-PE-006 | NX compatibility is cleared | BR-BINARY/1 | reject during mitigation inspection |
| BRM-PE-007 | image embeds C:/Users/example/build | BR-BINARY/1 | reject during byte-bound inspection |
| BRM-PATH-001 | runtime path is a/../b | BR-MATERIALIZE/1 | reject before creating mapped object |
| BRM-PATH-002 | paths CON.txt and con.txt collide | BR-MATERIALIZE/1 | reject before creating mapped object |
| BRM-PATH-003 | staging entry is a junction or hard link | BR-MATERIALIZE/1 | quarantine staging root |
| BRM-TREE-001 | runtime manifest repeats one virtual path | BR-MATERIALIZE/1 | reject exact-set validation |
| BRM-TREE-002 | an extra .pyc appears | BR-MATERIALIZE/1 | quarantine on enumeration |
| BRM-TREE-003 | reopened file is short or has changed identity | BR-MATERIALIZE/1 | quarantine before publication |
| BRM-PUBLISH-001 | destination exists before rename | BR-MATERIALIZE/1 | no publication; quarantine |
| BRM-PUBLISH-002 | a runtime file changes after rename | BR-MATERIALIZE/1 | reject final identity |
| BRM-RUNTIME-001 | manifests match but one B runtime byte differs | BR-REPRO/1 | reject runtime comparison |
| BRM-RUNTIME-002 | missing Python row is filled by host PATH | BR-MATERIALIZE/1 | reject runtime validation |
| BRM-RUNTIME-003 | jsonschema transitive file is missing | BR-MATERIALIZE/1 | reject runtime validation |
| BRM-RUNTIME-004 | packaged guard differs from inspected bytes | BR-BINARY/1 | reject before launch authority |
| BRM-RUNTIME-005 | loader accepts .pyc or an outside module | BR-MATERIALIZE/1 | reject runtime validation |
| BRM-RECORD-001 | record is truncated before final LF | BR-RECORD/1 | quarantine at record freeze |
| BRM-RECORD-002 | record claims rehearsal PASS | BR-RECORD/1 | reject record; grant no authority |
| BRM-RECORD-003 | record close/read-back fails | BR-RECORD/1 | quarantine; preserve prior success facts only as diagnostics |
| BRM-RETRY-001 | a materialization retry reuses failed staging root | BR-MATERIALIZE/1 | reject retry before any reuse |

## 6. Key-question and resource results

1. Ambient compiler, SDK, Python, dependency, source, or platform state is
   forbidden by prose, but findings BRM-IR-001 and BRM-IR-003 show that the
   closed profile cannot yet bind the complete prohibition.
2. A and B are forbidden to share roots, bytes, cache, generated objects,
   processes, or paths; the intended relation is noncircular.
3. Patch, normalization, or better-output selection is forbidden.
4. Static inspection is required from exact bytes without loading, but
   BRM-IR-002 shows that the required predicate set is not representable.
5. Windows aliases, case folds, reparse objects, links, ADS, and nonregular
   types are intended to fail before publication.
6. Every file must be closed, reopened, identity-checked, and rehashed before
   publication; BRM-IR-005 concerns the later record/publication ordering.
7. Host Python, site packages, DLL search, registry, PATH, and package
   installation may not fill a missing row; BRM-IR-003 requires the machine
   contract to encode that rule.
8. Profiles, build PASS, manifests, and records remain diagnostic and cannot
   grant live or rehearsal authority.
9. The twelve numeric resource limits are byte-for-byte equal between the
   interface map and schema. A valid-shaped fake in-memory placeholder passed
   the schema, and all 24 one-below/one-above limit mutations were rejected.
10. The design correctly states that the required native sources, tools,
    binaries, runtime distribution, platform behavior, and materialization do
    not yet exist.

## 7. Evidence limits, verdict, and remaining gate

This review is design evidence only. I created or observed no compiler,
build, runtime tree, native API call, loaded image, platform behavior, live
decision, official rehearsal, F0 input, provider/model execution, S0 result,
or E0 result.

Verdict: REVISE-AND-REVIEW.

Finding counts:

| Severity | Count |
|---|---:|
| BLOCKING | 0 |
| MAJOR | 5 |
| MINOR | 0 |

No successor gate is opened. The PASS-only gate
S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME
MATERIALIZATION DESIGN CONTROL INTEGRATION OPEN remains closed. The required
next action is a bounded design revision followed by a fresh independent
review of the revised exact package.

No commit or push is authorized or performed.
