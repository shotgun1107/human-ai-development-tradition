# S0 v0.14 public build/runtime materialization candidate v0.7 status

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.7 CPYTHON EMBEDDABLE RUNTIME AND JSONSCHEMA WHEEL CLOSURE EXTERNAL PIN ACTIVATION AND ACTUAL MATERIALIZATION`
- `branch`: `codex/build-runtime-materialization-v0.7`
- `base_commit`: `f4be29ff470946741ed4b39bbb90c1eef14537ed`
- `base_tree`: `40f0ec165af60037fd38363067e0479ef8b395b4`
- `candidate_status`: `PASS — ACCEPT AS THE AUTHENTICATED V0.7 RUNTIME-MATERIALIZATION CANDIDATE UNDER python-os-rename-windows-no-replace-v0.7 ONLY.`
- `independent_rereview_status`: `PASS`
- `independent_rereview_severity`: `0 BLOCKING / 0 MAJOR / 0 MINOR`
- `BRM-V07-IR-001`: `CLOSED-UNDER-FORMALLY-SUPERSEDED-V0.7-POLICY-ONLY`
- `retroactive_class22_validation`: false
- `final_test_status`: `PASS`
- `final_live_exit_code`: 0
- `runtime_status`: `COMPLETE-RUNTIME-MATERIALIZATION-ONLY`
- `publication_policy`: `python-os-rename-windows-no-replace-v0.7`
- `publication_primitive`: `python.os.rename`
- `publication.py_present`: false
- `F0_content_access`: none
- `commit_or_push_authorized`: false

## Authenticated candidate

All seven current implementation files match their supplied size and SHA-256
identities. `authority.py` has SHA-256
`985d64c7e9e65aaff97518729a32cde27062239b0a0de276c02871c88b3f12eb`,
and `materialize.py` has SHA-256
`17c2cf9032998fe9653a5f6b8535eb76e4f15693e8b834ca60d10755bfa430f7`.
The other five implementation files retain their prior authenticated hashes.
There is no `publication.py` implementation file.

The deterministic implementation inventory contains seven rows and has
SHA-256
`29bfb07328695668d5a78b4af1ddd4b8a5b4a4acb5e30b6bc61df2a0dbd4d333`.
The current TEST/verification inventory contains ten Python source rows and has
SHA-256
`a5a3c1b0f305492743b9715c26953f79849059f40ad177f1e129c40b0564eda3`.

The external authority manifest remains exactly 37,688 bytes with SHA-256
`b7896b00ba187aa431ff8f81840259f91f58f4dff7c33f5589d9ea1b33b6f084`.
It pins one prebuilt CPython embeddable ZIP and six prebuilt wheels. The r4
cache matched all seven expected sizes and hashes.

## Preserved decision and failure history

The first live run and r1 used `os.rename` successfully, but that did not
satisfy the old claimed class-22 policy. The prior independent review returned:

> REVISE-AND-REVIEW — NOT ACCEPTABLE AS THE AUTHENTICATED V0.7 RUNTIME-MATERIALIZATION CANDIDATE.

Its exact finding was `BRM-V07-IR-001`. Before r1, the initial and targeted
evidence recorded 22 PASS, three candidate FAIL, and one SKIP. The three
candidate defects were authority minting, Windows low-word reparse ZIP
acceptance, and the staging-junction pre-write gap. The initial raw artifacts
remain recorded in the candidate manifest with their sizes and hashes.

The r1 suite recorded 26 run, 25 PASS, and one SKIP after those three defects
were corrected. Its 41,027-byte raw result has SHA-256
`c6341392bcfbca1f6e09a3dae7ac0cb2c68b1782ac28346826a2aaaf57b9d431`.
The prior review nevertheless rejected candidate acceptance because the
claimed publication primitive had not been exercised.

The later exact class-22 correction failed closed with WinError 87. A
52-versus-56 structure-size hypothesis was tested and falsified. The failure
was not converted into success evidence.

The user then approved a standard-library publication-policy revision. CONTROL
superseded the historical class-22 requirement for v0.7 only with
`python-os-rename-windows-no-replace-v0.7`. The policy is supported by the
official [Python 3.12 `os.rename` documentation](https://docs.python.org/3.12/library/os.html#os.rename),
which specifies that on Windows an existing destination always raises
`FileExistsError`. The candidate uses no custom Windows rename API.

## Final r4 TEST/VERIFICATION

The exact command was:

```text
python -B s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/verification/run_standard_publication_r4.py
```

TEST ran it exactly once. The suite took 8,983 ms and recorded 29 run, 28 PASS,
zero FAIL, zero ERROR, and one SKIP. The skipped parent-symlink case could not
synthesize the link because Windows returned WinError 1314.

The 72,170-byte raw r4 result has SHA-256
`6377f74967564d4e877e2359fd5858e2b0c692fff6535fd4f1f442cadfa8529d`.
Its canonical sidecar targets that exact hash and has file SHA-256
`d94e79a394066bfa66e3631daca6b01f64dfc5b312b299e5cc7d79b79adc55d5`.

The r4 suite records:

- one real same-volume `os.rename` success and one primitive invocation;
- no retry and no fallback;
- an existing destination raising `FileExistsError` while preserving both
  source staging and destination;
- an attacker destination introduced immediately before rename being
  preserved, with no overwrite and no `COMPLETE` result;
- prepublication, payload, runtime, and status evidence-chain agreement;
- postpublication identity and 174-row readback agreement; and
- hostile working-directory, `PYTHONPATH`, `PYTHONHOME`, user-site, payload,
  and import-closure checks within the tested boundary.

## Final runtime evidence

The live path exited 0 in 1,546 ms. Its out-of-repository final root is
`C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\runtime-final-r4`.
The payload contains 174 files and 24,138,847 bytes. Read-only documentation
authentication recomputed every row and found zero size or SHA-256 mismatch.

- payload manifest SHA-256:
  `8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798`;
- prepublication record SHA-256:
  `0281893dce01d1aa54a1ad16cd621786615340844fcec35940095768e7dda9ca`;
- runtime record SHA-256:
  `5d6b61194b5a7f0e53aeb78ac0bdee40f6edea294adecb0f8a7462751f6e6a84`;
- status record SHA-256:
  `c8878e9df9d8c5979517efa3a9495b8e65c640b6f2c195fff029def6c262bbc6`.

## Fresh independent rereview

The fresh independent reviewer authenticated the 27-file candidate before
this preservation update: implementation 7/7, TEST/verification 10/10, the
external manifest and seven pins, every r4 raw/evidence pair, all 174 payload
files totaling 24,138,847 bytes, independent archive reconstruction, and all
imported origins matched exactly.

The exact verdict is:

> PASS — ACCEPT AS THE AUTHENTICATED V0.7 RUNTIME-MATERIALIZATION CANDIDATE UNDER python-os-rename-windows-no-replace-v0.7 ONLY.

Severity is 0 BLOCKING, 0 MAJOR, and 0 MINOR. `BRM-V07-IR-001` is closed only
under the formally superseded v0.7 policy; this is not retroactive validation
of the old class-22 policy. The verdict was returned to CONTROL only, so this
status report does not claim or invent a repository review artifact or path.

## Boundaries

The allowed claim is limited to the tested Windows 11 host, Python 3.12
runtime, filesystem context, exact pins, and observed operations. It does not
generalize the no-overwrite result to all Windows versions or filesystems.

The evidence does not establish supplier, TLS, or network-producer assurance;
resistance to a same-user or local-administrator attacker with trusted-parent
write or rebinding authority; complete OS DLL or runtime-loader closure; or
execution of the parent-symlink variant. It does not establish a completed
rehearsal or S0, central-system completion, Project Brain integration,
operational safety, economic value, or model-to-model transfer.
