# I0 gate decision

## Decision

- implementation candidate: **acceptable**
- I0 freeze: **withheld**
- sealed F0 authoring: **closed**
- S0 execution: **closed**
- reason: frozen F0-PUBLIC v0.1 data violates its package-ID/path schema
  contract in 20 related locations

The implementation findings from the first independent review were resolved and
the same reviewer found no new Critical or Major issue. The remaining failure is
upstream input conformance, not an I0 auto-repair target.

## Evidence

- implementation manifest:
  `e67004179fc9d922b9fb6d822ac961d576f9c6ca07cd512d4508e29ca038c105`
- regression: two runs, each 36 total / 35 passed / 1 host-constrained symlink skip
- public integrity: 90 files, 56 JSON, 8 packages passed
- deterministic reproduction: 8/8 exact bytes on two invocations
- designated schema errors: 4
- broader related errors: 20
- independent rereview verdict:
  `I0 implementation acceptable but upstream refreeze required`

## Recommended correction direction

Preserve the existing strict 12-character package payload contract. Rename the
four block-2 package stems from the 13-character `P0xB2EMBER001` form to one
consistent 12-character form, recommended `P0xB2EMBR001`. Update every public
package directory and reference, then recalculate the public bundle manifest,
F0-PUBLIC freeze record, and I0 authenticated allowlists/reports/manifests.

This is safer than widening three schemas to accept variable lengths because it
keeps the already-repeated fixed-width contract and changes only fictional
pre-run identifiers and their dependent hashes. No facts, questions, options,
scoring rules, transformations, or expected decisions should change.

## Required next authorization

Do not make that correction under `I0 OPEN`. The next exact protected command is:

`F0-PUBLIC REOPEN`

After that gate opens: correct names and references, validate every applicable
public schema instance, refreeze the public bundle, update the I0 candidate's
dependent hashes, rerun CONTROL tests, and perform a limited independent
rereview. Only then may CONTROL decide whether to freeze I0 or ask for the next
sealed-fixture gate.
