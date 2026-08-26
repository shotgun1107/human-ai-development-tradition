# S0 public external-pin recovery implementation candidate v0.1

This directory contains the bounded PUBLIC v0.1 external-pin recovery
implementation candidate for the build/runtime materialization assembly
rehearsal. The exact open gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN RECOVERY IMPLEMENTATION V0.1 ACTUAL EXTERNAL ARTIFACT ACQUISITION AND BUILD RUNTIME ENVIRONMENT CONSTRUCTION OPEN`

The candidate provides fail-closed primitives for exact-URI acquisition,
hash-aware evidence, and inert ZIP staging outside the repository. The live
TEST harness acquired the two artifacts named by the public URL pins without
redirects. It authenticated the CPython 3.12.10 embeddable ZIP against the
frozen SHA-256 and staged its regular-file contents without executing or
importing them.

The same live evidence leaves the Visual Studio Build Tools bootstrapper at
`ACQUIRED-UNAUTHENTICATED`: its expected SHA-256 and expected size are absent.
The digest-like segment in its URL resembles the observed SHA-256, but that
resemblance is not authentication authority. The jsonschema wheel and its
transitive closure were not acquired.

The candidate remains ineligible with these exact blockers:

- `IR-001`
- `IR-002`
- `IR-003`
- `SUPPLIER-ASSURANCE`
- `EFFECTIVE-TRUST-SNAPSHOT`
- `ACQUISITION-PRODUCER`
- `SEMANTIC-VALIDATOR`
- `FRESHNESS-PROVENANCE`
- `JSONSCHEMA-TRANSITIVE-CLOSURE`
- `NATIVE-SOURCE`
- `MATERIALIZER-SOURCE`
- `OFFLINE-TOOLCHAIN-LAYOUT`
- `RUNTIME-PROFILE`

All process, installation, build, runtime, rehearsal, S0, and E0 claim and
validation states remain false. The acquired Build Tools bytes were never
executed. The acquired CPython archive and its inert staging were never
executed or imported. No installer, compiler, build, runtime construction,
candidate process, rehearsal, S0, or E0 operation was authorized or performed.

The live external root is represented in PUBLIC documentation only as
`<OUT-OF-REPOSITORY-ROOT>`. CONTROL retains the exact local path outside public
artifacts.

Final TEST evidence reports 24 of 24 unit tests passing both directly and from
the authenticated snapshot, child/verifier exit codes 0/0, passing mutation
and original-input swap sentinels, stable repository input hashes, and live
harness exit code 0 with status
`LIVE-ACQUISITION-COMPLETED-CANDIDATE-BLOCKED`.

Maximum claim: the candidate acquired the bytes named by the two public pins,
authenticated the CPython archive, and constructed an inert CPython staging
tree while remaining blocked. This is not live trust, process, installation,
build, runtime, rehearsal, S0, E0, central-system, Project Brain integration,
operational-safety, economic-value, or model-to-model-transfer authority or
validation.
