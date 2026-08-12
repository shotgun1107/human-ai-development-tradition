# 집 PC CONTROL 재개 프롬프트 v0.1

당신은 `human-ai-development-tradition` 프로젝트를 집 PC에서 이어받는 기존
CONTROL 작업이다.

새 프로젝트 설명, 새 clone 또는 기초 설치를 처음부터 반복하지 마라. 과거
대화 기억은 보조 정보로만 사용하고 현재 Git 상태, 최신 root `AGENTS.md`,
인증된 저장소 기록을 정본으로 삼아라.

## 정본 식별자

- repository:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`
- 회사→집 handoff branch:
  `codex/company-to-home-handoff-20260812`
- handoff payload parent:
  `b9a332e8b2f2a3cda48325170076cd49b90d796a`
- payload parent tree:
  `032f7c53515ac7e1cb34f42508f8fd99d8976cc6`
- recorded origin/main:
  `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`
- main tree:
  `d1ed10e2e8e5e21a510322c002b69b9cf89de848`
- readiness audit commit:
  `f44b1d51670d34c86698ede692029feb0b7cb9f4`
- readiness audit tree:
  `0c890d604dd0430769c7e30d8b71c3ededfee024`

exact final handoff commit과 tree는 이 프롬프트를 전달하는 사용자 메시지에
별도로 적힌 값을 사용한다. 저장소 안의 이 프롬프트가 자기 자신의 final commit
hash를 주장한다고 가정하지 마라.

## 이번 첫 작업

이번 첫 작업은 집의 기존 작업을 보존하면서 Git-tracked 프로젝트 상태를 exact
final handoff tip으로 동기화하고 인증한 뒤 보고하는 것뿐이다.

다음을 하지 마라.

- 구현 또는 설계 수정
- 테스트 재실행 또는 추가 감사
- subagent/하위 에이전트 호출
- 새 commit, push, PR, main merge
- reset, clean, 자동 stash, rebase
- F0 내용·개별 filename 접근
- 다음 기술 gate 시작

## 1. 집의 기존 작업 보존 확인

기존 저장소에서 먼저 다음을 읽기 전용으로 확인한다.

- resolved repository path와 top-level
- origin URL
- 현재 branch, HEAD, upstream
- tracked/staged/unstaged 상태
- untracked와 ignored aggregate
- stash
- local-only commit
- worktree 목록
- detached HEAD 여부

origin은 다음 repository를 가리켜야 한다.

`https://github.com/shotgun1107/human-ai-development-tradition.git`

다른 repository면 아무것도 바꾸지 말고 보고 후 멈춰라.

dirty 작업, stash 또는 local-only commit이 하나라도 있으면 기존 worktree를
switch/reset/clean/stash/rebase/merge하지 마라. 기존 작업을 그대로 두고 exact
handoff tip을 별도 clean worktree에 배치한다. 완전히 clean한 경우에만 기존
저장소를 전용 handoff branch로 전환할 수 있다. 새 clone은 기존 저장소가 실제로
없을 때만 허용한다.

## 2. F0 동기화 경계

다음 세 경로군은 Git 동기화 대상이지만 AI 입력은 default-deny다.

- `s0-lab/control/f0-sealed/**`
- `s0-lab/f0-sealed-staging/**`
- `s0-lab/reviews/f0-sealed/**`

내용, 개별 filename, hash 목록, 답, oracle 또는 내부 구조를 출력·열람·검색하지
마라. aggregate tracked count, quiet diff exit code, supplied aggregate만 확인한다.

기대값:

- `32 / 11 / 10`
- total `53`

fetch 후 어떤 switch, checkout, merge, worktree materialization보다 먼저 exact
pinned target tree의 위 aggregate를 확인한다. native Git 출력은 filename이
나오지 않도록 캡처해 aggregate로 줄이고, 각 실패 exit code를 즉시 보존한다.

## 3. fetch와 exact pin 검증

읽기 전용 preflight가 통과하면 원격을 한 번 fetch한다. 그다음 사용자가 전달한
exact final handoff commit을 pin하고 다음을 검증한다.

- live remote `codex/company-to-home-handoff-20260812` tip = exact final tip
- final tip tree = 사용자가 전달한 exact final tree
- final tip의 유일한 첫 부모 =
  `b9a332e8b2f2a3cda48325170076cd49b90d796a`
- payload parent tree =
  `032f7c53515ac7e1cb34f42508f8fd99d8976cc6`
- `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`가 final tip의 조상
- `f44b1d51670d34c86698ede692029feb0b7cb9f4`가 final tip의 조상
- readiness audit tree =
  `0c890d604dd0430769c7e30d8b71c3ededfee024`
- exact target F0 aggregate = `32 / 11 / 10`
- payload parent→final tip의 세 F0 quiet diff exit code = `0 / 0 / 0`

하나라도 다르면 임의로 최신값을 받아들이거나 덮어쓰지 말고 실제 aggregate와
public commit 상태만 보고한 뒤 멈춰라.

## 4. exact tip materialization

기존 저장소가 clean이면 exact pinned commit만 사용해 handoff branch를
fast-forward 또는 tracking branch로 배치한다. fetch가 포함된 `git pull`은 쓰지
마라.

기존 저장소가 dirty/stash/local-only 상태면 별도 clean worktree를 exact pinned
commit에 배치한다. 기존 worktree의 branch, index, working files를 건드리지
마라.

materialization 후 다음을 확인한다.

- local HEAD = remote exact handoff tip
- local tree = exact handoff tree
- branch/upstream 또는 detached pinned worktree 관계가 의도와 일치
- status 출력 0
- staged diff exit 0
- unstaged diff exit 0
- local F0 aggregate `32 / 11 / 10`
- skip-worktree와 assume-unchanged aggregate 0

## 5. 공개 정본 인증과 읽기

최신 `AGENTS.md`를 처음부터 끝까지 읽는다. 그 지시를 적용한 뒤 canonical
validator를 인증하고 SelfTest를 실행한다.

SelfTest가 PASS일 때만 다음 두 Markdown/sidecar pair를 검증하고 완독한다.

1. `s0-lab/control/handoffs/company-to-home-2026-08-12/current-state-handoff-v0.1.md`
2. `s0-lab/control/handoffs/company-to-home-2026-08-12/home-local-resume-prompt-v0.1.md`

그다음 아래 공개 감사 문서와 sidecar를 인증해 읽는다.

- `s0-lab/control/readiness/s0-i0-i3-integration-readiness-audit-v0.1.md`

기록된 과거 심사나 테스트를 단순 불신 때문에 다시 실행하지 마라.

## 6. 현재 상태

- main의 I2 v0.4 공개 구현: 통합 완료
- main의 I3 v0.2 설계·공개 구현: 독립 재심 및 통합 완료
- I0–I3 개별 공개 계보: 승인됨
- I0→I3 공개 합성 end-to-end 조립 연습: 아직 없음
- sealed S0, hidden oracle, executor, judge, provider/model, E0: 미실행

다음 후보 gate는 다음 문구지만 이번 프롬프트는 열지 않는다.

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN OPEN`

## 7. 첫 보고 후 정지

다음을 과거·현재·미래 순서로 쉽게 보고한다.

- 과거: 집 기존 branch/HEAD와 보존해야 했던 local 상태
- 현재: final local/remote commit과 tree 일치, clean 여부, F0 aggregate,
  handoff pair/validator 결과
- 미래: readiness audit 결론과 다음 후보 gate가 하는 일

보고 후 아무 파일도 만들거나 수정하지 말고 사용자 지시를 기다려라.
