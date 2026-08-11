# 공개 Git 동기화 / AI 내용 default-deny 적대적 감사 보고서

## 판정

**Git 동기화 자체는 정상이다. 주된 결함은 정책·용어·우선순위다.**

현재 `HEAD`, index, 로컬 remote-tracking `origin/main`에는 세 F0 경로가 각각
32/11/10개, 합계 53개로 정상 추적되어 있다. ignore, sparse checkout,
skip-worktree, assume-unchanged, submodule, 공개 LFS 설정 또는 attributes가 이
경로를 clone/pull에서 제외한다는 증거는 없다.

반면 최고 공개 운영 규칙과 활성 onboarding 문서에는 다음 두 명제가 동시에
존재한다.

1. 53개는 공개 Git에 추적되어 모든 PC에 동기화되어야 한다.
2. `sealed`는 commit/push/public worktree에서 제외해야 한다.

안전을 우선하는 에이전트가 2번을 더 넓고 엄격한 금지로 해석하면, 파일을
“비공개·게시 불가”라고 잘못 보고하거나 push를 거부·누락하는 것이 현재
문서에서는 예측 가능한 결과다. 이는 기억력 문제가 아니라 **한 규칙 집합이
서로 반대 행동을 명령하는 결정성 있는 정책 결함**이다.

## 감사 범위와 경계

### 조사한 공개 입력

- 루트 `AGENTS.md`, `README.md`, `HOME-CODEX-START.md`
- 공개 `.gitignore`, `.gitattributes`
- 공개 handoff/resume 문서와 공개 protocol/I0/boundary/status 문서
- 세 금지 경로를 먼저 제외한 뒤 얻은 341개 공개 텍스트/config 파일
- Git index/tree/ref/config의 내용 비의존 aggregate metadata

### 조사하지 않은 것

- `s0-lab/control/f0-sealed/**`의 내부 파일명과 내용
- `s0-lab/f0-sealed-staging/**`의 내부 파일명과 내용
- `s0-lab/reviews/f0-sealed/**`의 내부 파일명과 내용
- hidden oracle, secret, personal/protected material, fixture 내용
- provider/model session과 live GitHub 네트워크 상태

세 경로는 오직 상위 경로와 32/11/10 aggregate tracked count로만 다뤘다.

## 의도된 상태

| 축 | 세 F0 경로의 의도된 값 | 의미 |
|---|---|---|
| Git publication/transport | `PUBLIC-GIT`, 추적·보존·동기화 필수 | 해당 commit/tree를 clone, fetch, checkout, pull, push하면 53개가 함께 간다. |
| AI content access | `AI-CONTENT-DEFAULT-DENY` | 정확한 현재 사용자 gate와 role allowlist 없이는 열기·검색·요약·파생·전달 금지다. |
| 실험 gate | 현재 닫힘 | Git 보존이 fixture authoring, executor, judge, S0 실행 승인을 뜻하지 않는다. |
| 진짜 비공개 자산 | `NONPUBLIC-OUT-OF-REPO` | hidden oracle, credentials, private keys, personal/real/secret material과 protocol이 별도 지정한 future canonical execution input이다. |

핵심은 첫째 축과 둘째 축이 독립이라는 점이다. **Git에 공개되어야 하지만 AI가
내용을 읽으면 안 되는 상태는 모순이 아니다.** 현재 문서가 그 두 축을 다시
합쳐버리는 것이 문제다.

## 실제 Git 상태

### 검증 사실

| 검사 | 결과 |
|---|---|
| 감사 branch | `codex/public-sync-default-deny-policy-audit-v01` |
| `HEAD` / 공급된 base | `6a40c94750d6a6edc015caa75f0f79ff2b990339` / 정확히 일치 |
| index tracked aggregate | 32 / 11 / 10 = 53 |
| `HEAD` tree aggregate | 32 / 11 / 10 = 53 |
| 로컬 `refs/remotes/origin/main` | `HEAD`와 동일 commit, 동일 32 / 11 / 10 |
| ignored-but-tracked | 세 경로 모두 0 |
| worktree delta | 세 경로 모두 0 |
| sparse checkout | unset/off |
| skip-worktree / assume-unchanged | aggregate 0 |
| submodule/gitlink | 세 경로 모두 0; 공개 `.gitmodules` 없음 |
| `.gitignore` | Python/docs 로컬 생성물만 제외; F0 패턴 없음 |
| `.gitattributes` | 일반 LF 정규화와 ZIP binary뿐; F0/LFS/배제 규칙 없음 |
| shallow/partial | full repository; shallow 아님 |

### 결론

Git은 `default-deny`를 집행하지 않는다. tracked tree를 그대로 운반한다. 현재
기록된 `origin/main`을 정상 clone/fetch/checkout/pull하면 53개가 함께 온다.
실제 동기화 실패를 일으킬 수 있는 것은 Git 설정이 아니라, 모순된 문구를
따라 에이전트가 삭제·untrack·sparse/prune·push 거부를 선택하는 경우다.

현재 감사 branch 자체에는 upstream이 없으므로 인자 없는 `git pull`은 실패할
수 있다. 이는 감사 branch의 로컬 설정 문제이고 세 F0 경로의 동기화 정책과는
무관하다.

## 발견 요약

| 심각도 | 수 |
|---|---:|
| Critical | 2 |
| Major | 5 |
| Minor | 2 |
| 합계 | 9 |

## 상세 발견

### C-01 — 최고 운영 규칙이 공개 추적과 게시 금지를 동시에 명령한다

**사실**

- `AGENTS.md:13-24`는 세 경로를 `tracked`라고 정의하고 public clone에 존재할
  수 있다고 명시하며, 동기화 역할의 metadata 확인을 허용한다.
- 같은 파일 `AGENTS.md:46-54`, 특히 `:51-54`는 `sealed`를 hidden-oracle,
  secret, personal, otherwise non-public과 한 목록에 넣고 commit/push publication
  대상에서 배제한다.
- Git commit은 staged diff만이 아니라 전체 tree snapshot을 가리킨다. 53개를
  포함한 조상에서 만든 handoff commit은 새 diff가 공개 문서뿐이어도 그 53개가
  있는 tree/history를 계속 참조한다. 따라서 “sealed는 commit에 포함하지
  않는다”를 문자 그대로 만족하면서 같은 계보를 보존하는 것은 불가능하다.

**추론과 영향**

나중에 등장하는 더 넓은 안전 금지를 우선하는 에이전트는 정상 push를 거부하거나
53개를 제거한 tree를 만들 수 있다. 반대로 staged-scope만 검사하면 “sealed는
게시하지 않았다”고 잘못 주장하면서 실제로는 해당 tree/history를 계속
publication한다. 어느 해석도 현재 문구를 완전히 만족시키지 못한다.

### C-02 — 활성 onboarding이 현재 Git 사실과 반대인 문서로 새 세션을 보낸다

**사실**

- `README.md:9`는 다른 PC/새 세션이 먼저 `HOME-CODEX-START.md`를 읽으라고 한다.
- `HOME-CODEX-START.md:35`는 F0-sealed가 untracked이고 Git으로 전달되지 않으며
  다른 PC에서 보이지 않는 것이 정상이라고 한다.
- 같은 문서 `:41-46`은 uncommitted sealed/staging/hidden-oracle 자료가 Git
  인수인계 대상이 아니라고 묶는다.
- 이 문서는 2026-08-07 상태를 기록하지만 superseded/history-only 경고가 없다.
- 현재 index/HEAD/`origin/main`에는 53개가 추적되어 있다.

**추론과 영향**

새 clone에서 53개를 본 에이전트가 이를 “예상치 못한 비공개 누출”로 판단해
중단·삭제·ignore/untrack 제안을 하는 것은 문서가 직접 유도하는 행동이다.

### M-01 — current handoff와 stale handoff가 모두 상반된 publication 규칙을 갖는다

**사실**

- current company→home 문서는 `:18-20`, `:145`, `:159-180`, `:360-376`에서
  53개가 Git-tracked/public-clone이며 AI 입력만 default-deny라고 정확히 쓴다.
- 같은 문서 `:102-104`는 sealed를 public worktree와 Git 게시 범위에서
  제외해야 한다고 하고, `:268-269`는 새 public worktree에 복사하지 말라고 한다.
- companion resume prompt도 `:21-24`에서 tracked 53을 인정한 뒤 `:114-115`에서
  sealed를 public handoff worktree에 복사하지 말라고 한다.
- `home-to-company-2026-08-10/current-state-handoff-v0.1.md:75-80`은 자동 handoff
  commit/push 권한에서 bare `sealed`를 제외하지만 `:86-110`은 32/11/10이
  tracked라고 한다.
- superseded 표시가 없는 2026-08-09 pair는 더 직접적으로 old local-only 정책을
  명령한다:
  - `home-to-company-2026-08-09/current-state-handoff-v0.1.md:22-27,221-230`
  - `home-to-company-2026-08-09/company-local-resume-prompt-v0.1.md:138-141,172-175`

**추론과 영향**

“복사”가 manual copy만 뜻하는지 normal checkout materialization까지 뜻하는지
정의되지 않았다. 구체적인 handoff 문구가 일반 root 규칙보다 작업에 더 가깝기
때문에 에이전트가 잘못된 exclusion을 우선할 가능성이 높다.

### M-02 — `sealed`가 서로 다른 publication class 두 개를 뜻한다

**사실**

- frozen canonical protocol
  `s0-lab/control/s0-protocol-v0.3-canonical-r1.md:353-363`은 future canonical
  input과 oracle/scoring을 저장소 밖 비공개 영역에서 생성하도록 한다.
- 그 문서가 authoritative canonical-r1임은
  `s0-lab/control/protocol-refreeze-v0.3-canonical-r1/control-final-refreeze-decision-v0.1.md:19-32`
  에서 확인된다.
- `docs/tradition/s0-e0-boundary-and-parallel-work.md:98-104,160-168`도 sealed/hidden
  자료를 일반 저장소와 별도로 통제하라고 한다.
- I0 문서 `s0-lab/control/i0/i0-gate-record.md:9-13`과
  `i0-refreeze-next-control-prompt-v0.1.md:80-91`은 sealed input/fixture가 해당
  public worktree/repository에 들어오면 안 된다고 한다.
- 동시에 root policy는 경로명이 F0-SEALED인 53개를 PUBLIC-GIT으로 보존한다.

**추론과 영향**

canonical execution payload와 “publicly tracked but AI-restricted preservation
artifact”가 같은 단어를 공유한다. 경로명만 보고 publication class를 결정하면
한쪽은 반드시 틀린다. frozen protocol 의미를 몰래 바꾸지 말고, root mapping이
두 artifact class가 같지 않음을 명시해야 한다.

### M-03 — 동기화 하네스가 default-deny 내용을 직접 출력할 수 있다

**사실**

공개 텍스트 검색에서 위험한 Git command occurrence 21개를 확인했다. 대표적인
current 문구는 다음과 같다.

- company→home current: `:285-288`, `:317-319`
- company→home resume prompt: `:125-128`, `:139-141`
- home→company 2026-08-10 resume prompt: `:68-69`, `:128-131`, `:141-143`
- `HOME-CODEX-START.md:76`

`git ls-files -t`와 bare `git ls-tree -r --name-only`는 filename을 출력한다.
Broad `git status`는 변경된 filename을 출력한다. `git diff --exit-code`는 quiet
mode가 아니므로 drift가 있을 때 filename뿐 아니라 diff content까지 출력한다.

**추론과 영향**

검증하려던 바로 그 drift가 존재할 때 가장 민감한 출력이 발생한다. unauthorized
read로 역할 증거를 무효화하라는 root 규칙과 하네스가 충돌한다. 이 결함은
sync를 막는 문제가 아니라 sync 감사 세션을 오염시키는 문제다.

### M-04 — 문서 우선순위와 supersession 모델이 없다

**사실**

- root policy, frozen protocol, dated handoff, README, HOME start 문서가 서로
  다른 상태를 말한다.
- dated handoff와 HOME 문서에 `HISTORICAL`, `SUPERSEDED`, `NOT CURRENT POLICY`
  같은 machine/human-visible 표지가 없다.
- 현재 문서가 old handoff의 역사적 사실과 현재 normative rule을 같은 시제로
  섞어 쓴다.
- README는 current policy index가 아니라 stale HOME 문서로 직접 연결한다.

**추론과 영향**

에이전트는 “더 최신”, “더 구체적”, “더 안전한 금지”, “root에 가까움” 중 무엇이
이기는지 임의로 선택한다. 보수적 모델일수록 publication을 막는 문장을 택한다.

### M-05 — publication 승인과 AI read gate가 양방향으로 독립되지 않았다

**사실**

현재 문서는 “Git presence가 read authority가 아니다”는 한 방향을 여러 곳에서
정확히 말한다. 그러나 다음 역방향 규칙이 명시되어 있지 않다.

- AI read/role gate가 열려도 NONPUBLIC artifact의 commit/push가 승인되는 것은 아니다.
- commit/push/handoff 승인이 있어도 AI content read가 승인되는 것은 아니다.
- bare `sealed` label은 어느 축의 승인도 자동 결정하지 않는다.

**추론과 영향**

현재의 혼동을 단순히 “sealed도 push 가능”으로 고치기만 하면, 미래의 truly
non-public canonical input이나 oracle까지 push해도 된다는 반대 방향 사고가
생길 수 있다. 두 축을 동시에 정의해야 안전하다.

### m-01 — 오래된 상태 문장이 현재 사실처럼 남아 있다

**사실**

- `docs/tradition/s0-isolated-design-execution-and-judgment-plan.md:53-60`은
  repository에 첫 commit이 없고 모든 문서가 untracked라고 한다.
- `s0-lab/README.md:3-6,51,71`과 `README.md:49`는 “sealed gate closed/not
  created”를 말한다.

**추론과 영향**

이 문장들은 당시의 gate/authoring 상태로는 성립할 수 있지만, current Git
inventory 설명으로 읽으면 틀리다. 역사와 현재를 분리하는 표지가 필요하다.

### m-02 — count-only 동기화 불변식이 한 곳에 정본화되지 않았다

**사실**

일부 current handoff에는 32/11/10 expectation이 있지만, root policy에는
“authoritative Git tree에서 반드시 보존해야 하는 수량”이라는 운영 불변식과
filename/content를 출력하지 않는 canonical check가 없다. 여러 handoff가 서로
다른 명령을 제공한다.

**추론과 영향**

에이전트마다 다른 명령을 재발명하고, filename listing이나 broad diff로
퇴행한다. count-only/root-tree identity recipe 하나를 current policy에 두는
편이 안전하다.

## 직접 충돌 조항 인벤토리

아래는 공개 corpus에서 Git exclusion 또는 그에 직접 연결되는 동작을 명령한
조항군이다. 단순히 “AI가 sealed를 읽지 않았다”는 review 기록은 여기에 넣지
않았다.

| 조항군 | 공개 근거 | 현재 효과 |
|---|---|---|
| Root handoff publication ban | `AGENTS.md:46-54` | bare `sealed`를 non-public과 동일시 |
| Active stale onboarding | `README.md:9`; `HOME-CODEX-START.md:35,41-46` | clone에 없어야 한다고 오인 |
| Current handoff Git exclusion | company→home current `:102-104` | public worktree/Git에서 제외 명령 |
| Current handoff copy exclusion | company→home current `:268-269`; prompt `:114-115` | normal checkout까지 막을 수 있음 |
| Current handoff auto-push exclusion | home→company 2026-08-10 current `:75-80` | inherited 53의 branch publication을 모호하게 금지 |
| Old local-only Git policy | home→company 2026-08-09 current `:22-27` | sealed를 public Git에 넣지 않음 |
| Old clean-worktree policy | 같은 문서 `:221-230` | sealed/oracle을 새 worktree에 복사 금지 |
| Old sync policy | 2026-08-09 resume `:138-141,172-175` | sealed 미동기화를 정상으로 선언 |
| Canonical execution storage | canonical protocol `:353-363` | true private input은 outside-repo; path label과 충돌 가능 |
| Boundary/I0 storage clauses | boundary `:98-104,160-168`; I0 prompt `:80-91` | task-scoped ban이 global path ban으로 오독 가능 |
| Unsafe Git recipes | current handoff command refs in M-03 | filename/content default-deny를 깨뜨릴 수 있음 |

## 올바른 반대 증거와 보존해야 할 문구

- `AGENTS.md:13-29`: tracked/public-clone presence와 AI input authority의 분리
- company→home current `:18-20,145,159-180,360-376`
- home→company current `:86-110`
- home→company company resume `:42-57`
- `.codex/agents/s0-fixture-author.toml:7-8`: sealed input과 private/outside-repository
  hidden oracle의 분리
- `s0-lab/reviews/f0-public/question-contract-v0.4/urc-v0.4-independent-review-v0.1.md:5`:
  `f0-sealed` 경로 아래 record도 public일 수 있다는 선례

이 문구들은 폐기할 것이 아니라 root 정의로 정규화할 재료다.

## 인과 사슬

1. 초기 handoff 시점에는 일부 F0 경로가 실제로 untracked/local-only였다.
2. 이후 사용자 결정으로 유실 방지를 위해 53개가 Git-tracked/public sync
   대상으로 바뀌었다.
3. 새 root 규칙에 tracked/public-clone 문장은 추가됐지만, 기존 bare `sealed`
   publication ban과 outside-repo 용어는 남았다.
4. README는 여전히 정책 전환 전 HOME 문서로 새 세션을 보낸다.
5. current handoff조차 새 상태와 옛 금지를 같은 문서에 함께 넣었다.
6. 에이전트는 안전상 더 넓은 금지를 선택해 `sealed = private = do not push`로
   단순화한다.
7. Git은 53개를 정상 운반하지만, 에이전트의 보고·staging·branch 선택이
   동기화를 망가뜨린다.

## 적대적 실패 시나리오

| # | 시나리오 | 현재 규칙이 만드는 실패 | 올바른 동작 |
|---:|---|---|---|
| 1 | 새 PC가 README→HOME 순서로 읽음 | clone에 53개가 보이면 누출로 오인하고 중단/삭제 제안 | 53개 presence/count를 정상 sync로 보고하고 내용은 읽지 않음 |
| 2 | handoff commit/push 승인 | `AGENTS.md:54`를 따라 53개를 `git rm --cached` | 기존 53개를 tree에 그대로 보존하고 새 public diff만 검증 |
| 3 | 안전을 위해 `.gitignore`에 F0 패턴 추가 | tracked 파일에는 효과가 없는데 보호됐다고 오보고 | ignore를 보안 수단으로 사용하지 않음 |
| 4 | agent가 “sealed push 금지”를 문자 해석 | 정상 branch push 자체를 거부 | PUBLIC-GIT tree transport와 AI read를 분리 |
| 5 | 금지를 만족하려 orphan/pruned branch 생성 | history/integrity와 cross-PC 동일성 파괴 | 동일 계보의 full tree 유지 |
| 6 | current handoff의 “공개 worktree에 복사 금지” 수행 | sparse checkout/manual omission으로 53개 미물질화 | normal checkout은 허용·필수, manual content read/copy만 금지 |
| 7 | staged public-only 검사만 수행 | ancestor/tree가 53개를 포함한다는 사실과 금지 문구가 충돌 | 53개를 명시적 PUBLIC-GIT 예외로 정의 |
| 8 | Git publication 승인 후 내용도 읽음 | transport 승인을 content gate로 오인 | metadata-only sync 유지 |
| 9 | exact F0 read gate 후 private oracle도 push | read gate를 publication 승인으로 오인 | NONPUBLIC-OUT-OF-REPO는 별도 publication 금지 유지 |
| 10 | dirty F0 상태에서 broad `git diff --exit-code` | diff content 출력으로 세션 오염/무효 | `--quiet`와 denied path metadata-only exit code 사용 |
| 11 | `git ls-files -t`/bare `ls-tree --name-only` 실행 | 53개 내부 filename 열거 | object mode/count 또는 root-tree identity만 출력 |
| 12 | “sealed gate closed”를 inventory absence로 해석 | tracked 파일을 제거하거나 수신 실패로 판단 | gate status와 Git presence를 별도 보고 |
| 13 | worktree를 비밀 경계로 간주 | public Git clone을 비공개로 오인하거나 반대로 secrecy를 과장 | worktree는 편집 격리일 뿐이라고 보고 |
| 14 | upstream 없는 branch에서 no-arg pull 실패 | F0 sync 정책/파일 탓으로 오진 | explicit remote/ref를 확인하고 branch config 문제로 분리 |

## 비문제(nonproblems)

- 경로명에 `sealed`가 들어간다는 사실 자체는 Git privacy 기능이 아니다.
- `.gitignore`는 현재 53개를 clone/pull에서 빼지 않는다.
- public Git presence는 AI read authority가 아니다.
- AI default-deny는 Git transport를 막지 않는다.
- unchanged 53개를 매 handoff diff에 다시 stage할 필요는 없다. commit tree에
  보존되면 된다.
- canonical protocol의 truly non-public future input을 outside-repo에 두는 원칙
  자체는 잘못이 아니다. 그것을 현재 PUBLIC-GIT 53개와 같은 class로 부르는
  taxonomy가 문제다.
- old handoff의 역사적 사실을 삭제할 필요는 없다. superseded banner와 current
  policy pointer면 충분하다.
- 53개를 rename/delete할 필요가 없다.

## 증거 한계

- live network fetch를 하지 않았다. `origin/main == HEAD`는 이 audit clone의
  local remote-tracking ref에 대한 사실이다.
- 원격 GitHub repository의 현재 visibility setting은 독립 확인하지 않았다.
  공개 clone이라는 publication class는 root policy, public handoff, 사용자
  명시 의도에 근거한다.
- 금지된 53개 내용과 내부 filename을 보지 않았으므로 내용 자체의 민감성이나
  protocol artifact identity는 판정하지 않는다.
- hidden oracle 또는 future canonical execution input이 실제로 존재하는지
  확인하지 않았다.

## 권고

가장 작은 일관된 수정은 53개를 rename/delete하는 것이 아니라 다음 네 가지다.

1. root에서 `PUBLIC-GIT / AI-CONTENT-DEFAULT-DENY`와
   `NONPUBLIC-OUT-OF-REPO`를 명시적으로 분리한다.
2. `AGENTS.md:46-54`의 bare `sealed` publication ban을 대체하고 양방향 독립
   규칙을 추가한다.
3. README/HOME/stale handoff에 current/superseded precedence를 표시하고 current
   handoff의 두 exclusion 문장을 고친다.
4. broad diff/status/name-listing recipe를 root-tree identity + quiet/count-only
   recipe로 교체한다.

정확한 제안 문구와 순서는 `minimal-rule-revision-proposal.md`에 제시한다.

## 정확한 다음 행동

사용자는 별도 **공개 운영정책 정합성 수정 작업**을 열어
`minimal-rule-revision-proposal.md`의 최소 patch 범위만 적용하게 해야 한다.
frozen canonical protocol의 의미는 이 작업에서 수정하지 말고 root mapping으로
구분한다. 수정 후 fresh public-only reviewer가 다음을 재검증해야 한다.

- `sealed = do not push` 직접 조항 0개
- 세 경로 aggregate 32/11/10 = 53 유지
- authoritative default branch tree와 수신 tree 동일
- denied filename/content를 출력하는 sync command 0개
- publication 승인과 AI read gate가 양방향 독립

그 재검증 전에는 이 감사가 source 수정, commit, push, PR 또는 protocol gate를
승인한 것으로 취급하지 않는다.
