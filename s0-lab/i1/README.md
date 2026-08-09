# I1 public runtime prerequisites revision

This directory implements only the non-semantic public construction layer
authorized by `S0 V0.14 PUBLIC IMPLEMENTATION PREREQUISITES REVISION OPEN`.
It is not an S0 run and does not implement or validate the central system.

## Frozen public facts represented here

- The public topology has 32 aggregated role rows and 40 row positions. Eight
  rows have two positions. These are not recast as a 40-role key registry.
- It has 27 literal stores, 22 signer role IDs, and 64 edge rows: E00A-E00H
  plus E01-E56.
- Status order is E02, E05, E08, E14, E21, E24, E25, E27, E29, E31, E35,
  E48, E50, and E56. There are 15 prefix states, 17 receipts, and 15 E51
  envelope/bundle pairs including ROOT.
- The authenticated seven-file public spec namespace is listed by
  `spec/public-runtime-files.sha256`. Its externally pinned manifest SHA-256
  is `9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e`.

## Authority and immutability boundaries

`ManifestGrant` is an API-level capability object binding an exact manifest path, externally
expected manifest SHA-256, namespace prefix, sorted allowed-entry set, and
purpose. `bind_external_manifest_grant` checks and binds values supplied by an
independently trusted caller; it does not discover, approve, or make those
values trustworthy. Under the supported trusted-caller API, a plain object,
unsupported direct constructor, adjacent manifest, or separately created but
equivalent grant cannot substitute for the exact caller-held object at the
runner boundary.

These Python objects are not a hostile same-process security boundary.
Module-private markers, frozen dataclasses, and expected hashes can be bypassed
by code that is already allowed to introspect or mutate this interpreter. The
integration caller must therefore be trusted and must obtain its pins
independently. Process/VM role isolation belongs to the later isolation phase;
the present tests prove API discipline and byte integrity, not resistance to
malicious code loaded into the CONTROL process.

Manifest entries retain the exact grant object, authority digest/path, entry
path, purpose, and same-byte hash. Complete-file-set loading performs initial
enumeration, authenticated reads, re-enumeration, an independent content
rehash, manifest revalidation, and a final enumeration. Success means those
observations were stable across the checks and the returned first-read bytes
were authenticated. It is not an atomic filesystem snapshot and does not
promise resistance to a privileged concurrent writer after return.

The pinned topology loader returns an API-level, deeply immutable
`FrozenTopology`. Receipt, bundle, status, and store-policy APIs accept only
that handle and recheck provenance, the complete snapshot digest, the pinned
manifest digest, and the topology audit at each boundary. Detached dictionaries
are diagnostic copies with no authority. Signer assignments likewise require
an immutable `SignerAuthority` matching an externally expected binding digest;
no key registry or trust root is created here.

## Exact public codecs and checks

The package implements exact ASCII/LF codecs and validators for:

- generic section-4 signed envelopes;
- all 17 evidence-receipt identities, ROOT/non-ROOT bundles, status records,
  and the complete ROOT-through-E56 chain;
- E43 and E45 comparison records and the ordered five-part recipient delivery,
  including full source-envelope hashes, extracted-record hashes, fixed roles,
  common byte equality, custodian signer, and the named record digest; and
- the publication record, E54/E55 decision-byte recomputation, and E56's
  single SHA-256 binding to the full signed publication envelope.

Signature decisions are injected and must return the exact Boolean `True`.
There is no cryptographic library, signing, key generation, private-key
custody, registry construction, root artifact, or rotation implementation.

The six Draft 2020-12 schemas are checked both as metaschemas and with positive
and negative instances. Expressible receipt edge/role/kind combinations,
ROOT/non-ROOT fields and counts, envelope-array counts, signer roles, and all
15 sequence/edge/mask/status relations are constrained in schema. Byte order,
hash scope, extraction, signature decisions, previous hashes, commitments,
timestamp ordering, comparison equality, and publication equality remain
runtime checks and are reported separately.

## Provider-neutral one-shot boundary

The runner requires the exact caller-held grant plus separately expected
authority digest, manifest path, request path, and purpose before transport. It
then makes one injected method call with zero retries, tools, or state. It
accepts only exact `ResponseFrame` values, exact string/bytes/Boolean fields,
one response ID, non-empty frames, at most 256 frames, and at most 8,192 raw
bytes. It stops at the first final frame and closes the iterator without
consuming a later response.

A cleanup failure invalidates an otherwise successful call. If validation or
transport already failed, that primary failure is preserved and cleanup
failure is secondary. JSON parsing is strict UTF-8 with no BOM, duplicate key,
surrogate, non-NFC string, non-finite number, or oversized integer.

For file output, the destination is exclusively reserved before the sole
invocation, so an existing-path collision causes zero transport calls. The
reservation is temporarily an empty file. Neutral result bytes are written
only after full runner success. Any failure closes and removes the reservation;
an inability to remove it is a distinct `OutputError`.

## Verification

Python 3.12 or later and the already installed pinned dependency are required:

```text
jsonschema[format]==4.26.0
```

From the repository root:

```powershell
$env:PYTHONPATH = 's0-lab/i1/implementation'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m unittest discover -s s0-lab/i1/tests -v
python -m s0_i1.cli verify
$trustedManifestSha256 = '<64 lowercase hex from an independently authenticated source>'
powershell -NoProfile -ExecutionPolicy Bypass -File s0-lab/i1/tools/verify-i1.ps1 -ExpectedManifestSha256 $trustedManifestSha256
```

The PowerShell verifier requires the external expected hash of
`verification/implementation-files.sha256`. It compares that value before
trusting the adjacent sidecar, authenticates all 26 payload files and the exact
forced-hidden file set, writes those already authenticated bytes to a temporary
snapshot, and only then sets `PYTHONPATH` and executes candidate Python from
that snapshot. It runs the tests and CLI there, repeats the full source
observation afterward, and removes the snapshot on exit.
It independently reports non-empty, exact EF-BB-BF BOM, UTF-8, LF-only,
final-LF, trailing-whitespace, ASCII, canonical lowercase hash syntax,
sidecar-format, sidecar-corroboration, and external-anchor checks.

The verifier script is executable code and must itself be obtained from an
already trusted copy or authenticated by its caller before execution. Its
source pre/post checks are deterministic observations over a mutable
filesystem. Candidate Python consumes the authenticated snapshot bytes rather
than reopening source payload paths. This is not a hostile privileged-
filesystem or operating-system proof.

The current construction suite runs 60 tests: 59 pass and one direct Windows
symlink-creation test is skipped when unprivileged symlink creation is denied.
The privilege-free reparse sentinel and mocked rejection path still run.

## Closed boundaries

This revision does not create or read a bank, question, answer, fixture,
oracle, score, hidden/sealed artifact, E0 artifact, real customer data, or
past-project data. It has no model/provider/network implementation, executor,
database, RAG, UI, service, Project Brain path, simulation, judge, comparator,
or scoring path.

Store backends, durable ACL enforcement, atomic E51/E54 writes, duplicate
publication prevention, actual root/registry/integration artifacts, keys, and
cryptographic verification remain closed. The generic signed envelope applies
only to the section-4 records that explicitly invoke it and does not replace
inherited signing formats. These construction results provide no A-D fairness,
operational-safety, economic-value, transfer, production, or S0 evidence.
