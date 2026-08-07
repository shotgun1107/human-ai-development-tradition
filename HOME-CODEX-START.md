# 집 Codex 시작점

- 문서 상태: `CONTROL 인수인계 v0.2`
- 기준 시각: `2026-08-07` (KST)
- 저장소: `https://github.com/shotgun1107/human-ai-development-tradition`
- 활성 기준선: `central-system-v2.1-s0-preparation`
- 용도: 새 PC·새 Codex 세션이 저장소를 읽고 프로젝트 이해를 보고한 뒤, 공홈 CONTROL 프로젝트의 정합성 검사를 거쳐 작업을 재개하기 위한 시작점

이 문서는 과거 대화를 증거로 대신하지 않는다. 새 세션은 반드시 현재 Git 상태, `AGENTS.md`, 동결 문서와 SHA-256 sidecar를 다시 확인해야 한다.

## 1. 프로젝트가 만드는 것

이 프로젝트는 모델을 파인튜닝하거나 동일한 AI 인격을 유지하는 시스템이 아니다. 여러 프로젝트에서 확인된 경험·Skill·판단 규칙·실패·반례를 모델 밖의 문서로 보존하고, 다음 AI 세션이 이를 검색·적용·재검증하도록 만드는 인간–AI 공동 작업 전통을 연구한다.

현재는 설계와 합성 시험 준비 단계다. 다음은 아직 구현되거나 검증되지 않았다.

- S0 실행과 표현 후보의 유효성
- 전통이 다음 작업을 개선하는 E0 효과
- 중앙 전통 시스템과 Project Brain 연결
- 실제 운영 안전성·경제성·모델 간 전승

## 2. 이 문서를 만들 때 확인한 Git 상태

| 항목 | 확인값 |
|---|---|
| 공개 기본 브랜치 | `main` |
| 인수인계 v0.2 작성 직전 `main` 및 `origin/main` | `29fb8aa86ce840310ccb278bd5d9c7f7caa19b16` |
| E0 설계 브랜치 | `codex/e0-effect-test-design` |
| E0 설계 HEAD 및 원격 HEAD | `84014378b48466c185e13cadd6b9a07549ffbaee` |
| E0와 `main`의 공통 기준점 | `6de2c6d9434ca2ff07f0c048a01b5f10bcae3b92` |
| S0 v0.5 브랜치 | 작성 시점에는 로컬·원격에 없음 |

이 문서를 포함한 최종 커밋은 위 `main` 값보다 뒤에 생긴다. 새 세션은 이 표를 현재 HEAD로 오해하지 말고 `git fetch` 후 실제 원격 상태를 다시 확인한다.

작성 PC의 `main` 작업 트리에는 `f0-sealed` 관련 미추적 경로가 있었다. 이번 문서 작업은 그 경로를 열거나 수정하거나 커밋하지 않았다. 미추적 봉인 경로는 Git으로 전달되지 않으며, 집 PC에서 보이지 않는 것이 정상이다. 어디에서든 보이면 공개 입력으로 취급하지 않는다.

### 저장소로 전달되는 것과 전달되지 않는 것

원격 저장소에는 공개하기로 한 연구·기획·설계, 게이트 규칙, 심사 결과, I0 결과와 E0 설계 후보가 보존돼 있다. 다만 모든 파일이 `main` 작업 폴더에 동시에 보이는 것은 아니다. `main`을 pull하면 `main` 파일이 보이고, E0 설계는 별도 원격 브랜치를 확인해야 한다.

다음은 Git 인수인계 대상이 아니다.

- Codex와 공홈의 대화 기록 및 모델 내부 기억
- 하위 에이전트가 대화에서만 제안하고 파일로 남기지 않은 분석
- 아직 작성되지 않은 S0 v0.5 후보
- 커밋하지 않은 봉인·staging·hidden-oracle 자료

따라서 새 Codex는 “저장소에 있는 사실”과 “이전 세션에만 있었던 생각”을 구분하고, 후자를 이미 승인된 기준처럼 복원하려 하지 않는다.

## 3. 현재 CONTROL 상태

### 완료되었지만 의미가 제한된 것

- F0-PUBLIC v0.1은 공개 범위에서 통과·동결됐다.
- I0 공개 최소 harness 후보와 F0-PUBLIC refreeze는 지정 범위에서 검토·동결됐다.
- 이는 공개 형식과 연결 로직의 제한된 준비가 끝났다는 뜻이지 S0 실행, 중앙 시스템 구현 또는 효과 검증이 아니다.

### 실패하여 다시 설계해야 하는 것

- F0-PUBLIC 질문 계약 URC v0.4는 독립 심사에서 `Critical 4`, `Major 3`, `Minor 1`로 거부됐다.
- v0.4는 실패 증거로 보존하며 제자리에서 수정하지 않는다.
- 다음 후보는 별도 `v0.5` 경로에서 설계해야 한다. 아직 저장소에 v0.5 후보 문서는 없다.

### 별도 브랜치에서 설계만 끝난 것

- E0 v0.1 효과시험 설계 패키지는 `codex/e0-effect-test-design`에 있다.
- 다섯 Markdown과 다섯 sidecar만 `docs/tradition/e0-effect-test/`에 추가됐다.
- 상태는 `독립 심사 전 설계 후보`다. 자료, oracle, runner, 모델 실행, 채점과 효과 결론은 모두 닫혀 있다.
- 제안된 A/D 16-call 시험은 저비용 파일럿일 뿐 효과 통과시험이 아니다. 내용 고유 효과를 주장하려면 A/B/D 확인시험이 필요하며 C는 선택 진단이다.

## 4. 집 PC의 첫 단계: 검증과 이해 감사

저장소가 없다면 clone하고, 이미 있다면 기존 변경을 지우지 않는다. 저장소 루트에서 다음을 확인한다.

```powershell
git status --short --branch
git remote -v
git fetch origin --prune
git branch -a
git log --oneline --decorate -12
git worktree list --porcelain
```

그다음 아래 순서로 처리한다.

1. `AGENTS.md`를 먼저 전부 읽는다.
2. 현재 `main`이 `origin/main`과 같은지 확인한다.
3. E0 작업을 다룰 때만 `origin/codex/e0-effect-test-design`의 HEAD와 문서 sidecar를 확인한다.
4. 작업 트리가 더러우면 사용자 변경으로 간주한다. `reset --hard`, 강제 checkout 또는 광범위 삭제를 하지 않는다.
5. 과거 문서의 다른 PC 절대경로는 증거가 아니다. 현재 clone의 저장소 루트를 기준으로 경로를 해석한다.
6. 동결 입력의 SHA-256이 다르면 그 입력에 의존한 작업을 시작하지 않는다.

검증이 끝나도 바로 설계·구현을 시작하지 않는다. 새 CONTROL 세션은 먼저 프로젝트 목적, 사용자가 원하는 AI의 성장, 인간–AI 공동 전통, 현재 완료·미완료 상태, S0/E0 경계와 역할 구조를 자기 말로 설명하는 **이해 보고서**를 작성하고 멈춘다.

사용자는 이 보고서를 이미 온보딩된 공홈 `AI 개발 전통 — CONTROL & Reviews` 프로젝트에 전달한다. 공홈은 저장소를 대신 운영하거나 설계를 독립 심사하는 것이 아니라, 새 Codex의 이해가 축적된 목적·철학·방향과 맞는지를 검사한다. 공홈이 `ALIGNED`를 주거나 지적한 오해가 교정되기 전에는 실제 작업 게이트를 열지 않는다.

## 5. 이해 정합성 확인 뒤의 다음 두 작업

### S0 질문 계약 v0.5

- 권장 브랜치: `codex/s0-question-contract-v05`
- 출력 전용 경로: `s0-lab/control/f0-public/question-contract-v0.5/`
- 필요한 새 세션 게이트: `F0-PUBLIC QUESTION CONTRACT V0.5 REDESIGN OPEN`
- 목적: v0.4 실패를 해결하는 새 질문 계약을 설계하고 독립 심사 가능한 패키지로 만드는 것
- 금지: 봉인 자료 접근, 문제·정답 작성, schema·runner 구현, 실행, S0 결론

처음 읽을 공개 입력의 상한은 다음 문서와 각 sidecar다.

1. `AGENTS.md`
2. `docs/tradition/s0-e0-boundary-and-parallel-work.md`
3. `s0-lab/control/s0-protocol-v0.3.md`
4. `s0-lab/control/f0-public/question-contract-v0.4/universal-response-contract-v0.4-candidate.md`
5. `s0-lab/control/f0-public/question-contract-v0.4/public-falsification-plan-v0.1.md`
6. `s0-lab/reviews/f0-public/question-contract-v0.4/urc-v0.4-independent-review-v0.1.md`
7. `s0-lab/control/f0-public/question-contract-v0.4/independent-review/independent-review-decision-v0.1.md`

CONTROL이 별도 승인하기 전에는 범위를 넓히지 않는다. 설계자와 독립 심사자는 fresh session으로 분리한다.

### E0 효과시험 설계 심사

- 대상 브랜치: `codex/e0-effect-test-design`
- 대상 커밋: `84014378b48466c185e13cadd6b9a07549ffbaee`
- 다음 권장 게이트: `E0 EFFECT TEST DESIGN REVIEW OPEN`
- 목적: v0.1 설계가 전통 내용의 효과, 추가 토큰·일반 조언 효과, 위해와 비용을 실제로 구분할 수 있는지 적대적으로 검토
- 금지: E0 자료·oracle·prompt·runner 작성, 모델 실행, 채점, 효과 주장

엄격한 독립 심사는 이 프로젝트의 전체 대화 기억을 가진 세션에 맡기지 않는다. `e0-independent-review-brief-v0.1.md`의 최대 입력만 받은 fresh session 또는 별도 공홈 프로젝트를 사용한다. 공홈의 장기 CONTROL 프로젝트는 독립 증거가 아니라 맥락 유지·일반 검토·다음 지시 정리에 사용한다.

## 6. 권장 진행 순서

```text
집 Codex CONTROL: Git·해시 검증
  → 프로젝트 이해 보고서 작성 후 정지
  → 공홈 CONTROL 프로젝트: 이해 정합성 검사
  → 오해 교정 및 사용자 작업 게이트 개방
      ├─ S0 전용 worktree/session: v0.5 설계 후보 작성
      │    └─ fresh 독립 심사
      └─ E0 fresh 심사 session: v0.1 설계 읽기 전용 심사
                 ↓
            CONTROL 통합 판단
                 ↓
      통과한 설계에 대해서만 다음 자료 작성 또는 구현 게이트 검토
```

S0와 E0는 설계 단계에서는 병렬로 진행할 수 있다. 그러나 E0 자료 작성·구현·실행은 S0가 유효한 표현 후보와 연결 계약을 만들기 전까지 열지 않는다.

## 7. 첫 이해 보고서의 필수 내용

새 집 Codex CONTROL 세션은 첫 답변에서 다음을 보고하고 멈춘다.

- 실제 저장소 경로와 원격 URL
- 현재 branch·HEAD·upstream 관계
- `main`과 E0 원격 브랜치 확인값
- 작업 트리 변경과 봉인·비공개 후보의 존재 여부를 내용 열람 없이 구분한 결과
- 동결 입력 hash 검사 결과
- 프로젝트를 시작한 근본적인 이유
- 사용자가 원하는 “AI의 성장”이 의미하는 것과 의미하지 않는 것
- 인간과 AI가 함께 만드는 브랜드·전통의 의미
- 중앙 전통 시스템이 장기적으로 담당해야 할 역할
- 현재 완료된 것과 아직 구현·검증되지 않은 것
- S0와 E0가 각각 검증하려는 다른 질문
- CONTROL, 설계자, 하위 에이전트, 독립 심사자의 역할 차이
- worktree·세션 분리의 목적과 보안상 한계
- 앞으로의 작업 순서와 현재 열리지 않은 게이트
- 절대 해서는 안 되는 주장과 행동
- 아직 확신하지 못해 확인이 필요한 부분

확인되지 않은 과거 대화, 공홈 프로젝트 기억 또는 모델의 추측으로 누락된 Git 증거를 채우지 않는다.

## 8. 공홈 정합성 검사 방식

공홈 장기 CONTROL 프로젝트에는 이 인수인계 v0.2와 최신 `README.md`를 추가한 뒤 집 Codex의 이해 보고서 전체를 전달한다. 공홈은 다음 네 가지로 각 핵심 주장을 분류한다.

- `SUPPORTED`: 축적된 목적·철학·현재 기준과 일치
- `CONTRADICTED`: 기준과 충돌
- `UNSUPPORTED`: 저장소 또는 기준 없이 추측
- `OMITTED`: 이어받기 위해 필요한 핵심이 빠짐

한 번의 유창한 요약만으로 `ALIGNED`를 주지 않는다. 공홈은 설계 통과와 효과 검증의 혼동, S0/E0 혼합, worktree의 보안 경계 오해, 공홈과 독립 심사자의 역할 혼동, 게이트 자체 확대를 포함한 검증 질문을 만든다. 집 Codex의 추가 답변까지 비교한 뒤 `ALIGNED / PARTIALLY ALIGNED / MISALIGNED` 중 하나를 판정한다.

이 검사는 집 Codex의 **생각과 방향의 정합성**을 보는 것이다. 집 PC의 실제 Git·파일·해시는 집 Codex가 검증하며, 공홈의 기억으로 대체하지 않는다. 실제 설계 심사는 집 Codex가 정확한 역할과 allowlist를 가진 fresh 하위 에이전트 또는 별도 세션에 배분한다.

## 9. 집 Codex에 처음 넣을 프롬프트

아래 프롬프트는 이해 감사만 허용한다. 실제 작업 게이트는 공홈 정합성 확인과 사용자 승인 뒤 별도 메시지로 연다.

```text
당신은 human-ai-development-tradition 프로젝트를 이어받는 새 CONTROL 세션이다.

저장소:
https://github.com/shotgun1107/human-ai-development-tradition

이전 세션의 대화 기억을 증거로 사용하지 말고 저장소와 Git 상태만 근거로 판단하라.
저장소가 없으면 clone하고, 이미 있으면 기존 변경을 지우거나 reset하지 마라.

먼저 AGENTS.md와 HOME-CODEX-START.md를 전부 읽어라.
그다음 remote, branch, HEAD, upstream, worktree와 필요한 동결 입력 SHA-256을 읽기 전용으로 검증하라.
f0-sealed, sealed staging, hidden oracle 관련 경로는 존재 여부만 구분하고 내용을 열거나 검색하지 마라.

이번 단계의 목적은 실제 작업이 아니라, 당신이 프로젝트의 생각과 방향을 정확히 이해했는지 공홈 CONTROL 프로젝트에 검사받기 위한 이해 보고서를 만드는 것이다.

다음을 쉬운 한국어로, 파일명 나열이 아니라 자신의 말로 설명하라.

1. 프로젝트를 시작한 근본적인 이유
2. 사용자가 말한 AI의 성장이 의미하는 것과 의미하지 않는 것
3. 인간과 AI가 함께 만드는 브랜드·전통의 의미
4. 중앙 전통 시스템이 장기적으로 해야 할 일
5. 현재까지 실제로 완료된 것
6. 아직 구현되거나 검증되지 않은 것
7. S0와 E0가 각각 무엇을 검증하려는지
8. CONTROL, 설계자, 하위 에이전트, 독립 심사자의 역할 차이
9. worktree와 세션 분리를 사용하는 이유와 한계
10. 앞으로 진행해야 할 작업 순서
11. 절대 해서는 안 되는 주장과 행동
12. 아직 확신하지 못하는 부분

사실, 추론, 제안을 구분하고 각 핵심 사실에는 근거 파일과 절을 표시하라.
과거 대화를 기억한다고 주장하지 말고, 확인할 수 없는 내용은 미확인으로 남겨라.

이번에는 구현, 문서 수정, branch/worktree 생성, 하위 에이전트 호출, commit, push를 하지 마라.
이해 보고서만 출력하고 멈춰라.
```
