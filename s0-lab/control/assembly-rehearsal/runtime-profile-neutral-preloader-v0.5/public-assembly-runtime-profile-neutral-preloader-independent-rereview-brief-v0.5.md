# Public Assembly Runtime Profile + Neutral Preloader Independent-Rereview Brief v0.5

Status: frozen brief for fresh, read-only independent design rereview2

## 1. Role, claim, and boundaries

The reviewer must be fresh for candidate v0.5, read-only, and must not have
served as CONTROL, CODE IMPLEMENTATION, TEST/VERIFICATION, or DOCUMENTATION
for this candidate. The only reviewable claim is that the complete successor
DESIGN v0.5 overlay, applied only after complete authenticated v0.4, closes
`RPNP5-IRR-001`, preserves review1's dispositions for `RPNP4-IRR-001`,
`RPNP4-IRR-002`, and `RPNP4-IRR-003`, and introduces no predecessor
regression. The reviewer must not edit artifacts, run substantive new tests,
read F0, grant Git authority, or treat worktree separation as secret
isolation.

The bounded threat model is the 15-row matrix in the v0.5 acceptance plan.
Review may identify contradictions or missing closure within that frozen
claim; it must not expand hypothetical threats into new required product
scope.

## 2. Exact input allowlist and authentication

Repository inputs are limited to these exact public sets:

1. `AGENTS.md`, SHA-256
   `6bff2cef0ddd3ecef6e3f997ec34e9460dc4097c4d46cae73bb32f5ddc10966c`.
2. `s0-lab/control/CURRENT-WORK-LEDGER.md`, SHA-256
   `b2297a6f795fc9695b43635e150a73b89706a79e8ba03464350e4583ed10d544`;
   `s0-lab/control/workstreams/README.md`; and
   `s0-lab/control/workstreams/public-end-to-end-assembly-rehearsal.md`,
   SHA-256
   `0b7167f253e0a03a7ef6ed0f55c9b8ff703b8b29ac2909fbe4f34903ec23c71c`.
3. v0.4 design manifest
   `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/design-package-files.sha256`,
   SHA-256
   `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`,
   exactly its six rows, and their same-basename sidecars.
4. v0.4 implementation manifest
   `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/verification/implementation-files.sha256`,
   SHA-256
   `670803a185e6968f97acb8bdc4acd99932e4dc7722157816a28d684b9e9989f5`,
   exactly its 19 rows, plus the exact candidate report pair. The report
   Markdown SHA-256 is
   `5f9b07ca4fb6f725a568aec281cd018b6012c6d3d8cf71d6176e9eecd732a4ca`.
5. Exactly these three public v0.4 review record pairs:
   `v0.4-independent-rereview-result-preservation-record-v0.1.md`
   (`9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71`),
   `v0.4-implementation-independent-review-result-preservation-record-v0.1.md`
   (`9457b7c358026c22fbe15ec8ffc030828af1085b3577a33af327c44789f100a8`),
   and
   `v0.4-implementation-independent-rereview-result-preservation-record-v0.1.md`
   (`1edea02f498a47839ae9575df41d4f75d4e949b98d6ca87521af2c02dca7c8ab`),
   all under the exact public v0.4 review directory. Do not recurse
   `s0-lab/reviews/`.
6. The exact v0.4 CONTROL decision pair under its v0.4 control directory;
   Markdown SHA-256
   `4342c64a012f6bc9fe9d2550d3879fbef89b592ef08ade1940a3344d9d1c2920`.
7. Exactly the seven v0.5 logical artifacts named by the adjacent
   `design-package-files.sha256`, their same-basename sidecars, and that
   manifest. The exact six non-self logical hashes are acceptance plan
   `2a763fba9e750abdac17b764f1b9d0f4c013423d1fb5458461b69ffe76c65254`,
   design revision
   `a0dc0ea069edebed738829c48ff7edea04c925ed0b0462a5b68b90a7456e9000`,
   interface map
   `83d10d27ce3f6aae21417be435691000f7583a58c86297f46b09752cc633a336`,
   schema
   `19d63a0c0d30369aaaae051e151641af5c6cf1fc71463fadf99bc37068121364`,
   v0.4 response
   `cf4f8ec142f88ddf044b9e72e83f70e658bb113a72f3202744b2faa206a1b1f2`,
   and v0.5 review1 response
   `e5a86cd5c70a6a20410218e12c520633855507eeba558e906014f691b217dfe6`.
   CONTROL must supply the final brief and seven-row manifest hashes.
8. The exact review1 preservation record pair under the exact public v0.5
   review directory; Markdown SHA-256
   `2ae3ce600d3aac263dc526e7fff19efc39a03c3aa22d36bbccfd9540219d463a`.
   The reviewed first-package manifest remains
   `c998b7d18560bfec3142312bb6a0f8f1f708e674082dbc630a7859b157b7b523`;
   it is historical reviewed-byte authority, not the corrected manifest.

Out-of-repository TEST4 inputs are limited to this exact directory and six
filenames:
`C:/Users/SSAFY/AppData/Local/Temp/rpnp-design-v05-test4-20260908/` with
`COMMANDS.md` (`e16f36a6fe7f1b4efcc0f55df96166a7a9583a270829cdb2041f7823bf800bf1`),
`evidence-ledger.json`
(`b36ebd40509ece442870df262b5910b0409dac529e85b81643e4706a3086dfc0`),
`results.json`
(`e0b8444103f89fb5ba00f1ab280a97c3e376f4d81bcd088af95131e1e3072f8f`),
`run_checks.py`
(`2f0c3b7dd78220be99cdaeacb8656cfdbdeece6a778e9b118518525f954f2cd9`),
`summary.md`
(`9cebf9dd922c9df8927f66bed182e3b36a3c78bcfaf2e9e6c4c18e64b05bacf4`),
and `artifacts.sha256`
(`6c49ee508d79d51fab693d6866b6782df14cf32e67237934c0fa24b2ff3e256f`).

Base identity is branch
`codex/runtime-profile-neutral-preloader-design-v0.4-revision`, commit
`440f4342bb27398c6f2a4131d5518f2b55722f4c`, tree
`c77b078ac934ab7a8b31142bad337cf86ee16ca1`. Any mismatch, missing sidecar,
unauthorized input, role contamination, or F0 access returns
`INVALID-REVIEW`. The immutable v0.4 decision's embedded `89fbac...` value is
stale historical metadata; the current record authority is `1edea0...` from
Git bytes and its canonical sidecar.

## 3. Required review questions

The reviewer must answer all of these questions:

1. Does the v0.5 package form one closed overlay that authenticates complete
   v0.4 first, rejects selective/mixed use, and preserves every unaffected
   predecessor obligation?
2. Does the API contract enumerate the exact authenticated guard 18+4 and
   preloader 44+7 role sets, accurately treat the current materializer's empty
   direct-call inventory, freeze the required future physical-isolation calls,
   and require source/import/profile/binary/loaded-route equality with unknown
   and alternate routes rejected? In particular, is the future materializer
   set exactly 29 ASCII-sorted unique calls, with `LocalFree` the sole
   explicitly classified supporting cleanup call and exact-once owner of each
   successful `GetSecurityInfo` allocation on every terminal path?
3. Does evidence v2 freeze US-ASCII/no-BOM/no-CR/exact-final-LF bytes, one
   header, eight ordered semantic groups, all 45 unique ordered fields and
   their exact widths/normalizations, with `external_pin_digest` and
   `workspace_root` inside `run-authority` and every v1/v2 mix rejected?
4. Does physical isolation require component-relative retained-handle opens,
   stable volume/file identity, ACL/token binding, reparse/junction/mount and
   rename/replacement rejection, fail-if-exists relative leaf creation, and
   retained-root-relative output/evidence operations through terminal state?
5. Is repository exclusion physical and explicit across the complete output
   ancestor chain, output root, and evidence root by identity, containment,
   alias, and reparse rebinding rather than lexical prefix?
6. Does each of the 15 frozen adversarial rows have a CODE owner/action, TEST
   diagnostic and expected fail-closed result, DOCUMENTATION claim/nonclaim,
   and review closure criterion, with unknowns blocking broader claims?
7. Do TEST4 results support only internal design/static closure, including
   rejection of all 11 targeted `LocalFree` weakenings, with all
   three UNVERIFIED classes and every downstream nonclaim preserved?
8. Is `RPNP5-IRR-001` closed and are the review1 dispositions for each of
   `RPNP4-IRR-001/002/003` preserved at the design-contract level, without
   claiming implementation or platform truth and without regression?

## 4. Verdict taxonomy and threshold

- `PASS`: valid review, BLOCKING 0, MAJOR 0, `RPNP5-IRR-001` explicitly
  closed, all three predecessor finding dispositions preserved, no
  predecessor regression, and all nonclaims preserved.
- `CORRECT/RETEST`: one or more bounded repairable design defects remain.
- `REJECT`: the frozen design claim cannot be met without redesign or
  unauthorized expansion.
- `INVALID-REVIEW`: authentication, allowlist, role-independence, or F0
  boundary failure prevents a semantic verdict.

Every finding must have an ID, severity (`BLOCKING`, `MAJOR`, or `MINOR`),
exact artifact/key or line location, failure mechanism, and minimum closure
condition. PASS is forbidden with any BLOCKING or MAJOR finding. MINOR items
require explicit CONTROL disposition. The reviewer issues no Git,
implementation, stage, or integration approval.

## 5. Mandatory nonclaims

The review does not prove predecessor profile bytes outside TEST4's allowlist;
runtime source/binary implementation; OS/filesystem/API behavior;
PE/import/loaded-image or full loader closure; post-close same-user/admin
resistance; all-Windows/filesystem correctness; supplier/TLS/provenance beyond
existing pins; stage 70; stage 80; live assembly; official rehearsal; S0; the
central system or Project Brain integration; operational safety; economic
value; model-to-model transfer; or Git publication/integration readiness.
