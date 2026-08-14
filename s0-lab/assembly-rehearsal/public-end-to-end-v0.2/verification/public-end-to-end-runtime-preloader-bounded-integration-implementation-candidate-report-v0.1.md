# Public end-to-end runtime/preloader bounded integration implementation candidate report v0.1

Status: bounded PUBLIC offline implementation candidate; no live or rehearsal authority

## Scope and authenticated inputs

This candidate implements only the v0.2 offline conformance lane beneath
`s0-lab/assembly-rehearsal/public-end-to-end-v0.2/`. It authenticates and
depends on the exact assembly implementation manifest (32 targets), runtime/
preloader v0.3 implementation manifest (11 targets), runtime/preloader v0.4
design manifest (6 targets), and integration design v0.1/v0.2 manifests.

Their manifest SHA-256 values are respectively:

- `0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623`;
- `5022d517864cae19520a1e3e34a683965609abf0ef29e167b30a11bade4a32c2`;
- `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`;
- `f55352771432404f4c2e9337665184e18afde076b8b3efe7a455ee6694d60e6b`; and
- `1349c6c4c97d24256f98216eb86a353451891419044b61d22c5c14d7eded5e7c`.

No F0, personal, real, secret, provider, model, network, native, or live input
is used.

## Implementation result

`prepare_offline_integration_diagnostic` first authenticates the RPNP v0.3
implementation and integration v0.1/v0.2 manifests plus their exact 11/5/6
target closures in the same call. It then passes original authenticated bytes,
byte mappings, the PUBLIC in-memory synthetic static bundle, and exact
`OfflinePreloaderInputs` to the sole admitted
`prepare_assembly_runtime_launch` bridge. It does not call a standalone
validator or source-audit function and exposes no dependency injection.

The success trace is exactly `OFFLINE-NEW`,
`OFFLINE-PUBLIC-ARTIFACTS-AUTHENTICATED`, `OFFLINE-PLAN-VALIDATED`, and
`OFFLINE-DIAGNOSTIC-COMPLETE`. Any bridge rejection produces only
`OFFLINE-NEW`, `OFFLINE-REJECTED`. Both results are canonical byte-bound
diagnostics with `candidate_only=true`, `native_api_reachable=false`, and
`rehearsal_pass=false`.

## Verification result

The focused suite contains five passing tests: exact happy-path bridge use,
authenticated-byte mutation rejection, nonoffline-result rejection, and
changed/missing/extra closure rejection before bridge use, plus source-level
absence of ambient/native/process/network execution surfaces. The verifier
requires an explicit lowercase SHA-256 pin for its own implementation
manifest, authenticates that manifest and its exact three rows, and then
authenticates all 32/11/6/5/6 targets. Only after authentication does it copy
the exact bytes and narrowly pinned predecessor schemas/report records into a
temporary snapshot. A separate isolated Python unittest process imports and
executes exclusively from that snapshot. The verifier then reauthenticates all
original source inputs and requires byte-for-byte equality with its pre-run
snapshot as a deterministic swap sentinel. Candidate
execution makes zero native, process, network, or provider calls; verifier
orchestration uses the explicitly reported Python unittest process.

This is implementation evidence for a later independent implementation and
security rereview only. It is not a runtime materialization, native preloader,
Windows platform probe, live assembly decision, public rehearsal PASS, S0, or
production evidence.
