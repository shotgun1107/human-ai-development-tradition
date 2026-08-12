# S0 v0.14 I2 public implementation v0.3 independent review v0.1

- `review_date`: `2026-08-12 KST`
- `review_role`: fresh independent PUBLIC-ONLY implementation reviewer
- `review_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.3 INDEPENDENT REVIEW OPEN`
- `candidate_branch`: `codex/s0-trust-root-role-isolation-public-implementation-v03-review`
- `candidate_head`: `be1d56c0f98dba97919f294c253fc1d8368ef623`
- `candidate_tree`: `78541d25d6fb80fbe2738336674d49e375de0610`
- `candidate_sole_parent`: `01a1430d29d3c87e9448d9370a404e60371f721d`
- `implementation_manifest_sha256`: `39386244bba397a1354204b7735508603b3071ef8884f60391beefabc6b21a24`
- `contract_sha256`: `d7d1e877d618508ffcd0f4148d5a8fd0137c2ae4fdca5267fd40e9164c15cd15`
- `verdict`: `REVISE-AND-REVIEW`
- `claim_kind`: bounded public implementation-construction review only

## 1. Verdict and finding count

The two v0.2 major supplied-set findings are closed by the v0.3 candidate.
The candidate nevertheless requires revision and a fresh independent review
because one new minor finding remains in the declared integer form of the
global-sequence comparison API.

| Severity | Count |
|---|---:|
| blocking | 0 |
| major | 0 |
| minor | 1 |

This verdict is not an implementation, operational, cryptographic, provider,
E0, or S0 result. It does not open CONTROL integration or any later gate.

## 2. Review validity and authenticated input boundary

### 2.1 Baseline facts

Before substantive review, Git metadata established the exact branch, HEAD,
tree, sole parent, and a clean worktree. The candidate/parent diff contained
13 path records: 11 modified, one added, and one deleted. Twelve records were
current admitted I2 paths; the sole deletion was predecessor contract-path
metadata, whose content was not read; there were zero other paths. Of the 18
current I2 namespace files, 12 changed and six were unchanged from the parent.

The 16-row implementation manifest had 16 unique paths, zero syntax failures,
zero missing files, and zero hash mismatches. Its complete-file SHA-256 matched
the externally supplied value, and `implementation-manifest.sha256` contained
the exact canonical corroborating record. The v0.3 contract complete-file hash
matched its separate external pin.

The 12-row public-source manifest had 12 unique paths, zero syntax failures,
zero missing files, and zero hash mismatches. The v0.2 review pair was also
authenticated before its findings were used.

The canonical text validator SelfTest passed all eleven regression cases.
Every admitted Markdown/same-basename sidecar pair to which it applied passed
UTF-8, BOM absence, final LF, trailing-whitespace, canonical sidecar, and hash
checks: the v0.2 review, candidate README, candidate verification report, four
v0.4 design/CONTROL pairs, and the final vector-freeze pair.

Execution note: an initial native multi-path argument form and one mistyped
nonexistent path produced `FILE_PRESENT=FAIL`; neither result was treated as a
validation. Exact-path invocations then validated all eight real pairs. No
bytes outside the admitted input set were read.

### 2.2 Complete admitted-input hashes

There were exactly 34 unique admitted input files.

| Input | Complete-file SHA-256 |
|---|---|
| `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` |
| `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-control-final-freeze-decision-v0.1.md` | `271ff05d7af484b072264a5c1f9d6a6bb157b0a6766613da5c6ddae8b994475c` |
| `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-control-final-freeze-decision-v0.1.sha256` | `095660dc02a72df89c8c71e2d92e270f34f66b4ad0141a39def670a8743d0122` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.md` | `f172ba01bc37a6a96077f6441aca24cd525f19f034623c752d638a00ec0378c0` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.sha256` | `36866659b1c401b5775c581c675b999489d786e7d5feb62cd9afa262de33c9cb` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md` | `19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.sha256` | `22333a6d80cd32ddd60947c6ade212331eece9b1e067958fc2264d1882f20f9a` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md` | `f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.sha256` | `3765f11d814d1fbacb55b3a3600f642c51d4d2a16d5012bfaa7ba9680fe9f03d` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md` | `5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.sha256` | `8332a01452c3207321e48b6fde5736ed2ecccda493474ae05cd51f5723fad545` |
| `s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |
| `s0-lab/i1/spec/public-runtime-files.sha256` | `9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e` |
| `s0-lab/i1/spec/public-runtime-v0.14.json` | `fd9e4a474bb5438065dff0a51c24cd2eb4e8e1caa2cbb5d6eb169b540c691d08` |
| `s0-lab/i2/implementation/s0_i2/__init__.py` | `78946756655afc4e35c45f31f23ff01443f652d147cc7c53c0ed49a1afd38123` |
| `s0-lab/i2/implementation/s0_i2/canonical.py` | `5e29dcc37eb733b92096011fe292e4779ec5f90e8cbf51221f2475c1bcae0eb6` |
| `s0-lab/i2/implementation/s0_i2/cli.py` | `27fa7866ec9676aa07a17ed89c55818073c0bafb8cae157f714f82989cd06f38` |
| `s0-lab/i2/implementation/s0_i2/contract.py` | `37f21dbcb18ed95572180e8a463600cf5b57e3ef003d629fa4395c7bcb7ad1dc` |
| `s0-lab/i2/implementation/s0_i2/errors.py` | `4ac722f697c4dfed911c77874341edf0e2a45f89f4548834baa74b5be3c6842f` |
| `s0-lab/i2/implementation/s0_i2/lifecycle.py` | `36efc0013e29ec43d11d25c630db424ed108b3c5400e24d2d0c910456f251880` |
| `s0-lab/i2/implementation/s0_i2/records.py` | `612a632ac5d639638ac662aaa54d54a92c0717726ea701f424708445bac65b90` |
| `s0-lab/i2/implementation/s0_i2/vectors.py` | `65b601a3e73fcca85e8da752e4e8daf0b0e3b2141813c0066a39d7984ddca75e` |
| `s0-lab/i2/README.md` | `34efa82564dec801425c1b975d5f14ba3faa7d8d177775c2d8edb6c1eb8eaa88` |
| `s0-lab/i2/README.sha256` | `5e286efe8e7e947dd117eed9cf063caf7b4fd1a8994145403d5085b56f65da70` |
| `s0-lab/i2/spec/public-source-files.sha256` | `e55b5945141d77a72880b6a9803e9d98ef0a92669711478bccdda043b0bd95a1` |
| `s0-lab/i2/spec/trust-root-role-isolation-contract-v0.3.json` | `d7d1e877d618508ffcd0f4148d5a8fd0137c2ae4fdca5267fd40e9164c15cd15` |
| `s0-lab/i2/tests/test_i2.py` | `4bcc44e23e6261dea4ca4a6ec50fa4998b649d9349e1d8caf2abec3310f34cce` |
| `s0-lab/i2/tools/verify-i2.ps1` | `bded132df64a274f68904bae33459ae0b87b7100ee3a4a15fc60c61a03f39fbe` |
| `s0-lab/i2/verification/implementation-files.sha256` | `39386244bba397a1354204b7735508603b3071ef8884f60391beefabc6b21a24` |
| `s0-lab/i2/verification/implementation-manifest.sha256` | `0b004c01b097da79f4b5127b256cc46b6174c825ef33265f5015b935e5a9a0d2` |
| `s0-lab/i2/verification/verification-report.md` | `83b789911241847c51a07450cbd01eb6d8a5f02b1ef6d1edc6e51b4c915757c9` |
| `s0-lab/i2/verification/verification-report.sha256` | `529c69f53e4504c103deabf101bcb15f49ea820d4ca6feacb7ab2ce730f8acd7` |
| `s0-lab/reviews/i2/i2-public-implementation-v02-independent-review-v0.1.md` | `e1b7672e7930cd00246de9263dc3ef7a348b756816ac841f426bc98f4ab27028` |
| `s0-lab/reviews/i2/i2-public-implementation-v02-independent-review-v0.1.sha256` | `daa5c0a10b0398887e088ba34e00af9403054ec0cefac6454220df9f163e78ad` |

### 2.3 Independence and ordering

The reviewer did not author or advise on I2 v0.2 or v0.3 and used no other
agent. Requirements were reconstructed from the authenticated v0.4 public
design, CONTROL decision, authority matrix, acceptance plan, vector-freeze
decision, I1 public runtime inputs, and v0.2 independent review before the
candidate README, report, tests, or implementation claims were relied on.

No F0 default-deny path, hidden material, handoff document, fixture, oracle,
protected/private data, provider/model output, E0 artifact, or S0 artifact was
opened, searched, hashed, or used.

## 3. Reconstructed public requirements used for judgment

The material requirements were:

1. The import event is exactly 31 ordered ASCII `name=value` lines, every line
   including the last ending in LF, with canonical unsigned decimal sequence,
   exact event hashing, and no duplicate, missing, reordered, unknown, or extra
   field.
2. Global predecessor/hash chaining and route-local predecessor-ID chaining are
   separate and mandatory at their declared caller-supplied boundaries.
3. Each route permits only `R/A/P/C`, the two early-terminal paths, and the
   eight post-pending completion classes. No event may follow consumed or
   terminal state.
4. Each supplied route identity may occur exactly once. A second identical or
   contradictory history is not a repeated valid binding.
5. Each route owns one result-media ID plus its `R/A/P/C` IDs in one five-ID
   supplied-set ownership domain. All result/result, result/event, and
   event/event cross-route collisions reject, including unused IDs burned by an
   early terminal and either group order.
6. Emitted event-ID uniqueness remains a separate supplied-set invariant.
7. The I1 binding is only the exact 22-role public identifier inventory with
   the root excluded from the 21 non-root event signers. It is not registry,
   key, or signature authority.
8. The frozen vector work is exact public evidence binding only. Complete
   admission/outcome grammar, frame selection, outcome truth, ledger/witness
   durability, project-lifetime uniqueness, provider/platform enforcement,
   cryptographic operations, protected work, E0, and S0 remain blocked.

## 4. V0.2 finding dispositions

### 4.1 `I2-V02-M01` — closed

**Code fact:** `validate_supplied_route_set` now builds a dedicated
`seen_route_identities` set and rejects an identity before registering the
second group. It separately validates every group as one complete permitted
route.

**Independent test result:** ten hostile pairs all rejected: an identical
accepted history; accepted versus early terminal in both orders; accepted
versus a different post-pending terminal in both orders; two different
post-pending terminals in both orders; terminal followed by an early history;
the reverse; and two early-terminal histories. Twelve additional traces with
an event appended after consumed or either early/post-pending terminal also
rejected.

**Independent inference:** the exact v0.2 repeated-route defect is closed at
the declared caller-supplied-set scope. This does not establish durable or
project-lifetime retry prevention.

### 4.2 `I2-V02-M02` — closed

**Code fact:** each route registers `result_media_id` and all four preallocated
event IDs in one `identifier_owners` map. The map operates on every ID even
when an early terminal did not emit it.

**Independent test result:** result/result, result/event, event/event, an
early-terminal unused event ID versus another result ID, and an early-terminal
unused event ID versus another event ID all rejected in forward and reversed
group order: ten hostile cases total. A disjoint two-route set passed.

**Independent inference:** the exact v0.2 five-ID ownership defect is closed at
the supplied-set scope. Project-lifetime ownership remains correctly blocked.

### 4.3 Separate emitted event-ID invariant — retained

**Code fact:** an `emitted_event_ids` set is distinct from both
`seen_route_identities` and `identifier_owners`; every validated emitted event
is checked and added separately. Independent AST review confirmed all three
structures and the emitted-ID membership/add operations. Event/event hostile
cases rejected in both group orders. The five-ID owner map will normally reject
such a collision first, so the separate check is intentionally defensive and
does not broaden the claimed scope.

## 5. Candidate verifier evidence

The shipped verifier was run exactly as required:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File s0-lab/i2/tools/verify-i2.ps1 -ExpectedManifestSha256 39386244bba397a1354204b7735508603b3071ef8884f60391beefabc6b21a24
```

It exited zero and reported 16 authenticated payload rows, the exact 12 public
sources, authenticated snapshot creation, Python `>=3.12,<4.0` under `-B -S
-P`, 37 tests run with zero failures, errors, skips, expected failures, or
unexpected successes, contract CLI pass, stdlib/snapshot-only import audit
pass, and original/snapshot/source final stability pass. It retained
`CLOSED_BOUNDARIES=BLOCKED_NOT_EXECUTED`.

This is candidate evidence, not the independent verdict. A separate hostile
run with a syntactically valid but incorrect manifest pin exited one before
candidate execution.

Line-by-line verifier review covered external pin and anchor comparison,
manifest text checks, path normalization, plain-file/reparse/device checks,
the exact I2 namespace, the hard-coded exact 12-source allowlist, authenticated
byte snapshotting, Python startup-hook exclusion, runtime environment controls,
test/CLI/import execution from the snapshot, pre/post byte stability,
environment restoration, and bounded temporary cleanup. The README and report
accurately disclose that already-executing verifier bootstrap is not made
trusted by its later self-hash check. No verifier-construction finding was
established.

## 6. Independent probes and broader audit

| Area | Independent result |
|---|---|
| exact codec | one exact 31-line round trip and final-LF SHA-256 passed; 12 BOM/CR/NUL/non-ASCII/order/cardinality/name/whitespace mutations rejected |
| canonical text decimals | seven malformed spellings rejected; a 6,000-digit text sequence and successor chain passed |
| declared integer sequence form | the numerically equivalent 5,001-digit integer raised raw `ValueError`; see `I2-V03-m01` |
| lifecycle coverage | all 39 route-class/single-variant combinations and all 30 complete paths passed |
| lifecycle hostiles | 141 tuple, sentinel, immutable-binding, and path mutations rejected, including 12 post-consumed/terminal traces |
| disagreement structural boundary | zero and nonzero frame-hash forms passed for all three classes; complete frame selection was not inferred |
| chain separation | one interleaved eight-event global chain and its two route-local chains passed; a wrong global predecessor rejected |
| v0.2 closures | ten M01 hostile pairs and ten M02 collision/order/early-terminal cases rejected |
| I1 binding | exact manifest and runtime hashes, 22 ordered roles, 21 non-root signers, and root exclusion passed |
| source and inventory binding | seven directly rehashed source bindings, three vector-decision-attested hashes, four exact distinct vector rows, and 14 preserved inventory fields matched |
| vector binding | exact package passed; row reordering and a forged handle rejected; no curve arithmetic ran |
| handles | wrong provenance and corrupted fields/raw/hash rejected; same-process introspection could reuse the private marker, confirming the disclosed non-security boundary |
| closed APIs | nine admission/outcome/classification/ledger/witness calls raised named `BLOCKED` errors |
| implementation imports | all eight implementation Python files used only `__future__`, `argparse`, `collections`, `dataclasses`, `hashlib`, `json`, `pathlib`, `re`, `types`, and `typing`; zero forbidden, third-party, dynamic-import, `eval`, or `exec` use |

**Candidate claim audit:** the contract, README, and verification report limit
their positive claims to byte codec, structural lifecycle and supplied-set
checks, public I1 identifier binding, and frozen vector evidence binding. They
keep complete outcome semantics, actual registry/key/signature authority,
ledger/witness durability, process/VM isolation, provider/model work,
protected material, E0, S0, the central system, and Project Brain blocked.
Those limits are accurate. The claimed absence of an undocumented decimal
ceiling is not fully accurate for the separately declared integer form, which
is the sole finding below.

## 7. Finding

### `I2-V03-m01` — minor — declared integer sequence input reintroduces the Python decimal digit ceiling and leaks a raw runtime exception

**Code fact:** `canonical.py` lines 61-68 declares normalization of either an
exact nonnegative integer or canonical decimal string, but the integer branch
uses `str(value)`. `lifecycle.py` lines 172-213 publicly types
`expected_sequence` and `expected_start_sequence` as `str | int` and catches
only candidate validation exceptions. The README claims canonical unsigned
decimal handling without an undocumented digit ceiling.

**Independent test result:** an event whose sequence was the canonical
5,001-digit text `1` followed by 5,000 zeroes parsed successfully and passed
`validate_event_global_link` when the expected sequence was the identical
string. Passing the numerically identical declared integer `10**5000` instead
raised Python's raw `ValueError` reporting the 4,300-digit integer-string
conversion limit.

**Impact inference:** this is fail-closed and does not admit an invalid event.
It also does not affect callers that retain canonical sequence text. It is
still a substantive public API and claim defect: one explicitly accepted input
form rejects a valid unbounded sequence at a runtime-specific ceiling and does
not return the stable I2 lifecycle error surface.

**Required repair:** either narrow both public global-sequence APIs to exact
canonical string input and deterministically reject every integer form with a
stable documented I2 error, or implement integer normalization without the
runtime integer-to-decimal digit ceiling. Update the contract/README/report if
the supported input surface changes, and add hostile tests above 4,300 digits
for both link and chain entry points. Do not treat raising or disabling a
process-global Python safety limit as independent evidence of an unbounded
codec.

## 8. Verdict limits and exact maximum next gate

The verdict is `REVISE-AND-REVIEW` with zero blocking, zero major, and one
minor finding. The v0.2 supplied-route and five-ID ownership repairs are
independently closed, but a zero-finding implementation review has not been
earned.

The exact maximum next gate is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.4 REVISION OPEN`

That gate must be separately opened by the user and may address only the
bounded public implementation finding. After a frozen repair, the maximum
following step would be a fresh, separately opened public-only v0.4 independent
review. Neither step opens CONTROL integration, `main` merge, an actual key,
registry, signature, ledger, witness, platform, provider/model session,
protected material, fixture/oracle, E0, or S0.

This review used authenticated public construction evidence only. It did not
validate a trust root, role isolation, operational safety, economic value,
production readiness, the central system, Project Brain integration, or
model-to-model transfer.
