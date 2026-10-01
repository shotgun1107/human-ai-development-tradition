# F-03 additional public input recovery — 2026-09-17

CONTROL/maintenance preservation only. This archive is not a runnable runtime, a new fixture, an independent-review verdict, or an automatically admissible role input. Do not import or execute the recovered historical recipe. An explicit role allowlist and the pinned bytes are required before downstream use.

## Authenticated original bytes

| Archived path | Original SHA-256 |
| --- | --- |
| `historical/runtime-profile-v0.4.json` | `266087f18cb16ced698fdfc8089a6ca305aac1d5d0278b1ee4c51f23044b3e9e` |
| `historical/python-named-cases.py` | `adbc21322564ed5f17d6ccfdd5c3c344eaee4b313f3555f39da232e548bdcd00` |
| `historical/base-payload-manifest.json` | `8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798` |
| `historical/historical-verification-summary.json` | `ee2cb08872de7e3abce2a694fcb2a8fffcc126953487728111d2012651d249bb` |
| `design/findclose-amendment-v0.1/amendment-files.sha256` | `980144638bb8b16687c22c0f4cea0fe43bf94a63bda4844529670bd9d45a983a` |
| `design/findclose-amendment-v0.1/amendment.md` | `ea433a52831b2a177455658f2a204950b42d4a91ff162db36419ed8e081df6cb` |
| `design/findclose-amendment-v0.1/amendment.sha256` | Original Markdown sidecar; checked by canonical validator |
| `design/findclose-amendment-v0.1/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.5.json` | `f6aa0f38ad7eb7bf2715fbc6084c5ce9c05db23eccca1af65956735e1e933623` |
| `design/findclose-amendment-v0.1/runtime-profile-v0.5.schema.json` | `04ae781b7d71e2954378cf7cdf2aa9070634ddc3a25c883ac52fb83ebe139d7e` |

Nine files were recovered. Eight content files match independently recorded original SHA-256 values; the ninth is the original amendment Markdown sidecar. No historical expected digest was changed.

## Provenance and transformations

- `historical/runtime-profile-v0.4.json`: original P4, 10,819 bytes. Public audit output at row 893 of `C:/Users/SSAFY/.codex/sessions/2026/09/09/rollout-2026-09-09T11-05-28-01a083e9-bc25-7d40-a70f-a794100e24c7.jsonl` contains the complete recovered P4 JSON. Ordinal-key-sorted compact ASCII JSON with final LF reproduces the original digest exactly. This is byte recovery, not running the historical validator.
- `historical/python-named-cases.py`: original 16,459-byte historical verification recipe. Public output at row 46 of `C:/Users/SSAFY/.codex/sessions/2026/09/08/rollout-2026-09-08T14-38-39-01a07f86-8da7-72c0-941c-4cd9f17cc5d0.jsonl` contains the exact source after authentication messages. Only the shell-added terminal CRLF was removed. The recipe was never executed during this recovery.
- `historical/base-payload-manifest.json`: original 34,849-byte, 174-file base-runtime inventory from public completed command row 31049 of `C:/Users/SSAFY/.codex/sessions/2026/08/26/rollout-2026-08-26T08-22-33-01a03b3b-8bf3-74d0-9833-a89d29ce487f.jsonl`. The captured JSON plus its original final LF matches the pinned digest. Inventory recovery does not restore its binaries or prove current availability.
- `historical/historical-verification-summary.json`: original 4,119-byte summary from public completed command row 34881 of that same parent log. Historical results are preserved claims of that run, not newly executed or revalidated results. The much larger evidence ledger was digest-matched in memory but not copied here: it is not needed for this bounded recovery packet.
- `design/findclose-amendment-v0.1/`: five original files from public completed command row 117 of `C:/Users/SSAFY/.codex/sessions/2026/09/08/rollout-2026-09-08T10-27-44-01a07ea0-d557-7023-87a2-11c1cc0c2efb.jsonl`. The JSON output embeds exact file contents. The original manifest pin was authenticated before admitting its schema, interface map and amendment; each recorded digest matched. The sidecar remains the original sidecar, not a new verdict.

Only selected public command/file-change/visible output records were recovery inputs. No private reasoning, hidden oracle, F0 content, unrelated project conversation body, or complete conversation export was copied. The archive retains historical paths inside original bytes; those are evidence, not instructions to recreate Temp directories or execute commands.

## Limits

The complete original historical static bundle is still unavailable. The original P4 calls for runtime manifest `776e01215b3b2f9edf2c28630f49e36e0c57ae1887b71251758ce398815e7ee0`; recovering P4 does not recover that manifest or its payload. The original 219-file current-runtime inventory, current native binaries and complete historical/base evidence are not restored by this archive. No full historical validator, native build, launch, S0/E0, scoring or provider execution was performed.

These inputs can support separately scoped source/data-flow work, but cannot support a real positive composition or execution claim without the missing material and applicable verification. Original source snapshots, earlier decisions, manifests and hashes remain unchanged. Session replacement alone does not erase exposure; this maintenance document and prior conclusions are not automatic fresh-review inputs.

No staging, commit, push, deletion, installation or Git-state mutation occurred. Branch/HEAD remained `codex/windows-build-toolchain-environment-v0.1` / `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a` (tree `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`).
