# S0 v0.14 Windows Authenticode trust profile v0.2 independent review brief

## 1. Role and independence

Assign a fresh independent PUBLIC security reviewer who did not author v0.2.
The reviewer is read-only with respect to the candidate package and must not
reuse author conclusions as evidence.

No download, executable or certificate inspection, native API, trust-store
query or mutation, process, installation, build, runtime, rehearsal, S0, E0,
or F0 content access is permitted.

## 2. Maximum inputs

- root `AGENTS.md`;
- canonical text-artifact validator;
- exact v0.2 package manifest and its eight targets/sidecars;
- exact v0.1 trust-profile package manifest and six targets/sidecars;
- exact v0.1 independent review and sidecar;
- exact recovery v0.2 package manifest and four targets/sidecars;
- exact recovery v0.2 independent-review record and sidecar;
- the official Microsoft pages listed in the v0.2 acceptance plan; and
- reviewer-created fake PUBLIC JSON objects and counterexamples.

Do not search the repository broadly. Do not open, list, search, or infer F0
filenames or content.

## 3. Required review

Authenticate all inputs before interpretation. Reconstruct and test:

1. every v0.1 finding and its claimed v0.2 correction;
2. exact Git and predecessor authority constants;
3. raw-observation versus derived-decision separation;
4. all 33 ordered semantic relations;
5. profile/verifier/observation/semantic-validator byte binding;
6. same-handle, same-file, same-provider-state, and same-chain relations;
7. Microsoft supplier assurance without static identity or algorithm pins;
8. mandatory timestamp presence and Authenticode timestamp policy;
9. the one exact signer/timestamp revocation route and per-element freshness;
10. effective trusted/disallowed authority scope and drift handling;
11. recovery v0.2 conflict-inventory completeness; and
12. every hostile mutation in the acceptance plan.

The reviewer must distinguish JSON-schema structure, computed semantic
relations, official Windows guarantees, future implementation obligations,
and current nonclaims.

## 4. Required output

Write one Markdown review and same-basename SHA-256 sidecar under:

`s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-windows-authenticode-trust-profile-v0.2/`

Report exact BLOCKING, MAJOR, and MINOR counts, finding IDs, evidence, impact,
and required corrections. End with exactly one verdict:

- `PASS-FOR-RECOVERY-V0.3-AND-VERIFIER-DESIGN-CONSIDERATION-ONLY`; or
- `REVISE-AND-REREVIEW`.

Do not modify, commit, push, merge, open later gates, or claim any operational
result.

