# F06 cost-definition erratum v0.1

Candidate: `a03-cost-definition-v0.1`. Date: 2026-09-16. Status: design correction; fresh independent review pending at packet freeze.
This bounded auxiliary evidence work corrects the accounting interpretation of sections 4.3, 4.4 and 6 of `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.4.md`. The historical v0.4 bytes and hash remain unchanged; use that source together with this erratum. This is not a full v0.5 plan or a new execution gate.

## 1. Corrected definitions

Section 4.3 already includes Q-restart primary compensation in `C_human_fixed_max`. Consequently, `C_human_Q_restart_fixed_max` is a visible included-subset memo, never an additional cash term:

```text
0 <= C_human_Q_restart_fixed_max <= C_human_fixed_max
C_total_human_max = C_human_fixed_max + sum_s C_human_s_max
```

The memo covers primary human work for all permitted Q-restart cycles, including identity review, packaging, fresh-pair review and human verification. Preserve explicit Q-restart subrows and their resource ceilings. Q absence/replacement compensation belongs once in `C_replacement_fixed_max`, separately from this primary-human memo; family-dependent replacement compensation remains in its direct family row.

`C_AI_fixed_max` excludes `C_AI_Q_restart_fixed_max`. Those AI fixed rows are disjoint and both remain additive once. Their sum is unchanged. No expense may inhabit both a direct family row and a fixed row, both human and replacement rows, or both base AI fixed and AI restart rows.

All source rows require explicit nonnegative finite values or authenticated zero at a future costing gate. Missing, negative, invalid or unclassified costs cause `STOP/DEFER` until classified; they cannot be silently omitted, including an unclassified zero. This erratum supplies no real prices, rates, people data or budget values.

## 2. Four-bucket attribution and total

Retain `S_ops = {R, H, R_reserve, H_reserve}` and the original result-independent allocation, factual basis, rounding rule and approval constraints. Each `a_s >= 0`, and the four allocations sum to 1. Missing buckets or an invalid allocation cause `STOP/DEFER`.

| Bucket | Attributed human ceiling, including Q compensation once |
|---|---|
| R | `C_human_R_max + a_R * C_human_fixed_max` |
| H | `C_human_H_max + a_H * C_human_fixed_max` |
| R_reserve | `C_human_R_reserve_max + a_R_reserve * C_human_fixed_max` |
| H_reserve | `C_human_H_reserve_max + a_H_reserve * C_human_fixed_max` |

Thus `sum_s C_human_s_attributed_max = C_human_fixed_max + sum_s C_human_s_max = C_total_human_max`. Attributed rows and the original fixed-plus-direct total are alternative views of the same cost: never add both views. Retain fixed and memo rows visibly for traceability. Replacement attribution remains separate under section 4.4.

In section 6, retain every original cash term except the extra additive `C_human_Q_restart_fixed_max`. The complete corrected cash formula is:

```text
C_cash_max = sum_s (C_AI_s_max + C_human_s_max
                   + C_replacement_s_max + C_tools_storage_s_max
                   + C_other_approved_s_max)
           + C_AI_fixed_max + C_AI_Q_restart_fixed_max
           + C_human_fixed_max
           + C_replacement_fixed_max
           + C_tools_storage_fixed_max + C_other_approved_fixed_max
```

Here `s` ranges over all four members of `S_ops`. All four attributed bucket ceilings must pass before totals may be used. Other cash categories, active/wait/calendar time, calls, tokens, staffing minima, fresh-pair restart rules, independence requirements and existing gates are unchanged. No scalar total substitutes for bucket approval.

Existing budget and response interpretations must apply these disjoint definitions before any future E0 plan is used. No mass rewrite of historical documents is authorized or performed, and no claim is made that every other document has been reviewed or aligned.

## 3. Evidence and bounded closure

TEST/VERIFICATION recorded 10 tests, 0 failures, 0 errors and 0 skips on Python 3.12.10 with `-I -S -B`. The records authenticate unchanged policy, source, branch, HEAD and tree before and after that run. The tests check CONTROL-specified algebra and invented exact Decimal arithmetic examples, not later erratum wording. These examples are neither observed costs nor S0/E0 fixtures. A fresh reviewer must compare this text with the source and tested algebra.

| Requirement and evidence flow | TEST evidence and expected rejection | Documentation limit and review closure |
|---|---|---|
| Disjoint cost labels -> fixed/direct map -> cash sum | Each of 26 physical terms has coefficient 1; Q memo coefficient 0; historical duplicate counterexample, zero/nonzero Q, distinct AI and replacement | Close only if the text counts each physical cost once and omits no original category; no observed-cost claim |
| Fixed human row -> four allocated rows -> conserved total | Four-bucket conservation; zero and single-bucket allocations; adding attributed rows as new costs rejects | Close only if both views conserve the same total and are never added together |
| Invalid/missing/unclassified input -> stop | Missing/unknown/negative/nonfinite costs, invalid Q subset and incomplete/invalid allocations reject | No silent omission or newly permissive gate; staffing, time, call and token requirements remain intact |
| TEST source -> recorded outputs -> erratum -> fresh review | Pinned test/source/policy hashes and recorded pre/post identity; no test of later prose | Text-to-math agreement remains for fresh review; documents and sidecars grant no execution or publication authority |

Read-only numerical reproduction, from the repository root:

```powershell
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B 's0-lab/audit-remediation/a03-cost-definition-v0.1/tests/test_cost_definition.py'
```

The evidence producer used the same command with `--record`; that option rewrites the two evidence files and is not a read-only review command. DOCUMENTATION did not execute the numerical tests or modify TEST artifacts.

The host OS, installed Python and standard library, and candidate output root are trusted prerequisites for the recorded benign checks. Their secure provenance, interpreter/import/native-library closure, ACLs, volume/root identity, reparse behavior, rename/replacement, retained handles, concurrency and TOCTOU resistance through evidence writes are `unverified`. Hashes bind inspected bytes, not a secure-host or execution-isolation proof. No external URL, redirect, download or provider authority is used or created. No hidden/shadow-artifact completeness or adversarial host claim is made.

## 4. Ownership, pins and exact review packet

CONTROL: root; CODE IMPLEMENTATION: explicitly skipped because this candidate has no production code/configuration artifact or action, with nobody absorbing CODE; TEST/VERIFICATION: `audit_a03_cost_test`; DOCUMENTATION: `audit_a03_cost_docs`; INDEPENDENT REVIEW: a fresh read-only role to be assigned after this packet. This document is not a review verdict or CONTROL acceptance.

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`.
Branch: `codex/windows-build-toolchain-environment-v0.1`.
Pinned HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`.
Let `C` below mean exactly `s0-lab/audit-remediation/a03-cost-definition-v0.1`.

| Exact allowed input | SHA-256 |
|---|---|
| `AGENTS.md` | `4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065` |
| `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.4.md` | `9124990ebfd328a8628728317cbce62385a2a059e888e30c300eb55627409057` |
| `C/tests/test_cost_definition.py` | `1a445ca0cb103ddb5934abbe7b95a5237ad8b70d91c38c11d8bf09b3c6e0da1f` |
| `C/verification/test-results.json` | `0b96e37f432f808e4e0fe2a9328c93354968f52636395521b07ef01d50733a38` |
| `C/verification/test-stdout.txt` | `302e883cd20512e1b1b23325066ca5bfc4524ccbafaf71fa0a505ea916bb79e3` |
| `s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |

DOCUMENTATION writes only `C/COST-DEFINITION-ERRATUM.md`, its same-basename `.sha256`, and `C/artifact-files.sha256`. The manifest lists exactly the three TEST files above plus the erratum and sidecar, using paths relative to C; it excludes itself. CONTROL must pin the final manifest hash at handoff. The fresh review packet is exactly the six allowed inputs above plus these three DOCUMENTATION outputs, with no linked-source expansion or inherited maintenance history.

The canonical text check uses the pinned validator under native Windows PowerShell, first `-SelfTest`, then `-Path C/COST-DEFINITION-ERRATUM.md` with C expanded. Capture each exit code immediately. Hash mismatch blocks dependent work; do not update historical expected hashes to pass a check.

## 5. Limits and disposition

This corrects a design-level double count only. It establishes no actual cost, economic value, staffing feasibility, operational safety, central-system implementation, Project Brain integration or model-to-model transfer. S0/E0 fixture creation, hidden-oracle work, execution/scoring, real provider calls and pricing remain closed. No F0 content, unlisted paths or other-condition outputs are authorized.

CONTROL reports one opaque unclassified Git-status blocker. This role did not inspect its filenames or waive it. No staging, commit, push, PR or other Git mutation is authorized here. Preserve all other work and the historical source. The auxiliary candidate remains bounded by the 30-minute limit and at most two independent correction cycles; stop before further expansion, framework work or a third correction. Fresh independent review and CONTROL disposition remain pending.
