# I1 public runtime structural verification report

## Result

- Candidate test suite: **PASS** (32 tests run; 31 passed and one direct
  symlink-creation test skipped on this Windows host).
- Authenticated public spec namespace: **PASS** (7/7 files).
- Draft 2020-12 schema-definition checks: **PASS** (6/6 schemas).
- Role/store/edge/status topology audit: **PASS** (0 issues).
- Runtime source boundary audit: **PASS** (0 forbidden provider/network
  imports).
- S0, empirical, operational, or central-system result: **NOT CLAIMED**.

This report records public construction tests only. It is not an S0 run,
executor result, model result, score, simulation, cryptographic verification,
or store/ACL/atomicity proof.

## Authenticated facts

- Public spec manifest SHA-256:
  `4469834a5aa480575cd9384a14881b83e596646686ce04f35fcb7bd9502faed2`.
- Frozen counts: 32 aggregated role rows, 40 row positions, eight paired rows,
  27 stores, 64 edges, 22 signer role IDs, 14 status edges, 15 states, 17
  receipts, and 15 E51 pairs.
- Frozen v0.14 source digests are embedded in the authenticated topology and
  are independently compared with implementation constants for the authorized
  protocol, contract, plan, review response, independent review, and CONTROL
  integration decision hashes.
- The runtime is provider-neutral and contains no provider or network
  implementation.

## Construction tests

The tests cover:

- same-bytes authentication/consumption after a path's bytes change;
- absolute path, traversal, substituted path, manifest-anchor, extra-file,
  symbolic-link, and reparse-attribute attacks;
- broader topology cross-index, declared-count, status-state, and receipt-count
  failures;
- omission-as-denial and position-specific cross-role store access;
- signed-envelope field order, length, record hash, role/key assignment,
  algorithm, trailing bytes, and injected verifier rejection;
- E25 two-producer receipt order/count, receipt identity/result, ROOT anchor,
  bundle commitment, previous status hash, prefix mask, sequence, and monotonic
  time mutations, plus one complete ROOT-through-E56 15-pair chain;
- exactly one transport invocation, zero retry/tool/state policy, 8,192-byte
  pre-parse enforcement, first-response selection, mixed-response rejection,
  strict UTF-8/BOM/duplicate-key/surrogate/NFC/non-finite-number checks, and
  manifest-provenance enforcement for the authenticated request; and
- no output on runner failure plus exclusive, no-overwrite neutral result
  emission.

The direct filesystem symlink test is skipped only for a permission/Windows
symlink-privilege error. A privilege-free reparse-attribute sentinel and a
mocked authenticated-path rejection exercise both reparse detection and its
actual input rejection path. This does not prove resistance to every privileged
filesystem race.

## Verification commands executed

Run from the repository root with `s0-lab/i1/implementation` on `PYTHONPATH`:

```powershell
python -c "from pathlib import Path; from s0_i1.topology import load_public_runtime_spec, audit_topology; s=load_public_runtime_spec(Path('.')); print(s['counts']); print(len(audit_topology(s)))"
python -m unittest discover -s s0-lab/i1/tests -v
python -m unittest discover -s s0-lab/i1/tests -v
python -m s0_i1.cli verify
powershell -NoProfile -ExecutionPolicy Bypass -File s0-lab/i1/tools/verify-i1.ps1
```

The initial development run found one ordinary CLI stdout-capture defect. A
later read-only QA pass found additional structural-test gaps and three parser
defects; these were corrected before freeze. The current unit run produces 32
tests, 31 passes, one host-limited skip, and exit 0. The final standalone CLI
returned a machine-readable `pass`; the PowerShell verifier repeated the pinned
runtime/dependency checks, all tests, the CLI audit, the separately anchored
26-row payload manifest, and the forced exact file-set audit, then exited 0.

## Closed proposals and limitations

- Actual Ed25519 verification is injected and was tested with a noncryptographic
  acceptance sentinel; no key or signature was generated.
- Root, registry, integration-manifest, store, durability, ACL, and atomic-write
  artifacts remain unimplemented.
- Effective answer semantics and its exact member order, canonical serializer,
  field/answer/response sublimits, direct-operation rule, and frozen question
  order are not implemented from unallowlisted predecessor bytes.
- No concrete runner package/common-resource schema, provider allowlist,
  provider implementation, run-log grammar, model call, executor, bank,
  question, answer, fixture, oracle, scoring, simulation, sealed path, E0 path,
  real-data path, or Project Brain integration exists here.
- Python 3.12 compatibility is by supported syntax and dependency constraint;
  the current command host reports Python 3.14.6. A separate Python 3.12 host
  was not available in this implementation turn.
