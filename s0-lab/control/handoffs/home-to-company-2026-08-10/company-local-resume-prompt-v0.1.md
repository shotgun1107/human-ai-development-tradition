# 회사 로컬 CONTROL 재개 프롬프트 v0.1

아래 구분선 사이의 내용을 회사 PC의 새 Codex CONTROL 세션 첫 메시지로
그대로 전달한다.

---

당신은 `human-ai-development-tradition` 프로젝트를 원래 주관하던 회사 PC의
새 CONTROL 세션이다. 집 PC가 회사 Git 정본을 인수하고 기존 집 저장소를
in-place 동기화한 결과를 다시 회사 로컬로 인수하라.

이전 집·회사 Codex의 대화 기억, 요약, 절대경로 또는 세션 정체성을 증거로
사용하지 마라. 현재 회사 PC의 Git 상태, live remote refs, 저장소의 공개
인수인계 문서와 SHA-256 기록만 근거로 판단하라.

이번 첫 작업은 동기화, 동일성 검증과 상태 보고뿐이다. 구현, 테스트, 하위
에이전트, 문서 수정, commit, push, PR, merge 또는 다음 기술 게이트를
시작하지 마라. 첫 보고 후 멈추고 사용자 지시를 기다려라.

## 1. 정본과 인수 기준

- repository:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`
- 회사 정본 branch:
  `codex/s0-order-eight-public-vector-independent-verification-v02`
- 확인된 정본 HEAD:
  `b857545113058321dd4d65f601c2d5ad8cceeec0`
- 확인된 정본 tree:
  `655bea08eb117a565bccc9241fb3361ce3c8f1d8`
- 필수 payload commit:
  `85ad19ba6703f43b1209a13164d1e28a4b62f6a4`
- 기록된 `origin/main`:
  `5add6e5e1675793ad179e98e51ffa1515feb3db8`
- 집→회사 handoff branch:
  `codex/home-to-company-handoff-20260810`
- 활성 기준선: `central-system-v2.1-s0-preparation`

이 값들은 인증할 기준점이지 강제로 맞출 목표가 아니다. 원격이 정상적으로
전진했으면 실제 live refs를 우선하고 차이를 보고한다. reset, force checkout,
rebase 또는 merge로 프롬프트의 SHA에 맞추지 마라.

## 2. F0-SEALED 절대 경계

다음 tracked 경로는 시험 문제·답지 관련 default-deny F0-SEALED 자료다.

- `s0-lab/control/f0-sealed/**`
- `s0-lab/f0-sealed-staging/**`
- `s0-lab/reviews/f0-sealed/**`

이번 CONTROL은 경로별 tracked file count만 확인할 수 있다. 내용, filename
목록, hash, 정답, oracle, 내부 구조를 열거나 검색하거나 요약하거나 다른
세션에 전달하지 마라. Git에 존재한다는 사실, private repository, clone,
worktree 또는 synchronization 역할은 입력 허가가 아니다. 정확한 sealed
gate와 role allowlist가 없으면 접근하지 않는다.

기대 수량은 각각 32, 11, 10이며 합계 53이다. 수량이 다르면 내용을 열지
말고 수신 불일치만 보고한다.

## 3. 회사 기존 저장소를 먼저 감사

새 clone을 만들기 전에 기존 회사 저장소에서 다음을 읽기 전용으로 확인한다.

```powershell
Get-Location
git remote get-url origin
git branch --show-current
git rev-parse HEAD
git status --short --branch --untracked-files=all
git status --short --ignored --untracked-files=all
git stash list
git worktree list --porcelain
git log --oneline --branches --not --remotes
```

origin이 다르거나 detached HEAD이면 변경하지 말고 보고한다. modified,
staged, untracked, ignored, stash 또는 원격에 없는 local-only commit이 있으면
사용자 작업으로 간주한다. pull, switch, checkout, reset, clean, stash,
rebase, merge, 삭제 또는 덮어쓰기를 하지 말고 영향 경로만 보고한다.

기존 저장소가 clean하고 origin이 일치할 때만 다음 단계로 간다.

## 4. 전체 원격 branch 동기화

원격 상태 변경 명령은 하나씩 실행하고 결과를 확인한 뒤 다음으로 간다.

```powershell
git fetch --prune origin "+refs/heads/*:refs/remotes/origin/*"
git rev-parse refs/remotes/origin/main
git rev-parse refs/remotes/origin/codex/s0-order-eight-public-vector-independent-verification-v02
git rev-parse refs/remotes/origin/codex/home-to-company-handoff-20260810
git cat-file -t 85ad19ba6703f43b1209a13164d1e28a4b62f6a4
git merge-base --is-ancestor 85ad19ba6703f43b1209a13164d1e28a4b62f6a4 refs/remotes/origin/codex/home-to-company-handoff-20260810
git merge-base --is-ancestor b857545113058321dd4d65f601c2d5ad8cceeec0 refs/remotes/origin/codex/home-to-company-handoff-20260810
git rev-parse "b857545113058321dd4d65f601c2d5ad8cceeec0^{tree}"
```

payload type은 `commit`, 두 ancestry 명령은 exit 0, 마지막 tree는
`655bea08eb117a565bccc9241fb3361ce3c8f1d8`이어야 한다. 다르면 임의로
다른 branch를 선택하거나 수정하지 말고 실제 값을 보고한 뒤 멈춘다.

기존 worktree가 완전히 clean하면 handoff branch를 local tracking branch로
전환하거나 기존 branch를 fast-forward한다.

local branch가 없을 때:

```powershell
git switch --track origin/codex/home-to-company-handoff-20260810
```

local branch가 이미 있고 divergence가 없을 때:

```powershell
git switch codex/home-to-company-handoff-20260810
git pull --ff-only origin codex/home-to-company-handoff-20260810
```

단순 `pull`로 현재 다른 branch에 handoff를 merge하지 마라. 기존 worktree가
dirty하면 in-place 동기화를 수행하지 말고 첫 상태만 보고한다.

## 5. 수신 동일성 검증

선택한 handoff worktree에서 다음을 각각 확인한다.

```powershell
git rev-parse HEAD
git rev-parse "HEAD^{tree}"
git rev-parse refs/remotes/origin/codex/home-to-company-handoff-20260810
git status --porcelain=v1
git diff --exit-code HEAD --
git diff --cached --exit-code HEAD --
git ls-files -t
```

local HEAD와 remote handoff tip이 같고 status가 비어 있으며 두 diff가 exit 0,
skip-worktree entry가 없어야 한다. Git tree 동일성은 대화, `.git`, cache,
`.venv`, OS 설정과 untracked/ignored 파일까지 두 PC가 같다는 의미가 아니다.

sealed 수량은 내용이나 filename을 출력하지 않고 count만 확인한다.

```powershell
@(git ls-files -- "s0-lab/control/f0-sealed").Count
@(git ls-files -- "s0-lab/f0-sealed-staging").Count
@(git ls-files -- "s0-lab/reviews/f0-sealed").Count
```

## 6. 처음부터 끝까지 읽을 공개 입력

새 환경에서 가장 먼저 `AGENTS.md`를 완독한다. 이어서 아래 두 파일과
same-basename sidecar만 인증하고 완독한다.

1. `s0-lab/control/handoffs/home-to-company-2026-08-10/current-state-handoff-v0.1.md`
2. `s0-lab/control/handoffs/home-to-company-2026-08-10/company-local-resume-prompt-v0.1.md`

canonical validator를 사용하기 전에 다음 SelfTest를 실행한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File s0-lab/control/tools/verify-text-artifacts.ps1 -SelfTest
```

그 뒤 위 공개 pair만 검증한다. 이번 첫 작업에서는 sealed 경로, order-eight
후보 계산 설명 또는 다른 문서를 추가로 읽지 마라.

## 7. 첫 상태 보고

사용자에게 다음을 간결하게 보고한다.

1. 회사 저장소의 실제 path, origin, 최초 branch/HEAD, upstream과 worktree
2. modified, staged, untracked, ignored, stash와 local-only commit 여부
3. 사용한 동기화 방식과 모든 live remote SHA
4. handoff가 `b857545...`와 payload `85ad19b...`를 포함하는지
5. local/remote HEAD, tree, status와 diff 결과
6. 최신 `AGENTS.md` 적용 여부
7. F0-SEALED가 32/11/10개 존재하지만 내용을 열지 않았다는 사실
8. 집 PC에서는 정본 동기화와 이 handoff 문서 작성 외 기술 작업을 하지
   않았다는 사실

보고 후 멈춘다. 다음 후보는 아래 boundary revision이지만 이 프롬프트는
게이트를 열지 않는다.

```text
S0 V0.14 ORDER-EIGHT PUBLIC VECTOR REVIEW INPUT BOUNDARY REVISION OPEN
```

사용자가 정확한 다음 게이트를 별도로 입력하기 전에는 boundary revision,
독립 검증, 벡터 동결, 구현, sealed 입력, 모델 실행 또는 `main` 병합을
시작하지 마라.

---
