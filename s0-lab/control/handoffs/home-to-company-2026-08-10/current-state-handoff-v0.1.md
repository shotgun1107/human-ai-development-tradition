# 집 CONTROL에서 회사 CONTROL로 보내는 동기화 인수인계 v0.1

- 작성 기준일: `2026-08-10` KST
- 저장소: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- 활성 기준선: `central-system-v2.1-s0-preparation`
- 회사 정본 branch: `codex/s0-order-eight-public-vector-independent-verification-v02`
- 확인된 정본 HEAD: `b857545113058321dd4d65f601c2d5ad8cceeec0`
- 확인된 정본 tree: `655bea08eb117a565bccc9241fb3361ce3c8f1d8`
- 필수 payload commit: `85ad19ba6703f43b1209a13164d1e28a4b62f6a4`
- 확인된 `origin/main`: `5add6e5e1675793ad179e98e51ffa1515feb3db8`
- 이 문서의 성격: 집 PC 동기화 결과와 회사 PC 재개 절차의 공개 기록
- 비의미: 구현, 벡터 검증·동결, sealed 입력 허가, S0/E0 실행 승인 아님

이 문서는 집 Codex의 대화 기억을 회사 PC에 전달하지 않는다. 회사 CONTROL은
실제 Git 상태, live remote refs, 이 문서와 SHA-256 기록만 근거로 인수한다.
기록된 SHA는 검증 기준이며, 실제 원격이 이후 정상적으로 전진했다면 원격을
되돌리는 데 사용하지 않는다.

## 1. 집 PC에서 수행한 작업

### 1.1 기존 저장소 감사

기존 집 저장소는 다음 경로였다.

`C:\Users\kimsiyeol\Documents\human-ai-development-tradition`

처음 확인한 상태는 다음과 같다.

- origin은 지정된 GitHub 저장소와 일치했다.
- branch는 `codex/s0-trust-root-role-isolation-design-v02`였다.
- HEAD는 `cb4198f4475881ba5b607517fdbb4f0db6b8ce5d`였다.
- modified, staged, untracked, ignored 파일과 stash가 없었다.
- 로컬 remote-tracking ref만 기준으로 local-only처럼 보인 5개 commit은 live
  `git ls-remote`와 ancestry 확인 결과 모두 실제 원격 branch에서 도달
  가능했다. 실제 local-only commit은 확인되지 않았다.

### 1.2 최초 안전 clone

회사→집 시작 프롬프트가 기존 폴더의 pull, switch, checkout, reset, clean,
stash, rebase와 merge를 명시적으로 금지했으므로 처음에는 새 sibling 경로에
단일 branch clone을 만들었다.

`C:\Users\kimsiyeol\Documents\human-ai-development-tradition-sync-b857545`

그 clone에서 다음을 확인했다.

- HEAD `b857545113058321dd4d65f601c2d5ad8cceeec0`
- tree `655bea08eb117a565bccc9241fb3361ce3c8f1d8`
- payload object type `commit`
- payload commit이 HEAD의 조상임
- status, unstaged diff와 staged diff가 모두 깨끗함

이 sibling clone은 삭제하지 않았으며 보조 안전 복사본으로 남아 있다. 현재
주 작업 경로의 정본 여부를 대신하는 별도 계보가 아니다.

### 1.3 기존 폴더의 in-place 동기화

사용자가 집·회사 PC를 번갈아 사용하므로 기존 폴더를 직접 동기화하는 운영
방식으로 정정했다. 기존 폴더가 깨끗하고 local-only 자료가 없음을 이미
확인했으므로 다음을 순차적으로 수행했다.

1. `origin` fetch 범위를 모든 heads로 확장했다.
2. `git fetch --prune origin`으로 전체 원격 branch refs를 갱신했다.
3. 정본 branch의 exact remote SHA가 `b857545...`인지 확인했다.
4. 기존 작업 폴더를 정본 branch로 전환하고 upstream을 연결했다.
5. `git pull --ff-only`가 `Already up to date`인지 확인했다.

최종 집 주 작업 경로 상태는 다음과 같다.

- branch: `codex/s0-order-eight-public-vector-independent-verification-v02`
- HEAD: `b857545113058321dd4d65f601c2d5ad8cceeec0`
- tree: `655bea08eb117a565bccc9241fb3361ce3c8f1d8`
- upstream: 같은 이름의 `origin` branch
- working tree: clean
- 이 handoff에서 `AGENTS.md`에는 향후 사용자가 cross-PC 또는 cross-session
  handoff package를 명시적으로 요청하면, 공개 handoff-only 산출물의 exact
  staged scope와 게시 적격성을 확인한 뒤 별도 재승인 없이 전용 handoff
  branch에 commit·push한다는 운영 규칙을 추가했다. 이 자동 승인은 sealed,
  secret, personal 자료, PR, `main` 병합, history rewrite 또는 삭제를 포함하지
  않는다.

이 인수인계 branch는 위 정본 commit에서 갈라져 이 공개 handoff package와
위 handoff 자동 게시 운영 규칙만 추가한다. order-eight 후보·검토 기록과
sealed 자료 자체는 수정하지 않는다.

## 2. F0-SEALED 경계

다음 세 경로는 Git에 추적되어 있어도 `AGENTS.md`상 default-deny다.

- `s0-lab/control/f0-sealed/**`
- `s0-lab/f0-sealed-staging/**`
- `s0-lab/reviews/f0-sealed/**`

집 동기화 세션은 Git path inventory로 파일 수만 확인했다.

| 경로 | 확인된 tracked file 수 |
|---|---:|
| `s0-lab/control/f0-sealed/` | 32 |
| `s0-lab/f0-sealed-staging/` | 11 |
| `s0-lab/reviews/f0-sealed/` | 10 |
| 합계 | 53 |

집 CONTROL은 이 파일들의 내용, filename 목록, hash, 의미, 정답, oracle 또는
내부 구조를 열거나 검색하거나 요약하지 않았다. 정확한 F0-SEALED gate와
role별 allowlist가 없는 CONTROL, executor, judge, public reviewer는 앞으로도
접근하지 않는다. 무단 read가 있으면 해당 역할의 종속 증거를 무효로 하고
즉시 중단한다.

이 규칙은 절차적 통제다. Git clone이나 worktree 자체는 비밀 보안 경계가
아니며, 실제 시험 전의 별도 접근격리 요구는 여전히 닫힌 작업이다.

## 3. 인수한 프로젝트 상태

회사→집 인수 문서에 따르면 order-eight 공개 벡터는 미래의 strict Ed25519
검증기가 거부해야 할 공개 음성 시험값이다. 현재까지 독립 검증은 두 번 모두
`INVALID-REVIEW`였으며 벡터의 수학적 정오 판정까지 도달하지 않았다.

두 번째 실패 원인은 공식 RFC 입력 고정의 LF/CRLF 불일치다.

- 실제 공식 응답: LF, 103,210 bytes,
  SHA-256 `ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3`
- 경계 문서가 HTTP 원문으로 선언한 값: CRLF 변환본, 106,573 bytes,
  SHA-256 `f13ab006baa1a30a7835113927e9d23ca9d9c460f352e721cbcdff8adbf1dee9`

fail-closed 처리로 reviewer는 RFC slice 노출, 독립 벡터 계산과 후보 비교를
수행하지 않았다. 따라서 벡터는 통과·실패·동결 중 어느 상태도 아니다.

현재 다음 후보 게이트는 아래 boundary revision이지만 이 문서와 동기화
작업이 대신 열지 않는다.

```text
S0 V0.14 ORDER-EIGHT PUBLIC VECTOR REVIEW INPUT BOUNDARY REVISION OPEN
```

구현, key/anchor/registry, VM·역할 격리, fixture, bank, label, oracle,
executor A-D, provider/model, judge, scoring, 통계, E0와 S0 실행 및 `main`
병합은 계속 닫혀 있다.

## 4. 회사 PC가 동기화할 때

회사 기존 저장소를 우선 사용한다. 먼저 path, origin, branch, HEAD, upstream,
status, stash, worktree와 local-only commit을 읽기 전용으로 확인한다.

- 완전히 clean하고 원격에 없는 commit이 없으면 전체 heads를 fetch한 뒤
  정본 또는 handoff branch로 switch하고 `pull --ff-only`를 사용한다.
- modified, staged, untracked, ignored, stash 또는 local-only commit이 있으면
  pull, switch, reset, clean, stash, rebase, merge 또는 파일 덮어쓰기를 하지
  않는다. 상태와 영향 경로만 보고하고 사용자의 결정을 기다린다.
- sealed 세 경로는 path/count/tracked state 외에는 확인하지 않는다.

회사 CONTROL은 live 원격에서 이 handoff branch를 직접 읽고 다음을 확인한다.

1. handoff tip이 `b857545...`를 조상으로 포함한다.
2. `b857545...`의 tree가 위 기록과 일치한다.
3. payload `85ad19b...`가 handoff tip의 조상이다.
4. 수신 worktree가 clean하고 local/remote HEAD가 일치한다.
5. 최신 `AGENTS.md`를 가장 먼저 적용한다.
6. 이 문서와 회사 재개 프롬프트의 sidecar가 일치한다.

## 5. 집 세션에서 하지 않은 일

- order-eight boundary revision 또는 독립 검증
- 코드·validator·helper 구현 또는 테스트
- sealed 내용 열람·검색·계산·전달
- key, fixture, bank, oracle, executor 또는 모델 실행
- PR 또는 `main` 병합
- 다음 실험 게이트 개방

이 handoff package의 문서·sidecar 작성, 위 제한된 `AGENTS.md` 운영 규칙과
Git 보존 외에는 프로젝트 산출물을 변경하지 않았다.
