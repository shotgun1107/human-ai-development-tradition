# I1 public runtime prerequisites

This directory implements only the authenticated public structural prerequisites
opened by `S0 V0.14 PUBLIC IMPLEMENTATION PREREQUISITES OPEN`. It is not an S0
run and does not implement or validate the central system.

## Authenticated facts represented here

- The frozen public topology contains 32 aggregated role matrix/index rows.
  Eight rows have two positions, so the rows describe 40 positions; they are
  not recast as a 40-role registry. Only the plan's 22 signer role IDs are
  machine-enumerated as signer roles.
- The topology contains 27 literal stores and 64 edge rows: E00A-E00H and
  E01-E56.
- Status order is E02, E05, E08, E14, E21, E24, E25, E27, E29, E31, E35,
  E48, E50, and E56. It has 15 prefix states, 17 receipts, and 15 E51
  envelope/bundle pairs including ROOT.
- E25, E27, E29, E35, E48, and E50 are explicitly frozen as separate
  protected-payload/public-receipt routes; the registrar path is receipt-only.
- `spec/public-runtime-files.sha256` authenticates the topology and six public
  Draft 2020-12 structure schemas. The implementation reads and hashes each
  file once, then parses those same in-memory bytes.

## Implemented public structure

The Python package provides:

- path-safe manifest authentication with traversal, substitution, symbolic
  link, reparse-point, file-identity, complete-file-set, and changed-during-read
  checks; runner inputs carry an internal provenance capability created only by
  the authenticated reader, so a self-hashed public dataclass is insufficient;
- deterministic topology inventory and role/store/edge cross-index validation,
  with omission-as-denial store reads and A/B or 1/2 position separation;
- exact ASCII/LF parsers and serializers for section-4 evidence receipts,
  ROOT and non-genesis bundles, status records, and generic signed envelopes;
- receipt ordering/count checks, ROOT manifest binding, and the complete
  genesis-through-prefix status transition validator;
- an injected signature-verifier protocol. No cryptographic library, public or
  private key generation, registry construction, or signature implementation
  is included; and
- a provider-neutral one-shot abstraction. It invokes one injected transport
  method once, exposes zero retry/tool/state surfaces, stops at the first final
  response, and enforces 8,192 raw bytes before UTF-8 or JSON parsing.

The neutral one-shot result records hashes and byte counts, not response
content or a semantic score. Optional file emission happens only after full
success and never overwrites an existing file.

## Runtime and verification

The code is Python 3.12-compatible and uses the pinned dependency in
`requirements.txt`:

```text
jsonschema[format]==4.26.0
```

Dependencies are not installed by this repository and no command below needs
network access. From the repository root, with the pinned dependency already
available:

```powershell
$env:PYTHONPATH = 's0-lab/i1/implementation'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m unittest discover -s s0-lab/i1/tests -v
python -m s0_i1.cli verify
powershell -NoProfile -ExecutionPolicy Bypass -File s0-lab/i1/tools/verify-i1.ps1
```

`verify-i1.ps1` verifies a separately anchored, exactly 26-row payload manifest.
It uses forced hidden-file enumeration and rejects any other extra (including
`__pycache__`), missing, unsafe, duplicate, or changed payload file. The
manifest and its digest anchor are the two excluded verification-control files.

## Construction-test evidence

On the current Windows host, 32 non-semantic tests run: 31 pass and one direct
symlink test is skipped because unprivileged symlink creation is unavailable. The
reparse-attribute sentinel, explicit traversal, resolved containment, path
substitution, manifest-anchor, complete-file-set, cross-role denial, receipt,
bundle, status, signature-injection, overflow-before-parse, first-response, and
no-output-on-failure tests all pass.

These are local construction tests only. They do not prove durable storage,
ACLs, atomic writes, cryptography, provider behavior, model behavior, executor
isolation, or any empirical outcome.

## Explicitly closed boundaries

This implementation does not create or read a bank, question, answer, fixture,
oracle, score, hidden/sealed artifact, E0 artifact, or real/past-project data.
It has no model/provider/network implementation, executor creation, database,
RAG, UI, service, Project Brain path, simulation, judge, comparator, or scoring
path.

The effective answer member order, field-specific size limits, ID-array rules,
direct-operation semantics, canonical response serializer, concrete package and
common-resource schemas, and run-log byte grammar are not reconstructed from
unauthorized predecessor sources. They remain explicitly unsupported at this
gate. Likewise, store backends, durability, ACL enforcement, atomic E51/E54
writes, actual root/registry artifacts, keys, and signature verification remain
closed. The generic signed envelope is used only for v0.14 section-4 records
that explicitly invoke it; it does not replace inherited signing formats.
