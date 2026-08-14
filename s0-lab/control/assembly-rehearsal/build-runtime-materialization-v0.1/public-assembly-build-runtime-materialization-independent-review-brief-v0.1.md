# S0 v0.14 public assembly build and runtime materialization design v0.1 independent review brief

## 1. Reviewer role and prohibited work

Use one fresh independent public-design reviewer that did not author, advise
on, or QA this v0.1 package. The reviewer must reconstruct the design from
authenticated public bytes and must not use the author conversation or another
review conclusion.

This is a read-mostly design review. Do not implement native or Python code,
install or invoke a compiler, create a runtime tree, execute a candidate
binary, load a DLL, call a native API, run a platform probe or rehearsal, or
access F0 content. Do not use provider/model execution, an oracle, executor,
judge, score, S0, or E0 input.

## 2. Exact baseline and external values required from CONTROL

CONTROL must provide all of these literal values in the review assignment:

- repository origin;
- review branch and exact HEAD;
- exact tree and sole parent;
- exact candidate remote-tracking ref and value;
- exact new design-package manifest SHA-256;
- exact hash for each candidate logical artifact and sidecar;
- exact hashes listed in Section 3; and
- exactly two authorized output paths from Section 9.

The reviewer must not infer a value from a moving branch, author report,
neighboring file, prior conversation, directory scan, or expected naming
convention.

## 3. Exact maximum public input set

The maximum set is the following literal files and the literal target rows of
the named authenticated manifests. A manifest target set means exactly the
paths encoded in that manifest after the manifest itself matches the stated
external pin; it does not permit directory enumeration or another path.

### 3.1 Governing and candidate inputs

1. `AGENTS.md`;
2. `s0-lab/control/tools/verify-text-artifacts.ps1`;
3. `s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.1/design-package-files.sha256`;
4. every logical target named by item 3;
5. every same-basename sidecar of the item 4 targets; and
6. no other file in the candidate directory.

### 3.2 Current CONTROL, candidate, and review records

1. `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.2/bounded-integration-implementation-v0.1-control-integration-and-main-merge-decision-v0.1.md` and sidecar, Markdown SHA-256 `acdbc42e75197ca22a078c4e8c8353f834be17dd6332f0c9ca361d70c6722d1a`;
2. `s0-lab/assembly-rehearsal/public-end-to-end-v0.2/verification/implementation-files.sha256`, SHA-256 `7469f62d67c9d5f416f38db7e4a14b5f3819e739cf38a71f1fec452421a7fabe`, and its exact 3 targets;
3. `s0-lab/assembly-rehearsal/public-end-to-end-v0.2/verification/verification-files.sha256`, SHA-256 `8f8140d678e5846639ff382b32035c342dc8b2dd7d929da5ff37a759f8aa9d7b`, and its exact 4 targets;
4. `s0-lab/reviews/assembly-rehearsal/public-end-to-end-v0.2/bounded-integration-implementation-v0.1-independent-review-v0.1.md` and sidecar, Markdown SHA-256 `ddf5d4ade01c4d87a2e027d8487a9c5a34e317a3df3aee1e19d624492849dbc0`;
5. `s0-lab/reviews/assembly-rehearsal/public-end-to-end-v0.2/bounded-integration-implementation-v0.1-minor-rereview-v0.1.md` and sidecar, Markdown SHA-256 `3adbdbb3a30457c7b9baae319e7e31b4def993c454e24182d4b3596a573d99aa`;
6. `s0-lab/reviews/assembly-rehearsal/public-end-to-end-v0.5/public-end-to-end-assembly-rehearsal-design-v0.5-independent-rereview-v0.1.md` and sidecar, Markdown SHA-256 `7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137`;
7. `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.4-independent-rereview-result-preservation-record-v0.1.md` and sidecar, Markdown SHA-256 `9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71`; and
8. `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.2/public-end-to-end-assembly-runtime-profile-neutral-preloader-integration-design-v0.2-independent-rereview-result-preservation-record-v0.1.md` and sidecar, Markdown SHA-256 `947b2713a04291357be88be86f96d1a2d805058b0ec602c3b5f4812b00db308c`.

### 3.3 Effective public design and implementation closures

1. `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/design-package-files.sha256`, SHA-256 `6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802`, and its exact 5 targets plus their sidecars;
2. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/design-package-files.sha256`, SHA-256 `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`, and its exact 6 targets plus their sidecars;
3. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.1/design-package-files.sha256`, SHA-256 `f55352771432404f4c2e9337665184e18afde076b8b3efe7a455ee6694d60e6b`, and its exact 5 targets plus their sidecars;
4. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.2/design-package-files.sha256`, SHA-256 `1349c6c4c97d24256f98216eb86a353451891419044b61d22c5c14d7eded5e7c`, and its exact 6 targets plus their sidecars;
5. `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/implementation-files.sha256`, SHA-256 `0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623`, and its exact 32 targets;
6. `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/verification/implementation-files.sha256`, SHA-256 `5022d517864cae19520a1e3e34a683965609abf0ef29e167b30a11bade4a32c2`, and its exact 11 targets;
7. `s0-lab/i0/verification/implementation-files.sha256`, SHA-256 `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae`, and its exact 15 targets;
8. `s0-lab/i1/verification/implementation-files.sha256`, SHA-256 `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c`, and its exact 26 targets;
9. `s0-lab/i2/verification/implementation-files.sha256`, SHA-256 `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6`, and its exact 16 targets;
10. `s0-lab/i3/verification/implementation-files.sha256`, SHA-256 `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648`, and its exact 17 targets; and
11. `s0-lab/public-practice/v0.1/bundle-files.sha256`, SHA-256 `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637`, and its exact 90 targets.

The reviewer may authenticate all listed target bytes but should read only
the files needed to reconstruct source imports, runtime mapping, and effective
design obligations. The allowlist is a maximum, not a reading quota.

## 4. Integrity procedure

1. authenticate Git identity and initial clean state;
2. run canonical validator SelfTest;
3. authenticate the candidate manifest before candidate content;
4. validate each admitted Markdown/sidecar separately;
5. apply byte-level UTF-8/no-BOM/final-LF/trailing-whitespace and canonical
   sidecar checks to JSON;
6. parse JSON with duplicate-key rejection;
7. validate the profile schema against Draft 2020-12 metaschema;
8. authenticate every predecessor manifest before reading a target;
9. retain exact input hashes for final recheck; and
10. stop as `INVALID-REVIEW` on any mismatch or boundary violation.

Do not use a decoded-string BOM test. Do not pass multiple artifact paths as
one PowerShell string. A reviewer-local checker error is corrected and rerun;
it is not a candidate finding unless the candidate caused it.

## 5. Required hostile reconstruction

Independently reconstruct and challenge:

- the current offline-only implementation boundary;
- all ten missing external pin classes;
- exact source/toolchain/command closure;
- two clean independent builds and all-output equality;
- PE/import/export/resource/mitigation inspection without loading targets;
- unsigned candidate policy;
- runtime path grammar, exact set, identity, read-back, and atomic publication;
- exact CPython/dependency/source-only import closure;
- failure precedence, quarantine, resource limits, and diagnostic-only records;
- the 46-row mutation matrix; and
- all later-gate and F0 nonclaims.

Agreement with prose is not evidence. Build one counterexample for every
mutation class and map it to one exact failure label and action boundary.

## 6. Key review questions

The review must answer at least:

1. Can any missing compiler, SDK, Python, dependency, source, or platform pin
   be filled from ambient state?
2. Can A and B share a byte, cache, generated object, process, or path that
   makes equality circular?
3. Can a nondeterministic output be patched or selected after comparison?
4. Can the static inspector omit an import or trust tool output without
   binding it to exact binary bytes?
5. Can a Windows path alias or object type create a second runtime-tree view?
6. Can the materializer publish before every file is closed, reopened, and
   rehashed?
7. Can host Python, site packages, DLL search, registry, or PATH satisfy a
   missing runtime row?
8. Can a record, manifest, build PASS, or runtime-tree equality become live or
   rehearsal authority?
9. Are the resource bounds mutually identical in prose, map, schema, and
   acceptance plan?
10. Does any requirement presuppose a native source, tool, or behavior that
    the design correctly marks as still absent?

## 7. Severity and verdict

- `BLOCKING`: grants denied content or live/rehearsal authority, permits
  unpinned executable input, or invalidates review integrity/independence;
- `MAJOR`: leaves source, toolchain, build, binary, runtime, failure, resource,
  or provenance behavior incomplete, contradictory, or multiply interpreted;
- `MINOR`: bounded exactness issue unable to affect executable bytes,
  authority, or a primary conclusion.

Return exactly one:

- `PASS-FOR-PUBLIC-BUILD-RUNTIME-IMPLEMENTATION-CONSIDERATION-ONLY` with zero
  BLOCKING and zero MAJOR findings;
- `REVISE-AND-REVIEW` with any finding; or
- `INVALID-REVIEW` for authentication, allowlist, independence, or F0 failure.

## 8. Evidence limits

The review is design evidence only. It must state that no compiler, build,
runtime tree, native API, loaded image, platform behavior, live decision,
official rehearsal, F0 input, provider/model, S0, or E0 result was created or
observed.

## 9. Exact authorized outputs

Write exactly:

1. `s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.1/public-assembly-build-runtime-materialization-design-v0.1-independent-review-v0.1.md`;
2. `s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.1/public-assembly-build-runtime-materialization-design-v0.1-independent-review-v0.1.sha256`.

After writing, run canonical validation, independently rehash the pair and all
inputs, require an exact two-file change set, confirm unchanged Git identity
and F0 aggregates, and report the verdict and findings. Do not commit or push.

With a valid PASS, the exact next candidate gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION DESIGN CONTROL INTEGRATION OPEN`
