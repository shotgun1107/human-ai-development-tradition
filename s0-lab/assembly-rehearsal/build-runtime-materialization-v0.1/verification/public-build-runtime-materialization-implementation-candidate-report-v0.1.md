# S0 v0.14 public build/runtime materialization implementation candidate report v0.1

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION CANDIDATE OPEN`
- `branch`: `codex/s0-build-runtime-materialization-implementation-v01`
- `baseline_commit`: `5766850afd380b63262ece118940959bd5c68986`
- `implementation_manifest_sha256`: `43a6670acf7165678852b664b9d4752611d7433b43473fe5376c5e1a64bafd70`
- `candidate_status`: bounded PUBLIC implementation candidate
- `external_pin_status`: `BLOCKED-MISSING-EXTERNAL-PIN`
- `build_execution_authorized`: false
- `runtime_materialized`: false
- `native_api_reachable`: false
- `rehearsal_pass`: false
- `F0_content_access`: none

## 1. Outcome

A bounded PUBLIC implementation candidate now exists. It authenticates the
exact five-version build/runtime design chain, reconstructs the effective
v0.5 semantic contract, and produces only an immutable diagnostic that stops
at `BLOCKED-MISSING-EXTERNAL-PIN`.

The implementation does not accept the ten unresolved external pin classes
as caller-selected arguments. This prevents an ambient compiler, SDK,
CPython distribution, dependency set, Windows image, build profile, or
runtime-tree profile from becoming authority by convenience.

## 2. Implemented surfaces

The ten-file implementation manifest covers nine Python modules and one test
module. The implementation provides:

1. strict public manifest and exact target authentication for the authenticated
   v0.1-v0.5 design packages;
2. exact approving-review and CONTROL-decision binding;
3. strict UTF-8/final-LF/duplicate-key JSON parsing and bounded JCS-plus-LF
   serialization;
4. the 6,805-byte semantic-relation preimage with SHA-256
   `5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db`;
5. the 896-byte normative publication policy preimage with SHA-256
   `3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b`;
6. exact matrix reconstruction from 46 base rows to 63, 97, 111, and 115
   effective rows, including failure-suffix/output-bit consistency;
7. equality of the twelve retained public resource ceilings;
8. target-set preimage, canonical virtual path, Windows directory identity,
   DLL-directory derivation, runtime-row and runtime-plan validation;
9. in-memory canonical diagnostic record construction with equal canonical,
   close, and readback hashes; and
10. an optional Draft 2020-12 schema adapter that is not imported by the
    runnable candidate while its exact dependency closure remains missing.

No implementation module imports `ctypes`, `os`, `pathlib`, `socket`,
`subprocess`, or `urllib`. No implementation module exposes `open`, process,
shell, network, native-call, provider, model, or build execution.

## 3. Verification

The verifier authenticated the externally supplied implementation-manifest
pin and all ten rows. It then authenticated the five exact design manifests
and their 6/7/9/9/7 targets, plus the approving v0.5 review and CONTROL
decision. Only those authenticated bytes and `AGENTS.md` were copied into an
isolated temporary snapshot.

The isolated `python -I -B` test process ran 13 PUBLIC synthetic tests with
zero failures, errors, or skips. Tests covered:

- every design-manifest byte mutation;
- changed, missing, extra, and non-byte targets across all five closures;
- approving-review and CONTROL-decision mutations;
- relation patch and policy-authority mutations;
- 115 unique effective mutation rows and 12 retained resource limits;
- target-set ordering and byte grammar;
- virtual-path, Windows reserved-name, separator, Unicode, and traversal
  rejection;
- Windows case-alias rejection and deterministic DLL-directory ordering;
- runtime row uniqueness and resource bounds;
- diagnostic record hash equality; and
- static absence of execution and ambient-import surfaces.

After the child exited, every original authenticated input was re-read and
compared byte-for-byte with the pre-execution snapshot. The swap sentinel
passed.

The verifier uses one Python child process only as test orchestration. The
candidate under test performs zero filesystem, process, native, network,
provider, model, build, materialization, rehearsal, S0, or E0 calls.

## 4. Deliberately closed work

The design requires exact external pins for native source, inspector and
materializer source, offline toolchain, compiler/linker/SDK/CRT identities,
CPython distribution, Python dependencies, Windows platform, complete build
profile, runtime-tree profile, and the approving review. This gate did not
supply those artifacts as a complete authenticated closure.

Therefore this candidate does not:

- compile the native preloader or guard;
- invoke a compiler, linker, SDK tool, materializer, or PE inspector;
- create build roots A/B or a runtime staging tree;
- publish or quarantine a filesystem object;
- call `CreateProcessW`, `NtCreateFile`, or
  `SetFileInformationByHandle`;
- claim that a schema-valid profile authorizes execution; or
- claim a build, runtime, Windows behavior, rehearsal, S0, or E0 result.

The schema adapter remains source-only and outside the runnable import graph
because the exact `jsonschema` dependency closure is itself one of the
unresolved external authorities. Using the host installation would violate
the authenticated-runtime boundary.

## 5. Maximum claim and next review

Maximum claim: the repository now contains a PUBLIC, authenticated-input,
non-executing prerequisite implementation for build/runtime admission and
planning. It correctly refuses to cross the unresolved external-pin boundary.

Fresh independent implementation review is required before CONTROL may
consider any successor. That review must distinguish implemented validation
logic from still-blocked compiler, native source, toolchain, runtime
distribution, materialization, and execution work.
