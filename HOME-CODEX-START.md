# 집 Codex 시작점

- 문서 상태: `CONTROL 인수인계 v0.1`
- 기준 시각: `2026-08-07` (KST)
- 저장소: `https://github.com/shotgun1107/human-ai-development-tradition`
- 활성 기준선: `central-system-v2.1-s0-preparation`
- 용도: 새 PC·새 Codex 세션이 대화 기억 없이 저장소 증거만으로 작업을 재개하기 위한 시작점

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
| 인수인계 작성 직전 `main` 및 `origin/main` | `6de2c6d9434ca2ff07f0c048a01b5f10bcae3b92` |
| E0 설계 브랜치 | `codex/e0-effect-test-design` |
| E0 설계 HEAD 및 원격 HEAD | `84014378b48466c185e13cadd6b9a07549ffbaee` |
| E0와 `main`의 공통 기준점 | `6de2c6d9434ca2ff07f0c048a01b5f10bcae3b92` |
| S0 v0.5 브랜치 | 작성 시점에는 로컬·원격에 없음 |

이 문서를 포함한 최종 커밋은 위 `main` 값보다 뒤에 생긴다. 새 세션은 이 표를 현재 HEAD로 오해하지 말고 `git fetch` 후 실제 원격 상태를 다시 확인한다.

작성 PC의 `main` 작업 트리에는 `f0-sealed` 관련 미추적 경로가 있었다. 이번 문서 작업은 그 경로를 열거나 수정하거나 커밋하지 않았다. 미추적 봉인 경로는 Git으로 전달되지 않으며, 집 PC에서 보이지 않는 것이 정상이다. 어디에서든 보이면 공개 입력으로 취급하지 않는다.

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

## 4. 집 PC에서 처음 할 검증

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

## 5. 다음 두 작업과 분리 원칙

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
집 Codex CONTROL: Git·해시·게이트 검증
  ├─ S0 전용 worktree/session: v0.5 설계 후보 작성
  │    └─ fresh 독립 심사
  └─ E0 fresh 심사 session: v0.1 설계 읽기 전용 심사
             ↓
        CONTROL 통합 판단
             ↓
  통과한 설계에 대해서만 다음 자료 작성 또는 구현 게이트 검토
```

S0와 E0는 설계 단계에서는 병렬로 진행할 수 있다. 그러나 E0 자료 작성·구현·실행은 S0가 유효한 표현 후보와 연결 계약을 만들기 전까지 열지 않는다.

## 7. 세션이 처음 보고해야 할 것

새 집 Codex CONTROL 세션은 첫 답변에서 다음만 보고하고 멈춘다.

- 실제 저장소 경로와 원격 URL
- 현재 branch·HEAD·upstream 관계
- `main`과 E0 원격 브랜치 확인값
- 작업 트리 변경과 봉인·비공개 후보의 존재 여부를 내용 열람 없이 구분한 결과
- 동결 입력 hash 검사 결과
- S0 v0.5와 E0 심사 중 지금 열린 정확한 게이트
- 허용 작업, 금지 작업, 다음 한 단계

확인되지 않은 과거 대화, 공홈 프로젝트 기억 또는 모델의 추측으로 누락된 Git 증거를 채우지 않는다.
