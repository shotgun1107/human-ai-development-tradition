# 회사 PC CONTROL 재개 프롬프트 v0.1

당신은 `human-ai-development-tradition` 프로젝트를 회사 PC에서 이어받는 기존
CONTROL 작업이다. 새 프로젝트 설명, 새 clone 또는 기초 설치를 처음부터
반복하지 마라. 과거 대화 기억은 보조 정보로만 사용하고 현재 Git 상태, 최신
root `AGENTS.md`, 인증된 저장소 기록을 정본으로 삼아라.

## 정본 식별자

- repository:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`
- 집→회사 handoff branch:
  `codex/home-to-company-handoff-20260812`
- handoff payload parent:
  `179dd6f76f2709881900a42dc32cbde8c33c33b0`
- payload parent tree:
  `86bd304b06180c304f0e09ae5ecd0f0d7019e25a`
- recorded origin/main:
  `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`
- included company→home handoff:
  `f7048e919ab0e698d78ca4ff4cc4eb31ca6f612c`
- v0.1 design/review:
  `49ecc05dacebf043ed8b2b479eb021018d4b4fe6` /
  `571c8751d0abb8acfb853d402c072fdb7667bde7`
- v0.2 design/review:
  `18a9562a9da48ce5743fc183c8c68c15d00cf249` /
  `179dd6f76f2709881900a42dc32cbde8c33c33b0`

exact final handoff commit과 tree는 이 프롬프트를 전달하는 사용자 메시지의 값을
사용한다. 저장소 안의 프롬프트가 자기 자신의 final commit을 주장한다고
가정하지 마라. branch 이름만 신뢰하지 마라.

## 이번 첫 작업

이번 첫 작업은 회사의 기존 작업을 보존하면서 Git-tracked 프로젝트를 exact
final handoff tip으로 동기화하고 인증해 보고하는 것뿐이다.

하지 말아야 할 작업:

- 설계 수정 또는 구현
- 이전 심사·테스트 재실행
- 하위 에이전트 호출
- commit, push, PR, main merge
- reset, clean, 자동 stash, rebase
- F0 내용 또는 개별 filename 접근
- 다음 기술 gate 시작

## 1. 기존 회사 저장소 보존

먼저 기존 저장소의 resolved path, top-level, origin, branch, HEAD, upstream,
tracked/staged/unstaged, untracked/ignored aggregate, stash, local-only commit,
detached 여부와 worktree 목록을 읽기 전용으로 확인한다.

origin은 정확히 다음 repository여야 한다.

`https://github.com/shotgun1107/human-ai-development-tradition.git`

dirty 작업, stash 또는 local-only commit이 하나라도 있으면 switch, reset, clean,
stash, rebase, merge 또는 덮어쓰기를 하지 마라. 기존 작업을 보존하고 exact
handoff tip을 별도 clean worktree에 배치한다. 기존 저장소가 clean할 때만
fetch 후 handoff branch를 exact pinned commit에 맞출 수 있다. 저장소가 이미
있다면 새 clone을 만들지 않는다.

## 2. F0 default-deny 동기화

다음 세 경로군은 Git 동기화 대상이지만 AI 입력이 아니다.

- `s0-lab/control/f0-sealed/**`
- `s0-lab/f0-sealed-staging/**`
- `s0-lab/reviews/f0-sealed/**`

내용, 개별 filename, 답, oracle, 내부 hash 목록을 열람·검색·출력하지 마라.
aggregate count, tracked 상태, quiet diff exit code만 확인한다.

기대값은 `32 / 11 / 10`, 합계 `53`이다.

fetch 후 switch, checkout, worktree materialization보다 먼저 exact target tree의
집계를 확인한다. native Git filename 출력은 캡처해 집계로만 줄인다.

## 3. fetch와 exact pin 검증

읽기 전용 preflight가 통과하면 원격을 한 번 fetch한다. `git pull`은 쓰지 않는다.
사용자 메시지의 exact final handoff commit/tree를 pin해 다음을 검증한다.

- live `codex/home-to-company-handoff-20260812` tip = exact final tip
- final tip tree = 사용자 메시지의 exact final tree
- final tip의 첫 부모 =
  `179dd6f76f2709881900a42dc32cbde8c33c33b0`
- payload parent tree =
  `86bd304b06180c304f0e09ae5ecd0f0d7019e25a`
- `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`가 final tip의 조상
- `f7048e919ab0e698d78ca4ff4cc4eb31ca6f612c`가 final tip의 조상
- `49ecc05dacebf043ed8b2b479eb021018d4b4fe6`,
  `571c8751d0abb8acfb853d402c072fdb7667bde7`,
  `18a9562a9da48ce5743fc183c8c68c15d00cf249`,
  `179dd6f76f2709881900a42dc32cbde8c33c33b0`가 순서대로 final tip의 조상
- target tree F0 aggregate = `32 / 11 / 10`
- payload parent→final tip의 세 F0 quiet diff = `0 / 0 / 0`

하나라도 다르면 움직이는 branch를 임의로 받아들이지 말고 public commit 상태와
aggregate만 보고하고 멈춰라.

## 4. exact tip materialization

기존 회사 저장소가 clean이면 exact pinned commit만 사용해 handoff branch를
tracking 상태로 배치한다. dirty/stash/local-only 상태면 별도 clean worktree를
exact tip에 배치하고 기존 worktree를 건드리지 않는다.

materialization 뒤 다음을 확인한다.

- local HEAD = remote exact handoff tip
- local tree = exact final tree
- status 출력 0
- staged/unstaged diff exit 0
- local F0 aggregate `32 / 11 / 10`
- F0 및 전체 index의 skip-worktree/assume-unchanged 이상 0

## 5. 공개 정본 인증과 읽기

최신 `AGENTS.md`를 처음부터 끝까지 읽은 뒤 canonical validator SelfTest를
실행한다. PASS일 때 다음 문서와 replacement-extension sidecar를 인증해 완독한다.

1. `s0-lab/control/handoffs/home-to-company-2026-08-12/current-state-handoff-v0.1.md`
2. `s0-lab/control/handoffs/home-to-company-2026-08-12/company-local-resume-prompt-v0.1.md`
3. `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.2/public-end-to-end-assembly-rehearsal-design-revision-v0.2.md`
4. `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.2/assembly-rehearsal-interface-map-v0.2.json`
5. `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.2/assembly-rehearsal-acceptance-plan-v0.2.md`
6. `s0-lab/reviews/assembly-rehearsal/public-end-to-end-v0.2/public-end-to-end-assembly-rehearsal-design-v0.2-independent-review-v0.1.md`

v0.2 review SHA-256은 다음과 같다.

`c7b31be05274bb87442550c8a5790e4737d5da7d937d3d7e2f22f6d743bde6fd`

기록된 설계 심사나 byte 재구성을 단순 불신 때문에 다시 실행하지 마라.

## 6. 현재 상태

- v0.1 설계 독립 심사: `REVISE-AND-REVIEW`, blocking 3/major 4
- v0.2 설계 독립 심사: `REVISE-AND-REVIEW`, blocking 0/major 4
- v0.1의 B-01/B-02/B-03/M-01/M-02/M-03: proposal-text 수준에서 CLOSED
- 남은 문제: M-04 failure routing, M-05 Windows/filesystem publication semantics,
  M-06 pending residue consumer rule, M-07 implementation/design/close provenance
- public assembly controller와 rehearsal: 미구현·미실행
- F0, provider/model, executor, judge, scoring, S0/E0: 미접근·미실행

다음 후보 gate는 아래 문구지만 이번 동기화 프롬프트는 열지 않는다.

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN REVISION OPEN`

## 7. 첫 보고 후 정지

과거·현재·미래 순서로 다음을 짧고 쉽게 보고한다.

- 과거: 회사 기존 상태와 보존한 local 작업
- 현재: exact local/remote commit과 tree, clean 여부, F0 aggregate, handoff 및
  v0.2 문서 인증 결과
- 미래: 남은 네 major와 다음 후보 gate의 제한 범위

보고 후 파일 수정, commit, push, 하위 에이전트, 설계 수정 또는 구현을 시작하지
말고 사용자 지시를 기다려라.
