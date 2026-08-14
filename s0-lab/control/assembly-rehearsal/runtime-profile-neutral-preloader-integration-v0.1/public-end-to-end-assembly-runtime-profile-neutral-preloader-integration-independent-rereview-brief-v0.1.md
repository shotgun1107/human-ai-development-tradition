# Public end-to-end assembly runtime profile and neutral preloader bounded integration design v0.1 independent rereview brief

## 1. Role and decision

Use one fresh independent public integration-design reviewer. The reviewer is
read-only and must judge authenticated Git bytes rather than prior
conversation, CONTROL summaries, candidate self-reports, or implementation
intent.

The required verdict is exactly one of:

- `PASS-FOR-BOUNDED-ASSEMBLY-RUNTIME-PRELOADER-INTEGRATION-IMPLEMENTATION-CONSIDERATION-ONLY`;
- `RETURN-TO-INTEGRATION-DESIGN-REVISION`; or
- `INVALID-REVIEW` after an authentication or input-boundary failure.

PASS requires zero BLOCKING and zero MAJOR findings. MINOR findings require an
explicit CONTROL disposition and do not silently change any authority.

## 2. Allowed inputs

The allowed inputs are a maximum, not a repository-search suggestion.

### 2.1 Policy and validator

- root `AGENTS.md`;
- `s0-lab/control/tools/verify-text-artifacts.ps1`.

### 2.2 Exact v0.1 integration-design package

Only the five logical artifacts, their five same-basename SHA-256 sidecars,
and `design-package-files.sha256` under:

`s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.1/`

### 2.3 Exact assembly authorities and relevant sources

- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/implementation-files.sha256`;
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/public-end-to-end-assembly-rehearsal-implementation-candidate-report-v0.1.md`;
- its same-basename sidecar;
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_child_bootstrap.py`;
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_verifier/harness.py`; and
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/tests/test_harness.py`.

The implementation manifest may be parsed to authenticate its exact 32-row
closed public path set, but no other target may be opened unless CONTROL first
adds its exact logical path to the role allowlist. Any F0 row, unsafe path, or
hash mismatch invalidates the review before target reading.

### 2.4 Exact runtime/preloader implementation authorities and relevant sources

- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/verification/implementation-files.sha256`;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/verification/public-assembly-runtime-profile-neutral-preloader-implementation-candidate-report-v0.3.md`;
- its same-basename sidecar;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/implementation/s0_public_runtime_preloader/__init__.py`;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/implementation/s0_public_runtime_preloader/integration.py`;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/implementation/s0_public_runtime_preloader/preloader.py`;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/implementation/s0_public_runtime_preloader/profile.py`;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/implementation/s0_public_runtime_preloader/source_audit.py`;
- `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-implementation-v0.3/rpnp-implementation-v0.3-independent-rereview-result-v0.1.md`; and
- its same-basename sidecar.

The runtime/preloader manifest may be parsed and all 11 target hashes may be
authenticated, but target contents outside the five named source files remain
unread unless CONTROL explicitly expands the allowlist.

### 2.5 Exact v0.4 design authority

- `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/design-package-files.sha256`;
- `public-assembly-runtime-profile-neutral-preloader-design-revision-v0.4.md`;
- `public-assembly-runtime-profile-neutral-preloader-interface-map-v0.4.json`;
- `runtime-profile-v0.4.schema.json`;
- `public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.4.md`;
- each named artifact's same-basename sidecar;
- `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.4-independent-rereview-result-preservation-record-v0.1.md`; and
- its same-basename sidecar.

## 3. Forbidden inputs and actions

The reviewer must not:

- open, search, quote, summarize, or enumerate individual filenames or
  contents under any F0 path family;
- search the repository broadly;
- open implementation-manifest targets outside the exact allowed source list;
- use past conversation as evidence;
- edit or create any repository file;
- implement code, build, compile, install dependencies, materialize a runtime,
  load a candidate binary, call a native API, start a child, reserve an output
  root, run a platform probe, or run a rehearsal;
- access an oracle, provider, network, real customer data, personal data, or
  secret material; or
- commit, push, open a PR, merge, integrate to main, or open a later gate.

F0 checks are aggregate-only. The expected tracked inventory is
`32 / 11 / 10`, and every local anomaly count must be zero.

## 4. Authentication preflight

Before semantic reading, the reviewer must:

1. authenticate the exact CONTROL-supplied branch, commit, tree, sole parent,
   upstream, and live remote tip;
2. require clean worktree and index state;
3. reproduce every external SHA-256 pin named in the design and interface map;
4. run the canonical validator SelfTest and validate all admitted Markdown
   and sidecar pairs;
5. parse both integration JSON artifacts with duplicate-key rejection;
6. meta-validate the integration schema as Draft 2020-12;
7. validate the interface map against that exact schema;
8. require a canonical five-row package manifest with exact target hashes;
9. authenticate the assembly 32-row and runtime/preloader 11-row manifests
   before reading any admitted target; and
10. complete aggregate-only F0 inventory and quiet-state checks.

Any failure is `INVALID-REVIEW`. The reviewer must not repair an input or
continue with semantic judgment after a boundary failure.

## 5. Required adversarial questions

The reviewer must answer each question explicitly:

1. Does the design accurately reconstruct the current zero-call integration
   gap and unconditional live fail-close?
2. Does `prepare_assembly_runtime_launch` actually authenticate original
   assembly/design bytes and reach the snapshotted high-level preloader path?
3. Can the standalone validator, reusable candidate objects, or source audit
   reach any authority under the proposed boundary?
4. Is the future admission wrapper specified strongly enough to prevent
   cached-object or split-operation authorization?
5. Does every runtime, executable, dependency, build, binary, import,
   platform, and loaded-image fact have exactly one evidence owner?
6. Can any public parameter, callback, path, environment value, ambient loader,
   package version, or fallback select executable code outside the manifest?
7. Is the parent/preloader/verifier responsibility split consistent with the
   effective v0.4 design, especially the exact five-handle list and
   process-wide absence nonclaim?
8. Can any action occur before its corresponding authentication state?
9. Are the fail-close release conditions complete, falsifiable, and tied to
   separately gated evidence?
10. Does the design avoid converting an offline Python plan into native,
    platform, live, production, or rehearsal authority?

## 6. Finding requirements

Every finding must include:

- stable ID;
- severity: BLOCKING, MAJOR, or MINOR;
- exact file and line evidence;
- violated authority or requirement;
- deterministic false-PASS, ambiguity, or incompleteness argument;
- impact on later implementation or live release; and
- smallest correction direction.

Any route that permits unauthenticated executable selection, pre-auth import
or output mutation, standalone-validator authority, candidate-to-live upgrade,
responsibility circularity, or release of the current live fail-close without
the required later evidence is at least MAJOR.

## 7. Verdict boundary

A PASS means only that this exact public integration design is coherent enough
for separate bounded implementation consideration. It does not approve code,
builds, binaries, runtime material, native calls, platform behavior, live
assembly, official rehearsal, F0 or oracle access, S0, production use, Git
publication, or main integration.
