# F0-PUBLIC independent review brief

## Role

You are an independent read-only reviewer. You did not author the F0-PUBLIC bundle and must not edit it. This is a review of public practice material only, not sealed F0 pre-review or S0 judging.

## Allowed inputs

The allowlist is a hard maximum:

1. `AGENTS.md` — expected SHA-256 `14f1d05cca42fd4d7930cad2537bb34bcec17ebcb22630e2f004798123f7a5a2`
2. `s0-lab/control/f0-public/f0-public-authoring-brief.md` — expected SHA-256 `cc30d87e96e58e80edb8ebebee062e87f753b7edbac61b1fbc2db536c213dcb7`
3. `s0-lab/control/s0-protocol-v0.3.md` — expected SHA-256 `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c`
4. The 11 schema files named in the authoring brief, at the exact hashes recorded there
5. `s0-lab/public-practice/v0.1/bundle-files.sha256` — expected SHA-256 `625077016e8597eaa069bef033409c1dcb7f5a1c58d87a31f1bfd827485b0a87`
6. Only the 90 bundle files named and hashed by that manifest

Do not search the repository or read any other file. Verify all controlling hashes before substantive review. If any differs, stop.

## Review questions

1. Do all 90 manifest entries exist, match SHA-256, and exclude the manifest itself with no extra bundle files?
2. Do all JSON files parse, and do the 11 designated instances satisfy their frozen schemas, including conditionals and closed-object rules? State clearly whether this is engine validation or static review.
3. Are file-to-file hashes, IDs, paths, fact/record/question sets, P01–P04 pairings, and both block bindings internally consistent?
4. Does every P01–P04 package for a block preserve the same facts and question opportunities without adding unsupported meaning?
5. Are package byte differences within 15% without padding, and are the byte calculations reproducible?
6. Do runner-visible names, instructions, inputs, and questions avoid revealing a preferred condition, A–D mapping, H0/H1, scoring, or error-code hints?
7. Is every datum visibly fictional and public, with no claim that public oracle/scoring is hidden or operational evidence?
8. Is the bundle sufficient and reasonably minimal for I0 format/implementation practice, or does its 91-file structure introduce avoidable complexity or misleading stand-ins?
9. Could any public practice name, wording, answer order, or derived relation accidentally constrain or contaminate later sealed F0 material?
10. Does the candidate honestly preserve the boundary: no implementation, no execution, no operational isolation proof, no S0 evidence?

## Verdict and output

Return one of:

- `현재 F0-PUBLIC 동결 가능`
- `제한 수정 후 재심사`
- `동결 불가`

List findings as blocker `F0P-Bxx`, major `F0P-Mxx`, or minor `F0P-Nxx`; include exact file paths and concise evidence. Separate verified facts, inference, and recommendation. Also report checked and unchecked scope. Do not write files, create code, run S0, commit, push, branch, or spawn another agent.
