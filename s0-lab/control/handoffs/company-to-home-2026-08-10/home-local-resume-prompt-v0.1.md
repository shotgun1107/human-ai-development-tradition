# 집 로컬 CONTROL 재개 프롬프트 v0.1

아래 구분선 사이의 내용을 집 PC의 새 Codex CONTROL 세션 첫 메시지로 그대로
전달한다.

---

당신은 `human-ai-development-tradition` 프로젝트를 집 PC에서 이어받는 새
CONTROL 세션이다. 회사 PC가 공개 Git 계보에서 수행한 `main` 반영, 공개
order-eight 벡터 준비와 두 번째 독립 검증 실패를 Git 정본으로 인수하라.

이전 집·회사 Codex의 대화 기억, 요약, 절대경로와 세션 정체성을 증거로
사용하지 마라. 현재 집 PC의 Git 상태, 원격 refs, 인수인계 문서와 SHA-256만
근거로 판단하라.

이번 첫 세션은 **동기화·동일성 확인·맥락 인수 보고만** 한다. boundary 수정,
독립 검증, 하위 에이전트 호출, 구현, 키 생성, fixture/oracle, E0/S0 실행,
commit, push, PR 또는 `main` 병합을 하지 마라. 보고 후 사용자의 정확한 다음
게이트를 기다려라.

인수 branch에는 유실 방지를 위해 F0-SEALED 53개 파일도 Git 추적돼 있다.
public clone에 존재한다는 이유로 입력 권한이 생기지 않는다. 아래 세 경로는
이번 동기화 역할에서 path/count/tracked state 확인만 허용되며 내용 열기,
검색, hash 외 파생, 요약 또는 다른 세션 전달은 금지한다.

- `s0-lab/control/f0-sealed/**`
- `s0-lab/f0-sealed-staging/**`
- `s0-lab/reviews/f0-sealed/**`

## 1. 정본

- repository: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- handoff branch:
  `codex/s0-order-eight-public-vector-independent-verification-v02`
- recorded approved remote `main`:
  `5add6e5e1675793ad179e98e51ffa1515feb3db8`
- handoff predecessor:
  `daba763e219f597197768769115c01e5ea929c8a`
- active baseline: `central-system-v2.1-s0-preparation`

기록된 SHA에 맞추기 위해 원격이나 로컬을 되돌리지 마라. 먼저 fetch한 실제
원격을 확인하고 차이가 있으면 보고한다.

## 2. 기존 집 작업 보존

집에 저장소가 있으면 먼저 다음을 읽기 전용으로 확인한다.

```powershell
Get-Location
git remote get-url origin
git branch --show-current
git rev-parse HEAD
git status --short
git status -sb
git stash list
git log --oneline --branches --not --remotes
```

origin이 위 URL 또는 그 SSH 등가가 아니면 변경하지 말고 보고 후 멈춰라.
detached HEAD, modified/staged/untracked 파일, stash 또는 local-only commit이
있으면 reset, clean, checkout, switch, stash, rebase, merge 또는 pull하지
마라. 기존 상태를 보존하고 fetch 뒤 별도 clean worktree 방식만 검토한다.

저장소가 전혀 없을 때만 위 handoff branch를 지정해 새 clone을 만들 수 있다.
기초 설치나 `.venv` 구성은 하지 마라.

## 3. 원격 인수

안전 조건을 확인한 뒤 다음 원격 refs를 fetch한다.

```powershell
git fetch origin
git rev-parse origin/main
git rev-parse origin/codex/s0-order-eight-public-vector-independent-verification-v02
git merge-base --is-ancestor origin/main origin/codex/s0-order-eight-public-vector-independent-verification-v02
git rev-list --left-right --count origin/main...origin/codex/s0-order-eight-public-vector-independent-verification-v02
git log --oneline --left-right --decorate origin/main...origin/codex/s0-order-eight-public-vector-independent-verification-v02
```

원격 handoff branch가 없거나 `origin/main`이 그 조상이 아니면 임의로 branch를
선택하거나 병합하지 말고 실제 refs와 commit 목록을 보고한 뒤 멈춰라.

기존 worktree가 완전히 clean하고 local branch가 없으면:

```powershell
git switch --track origin/codex/s0-order-eight-public-vector-independent-verification-v02
```

같은 local branch가 있고 clean하며 divergence가 없으면:

```powershell
git switch codex/s0-order-eight-public-vector-independent-verification-v02
git pull --ff-only origin codex/s0-order-eight-public-vector-independent-verification-v02
```

기존 저장소가 dirty이거나 다른 작업을 보존해야 하면 그 worktree를 건드리지
마라. 실제 집 환경에서 존재하지 않는 안전한 sibling path를 정하고 확인한 뒤
다음을 사용한다.

```powershell
git worktree add --detach "<NEW_HANDOFF_WORKTREE>" origin/codex/s0-order-eight-public-vector-independent-verification-v02
```

worktree는 편집 격리일 뿐 비밀 보안 경계가 아니다. sealed, oracle, 개인·비밀
자료를 공개 handoff worktree에 복사하지 마라.

## 4. 동일성 확인

선택한 인수 경로에서 다음을 확인한다.

```powershell
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git rev-parse origin/codex/s0-order-eight-public-vector-independent-verification-v02
git status --porcelain=v1
git diff --exit-code origin/codex/s0-order-eight-public-vector-independent-verification-v02 -- .
git diff --cached --exit-code HEAD -- .
git ls-files -t
```

local/remote HEAD와 tree가 같고 status가 비어 있으며 두 diff가 성공하고
skip-worktree entry가 없어야 한다. 하나라도 다르면 수정하지 말고 보고한다.
Git tree 동일성은 대화, `.git`, temp, cache, `.venv`, untracked/ignored 파일,
checkout 줄바꿈까지 두 PC가 동일하다는 뜻이 아니다.

F0-SEALED 보존 수량은 내용 없이 별도로 확인한다.

```powershell
@(git ls-tree -r --name-only HEAD -- s0-lab/control/f0-sealed).Count
@(git ls-tree -r --name-only HEAD -- s0-lab/f0-sealed-staging).Count
@(git ls-tree -r --name-only HEAD -- s0-lab/reviews/f0-sealed).Count
```

기대값은 순서대로 32, 11, 10이며 합계 53이다. 다르면 내용을 열지 말고
수신 불완전으로 보고한다.

## 5. 맥락 인수

다음을 순서대로 완독한다. same-basename `.sha256`이 있으면 읽기 전에
인증한다.

1. `AGENTS.md`
2. `s0-lab/control/handoffs/company-to-home-2026-08-10/current-state-handoff-v0.1.md`
3. 이 시작 프롬프트
4. `s0-lab/reviews/isolation/order-eight-public-vector-v0.1/independent-verification-v0.2.md`
5. `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-review-input-boundary-revision-v0.1.md`
6. `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-independent-verification-brief-v0.2.md`

새 환경에서 canonical validator를 신뢰하기 전에 실행한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File s0-lab/control/tools/verify-text-artifacts.ps1 -SelfTest
```

허용된 공개 Markdown/sidecar pair만 검증한다. sealed 경로, unlisted 문서,
후보 벡터 계산 설명을 추가로 검색하지 마라.

## 6. 반드시 이해할 현재 상태

- 회사의 기존 local `main`은 `d88097d...`였고 원격보다 52 commits 뒤였다.
- 그 경로에 세 개의 미추적 F0-sealed 관련 디렉터리가 있어 회사 CONTROL은
  pull/reset/stash하지 않고 별도 clean worktree를 사용했다.
- 사용자 결정에 따라 그 세 경로의 53 files를 인수 branch에 그대로
  보존했다. 새 `AGENTS.md`는 정확한 F0-SEALED gate와 role allowlist 없이는
  AI가 내용을 읽지 못하도록 default-deny한다.
- 승인된 계보의 원격 `main`은 `5add6e5...`다.
- order-eight 벡터 작성과 두 검증 기록은 아직 `main` 밖의 선형 branch다.
- 첫 독립 검증은 독립 숫자 `d` 입력 부족으로 `INVALID-REVIEW`였다.
- 입력 경계를 수정한 뒤의 두 번째 검증도 `INVALID-REVIEW`였다.
- 두 번째 원인은 공식 RFC 실제 LF 원문 103,210 bytes/hash
  `ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3`
  와 문서가 HTTP 원문이라고 선언한 CRLF 변환본 106,573 bytes/hash
  `f13ab006baa1a30a7835113927e9d23ca9d9c460f352e721cbcdff8adbf1dee9`
  의 불일치다.
- fail-closed 처리로 두 번째 reviewer는 RFC slice, 벡터 독립 계산, 후보
  비교를 수행하지 않았다.
- 벡터는 틀렸다고 판정된 것도, 맞다고 검증된 것도 아니며 동결되지 않았다.
- 벡터 최종 동결, 구현, 키 생성, protected material, fixture/oracle,
  provider/model, E0와 S0 gate는 닫혀 있다.

## 7. 첫 보고와 정지

사용자에게 다음을 과거·현재·미래 순서로 쉽게 보고한다.

1. 처음 발견한 집 branch, HEAD, status, stash와 local-only commit
2. 기존 clean branch, 별도 worktree 또는 clone 중 사용한 동기화 방식
3. local/remote commit·tree 동일성, status와 diff
4. `origin/main`과 handoff branch의 ancestry와 commit 차이
5. 회사가 기존 dirty `main`을 보존하고 clean worktree로 작업한 이유
6. order-eight 벡터의 목적과 두 번의 `INVALID-REVIEW`
7. 현재 LF/CRLF 입력 경계 결함과 벡터 미검증·미동결 상태
8. 계속 닫힌 구현·실행 범위
9. F0-SEALED 32/11/10 file count와 default-deny 경계

보고 후 아무 파일도 만들거나 수정하지 말고 사용자의 정확한 다음 게이트를
기다려라. 다음 후보는 아래 문구지만 이 프롬프트가 대신 열지 않는다.

```text
S0 V0.14 ORDER-EIGHT PUBLIC VECTOR REVIEW INPUT BOUNDARY REVISION OPEN
```

`ㄱㄱ`, `계속`, `끝까지 진행` 또는 과거 스레드의 승인을 이 민감한 다음
게이트와 같다고 해석하지 마라.

---
