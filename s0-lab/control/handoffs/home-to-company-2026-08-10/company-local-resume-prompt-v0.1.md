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
$gitExe = (Get-Command git.exe -ErrorAction Stop).Source
function git { & $gitExe @args 2>$null }
$repoRoot = (git rev-parse --show-toplevel).Trim()
$repoRootExit = $LASTEXITCODE
if ($repoRootExit -ne 0) { throw 'Repository root resolution failed' }
Set-Location -LiteralPath $repoRoot -ErrorAction Stop
$originUrl = (git remote get-url origin).Trim()
$originExit = $LASTEXITCODE
$allowedOrigins = @(
  'https://github.com/shotgun1107/human-ai-development-tradition.git'
  'git@github.com:shotgun1107/human-ai-development-tradition.git'
)
if ($originExit -ne 0 -or $originUrl -notin $allowedOrigins) { throw 'Origin mismatch' }
$currentBranch = (git symbolic-ref --quiet --short HEAD).Trim()
$branchExit = $LASTEXITCODE
if ($branchExit -ne 0 -or [string]::IsNullOrWhiteSpace($currentBranch)) { throw 'Detached HEAD' }
$currentHead = (git rev-parse HEAD).Trim()
$headExit = $LASTEXITCODE
if ($headExit -ne 0) { throw 'HEAD resolution failed' }
"REPOSITORY_ROOT_VERIFIED=1"
"ORIGIN_VERIFIED=1"
"BRANCH=$currentBranch"
"HEAD=$currentHead"
$f0Paths = @('s0-lab/control/f0-sealed','s0-lab/f0-sealed-staging','s0-lab/reviews/f0-sealed')
function Assert-SyncPreflight {
  $repoStatusRecords = @(git status --porcelain=v1 --untracked-files=all)
  $repoStatusExit = $LASTEXITCODE
  $repoStatusCount = $repoStatusRecords.Count
  $repoStatusRecords = $null
  $repoIgnoredRecords = @(git ls-files --others --ignored --exclude-standard)
  $repoIgnoredExit = $LASTEXITCODE
  $repoIgnoredTotalCount = $repoIgnoredRecords.Count
  $repoUnclassifiedIgnoredCount = @($repoIgnoredRecords | Where-Object {
    $_ -notmatch '(^|/)\.venv-docs(/|$)' -and
    $_ -notmatch '(^|/)\.mkdocs-site(/|$)' -and
    $_ -notmatch '(^|/)__pycache__(/|$)' -and
    $_ -notmatch '\.py[cod]$'
  }).Count
  $repoIgnoredRecords = $null
  $repoApprovedLocalEnvIgnoredCount = $repoIgnoredTotalCount - $repoUnclassifiedIgnoredCount
  git diff --quiet HEAD -- @f0Paths
  $f0UnstagedExit = $LASTEXITCODE
  git diff --cached --quiet HEAD -- @f0Paths
  $f0StagedExit = $LASTEXITCODE
  $f0UntrackedRecords = @(git ls-files --others --exclude-standard -- @f0Paths)
  $f0UntrackedQueryExit = $LASTEXITCODE
  $f0UntrackedCount = $f0UntrackedRecords.Count
  $f0UntrackedRecords = $null
  $f0IgnoredRecords = @(git ls-files --others --ignored --exclude-standard -- @f0Paths)
  $f0IgnoredQueryExit = $LASTEXITCODE
  $f0IgnoredCount = $f0IgnoredRecords.Count
  $f0IgnoredRecords = $null
  $f0TaggedRecords = @(git ls-files -v -- @f0Paths)
  $f0TaggedQueryExit = $LASTEXITCODE
  $f0SpecialIndexCount = @($f0TaggedRecords | Where-Object { $_ -cmatch '^(S|[a-z]) ' }).Count
  $f0TaggedRecords = $null
  $stashRecords = @(git stash list --format='%gd')
  $stashQueryExit = $LASTEXITCODE
  $stashCount = $stashRecords.Count
  $stashRecords = $null
  "REPO_STATUS_COUNT=$repoStatusCount"
  "REPO_APPROVED_LOCAL_ENV_IGNORED_COUNT=$repoApprovedLocalEnvIgnoredCount"
  "REPO_UNCLASSIFIED_IGNORED_COUNT=$repoUnclassifiedIgnoredCount"
  "F0_UNSTAGED_EXIT=$f0UnstagedExit"
  "F0_STAGED_EXIT=$f0StagedExit"
  "F0_UNTRACKED_COUNT=$f0UntrackedCount"
  "F0_IGNORED_COUNT=$f0IgnoredCount"
  "F0_SPECIAL_INDEX_COUNT=$f0SpecialIndexCount"
  "STASH_COUNT=$stashCount"
  if ($repoStatusExit -ne 0 -or $repoStatusCount -ne 0 -or
      $repoIgnoredExit -ne 0 -or $repoUnclassifiedIgnoredCount -ne 0 -or
      $f0UnstagedExit -ne 0 -or $f0StagedExit -ne 0 -or
      $f0UntrackedQueryExit -ne 0 -or $f0UntrackedCount -ne 0 -or
      $f0IgnoredQueryExit -ne 0 -or $f0IgnoredCount -ne 0 -or
      $f0TaggedQueryExit -ne 0 -or $f0SpecialIndexCount -ne 0 -or
      $stashQueryExit -ne 0 -or $stashCount -ne 0) {
    throw 'Sync preflight blocked; aggregate conditions only'
  }
}
function Assert-NoLocalOnlyCommits {
  $localOnlyRecords = @(git rev-list --branches --not --remotes)
  $localOnlyQueryExit = $LASTEXITCODE
  $localOnlyCount = $localOnlyRecords.Count
  $localOnlyRecords = $null
  "LOCAL_ONLY_COMMIT_COUNT=$localOnlyCount"
  if ($localOnlyQueryExit -ne 0 -or $localOnlyCount -ne 0) {
    throw 'Local-only commit preflight blocked after fetch'
  }
}
function Assert-F0TreeInventory([string]$Commit) {
  $records0 = @(git ls-tree -r --format='%(objectmode)' $Commit -- $f0Paths[0])
  $exit0 = $LASTEXITCODE
  $records1 = @(git ls-tree -r --format='%(objectmode)' $Commit -- $f0Paths[1])
  $exit1 = $LASTEXITCODE
  $records2 = @(git ls-tree -r --format='%(objectmode)' $Commit -- $f0Paths[2])
  $exit2 = $LASTEXITCODE
  $counts = @($records0.Count,$records1.Count,$records2.Count)
  $records0 = $records1 = $records2 = $null
  "F0_TREE_COUNTS=$($counts -join '/')"
  if ($exit0 -ne 0 -or $exit1 -ne 0 -or $exit2 -ne 0 -or
      $counts[0] -ne 32 -or $counts[1] -ne 11 -or $counts[2] -ne 10) {
    throw 'Pinned tree F0 inventory mismatch'
  }
}
function Assert-RemotePin([string]$Ref,[string]$Pinned) {
  $current = (git rev-parse $Ref).Trim()
  $queryExit = $LASTEXITCODE
  if ($queryExit -ne 0 -or $current -ne $Pinned) {
    throw 'Remote ref moved after pin verification'
  }
}
Assert-SyncPreflight
Assert-F0TreeInventory -Commit HEAD
```

origin이 다르거나 detached HEAD이면 변경하지 말고 보고한다. 최초 aggregate
preflight 중 하나라도 실패하면 사용자 작업으로 간주한다. local-only commit은
clean 상태에서 fetch로 remote refs를 갱신한 직후 판단한다. 실패하면 pull,
switch, checkout, reset, clean, stash, rebase, merge, 삭제 또는 덮어쓰기를
하지 말고 filename 없이 aggregate 상태만 보고한다.

기존 저장소가 clean하고 origin이 일치할 때만 다음 단계로 간다.

## 4. 전체 원격 branch 동기화

원격 상태 변경 명령은 하나씩 실행하고 결과를 확인한 뒤 다음으로 간다.

```powershell
if ((Get-Command git -ErrorAction Stop).CommandType -ne 'Function') { throw 'Safe Git wrapper missing' }
git fetch --prune origin "+refs/heads/*:refs/remotes/origin/*"
if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }
Assert-NoLocalOnlyCommits
$mainCommit = (git rev-parse refs/remotes/origin/main).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Main ref resolution failed' }
$predecessorCommit = (git rev-parse refs/remotes/origin/codex/s0-order-eight-public-vector-independent-verification-v02).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Predecessor ref resolution failed' }
$targetCommit = (git rev-parse refs/remotes/origin/codex/home-to-company-handoff-20260810).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Target ref resolution failed' }
Assert-F0TreeInventory -Commit $targetCommit
$payloadType = (git cat-file -t 85ad19ba6703f43b1209a13164d1e28a4b62f6a4).Trim()
if ($LASTEXITCODE -ne 0 -or $payloadType -ne 'commit') { throw 'Payload type mismatch' }
git merge-base --is-ancestor 85ad19ba6703f43b1209a13164d1e28a4b62f6a4 $targetCommit
if ($LASTEXITCODE -ne 0) { throw 'Payload ancestry mismatch' }
git merge-base --is-ancestor b857545113058321dd4d65f601c2d5ad8cceeec0 $targetCommit
if ($LASTEXITCODE -ne 0) { throw 'Predecessor ancestry mismatch' }
git diff --quiet b857545113058321dd4d65f601c2d5ad8cceeec0 $targetCommit -- @f0Paths
$predecessorF0DiffExit = $LASTEXITCODE
if ($predecessorF0DiffExit -ne 0) { throw 'Target changed F0 after approved predecessor' }
$predecessorTree = (git rev-parse "b857545113058321dd4d65f601c2d5ad8cceeec0^{tree}").Trim()
if ($LASTEXITCODE -ne 0 -or $predecessorTree -ne '655bea08eb117a565bccc9241fb3361ce3c8f1d8') { throw 'Predecessor tree mismatch' }
```

위 block은 fetch, local-only, refs, payload type, ancestry와 predecessor tree를
각 단계에서 fail closed한다. 실패하면 임의로 다른 branch를 선택하거나
수정하지 말고 filename 없이 실패 조건과 aggregate만 보고한다.

기존 worktree가 완전히 clean하면 handoff branch를 local tracking branch로
전환하거나 기존 branch를 fast-forward한다.

local branch가 없을 때:

```powershell
if ((Get-Command git -ErrorAction Stop).CommandType -ne 'Function') { throw 'Safe Git wrapper missing' }
Assert-RemotePin -Ref refs/remotes/origin/codex/home-to-company-handoff-20260810 -Pinned $targetCommit
git switch -c codex/home-to-company-handoff-20260810 $targetCommit
$switchExit = $LASTEXITCODE
if ($switchExit -ne 0) { throw 'Pinned branch creation failed' }
git branch --set-upstream-to=origin/codex/home-to-company-handoff-20260810 codex/home-to-company-handoff-20260810
$upstreamExit = $LASTEXITCODE
if ($upstreamExit -ne 0) { throw 'Upstream binding failed' }
$materializedHead = (git rev-parse HEAD).Trim()
$headQueryExit = $LASTEXITCODE
$materializedUpstream = (git rev-parse --symbolic-full-name '@{upstream}').Trim()
$upstreamQueryExit = $LASTEXITCODE
if ($headQueryExit -ne 0 -or $materializedHead -ne $targetCommit -or
    $upstreamQueryExit -ne 0 -or $materializedUpstream -ne 'refs/remotes/origin/codex/home-to-company-handoff-20260810') {
  throw 'Pinned branch identity mismatch'
}
```

local branch가 이미 있고 divergence가 없을 때:

```powershell
if ((Get-Command git -ErrorAction Stop).CommandType -ne 'Function') { throw 'Safe Git wrapper missing' }
$localTarget = (git rev-parse refs/heads/codex/home-to-company-handoff-20260810).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Local target resolution failed' }
Assert-F0TreeInventory -Commit $localTarget
Assert-RemotePin -Ref refs/remotes/origin/codex/home-to-company-handoff-20260810 -Pinned $targetCommit
git switch codex/home-to-company-handoff-20260810
$switchExit = $LASTEXITCODE
if ($switchExit -ne 0) { throw 'Existing branch switch failed' }
git merge --ff-only $targetCommit
$mergeExit = $LASTEXITCODE
if ($mergeExit -ne 0) { throw 'Pinned fast-forward failed' }
$materializedHead = (git rev-parse HEAD).Trim()
$headQueryExit = $LASTEXITCODE
if ($headQueryExit -ne 0 -or $materializedHead -ne $targetCommit) { throw 'Pinned target mismatch' }
```

단순 `pull`로 현재 다른 branch에 handoff를 merge하지 마라. public-only
변경·미추적, F0 quiet diff 실패, F0 local-only/ignored 또는 special-index
aggregate count, stash, local-only commit 중 하나라도 있으면 dirty로 취급한다.
dirty하면 in-place 동기화를 수행하지 말고 첫 상태만 보고한다.

## 5. 수신 동일성 검증

선택한 handoff worktree에서 다음을 각각 확인한다.

```powershell
if ((Get-Command git -ErrorAction Stop).CommandType -ne 'Function') { throw 'Safe Git wrapper missing' }
git rev-parse HEAD
git rev-parse "HEAD^{tree}"
$finalRemote = (git rev-parse refs/remotes/origin/codex/home-to-company-handoff-20260810).Trim()
$finalRemoteExit = $LASTEXITCODE
$finalHead = (git rev-parse HEAD).Trim()
$finalHeadExit = $LASTEXITCODE
if ($finalRemoteExit -ne 0 -or $finalRemote -ne $targetCommit -or
    $finalHeadExit -ne 0 -or $finalHead -ne $targetCommit) {
  throw 'Final pinned identity mismatch'
}
Assert-SyncPreflight
Assert-NoLocalOnlyCommits
Assert-F0TreeInventory -Commit HEAD
```

local HEAD와 remote handoff tip이 같고 모든 preflight aggregate가 통과해야
한다. Git tree 동일성은 대화, `.git`, cache,
`.venv`, OS 설정과 untracked/ignored 파일까지 두 PC가 같다는 의미가 아니다.

sealed 수량은 내용이나 filename을 출력하지 않고 count만 확인한다.

```powershell
if ((Get-Command git -ErrorAction Stop).CommandType -ne 'Function') { throw 'Safe Git wrapper missing' }
@(git ls-files --format='%(objectmode)' -- "s0-lab/control/f0-sealed").Count
@(git ls-files --format='%(objectmode)' -- "s0-lab/f0-sealed-staging").Count
@(git ls-files --format='%(objectmode)' -- "s0-lab/reviews/f0-sealed").Count
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
