# I1 public runtime prerequisites revision verification report

## Result

- Authorized gate: `S0 V0.14 PUBLIC IMPLEMENTATION PREREQUISITES REVISION OPEN`.
- Unit suite: **PASS** (61 run, 60 passed, one host-limited symlink skip).
- Authenticated public spec namespace: **PASS** (7/7 files).
- Public spec manifest SHA-256:
  `9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e`.
- Schema definitions: **PASS** (6/6 Draft 2020-12 metaschemas).
- Schema instances: **PASS** (39 positive accepted; 12 negative rejected).
- Frozen topology audit: **PASS** (0 issues).
- Runtime source boundary audit: **PASS** (0 forbidden provider/network imports).
- S0, empirical, operational, cryptographic, or central-system result: **NOT
  CLAIMED**.

This is public construction-test evidence only. It is not an S0 run, executor
result, model result, score, simulation, signature-security result, durable
store result, ACL proof, or atomicity proof.

## Finding closure evidence

### I1-M01: manifest provenance and runner authority

The manifest, grant, authenticated-manifest, and authenticated-byte types have
API-level provenance markers and digest-revalidated bindings. A grant binds the exact
externally expected manifest digest/path/prefix, allowed paths, and purpose.
The runner separately requires that exact grant object, authority digest,
manifest path, request path, and purpose before its only transport call.

Negative tests reject a plain forged object, an unsupported direct constructor,
a tampered authenticated value, a different-purpose grant, and a separately
created equivalent grant with zero transport calls. Trust remains conditional
on the caller independently pinning and holding the required grant; the binding
helper does not authenticate its own inputs. Module-private Python markers are
not anti-forgery protection against hostile code already executing in this
interpreter. Such code is outside this public construction layer and must be
excluded later by process/VM role isolation.

### I1-M02: topology, receipt, store, and signer authority

The pinned loader returns a deeply immutable `FrozenTopology`. Every policy or
record boundary rechecks its API provenance, manifest pin, complete snapshot
digest, and topology audit. Receipt tables and store scopes are derived only
from that handle. Detached or mutated dictionaries cannot authorize a receipt
or store read. Signer mappings are immutable and externally digest-bound; a
plain mapping, altered assignment, or post-load binding-digest mutation rejects.

### I1-M03: published schema accuracy

Receipt schemas enumerate every allowed edge/producer/kind tuple. Bundle schema
branches distinguish ROOT, E02, E25, and one-receipt edges and tie each count to
the envelope array while excluding a ROOT manifest field from non-ROOT records.
Status schema branches tie all sequences 0-14 to the exact event, mask, and
state, including the genesis zero previous hash. Signed-envelope roles are the
22 exact signer IDs.

Direct `jsonschema.ValidationError` tests cover E99, wrong producer/kind,
missing or populated ROOT, E25 count/array mismatch, a non-ROOT manifest field,
and invalid status relations. The verification record separately identifies
byte/hash/signature/chain relations that JSON Schema cannot express.

### I1-M04: namespace change during authentication

Complete-file-set authentication observes initial enumeration, first reads,
re-enumeration, independent rehashes, manifest revalidation, and final
enumeration. Deterministic hooks adding a file after initial enumeration,
changing content after its first read, or adding a file during final manifest
revalidation all reject. Returned bytes are the authenticated first-read bytes.

This closes the demonstrated post-enumeration success counterexample. It does
not claim an atomic immutable filesystem snapshot or protection after return.

### I1-M05: exact scalar and resource bounds

Canonical serializers reject Boolean-as-integer values. Decimal fields are
digit-bounded before integer conversion and failures normalize to the stable
canonical exception. Signature decisions must be exact Boolean `True`.

Runner frames require exact response ID, bytes, and Boolean-final types; empty
frames reject; frame count is at most 256; raw response is at most 8,192 bytes.
Iterator close-call and close-property lookup failures invalidate an otherwise
successful result, while an active primary failure is preserved.

### I1-M06: E43/E45 comparison and publication bindings

E43/E45 codecs implement the exact field order, fixed source roles, full
source-envelope hashes, extracted-record hashes, common agreed-record hash,
fixed custodian signer, and `comparison_digest=SHA256(record_bytes)`. Recipient
verification consumes the exact ordered five-part delivery and repeats every
signature, extraction, role, byte-equality, and digest-scope check.

Publication codecs require byte-identical E53/stored decision bytes, equal
source/published hashes, the exact publisher role/store/result constants, and
canonical timestamp. E54/E55 recipient recomputation binds delivered bytes.
E56 requires the publisher-signed evidence receipt to contain SHA-256 of the
full exact signed publication envelope once, not a hash of its ASCII digest.

Tests mutate source order and roles, source signature, every comparison hash
field, agreed bytes, custodian signer, named digest scope, comparison byte
canonicality, publication hashes/bytes/role/timestamp, E56 edge/role/kind/
signer, double hashing, and premature E56 status order.

### I1-m01 and advisory verifier findings

`verify-i1.ps1` has a mandatory canonical `-ExpectedManifestSha256`. It compares
that external value with the payload manifest before interpreting the adjacent
sidecar. It reads and hashes each payload once, writes those same authenticated
bytes to a temporary snapshot, and only then sets `PYTHONPATH` and runs that
snapshot's tests/CLI. A coordinated payload + manifest + sidecar rewrite is
rejected before a corrupt Python import side effect occurs.

The verifier reports independent non-empty, EF-BB-BF BOM, strict UTF-8,
LF-only, final-LF, trailing-whitespace, ASCII, canonical lowercase hash syntax,
sidecar-format, sidecar-corroboration, and external expected-hash checks. It repeats hashes and
the forced-hidden exact file set after tests/CLI and requires equality with the
pre-execution observation, then removes the execution snapshot.

Output paths are exclusively reserved before invocation. Collision tests show
zero transport calls, and failure removes the transient empty reservation.
Final neutral bytes are written only after runner success.

### I1-v02-m01: exact string path contract

Manifest and entry identifiers now use an exact `str` annotation and runtime
check. Canonical POSIX-relative strings authenticate normally, while a concrete
`pathlib.Path` is intentionally rejected with the matching exact-string error.
The filesystem workspace root remains a `Path`. A regression test binds the
public annotation, accepted string behavior, and fail-closed `Path` rejection.

## Verification commands executed

From the repository root with bytecode writes disabled:

```powershell
$env:PYTHONPATH='s0-lab/i1/implementation'; $env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest discover -s s0-lab/i1/tests -v
$env:PYTHONPATH='s0-lab/i1/implementation'; $env:PYTHONDONTWRITEBYTECODE='1'; python -m s0_i1.cli verify
powershell -NoProfile -ExecutionPolicy Bypass -File s0-lab/i1/tools/verify-i1.ps1 -ExpectedManifestSha256 <externally authenticated implementation-files.sha256 digest>
git diff --check
```

The exact final command results and external implementation-manifest identity
are recorded at handoff after payload freeze. The digest is intentionally not
embedded in this payload namespace, which would create circular self-trust.

## Remaining boundaries

The external grant and signer-binding inputs must be independently trusted.
The verifier script itself must be invoked from a trusted copy or authenticated
by its caller. Source observations are not an atomic or hostile privileged-
writer proof, although candidate Python executes the authenticated temporary
byte snapshot rather than source paths.

No provider/network/model/executor, bank/question/answer/fixture/oracle,
scoring/simulation, sealed/E0, real-data, database/RAG/UI/service, Project Brain,
key/root/registry generation, cryptographic implementation, store backend,
durability, ACL enforcement, atomic E51/E54 write, or duplicate-publication
backend exists. No A-D equality, safety, economic, transfer, production, or S0
claim follows from this revision.
