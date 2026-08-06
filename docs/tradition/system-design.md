# 개인 AI 개발 전통 시스템 설계

## 1. 목적, 원칙, 경계

목적은 과거를 많이 저장하는 것이 아니라 다음 프로젝트에서 더 좋은 결정을 내리고 그 효과를 검증하는 것이다. 시스템의 품질은 문서 수가 아니라 다음 세 능력으로 판단한다.

1. 필요한 시점에 관련 경험과 현재 효력 있는 규칙을 찾을 수 있는가?
2. 그 규칙이 어떤 증거·맥락·사람 승인에서 왔는지 추적할 수 있는가?
3. 적용 뒤 실제로 품질이 좋아졌는지, 부작용은 없었는지 판단하고 되돌릴 수 있는가?

설계 원칙:

- 원본 우선: 해석보다 사건·실험·결정의 원자료를 먼저 보존한다.
- 사실/추론/제안 분리: 세 종류를 같은 문장이나 필드에 섞지 않는다.
- 관찰≠교훈: 조치와 효과 검증 전까지 후보 상태다.
- 좁은 범위 우선: 불확실할수록 프로젝트·작업 유형·도구 버전 범위를 좁힌다.
- 반례 우선 탐색: 승격 심사 전에 지지 증거보다 반례와 실패한 적용을 먼저 찾는다.
- 실행 가능성: 교리는 적어도 하나의 체크리스트·시험·프롬프트·템플릿 또는 명시적 “행동 없음” 결정으로 연결한다.
- 가역성: 모든 효력 있는 규칙은 판본과 롤백·폐기 경로를 가진다.
- 사람 통제: AI는 증거의 의미와 교리 효력을 확정하지 않는다.
- 최소 수집: 비밀·개인정보·불필요한 대화 전문을 전통 저장소에 넣지 않는다.

범위 밖:

- 실행 원장과 모델 대화 전체의 장기 보관
- 인사 평가, 비난, 법적 책임 판단
- 모델 가중치 업데이트 또는 자동 파인튜닝
- 무승인 자동 프롬프트·코드 변경
- 기존 incident 하네스나 B1 구현의 재설계

## 2. 계층과 책임

```text
L0 원자료          incident JSON, 실험 결과, commit, benchmark, 결정 로그
L1 경험 레코드     성공·실패·결정·실험·근접실패를 공통 형식으로 색인
L2 교훈 후보       증거를 종합한 조건부 주장, 반례와 불확실성 포함
L3 교리            승인된 프로젝트 교리 또는 개인 범용 교리
L4 실행 산출물     체크리스트·프롬프트·테스트·템플릿·정책
L5 적용·평가       어느 판본을 어디에 적용했고 무엇이 변했는지
L6 월간 리뷰       승인·기각·수정·강등·폐기 결정과 다음 실험
```

L0는 각 원천의 기존 형식을 유지한다. 전통 시스템은 원문을 복제하기보다 안정적인 상대 경로, ID, commit 또는 hash를 가리킨다. 원본이 민감하거나 저장소 밖이면 비식별 요약과 접근 제한 포인터만 둔다.

## 3. 기존 자산 평가

### 3.1 재사용할 것

원천 오케스트레이터의 `tools/implementation-log/`와 당시 확인한 초기 개발 incident에서 재사용할 개념:

- 고유 ID와 엄격한 상태
- JSON 원본과 결정적 사람용 렌더링 분리
- 알 수 없는 필드 거부
- 증상, 재현, 증거 종류, 근본 원인, 대안, 해결, 회귀시험, 검증, 남은 위험 분리
- 해결 상태의 필수 증거 게이트
- 안전한 저장소 상대 경로 검사
- 대표적 token 패턴 탐지
- 관련 commit과 출처 참조

`codex-revision-log.md`에서 재사용할 개념:

- 확인한 범위와 확인하지 못한 범위의 명시
- 작업 전후 hash·줄 수·판본 같은 무결성 단서
- 변경 범위와 보호 문서의 분리
- 시간순 의사결정과 검증의 서술

### 3.2 부족한 것

incident 하네스는 다음을 표현하지 못한다.

- 성공, 의도적 실험, 결정, 근접 실패, 반복 패턴, 반례
- 여러 사건을 종합한 하나의 교훈과 하나의 사건에서 나온 여러 후보
- 증거의 독립성·직접성·전이성·신선도
- 교훈의 적용 조건, 금지 조건, 예상 메커니즘
- 프로젝트 교리와 개인 범용 교리의 수명주기
- 상충 교리, 대체 판본, 폐기 이유
- 교리에서 파생된 산출물과 실제 적용 결과
- 월간 승인, 다음 재검토일, 검증 실패

revision log는 풍부하지만 장문 append-only 문서이므로 다음이 어렵다.

- 최신 효력 판본의 기계적 검색
- 중복·반례·반복 패턴 집계
- 교훈별 증거 그래프와 적용 효과 추적
- 기각·폐기된 지식이 현재 프롬프트에 섞이지 않게 하는 상태 필터

따라서 기존 두 자산을 수정해 만능 스키마로 만들지 않고, 새 계층이 ID와 경로로 참조한다.

## 4. 핵심 객체 모델

이 절의 YAML은 구현 스키마가 아니라 최소 논리 데이터 계약이다. 초기에는 Markdown front matter 또는 수작업 표로 충분하며, 실제 구현 전 별도 검증이 필요하다.

### 4.1 Experience

```yaml
schema_version: 1
id: EXP-20260805-001
kind: incident | success | experiment | decision | near-miss | observation
project: local-agent-orchestrator
stage: b1
occurred_at: 2026-08-05T00:00:00+09:00
summary: "동결 manifest의 placeholder를 사전 감사에서 발견했다"
expected: "fixture 출처가 실제 commit과 tree로 고정됨"
observed: "commit 필드가 placeholder였음"
outcome: corrected-before-comparison
context:
  task_type: benchmark-preflight
  tool_versions: []
  constraints: []
claims:
  facts: []
  interpretations: []
  proposals: []
source_refs:
  - type: incident
    ref: docs/operations/implementation-incidents/entries/DEV-20260805-001.json
    integrity: commit-or-sha256
verification:
  method: reproducible-test
  result: supported
sensitivity: public | internal | restricted
redaction_status: reviewed
```

규칙:

- `facts`는 출처가 직접 보이는 주장만 쓴다.
- `interpretations`는 원인·메커니즘·일반화이며 작성자와 확신도를 표시한다.
- `proposals`는 미래 행동으로 효력이 없다.
- 성공은 “성공했다”만 적지 않고 예상, 관측 결과, 검증 방법, 우연·외부 요인을 적는다.
- 결정은 채택 대안뿐 아니라 고려 대안과 당시 제약을 ADR처럼 보존한다.

### 4.2 Lesson Candidate

```yaml
schema_version: 1
id: LES-202608-001
status: proposed | under-review | experiment-required | rejected
claim: "비교 입력은 출처 commit뿐 아니라 대상 subtree hash로 고정한다"
scope:
  level: project
  projects: [local-agent-orchestrator]
  task_types: [benchmark]
  applies_when: []
  does_not_apply_when: []
mechanism: "commit 하나만으로는 fixture 내용 경계를 명시하지 못한다"
supporting_evidence: [EXP-20260805-001]
counterevidence: []
alternatives: []
evidence_grade: E2
uncertainties: []
proposed_artifacts: []
proposed_test: "새 fixture에서 placeholder와 tree drift를 자동 탐지"
owner: human
review_due: 2026-09-05
```

교훈 후보는 관찰의 요약이 아니라 **조건부로 반증 가능한 주장**이어야 한다. “문서를 잘 쓴다”는 후보가 아니고, “동결 benchmark는 실행 전 manifest commit과 subtree hash 일치를 자동 검사하면 입력 drift 발견률이 높아진다”처럼 적용·측정 가능한 형태여야 한다.

### 4.3 Doctrine

```yaml
schema_version: 1
id: DOC-PROJ-001
version: 1.0.0
status: trial | active | constrained | deprecated | retired
scope_level: project | personal-general
normative_rule: "benchmark 비교 전 입력 commit과 fixture tree를 검사한다"
rationale: "비교 가능성을 실행 전에 fail-closed로 확보한다"
evidence_refs: [LES-202608-001]
counterevidence_refs: []
applicability: []
exceptions: []
confidence: moderate
effective_from: 2026-09-01
review_due: 2026-12-01
supersedes: null
superseded_by: null
approved_by: human
approval_record: REV-202608-001
```

교리의 의미:

- `trial`: 다음 적용에서 측정해야 하는 가설적 규칙
- `active`: 승인된 기본값
- `constrained`: 일부 맥락에서만 유지되도록 범위 축소
- `deprecated`: 신규 적용은 중단하되 기존 참조의 이행 기간
- `retired`: 효력 없음; 역사·반례 검색에만 사용

### 4.4 Artifact

```yaml
id: ART-CHK-001
kind: checklist | prompt | test | template | policy
version: 1.1.0
derived_from:
  doctrine_id: DOC-PROJ-001
  doctrine_version: 1.0.0
status: draft | active | deprecated | retired
target_stage: benchmark-preflight
content_ref: path-or-anchor
validation_refs: []
```

산출물은 교리와 별도 판본을 가진다. 표현 개선은 artifact patch일 수 있지만 규범 의미가 바뀌면 doctrine 판본도 바꾼다.

### 4.5 Application과 Evaluation

```yaml
application:
  id: APP-202609-001
  project: local-agent-orchestrator
  doctrine: DOC-PROJ-001@1.0.0
  artifacts: [ART-CHK-001@1.1.0]
  decision: applied | waived | not-applicable
  waiver_reason: null
  baseline_ref: null
  started_at: timestamp

evaluation:
  id: EVAL-202609-001
  application_id: APP-202609-001
  hypothesis: "사전 검사로 비교 실행 전 입력 drift를 탐지한다"
  primary_metrics: []
  guardrail_metrics: []
  result: supports | mixed | contradicts | inconclusive
  confounders: []
  evidence_refs: []
  reviewed_by: human
```

`waived`도 중요한 데이터다. 적용률이 낮은 이유가 잊음, 검색 실패, 과도한 비용, 잘못된 범위인지 구분한다.

### 4.6 Monthly Review

```yaml
id: REV-202609-001
period: 2026-08
inputs_snapshot: commit-or-hash
included_ids: []
excluded_ids: []
decisions:
  - target: LES-202608-001
    action: approve-trial | activate | revise | reject | defer | deprecate | retire
    reason: "..."
approver: human
approved_at: timestamp
ai_assistance:
  model: recorded-if-used
  prompt_version: recorded-if-used
  outputs_are_advisory: true
open_actions: []
```

## 5. 증거 모델

### 5.1 증거 유형

- `D` 직접 관찰: 원장, diff, 로그, 결과 파일처럼 실제 사건을 보여준다.
- `R` 재현 시험: 동일 조건에서 반복 가능하다.
- `C` 비교·대조: baseline, 비교군, 전후 또는 A/B가 있다.
- `X` 독립 반복: 다른 프로젝트·작업·도구 버전에서 같은 방향이다.
- `S` 소스 검사: API·코드·공식 문서와 대조했다.
- `E` 전문가/독립 심사: 이해관계가 다른 사람이 검토했다.
- `I` 추론: 직접 검증 전의 인과 설명 또는 일반화다.
- `A` 일화·회상: 보조 신호일 뿐 단독 승격 근거가 아니다.

유형은 우열의 단순 순서가 아니다. API 사실에는 `S`가 강하고, 효과 주장에는 `C`·`X`가 더 중요하다.

### 5.2 종합 등급

| 등급 | 의미 | 허용 상태 |
|---|---|---|
| E0 | 출처 없는 주장, AI 생성 추정, 회상만 존재 | 수집함 또는 기각 |
| E1 | 출처 있는 단일 관찰·결정·성공 | lesson candidate |
| E2 | 재현 또는 두 개 이상 상호보완 증거, 반례 검색 수행 | project doctrine `trial` |
| E3 | 프로젝트 내 반복 적용과 사전 지표로 효과 확인 | project doctrine `active` |
| E4 | 독립 프로젝트/상이한 조건에서 반복, 전이 한계 명시 | personal-general doctrine `trial` 또는 `active` |

등급 상승 조건:

- 증거가 같은 원자료를 재서술한 것인지 확인해 가짜 독립성을 제거한다.
- 결과뿐 아니라 시행 충실도와 버전을 확인한다.
- 반례·실패한 적용·관측되지 않은 부작용을 기록한다.
- 오래된 도구/API 의존 증거는 신선도를 낮춘다.
- 등급은 AI가 제안할 수 있지만 사람이 승인한다.

## 6. 전체 수명주기

### 6.1 사실·사건 → 검증된 경험

수집 trigger:

- 예상과 실제의 중요한 차이
- 반복 가능한 실패 또는 근접 실패
- 비용·시간·품질이 비정상적으로 좋았던 성공
- 되돌리기 어렵거나 장기 영향을 가진 결정
- 가설과 사전 지표가 있는 실험
- 기존 교리와 모순된 결과

게이트:

1. 원본 포인터와 시간·프로젝트·도구 버전을 기록한다.
2. 비밀·개인정보를 제거하거나 제한 포인터로 바꾼다.
3. 사실·추론·제안을 분리한다.
4. 재현 가능하면 시험하고, 불가능하면 독립 자료로 삼각검증한다.
5. 검증 한계를 적는다.

### 6.2 검증된 경험 → 교훈 후보

AI가 할 수 있는 일:

- 유사 경험 군집화
- 기존 교리·후보·반례 검색
- 조건부 claim 초안
- 누락 필드와 출처 없는 주장 표시

사람이 해야 하는 일:

- 군집이 같은 현상을 다루는지 판단
- 인과와 상관을 구분
- 적용·금지 조건 확정
- 증거 등급과 다음 실험 승인

후보는 다음 질문에 답하지 못하면 보류한다.

- 무엇을 해야 하거나 피해야 하는가?
- 어떤 조건에서인가?
- 왜 효과가 있을 것으로 보는가?
- 어떤 결과가 이 주장을 반박하는가?
- 다음 적용에서 무엇을 측정할 것인가?

### 6.3 월간 회고 → 교리

월간 회고는 후보를 무더기로 승인하는 회의가 아니다. 신규 `active` 교리는 월 1~3개로 제한하는 것을 초기 운영 가설로 둔다. 나머지는 실험·보류·기각한다.

- 프로젝트 교리 `trial`: E2 이상, 구체적 시험, 소유자, 재검토일
- 프로젝트 교리 `active`: E3 이상, 적어도 한 번의 의도적 적용 효과
- 범용 교리 `trial`: E4 또는 명시적으로 다른 두 맥락의 반복과 전이 가설
- 범용 교리 `active`: 두 맥락 이상에서 유용성, 치명 반례 없음, 실행 산출물과 guardrail 존재

### 6.4 교리 → 실행 산출물

규범 문장을 기억에만 의존하지 않는다.

| 교리 성격 | 우선 산출물 |
|---|---|
| 매번 확인할 안전 경계 | 짧은 체크리스트 + 자동 검사 |
| 모델 행동·출력 형식 | versioned prompt + golden test |
| 회귀 가능 결함 | 결정적 테스트 |
| 반복 작업 시작점 | 템플릿 |
| 예외·승인 조건 | 정책 + waiver 기록 |

가능하면 가장 검증 가능한 표현을 우선한다. 테스트로 강제할 수 있는 규칙을 장문 프롬프트에만 넣지 않는다.

### 6.5 다음 프로젝트 적용 → 효과 측정

프로젝트 시작 시 다음 순서로 적용한다.

1. 프로젝트 특성표를 작성한다: 작업 유형, 실패 비용, 모델·도구 버전, 데이터 민감도, 평가 방식.
2. `active` 범용 교리 중 조건이 맞는 것만 검색한다.
3. 프로젝트 교리를 추가하고 충돌을 표시한다.
4. 적용·면제·비적용 결정을 판본과 함께 기록한다.
5. 결과를 보기 전에 주요 지표와 guardrail을 고정한다.
6. 결과 뒤 교리 적용의 효과와 혼란변수를 평가한다.

### 6.6 수정·강등·폐기

- `revise`: 의미는 유지되지만 설명·산출물·조건이 개선됨
- `constrain`: 반례 때문에 적용 범위를 좁힘
- `demote`: 범용에서 프로젝트로, 또는 active에서 trial로 강등
- `deprecate`: 신규 사용을 중지하고 대체 판본으로 이행
- `retire`: 효과 없음, 해로움, 중복, 기술 소멸로 효력 제거
- `reject`: 후보가 증거 부족·비반증 가능·중복으로 교리가 되지 못함

폐기 문서는 삭제하지 않는다. 효력 검색에서 제외하고 이유, 마지막 유효 판본, 대체 규칙, 관련 반례를 남긴다.

## 7. 범용 전통과 프로젝트 전통

### 7.1 기본 우선순위

충돌하지 않을 때 두 계층을 합친다. 충돌할 때는 다음 순서로 결정한다.

1. 법·보안·사용자 명시 요구와 더 강한 안전 제약
2. 현재 프로젝트의 검증된 프로젝트 교리
3. 개인 범용 교리
4. trial 후보와 과거 사례

프로젝트 교리가 범용 교리를 재정의할 때는 자동 override가 아니라 `exception`과 이유를 기록한다. 범용 교리가 더 일반적이라는 이유만으로 로컬 근거를 이기지 않는다.

### 7.2 승격 규칙

프로젝트 → 범용 승격에 모두 필요:

- 동일 해결의 이름만 같은 것이 아니라 메커니즘이 같은가?
- 서로 독립적인 두 프로젝트 또는 의도적으로 다른 두 조건의 증거가 있는가?
- 도구·모델·저장소 특수성을 제거해도 규칙이 의미가 있는가?
- 반례 검색과 실패한 적용 검토를 했는가?
- 범용화로 생기는 추가 비용과 오적용 위험을 측정했는가?
- 최소 하나의 재사용 산출물과 적용 guardrail이 있는가?
- 사람이 범용 범위와 재검토일을 승인했는가?

### 7.3 강등·폐기 규칙

- 새 반례가 범용 claim을 깨지만 특정 맥락에서는 유효하면 프로젝트 교리로 강등한다.
- 핵심 API·모델·도구 버전이 바뀌면 자동으로 `review-required`; 재검증 전에는 `constrained`로 본다.
- 두 번 연속 효과가 없거나 guardrail 악화가 반복되면 active를 trial로 강등한다.
- 심각한 부작용, 비밀 노출, 안전 경계 위반은 즉시 deprecated/retired 후보로 올리고 적용을 중단한다.
- 3회 재검토에서 사용되지 않고 미래 적용 조건도 없으면 중복·비용을 검토해 폐기한다.

## 8. 모순 처리

모순은 덮어쓸 오류가 아니라 학습의 주요 입력이다.

1. 문장 충돌인지 조건 충돌인지 분해한다.
2. 각 주장에 프로젝트, 작업 유형, 버전, 데이터, 위험 수준을 붙인다.
3. 결과 지표와 검증 강도를 비교한다.
4. 같은 조건의 진짜 모순이면 둘 다 `contested`로 두고 새 판정을 유예한다.
5. 판별 실험을 설계하고 어느 결과가 어느 주장을 지지하는지 사전에 적는다.
6. 해소 뒤 승자만 남기지 않고 패배한 주장을 반례·폐기 기록으로 연결한다.

금지 사항:

- 증거 수를 단순 투표처럼 세기
- 최신 기록이라는 이유로 자동 우선
- AI confidence를 증거 강도로 사용
- 결과를 본 뒤 적용 조건을 바꿔 항상 맞는 교리 만들기

## 9. 버전 관리와 변경 의미

교리 판본은 의미 기반으로 관리한다.

- major: 규범 방향, 기본 행동, 안전 경계가 바뀜
- minor: 적용 조건·예외·새 산출물이 추가되나 기존 의미와 호환
- patch: 오탈자·링크·설명 명료화, 규범 의미 불변

각 승인 판본은 Git commit 또는 content hash, 승인 기록, 효력일, 재검토일을 가진다. 과거 application은 항상 당시 정확한 판본을 가리킨다. `latest`만 저장하지 않는다.

## 10. 사람 승인 게이트와 역할

한 사람 시스템에서도 역할을 시간적으로 분리한다.

| 역할 | 책임 | AI 대체 가능 여부 |
|---|---|---|
| 기록자 | 원자료 링크, 사실·추론 분리, redaction | 초안만 가능 |
| 분석자 | 군집, 원인 가설, 반례·대안 탐색 | 보조 가능 |
| 승인자 | 효력·증거 등급·범위·폐기 결정 | 불가 |
| 적용자 | 프로젝트에서 적용·면제 기록 | 보조 가능 |
| 평가자 | 사전 지표 대조, 혼란변수·부작용 검토 | 초안만 가능 |

같은 사람이 모두 맡더라도 한 세션에서 사건 직후 바로 승인하지 않는다. 최소 cooling-off 기간 또는 월간 회고를 둔다. 고위험 규칙은 독립 reviewer가 없으면 범용 active로 승격하지 않고 trial로 유지한다.

필수 사람 승인:

- E2 이상 등급 부여
- doctrine 생성·활성화·범위 확대
- 비밀·개인정보가 포함될 가능성이 있는 자료의 저장·공유
- 자동 적용 산출물 활성화
- 상충 교리 판정
- 강등·폐기와 대체 판본 확정

## 11. 개인정보·비밀정보 처리

### 11.1 수집 전 최소화

- 원문 대화·환경 전체를 복사하지 않는다.
- 필요한 기술 사실만 추출하고 계정, 사용자명, 로컬 절대경로, 조직·고객명, 이메일, token, prompt의 민감 데이터는 제거한다.
- 비밀 원본은 기존 보안 저장소에 두고 전통에는 접근 제한 포인터와 비식별 요약만 둔다.

### 11.2 자동 검사와 사람 검사

기존 하네스의 API·GitHub token regex는 재사용할 출발점이지만 충분하지 않다. 추가 후보:

- 이메일·전화·IP·개인명·조직명·고객 ID
- `.env`, 인증 파일, 쿠키, bearer header, signed URL
- 로컬 홈 경로와 저장소 밖 절대경로
- prompt에 포함된 영업비밀·라이선스 제한 원문

자동 탐지는 false negative를 전제로 한다. `redaction_status: reviewed`는 사람 검토 전 설정하지 않는다. redaction 전 원문을 외부 모델에 보내지 않는다.

### 11.3 보존과 삭제

- 제한 자료는 최소 보존 기간과 재검토일을 둔다.
- 삭제 요청·비밀 회수 시 파생 요약·embedding·cache·backup까지 영향 범위를 기록한다.
- 공개 가능한 전통과 제한 evidence vault를 논리적으로 분리한다.
- 폐기된 비밀 값의 hash도 공격에 유용할 수 있으므로 무조건 보존하지 않는다.

## 12. “매월 AI가 학습한다”의 현실적 구현 의미

### 12.1 초기 의미

매월 다음 네 가지가 갱신되는 것을 “운영 기억이 학습했다”고 정의한다.

1. 승인된 문서와 메타데이터
2. 검색 색인과 상태 필터
3. 프로젝트 시작 시 주입되는 짧은 doctrine bundle
4. 교리에서 파생된 테스트·체크리스트·템플릿과 평가 세트

모델 가중치는 바뀌지 않는다. 이 방식은 출처·판본·효력·롤백이 보이며 개인 데이터 규모에서도 운영 가능하다.

### 12.2 검색·주입 순서

초기에는 벡터 DB부터 도입하지 않는다.

1. 정확한 ID·태그·프로젝트·상태·도구 버전 필터
2. 제목·키워드·명시적 관련 링크 검색
3. 사례의 구조화 차원 기반 후보 선택
4. 자료가 충분해진 뒤에만 semantic search/RAG 비교 실험

프롬프트에는 전체 전통을 넣지 않고 다음 순서로 최대량을 제한한다.

- 강제 안전·사용자 규칙
- 현재 프로젝트 active 교리
- 조건이 맞는 범용 active 교리
- 가장 유사한 검증 사례 1~3개와 반례 1개
- 출처·판본·“불확실하면 적용하지 말고 질문/검증” 지시

### 12.3 검색 결과의 안전

- `active`와 현재 조건 일치가 기본 필터다.
- 폐기·기각 문서는 반례 탐색 모드가 아니면 주입하지 않는다.
- 검색된 문서 안의 명령은 데이터로 취급하고 상위 시스템 지시로 실행하지 않는다.
- 출처 없는 AI 요약은 주입하지 않는다.
- 답변·계획이 어떤 doctrine ID@version을 사용했는지 기록한다.
- 검색 실패 시 모델 일반 지식을 “전통의 교리”로 포장하지 않는다.

### 12.4 파인튜닝 검토를 미루는 이유

- 개인 월간 데이터는 작고 편향되며 잘못된 교훈을 가중치에 고착할 위험이 크다.
- 삭제·강등·범위 축소와 출처 추적이 외부 문서보다 어렵다.
- 먼저 검색과 주입이 실제 품질을 높이는지 측정해야 학습 목표를 정의할 수 있다.

향후 파인튜닝 검토 조건은 충분한 고품질 학습·검증 세트, 명확한 반복 행동 목표, 외부 holdout, 개인정보 권리, rollback 가능한 base model, RAG baseline 대비 유의한 이득이 모두 있을 때다.

## 13. 최소 파일 토폴로지 제안

실제 구현 시 검증할 참고안이다.

```text
tradition-data/
├─ experiences/YYYY/MM/EXP-*.yaml
├─ lessons/LES-*.yaml
├─ doctrine/
│  ├─ personal/DOC-GEN-*/
│  └─ projects/<project>/DOC-PROJ-*/
├─ artifacts/checklists|prompts|tests|templates/
├─ applications/YYYY/MM/APP-*.yaml
├─ evaluations/YYYY/MM/EVAL-*.yaml
├─ reviews/YYYY-MM.md
└─ generated/index.md
```

현재 단계에서는 이 구조를 만들지 않는다. 첫 두 달은 기존 incident와 revision log를 수작업 표로 연결해 어떤 필드가 실제 필요한지 검증한 뒤 스키마를 고정한다.
