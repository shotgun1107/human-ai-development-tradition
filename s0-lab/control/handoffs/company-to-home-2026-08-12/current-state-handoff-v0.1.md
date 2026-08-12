# 회사→집 CONTROL 상태 인수인계 v0.1

- `date_kst`: 2026-08-12
- `repository`: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- `handoff_branch`: `codex/company-to-home-handoff-20260812`
- `handoff_payload_parent`: `b9a332e8b2f2a3cda48325170076cd49b90d796a`
- `handoff_payload_parent_tree`: `032f7c53515ac7e1cb34f42508f8fd99d8976cc6`
- `recorded_origin_main`: `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`
- `recorded_origin_main_tree`: `d1ed10e2e8e5e21a510322c002b69b9cf89de848`
- `readiness_audit_commit`: `f44b1d51670d34c86698ede692029feb0b7cb9f4`
- `readiness_audit_tree`: `0c890d604dd0430769c7e30d8b71c3ededfee024`
- `status`: company work complete; exact home synchronization and first report pending

## 1. 이 문서의 목적

이 문서는 회사 PC에서 끝난 Git-tracked 프로젝트 상태를 집 PC에 빠짐없이
전달하기 위한 정본 기록이다. 최종 handoff commit은 이 문서 자신을 포함하므로
그 commit과 tree는 커밋·푸시가 끝난 뒤 사용자가 전달하는 시작 프롬프트의 값을
정본으로 삼는다.

동기화 대상은 Git이 추적하는 프로젝트 파일과 디렉터리다. `.venv`, cache,
Codex 대화 기억, OS 설치 경로처럼 PC마다 다시 만들 수 있는 환경은 동일화
대상이 아니다. 반대로 다음 작업에 필요한 추적 문서·코드·검토 기록은 모두
최종 handoff tree에 들어 있어야 한다.

## 2. 과거 — 회사에서 무엇을 했는가

### 2.1 공개 구현 계보 완료

회사 작업에서는 I2 공개 구현의 수정·독립 심사·통합을 끝낸 뒤 I3를 설계하고
구현했다.

- I2 v0.4는 임의 길이 정수 sequence 정규화 결함을 수정했고 독립 심사에서
  finding 0건으로 통과했다.
- I3 v0.2 설계는 import 결과의 분류, I2 completion event 연결, 최종 권한
  부여 규칙을 고정했고 독립 재심에서 finding 0건으로 통과했다.
- I3 구현 v0.1은 I2 global predecessor/sequence 검증 없이 authority를 줄 수
  있는 blocking 결함이 발견되어 통과하지 못했다.
- I3 구현 v0.2는 I2 global-link 검증을 필수로 추가했고 fresh 독립 재심에서
  finding 0건으로 통과했다.
- CONTROL 통합 결정과 main 통합 결정을 거쳐 `origin/main`은
  `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`가 되었다.

### 2.2 준비성 감사

main 통합 뒤 `f44b1d51670d34c86698ede692029feb0b7cb9f4`에서 I0–I3의
통합 준비성을 공개 문서 기준으로 감사했다.

감사 결론은 다음과 같다.

- I0, I1, I2, I3는 각자의 공개 계약과 독립 승인 계보를 갖는다.
- 아직 네 부품을 한 번에 조립해 연결이 실제로 맞는지 확인한 공개 end-to-end
  rehearsal은 없다.
- 따라서 sealed S0 실행은 아직 열면 안 된다.
- 새 저수준 I4를 추가하는 것보다 먼저 공개 합성 조립 연습의 설계를 만드는
  편이 맞다.

감사 문서:

- `s0-lab/control/readiness/s0-i0-i3-integration-readiness-audit-v0.1.md`
- artifact SHA-256:
  `0ca3e51e8a566a94ed168325d18f5fe6196a132de5c4c6979c8ab7348483ffbf`

### 2.3 회사 고유 공개 기록 보존

회사 기본 worktree에는 집에서 회사로 넘겼던 2026-08-11 공개 인수인계 문서
4개가 남아 있었지만, 최신 main/감사 계보에는 포함되지 않은 분기 상태였다.
그대로 새 handoff를 만들면 다음 PC에서 이 기록이 사라질 수 있으므로, 해당
단일 공개 문서 commit만 최신 감사 tip 위에 재적용했다.

- 보존 후 commit: `b9a332e8b2f2a3cda48325170076cd49b90d796a`
- 보존 후 tree: `032f7c53515ac7e1cb34f42508f8fd99d8976cc6`
- 추가된 범위: 2026-08-11 `home-to-company` 공개 인수인계 Markdown 2개와
  같은 이름의 sidecar 2개뿐이다.

이 처리는 오래된 기술 계보를 main에 병합한 것이 아니라, 누락되던 공개
인수인계 기록만 최신 계보에 보존한 것이다.

## 3. 현재 — 집으로 전달되는 정확한 상태

최종 handoff branch는 다음을 모두 조상으로 포함한다.

1. 현재 main `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`
2. I0–I3 준비성 감사 `f44b1d51670d34c86698ede692029feb0b7cb9f4`
3. 누락되던 회사 고유 공개 인수인계 기록을 보존한
   `b9a332e8b2f2a3cda48325170076cd49b90d796a`
4. 이 문서와 집 PC 재개 프롬프트 및 각 sidecar

세 PUBLIC-GIT / AI-CONTENT-DEFAULT-DENY F0 경로군도 최종 tree에 추적된
상태로 보존된다. 내용이나 개별 filename을 읽는 권한은 부여하지 않으며,
동기화 시 집계만 확인한다.

- aggregate tracked counts: `32 / 11 / 10`
- total: `53`

이 53개는 Git 동기화 대상이다. 경로 이름의 `sealed`는 Git 비공개 판정이
아니라 AI 평가 입력 접근 제한을 뜻한다. clone/fetch/switch/push가 이 파일을
보존해도 AI가 내용을 읽을 권한은 생기지 않는다.

현재 주장할 수 없는 것:

- S0 실행 또는 통과
- hidden oracle, canonical sealed bank, executor, judge 실행
- 실제 key/registry/VM/sandbox/provider/model 실행
- central system 또는 Project Brain 구현
- E0 효과 검증

## 4. 집 PC 동기화 원칙

### 4.1 덮어쓰기보다 보존이 먼저다

집의 기존 저장소에서 먼저 origin, branch, HEAD, status, staged/unstaged,
untracked/ignored, stash, local-only commit, worktree를 읽기 전용으로 확인한다.

- dirty 작업, stash 또는 local-only commit이 있으면 기존 worktree를 움직이거나
  숨기거나 삭제하지 않는다.
- 이 경우 final handoff tip을 별도 clean worktree에 배치한다.
- 완전히 clean한 경우에만 기존 저장소에서 전용 handoff branch로 이동한다.
- `reset --hard`, `clean`, 자동 stash, rebase, main merge는 첫 동기화에서 하지
  않는다.

### 4.2 final handoff tip을 먼저 pin한다

집 PC는 사용자가 대화로 전달한 exact handoff commit과 tree를 먼저 고정한다.
그 뒤 remote branch tip, first parent, ancestry, tree를 비교한다. 움직이는 branch
이름만 믿고 materialize하지 않는다.

반드시 확인할 관계:

- live remote handoff tip = 사용자가 전달한 exact handoff tip
- final handoff first parent =
  `b9a332e8b2f2a3cda48325170076cd49b90d796a`
- payload parent tree =
  `032f7c53515ac7e1cb34f42508f8fd99d8976cc6`
- `402a4a0...`와 `f44b1d5...`가 final tip의 조상
- final tree = 사용자가 전달한 exact handoff tree
- 최종 status와 staged/unstaged diff가 clean

### 4.3 F0는 보존하되 읽지 않는다

최신 root `AGENTS.md`를 먼저 완독한다. F0 세 경로군은 내용을 열거나 검색하거나
filename을 출력하지 않는다. 다음 aggregate만 확인한다.

- final pinned tree counts `32 / 11 / 10`
- local tracked counts `32 / 11 / 10`
- payload parent→final tip quiet diff exit codes가 모두 `0`
- untracked, ignored, skip-worktree, assume-unchanged aggregate가 허용 범위를
  벗어나지 않음

검사 실패는 generic path-family/count 상태만 보고하고 Git 변경을 중단한다.

## 5. 집 PC에서 처음 읽을 공개 정본

동기화와 canonical validator SelfTest가 끝난 뒤 다음 공개 파일만 먼저 읽는다.

1. `AGENTS.md`
2. 이 문서와 same-basename sidecar
3. `s0-lab/control/handoffs/company-to-home-2026-08-12/home-local-resume-prompt-v0.1.md`
   및 sidecar
4. `s0-lab/control/readiness/s0-i0-i3-integration-readiness-audit-v0.1.md`
   및 sidecar

기록된 독립 심사와 테스트를 단순 불신 때문에 다시 실행하지 않는다. 첫 작업은
동기화·인증·인수 보고만 하고 멈춘다.

## 6. 미래 — 다음 작업

다음 후보 gate는 아래 하나다.

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN OPEN`

이 gate가 할 일은 I0→I1→I2→I3 공개 출력과 입력이 실제로 이어지는 작은 합성
조립 연습을 **설계**하는 것이다. 구현, F0 내용 접근, hidden oracle, executor,
judge, provider/model 또는 S0 실행을 여는 gate가 아니다.

집 PC의 첫 동기화 프롬프트는 이 gate를 열지 않는다. 집 CONTROL은 동기화 결과를
과거·현재·미래 순서로 보고한 뒤 사용자 지시를 기다린다.

## 7. 동기화 완료 조건

- exact final handoff commit/tree가 local/remote에서 일치
- final tip이 main, readiness audit, 보존 payload parent를 모두 포함
- Git-tracked 프로젝트 tree가 clean
- F0 aggregate가 `32 / 11 / 10`, parent→final quiet diff가 `0 / 0 / 0`
- handoff 두 Markdown/sidecar pair가 canonical validator에서 PASS
- 새 기술 gate, 구현, 테스트, subagent, commit, push, PR, main merge를 시작하지 않음

이 조건이 충족되면 집 PC는 오늘 회사 작업을 손실 없이 이어받은 것이다.
