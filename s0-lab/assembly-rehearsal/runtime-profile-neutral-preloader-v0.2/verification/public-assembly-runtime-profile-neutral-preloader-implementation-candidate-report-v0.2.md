# Public assembly runtime profile and neutral preloader implementation candidate report v0.2

## 1. Scope and provenance

This package is a bounded public revision of the v0.1 offline implementation
candidate. It responds to the independent v0.1 implementation rereview. It is
not a runtime-profile materialization, native neutral preloader, implementation
acceptance, platform result, or public assembly rehearsal.

- repository: `human-ai-development-tradition`;
- baseline commit: `f6f4e2cc1413bb3d9d9dda2b7c4cdb791a04b7f7`;
- baseline tree: `7a2d4e697abee3383477174310f167db1d554d09`;
- implementation branch:
  `codex/s0-rpnp-v02-implementation-revision-v01`;
- v0.4 design-package manifest SHA-256:
  `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`;
- approving v0.4 independent-rereview preservation-record SHA-256:
  `9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71`;
- v0.1 candidate commit:
  `f6f4e2cc1413bb3d9d9dda2b7c4cdb791a04b7f7`.

The implementation manifest covers ten package sources and one test source.
No runtime profile, executable, persisted synthetic fixture, hidden oracle, or
F0 content was created or read.

## 2. Independent-rereview findings and revision response

| v0.1 finding | v0.2 response | Current boundary |
|---|---|---|
| Reusable Python authority was forgeable and mutable | Removed the token, registry, authenticated-profile class, and authority predicate. Every operation revalidates original schema, profile, manifest, and target bytes. Returned objects are openly constructible `candidate_only` data and no consumer accepts them as authority. | Closed for this bounded candidate; no Python object is a live authority. |
| Caller-fabricated semantic evidence could issue acceptance | Only three relations derivable from exact bytes are returned as `BYTE_VERIFIED_RELATIONS`. PE provenance, loaded-image identity, exports, direct imports, and platform observations are explicitly `DEFERRED_STATIC_RELATIONS`. Dynamic observations remain explicitly offline. | False acceptance closed; the deferred native/platform evidence itself remains unimplemented and unvalidated. |
| Launch inputs, identity, locators, and admission claims were unbound | The launch-control path is fixed to `runtime/launch-inputs.json`; its exact bytes must be a target of the authenticated runtime-files manifest, and its SHA-256 enters launch diagnostic bytes. Locators are fixed-order and digest-bound. Admission construction revalidates raw inputs and derives hashes internally. | Closed for deterministic offline diagnostics; no live process observation is claimed. |
| Integration compared caller-supplied hash strings | The bridge hashes all four authority artifacts itself, parses both manifests, and verifies the exact 32-row assembly and 6-row design target-byte closures. | Closed for the pinned public byte sets. |
| AST blacklist could be bypassed while claiming proof | Replaced the path-reading audit with an already-supplied, exact ten-file byte-mapping structural diagnostic. It blocks the reviewed import, ambient-loader, frame, rebinding, shadowing, pattern-capture, and filesystem-method mutations. The module explicitly states that it is not a capability proof, sandbox, or acceptance authority. | The false proof claim is removed. Manifest authentication and independent source review remain mandatory. |

## 3. Implemented bounded behavior

The v0.2 package provides:

1. strict canonical JSON and exact manifest-target authentication;
2. a dependency-free executor for the complete keyword vocabulary used by the
   pinned runtime-profile v0.1 through v0.4 schemas, including object-valued
   `additionalProperties`;
3. raw-byte verification of all predecessor profiles, runtime-files manifest,
   exact five-row effective package, and semantic-validator artifact;
4. explicit separation of byte-verified, deferred static, offline
   precreation, and offline postcreation relation sets;
5. a fixed, manifest-authenticated launch-control artifact whose digest binds
   application, command line, environment, current directory, and four launch
   artifact identities into the offline launch diagnostic;
6. exact five-position locator, role, kind, access, guard, and retained-root
   consistency checks;
7. offline launch and admission diagnostic bytes with non-production schema
   IDs plus in-band `candidate_only=true` and `rehearsal_pass=false` markers;
8. exact raw-byte integration with the existing public assembly candidate and
   approved v0.4 design/rereview authorities; and
9. a non-authoritative source-structure diagnostic over already supplied
   bytes, with no implementation-side filesystem traversal.

There is no native invocation method. Every prepared result has
`native_api_reachable=False`.

## 4. Verification results

The final bounded offline suites passed:

- v0.2 revision suite: `16 / 16`;
- v0.1 runtime/preloader regression suite: `13 / 13`;
- existing public assembly candidate regression suite: `47 / 47`;
- total: `76 / 76 PASS`.

The v0.2 suite also reproduced:

- all four pinned schema-family samples accepted;
- required-property deletion mutations: `185 / 185` rejected;
- closed-object unknown-property mutations: `28 / 28` rejected;
- fixed-constant mutations: `106 / 106` rejected;
- all eleven Python files strict UTF-8, LF-only, final-LF, BOM-free, and
  successfully AST-parsed;
- exact 32-row and 6-row integration target closures; and
- reviewed source-structure mutations for dynamic import, module laundering,
  relative-import laundering, ambient loader access, traceback/frame access,
  import rebinding and shadowing, pattern capture, and filesystem methods.

The environment did not contain the external `jsonschema` package. It was not
installed, and no external-package cross-check is claimed. The bounded fixed
executor and pinned-schema tests are the reported evidence.

Fresh `gpt-daybreak-blue-latest` adversarial subreviews were used during the
revision. They found four pre-fix MAJOR issues, then one ambient/frame MAJOR
and one generic-schema MINOR, then two further source-diagnostic bypasses.
Each confirmed issue was converted into a regression or an explicit claim
reduction. The final focused delta review reported BLOCKING `0`, MAJOR `0`,
and MINOR `0` for the packaged structural claims. These were implementation
reviews, not the formal independent gate.

## 5. Deliberately unexecuted and unproved work

This candidate does not prove or claim:

- authenticated runtime-profile or executable materialization;
- PE parsing, source-to-binary provenance, file identity, loaded-image
  identity, export address, or direct-import observation;
- native guard, compiler, linker, import table, CRT, or system-image closure;
- actual application, token, security-attribute, mitigation, job, or process
  creation behavior;
- live handle inheritance, current PID, kernel semantics, or platform probe;
- production admission-frame acceptance;
- native API invocation, child creation, provider/model access, F0 access,
  hidden-oracle access, or public assembly rehearsal; or
- implementation acceptance, CONTROL integration, commit, push, merge, or
  main integration.

The three deferred static relations require separately authenticated native
or platform-derived evidence. Relabeling them as deferred is a fail-closed
correction, not completion of that future work.

## 6. Candidate disposition

The v0.2 bytes are suitable for an independent implementation rereview. They
must not be treated as live authority or as approval to materialize a runtime
package, invoke native APIs, run a platform probe, or open an assembly
rehearsal. Any next gate requires a separate explicit decision.
