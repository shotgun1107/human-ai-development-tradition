# 집 PC CONTROL 동기화 시작 프롬프트 v0.1

당신은 `human-ai-development-tradition` 프로젝트를 회사 PC에서 집 PC로
동기화해 이어받는 기존 CONTROL 작업이다.

새 프로젝트 설명이나 기초 설치를 처음부터 반복하지 마라. 과거 대화는 증거로
사용하지 말고 현재 Git 정본, 최신 root `AGENTS.md`, 인증된 handoff 기록만
증거로 사용하라.

## 정본 식별자

- repository:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`
- 회사→집 handoff branch:
  `codex/company-to-home-handoff-20260813`
- handoff payload parent:
  `a34e54b0ac8fbfa4c42ffced5dcd2ac15016f0e3`
- payload parent tree:
  `454186959ec5f929f25d9bd4f48be4fd3023f33f`
- source feature branch:
  `codex/s0-public-assembly-rehearsal-implementation-v01`
- recorded origin/main:
  `41e0b684a7cca387be6d264c4a5b63de2561fd7c`
- origin/main tree:
  `a14e8b9c9bc8905060cd8811e8934643e2aa4aa3`
- runtime/preloader v0.3 package manifest SHA-256:
  `c2ecd2931e15a99b68d3e669026342f59a42995268f8b4937ba96e63d731481b`

exact final handoff commit과 tree는 이 프롬프트를 전달하는 사용자 메시지에 적힌
값을 사용한다. 이 파일이 자기 자신의 final commit hash를 안다고 가정하지 마라.

## 이번 첫 작업의 범위

집의 기존 작업을 보존하면서 Git-tracked 프로젝트를 exact final handoff tip으로
동기화하고 인증한 뒤, 과거·현재·미래 순서로 상태를 보고하고 멈춰라.

이번 첫 작업에서 다음을 하지 마라.

- 구현·설계·문서 수정;
- 테스트 재실행 또는 추가 감사;
- subagent/하위 에이전트 호출;
- 새 commit, push, PR, main merge;
- reset, clean, 자동 stash, rebase;
- F0 내용 또는 개별 filename 접근;
- 다음 기술 gate 시작.

## 1. 집의 기존 작업 보존 확인

기존 저장소에서 먼저 다음을 읽기 전용으로 확인하라.

- resolved repository path와 top-level;
- origin URL;
- branch, HEAD, upstream, detached 여부;
- staged, unstaged, untracked, ignored aggregate;
- stash와 local-only commit;
- worktree 목록.

origin은 반드시 아래 repository를 가리켜야 한다.

`https://github.com/shotgun1107/human-ai-development-tradition.git`

다른 repository라면 아무것도 변경하지 말고 보고 후 멈춰라.

dirty 작업, stash 또는 local-only commit이 있으면 기존 worktree를 switch,
reset, clean, stash, rebase, merge하지 마라. 기존 작업을 그대로 두고 exact
handoff tip을 별도 clean worktree에 배치하라. 완전히 clean할 때만 기존
worktree를 handoff branch로 전환할 수 있다. 새 clone은 기존 저장소가 실제로
없을 때만 허용한다.

## 2. F0 동기화 경계

다음 세 경로군은 Git 동기화 대상이지만 AI 입력은 default-deny다.

- `s0-lab/control/f0-sealed/**`
- `s0-lab/f0-sealed-staging/**`
- `s0-lab/reviews/f0-sealed/**`

내용, 개별 filename, hash 목록, 답, oracle 또는 내부 구조를 열람·검색·출력하지
마라. aggregate tracked count, quiet diff exit code, 승인된 aggregate만 확인하라.

기대값:

- `32 / 11 / 10`
- total `53`

fetch 뒤 어떤 switch, checkout, merge 또는 worktree materialization보다 먼저
exact pinned target tree의 aggregate를 확인하라. native Git stdout은 filename이
나오지 않도록 캡처해 aggregate로 줄이고, 실패 exit code를 즉시 보존하라.

## 3. fetch와 exact pin 검증

보존 preflight가 통과하면 origin을 한 번 fetch하라. `git pull`은 사용하지 마라.
사용자가 전달한 exact final handoff commit을 pin하고 다음을 검증하라.

- live remote `codex/company-to-home-handoff-20260813` tip = exact final tip;
- final tip tree = 사용자가 전달한 exact final tree;
- final tip의 유일한 첫 부모 =
  `a34e54b0ac8fbfa4c42ffced5dcd2ac15016f0e3`;
- payload parent tree =
  `454186959ec5f929f25d9bd4f48be4fd3023f33f`;
- `41e0b684a7cca387be6d264c4a5b63de2561fd7c`가 final tip의 조상;
- `da4ad3af483652bd755deff9d024a9833c177d39`가 final tip의 조상;
- `ce62b7ef3f819e182a6f68e2a50eed6ec76d56e4`가 final tip의 조상;
- `a34e54b0ac8fbfa4c42ffced5dcd2ac15016f0e3`가 final tip의 조상;
- exact target F0 aggregate = `32 / 11 / 10`;
- payload parent→final tip의 세 F0 quiet diff = `0 / 0 / 0`.

하나라도 다르면 branch 이름이나 임의의 최신값을 받아들이지 말고 실제 public
commit 및 aggregate 상태만 보고한 뒤 멈춰라.

## 4. exact tip materialization

기존 저장소가 clean이면 exact pinned commit만 사용해 handoff branch를 tracking
branch 또는 fast-forward로 배치하라. fetch가 포함된 `git pull`은 쓰지 마라.

기존 저장소가 dirty, stash, local-only 상태면 별도 clean worktree를 exact
pinned commit에 배치하라. 기존 worktree의 branch, index, working files를
건드리지 마라.

materialization 후 다음을 확인하라.

- local HEAD = remote exact handoff tip;
- local tree = exact handoff tree;
- branch/upstream 또는 detached pinned worktree 관계가 의도와 일치;
- status 출력 0;
- staged diff와 unstaged diff exit 0;
- local F0 aggregate `32 / 11 / 10`;
- skip-worktree와 assume-unchanged aggregate가 허용 상태;
- 기존 집 작업의 손실·변경 없음.

## 5. 공개 정본 인증과 읽기

최신 root `AGENTS.md`를 처음부터 끝까지 읽어라. 그 지시를 적용한 뒤 canonical
text-artifact validator를 읽고 SelfTest를 실행하라.

SelfTest가 PASS일 때만 다음 두 Markdown/sidecar pair를 검증하고 완독하라.

1. `s0-lab/control/handoffs/company-to-home-2026-08-13/current-state-handoff-v0.1.md`
2. `s0-lab/control/handoffs/company-to-home-2026-08-13/home-local-resume-prompt-v0.1.md`

그다음 v0.3 design package manifest SHA-256을 재현하라.

`c2ecd2931e15a99b68d3e669026342f59a42995268f8b4937ba96e63d731481b`

기록된 과거 심사나 테스트를 단순 불신 때문에 다시 실행하지 마라. 구현 source,
test, F0 또는 다른 repository 경로로 범위를 넓히지 마라.

## 6. 현재 기술 상태

- origin/main `41e0b684...`: v0.5 assembly rehearsal 설계 main 통합 완료;
- 공개 assembly candidate: 기능 브랜치에 존재하지만 공식 rehearsal 미실행;
- runtime/preloader v0.1: 독립 재심사에서 수정 요구;
- runtime/preloader v0.2: 재심사 `MAJOR 2 / MINOR 1`;
- runtime/preloader v0.3: 세 finding을 설계 수준에서 보완, fresh 독립 재심사
  대기;
- native guard, `NtCreateFile` preloader, runtime-profile materialization,
  platform probe: 미구현·미검증;
- F0, oracle, executor, judge, provider/model, S0/E0: 미실행.

다음 후보 gate는 아래 문구지만 이번 동기화 프롬프트는 이를 열지 않는다.

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.3 INDEPENDENT REREVIEW OPEN`

## 7. 첫 보고 후 정지

다음을 짧고 읽기 쉽게 과거·현재·미래 순서로 보고하라.

- 과거: 집의 기존 branch/HEAD와 보존해야 했던 local 상태;
- 현재: final local/remote commit과 tree 일치, clean 여부, F0 aggregate,
  handoff pair 및 validator 결과;
- 미래: v0.3 독립 설계 재심사가 다음 후보이며 구현 gate가 아니라는 점.

보고 후 아무 파일도 만들거나 수정하지 말고 사용자 지시를 기다려라.
