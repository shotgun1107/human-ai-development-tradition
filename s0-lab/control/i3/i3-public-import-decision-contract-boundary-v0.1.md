# S0 v0.14 I3 public import-decision contract boundary v0.1

- `defined_at`: `2026-08-12T11:24:17.6574700+09:00`
- `definition_role`: `CONTROL`
- `source_main`: `0a82a8a091f4aae37b6cf22bd736cc228c420c7f`
- `source_main_tree`: `f5420e159fb4653651773ebff9adef0f9b7e0d2e`
- `status`: boundary definition only
- `implementation_status`: not opened
- `claim_kind`: proposed next public model-free construction boundary

## 1. What I3 means

I3 is the proposed **public import-decision contract** stage after the
main-integrated I2 v0.4 construction.

I2 can authenticate and structurally validate the public 31-line import-event
record, lifecycle tuples, caller-supplied chains and route sets, public signer
inventory, and frozen vector evidence. It deliberately cannot parse a complete
import admission or outcome, or decide the complete outcome class, because the
authenticated public inputs do not yet provide exact byte grammars for those
records.

I3 exists to close only that model-free contract gap. It is not the stage that
creates real keys, starts AI sessions, provisions a VM, reads F0, or runs S0.

## 2. Evidence for this boundary

The main-integrated I2 v0.4 contract reports these nine unsupported
boundaries:

1. `import-admission-exact-grammar`;
2. `import-outcome-exact-grammar`;
3. `complete-outcome-classification`;
4. `durable-ledger`;
5. `project-lifetime-uniqueness`;
6. `atomic-append`;
7. `witness-validation`;
8. `actual-registry-authority`; and
9. `provider-or-platform-enforcement`.

The first three are one coherent public, deterministic problem: exact bytes go
in and one declared classification comes out. The remaining six require
persistence, lifetime state, external authority, or platform behavior. Mixing
them into I3 would turn a bounded model-free contract step into an operational
security system and would recreate the over-expansion risk seen in earlier
review loops.

The v0.4 identity-authority matrix also requires a later separately approved
implementation gate to derive exact machine-readable schemas for
`S0-SIGNER-IMPORT-ADMISSION-2`, `S0-SIGNER-IMPORT-OUTCOME-1`, and the existing
31-line import event from authenticated public text. I2 already supplies the
event codec; I3 must preserve it and add the two missing records rather than
invent a competing event format.

## 3. I3 objective

Produce one authenticated public contract in which:

1. `S0-SIGNER-IMPORT-ADMISSION-2` has one exact canonical byte grammar;
2. `S0-SIGNER-IMPORT-OUTCOME-1` has one exact canonical byte grammar;
3. the existing `S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` grammar remains
   byte-for-byte compatible with the accepted I2 v0.4 contract;
4. every admitted combination of admission, outcome, appliance-state claim,
   route state, event evidence, and failure signal maps to exactly one public
   classification; and
5. every malformed, incomplete, duplicated, replayed, cross-bound, or
   contradictory input rejects deterministically without granting authority.

The desired result is a model-free parser, serializer, and pure classifier
contract that can later be implemented and independently tested. It is not
evidence that a real appliance, host, signer, registry, ledger, or AI obeys the
contract.

## 4. Exact design scope

An I3 design may specify only the following:

- exact record names and version identifiers;
- exact ordered fields, field types, canonical text or byte encoding, line
  endings, maximum lengths, zero values, and forbidden extra bytes;
- exact identity and hash bindings across campaign, ceremony, signer, route,
  request, capability, admission, media, outcome, and event records;
- exact before-state, after-state, route-state, and decision values;
- one deterministic classification precedence and complete classification
  table;
- accepted, rejected, terminal, and structurally blocked results;
- duplicate, missing, malformed, truncated, oversized, replayed, cross-route,
  cross-signer, cross-campaign, and state-disagreement behavior;
- pure model-free validation interfaces and stable error categories;
- a finite conformance and hostile-mutation test plan; and
- migration from the exact I2 v0.4 public contract without changing its
  already accepted event bytes or supplied-set semantics.

The design must distinguish three layers:

1. **byte validity** — whether one record is exactly canonical;
2. **structural consistency** — whether authenticated public records bind the
   same identities, hashes, route, and state transition; and
3. **classification** — which declared public outcome follows from those
   inputs.

Passing any one layer cannot compensate for failure in another.

## 5. Explicitly excluded scope

I3 must not design, implement, provision, or claim:

- durable ledger or witness behavior;
- project-lifetime uniqueness or atomic append;
- actual key generation, custody, signature, anchor, or registry authority;
- hostile same-process protection;
- VM, sandbox, operating-system account, ACL, network, clipboard, Git, vault,
  appliance, provider, or platform enforcement;
- provider or model sessions;
- F0 content, hidden oracle, fixture, executor, judge, scoring, or statistics;
- E0, S0, central-system implementation, or Project Brain integration; or
- operational safety, economic value, production readiness, or model-to-model
  transfer.

Those are not silently waived. They remain closed for later separately gated
live-isolation, persistence, authority, and experiment work.

## 6. Minimum design deliverables

The I3 design gate should produce no more than these four public artifacts and
their same-basename sidecars:

1. one main contract specification covering the three record relationships;
2. one field-and-binding table;
3. one complete classification table; and
4. one implementation and test brief.

Do not create code, fixtures, generated cases, a hidden oracle, platform
configuration, or execution data during the design gate.

The design package must reuse authenticated I2 identifiers and definitions by
exact hash or explicit unchanged reference. It must not copy and subtly fork
the I2 event grammar.

## 7. Design acceptance criteria

The design is ready for independent review only when all of the following are
true:

- each of the two new record grammars has one unique serialization;
- each field has one source, type, canonical representation, and authority;
- every classification input tuple maps to exactly one result;
- precedence cannot suppress a more serious failure or turn uncertainty into
  acceptance;
- accepted classification requires all mandatory identity, hash, state, and
  event bindings;
- missing or contradictory evidence cannot be inferred from shutdown,
  detachment, filename, timing, or host guesswork;
- all rejected paths are terminal at the pure contract level and grant no
  retry or new authority;
- I2 v0.4 event bytes, route semantics, ID ownership, signer inventory, vector
  binding, and closed boundaries remain unchanged; and
- every required hostile case identifies one exact rule and expected result.

No score or aggregate pass may compensate for an ambiguous serialization,
non-total classification, authority escalation, or I2 regression.

## 8. Review-loop limits

I3 review is limited to the stated public byte and classification boundary.

- A review may block only for a concrete ambiguity, contradiction, missing
  case, authority leak, non-total classification, non-determinism, or I2
  regression within that boundary.
- A review must not require VM hardening, Git race defenses, durable storage,
  real cryptography, provider behavior, F0 controls, or S0 execution as an I3
  closure condition.
- Pure wording or presentation improvements that cannot change bytes,
  classification, authority, or fail-closed behavior are non-blocking cleanup.
- If a finding requires one of the explicitly excluded systems, it is recorded
  as a later dependency rather than added to I3.

This rule prevents independent review from continuously expanding I3 into the
whole trust-root and role-isolation system.

## 9. Proposed gate sequence

This boundary document opens no gate automatically. The proposed first exact
gate is:

`S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT DESIGN OPEN`

If separately opened, it authorizes only the four design deliverables in
section 6. The maximum following sequence is:

1. I3 public contract design;
2. one fresh independent design review;
3. bounded model-free implementation candidate;
4. one fresh independent implementation review;
5. CONTROL and main integration decisions.

Revision and rereview occur only for concrete findings inside the frozen I3
boundary. They do not automatically widen the scope.

## 10. What comes after I3

After a zero-finding I3 implementation is integrated, the project can define a
separate minimal live-isolation gate for process or VM boundaries, actual
authority and persistence, and observable enforcement. Only after that live
boundary is demonstrated should protected fixture authoring and S0 execution
be considered.

This ordering keeps public deterministic contract defects separate from
environment and AI-behavior failures, making later S0 results easier to
interpret.

## 11. Maximum claim

The maximum claim from this document is that I3 is now defined as the bounded
public import-admission, import-outcome, and complete-classification contract
stage following I2 v0.4.

No I3 design, implementation, live isolation, authority, F0, E0, or S0 result
has been produced or validated.
