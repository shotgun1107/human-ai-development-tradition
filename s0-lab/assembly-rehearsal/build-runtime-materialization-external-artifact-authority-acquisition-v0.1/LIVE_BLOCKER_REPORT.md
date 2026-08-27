# Live Build Tools authority blocker

## Bounded conclusion

**PRIMARY CURRENT BLOCKER:** V0.1 has not authenticated the complete transitive authority closure of the historical v0.4 Authenticode path. The public Build Tools proposal entrypoint and public issuance checker therefore unconditionally raise `BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED` before metadata validation, acquisition-record construction, any v0.4 call, or native trust. `BUILD-TOOLS-AUTHENTICODE-LIVE-RESULT-PENDING` remains a separate permanent V0.1 blocker.

**PRESERVED FRESH INDEPENDENT REREVIEW ACCEPTANCE:** state `INDEPENDENT-REREVIEW-PASS-ACCEPT-CORRECTION-CLOSURE`; exact human verdict `PASS — ACCEPT CORRECTION CLOSURE`; `BLOCKING 0 / MAJOR 0 / MINOR 0`; no new equal-or-higher issue. The reviewer accepted closure of the fail-closed correction and closed all four named findings. That acceptance is correction closure only and does not remove either blocker, resolve the separate inherited provider-owned `hAdditionalStore` diagnostic, or grant a public proposal, CONTROL promotion, active Build Tools/final/process authority, or integration readiness.

**BLOCKED:** no public Build Tools proposal can be issued, no private TEST proposal can satisfy the public checker or candidate assembly, final Build Tools authority is false, CONTROL promotion is false, and process or executed-code authority is absent.

**SEPARATE INHERITED DIAGNOSTIC:** historical v0.4 also omitted the WinVerifyTrust provider-owned `hAdditionalStore` from its separate chain reconstruction. That older diagnosis remains relevant to future v0.4 remediation, but it does not close or replace the primary current transitive-closure blocker and is not an artifact signature failure.

## Exact reproduction boundary

- **Gate/candidate:** `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL ARTIFACT AUTHORITY ACQUISITION CPYTHON BUILD TOOLS AND JSONSCHEMA AUTHORITATIVE PIN SIZE SOURCE AND TRANSITIVE CLOSURE IMPLEMENTATION V0.1 OPEN`.
- **Result-preservation gate:** `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL ARTIFACT AUTHORITY ACQUISITION CPYTHON BUILD TOOLS AND JSONSCHEMA AUTHORITATIVE PIN SIZE SOURCE AND TRANSITIVE CLOSURE IMPLEMENTATION V0.1 INDEPENDENT CODE AND SECURITY REREVIEW RESULT PRESERVATION OPEN`.
- **Repository identity:** branch `codex/s0-external-artifact-authority-acquisition-v01`; commit `b469b71f3e1dd23b39b9992532785c9d6a57363d`; tree `4ae99d86fa3ae430074d9ff99d2dda1c7543fd3e`.
- **Live harness:** `s0-lab/assembly-rehearsal/build-runtime-materialization-external-artifact-authority-acquisition-v0.1/verification/acquire_live_authority.py`, SHA-256 `02bd439e80ee931cd656caf6cebd4935b9237a1c857837abfc3fb8caaf4ecdd4`, size `47264`.
- **Candidate verifier:** `s0-lab/assembly-rehearsal/build-runtime-materialization-external-artifact-authority-acquisition-v0.1/verification/verify_candidate.py`, SHA-256 `525f45d8f0b95a93d7a37c74c48f053d62c0dbc621bfb8302db49616992e7f56`, size `20667`.
- **v0.4 outer implementation manifest:** SHA-256 `ba66b457e169106bc830d68e10d72bcfe0fe3248e83515ee330d94457b34e77c`; its exact nine implementation hashes remain preserved in `evidence-manifest.json`.
- **Retained evidence root:** `C:\Users\SSAFY\AppData\Local\Temp\s0-v01-live-504690da91a42646967203c8`, classified `NONPUBLIC-OUT-OF-REPO`. Its downloaded contents must not be committed.
- **Historical pre-dual-inventory evidence:** `evidence/live-authority-evidence.json`, size `33486`, SHA-256 `ba579e22402900bee2788e4c607486c0e36a02dfa0910254b867ac92aa62c4ee`; sidecar size `95`, SHA-256 `69fc2b831859ac26085b2281f8a2384bdef958fc02e589050e5b99134f6b758e`.
- **Current retained-root command:** `python -I -B 's0-lab/assembly-rehearsal/build-runtime-materialization-external-artifact-authority-acquisition-v0.1/verification/verify_candidate.py' --retained-root 'C:\Users\SSAFY\AppData\Local\Temp\s0-v01-live-504690da91a42646967203c8'`.

**FACT:** the historical evidence stopped earlier at `wheel_metadata_requires_dist_inventory_mismatch`, before any Authenticode phase. Current TEST/VERIFICATION reauthenticated all 18 retained files and passed CPython, Microsoft, six PyPI, six wheel, dual-inventory, and closure validation read-only. It then proved public proposal/checker blocker precedence with v0.4/native invocation count `0`, final authority false, and all five acquired-byte actions false. Historical live evidence and this current read-only retained-root validation are distinct evidence events.

**FACT — post-rereview whitespace hash cascade:** `implementation/s0_external_artifact_authority_acquisition/errors.py` changed only by removal of one redundant terminal LF, from size `182` and SHA-256 `bdde03f9cd3a8ace87355f6334462ed822e14df1450f0f2fcd3c30f10faef055` to size `181` and SHA-256 `3792fd5467e39b18dcc58bb063e6075c422c8f6b2d7d061c1c537cd6ea6c1221`. Required exact-pin updates produced current `tests/test_authority_acquisition.py` size `6260`, SHA-256 `edfaff91f13d1fc90fa2f0cd4bfcc64cd2a827b08e7e6e6cb08a8c871ef571c6`; live harness size `47264`, SHA-256 `02bd439e80ee931cd656caf6cebd4935b9237a1c857837abfc3fb8caaf4ecdd4`; and verifier size `20667`, SHA-256 `525f45d8f0b95a93d7a37c74c48f053d62c0dbc621bfb8302db49616992e7f56`. The other 12 non-documentation candidate files remained unchanged. Supplied TEST/VERIFICATION reruns remained 44/44 PASS, live-harness self-test PASS with network/native false and unchanged evidence SHA-256, verifier 32/44 PASS with stable bytes and sentinels, and retained-root validation 18/18 with final authority false. This was not a design change, finding, verdict change, or new independent review.

## Current public fail-closed effect

The corrected public surface behaves as follows:

- `verify_buildtools_and_propose_pin(...)` immediately raises `BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED`;
- `_require_issued_buildtools_proposal(...)` raises the same blocker for every value;
- the blocker precedes every tested reachable mutable v0.4 global, metadata call, record builder, verifier, and native trust path;
- the isolated private TEST adapter has a hard proposal cap of `1` and cannot satisfy the public checker;
- candidate assembly rejects any supplied proposal with the same permanent blocker;
- the no-proposal candidate state preserves both `BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED` and `BUILD-TOOLS-AUTHENTICODE-LIVE-RESULT-PENDING` and keeps final authority false.

**TEST RESULT:** public blocker and checker precedence, mutation/rebinding cases, private-seam isolation, proposal cap/drop recovery, candidate rejection, and cleanup recovery passed. The live-harness self-test reported native trust not invoked and evidence SHA-256 `87d674cea114938393e7bdd9dbccc8d991d11fdeed74325d61c8d84cb13cf5cf`.

## Historical artifact and provider-store diagnostic

Historical bounded observations recorded:

- artifact `vs_BuildTools.exe` at exact URL `https://download.visualstudio.microsoft.com/download/pr/fa619120-9c0e-47e6-bfe0-3ee96fb671b2/236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/vs_BuildTools.exe`;
- size `4473936`, SHA-256 `236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29`, and stable retained identity;
- WinVerifyTrust VERIFY return `0` and CLOSE return `0`;
- provider chain leaf `d33927e4dda9b91def9f8ed282549a49217ed8cacf54577a690963cbc5eff3ed`, intermediate `3dadfaf812dd1bbaef45834ccbd188f3cd97139e2ed1aca69c2dd63082142f8f`, and root `847df6a78497943f27fc72eb93f9a637320a02b561d0a91b09e87a7807ed7c61`.

| Historical reconstruction variant | Result |
|---|---|
| Local-machine/default without provider-owned additional store | Leaf only |
| Local-machine/no-additional-store | Leaf only |
| Provider-owned `hAdditionalStore` included | Exact leaf/intermediate/root chain; trust error `0` |

**RESULT:** the intermediate was absent from the read-only CU/LM MY/CA/ROOT inventory, while the root was present in CU ROOT and LM ROOT. The diagnostic made no trust-store or cache mutation.

**BOUNDED INFERENCE:** historical v0.4’s separate rebuild lacked provider-owned certificate material returned by WinVerifyTrust. This explains that historical chain-rebuild failure but does not authenticate v0.4’s complete transitive execution authority, authorize a V0.1 proposal, or grant active authority.

## Historical review and correction disposition

**HISTORICAL REVIEW INPUT:** the initial fresh review returned `REJECT — BLOCKED` with one BLOCKING finding for mutable transitive v0.4 globals and one MAJOR finding for unbounded strong-reference issuance registries. A later fresh rereview closed both initial findings but returned `REJECT-MAJOR-CONCURRENT-CONSUME-SNAPSHOT-GAP`. The next fresh rereview closed that finding and returned the exact new verdict `REJECT-MAJOR-SNAPSHOT-COMPARATOR-TYPE-CONFLATION` because Python tuple equality could conflate `bool`/`int` and `int`/equal-valued `float` and dispatch attacker-controlled equality while the lock was held.

**CORRECTION EVIDENCE:** the public v0.4 path remains disabled before all transitive calls. Snapshots now recursively canonicalize to exact internal type-tag rows admitting only exact builtin `None`, `bool`, `int`, `str`, and `tuple`; floats, bytes, subclasses, and arbitrary objects reject before equality. Captured nondispatching operations and captured `object.__getattribute__` ensure comparisons operate only on exact internal builtin rows. Direct and nested type conflations and subclasses rejected; hostile `eq`, `iter`, `repr`, `hash`, `int`, `index`, `str`, and `bool` invocation count was `0`; unsafe issue installed no entry and incremented no generation; all `21` production metadata/closure/private-proposal discriminator cases passed. All `9/9` race tests, every cleanup/recovery path, and the prior flood, ABA, and deadlock diagnostics remained green. The earlier stored/pre/result/post/current-entry checks under `RLock`, frozen materializer, exact-once `finally` removal, hard caps, weak callbacks, and generation/ABA-safe removal remain preserved.

**PRESERVED FINAL REREVIEW DISPOSITION:** `INDEPENDENT-REREVIEW-PASS-ACCEPT-CORRECTION-CLOSURE`. The fresh reviewer closed `CAPTURED-HISTORICAL-V0.4-FUNCTION-RESOLVED-MUTABLE-TRANSITIVE-GLOBALS`, `UNBOUNDED-STRONG-REFERENCE-ISSUANCE-REGISTRIES`, `CONCURRENT-CONSUME-DETACHED-RESULT-NOT-SNAPSHOT-AUTHENTICATED`, and `SNAPSHOT-COMPARATOR-TYPE-CONFLATION`, with counts `BLOCKING 0 / MAJOR 0 / MINOR 0` and no new equal-or-higher issue. Before the whitespace hash cascade, the reviewer authenticated 24/24 candidate hashes and sizes, the manifest and sidecar, verifier SHA-256 `4f57c4ad0d56eb2a3e7d21fc067b208d0ddf0925f90188107f466cc5ce2adf2c`, all 9 v0.4 and 8 lifecycle inputs, and the exact second and third external evidence pairs. Under the review prohibition, the reviewer did not independently query Git and did not run tests, network, native trust, or downloaded bytes. This report preserves the supplied reviewer result and does not render a review verdict of its own.

## Required correction boundary

Any correction to historical v0.4 belongs to a separately opened future verifier candidate/gate. That future work must address both complete transitive authority closure and the provider-owned `hAdditionalStore` relation while preserving acquisition, identity, hash, path, VERIFY/CLOSE, evidence, cleanup, and fail-closed constraints. This report invents no future version or gate phrase and modifies no v0.4 byte.

## Required nonclaims

The following remain false or unverified despite correction-closure acceptance: acquired-byte execution, import, installation, compilation, or linking; CPython Sigstore cryptographic/certificate-chain/transparency-log/signature verification; host runtime authority; network producer authority; acquisition producer authority; effective trust; supplier assurance; offline toolchain layout; runtime profile; installation; build; runtime; rehearsal; S0; E0; central system; Project Brain integration; operational safety; economic value; and model-to-model transfer.

This DOCUMENTATION artifact preserves the exact fresh independent-review result, supplies no review verdict of its own, and authorizes no Git mutation.
