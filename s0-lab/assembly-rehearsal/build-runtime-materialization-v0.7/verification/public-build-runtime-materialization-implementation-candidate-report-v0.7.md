# S0 v0.14 public build/runtime materialization implementation candidate report v0.7

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.7 CPYTHON EMBEDDABLE RUNTIME AND JSONSCHEMA WHEEL CLOSURE EXTERNAL PIN ACTIVATION AND ACTUAL MATERIALIZATION`
- `branch`: `codex/build-runtime-materialization-v0.7`
- `base_commit`: `f4be29ff470946741ed4b39bbb90c1eef14537ed`
- `base_tree`: `40f0ec165af60037fd38363067e0479ef8b395b4`
- `runtime_materialization_manifest_sha256`: `43277a32068fef853b004d90938cf00fe1c77cccd49b6f0c6a65953bc1489f0b`
- `candidate_status`: `PASS — ACCEPT AS THE AUTHENTICATED V0.7 RUNTIME-MATERIALIZATION CANDIDATE UNDER python-os-rename-windows-no-replace-v0.7 ONLY.`
- `independent_rereview_status`: `PASS`
- `independent_rereview_severity`: `0 BLOCKING / 0 MAJOR / 0 MINOR`
- `BRM-V07-IR-001`: `CLOSED-UNDER-FORMALLY-SUPERSEDED-V0.7-POLICY-ONLY`
- `retroactive_class22_validation`: false
- `F0_content_access`: none

## 1. Current outcome

The revised v0.7 candidate activates the exact frozen external authority and
materializes the CPython 3.12.10 AMD64 embeddable distribution with the exact
six-wheel jsonschema dependency closure. It uses prebuilt artifacts, does not
compile CPython, does not use Build Tools, and does not contain a separate
`publication.py` module.

After a user-approved v0.7-only policy revision, the active publication policy
is `python-os-rename-windows-no-replace-v0.7`. It uses one
`python.os.rename` call with no retry or fallback and no custom Windows rename
API. Final r4 TEST evidence records a real successful materialization plus
existing-destination and intervening-destination fail-closed behavior.

The allowed claim is bounded to the tested Windows 11 host, Python 3.12
runtime, filesystem context, exact pins, and recorded operations. This report
does not approve the candidate.

## 2. Frozen current identity

The seven implementation files match the frozen current identities.
`authority.py` is 20,467 bytes with SHA-256
`985d64c7e9e65aaff97518729a32cde27062239b0a0de276c02871c88b3f12eb`.
`materialize.py` is 37,788 bytes with SHA-256
`17c2cf9032998fe9653a5f6b8535eb76e4f15693e8b834ca60d10755bfa430f7`.
The other five implementation files retain their prior authenticated hashes.

The implementation inventory has seven rows and SHA-256
`29bfb07328695668d5a78b4af1ddd4b8a5b4a4acb5e30b6bc61df2a0dbd4d333`.
The TEST/verification inventory covers all ten current Python test and runner
sources and has SHA-256
`a5a3c1b0f305492743b9715c26953f79849059f40ad177f1e129c40b0564eda3`.
The final `test_v07.py` SHA-256 is
`47dff890c395020a1a6044fae9a019ff77e97168ab0434788984ddf16cfe72eb`,
and the r4 runner SHA-256 is
`52f0836c7a284699f5da76be5e540f83c62ff9ddc029b630b0374362fc4f83d2`.

The authority input remains the 37,688-byte external evidence manifest with
SHA-256
`b7896b00ba187aa431ff8f81840259f91f58f4dff7c33f5589d9ea1b33b6f084`.
Its activated closure is one exact prebuilt CPython embeddable ZIP and six
exact wheels.

## 3. Preserved failure and review history

The initial live path succeeded, but the initial and targeted adversarial
evidence was not an acceptance result: 22 PASS, three candidate FAIL, and one
SKIP. The three isolated defects were caller-mintable authority, Windows
low-word reparse ZIP acceptance, and the staging-junction pre-write gap.

The initial raw artifacts remain referenced in the candidate manifest:

- `verification-result.json`: 42,165 bytes, SHA-256
  `bae46e164fa54cd3c7eb60d4ee091e702229b660f07f3ac82f2e3dd2705259f4`;
- `targeted-verification-result.json`: 38,500 bytes, SHA-256
  `6e4826be082435ae56b1adaeec670f8124a4354e7ef915318ca5b3266060196a`.

After correcting those three defects, r1 recorded 26 run, 25 PASS, and one
SKIP. Its raw result is 41,027 bytes with SHA-256
`c6341392bcfbca1f6e09a3dae7ac0cb2c68b1782ac28346826a2aaaf57b9d431`.
However, the old independent review found `BRM-V07-IR-001`: the candidate
claimed the old class-22 policy, but that primitive was not executed. The exact
verdict was:

> REVISE-AND-REVIEW — NOT ACCEPTABLE AS THE AUTHENTICATED V0.7 RUNTIME-MATERIALIZATION CANDIDATE.

The subsequent exact class-22 correction failed closed with WinError 87. The
52-versus-56 structure-size hypothesis was tested and falsified. Neither the
failed class-22 attempt nor its rejected hypothesis is presented as success.

## 4. Approved standard-policy revision

The user authorized a standard-library publication revision, and CONTROL
superseded the historical class-22 policy for v0.7 only. The new policy is
`python-os-rename-windows-no-replace-v0.7`, with policy SHA-256
`7ca87e4b38444ddef0a9423312dbe9b5b11a664477e342300eb8e069a9741ced`.

The authority source is the official
[Python 3.12 `os.rename` documentation](https://docs.python.org/3.12/library/os.html#os.rename),
which states that on Windows an existing destination always raises
`FileExistsError`. The candidate invokes `python.os.rename` once, on the same
volume, after a destination-absence recheck. Retry and fallback are forbidden.
This is a bounded Python/Windows standard-policy claim, not a claim about every
Windows version, filesystem, mount, or adversary.

## 5. Final r4 TEST evidence

TEST/VERIFICATION ran exactly once:

```text
python -B s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/verification/run_standard_publication_r4.py
```

The suite took 8,983 ms and recorded 29 run, 28 PASS, zero FAIL, zero ERROR,
and one SKIP. The parent-symlink case was not executed because Windows denied
link synthesis with WinError 1314.

The suite records the following bounded publication results:

1. A real same-volume `os.rename` succeeded exactly once. The final identity,
   payload inventory, and record chain were verified after reopening.
2. With an existing destination, real `os.rename` raised `FileExistsError`
   and preserved both staging and destination.
3. When an attacker destination was introduced immediately before the rename,
   it was preserved. The candidate did not overwrite, retry, fall back, or
   emit a `COMPLETE` result.
4. Prepublication, payload, runtime, and status hashes remained linked through
   the result records.
5. Hostile working-directory, `PYTHONPATH`, `PYTHONHOME`, user-site, payload,
   and import-closure checks passed within the tested boundary.

The exact 72,170-byte raw r4 record has SHA-256
`6377f74967564d4e877e2359fd5858e2b0c692fff6535fd4f1f442cadfa8529d`.
Its canonical sidecar targets that value and has SHA-256
`d94e79a394066bfa66e3631daca6b01f64dfc5b312b299e5cc7d79b79adc55d5`.

The separate exact no-replace rerun returned exit 2 with `PathSafetyError` and
empty standard output.

## 6. Materialized runtime evidence

The final live path exited 0 in 1,546 ms after authenticating all seven cached
artifacts. The out-of-repository root is
`C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\runtime-final-r4`.

The physical payload contains 174 rows totaling 24,138,847 bytes. Read-only
documentation authentication recomputed every row and found zero size or
SHA-256 mismatch. The reopened publication record reports the same 174 rows
and byte total.

The evidence identities are:

- payload manifest:
  `8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798`;
- prepublication record:
  `0281893dce01d1aa54a1ad16cd621786615340844fcec35940095768e7dda9ca`;
- runtime record:
  `5d6b61194b5a7f0e53aeb78ac0bdee40f6edea294adecb0f8a7462751f6e6a84`;
- status record:
  `c8878e9df9d8c5979517efa3a9495b8e65c640b6f2c195fff029def6c262bbc6`.

## 7. Required nonclaims

Exact URLs, sizes, and SHA-256 pins do not establish supplier, TLS, or
network-producer assurance. The evidence does not establish resistance to a
same-user or local-administrator attacker who can write or rebind the trusted
parent. It does not generalize no-overwrite behavior to all Windows versions
or filesystems, and it does not establish complete OS DLL or runtime-loader
closure. The parent-symlink variant remains unexecuted because of WinError
1314.

No rehearsal or S0 was completed. The candidate does not establish a central
system, Project Brain integration, operational safety, economic value, or
model-to-model transfer.

## 8. Fresh independent rereview result

The fresh independent reviewer authenticated the 27-file candidate before
this documentation preservation update: implementation 7/7,
TEST/verification 10/10, the external manifest and seven pins, all r4 raw and
evidence pairs, all 174 payload files totaling 24,138,847 bytes, independent
archive reconstruction, and all imported origins were exact.

The exact verdict is:

> PASS — ACCEPT AS THE AUTHENTICATED V0.7 RUNTIME-MATERIALIZATION CANDIDATE UNDER python-os-rename-windows-no-replace-v0.7 ONLY.

Severity is 0 BLOCKING, 0 MAJOR, and 0 MINOR. `BRM-V07-IR-001` is closed under
the formally superseded v0.7 policy only. This result does not retroactively
validate the historical class-22 policy. The verdict was returned to CONTROL
only; no repository review artifact or path is claimed or invented.

## 9. Maximum claim

Maximum claim: the frozen revised PUBLIC v0.7 candidate and authenticated r4
TEST evidence materialized the exact prebuilt CPython and six-wheel runtime on
the tested host, exercised one successful standard `os.rename` publication,
and demonstrated fail-closed preservation for the tested existing and
immediately-intervening destination cases with no retry or fallback. Fresh
independent review accepts this as the authenticated v0.7
runtime-materialization candidate under
`python-os-rename-windows-no-replace-v0.7` only. That acceptance does not
broaden any stated nonclaim or validate the superseded class-22 policy.
