# 회사 로컬 CONTROL 재개 프롬프트 v0.1

> **HISTORICAL / SUPERSEDED — DO NOT COPY OR EXECUTE.** Preserve this file
> only as historical evidence. Use a current handoff prompt governed by the
> repository-root `AGENTS.md`.

The embedded prompt below is historical evidence and must not be transferred
into a new task.

---

> **STOP — HISTORICAL / SUPERSEDED.** Do not execute any command in this
> embedded prompt. Read the current repository-root `AGENTS.md` and obtain a
> current handoff prompt.

당신은 `human-ai-development-tradition` 프로젝트를 원래 주관하던 회사
로컬의 새 CONTROL 세션이다. 집 로컬에서 완료된 공개 S0 준비 작업을 Git으로
인수하고, 먼저 현재 상태를 보고한 뒤 같은 세션에서 승인된 public design
revision을 이어서 수행한다.

이전 회사 Codex나 집 Codex의 대화 기억, 세션 정체성, 절대경로를 증거로
사용하지 마라. 현재 회사 로컬의 Git 상태, 원격 refs, 저장소 문서와
SHA-256 기록만 근거로 판단하라.

## 1. 저장소와 확인 대상

- repository: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- active baseline: `central-system-v2.1-s0-preparation`
- live-state comparison date: `2026-08-09` KST
- recorded `origin/main`: `93e353ac975c3cb5c948d61609fe4e43c57a0f37`
- v0.2 design branch: `codex/s0-trust-root-role-isolation-design-v02`
- v0.2 design commit: `cb4198f4475881ba5b607517fdbb4f0db6b8ce5d`
- v0.2 review branch: `codex/s0-trust-root-role-isolation-review-v02`
- v0.2 review commit: `7d251f04588babeb180b743c8f6860929997b17c`
- handoff branch: `codex/home-to-company-handoff-20260809`
- intended successor branch: `codex/s0-trust-root-role-isolation-design-v03`

이 SHA들은 강제로 맞춰야 할 값이 아니라 인증할 인수인계 기준점이다. 원격이
이후 정상적으로 갱신됐으면 실제 원격을 우선하고 차이를 보고하라. 프롬프트에
맞추기 위해 reset, force checkout 또는 ref 되돌리기를 하지 마라.

### 1.1 Git으로 전체 프로젝트 트리 받기

회사 PC의 기존 저장소 root에서 먼저 `origin`과 현재 변경 상태를 확인한 뒤
원격 refs를 갱신한다. 다음 상태 변경 명령은 순차적으로 실행하고 각 결과를
확인한 후 다음 명령으로 넘어간다.

인수인계 대상은 handoff Markdown 네 개만이 아니다. 원격 handoff commit이
가리키는 전체 Git-tracked project tree를 받아야 한다. 네 파일만 복사하거나
cherry-pick하지 마라.

```powershell
git remote get-url origin
git status --short --branch --untracked-files=all
git status --short --ignored --untracked-files=all
git fetch origin +refs/heads/main:refs/remotes/origin/main
git fetch origin +refs/heads/codex/home-to-company-handoff-20260809:refs/remotes/origin/codex/home-to-company-handoff-20260809
git fetch origin +refs/heads/codex/s0-trust-root-role-isolation-design-v02:refs/remotes/origin/codex/s0-trust-root-role-isolation-design-v02
git fetch origin +refs/heads/codex/s0-trust-root-role-isolation-review-v02:refs/remotes/origin/codex/s0-trust-root-role-isolation-review-v02
```

fetch 직후 live `main`을 기록점과 비교한다. filename/status 확인은 sealed
내용을 읽는 허가가 아니며, 아래 명령으로 확인한 경로의 내용은 현재 공개
allowlist에 포함된 경우에만 읽는다.

```powershell
git rev-parse refs/remotes/origin/main
git log --oneline --decorate 93e353ac975c3cb5c948d61609fe4e43c57a0f37..refs/remotes/origin/main
git diff --name-status 93e353ac975c3cb5c948d61609fe4e43c57a0f37...refs/remotes/origin/main
git show refs/remotes/origin/main:AGENTS.md
git merge-base refs/remotes/origin/main refs/remotes/origin/codex/home-to-company-handoff-20260809
```

그다음 두 방향의 ancestry를 각각 판정한다. `--is-ancestor`의 exit 0은 참,
exit 1은 거짓이며 명령 실패로 오해하지 않는다.

```powershell
git merge-base --is-ancestor refs/remotes/origin/main refs/remotes/origin/codex/home-to-company-handoff-20260809
git merge-base --is-ancestor refs/remotes/origin/codex/home-to-company-handoff-20260809 refs/remotes/origin/main
```

판정 규칙은 다음과 같다.

- live `main`과 기록점이 같거나 live `main`이 handoff의 조상이면 handoff
  HEAD를 continuation base로 사용할 수 있다.
- handoff가 live `main`의 조상이면 live `main`이 v0.2 design/review와
  handoff 문서를 실제로 포함하는지 확인하고 live `main`을 continuation
  base로 사용한다.
- 어느 방향도 조상이 아니면 두 branch가 갈라진 상태다. 기록점 이후
  `main`의 commits와 changed paths, 특히 `AGENTS.md`, protocol,
  F0/I1/isolation/validator 변경을 첫 보고에 포함한다. handoff tree의 fetch,
  별도 worktree materialization, 전체 tracked-tree 검증과 첫 상태 보고까지는
  계속하되, 그 뒤의 v0.3 continuation을 멈춘다. merge, rebase, cherry-pick,
  새 v0.3 branch/worktree 생성을 하지 말고 사용자에게 기준점 통합 결정을
  요청한다.

현재 worktree가 이미 `codex/home-to-company-handoff-20260809`이고 완전히
깨끗하며, 두 status 검사에서 pull 대상과 충돌할 수 있는 untracked, ignored,
local-only 경로가 전혀 없다고 확인된 경우에만 다음 fast-forward pull을
사용할 수 있다. 조금이라도 불명확하면 pull하지 않고 아래 별도 worktree
경로를 사용한다.

```powershell
git pull --ff-only origin codex/home-to-company-handoff-20260809
```

다른 branch이거나 변경·미추적 파일이 있으면 그 worktree에 pull, switch,
checkout 또는 merge하지 않는다. 회사에서 승인된 안정적인 새 경로에
handoff 원격 ref의 detached worktree를 만들고 그 worktree를 읽기 전용
용도로만 사용한다. `git worktree add --detach` 자체가 파일 쓰기를 막는
보안 경계라고 주장하지 않는다. `<HANDOFF_PATH>`는 실제 회사 PC에서
확인한 절대경로로 바꾼다. `C:\\tmp`를 기본 경로로 가정하지 않는다.

```powershell
git worktree add --detach "<HANDOFF_PATH>" refs/remotes/origin/codex/home-to-company-handoff-20260809
```

handoff worktree를 만든 직후 전체 tracked tree 수신을 검증한다. 아래 명령은
`<HANDOFF_PATH>`를 실제 경로로 바꿔 각각 실행한다.

```powershell
git -C "<HANDOFF_PATH>" sparse-checkout disable
git -C "<HANDOFF_PATH>" rev-parse HEAD
git -C "<HANDOFF_PATH>" rev-parse 'HEAD^{tree}'
git -C "<HANDOFF_PATH>" diff --exit-code HEAD --
git -C "<HANDOFF_PATH>" diff --cached --exit-code HEAD --
git -C "<HANDOFF_PATH>" status --porcelain=v2 --untracked-files=all
git -C "<HANDOFF_PATH>" ls-files -t
git -C "<HANDOFF_PATH>" ls-files --others --exclude-standard
git -C "<HANDOFF_PATH>" ls-files --others --ignored --exclude-standard
git -C "<HANDOFF_PATH>" config --show-origin --get-regexp "^(core\.(autocrlf|eol|symlinks|filemode)|filter\.)"
```

첫 SHA는 fetch한 handoff ref의 exact commit과 같아야 한다. tree SHA는 같은
commit에서 읽은 tree와 같아야 한다. 두 diff는 exit 0이어야 하며 tracked
변경이 없어야 한다. `ls-files -t`에는 `S `로 시작하는 skip-worktree entry가
없어야 한다. untracked 또는 ignored 출력이 있으면 경로만 보고하고 삭제·
이동하지 않는다. checkout 설정은 집에서 확인된 `core.autocrlf=true`,
`core.symlinks=false`, `core.filemode=false` 및 system Git LFS filter와
비교해 차이를 보고하되 임의로 설정을 변경하지 않는다.

commit/tree/index 동일성은 모든 tracked path, blob, Git mode와 symlink
entry의 공식 동일성을 보장한다. 그러나 `git diff`는 checkout filter와
line-ending 정규화를 적용할 수 있으므로 물리 working-tree bytes/type까지
항상 같은지를 단독으로 증명하지 않는다. 이 둘을 구분해 보고한다.

Git은 empty directory, `.git` 내부, virtual environment, cache,
untracked/ignored 파일 또는 회사 전용 sealed 자료를 동기화하지 않는다.
회사 전용 자료가 기존 worktree에 있으면 그대로 보존하고, 새 handoff
worktree의 commit tree를 공식 프로젝트 동일성 기준으로 사용한다.

그 worktree에서 아래 두 파일과 sidecar를 먼저 읽고 인증한다.

```text
s0-lab/control/handoffs/home-to-company-2026-08-09/current-state-handoff-v0.1.md
s0-lab/control/handoffs/home-to-company-2026-08-09/company-local-resume-prompt-v0.1.md
```

파일이 없거나 remote ref, ancestry 또는 sidecar가 다르면 다른 branch의
비슷한 파일로 대체하지 말고 수신 실패를 보고한다.

## 2. 첫 단계: 회사 로컬 상태를 읽기 전용으로 보고

저장소가 이미 있으면 새 clone을 만들지 말고 기존 저장소를 사용한다. 먼저
다음을 읽기 전용으로 확인한다.

- 실제 repository root
- `origin`
- 현재 branch와 HEAD
- upstream
- `git status --short --branch`
- `git worktree list --porcelain`
- live remote `main`, v0.2 design, v0.2 review, handoff branch SHA
- `7d251f04...`와 handoff branch의 ancestry

로컬 변경 또는 미추적 파일이 하나라도 있으면 사용자 작업으로 간주한다.
`reset --hard`, `clean`, stash, 강제 checkout, 삭제 또는 이동을 하지 마라.
영향받는 경로만 보고하고 그 worktree에서의 후속 변경을 멈춰라. 충돌하지
않는 별도 clean worktree를 안전하게 만들 수 있는지는 그 뒤 판단한다.

회사 PC에만 있는 미추적 sealed 자료가 Git으로 집 PC에 전달되지 않은 것은
정상일 수 있다. 이번 공개 CONTROL 작업에서는 sealed, hidden oracle,
bank, label, condition map, executor output의 존재·Git 추적 여부를 넘어서
내용을 열거나 검색하거나 해시 계산하지 마라.

## 3. 처음부터 끝까지 읽을 최대 공개 입력

먼저 다음 두 문서를 완독한다.

1. `AGENTS.md`
2. `s0-lab/control/handoffs/home-to-company-2026-08-09/current-state-handoff-v0.1.md`

그다음 아래 공개 입력만 읽는다. 같은-basename `.sha256`이 있으면 내용을
신뢰하기 전에 검증한다.

1. `s0-lab/control/s0-protocol-v0.3.md`
2. `s0-lab/control/f0-public/question-contract-v0.14/control-integration-decision-v0.1.md`
3. `s0-lab/control/i1/i1-public-runtime-v02-control-integration-decision-v0.1.md`
4. `s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1.md`
5. `s0-lab/control/isolation/trust-root-role-isolation-v0.1/role-position-isolation-matrix-v0.1.md`
6. `s0-lab/control/isolation/trust-root-role-isolation-v0.1/isolation-acceptance-plan-v0.1.md`
7. `s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-independent-review-brief-v0.1.md`
8. `s0-lab/reviews/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1-independent-review.md`
9. `s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.md`
10. `s0-lab/control/isolation/trust-root-role-isolation-v0.2/identity-authority-matrix-addendum-v0.2.md`
11. `s0-lab/control/isolation/trust-root-role-isolation-v0.2/isolation-acceptance-plan-addendum-v0.2.md`
12. `s0-lab/control/isolation/trust-root-role-isolation-v0.2/review-response-v0.1.md`
13. `s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-independent-review-brief-v0.2.md`
14. `s0-lab/reviews/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-v0.2-independent-review.md`
15. `s0-lab/control/handoffs/home-to-company-2026-08-09/company-local-resume-prompt-v0.1.md`

저장소를 광범위하게 검색하지 말고 manifest가 가리키는 구현 파일, E0 자료,
sealed 경로 또는 unlisted 문서를 단순 참고 목적으로 따라가지 마라.

새 환경에서 canonical public text validator를 처음 사용하기 전에 다음을
실행한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File s0-lab/control/tools/verify-text-artifacts.ps1 -SelfTest
```

SelfTest가 통과한 뒤 허용된 공개 Markdown/sidecar pair만 검증한다. hash,
sidecar, branch 또는 ancestry가 다르면 수정하지 말고 불일치를 보고하라.

## 4. 첫 상태 보고

후속 설계를 시작하기 전에 사용자에게 다음을 간결하게 보고한다.

1. 실제 경로, origin, branch, HEAD, upstream, status와 worktree
2. live remote SHA와 기록된 기준점의 일치 여부
3. 기록점 이후 live `main`의 commits·changed paths와 handoff branch 사이의
   ancestry 판정
4. handoff branch가 v0.2 review commit을 포함하는지
5. handoff worktree의 exact commit/tree/index, sparse/skip-worktree 상태,
   tracked diff, checkout 설정과 untracked/ignored 경로 유무
6. 공개 sidecar 검증 결과
7. `main`에 통합된 E0 v0.4 설계, F0 v0.14, I1 v0.2와 아직 `main` 밖인
   trust-root/role-isolation v0.2의 구분
8. v0.2 독립 심사의 `REVISE-AND-REVIEW`, `TRI2-M01`, `TRI2-m01`
9. 구현·실행되지 않은 범위

보고가 끝나고 hash가 일치하며, live `main`과 handoff가 위 ancestry 규칙으로
하나의 안전한 continuation base를 제공하고, clean 작업공간을 확보할 수
있으면 추가 승인 대기 없이 아래 공개 설계 수정으로 이어서 진행한다. 둘이
갈라졌으면 이 자동 continuation은 적용되지 않는다. 이 프롬프트는 위 조건을
충족한 design-only continuation만 사용자로부터 위임받은 지시다.

```text
S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN
```

## 5. 이어서 수행할 v0.3 설계 수정

위 ancestry 규칙으로 선택한 exact continuation base에서
`codex/s0-trust-root-role-isolation-design-v03`과 별도 clean worktree를
만든다. live `main`과 handoff가 갈라졌으면 만들지 않는다. 회사 로컬의
기존 작업 트리, v0.2 design branch 또는 과거 세션을 재사용해 덮어쓰지
않는다. worktree는 편집 충돌 격리이며 비밀 보안 경계가 아니다.

기존 v0.1/v0.2 문서와 sidecar를 수정하지 않는다. 새 출력은
`s0-lab/control/isolation/trust-root-role-isolation-v0.3/` 아래의 public
successor 문서와 same-basename sidecar로 제한한다. 최소 패키지는 다음과
같다.

- `trust-root-role-isolation-design-revision-v0.3.md`
- `identity-authority-matrix-addendum-v0.3.md`
- `isolation-acceptance-plan-addendum-v0.3.md`
- `review-response-v0.2.md`
- `trust-root-role-isolation-independent-review-brief-v0.3.md`

정확히 두 finding만 폐쇄한다.

### `TRI2-M01`

preactivation-context, registry-binding, activation-binding import 각각에
canonical host-observable outcome 경로를 정의한다. campaign, ceremony,
signer, import class, from/to state, package/admission hash, capability,
before/after appliance state, decision과 signer-media events를 결박하고,
success, parse rejection, crash, missing outcome, duplicate와 host/appliance
disagreement를 fail-closed로 구분한다. 결과의 TCB/signature authority,
bounded bytes, persistence와 cleanup을 명확히 한다. 새 experimental role,
store, reader 또는 edge를 임의로 만들지 않는다.

### `TRI2-m01`

RFC 9381 section 5.4.5가 `bad_y2`와 네 encoding의 실제 출처라는 주장을
제거한다. 검증 가능한 derivation과 exact 32-byte encoding을 제시하거나
실제로 그 값을 제공하는 공식 primary source를 인용한다. strict
order-L predicate와 future independent construction/order check는 유지한다.

## 6. 반드시 보존할 불변식

- 32 aggregated role rows
- 40 role positions
- 8 paired rows
- 21 experimental section-4 signers와 non-row root 1개
- registry ID 22개
- store 27개
- explicit reader 46개
- edge row 64개
- A-D의 동일 source information, authority, model condition, time, output와
  scoring opportunity
- 세 exclusive signature scope
- closed provider, implementation, protected-material, E0와 S0 게이트

다음을 하지 마라.

- 구현 코드, validator, helper script 또는 acceptance-test harness 작성
- VM/sandbox/account/network/clipboard/Git 차단 구성
- key, anchor, registry, signature 또는 crypto vector 실행
- fixture, bank, label, oracle, condition map 또는 executor 생성
- provider/model 호출, 공홈 Pro 심사, 채점 또는 통계
- E0 후속 작업
- `main` merge
- 독립 심사 수행

작성자 측 bounded QA가 필요하면 공개 allowlist만 가진 하위 에이전트를 사용할
수 있지만 그 결과는 독립 심사 증거가 아니다. v0.3 독립 심사는 문서 동결과
사용자의 별도 정확한 review gate 이후 fresh reviewer가 수행한다.

## 7. 종료와 Git 보존

v0.3 문서와 sidecar를 canonical validator로 검증하고 exact change set을
확인한 뒤 다음을 보고한다.

- 실제 수정 내용과 두 finding의 폐쇄 방식
- 남은 blocker/major/minor 가능성
- 검증 결과와 output hashes
- 구현이나 acceptance test를 실행하지 않았다는 사실

commit과 push는 실질 설계 작업으로 계산하지 않지만 사용자의 별도 승인을
받아야 한다. 승인을 요청할 때 repository, branch, 공개 파일 범위와
commit/push 여부를 눈에 띄게 표시하되 보안 코드나 별도 승인 문구를 만들지
마라. PR과 `main` merge는 요청하지 않은 이상 수행하지 마라.

---
