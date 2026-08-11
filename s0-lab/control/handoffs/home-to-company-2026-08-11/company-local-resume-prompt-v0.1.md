# 회사 PC CONTROL 재개 프롬프트 v0.1

당신은 `human-ai-development-tradition` 프로젝트를 회사 PC에서 이어받는 기존
CONTROL 작업이다. 새 프로젝트 설명, 새 clone 또는 기초 설치를 처음부터
반복하지 마라. 과거 대화 기억은 보조 정보로만 사용하고 현재 Git 상태와 인증된
저장소 기록을 정본으로 삼아라.

repository:

`https://github.com/shotgun1107/human-ai-development-tradition.git`

집→회사 handoff branch:

`codex/home-to-company-handoff-20260811`

handoff payload parent:

`be1d56c0f98dba97919f294c253fc1d8368ef623`

recorded origin/main:

`aa68f797ff4be1175048d8329f98d3c469dfb904`

정확한 handoff tip은 이 프롬프트를 전달한 채팅의 값으로 검증한다. branch 이름만
신뢰하지 마라. 채팅에 exact tip이 없거나 live remote tip과 다르면 중단하고
사용자에게 보고하라.

## 1. 기존 회사 저장소 보존

먼저 기존 저장소의 path, origin, branch, HEAD, upstream, tracked/staged/untracked/
ignored 상태, stash, local-only commit과 worktree 목록을 읽기 전용으로 확인하라.

기존 작업이 dirty이거나 stash/local-only commit이 있으면 switch, reset, clean,
stash, rebase, merge 또는 덮어쓰기를 하지 마라. 기존 작업을 보존하고 exact
handoff tip을 별도 clean worktree에 배치하라. clean이면 fetch 후 exact tip을
pin해 동기화할 수 있다. 새 clone은 만들지 않는다.

## 2. F0 default-deny

다음 세 경로군은 Git에 반드시 존재해야 하지만 AI 입력은 아니다.

- `s0-lab/control/f0-sealed/**`
- `s0-lab/f0-sealed-staging/**`
- `s0-lab/reviews/f0-sealed/**`

내부 파일명이나 내용을 출력·열람·검색하지 마라. 상위 경로별 aggregate count,
tracked 상태, quiet diff와 supplied hash만 확인한다. 기대값은 `32/11/10`, 합계
`53`이다. 동기화나 공개 Git 존재는 내용 접근 권한을 열지 않는다.

## 3. exact Git 검증

fetch 후 다음을 확인하라.

- live handoff branch tip = 채팅으로 전달된 exact handoff tip
- handoff tip의 첫 부모 =
  `be1d56c0f98dba97919f294c253fc1d8368ef623`
- payload parent tree =
  `78541d25d6fb80fbe2738336674d49e375de0610`
- payload parent의 I2 implementation manifest SHA-256 =
  `39386244bba397a1354204b7735508603b3071ef8884f60391beefabc6b21a24`
- payload parent의 I2 contract SHA-256 =
  `d7d1e877d618508ffcd0f4148d5a8fd0137c2ae4fdca5267fd40e9164c15cd15`
- current `origin/main`을 다시 확인하고 기록값
  `aa68f797ff4be1175048d8329f98d3c469dfb904`와 다르면 실제 원격을 우선해 보고
- 최종 status와 staged/unstaged diff가 clean

## 4. 인증해 읽을 공개 문서

동기화 후 최신 `AGENTS.md`를 처음부터 끝까지 읽는다. canonical validator
`-SelfTest`를 실행한 뒤 다음 두 handoff Markdown과 replacement-extension
sidecar를 검증해 완독한다.

1. `s0-lab/control/handoffs/home-to-company-2026-08-11/current-state-handoff-v0.1.md`
2. `s0-lab/control/handoffs/home-to-company-2026-08-11/company-local-resume-prompt-v0.1.md`

그다음 공개 I2 v0.3 후보에 대해 다음 명령을 실행한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File s0-lab/i2/tools/verify-i2.ps1 `
  -ExpectedManifestSha256 39386244bba397a1354204b7735508603b3071ef8884f60391beefabc6b21a24
```

기대 결과는 unit tests `37/37 PASS`, static/source/CLI/import/final stability PASS,
closed boundaries `BLOCKED_NOT_EXECUTED`다. 이것은 공개 construction 검증이며
실제 role isolation이나 S0 성공이 아니다.

## 5. 현재 상태와 종료 조건

- I2 v0.2 공개 구현 후보: 작성 및 독립 심사 완료, verdict `REVISE-AND-REVIEW`
- I2 v0.3 공개 수정 후보: 작성자 검증 완료, fresh independent review 전
- `origin/main`: I2 계보 미통합
- 실제 key, registry, VM/Sandbox, provider/model, sealed bank, oracle, executor,
  judge, S0/E0: 미구현·미실행

동기화와 인증 결과를 과거·현재·미래 순서로 짧게 보고한 뒤 멈춰라. 다음 기술
작업은 사용자가 아래 exact gate를 별도로 열 때만 시작한다.

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.3 INDEPENDENT REVIEW OPEN`

이번 첫 재개 작업에서는 구현 수정, 독립 심사 시작, 하위 에이전트 호출, commit,
push, PR 또는 main 병합을 하지 마라.
