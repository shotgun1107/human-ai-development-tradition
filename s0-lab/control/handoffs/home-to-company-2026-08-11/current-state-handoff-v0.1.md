# 집 PC에서 회사 PC로 넘기는 현재 상태 handoff v0.1

- `handoff_date`: `2026-08-11 KST`
- `repository`: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- `handoff_branch`: `codex/home-to-company-handoff-20260811`
- `handoff_payload_parent`: `be1d56c0f98dba97919f294c253fc1d8368ef623`
- `handoff_payload_parent_tree`: `78541d25d6fb80fbe2738336674d49e375de0610`
- `recorded_origin_main`: `aa68f797ff4be1175048d8329f98d3c469dfb904`
- `active_baseline`: `central-system-v2.1-s0-preparation`
- `claim_kind`: public CONTROL handoff only

이 문서는 집 PC에서 완료한 공개 작업을 회사 PC의 기존 CONTROL 작업에 넘긴다.
대화 기억은 보조 정보일 뿐이며, 회사 PC는 원격 branch, commit, tree, manifest,
sidecar와 현재 `AGENTS.md`를 다시 인증해야 한다.

## 1. 오늘 완료한 공개 작업

### I2 v0.2 공개 구현 후보

- branch: `codex/s0-trust-root-role-isolation-public-implementation-v02`
- commit: `5dc29a6fd1cfebb18c815afc67e34964233d5e58`
- 내용: I1을 수정하지 않는 `s0-lab/i2/**` successor를 만들었다.
- 범위: 공개 import-event codec, 구조적 route lifecycle, 공급 범위 ID 검사,
  공개 signer inventory 결박, 동결 공개 vector 결박과 model-free verifier다.
- 실제 key, signature, VM, provider/model, protected material 또는 S0 실행은 없다.

### I2 v0.2 독립 심사

- branch: `codex/s0-trust-root-role-isolation-public-implementation-v02-review`
- commit: `01a1430d29d3c87e9448d9370a404e60371f721d`
- verdict: `REVISE-AND-REVIEW`
- findings: blocking 0, major 2, minor 0
- review SHA-256:
  `e1b7672e7930cd00246de9263dc3ef7a348b756816ac841f426bc98f4ab27028`

두 major finding은 다음과 같다.

1. 같은 immutable route identity의 성공·실패 또는 복수 종료 이력이 하나의
   supplied set에서 함께 허용됐다.
2. route 간 `result_media_id`/`result_media_id` 및
   `result_media_id`/event-ID 충돌이 aggregate 검사에서 빠졌다.

### I2 v0.3 수정 후보

- branch: `codex/s0-trust-root-role-isolation-public-implementation-v03`
- commit: `be1d56c0f98dba97919f294c253fc1d8368ef623`
- parent: `01a1430d29d3c87e9448d9370a404e60371f721d`
- tree: `78541d25d6fb80fbe2738336674d49e375de0610`
- contract SHA-256:
  `d7d1e877d618508ffcd0f4148d5a8fd0137c2ae4fdca5267fd40e9164c15cd15`
- implementation manifest SHA-256:
  `39386244bba397a1354204b7735508603b3071ef8884f60391beefabc6b21a24`

v0.3은 supplied set에서 immutable route identity를 정확히 한 번만 허용하고,
각 route의 결과 매체 ID 1개와 preallocated event ID 4개를 하나의 다섯-ID
ownership map으로 검사한다. 동일·모순 이력, 두 completion, 역순 충돌과
early-terminal 변형을 회귀시험에 추가했다.

검증 결과:

- unit tests: `37/37 PASS`, skip 0
- shipped verifier: PASS
- `STATIC_INTEGRITY=PASS`
- `PUBLIC_SOURCE_INPUTS=PASS`
- `CONTRACT_CLI=PASS`
- `FORBIDDEN_IMPORT_AUDIT=PASS`
- `FINAL_STABILITY=PASS`
- `CLOSED_BOUNDARIES=BLOCKED_NOT_EXECUTED`
- canonical README/report pairs: PASS
- `git diff --check`: PASS

## 2. 현재 판정

I2 v0.3은 작성자 측 공개 수정 후보다. 아직 fresh independent review를 받지
않았으므로 완료·통합됐다고 주장하면 안 된다. `origin/main`에는 I2 v0.2 심사나
v0.3 수정 후보가 들어 있지 않다.

다음 기술 작업은 별도 게이트인 다음 작업이다.

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.3 INDEPENDENT REVIEW OPEN`

이 심사가 통과하고 CONTROL 통합이 별도로 승인되기 전에는 main 병합이나 실제
key, root, registry, VM/Sandbox, provider/model 또는 S0 실행을 시작하지 않는다.

## 3. 공개·봉인 경계

F0의 세 default-deny 경로군은 Git 동기화 대상이지만 AI 입력이 아니다. 회사
CONTROL은 동기화 감사에서 상위 경로별 aggregate count, tracked 상태, quiet diff,
supplied hash만 확인할 수 있다. 내부 파일명·내용을 열거나 검색하거나 다른
에이전트에 전달하면 안 된다. 기대 aggregate는 `32/11/10`, 합계 `53`이다.

이번 handoff와 I2 작업에는 F0 내부 내용, hidden oracle, protected material,
fixture, 실제 key, provider/model session 또는 실행 결과가 포함되지 않는다.

집 PC의 payload parent에서 내용 비열람 방식으로 확인한 결과는 aggregate
`32/11/10`, 합계 `53`, `origin/main` 대비 quiet diff exit `0`, F0 status anomaly
count `0`이다.

## 4. 회사 PC 동기화 원칙

1. 기존 회사 저장소를 새 clone으로 대체하지 않는다.
2. 먼저 path, origin, branch, HEAD, upstream, tracked/staged/untracked/ignored,
   stash, local-only commit과 worktree를 읽기 전용으로 확인한다.
3. dirty, stash 또는 local-only commit이 있으면 이를 보존하고 새 clean worktree를
   exact handoff tip에서 만든다. reset, clean, stash, rebase 또는 덮어쓰기를 하지
   않는다.
4. clean이면 fetch 후 움직이는 branch 이름이 아니라 채팅으로 전달된 exact
   handoff tip을 pin한다.
5. handoff tip의 첫 부모가 이 문서의 `handoff_payload_parent`인지 확인한다.
6. 동기화 후 현재 `AGENTS.md`를 완독하고 이 문서와 resume prompt의 sidecar를
   canonical validator로 검증한다.
7. I2 verifier는 위 implementation manifest hash를 외부 pin으로 사용한다.

## 5. 아직 주장하면 안 되는 것

- I2 v0.3 독립 심사 통과 또는 CONTROL 통합
- 실제 trust root, key custody 또는 role-isolation deployment
- sealed bank, label/oracle, projection 또는 실행 package 완성
- executor, judge, scoring, S0 또는 E0 실행·효과
- 중앙 전통 시스템, Project Brain 통합, 운영 안전성, 경제성 또는 장기 전승
