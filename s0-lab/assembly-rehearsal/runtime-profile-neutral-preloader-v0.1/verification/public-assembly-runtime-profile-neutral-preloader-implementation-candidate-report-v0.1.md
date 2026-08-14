# Public Assembly Runtime Profile + Neutral Preloader Implementation Candidate Report v0.1

Status: `BOUNDED-PUBLIC-CANDIDATE-COMPLETE; NATIVE-AND-PLATFORM-GATES-CLOSED`

## 1. Gate and authenticated baseline

CONTROL opened only:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER BOUNDED PUBLIC IMPLEMENTATION CANDIDATE OPEN`

The candidate was produced from this authenticated Git baseline:

- baseline commit: `7de5e765f2500fd66a6895ca764a357a211c1381`;
- baseline tree: `4133d619105b8fcce7e7f2b674ceb9547cb9308c`;
- implementation branch:
  `codex/s0-rpnp-v04-bounded-public-implementation-v01`;
- runtime/preloader v0.4 design-package manifest SHA-256:
  `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`;
- approving v0.4 independent-rereview preservation-record SHA-256:
  `9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71`;
- existing public assembly implementation-manifest SHA-256:
  `0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623`;
- existing public assembly candidate-report SHA-256:
  `520a237109686a17b8c075c15f1cc676a43d450716a6157bce7b48585f0c5005`;
- runtime-profile v0.4 schema SHA-256:
  `3cdcf7e39d39536213f5ab577970f39643b13aa542d854176c213590a16f92dd`.

The three PUBLIC-GIT / AI-CONTENT-DEFAULT-DENY F0 families remained content-
unread. Their authenticated aggregate inventory was `32 / 11 / 10`, and all
quiet/special-index/untracked/ignored aggregate differences were zero.

## 2. Exact implemented scope

The candidate contains eleven implementation/test files pinned by
`implementation-files.sha256`, whose SHA-256 is
`31aaed186fdacd982ea0a3a2dd627cf68412788fd8b4cbbda973c8e185438575`.
It implements:

1. strict public JSON and manifest primitives with UTF-8, BOM, LF,
   duplicate-key, canonical-form, non-finite-number, path, sorting, and SHA-256
   rejection;
2. a dependency-free executor for the complete, fixed Draft 2020-12 keyword
   surface used by the authenticated v0.4 schema;
3. immutable process-local runtime-profile authority issued only after exact
   schema pinning, structural validation, current-profile byte binding, and
   all semantic checks;
4. an executable validator for the exact ten v0.4 cross-object semantic
   relations and the authenticated semantic-validator identity;
5. exact ASCII final-LF `S0-LAUNCH-HANDLE-SET-EVIDENCE-1` construction;
6. canonical, locator-free, maximum-8,192-byte admission-frame v4
   construction;
7. a neutral preloader plan that constructs role/kind/access order internally
   from five separately named locator inputs, freezes the exact one-attribute,
   five-handle, 40-byte x64 launch tuple, and exposes no caller-selected handle
   array route;
8. an exact pin-only bridge to the existing assembly candidate and the v0.4
   design/rereview authorities; and
9. a static source audit proving that this bounded Python package imports or
   names no native/process/network authority.

`PreparedLaunch.invoke_native_process_creation()` always raises
`PlatformGateClosed`. The old assembly candidate's live entry remains
unchanged and fail-closed. No candidate path can return a live assembly
decision.

## 3. Verification results

The new offline suite passed `13 / 13` tests. Its exhaustive structural and
semantic mutation inventory was:

- instantiated schema objects: `28`;
- required-property deletion mutations: `185 / 185` rejected;
- unknown-property mutations at closed object depths: `28 / 28` rejected;
- fixed-constant mutations: `106 / 106` rejected;
- semantic-relation mismatch mutations: `10 / 10` rejected;
- duplicate, noncanonical, `NaN`, positive infinity, and negative infinity
  JSON cases rejected;
- locator reorder/duplicate cases rejected;
- foreign, copied, deep-copied, serialized, mutable, and `object.__new__`
  authority paths rejected; and
- the four assembly/design/rereview pin targets and schema bytes reproduced
  their compiled constants.

The complete existing public assembly candidate suite then passed
`47 / 47`. Total executed offline tests were `60 / 60 PASS`.

The synthetic valid profile existed only in test memory. No synthetic fixture,
hidden oracle, runtime profile, runtime package, or executable was persisted.

## 4. Deliberately unexecuted and unproved work

This report does not claim a native neutral-preloader implementation or
implementation acceptance. The following acceptance-plan obligations remain
unproved:

- authenticated runtime-profile and five-row package materialization;
- authenticated guard source/build/compiler/linker/import/CRT/binary/loaded-
  image closure;
- an actual direct `kernel32.dll!CreateProcessW` source and binary path;
- construction of live pipes, reduced root duplicate, and reduced preloader-
  process handle;
- immutable native `STARTUPINFOEXW` and
  `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` storage across the call;
- actual verifier PID/result binding from successful process creation;
- source/build/binary/import independent review;
- real-Windows platform build pinning and the bounded decoy/opposite-end
  inheritance probe; and
- official public assembly rehearsal and every later experimental gate.

No compiler was available in this environment (`cl`, `clang-cl`, and `gcc`
were absent). More importantly, v0.4 requires authenticated compiler, build,
import, runtime, and binary closure before compilation or execution. Therefore
this candidate did not compile, install dependencies, materialize a runtime,
or call `CreateProcessW`, `NtCreateFile`, `MoveFileExW`, another design-target
native API, provider/model/network, F0, oracle, executor, or judge path.

## 5. CONTROL disposition

The bounded implementation candidate is complete for its stated non-native
scope and is materially stronger than the earlier unconditional runtime-
profile blocker: it supplies the fixed schema executor, the ten executable
semantic relations, deterministic evidence/admission construction, internal
five-position ordering, and exact assembly pin bridge.

It is not sufficient to open a platform probe or official rehearsal. The
smallest rational next candidate is an independently reviewed native
source/build/import closure that preserves this fail-closed boundary. Only
after that closure produces authenticated source, compiler/build records,
imports, binary, and runtime-package identities should CONTROL consider a
bounded real-Windows platform-probe gate.
