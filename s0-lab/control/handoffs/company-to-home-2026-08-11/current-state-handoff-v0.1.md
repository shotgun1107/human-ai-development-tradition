# 회사 CONTROL에서 집의 기존 CONTROL 작업으로 보내는 인수인계 v0.1

- 작성일: `2026-08-11` KST
- 저장소: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- 원격 `main`: `aa68f797ff4be1175048d8329f98d3c469dfb904`
- 인수인계 브랜치: `codex/company-to-home-handoff-20260811`
- 인수인계 브랜치의 작성 기준 부모: `aa68f797ff4be1175048d8329f98d3c469dfb904`
- 활성 설계 기준선: `central-system-v2.1-s0-preparation`
- 다음 기술 작업: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION CANDIDATE OPEN`
- 성격: 회사에서 확인한 Git 정본, 동기화 문제와 해결, 현재 기술 상태, 집에서의 재개 경계
- 비의미: S0·E0·중앙 시스템·Project Brain·운영 안전성·경제성의 구현 또는 검증 완료가 아님

이 문서는 새 대화를 위한 일반 소개문이 아니다. 오늘 이 프로젝트를 이미 다룬
집 PC의 기존 CONTROL 작업이 회사의 최신 Git 상태를 받아 곧바로 이어가기 위한
기록이다. 과거 대화 기억보다 Git 상태, 이 문서, 인증된 공개 산출물을 우선한다.

## 1. 한 줄 결론

역할 격리 v0.4 설계와 order-eight 공개 벡터의 검증·동결은 `main`에 들어갔고,
53개 F0 자료도 빠짐없이 Git으로 동기화된다. 오늘 발견한 문제는 Git이 아니라
`sealed`를 “Git 비공개”와 “AI 입력 금지”로 섞어 쓴 규칙이었으며, 이를
`PUBLIC-GIT / AI-CONTENT-DEFAULT-DENY` 두 축으로 분리해 고쳤다. 다음 작업은
정책을 더 강화하는 것이 아니라 아직 시작하지 못한 공개 구현 후보 작업이다.

## 2. 과거: 원래 기술 작업은 어디까지 왔나

### 2.1 trust-root와 role-isolation 설계

S0 v0.14의 공개 trust-root/role-isolation 설계는 v0.4까지 수정됐다.
독립 심사는 blocking, major, minor 모두 0건으로 통과했고 CONTROL은 이를 현재
공개 설계 기준선으로 채택했다.

주요 확정 사항은 다음과 같다.

- import event는 정확한 31개 필드와 순서를 갖는다.
- global chain과 route-local chain은 서로 다르며 둘 다 필요하다.
- 성공, 거절, 실패, 충돌, 중단의 상태 전이는 정해진 경우만 허용한다.
- 성공을 추측하거나 실패 후 재시도해 권한을 얻는 경로를 두지 않는다.
- A-D 조건의 정보·권한·모델·시간·출력·채점 기회를 동일하게 유지한다.

이는 공개 설계 문서가 통과했다는 뜻이다. parser, ledger, signer, appliance,
격리 환경이나 실제 실행기가 구현됐다는 뜻은 아니다.

기준 문서:

- `s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.md`
- `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md`
- `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md`
- `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md`

### 2.2 order-eight 공개 벡터

과거 검증은 입력 경계와 줄바꿈 처리 문제로 여러 번 `INVALID-REVIEW`가 됐다.
벡터 값 자체의 실패가 아니라 검증기가 공식 RFC 자료를 안전하게 읽는 계약이
틀렸거나 불완전했던 것이 원인이었다.

최종 v0.4 독립 검증에서는 공식 RFC 입력 경계, 독립 사전 계산, 후보와의 비교,
엄격한 거부 위치가 모두 통과했다. 네 개 공개 벡터는 CONTROL 최종 동결을
받았고 그 계보는 `main`에 반영됐다.

기준 문서:

- `s0-lab/reviews/isolation/order-eight-public-vector-v0.1/independent-verification-v0.4.md`
- `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-control-final-freeze-decision-v0.1.md`

이 동결은 공개 시험 벡터의 증거만 확정한다. key 생성, signature 실행,
protected material, provider/model, E0 또는 S0를 열지 않는다.

## 3. 오늘 회사에서 실제로 발생한 동기화 문제

### 3.1 보이는 증상

세 F0 경로가 공개 Git에 들어 있어도 일부 문서와 에이전트는 계속 다음처럼
해석했다.

- `sealed`이므로 commit/push하면 안 된다.
- 다른 PC로 전달하면 안 된다.
- public worktree에 존재하면 유출이다.
- 동기화할 때 제외해야 한다.

이 해석을 따르면 새 PC에서 53개가 빠지거나, 에이전트가 정상 push를 거부하거나,
기존 계보와 다른 불완전한 tree를 만들 수 있다. 사용자가 과거에 겪은 “후속
작업에 필요한 파일이 없어 하루를 잃는 문제”를 다시 만들 수 있는 상태였다.

### 3.2 실제 원인

Git 자체는 정상 작동하고 있었다. 세 경로는 이미 tracked 상태였고 clone,
fetch, checkout, pull, push에서 제외하는 ignore, sparse checkout, submodule,
LFS 규칙은 없었다.

진짜 원인은 문서의 용어 충돌이었다.

1. 한쪽은 53개를 Git으로 보존해야 한다고 썼다.
2. 다른 쪽은 bare `sealed`라는 단어만 보고 게시 금지라고 썼다.
3. 오래된 시작 문서와 인수인계 문서가 현재 규칙처럼 연결돼 있었다.
4. 에이전트는 안전한 쪽으로 판단하면서 더 넓은 게시 금지를 선택했다.

즉 기억력 부족만의 문제가 아니라, 같은 저장소 규칙이 서로 반대 행동을
요구하는 정책 결함이었다.

## 4. 어떻게 해결했고 무엇을 우회했나

### 4.1 분류를 두 축으로 분리

현재 정본 규칙은 다음처럼 나눈다.

| 구분 | 의미 |
|---|---|
| `PUBLIC-GIT` | Git tree에 추적하고 모든 PC로 빠짐없이 동기화한다. |
| `AI-CONTENT-DEFAULT-DENY` | 정확한 역할 gate와 입력 목록 없이는 내부 AI가 내용을 읽거나 유추에 사용하지 않는다. |
| `NONPUBLIC-OUT-OF-REPO` | hidden oracle, credential, private key, 개인정보, 실제 고객·비밀 자료처럼 Git에 넣지 않는 진짜 비공개 자료다. |

세 F0 경로의 현재 분류는 첫째와 둘째가 동시에 적용되는 상태다. 공개 Git에
존재하지만 평가 대상 AI와 내부 CONTROL/검증 AI의 일반 입력은 아니다.

### 4.2 기존 작업을 덮지 않는 방식

정책 감사와 수정은 별도 clean worktree와
`codex/public-sync-default-deny-policy-audit-v01` 브랜치에서 수행했다. 이
방식은 편집 충돌을 피하기 위한 것이며 비밀 보안 경계라고 주장하지 않는다.

F0 내부 내용이나 내부 파일명은 읽지 않았다. 상위 경로, tracked 여부,
32/11/10이라는 합계, quiet diff 결과만 사용했다.

### 4.3 인증 문제의 실제 처리

GitHub CLI의 `gh auth status`는 저장된 `gh` token을 invalid로 보고했다.
그러나 HTTPS Git push는 `gh` token이 아니라 Git Credential Manager에 저장된
별도 자격증명을 사용하고 있었다. 실제 Git dry-run과 push가 성공했으므로,
PR이나 GitHub API가 필요 없는 작업에서 `gh` 실패를 Git push 실패로 오인하지
않도록 정리했다.

임시 worktree는 sandbox 사용자에게 ownership 경고가 났다. 전역 설정을
바꾸지 않고 승인된 명령에 한해 해당 worktree를 `safe.directory`로 지정해
검증과 push를 수행했다.

### 4.4 main 반영 중 발생한 도구 오류

원격 `main` push 전 검증 스크립트가 세 번 중단됐다.

1. PowerShell 함수 인수명이 예약 변수와 충돌했다.
2. 한 줄 Git 출력을 문자 배열처럼 처리했다.
3. 정상적인 `git fetch` 진행 메시지를 PowerShell이 오류 스트림으로 취급했다.

세 경우 모두 push 전에 멈췄고 저장소 내용은 바뀌지 않았다. 마지막에는 Git
종료코드를 직접 확인하고 stderr를 일반 오류 조건으로 처리하도록 바꿨다.
그 뒤 정확한 commit을 `main`으로 fast-forward push하고 원격 SHA를 다시
확인했다.

이것은 보안 우회가 아니다. 사용자의 명시적 `main` 승인 뒤, sandbox와
PowerShell의 실행 차이를 처리한 것이다.

## 5. 과잉 구현 감사의 결론

정책 수정 과정에서 Blue/Sol 재심이 새로운 fail-closed 조건을 계속 추가했다.
stderr 완전 숨김, 모든 Git 실패코드의 별도 처리, clone/switch/merge/worktree
세부 검증, remote ref race 방어, payload에서 target까지의 추가 quiet diff 등이
확대됐다.

사용자가 실제 위협 모델을 다시 명확히 한 뒤 작업을 멈추고 재평가했다.

- F0는 세상 누구에게도 비밀이어야 하는 자료가 아니다.
- 목표는 평가 대상 AI와 프로젝트 내부 AI가 시험 자료를 미리 봐 평가가
  오염되는 것을 막는 것이다.
- 신뢰된 외부 사람/AI는 직접 확인할 수 있다.
- 내부 AI에는 pass/fail, count, hash 일치 같은 최소 결과만 전달하면 된다.

최종 판단은 **B: 과잉 구현된 부분은 있지만 그대로 두어도 문제없으므로 작업
종료**였다. 이미 들어간 방어를 되돌리지 않았지만 추가 강화와 재심 루프도
중단했다. 집 CONTROL은 구체적인 F0 노출 경로나 명백한 규칙 위반이 없는 한
새 정책 감사, 새 Blue/Sol 심사, 새 Git 방어 설계를 시작하지 않는다.

## 6. 회사에서 오늘 실제로 완료한 것

1. 정책 감사 산출물과 수정 19개 공개 파일을 commit했다.
2. 정책 브랜치를 원격에 push했다.
3. 원격 `main`이 정책 브랜치의 조상인지 확인했다.
4. `main` 전용 명시 승인을 받은 뒤 한 commit을 fast-forward했다.
5. 원격 `main`이 `aa68f797ff4be1175048d8329f98d3c469dfb904`인지 재확인했다.
6. `main` 반영 범위가 공개 파일 19개이며 F0 세 경로의 diff가 0인지 확인했다.
7. F0 Git tree 수량이 32/11/10, 합계 53인지 확인했다.
8. 회사 로컬 `main`도 원격 `main`과 같은 commit으로 fast-forward했다.
9. 이 인수인계를 위해 `codex/company-to-home-handoff-20260811` 브랜치를
   `aa68f797...`에서 만들었다.

정책 commit:

```text
aa68f797ff4be1175048d8329f98d3c469dfb904
fix: separate F0 sync from AI read access
```

정책 감사 문서:

- `docs/operations/policy-audits/public-sync-default-deny-v0.1/audit-report.md`
- `docs/operations/policy-audits/public-sync-default-deny-v0.1/exploration-log.md`
- `docs/operations/policy-audits/public-sync-default-deny-v0.1/minimal-rule-revision-proposal.md`

## 7. 현재 Git 정본과 동기화 불변식

| 항목 | 현재 값 |
|---|---|
| 원격 `main` | `aa68f797ff4be1175048d8329f98d3c469dfb904` |
| 회사 로컬 `main` | `aa68f797ff4be1175048d8329f98d3c469dfb904`로 fast-forward 완료 |
| handoff branch | `codex/company-to-home-handoff-20260811` |
| handoff 작성 기준 부모 | `aa68f797ff4be1175048d8329f98d3c469dfb904` |
| F0 aggregate | 32 / 11 / 10 = 53 |
| 정책 반영 전후 F0 diff | 없음 |
| 특별 index flag | 없음 |
| unclassified ignored | 없음 |
| 회사 로컬 disposable ignored | 존재하며 `.venv-docs`, `.mkdocs-site`, Python cache 계열뿐 |

이 문서의 최종 commit은 self-reference를 피하기 위해 문서 안에 기록하지
않는다. 집 CONTROL은 fetch 후 원격 handoff branch의 live tip을 직접 pin하고,
그 tip이 `aa68f797...`을 조상으로 포함하는지 확인한다.

## 8. 현재 기술 상태와 다음 작업

현재까지 확정된 것은 다음 두 가지다.

1. trust-root/role-isolation v0.4 공개 설계가 CONTROL 기준선으로 채택됐다.
2. 그 설계가 요구한 order-eight 공개 벡터가 독립 검증을 통과하고 동결됐다.

아직 하지 않은 것은 공개 구현 후보다. 사용자가 회사 세션에서 정확히 다음
gate를 열었으나, F0 동기화 정책 문제를 먼저 해결하느라 구현 작업을 진행하지
못했다.

```text
S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION CANDIDATE OPEN
```

집 CONTROL의 다음 실제 작업은 이 gate를 이어받아 공개 설계를 최소한의 공개
구현 후보로 옮기는 것이다. 먼저 기존 public runtime/I1 경계, v0.4 설계,
authority matrix, acceptance plan, 동결 벡터와 현재 구현 파일의 관계를 좁은
입력 목록으로 확인하고, 구현 범위와 출력 경로를 고정한 뒤 작업한다.

이 gate가 허용하지 않는 것은 계속 닫혀 있다.

- F0 내부 내용 읽기·검색·요약·유추
- hidden oracle 또는 정답 제작·열람
- 실제 key 또는 private/protected material 생성
- provider/model session, executor A-D, judge, scoring
- E0 또는 S0 실행
- 중앙 전통 시스템 또는 Project Brain 구현
- 운영 안전성·경제성·실험 효과 검증 완료 주장
- `main` 병합, PR, release, branch 삭제

## 9. 집 PC에서 안전하게 동기화하는 원칙

집의 기존 저장소와 기존 CONTROL 작업을 그대로 사용한다. 새 clone이나 새
Codex 작업을 기계적으로 만들지 않는다.

### 9.1 먼저 보존할 것

집 저장소의 origin, branch, HEAD, upstream, working tree, index, untracked,
ignored, stash, local-only commit을 먼저 확인한다. 파일명 출력은 현재 공개
allowlist로 제한하고 그 밖의 상태는 합계만 보고한다.

다음 중 하나라도 있으면 기존 worktree에서 switch, merge, reset, clean,
stash, rebase, checkout 또는 덮어쓰기를 하지 않는다.

- modified, staged 또는 untracked 작업 존재
- unclassified ignored 파일 존재
- stash 존재
- 원격에 없는 local-only commit 존재
- detached HEAD
- 다른 origin
- F0 aggregate가 32/11/10이 아님
- F0 worktree/index diff, untracked, ignored, special-index flag가 0이 아님

이 경우 기존 작업을 그대로 두고, fetch한 exact handoff tip으로 별도 clean
worktree를 만든다. worktree는 편집 충돌 방지 수단이지 비밀 보안 경계가 아니다.

### 9.2 깨끗할 때 받을 정본

1. 모든 원격 ref를 fetch한다.
2. `origin/main`을 `aa68f797...` 이상으로 확인한다.
3. `origin/codex/company-to-home-handoff-20260811`의 live tip을 pin한다.
4. live tip이 `aa68f797...`을 조상으로 포함하는지 확인한다.
5. target tree의 F0 aggregate가 32/11/10인지 확인한다.
6. 검증한 exact target commit으로만 fast-forward 또는 새 worktree를 만든다.
7. local HEAD와 remote tip, tree, clean status와 diff를 다시 확인한다.

동기화는 Git이 관리하는 전체 tree와 디렉터리 구조를 전달한다. Codex 대화,
`.venv`, `.mkdocs-site`, cache, OS 설정, Git credential과 임시 파일은 전달하지
않는다. 후속 작업에 필요한 정본 프로젝트 파일은 handoff branch에 포함돼야
하며, 집 CONTROL은 문서 pair의 인증과 Git tree 동일성으로 이를 확인한다.

## 10. 집 CONTROL이 읽을 공개 파일

동기화 후 다음 순서로 읽는다.

1. `AGENTS.md`
2. 이 문서와 same-basename sidecar
3. `docs/operations/policy-audits/public-sync-default-deny-v0.1/audit-report.md`
4. `s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.md`
5. `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md`
6. `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md`
7. `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md`
8. `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-control-final-freeze-decision-v0.1.md`

same-basename sidecar가 있는 공개 Markdown은 읽기 전에 인증한다. 새 PC 환경에서
canonical validator를 신뢰하기 전에 SelfTest를 먼저 실행한다.

세 F0 경로는 위 공개 입력 목록에 포함되지 않는다. 동기화 역할은 상위 경로와
32/11/10 합계, tracked/quiet-diff 결과만 확인한다.

## 11. 집에서 이어갈 작업 순서

1. 기존 집 저장소를 보존 검사한다.
2. handoff branch를 exact commit으로 동기화한다.
3. Git 동일성과 F0 aggregate만 확인한다.
4. 이 문서와 공개 기준 문서를 인증해 읽는다.
5. 사용자에게 과거·현재·미래 순서로 짧게 인수 결과를 보고한다.
6. 동기화가 통과하면 같은 작업에서 공개 구현 후보 gate를 이어간다.
7. 좁은 입력 목록과 구현 대상 파일을 먼저 고정한다.
8. 공개 구현 후보와 공개 검증만 수행한다.
9. F0, hidden oracle, provider/model, E0/S0는 건드리지 않는다.
10. 집에서 material한 작업이 생기면 별도 branch에 보존하고 다음 회사 인수를
    위한 최신 handoff를 갱신한다.

## 12. 확인 범위와 미확인 범위

확인한 사실:

- 원격과 회사 로컬 `main`이 `aa68f797...`로 맞춰졌다.
- 정책 반영은 공개 파일 19개이며 F0 diff는 없다.
- F0 Git tree aggregate는 32/11/10이다.
- trust-root/role-isolation v0.4 설계는 공개 설계 수준에서 통과했다.
- order-eight 공개 벡터는 독립 검증과 CONTROL 동결을 완료했다.
- 공개 구현 후보는 아직 산출물이 없다.

확인하지 않았거나 주장하지 않는 것:

- F0 내부 파일명·내용·정답·oracle
- 집 PC의 현재 dirty/clean 상태와 local-only 작업
- 실제 trust-root/role-isolation 구현의 동작
- 실제 S0 또는 E0 효과
- 중앙 전통 시스템의 운영·비용·장기 효과

집 CONTROL은 집 PC의 실제 Git 상태를 새로 확인해야 한다. 이 문서는 그 결과를
미리 단정하지 않는다.
