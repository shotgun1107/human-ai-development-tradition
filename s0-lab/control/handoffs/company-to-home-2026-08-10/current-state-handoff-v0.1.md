# 회사 CONTROL에서 집 CONTROL로 보내는 현재 상태 인수인계 v0.1

- 작성 기준일: `2026-08-10` KST
- 저장소: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- 활성 기준선: `central-system-v2.1-s0-preparation`
- 인수인계 브랜치: `codex/s0-order-eight-public-vector-independent-verification-v02`
- 인수인계 기준 부모: `daba763e219f597197768769115c01e5ea929c8a`
- 동기화 payload commit: `85ad19ba6703f43b1209a13164d1e28a4b62f6a4`
- 동기화 payload tree: `11f31ab0cac263cc876467c6adf7e902a40621d0`
- 공개 `main` 기준: `5add6e5e1675793ad179e98e51ffa1515feb3db8`
- 성격: 공개 Git 추적 자료와 현재 CONTROL 상태의 회사→집 인계
- 비의미: 구현 완료, 벡터 통과·동결, 키 생성, S0 또는 E0 실행 승인 아님

이 문서는 회사 Codex의 대화 기억을 복사하는 파일이 아니다. 집 CONTROL은
Git 원격 ref, commit, tree, working-tree 상태, 공개 문서와 SHA-256을 직접
확인해야 한다. Git이 전달하지 않는 대화, 임시 worktree, `.venv`, cache,
OS 설정과 이 인수 branch 밖의 untracked/ignored 파일은 동기화 대상이
아니다. 회사에만 남아 있던 F0-SEALED 53개 파일은 유실 방지를 우선한다는
사용자 결정에 따라 이 인수 branch에서 Git 추적한다. 공개 Git에 있다는
사실은 AI의 입력 허가가 아니며 `AGENTS.md`의 default-deny 규칙을 따른다.

## 1. 한눈에 보는 과거·현재·미래

### 과거

1. 집 PC에서 trust-root/role-isolation 설계를 확장했고, 회사 PC는 이전
   인수인계 문서와 Git 정본을 이용해 그 작업을 이어받았다.
2. v0.4 역할 격리 설계는 독립 심사를 통과하고 CONTROL 통합 판단을 받았다.
3. order-eight 공개 벡터 4개와 계산 설명을 작성했다. 이 벡터는 실제 키가
   아니라, 미래의 엄격한 Ed25519 검증기가 반드시 거부해야 하는 공개
   음성 시험값이다.
4. 첫 독립 검증 v0.1은 공식 자료에 숫자 `d`가 없다는 입력 경계 문제로
   `INVALID-REVIEW`가 됐다.
5. 입력 경계를 고친 후보 `daba763...`을 만들고 원격 전용 브랜치에
   푸시했다.
6. 승인된 선행 계보만 원격 `main`에 fast-forward로 반영했다. 원격
   `main`은 `5add6e5...`이고, 벡터 작성·검증 계보는 아직 `main` 밖이다.

### 현재

1. 두 번째 독립 검증 v0.2도 `INVALID-REVIEW`다.
2. 이번 실패는 벡터 수학의 실패가 아니라 공식 RFC 파일을 고정한 방식의
   실패다. 경계 문서는 HTTP 원문을 106,573 bytes, SHA-256
   `f13ab006baa1a30a7835113927e9d23ca9d9c460f352e721cbcdff8adbf1dee9`
   로 선언했지만, 실제 공식 응답은 LF 줄바꿈의 103,210 bytes, SHA-256
   `ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3`
   였다.
3. 실제 응답의 3,363개 LF를 CRLF로 바꾸면 문서의 길이와 해시가 정확히
   재현된다. 즉 문서가 HTTP 원문이라고 부른 값은 실제로 CRLF 변환본이었다.
4. fail-closed 규칙 때문에 검토자는 RFC 조각을 노출하지 않았고, 벡터를
   독립 계산하지 않았으며, 후보 벡터와 작성자 계산 설명을 의미상 읽지
   않았다. 따라서 벡터는 통과도 실패도 아니다.
5. 검증 보고서의 판정은 `INVALID-REVIEW`, 검토 무결성 blocking 1건,
   실질 벡터 finding은 미평가다.
6. 벡터 최종 동결 게이트는 닫혀 있다.

### 미래

1. 공식 RFC 입력을 LF로 정규화하는 규칙을 정확히 정의하거나, 공식 원문의
   실제 LF bytes를 기준으로 길이·전체 hash·slice offset·slice hash를 다시
   고정한다.
2. 줄바꿈 차이에 강하면서 내용 변조에는 닫히려면 다음 revision에서
   `CRLF → LF`만 허용하고 bare CR, 다른 byte 변경, marker 누락은 거부하는
   방식이 권장된다. 이 항목은 아직 제안이지 승인된 수정이 아니다.
3. 수정된 경계와 brief를 별도 문서/sidecar로 동결한다.
4. 사용자가 정확한 독립 검증 게이트를 다시 열면, 이전 검토 결과를 보지
   않은 fresh reviewer가 공식 자료에서 먼저 값을 계산한다.
5. zero-finding 통과일 때만 별도 CONTROL 최종 동결 게이트를 연다.
6. 벡터 동결 뒤에도 구현, 키 생성, protected material, fixture/oracle,
   provider/model, E0 또는 S0 실행은 자동으로 열리지 않는다.

## 2. 회사 PC에서 실제로 겪은 상황

### 2.1 기존 `main` 작업 폴더를 직접 동기화하지 않은 이유

회사 기본 저장소 경로는 다음 상태였다.

- branch: `main`
- local HEAD: `d88097df450c7869ebf336e3e1089d952955ea3f`
- `origin/main`보다 52 commits 뒤
- local stash 없음
- 다음 미추적 디렉터리 존재
  - `s0-lab/control/f0-sealed/`
  - `s0-lab/f0-sealed-staging/`
  - `s0-lab/reviews/f0-sealed/`

이 경로에서 pull, switch, checkout, merge, reset, clean 또는 stash를 하면
회사 고유 봉인 작업을 덮거나 숨길 위험이 있었다. 따라서 그 작업 폴더는
건드리지 않았다. 미추적 경로의 내용도 이번 공개 작업에서 읽지 않았다.

### 2.2 회사에서 사용한 안전한 동기화 방식

1. 기존 dirty `main`을 그대로 보존했다.
2. 공개 commit에서 별도 clean 임시 worktree와 branch를 만들었다.
3. `main`과 대상 계보의 양방향 ancestry와 exact commit을 확인했다.
4. main-only commit이 0개인 것을 확인한 뒤 승인된 exact commit
   `5add6e5...`만 `refs/heads/main`으로 fast-forward push했다.
5. 벡터 작성·검증 계보는 `main`과 섞지 않고 별도 branch에서 계속했다.
6. 모든 공개 Markdown/sidecar는 canonical validator SelfTest와 개별 검사를
   통과시킨 뒤 보존했다.

이 방식은 편집 충돌을 피한 것이지 봉인 자료를 보호하는 보안 경계를 만든
것은 아니다. 봉인 자료는 애초에 공개 worktree와 Git 게시 범위에서 제외해야
한다.

### 2.3 게이트 처리에서 발생한 절차 문제

CONTROL은 사용자의 `승인 계보 main 병합 → 벡터 검증·동결까지 진행`을
독립 검증 게이트까지 열린 것으로 넓게 해석해 검토 세션 하나를 너무 일찍
시작했다. 사용자가 정확한 게이트가 없음을 지적하자 즉시 중단했다. 그
세션은 파일을 만들지 않았고 commit/push도 하지 않았지만 독립 검토자로는
재사용하지 않는다.

그 뒤 사용자가 정확히 다음 문구를 입력했다.

```text
S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN
```

완전히 새로운 reviewer가 현재 v0.2 `INVALID-REVIEW` 보고서를 만들었다.
정확한 게이트 문구는 암호나 사용자 인증 수단이 아니라 민감한 단계의
실수 방지 규칙이다. 사용자는 별도 Gate Broker까지 구축하지 않기로 했으므로,
집 CONTROL은 민감한 다음 게이트를 자연어 `ㄱㄱ`, `계속`, `끝까지`로
확대 해석하지 않는다.

## 3. Git 계보와 정본

현재 확인된 공개 계보는 다음과 같다.

```text
5add6e5  origin/main: approved public prerequisite lineage
  -> 56fb330  author four order-eight public vectors
  -> dbba47b  preserve first INVALID vector review
  -> daba763  revise independent-review input boundary
  -> working outputs: second INVALID vector review + F0-SEALED preservation
     + this handoff package
```

확인된 원격 ref:

| ref | 확인된 commit | 상태 |
|---|---|---|
| `origin/main` | `5add6e5e1675793ad179e98e51ffa1515feb3db8` | 원격 `main`에 반영됨 |
| `origin/codex/s0-order-eight-public-vector-review-input-boundary-r1` | `daba763e219f597197768769115c01e5ea929c8a` | 원격에 반영됨 |
| `origin/codex/s0-order-eight-public-vector-independent-verification-v02` | payload 게시 시 `85ad19ba6703f43b1209a13164d1e28a4b62f6a4` | 검증 보고서, F0-SEALED 53개, `AGENTS.md`, 인수인계 초안 포함 |

이 문서와 sidecar를 최종화하는 후속 commit은 self-reference를 피하기 위해
자기 SHA를 문서 안에 기록하지 않는다. 집 CONTROL은 live 원격 tip을 직접
읽고, 그 tip이 payload commit `85ad19b...`을 조상으로 포함하며 위 payload
tree의 파일을 모두 보존하는지 확인한다. 최종 게시 보고의 원격 tip과 live
원격이 다르면 임의로 맞추지 말고 차이를 보고한다.

`5add6e5...`는 `daba763...`의 조상이고, boundary branch는 `main`보다 정확히
3 commits 앞선다. 집 PC는 `main`만 pull해서는 최신 벡터 작업과 두
`INVALID-REVIEW` 기록을 받을 수 없다. 이 인수인계가 게시된 뒤에는
`codex/s0-order-eight-public-vector-independent-verification-v02`의 전체
Git tree를 받아야 한다.

### 3.1 함께 보존하는 F0-SEALED 자료

회사 로컬에만 있던 다음 세 경로의 53개 파일도 같은 branch에 보존한다.

| 경로 | 파일 수 | 용도 | 기본 AI 접근 |
|---|---:|---|---|
| `s0-lab/control/f0-sealed/` | 32 | authoring/revision/review brief, gate, CONTROL 결정, 질문 설계 제안 | 거부 |
| `s0-lab/f0-sealed-staging/` | 11 | 두 합성 source block, 질문·runner projection, manifest와 authoring report | 거부 |
| `s0-lab/reviews/f0-sealed/` | 10 | 제한 심사와 비교 심사 기록 | 거부 |

경로·확장자·자격증명 패턴·JSON property 이름만 대상으로 게시 적격성을
검사했다. 실제 API/GitHub/AWS/Google/Slack token, private-key header,
이메일과 Windows 사용자 절대경로는 발견되지 않았다. staging JSON에는
`correct_answer`, answer key 또는 oracle value property가 없고 runner
projection은 answer marker 제외 불변식을 선언한다. CONTROL 문서의
`oracle` 단어는 경계·금지 설명에 존재할 수 있으므로 공개 여부와 AI 입력
허가는 별개다.

세 경로는 public clone에 물리적으로 존재하지만 다음 규칙을 적용한다.

- 동기화 세션은 path inventory, tracked state, file count와 SHA만 비교한다.
- 정확한 F0-SEALED gate와 role allowlist가 없으면 내용 검색·열기·요약·전달을
  하지 않는다.
- executor, judge, public reviewer와 무관한 CONTROL은 이 경로를 입력으로
  사용하지 않는다.
- 무단 read가 발생하면 해당 역할의 후속 증거를 무효로 하고 중단한다.

이것은 암호화나 OS ACL이 아니라 사용자 선택에 따른 절차적 격리다.

## 4. 현재 검증 결과

두 번째 검증 출력은 다음 pair다.

- `s0-lab/reviews/isolation/order-eight-public-vector-v0.1/independent-verification-v0.2.md`
- `s0-lab/reviews/isolation/order-eight-public-vector-v0.1/independent-verification-v0.2.sha256`
- Markdown SHA-256:
  `1214e3b30e0002210b3e1fa2ffa5aad2443786284320bea98e5240daef7baaf3`

검토 종료 시 확인된 사실:

- 26개 허용 입력 hash 전부 유지
- validator SelfTest 통과
- 출력 pair canonical validation 통과
- branch, HEAD, tree와 부모 관계 유지
- 허용 출력 두 개 외 변경 없음
- 후보 벡터 계산·비교 없음
- commit/push 없음

## 5. 집 PC 동기화 절차

### 5.1 공통 중단 조건

기존 집 저장소가 있으면 먼저 origin, branch, HEAD, status와 stash를 확인한다.
다음 중 하나라도 있으면 기존 worktree에 pull, switch, reset, clean, stash,
rebase 또는 merge하지 않는다.

- origin이 위 저장소와 다름
- detached HEAD
- modified, staged 또는 untracked 파일 존재
- 기존 stash 존재
- 원격에 없는 local-only commit 존재

이 경우 상태를 보존하고, fetch 뒤 별도 clean worktree에서 인수한다.

### 5.2 기존 저장소가 깨끗한 경우

```powershell
git remote get-url origin
git branch --show-current
git rev-parse HEAD
git status --short
git stash list
git fetch origin
git rev-parse origin/main
git rev-parse origin/codex/s0-order-eight-public-vector-independent-verification-v02
git cat-file -t 85ad19ba6703f43b1209a13164d1e28a4b62f6a4
git rev-parse '85ad19ba6703f43b1209a13164d1e28a4b62f6a4^{tree}'
git merge-base --is-ancestor 85ad19ba6703f43b1209a13164d1e28a4b62f6a4 origin/codex/s0-order-eight-public-vector-independent-verification-v02
git log --oneline --branches --not --remotes
```

`cat-file`은 `commit`, payload tree는
`11f31ab0cac263cc876467c6adf7e902a40621d0`, ancestry 명령은 exit 0이어야
한다.

인수 branch가 로컬에 없으면:

```powershell
git switch --track origin/codex/s0-order-eight-public-vector-independent-verification-v02
```

이미 있고 clean하며 divergence가 없으면:

```powershell
git switch codex/s0-order-eight-public-vector-independent-verification-v02
git pull --ff-only origin codex/s0-order-eight-public-vector-independent-verification-v02
```

### 5.3 기존 저장소가 dirty이거나 다른 작업 중인 경우

기존 경로를 그대로 두고, 사용자가 관리하는 안전한 새 sibling path에 원격
인수 branch의 worktree를 만든다. 경로는 실제 환경에서 충돌하지 않는지 먼저
확인한다.

```powershell
git fetch origin
git worktree add --detach "<NEW_HANDOFF_WORKTREE>" origin/codex/s0-order-eight-public-vector-independent-verification-v02
```

worktree는 편집 격리일 뿐 비밀 보안 경계가 아니다. sealed, oracle, 개인·비밀
자료를 새 공개 worktree에 복사하지 않는다.

### 5.4 clone이 전혀 없는 경우

```powershell
git clone --branch codex/s0-order-eight-public-vector-independent-verification-v02 https://github.com/shotgun1107/human-ai-development-tradition.git
```

### 5.5 수신 동일성 확인

인수 경로에서 다음을 확인한다.

```powershell
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git rev-parse origin/codex/s0-order-eight-public-vector-independent-verification-v02
git status --porcelain=v1
git diff --exit-code origin/codex/s0-order-eight-public-vector-independent-verification-v02 -- .
git diff --cached --exit-code HEAD -- .
git ls-files -t
```

조건은 local/remote HEAD 일치, local/remote tree 일치, clean status, 두 diff
성공, skip-worktree entry 없음이다. 이 검증은 Git-tracked tree 동일성을
보일 뿐 두 PC의 대화, temp, `.git`, cache, untracked/ignored 파일과 물리적
줄바꿈 설정까지 같다는 뜻은 아니다.

## 6. 집 CONTROL이 먼저 읽을 파일

동기화 검증 뒤 다음 순서로 읽는다.

1. `AGENTS.md`
2. 이 파일
3. `s0-lab/control/handoffs/company-to-home-2026-08-10/home-local-resume-prompt-v0.1.md`
4. `s0-lab/reviews/isolation/order-eight-public-vector-v0.1/independent-verification-v0.2.md`
5. `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-review-input-boundary-revision-v0.1.md`
6. `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-independent-verification-brief-v0.2.md`

각 Markdown은 same-basename sidecar가 있으면 읽기 전에 인증한다. 새 환경에서
validator를 신뢰하기 전에 다음을 실행한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File s0-lab/control/tools/verify-text-artifacts.ps1 -SelfTest
```

F0-SEALED 세 경로는 읽을 파일 목록이 아니다. 다음 path/count 검사만 허용된다.

```powershell
git ls-tree -r --name-only HEAD -- s0-lab/control/f0-sealed
git ls-tree -r --name-only HEAD -- s0-lab/f0-sealed-staging
git ls-tree -r --name-only HEAD -- s0-lab/reviews/f0-sealed
```

예상 파일 수는 각각 32, 11, 10이며 합계 53이다.

## 7. 다음 작업 경계

동기화 세션은 상태 보고 후 멈춘다. 다음 boundary revision은 사용자가 현재
집 스레드에서 다음 정확한 게이트를 다시 열었을 때만 시작한다.

```text
S0 V0.14 ORDER-EIGHT PUBLIC VECTOR REVIEW INPUT BOUNDARY REVISION OPEN
```

그 revision의 최소 범위는 다음과 같다.

1. 실제 공식 LF bytes 또는 엄격한 CRLF→LF 정규화 중 하나를 명시적으로 선택
2. 전체 길이/hash와 두 slice의 offset/length/hash 재계산
3. 숫자 `p`, `d`, `L`과 encode/decode/addition 조각이 분리된 공식 자료
   경계에서 실제로 재현되는지 확인
4. browser, search, alternate mirror와 author answer-key fallback 금지 유지
5. predecessor 문서와 실패 보고서의 역사성 보존
6. 수정된 brief를 fresh reviewer가 사용할 수 있도록 동결

경계 수정만으로 벡터가 맞다고 주장하지 않는다. 수정 뒤 다음 exact review
gate를 별도로 열고 zero-finding 결과를 받아야 한다. 그 뒤에도 최종 동결은
별도 CONTROL gate다.

## 8. 계속 닫혀 있는 범위

- trust-root 또는 role-isolation 구현
- Ed25519 key, anchor, registry 또는 signature 생성
- private/protected material
- VM, sandbox, account, network, clipboard, Git 제한 구성
- fixture, bank, label, condition map, hidden oracle
- executor A–D, provider/model session, judge, scoring, statistics
- E0 또는 S0 실행
- 중앙 전통 시스템과 Project Brain 통합
- 운영 안전성, 경제성, 장기 전승 효과 주장
- 벡터 계보의 `main` 병합

F0-SEALED 53개 파일의 Git 보존은 위 항목의 구현·실행 승인이 아니며, 그
내용을 이번 벡터 작업의 입력으로 추가하지 않는다.

## 9. 인수 완료 보고 항목

집 CONTROL은 다음을 사용자에게 과거·현재·미래 순서로 보고하고 멈춘다.

1. 기존 집 저장소의 branch, HEAD, 변경·stash·local-only commit 여부
2. 사용한 동기화 방법: 기존 clean branch, 별도 worktree 또는 clone
3. remote/local commit과 tree 동일성, status와 diff 결과
4. `origin/main`과 인수 branch의 관계
5. 회사가 dirty `main`을 보존하고 clean worktree로 작업한 이유
6. 벡터 작성, 두 번의 `INVALID-REVIEW`, 현재 LF/CRLF 결함
7. 벡터가 아직 검증·동결되지 않았다는 사실
8. 다음 정확한 boundary revision gate와 계속 닫힌 범위
9. F0-SEALED 세 경로가 각각 32/11/10 files로 Git tree에 존재하지만
   default-deny 입력이라는 사실
