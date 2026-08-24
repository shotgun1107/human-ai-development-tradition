# S0 v0.14 Windows Authenticode trust profile v0.1 independent review brief

## 1. Role

Use a fresh independent PUBLIC security reviewer. The reviewer must not have
authored this package and must not modify it. No subagent, download, native
API, trust-store mutation, process, provider/model call beyond the assigned
review model, build, runtime, rehearsal, S0, or E0 is permitted.

## 2. Maximum inputs

- root `AGENTS.md`;
- canonical text validator;
- exact trust-profile package manifest and its six targets/sidecars;
- exact recovery v0.2 package manifest and four targets/sidecars;
- recovery v0.2 independent-review preservation record and sidecar;
- the official Microsoft pages named by the authoring and acceptance records;
  and
- reviewer-created fake PUBLIC JSON objects and counterexamples.

No repository-wide search or F0 content access is allowed.

## 3. Required reconstruction

Independently reconstruct the profile and evidence schemas, every constant,
the fixed URL, WinVerifyTrust call contract, revocation/timestamp policy,
byte-identity sequence, claim boundary, and v0.2 compatibility disposition.

Prove from current official Microsoft guidance whether static certificate and
algorithm pins are forbidden or supported. Treat any conflict between the
profile, recovery v0.2, and current Microsoft guidance as substantive rather
than resolving it by reviewer discretion.

Run every hostile mutation in the acceptance plan. Distinguish an honest
blocked authoring candidate from a completed trust profile or real signature
result.

## 4. Output

Produce one Markdown review and same-basename SHA-256 sidecar under:

`s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-windows-authenticode-trust-profile-v0.1/`

Report BLOCKING, MAJOR, and MINOR counts and one exact verdict. Do not commit,
push, merge, open later gates, or claim operational evidence.
