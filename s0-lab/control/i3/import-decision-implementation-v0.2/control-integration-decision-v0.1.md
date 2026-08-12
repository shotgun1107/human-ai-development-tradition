# S0 v0.14 I3 public import-decision implementation v0.2 CONTROL integration decision v0.1

- `status`: CONTROL integration decision
- `decision_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT IMPLEMENTATION V0.2 CONTROL INTEGRATION DECISION OPEN`
- `candidate_commit`: `4dad07167dbd1c14168c41d78f11fccbe0d07b09`
- `candidate_tree`: `a6b4e375a431aa761fcfacb4fffdd3678332fac3`
- `candidate_parent`: `d1b79cb8a032c285202aef7d72b80121065e217d`
- `candidate_parent_tree`: `4e54bb717398eefd213c6c8c026f9343bd1fba24`
- `independent_rereview_sha256`: `164a5e0d0ec99a503b17ebaee7d8778f2b840c672b3f74760fdee6320f6ddc48`
- `decision`: `ACCEPT-FOR-MAIN-INTEGRATION-CONSIDERATION-ONLY`
- `operational_implementation_status`: closed
- `finding_count`: `0`

## 1. CONTROL decision

CONTROL accepts the authenticated I3 v0.2 bounded public model-free
implementation candidate and its fresh zero-finding independent rereview as
eligible for a separately opened main integration decision.

This decision does exactly three things:

1. recognizes the v0.2 public implementation candidate as the current proposed
   I3 implementation baseline, replacing v0.1 for future implementation
   interpretation;
2. records independent closure of predecessor finding `I3-IIR-B01`; and
3. permits only a separately opened main integration decision gate after this
   decision lineage is preserved in Git.

It does not merge or fast-forward main. It does not establish a real import,
durable ledger, witness, destination authority, protected-material path, E0,
or S0 execution.

## 2. Authenticated decision inputs

| Artifact | SHA-256 | CONTROL use |
|---|---|---|
| root `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` | current role, publication, and F0 boundary |
| canonical text validator | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` | public text and sidecar validation |
| I3 boundary v0.1 | `9a638245f57fe49b4e3557748f0b37d097d794acc9d9650bac7fc7ea2af50aae` | exact bounded I3 scope |
| I3 v0.2 main design | `f04dae684b7373a4c613c3f0e357ef8266f0bf307e78e78d105cb04168f61594` | accepted design authority |
| I3 v0.2 field-binding table | `b034fadf16e7b5d11594c6987ba714e791ef2b2d02409589c6e7b90126e2fa02` | exact field and binding authority |
| I3 v0.2 classification table | `82f787c737f0a255970679b4c501b93061de7b7778e10843d71c047aa69ea706` | exact ordered outcomes and finalization |
| I3 v0.2 implementation/test brief | `182df459eee2877d5c4710794ad7a7c86a56a44abe7ce14d09e629fc1c29ac62` | implementation and closure requirements |
| I2 v0.4 machine-readable contract | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` | unchanged 31-field event authority |
| predecessor I3 v0.1 implementation review | `ec1ecc1f9aaf9b32ca7d285d898ec5620e05a8327716a0e16eed2d01530b28ca` | blocking predecessor finding |
| I3 v0.2 implementation contract JSON | `ae834becfc393e4f525265aff473ae32d12f349713fb48b2e0bb60ea39fc7ac8` | public machine-readable candidate contract |
| I3 v0.2 implementation manifest | `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648` | exact 17-record candidate payload |
| I3 v0.2 public-source manifest | `1b3e96bc5d7e6dcc00efbb9d546f975fb31d6f61dbccd3a1baf5d95bfcb00989` | exact 21-record public source set |
| I3 v0.2 author verification report | `6b218c4e68d3ae091d0998ab141b902041621657da369b9146d3ba87c27c08dc` | bounded author-side evidence only |
| I3 v0.2 independent rereview | `164a5e0d0ec99a503b17ebaee7d8778f2b840c672b3f74760fdee6320f6ddc48` | fresh zero-finding disposition |
| independent rereview sidecar file | `b8ebc5a1a7e8558172e6370a7e19f3c0e3791d83407edca7959cbee1778b88d2` | exact review authentication record |

The independent rereview authenticated and rehashed all 57 admitted public
inputs. Its canonical validator SelfTest passed all 11 named cases, all 13
admitted Markdown/sidecar pairs passed, and the review output pair itself
passed canonical validation. CONTROL independently confirmed that the review
artifact hash equals its same-basename sidecar record before writing this
decision.

## 3. Git and role lineage

The reviewed candidate lineage is:

```text
d1b79cb8a032c285202aef7d72b80121065e217d
  -> 4dad07167dbd1c14168c41d78f11fccbe0d07b09
```

- `d1b79cb` preserves the authenticated v0.1 implementation review that found
  `I3-IIR-B01`;
- `4dad071` adds the bounded v0.2 repair candidate with exactly 13 changed
  public I3 paths; and
- the fresh rereviewer wrote exactly one review Markdown and its sidecar after
  authenticating that candidate.

At CONTROL entry, HEAD remained `4dad071`, tree `a6b4e37`, with exactly the two
authorized untracked rereview outputs and no staged or tracked modification.
CONTROL did not modify any candidate or review input. This decision adds only
this Markdown and its same-basename sidecar. A later preservation commit and
push require their own ordinary Git approval and do not themselves authorize
main integration.

## 4. Finding disposition

### 4.1 `I3-IIR-B01`: closed

The v0.1 finalizer could grant destination authority from a route-compatible
standalone I2 completion event without validating its global sequence and
predecessor hash. The v0.2 finalizer now requires caller-supplied
`expected_sequence` and `expected_previous_event_sha256` and invokes unchanged
I2 `validate_event_global_link` before event-variant matching or any authority
grant.

The independent rereviewer confirmed all of the following:

- exact event link plus accepted classification plus persisted append is the
  sole authority-granting path;
- changing event sequence alone, event predecessor alone, expected sequence
  alone, or expected predecessor alone fails closed;
- missing either or both expected-link values fails closed;
- a hostile huge event sequence with a different predecessor fails closed;
- wrong class, completion ID, route, `H`, state, or append result fails closed;
  and
- direct wrong-link validation produces the stable public I3 error surface
  without exposing raw I2 mismatch text.

The closure is bounded to structural public evidence. Matching caller-supplied
link values and `append_status=persisted` do not prove that a real durable
ledger or witness exists.

### 4.2 New findings

The fresh independent rereview reported:

- blocking: 0;
- major: 0; and
- minor: 0.

Its exact verdict was
`PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`.

## 5. Accepted implementation boundary

CONTROL accepts only these bounded public deterministic implementation claims:

- exact 21-field admission, 26-field outcome, and unchanged I2 31-field event
  grammars;
- exact route mapping, hash, `H/Z`, state, media-size, and ordered
  classification behavior;
- explicit authenticated I2 route context with no hidden route inference;
- I2 global-link validation against both explicit expected-link values before
  any authority grant;
- stable I3 error translation for incompatible completion events;
- destination availability only for an accepted classification, exact event
  and link, and caller-supplied persisted append status;
- deterministic public tests, manifests, verifier, CLI, and closed-boundary
  stubs; and
- preservation of the accepted I3 v0.2 design and I2 v0.4 public contract.

The v0.1 implementation remains historical evidence. It is not a competing
current implementation authority.

## 6. Verified evidence and limits

The authenticated I3 verifier reported generator SelfTest PASS, 26 test
methods PASS, grammar/hash/binding PASS, classification PASS, finalization
PASS, contract CLI version `0.2.0`, import audit PASS, final stability PASS,
static integrity PASS, public-source integrity PASS, and closed boundaries as
`BLOCKED_NOT_EXECUTED`.

The independent rereviewer additionally ran 41 focused closure and boundary
probes plus 33 classification and 33 exact-event finalization cases spanning
all three routes and all 11 rows. Exactly three cases made destination
authority available: one exact accepted case per route. No new finding was
reported.

These are model-free public structural tests. They do not prove durable
persistence, an authentic external witness, project-lifetime uniqueness,
atomic append, real registry or destination authority, key or signature
behavior, hostile-process isolation, platform enforcement, or provider/model
behavior.

## 7. Noncompensatory conditions

Main integration consideration is allowed only while all of the following
remain exact:

1. candidate commit `4dad07167dbd1c14168c41d78f11fccbe0d07b09` and tree
   `a6b4e375a431aa761fcfacb4fffdd3678332fac3`;
2. the candidate's exact 13-path public I3 change set;
3. implementation manifest hash
   `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648`;
4. independent rereview hash
   `164a5e0d0ec99a503b17ebaee7d8778f2b840c672b3f74760fdee6320f6ddc48`;
5. zero findings and the authenticated rereview verdict;
6. unchanged accepted I3 v0.2 design and I2 v0.4 event contract;
7. unchanged inherited PUBLIC-GIT F0 inventory and no F0 content access; and
8. no operational, provider/model, protected-material, E0, or S0 claim.

Any mismatch blocks main integration consideration. A later commit or merge
cannot repair a mismatch by silently replacing reviewed bytes.

## 8. Gates that remain closed

This CONTROL decision does not authorize:

- a real import appliance, raw-media transport, durable ledger, witness,
  registry, key, signature, vault, VM, sandbox, network, or provider;
- actual persistence, atomic append, retry, replacement, project-lifetime
  uniqueness, or destination authority;
- F0 content access, fixture or oracle authoring, executor or judge work;
- model sessions, E0, S0, central-system implementation, or Project Brain
  integration;
- main merge, fast-forward, PR, release, or branch deletion; or
- any claim of operational safety, production readiness, economic value, or
  model-to-model transfer.

## 9. Decision and next gate

**Decision: `ACCEPT-FOR-MAIN-INTEGRATION-CONSIDERATION-ONLY`.**

After the review and this decision are preserved and authenticated in Git, the
exact next permissible experimental gate is:

`S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT IMPLEMENTATION V0.2 MAIN INTEGRATION DECISION OPEN`

That gate may decide whether the authenticated v0.2 public implementation
lineage should be integrated into main. It does not itself perform a merge or
fast-forward.

## 10. Maximum claim

CONTROL has accepted the authenticated zero-finding I3 v0.2 bounded public
model-free implementation candidate for a separate main integration decision.
No real import system, durable authority, platform behavior, protected
material, F0/E0/S0 result, or production readiness has been implemented or
validated by this decision.
