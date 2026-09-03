# S0 public build/runtime materialization implementation candidate v0.7

This directory contains the bounded PUBLIC v0.7 candidate that activates the
frozen external CPython and wheel pins and materializes a usable runtime from
prebuilt artifacts. It does not compile CPython, use Visual Studio Build
Tools, or contain a separate `publication.py` module.

The authenticated input is the 37,688-byte external authority evidence
manifest at
`s0-lab/assembly-rehearsal/build-runtime-materialization-external-artifact-authority-acquisition-v0.1/evidence-manifest.json`,
SHA-256
`b7896b00ba187aa431ff8f81840259f91f58f4dff7c33f5589d9ea1b33b6f084`.
The activated closure is the CPython 3.12.10 AMD64 embeddable ZIP plus six
prebuilt wheels: jsonschema, attrs, jsonschema-specifications, referencing,
rpds-py, and typing-extensions.

## Publication-policy revision

The initial and r1 implementations materialized with `os.rename`, but the old
independent review returned exactly:

> REVISE-AND-REVIEW — NOT ACCEPTABLE AS THE AUTHENTICATED V0.7 RUNTIME-MATERIALIZATION CANDIDATE.

Finding `BRM-V07-IR-001` identified that the then-claimed class-22 policy was
not the operation actually executed. The attempted exact class-22 correction
subsequently failed closed with WinError 87, and the proposed 52-versus-56
structure-size explanation was falsified.

After explicit user approval, CONTROL superseded the historical class-22
policy for v0.7 only with
`python-os-rename-windows-no-replace-v0.7`. The standard policy uses exactly
one `python.os.rename` call and permits no retry or fallback. Python 3.12's
official [`os.rename` documentation](https://docs.python.org/3.12/library/os.html#os.rename)
states that on Windows an existing destination always raises
`FileExistsError`. This candidate does not introduce a custom Windows rename
API.

## Final r4 evidence

TEST/VERIFICATION ran this command exactly once:

```text
python -B s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/verification/run_standard_publication_r4.py
```

The suite completed in 8,983 ms with 29 run, 28 PASS, zero FAIL, zero ERROR,
and one SKIP. The skip records WinError 1314 while attempting to synthesize a
parent-directory symlink; it is not counted as a pass.

The r4 evidence records one real, same-volume `os.rename` materialization
success. It separately records that an already existing destination and a
destination introduced immediately before the rename both raise
`FileExistsError`, preserve the destination, and produce no overwrite,
fallback, retry, or `COMPLETE` result. Prepublication, payload, runtime, and
status records form the checked evidence chain. The hostile working-directory,
`PYTHONPATH`, `PYTHONHOME`, user-site, payload, and import-closure checks pass
within the tested boundary.

The live run exited 0 in 1,546 ms after authenticating all seven cached
artifacts. Its out-of-repository final root is
`C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\runtime-final-r4`.
The payload contains 174 files totaling 24,138,847 bytes. Evidence hashes are:

- payload manifest:
  `8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798`;
- prepublication record:
  `0281893dce01d1aa54a1ad16cd621786615340844fcec35940095768e7dda9ca`;
- runtime record:
  `5d6b61194b5a7f0e53aeb78ac0bdee40f6edea294adecb0f8a7462751f6e6a84`;
- status record:
  `c8878e9df9d8c5979517efa3a9495b8e65c640b6f2c195fff029def6c262bbc6`.

The canonical candidate manifest is `runtime-materialization-manifest.json`,
SHA-256
`43277a32068fef853b004d90938cf00fe1c77cccd49b6f0c6a65953bc1489f0b`.

## Independent rereview result

The fresh independent review returned the exact verdict:

> PASS — ACCEPT AS THE AUTHENTICATED V0.7 RUNTIME-MATERIALIZATION CANDIDATE UNDER python-os-rename-windows-no-replace-v0.7 ONLY.

Severity counts are 0 BLOCKING, 0 MAJOR, and 0 MINOR. `BRM-V07-IR-001` is
closed only under the formally superseded v0.7 publication policy. The result
does not retroactively validate the historical class-22 policy. The reviewer
returned the verdict to CONTROL only; no repository review artifact or path is
claimed here.

## Maximum claim

The candidate and r4 TEST evidence show the bounded standard-policy behavior
on the tested Windows 11 host, Python 3.12 runtime, filesystem context, and
exact external pins. Fresh independent review accepts it as the authenticated
v0.7 runtime-materialization candidate under
`python-os-rename-windows-no-replace-v0.7` only.

The evidence does not establish supplier, TLS, or network-producer assurance;
resistance to a same-user or local-administrator trusted-parent writer or
rebinding attacker; no-overwrite behavior across all Windows versions and
filesystems; complete OS DLL or runtime-loader closure; or execution of the
skipped parent-symlink variant. It does not establish a completed rehearsal or
S0, central-system completion, Project Brain integration, operational safety,
economic value, or model-to-model transfer.
