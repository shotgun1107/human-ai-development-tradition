# S0 v0.14 I2 public implementation v0.4 independent review v0.1

- `review_date`: `2026-08-12 KST`
- `review_role`: fresh independent PUBLIC-ONLY implementation reviewer
- `review_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.4 INDEPENDENT REVIEW OPEN`
- `candidate_branch`: `codex/s0-trust-root-role-isolation-public-implementation-v04-independent-review`
- `candidate_head`: `cfb532f72a1434095e2a7af754e9f7c414e3b888`
- `candidate_tree`: `1aadf50b88c7c6fa1de56f6582739dc65e6f1a43`
- `candidate_sole_parent`: `5e374933a80fd89afb85649c83353317d40581ec`
- `implementation_manifest_sha256`: `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6`
- `verdict`: `PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`
- `claim_kind`: bounded public implementation-construction review only

## 1. Verdict and finding count

The v0.4 candidate closes predecessor finding `I2-V03-m01`. Both exported
global-sequence APIs accept a canonical 5,001-digit nonnegative integer exactly
like its canonical text, reject invalid inputs with stable project errors, and
leave Python's process-global integer-string digit limit unchanged. The earlier
supplied-set route-identity and five-ID ownership closures also remain intact.

| Severity | Count |
|---|---:|
| blocking | 0 |
| major | 0 |
| minor | 0 |

The exact verdict is `PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`. It is
not an operational, cryptographic, provider, E0, or S0 result and does not open
another gate automatically.

## 2. Independence, role boundary, and Git baseline

The reviewer did not author or advise on v0.4, used no other reviewer or
subagent, used no web or outside source, and did not inherit the author's
closure conclusion. The predecessor independent review was authenticated and
read first. Its finding was reconstructed and closure criteria were fixed
before candidate implementation details were inspected.

The review used only the exact assigned worktree. Normalized path comparison,
branch, HEAD, tree, sole parent, and parent tree matched the externally supplied
values. Initial status was clean. The parent-to-candidate diff contained 13
path records, all under `s0-lab/i2/**`; a quiet exclusion diff proved zero
tracked change elsewhere. The records were 12 modifications and one v0.3 to
v0.4 contract rename. Aggregate tracked F0 counts were 32, 11, and 10, and all
three parent-to-candidate F0 quiet-diff exit codes were zero.

No F0 default-deny content or filename was opened, searched, printed, hashed,
or used. Only aggregate counts and quiet-diff results were obtained. No key,
signature, registry, VM/sandbox, provider/model, protected material,
fixture/oracle, E0, or S0 capability was executed. Repository writes were
limited to this review Markdown and its same-basename sidecar. No commit, push,
merge, or PR was performed.

## 3. Authenticated inputs

The root instructions were hashed before being read. The implementation
manifest and its anchor matched their external pins; the anchor contained one
canonical record binding the exact manifest hash and basename. The manifest
contained exactly 16 ordered, unique rows with zero missing files or hash
mismatches. The public-source manifest matched its external pin and contained
exactly 12 ordered, unique rows with zero missing files or hash mismatches. The
predecessor review pair matched both external pins before it was read.

There were exactly 34 unique admitted inputs:

| Input | Complete-file SHA-256 |
|---|---|
| `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` |
| `s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |
| `s0-lab/i2/verification/implementation-files.sha256` | `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6` |
| `s0-lab/i2/verification/implementation-manifest.sha256` | `82d0167eaa8bde75b58f5c3bf116de1a91e555f16e7de85444f3eaf6736df00c` |
| `s0-lab/i2/implementation/s0_i2/__init__.py` | `9fdbfc779202a69b061465836c46fc5e1a143f2b24a06f6d918ac69445d94fcf` |
| `s0-lab/i2/implementation/s0_i2/canonical.py` | `93873f098e551478140b6b90e89466849ba523ef7a48bc59121a83099126ce0b` |
| `s0-lab/i2/implementation/s0_i2/cli.py` | `27fa7866ec9676aa07a17ed89c55818073c0bafb8cae157f714f82989cd06f38` |
| `s0-lab/i2/implementation/s0_i2/contract.py` | `a434bd7e6d6b113cefe1339ceb9dfd8985c30677c605677ffd2106c6f8977a42` |
| `s0-lab/i2/implementation/s0_i2/errors.py` | `4ac722f697c4dfed911c77874341edf0e2a45f89f4548834baa74b5be3c6842f` |
| `s0-lab/i2/implementation/s0_i2/lifecycle.py` | `c31fbe83dc02a4c05be5b83b8f39a68b54ce127e88249d77c4c481dbdc5764ba` |
| `s0-lab/i2/implementation/s0_i2/records.py` | `c83d7e0832e38c74b96e38ef8ddea71182cf29f5eb9f1df51f7013df5d27d5b9` |
| `s0-lab/i2/implementation/s0_i2/vectors.py` | `65b601a3e73fcca85e8da752e4e8daf0b0e3b2141813c0066a39d7984ddca75e` |
| `s0-lab/i2/README.md` | `e0a89bf910ac4d1945f2ece78242c315a2a0b66760375004e2eb726187c4a9ae` |
| `s0-lab/i2/README.sha256` | `52173876a43de36805500b301b0364584bb30e44ce70fdb2fdf1f91765e0c8e2` |
| `s0-lab/i2/spec/public-source-files.sha256` | `e55b5945141d77a72880b6a9803e9d98ef0a92669711478bccdda043b0bd95a1` |
| `s0-lab/i2/spec/trust-root-role-isolation-contract-v0.4.json` | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` |
| `s0-lab/i2/tests/test_i2.py` | `be94df24b11e3b48cc4cc86f64aecaa5a17aeed3f6651b692002314686f3e8a6` |
| `s0-lab/i2/tools/verify-i2.ps1` | `bded132df64a274f68904bae33459ae0b87b7100ee3a4a15fc60c61a03f39fbe` |
| `s0-lab/i2/verification/verification-report.md` | `2ad17e66cf1cae6d0962c5eb0ca17d79b5419bd8c8f6831afac549332cedb7d4` |
| `s0-lab/i2/verification/verification-report.sha256` | `bd3bb58000b18dd205a42aca1ac947cf07d9476b36d5049cc1cf9bc2a1cd8673` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.md` | `f172ba01bc37a6a96077f6441aca24cd525f19f034623c752d638a00ec0378c0` |
| its `.sha256` sidecar | `36866659b1c401b5775c581c675b999489d786e7d5feb62cd9afa262de33c9cb` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md` | `5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3` |
| its `.sha256` sidecar | `8332a01452c3207321e48b6fde5736ed2ecccda493474ae05cd51f5723fad545` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md` | `19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8` |
| its `.sha256` sidecar | `22333a6d80cd32ddd60947c6ade212331eece9b1e067958fc2264d1882f20f9a` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md` | `f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73` |
| its `.sha256` sidecar | `3765f11d814d1fbacb55b3a3600f642c51d4d2a16d5012bfaa7ba9680fe9f03d` |
| `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-control-final-freeze-decision-v0.1.md` | `271ff05d7af484b072264a5c1f9d6a6bb157b0a6766613da5c6ddae8b994475c` |
| its `.sha256` sidecar | `095660dc02a72df89c8c71e2d92e270f34f66b4ad0141a39def670a8743d0122` |
| `s0-lab/i1/spec/public-runtime-files.sha256` | `9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e` |
| `s0-lab/i1/spec/public-runtime-v0.14.json` | `fd9e4a474bb5438065dff0a51c24cd2eb4e8e1caa2cbb5d6eb169b540c691d08` |
| `s0-lab/reviews/i2/i2-public-implementation-v03-independent-review-v0.1.md` | `ba18afafacb86035bc4835e4807ee602ab86306bcc38ee03ca65a4d6e43a2473` |
| its `.sha256` sidecar | `cde1cd31e1250e7113f2064c68ccb004ac7b4babb0f5ffd0e08a9b0dc8020276` |

## 4. Canonical validator and shipped verifier

The canonical text validator's complete-file hash matched the authenticated
predecessor input record before execution. Its SelfTest passed all eleven
regression cases. All eight admitted Markdown/same-basename sidecar pairs
passed independently labeled UTF-8 validity, BOM absence, final-LF,
trailing-whitespace, sidecar-format, sidecar-hash, and overall checks: the
predecessor review, candidate README, candidate verification report, four v0.4
design/CONTROL pairs, and the final vector-freeze pair.

The shipped verifier was run with the exact external pin:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File s0-lab/i2/tools/verify-i2.ps1 -ExpectedManifestSha256 18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6
```

It exited zero. It authenticated 16 payload rows and the exact 12 public
sources, created and rehashed an authenticated snapshot, ran under Python
`>=3.12,<4.0` with site disabled and safe path enabled, and reported 38 tests,
zero failures, errors, skips, expected failures, or unexpected successes.
`STATIC_INTEGRITY`, `PUBLIC_SOURCE_INPUTS`, `UNIT_TESTS`, `CONTRACT_CLI`,
`FORBIDDEN_IMPORT_AUDIT`, `MODEL_FREE_BEHAVIOR_TESTS`, and `FINAL_STABILITY`
were `PASS`. `CLOSED_BOUNDARIES` remained `BLOCKED_NOT_EXECUTED`. This is
candidate verifier evidence, not the independent verdict.

## 5. Independent finding reconstruction and frozen closure criteria

`I2-V03-m01` was independently reconstructed from the authenticated v0.3
review. The public global-link and global-chain signatures declared
`str | int`, but their integer normalization used `str(value)`. Canonical
5,001-digit text therefore passed while the numerically identical `10**5000`
leaked Python's raw `ValueError` at the default 4,300-digit conversion limit.
The defect was fail-closed but contradicted the declared input surface and
stable I2 error contract.

Before reading v0.4 implementation details, the following closure criteria
were fixed:

1. Both exported global-link and global-chain APIs must accept the canonical
   5,001-digit nonnegative integer exactly like its canonical text.
2. Neither API may leak `ValueError`, `OverflowError`, or `RecursionError`.
3. Negative integers, `bool`, malformed canonical text, and non-string/non-int
   values must produce stable project validation errors.
4. The process-global integer-string digit limit must be identical before and
   after all normalization probes.
5. Zero, values around the base/chunk boundary, and multi-chunk values must
   normalize to the exact canonical decimal.

## 6. Independent model-free probe results

All probes ran from temporary in-memory scripts/processes with `-B -S -P`; no
repository probe file was created.

| Probe area | Independent result |
|---|---|
| 5,001-digit equivalence | `10**5000` and `"1" + "0"*5000` passed both global-link and one-event global-chain entry points |
| zero and chunk boundaries | `0`, `1`, `10^9-1`, `10^9`, `10^9+1`, `10^18-1`, `10^18`, and `10^18+1` passed as both text and integer through both APIs |
| multi-chunk canonicality | `10^90 + 10^45 + 123456789` passed all four text/integer and link/chain combinations |
| hostile huge boundaries | `10**5000-1` with 5,000 nines and `10**5000+1` with the hand-constructed canonical text passed both APIs |
| huge successor | a two-event chain from 5,000 nines to the 5,001-digit power of ten passed when the start was supplied as the huge integer |
| invalid normalization | 18 values covering negative and huge-negative integers, both booleans, empty/leading-zero/signed/space/non-ASCII-digit text, `None`, float, bytes, list, object, and an `int` subclass rejected on both APIs |
| error stability | each invalid call was repeated twice; every type/message pair was stable `LifecycleError`, with no raw runtime exception |
| process safety limit | `sys.get_int_max_str_digits()` was 4300 before and after; direct built-in `str(10**5000)` still raised the limit error |

The primary matrix covered 40 valid API/form combinations and 72 repeated
invalid calls, with zero failures. Additional hostile huge-boundary and
successor probes also had zero failures.

## 7. Code, contract, documentation, and non-regression audit

### 7.1 `I2-V03-m01` disposition — closed

`canonical.normalize_decimal` retains exact-type input discipline. Negative
integers reject and zero returns `"0"`. Positive integers are divided into
base-1e9 chunks; only bounded chunk values are converted with `str`/decimal
formatting, the head is unpadded, and every tail chunk is exactly nine digits.
The operation is iterative, contains no recursion or hidden application
ceiling, imports no `sys`, and never calls or exposes a process-global digit
limit setter.

Both public APIs already route expected sequence input through this one
normalizer and translate `CanonicalRecordError` to `LifecycleError`. The new
test exercises `10**5000` at both entry points and retains negative and boolean
rejection. Source inspection and the independent matrix establish the broader
malformed-type and chunk-boundary behavior.

The v0.4 contract identifies ceiling-free canonical text or nonnegative
integer normalization within the same bounded caller-supplied structural-link
scope. README and verification-report claims accurately describe the base-1e9
mechanism, stable invalid-input errors, and unchanged process safety limit.

### 7.2 Earlier supplied-set closures — retained

The aggregate validator still uses separate `seen_route_identities`,
`identifier_owners`, and `emitted_event_ids` structures. Route identity is
rejected before a second group is registered. Each route registers its
nonzero result-media ID and all four preallocated `R/A/P/C` IDs, including IDs
unused by an early terminal. Emitted event IDs remain an independent check.

Independent probes passed a disjoint two-route set, then rejected three
identical/contradictory repeated-identity cases. Four result/result,
result/unused-event, unused-event/event, and emitted-event overlap classes each
rejected in both group orders. These results retain the v0.3 dispositions of
`I2-V02-M01` and `I2-V02-M02` at the explicitly caller-supplied-set scope;
project-lifetime uniqueness remains blocked.

### 7.3 Closed capabilities and bounded change

All nine public admission/outcome/classification/ledger/witness entry points
independently raised named `UnsupportedBoundaryError` values beginning with
`BLOCKED:`. No closed capability executed. Contract, README, report, CLI, and
verifier output preserve complete classification, durable ledger/witness,
actual registry/key/signature authority, process/VM enforcement,
provider/model, protected material, fixture/oracle, E0, and S0 as unavailable.

The 13-record candidate diff is bounded to the normalization repair, a focused
regression test, v0.4 version/contract bindings, matching documentation, and
their manifests/sidecars. CLI, errors, vectors, the public-source manifest, and
the verifier retained their authenticated bytes. `git diff --check` passed.
No unrelated implementation or capability change was found. The author
verification report was treated only as a claim and matched independently
observed behavior within its stated boundary.

## 8. Findings and exact verdict

| Finding | Severity | Disposition |
|---|---|---|
| `I2-V03-m01` | predecessor minor | closed |
| `I2-V02-M01` | predecessor major | retained closed |
| `I2-V02-M02` | predecessor major | retained closed |
| new findings | none | zero blocking, zero major, zero minor |

The exact verdict is:

`PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`

A valid zero-finding result permits only separate user consideration of the
maximum next gate:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.4 CONTROL INTEGRATION DECISION OPEN`

That gate is not opened by this report.

## 9. Evidence limits and final audit

This review authenticates and tests only bounded public construction evidence.
It does not validate an actual trust root, role isolation, cryptographic
correctness, registry or key authority, durable ledger/witness, platform or
provider enforcement, protected work, fixture/oracle work, E0, S0, the central
system, Project Brain integration, operational safety, economic value,
production readiness, or model-to-model transfer.

After all verifier, probe, output-validation, and review work, all 34 admitted
inputs were rehashed and had zero mismatches. Final normalized worktree path,
branch, HEAD, tree, sole parent, and parent tree remained the exact baseline.
F0 aggregate counts remained 32/11/10 with zero candidate/parent quiet diffs.
Final status contained exactly the two authorized untracked review outputs and
no other change.
