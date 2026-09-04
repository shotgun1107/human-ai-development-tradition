# Public assembly runtime profile and neutral preloader implementation candidate report v0.4

## 1. Scope and provenance

This package is the corrected bounded stage-50 implementation candidate for
the authenticated runtime-profile and neutral-preloader v0.4 design. It adds
the native Windows preloader, native one-use handle guard, build contract,
runtime materializer, closed control schema, and runtime authority declaration
needed to test the pre-import boundary.

The final result recorded here is a bounded stage-50 TEST/VERIFICATION PASS.
It is not a final independent-review verdict, CONTROL acceptance, stage-70
platform result, stage-80 live-bridge result, official public rehearsal, or S0
run.

- repository: `human-ai-development-tradition`;
- branch: `codex/runtime-profile-neutral-preloader-v0.4`;
- base commit: `00491ddb9b656a901e62b31dc4a87d910dda2888`;
- base tree: `654285f032b30c389a97a6ee36c32dc98519376b`;
- authenticated v0.4 design-package manifest SHA-256:
  `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`;
- approving v0.4 design-rereview preservation-record SHA-256:
  `9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71`;
- corrected 19-file implementation-manifest SHA-256:
  `670803a185e6968f97acb8bdc4acd99932e4dc7722157816a28d684b9e9989f5`;
- first implementation-review preservation-record SHA-256:
  `9457b7c358026c22fbe15ec8ffc030828af1085b3577a33af327c44789f100a8`;
- final TEST artifact-manifest SHA-256:
  `7afb04bb27c21d8515e062201de3b972d9e4f06659d7972fee2033f67194900a`;
- final TEST evidence-ledger SHA-256:
  `103084ead090f180dae4418769a132a2d6804101dc09b65aff1b2f25a78ee64c`;
- final TEST verification-summary SHA-256:
  `ee2cb08872de7e3abce2a694fcb2a8fffcc126953487728111d2012651d249bb`.

DOCUMENTATION reauthenticated all six design-package targets, all 19 final
implementation targets, and all 1,008 exact external TEST artifact targets
with zero missing or mismatched files. That byte authentication is not a
substantive retest or an approval verdict.

## 2. Implemented bounded behavior

The candidate preserves the authenticated v0.3 Python implementation where
its bytes remain applicable and adds the v0.4 native boundary:

1. a direct native Windows preloader with the frozen `CreateProcessW` launch
   shape, one `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`, and five ordered
   inheritable handles;
2. a native `s0_runtime_handle_guard_v0_4` extension that validates and binds
   the five known handles once before a guarded transaction;
3. exact 28-key admission closure and bind-time preloader-process liveness;
4. evidence-bound external pin, runtime-profile v0.1 through v0.4 hashes, and
   workspace root;
5. canonical launch-handle-set evidence and postcreation admission tied to
   the actual verifier PID and frozen policy identifiers;
6. an exact x64 build contract and PowerShell build path for the EXE and PYD;
7. a materializer that revalidates the immutable v0.7 base runtime and exact
   overlay before producing a separate output root;
8. bounded overlap, replacement, reparse, hard-link, alternate-data-stream,
   inventory, size, and digest checks; and
9. a closed v0.4 control envelope, runtime authority record, pre-import
   bootstrap, closed profiles and schemas, and the ten-relation semantic
   validator.

The guard validates the five handles supplied to it. It is not a process-wide
handle enumerator, and this candidate does not claim the later stage-70 decoy,
concurrency, or broader-kernel result.

## 3. First independent review and corrections

The first independent implementation review returned `CORRECT/RETEST` with
`BLOCKING 0 / MAJOR 4 / MINOR 1`. Its preserved findings were:

- `IR-001` (MAJOR): exact 28-key admission closure gap;
- `IR-002` (MAJOR): bind-time preloader-liveness gap;
- `IR-003` (MAJOR): the positive matrix did not prove the required production
  negative cases;
- `IR-004` (MAJOR): lifecycle cleanup and Python evidence were not
  reproducibly chained; and
- `IR-005` (MINOR): the report over-attributed a generic exit `70` to a
  missing live bridge.

CODE correction 8 added exact admission-key closure and bind-time liveness.
CODE correction 9 symmetrically evidence-bound the external pin, profile
v0.1 through v0.4 hashes, and workspace root. TEST then rebuilt the production
artifacts and reran the affected and final bounded checks.

The two corrected native-source SHA-256 values are:

- preloader C++:
  `a32fb997638607e3577ac44382b29c015685920655ee1c2499aa975131250cae`;
- guard C++:
  `ed22d812d873a03e5d0f21a46a8c3a5e8eba47eb29744cf4e7e2341d814e599f`.

The first-review preservation record does not upgrade `CORRECT/RETEST` to a
final independent PASS. The corrected candidate still requires fresh
independent review.

## 4. Authenticated final TEST evidence

The following are TEST/VERIFICATION facts reauthenticated by DOCUMENTATION.
They are not a DOCUMENTATION or independent-review verdict.

### 4.1 Exact source, build, and binary chain

The final production build trace is the exact ledger-listed artifact
`build-production/build-trace.json`, SHA-256
`d1ae0edc69d59ab89e9d341aece05e3981e5a6752502596a638adff1590c2e35`.
It records:

- architecture: `x64`;
- build recipe `implementation/native/build.ps1` SHA-256:
  `82a3e842855c55453c945f04b341a63ff290e9b20b2548c921ca86d12ff43fd3`;
- MSVC `cl.exe` version `19.44.35228.0`, SHA-256:
  `88c8344236a27a6e727e0a8edc49aaa2690bdc7a9464b9d18cc7abe70a9f1c0d`;
- Microsoft `link.exe` version `14.44.35228.0`, SHA-256:
  `ca11e6c45debd34bf652dfe984c5360a531a005ed78bf72852330c9c2590cf0d`;
- Python 3.12 import library SHA-256:
  `f55daa479f2d82a073efbe6315c2164eb6c955cb1cc722ce03705afa8c93544f`;
- production `s0_neutral_preloader_v0_4.exe`, 289,792 bytes, SHA-256:
  `bc9de1aebae55a4f08af93ff5f9eb488cb7c696809d2ded64bebe968ac14a3a6`;
  and
- production `s0_runtime_handle_guard_v0_4.pyd`, 221,696 bytes, SHA-256:
  `c0e05fb39596db475780245581dadd52ea2b204a8267095c1c93fc2a160f73f1`.

The trace binds the build contract, build recipe, corrected two C++ sources,
and shared header to those outputs. It records the production compiler flags
`/O2`, `/W4`, `/WX`, `/GS`, `/guard:cf`, `/Qspectre`, `/sdl`, and `/MT`, and
the linker protections `/DYNAMICBASE`, `/HIGHENTROPYVA`, `/NXCOMPAT`,
`/CETCOMPAT`, and `/GUARD:CF`.

The PE/import/export/build audit passed 23 detailed rows plus its PASS summary.
This local build identity does not establish supplier, TLS, SDK, compiler,
linker, or tool provenance.

### 4.2 Immutable input, overlay, and final runtime

The immutable v0.7 input was identical before and after materialization:

- 182 total files: 174 payload plus 8 evidence files;
- 24,222,224 total bytes;
- canonical base manifest SHA-256:
  `8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798`;
- before and after snapshot SHA-256:
  `5819a930ddcd7087fed0bd6638fbf6f0e60ef9f17caf592a40b3abfee06ee46e`;
  and
- snapshot inventory SHA-256:
  `025d41d9e4173dd3761fac78216ef13254908c0e729168968f54cb7701010dfc`.

The final authenticated overlay contains 45 files and 798,666 bytes. Its
manifest SHA-256 is
`7ae9e33523dc4be720516533763bfae04d3c7e756c733c645bf0e630bbab510e`.

The final runtime contains 219 files and 24,937,513 bytes. Its exact final
manifest SHA-256 is
`67295a366ebc280830a0b993b3dac9358d3e9eb5c1652104e4ebf4f4cb36b009`.
TEST reports that all 174 base payload rows were preserved.

### 4.3 Production-guard negative matrix

The fresh-process invalid-input matrix used the production guard PYD and
reported:

- `70 / 70` expected rejections;
- `0` unexpected acceptances; and
- `70` unique child PIDs.

The six formerly accepted values now reject explicitly: `profile_1`,
`profile_2`, `profile_3`, `profile_4`, `external_pin`, and `workspace_root`.

The three zero-byte delayed-teardown cases also closed with explicit guard
results:

- `access_0`: `REJECTED`, result SHA-256
  `9f130a0246e10de64d5276a5c33f8c9234cbb048c4f430ec480d2145f7e207e1`;
- `kind_1`: `REJECTED`, result SHA-256
  `fe3e9883f8979a79d66ddcd822b2593b4a9fef22d8a15fb1d88557c38f9f83c7`;
- `state_1`: `REJECTED`, result SHA-256
  `9c60a2ff707b8e6c03f62a447e0c22680a438367b7817511b068df2835355eab`.

The matrix's mutation preloader and launch harness are TEST-only instruments,
not production artifacts. The production EXE identity is established by the
separate build and positive-lifecycle evidence.

### 4.4 Positive lifecycle and cleanup

The authenticated lifecycle artifacts are:

- `lifecycle-result.json` SHA-256:
  `e942701f313aa44d4a2322777a6c7359809debd99295f35af5a96bf3aef9fb46`;
- `lifecycle-run.json` SHA-256:
  `d6d501952b3cef608acb7956e1dd6f27f5a08cbdef4681cb32329319d11c70c4`.

They record admission-handle close, first bind PASS, first commit PASS,
repeated bind and commit rejection, and post-commit deallocation PASS. After
deallocation, all five inherited handle locators returned
`ERROR_INVALID_HANDLE=6`: admission-read, commit-request, commit-reply,
output-root, and preloader-process. The recorded output-root locator is
`0x00000000000008d8`; the preloader-process locator is
`0x00000000000008dc`.

The production preloader exited `0`, and the atomically created output root
was empty. The TEST-owned lifecycle bootstrap is diagnostic evidence for this
bounded lifecycle, not the production downstream live bridge.

TEST checked 142 recorded mutation, lifecycle-child, and preloader PIDs; none
remained active. TEST reports zero repository changes, zero F0 accesses, zero
network accesses, zero Git mutations, and no `__pycache__` in its checked
scope.

### 4.5 Python, schemas, semantics, and final QA

The named Python, closed-schema, and ten-semantic-relation harness reported
`16 / 16 PASS`, chained to these predecessor schema hashes:

- schema v0.1:
  `92943a96249c312d0e2631705a667170d60d22d8e75f2571961ed1f728e934af`;
- schema v0.2:
  `e2e96940bbafc6a80987634fe794d700844dbc7d0b48e0e269922f03364fb34f`;
- schema v0.3:
  `1404f4981d3d7815e98a6c5d745596f15bb8d50a296410584d03d7ccb11ce3dd`.

The corresponding runtime-profile hashes for v0.1 through v0.4 are
`e0f7559d16068cc4cb6589a87fdb2129915ab018a76e41cfc09b4259d543008e`,
`3a0f2fd92629e4a3eb419ab2ae2dbc586bf83ae7152a8b08cfdcabc966028125`,
`9741561972db10c39b824b60364219a07e1e1a440f154b562bae91f864aeb8c5`,
and `266087f18cb16ced698fdfc8089a6ca305aac1d5d0278b1ee4c51f23044b3e9e`.

The final bounded QA matrix reports `15 PASS / 0 FAIL / 4 UNVERIFIED`.
The four unverified rows are stage-70 concurrency/platform, stage-80 live
integration, official rehearsal, and S0.

### 4.6 Excluded generic exit-70 observation

An aborted attempt produced generic exit `70` without an isolated cause. That
observation is excluded from relied evidence and is not attributed to a
missing live bridge or any other specific cause.

## 5. Bounded TEST disposition

TEST reported bounded stage-50 PASS for the authenticated 19-file candidate,
its source/build/binary chain, immutable input and materialization closure,
production-guard negative cases, positive one-use lifecycle, chained Python
and schema/semantic checks, PE/build audit, and recorded-process cleanup.

This is a TEST/VERIFICATION result awaiting a fresh independent review and
CONTROL decision. DOCUMENTATION neither approves nor expands it.

## 6. Mandatory nonclaims

This candidate does not prove or claim:

- stage-70 platform, decoy, concurrency, or broader-kernel behavior;
- stage-80 live bridge, live assembly, or a production live-consumer
  transaction;
- supplier, TLS, package-manager, compiler, linker, SDK, or tool provenance;
- resistance to a same-user attacker or local administrator, or build-input
  TOCTOU resistance;
- correctness across all Windows versions or filesystems, or full operating-
  system loader, standard-library, native-library, or dynamic-import closure;
- an official public end-to-end assembly rehearsal;
- F0 access, hidden-oracle access, executor or judge work, provider/model
  access, a network transaction, or Git mutation by TEST; or
- S0 execution, central-system implementation, Project Brain integration,
  operational safety, economic value, or model-to-model transfer.

## 7. Candidate disposition

The corrected 19-file v0.4 implementation and authenticated bounded
stage-50 TEST record are ready to be presented to a fresh independent code and
security reviewer. This report does not issue that review verdict and does not
pre-authorize CONTROL acceptance, publication, commit, push, PR creation,
`main` integration, stage 70, stage 80, or any later gate.
