# 최소 운영규칙 수정 제안

## 목표

다음 상태를 한 번만 읽어도 오해할 수 없게 고정한다.

> 세 F0 경로의 기존 53개 파일은 공개 Git 추적 자료이며 authoritative tree와
> 함께 모든 PC에 동기화된다. 그러나 AI agent는 현재 사용자 메시지의 정확한
> F0 gate와 역할별 allowlist가 동시에 없으면 그 내용을 읽지 않는다.

## 비목표

- 53개 파일이나 세 상위 경로를 rename/delete하지 않는다.
- frozen canonical protocol 의미를 몰래 변경하지 않는다.
- hidden oracle, future canonical execution input 또는 secret을 repository에
  넣도록 허용하지 않는다.
- S0, fixture authoring, executor, judge, provider/model 또는 구현 gate를 열지 않는다.
- 이 제안 자체로 source edit, commit, push, PR, merge를 승인하지 않는다.

## 1. 정본 용어

| 용어 | 정의 | 세 F0 경로 |
|---|---|---|
| `PUBLIC-GIT` | commit/tree에 존재하며 clone/fetch/checkout/pull/push로 운반되는 publication class | **예** |
| `AI-CONTENT-DEFAULT-DENY` | agent가 내용·내부 filename·의미를 task input으로 읽지 못하는 access class | **예** |
| `NONPUBLIC-OUT-OF-REPO` | Git publication 금지 class: hidden oracle, credential, private key, personal/real/secret material, protocol이 별도 지정한 future canonical execution input | **아니오** |
| `ROLE-GATED` | 현재 사용자 gate + 명시된 role allowlist가 있어야 접근 가능한 experimental class | **예** |

규범 문장:

> Publication class와 AI content-access class는 독립이다. `SEALED`라는 경로
> label만으로 Git publication class를 결정하지 않는다.

## 2. root `AGENTS.md` 최소 대체 문구

### 2.1 `AGENTS.md:13-25` 뒤에 추가할 정본 block

```markdown
### Git publication and AI content access are independent

- The three F0-SEALED path families named above are **PUBLIC-GIT / AI-CONTENT-DEFAULT-DENY**.
- Their `SEALED` label is an experimental/role-access label, not a Git privacy or publication label.
- The existing tracked inventory must remain present in every authoritative tree that is intended to synchronize the repository: 32 files under `s0-lab/control/f0-sealed/`, 11 under `s0-lab/f0-sealed-staging/`, and 10 under `s0-lab/reviews/f0-sealed/` (53 total).
- Clone, fetch, checkout, pull, push, branch ancestry, worktree materialization, and unchanged tree preservation do not grant an agent authority to open, search, quote, summarize, derive from, or pass the contents.
- An exact F0 role/read gate grants only the content access and role actions explicitly named by the current user message and role allowlist. It does not by itself authorize commit or push.
- Git publication or handoff approval grants only the stated Git action. It does not by itself authorize content access.
- `NONPUBLIC-OUT-OF-REPO` means hidden oracle, credentials, private keys, personal/real/secret material, and any future canonical execution input that the frozen protocol requires outside the repository. Never commit or push that class. Do not use the bare word `sealed` as a publication decision.
```

### 2.2 `AGENTS.md:46-54`의 handoff/publication block 전체 대체

```markdown
- When preserving, reviewing, transferring, or publishing completed public work would materially benefit from a branch, commit, or push, request or use Git approval exactly as specified below. Git approval and AI content-read authority are separate.
- For an ordinary commit or push approval request, state the exact repository, branch, staged change scope, and requested Git action. An unambiguous reply such as `ㄱㄱ`, `승인`, or `푸시해` is sufficient after that clear request.
- When the user explicitly requests a cross-PC or cross-session handoff package, that request authorizes commit and push of the completed public handoff-only **changes** to a dedicated handoff branch after exact staged-scope verification. The branch must preserve the inherited PUBLIC-GIT tree, including the unchanged 32/11/10 F0 inventory; that inherited presence is required synchronization, not a forbidden content read or an extra handoff change.
- Never commit or push `NONPUBLIC-OUT-OF-REPO` material. Existing or future approved bytes under the three PUBLIC-GIT F0 path families are not excluded merely because their path label contains `sealed`; modifying their contents still requires the exact role gate and a separate applicable Git approval.
- No ordinary or handoff Git approval authorizes a PR, release, `main` merge, history rewrite, deletion, or AI content read unless those actions are separately explicit.
```

### 2.3 root precedence block 추가

```markdown
### Current-policy precedence

- Platform instructions and the current user task remain authoritative.
- For repository-local interpretation, this root `AGENTS.md` controls current Git publication/synchronization classification.
- A current role prompt may narrow allowed inputs and actions, but it may not silently reclassify the three PUBLIC-GIT F0 path families as Git-private.
- Frozen protocol text controls experimental protocol semantics, including future canonical execution-input storage; it does not reclassify the existing three PUBLIC-GIT preservation path families.
- Dated README, HOME, handoff, resume, work-report, and review documents are historical evidence unless the current user message explicitly designates one. Historical text never overrides current tracked state or this publication/access mapping.
- If two current documents still conflict, stop before reading denied content or changing Git state and report the exact public clauses.
```

## 3. onboarding과 handoff 최소 patch

### 반드시 수정할 공개 파일

| 파일 | 최소 변경 |
|---|---|
| `README.md:9` | `AGENTS.md`의 current two-axis policy를 먼저 읽게 하고 `HOME-CODEX-START.md`는 역사적 context라고 표시 |
| `HOME-CODEX-START.md:1-9` | `SUPERSEDED FOR CURRENT GIT SYNC POLICY` banner와 current policy pointer 추가 |
| `HOME-CODEX-START.md:35,41-46` | 2026-08-07 당시 untracked였다는 역사와 현재 53개 PUBLIC-GIT 상태를 둘 다 명시; bare sealed를 `uncommitted NONPUBLIC-OUT-OF-REPO`로 교체 |
| company→home 2026-08-10 current `:102-104` | “봉인 전체 제외”를 “NONPUBLIC-OUT-OF-REPO만 제외; tracked 53의 normal checkout 보존”으로 교체 |
| 같은 문서 `:268-269` | manual copy 금지 대상을 NONPUBLIC class로 한정; normal checkout의 53은 유지 |
| company→home companion prompt `:114-115` | 같은 교정 |
| home→company 2026-08-10 current `:75-80` | handoff auto-push 제외 대상을 NONPUBLIC class로 한정 |
| 두 2026-08-09 handoff/resume 문서 상단 | `HISTORICAL/SUPERSEDED — old local-only state; not current publication policy` banner 추가; 역사 문장 자체는 보존 |

### 권장하지만 2차로 미룰 수 있는 정리

- `docs/tradition/s0-isolated-design-execution-and-judgment-plan.md:53-60`에
  historical snapshot banner 추가
- `s0-lab/README.md:3-6,51,71`에서 `closed`는 authoring/execution gate이고
  current Git inventory absence를 뜻하지 않는다고 한 문장 추가
- I0/boundary 문서에 나오는 `sealed input/fixture`가 task-scoped future execution
  artifact를 뜻하며 세 PUBLIC-GIT preservation path 전체를 뜻하지 않는다는
  root cross-reference 추가

### frozen protocol 처리

`s0-protocol-v0.3-canonical-r1.md:353-363`은 이 운영정책 patch에서 수정하지
않는다. 그 문서가 outside-repo로 지정한 future canonical input은 계속
`NONPUBLIC-OUT-OF-REPO`다. root mapping만 다음을 분명히 한다.

> “Protocol canonical execution input”과 “경로명이 F0-SEALED인 기존 공개 Git
> preservation artifacts”는 동일 class가 아니다.

protocol 자체의 storage 의미를 바꾸려면 별도 protocol gate/refreeze가 필요하다.

## 4. 안전한 동기화 하네스

### 금지할 command 형태

- agent-visible broad `git diff` 또는 `git diff --exit-code`
- bare `git ls-files -t` / `git ls-files -v`
- bare `git ls-tree -r --name-only` on denied paths
- denied paths를 제외하지 않은 broad `git status --short/--porcelain`

### 권장 recipe

아래 recipe는 denied filename이나 content 대신 commit/tree ID, object mode count와
exit code만 출력한다. remote ref는 작업에서 지정한 authoritative ref로 바꾼다.

```powershell
$f0Expected = [ordered]@{
  's0-lab/control/f0-sealed' = 32
  's0-lab/f0-sealed-staging' = 11
  's0-lab/reviews/f0-sealed' = 10
}

$localCommit = git rev-parse HEAD
$localTree = git rev-parse 'HEAD^{tree}'
$remoteCommit = git rev-parse refs/remotes/origin/main
$remoteTree = git rev-parse 'refs/remotes/origin/main^{tree}'

if ($localCommit -ne $remoteCommit -or $localTree -ne $remoteTree) {
  throw 'local/authoritative Git identity mismatch'
}

foreach ($path in $f0Expected.Keys) {
  $treeCount = (git ls-tree -r --format='%(objectmode)' HEAD -- $path |
    Measure-Object -Line).Lines
  $indexCount = (git ls-files --format='%(objectmode)' -- $path |
    Measure-Object -Line).Lines
  if ($treeCount -ne $f0Expected[$path] -or $indexCount -ne $f0Expected[$path]) {
    throw "F0 aggregate mismatch: $path"
  }
  [pscustomobject]@{ Path = $path; TreeCount = $treeCount; IndexCount = $indexCount }
}

$f0Paths = @($f0Expected.Keys)
git diff --quiet HEAD -- @f0Paths
if ($LASTEXITCODE -ne 0) { throw 'F0 tracked worktree drift; content not displayed' }
git diff --cached --quiet HEAD -- @f0Paths
if ($LASTEXITCODE -ne 0) { throw 'F0 staged drift; content not displayed' }

git status --porcelain=v1 -- . `
  ':(exclude)s0-lab/control/f0-sealed/**' `
  ':(exclude)s0-lab/f0-sealed-staging/**' `
  ':(exclude)s0-lab/reviews/f0-sealed/**'
```

주의:

- `git fetch`가 필요한지는 현재 작업의 network/write 권한에 따라 별도로 승인·판단한다.
- remote commit/tree가 다르면 자동 merge/reset하지 말고 차이만 보고한다.
- skip-worktree/assume-unchanged 감사를 꼭 해야 하면 agent-visible
  `git ls-files -t/-v`를 쓰지 말고, filename을 폐기하고 aggregate flag count만
  내보내는 사전 검토된 helper를 별도 사용한다.
- count 불일치 시 내부 filename을 출력해 원인을 찾지 말고 정확한 gate를 요청한다.

## 5. publication eligibility 검증 모델

현재의 “staged scope에 sealed가 없으면 안전” 모델을 다음처럼 바꾼다.

| 검사 | 질문 |
|---|---|
| Inherited tree | authoritative parent/tree에 PUBLIC-GIT 53개가 보존되는가? |
| New diff | 이번 commit의 변경이 승인된 public scope뿐인가? |
| Nonpublic exclusion | NONPUBLIC-OUT-OF-REPO material이 새 blob/history에 들어가지 않았는가? |
| AI boundary | 검증 과정이 denied filename/content를 출력하지 않았는가? |
| Git authority | branch/commit/push 범위가 사용자 승인과 일치하는가? |

`sealed`라는 문자열은 어느 행의 pass/fail 조건도 아니다.

## 6. acceptance criteria

수정 후 fresh public-only reviewer는 다음을 확인해야 한다.

1. `AGENTS.md`가 세 경로를 `PUBLIC-GIT / AI-CONTENT-DEFAULT-DENY`로 정확히 한
   번 정의한다.
2. bare `sealed`를 이유로 commit/push/public worktree에서 제외하라는 current
   normative clause가 0개다.
3. README가 superseded HOME state를 current policy로 라우팅하지 않는다.
4. current handoff가 32/11/10을 동기화 필수로, 내용 접근은 default-deny로
   동시에 말한다.
5. historical handoff에는 superseded banner가 있다.
6. authoritative default branch와 index/tree aggregate가 32/11/10 = 53이다.
7. denied path 검증 command가 filename/content를 출력하지 않는다.
8. Git publication approval과 AI content-read gate가 양방향으로 독립이다.
9. hidden oracle, secret, personal/real material, future nonpublic canonical input의
   repository 금지는 그대로다.
10. 53개 filename/content, frozen protocol bytes, implementation, gate 상태는
    이 policy patch에서 변경되지 않는다.

## 7. 가장 작은 실행 순서

1. `AGENTS.md`의 two-axis 정의, publication block, precedence block을 먼저 수정한다.
2. README/HOME route와 current handoff의 직접 모순만 수정한다.
3. old handoff 두 개에 superseded banner만 추가한다.
4. current sync recipes를 quiet/count-only recipe로 교체한다.
5. public-only hostile re-review를 실행한다.
6. exact staged public scope를 확인한 뒤에만 별도 Git 승인에 따라 commit/push한다.

이 순서는 53개를 건드리지 않고, frozen protocol을 재동결하지 않으면서, 혼동을
만드는 최소 원인을 제거한다.
