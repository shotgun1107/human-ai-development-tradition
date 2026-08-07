# E0 운영 비용·게이트 계획 v0.2

- 상태: `수정 제안 — 새 독립 심사 필요, 설계 전용`
- 제안 라벨: `E0`는 공식 단계로 동결되지 않았다.
- 현재 허용: v0.2 설계의 read-only 심사와 CONTROL 통합 적합성 검토만
- 현재 금지: 자료·oracle·prompt·schema·code 작성, 모델 호출, 채점, 통계·simulation 실행, 가격 조회, 구현, 실행, 효과·안전·경제성 주장, downstream gate 개방
- 비용 원칙: 현재 가격이나 노동 단가를 추정하지 않는다. authoring 전에 실제 담당자·보상·시간과 모든 AI 지원 호출의 최악 상한을 숫자로 승인한다.

## 1. 사실, 추론, 제안

### 1.1 확인된 사실

1. E0의 실제 인력, 보상, 시간, 모델, 가격, 호출 수, 표본 수와 운영 결과는 정해지지 않았다.
2. v0.1은 역할별 사람시간 범주를 열거했지만 최소 독립 staffing, 보상·가용시간, absence stop과 모든 authoring/review AI 호출을 완전히 고정하지 않았다.
3. CONTROL이 제공한 독립 심사는 이를 major feasibility 결함으로 판정했다.

### 1.2 추론

1. confirmatory independence를 지키면 E0는 한 사람 운영 시험이 아니다.
2. 독립 인력을 구할 수 없다는 사실은 역할 겸임을 조용히 늘릴 이유가 아니라 `DEFER/STOP` 근거다.
3. executor 호출만 세면 AI-assisted authoring, 감사, redaction, 판정, 분석과 review 비용을 숨기게 된다.
4. 사람의 무급 도움, subscription 안의 호출과 대기시간도 0 비용으로 사라지지 않는다.

### 1.3 제안

- Stage마다 최소 distinct people과 금지 겸임을 고정한다.
- 각 사람의 보상 방식, rate, 최소·최대 능동시간, 달력 가용성과 replacement를 authoring 전에 승인한다.
- 모델을 사용한 모든 지원 활동을 호출·token·tool·현금 장부에 포함한다.
- 필수 역할의 부재·conflict·상한 미승인은 자료 작성 또는 다음 block release를 즉시 막는다.

## 2. 단계별 질문과 기본 조건

| Stage | 조건 | 목적 | 효과 주장 |
|---|---|---|---|
| 0 | 설계 v0.2 read-only review | B-01·M-01~M-07의 설계 폐쇄 확인 | 없음 |
| 1 | 의존성·staffing·budget | 단일 표현 참조와 실행 전 상한 | 없음 |
| 2 | 별도 승인 authoring | 미래 합성 package의 역할별 작성 | 없음 |
| 3 | preflight·calibration | hash, leakage, B quality, 판정·redaction 가능성 | 없음 |
| 4 | A/D pilot | 총패키지 방향·위해·비용 선별 | pilot-only |
| 5 | A/B/D confirmatory | 관련 내용의 제한 효과 | 모든 공동 기준 통과 시에만 제한 주장 |
| 6 | optional C/D | 정제의 추가 가치 | 별도 진단 주장만 |
| 7 | 선택 확장 | 새 모델·과제군·전달 방식 | 각각 새 사전등록과 승인 |

C 또는 네 조건 동시 실행은 기본 경로가 아니다. Stage 5 통과 전 Stage 6·7을 열지 않으며, pilot을 confirmatory로 승격하지 않는다.

## 3. 최소 독립 staffing

### 3.1 공통 원칙

- `distinct person`은 서로 다른 자연인을 뜻한다. 다른 계정, agent, session 또는 worktree는 사람 독립성을 만들지 않는다.
- 동일 공급자·모델의 여러 agent도 독립 human reviewer를 대신하지 않는다.
- 아래 금지 겸임은 staffing 상한을 맞추기 위해 면제할 수 없다.
- 한 사람이 맡을 수 있는 역할은 표에 명시된 결합만 허용한다. 추가 결합은 새 독립 review와 새 예산 승인을 요구한다.

### 3.2 A/D pilot 최소선: 13 distinct people

| 사람 | 역할 | 허용 결합과 경계 |
|---:|---|---|
| 1 | CONTROL + protocol owner + 결과 잠금 뒤 analyst | 자료·출력 작성과 판정 금지 |
| 2 | tradition curator | task/oracle/B/output 접근 금지 |
| 3 | task/oracle author·외부 oracle custodian | D/output 접근 금지 |
| 4 | leakage/B-quality reviewer 1 | authoring·execution·판정·analysis 금지 |
| 5 | leakage/B-quality reviewer 2 | 4번과 독립; 같은 금지 |
| 6 | packager + scheduler + run operator | oracle·score·효과 mapping 접근 금지 |
| 7 | redaction officer | oracle·mapping·score 접근 금지 |
| 8 | redaction QC | 7번과 독립; adjudicator 겸임 금지 |
| 9 | safety monitor | locked critical의 최소 mapping 외 접근 금지 |
| 10 | adjudicator 1 | condition package·mapping 접근 금지 |
| 11 | adjudicator 2 | 10번과 독립; 같은 금지 |
| 12 | blind disagreement resolver | mapping·다른 score 사전 접근 금지 |
| 13 | independent read-only reviewer | authoring·gate 승인·실행·판정 금지 |

pilot에는 B를 실행하지 않지만 4·5번은 near-copy와 전이 경계를 독립 감사한다. B-quality 검토는 Stage 5에서만 활성화한다.

### 3.3 A/B/D confirmatory 최소선: 14 distinct people

pilot 최소선에 다음 한 사람을 추가한다.

| 사람 | 역할 | 경계 |
|---:|---|---|
| 14 | matched-control B author | task/oracle/output 접근 금지; curator와 별도 |

4·5번 reviewer는 B/D의 실질 품질 동등성과 B 무관성을 각각 독립 승인할 수 있다. 이미 source·task·oracle 의미를 감사했으므로 executor, redactor, adjudicator, resolver 또는 analyst가 될 수 없다.

C가 추가되어도 기본 인원은 줄지 않는다. C curator가 별도로 필요하다고 pre-result conflict audit이 판정하면 그 사람과 비용을 추가한다. 다른 모델 또는 새 task family 반복은 새 가용성 확인을 요구한다.

### 3.4 인력 부족 판정

다음 중 하나면 해당 Stage는 열리지 않는다.

- 최소 distinct people 미달
- 한 사람의 금지 입력 노출 또는 이해충돌
- safety monitor, redaction QC, 두 adjudicator, resolver 중 하나가 미지정
- oracle custodian의 저장소 밖 통제 환경 미확정
- independent reviewer가 authoring이나 실행을 겸함

인력 부족 상태에서 `pilot`, `confirmatory`, `independent`, `condition-blind`라는 라벨을 유지하지 않는다.

## 4. 보상·시간·가용성 동결

### 4.1 authoring 전 필수 기록

각 사람에 대해 다음 값을 숫자와 명시 문구로 기록하고 사용자가 승인한다.

- 역할, 실제 담당자, conflict declaration과 금지 입력 확인
- 보상 형태: hourly, fixed 또는 명시적 volunteer
- rate, 통화, 세금·수수료 포함 여부와 최대 지급액
- 예상 최소·최대 능동시간과 대기시간
- calibration, authoring, audit, execution block, adjudication, dispute, analysis별 시간 상한
- 참여 가능한 달력 구간, 응답 기한과 최대 block turnaround
- 중도 이탈 시 사전 적격 replacement 또는 `no replacement`
- AI 보조 허용 여부, 허용 모델·정보와 human verification 시간

volunteer도 rate를 0으로 숨기지 않는다. 현금 지급이 0이면 `unpaid`, 동의 범위, 능동시간과 기회비용을 별도로 기록한다. 사용자의 own time도 같은 방식으로 기록한다.

### 4.2 시간 장부

```text
H_total_active = H_protocol + H_source + H_tradition + H_B
               + H_task_oracle + H_leakage_quality + H_packaging
               + H_run_ops + H_redaction + H_safety
               + H_adjudication + H_resolution + H_analysis + H_review

H_total_wait = 같은 역할들의 대기시간 합
```

각 항목은 계획 최소·계획 최대·실제를 구분한다. AI가 초안을 만들고 사람이 검증한 시간은 AI 호출 장부와 사람 능동시간 양쪽에 들어간다. calendar 상한은 능동시간과 별도로 둔다.

### 4.3 absence stop

- 필수 담당자가 예정 block 전에 가용성을 재확인하지 않으면 block을 release하지 않는다.
- adjudicator 한 명, resolver, redaction officer/QC 또는 safety monitor가 없으면 실행을 시작하거나 계속하지 않는다.
- 실행 중 결원이 생기면 scheduler는 새 호출을 멈추고 미완료 block을 닫는다.
- replacement는 이전 역할의 금지 정보를 보지 않았고 같은 conflict·보상·시간 승인을 새로 통과해야 한다.
- critical unblinding 뒤 safety monitor를 교체하지 않는다. 불가피하면 실행을 종료한다.
- replacement 때문에 자료·판정 가능성·시간 block이 바뀌면 기존 결과에 이어 붙이지 않고 새 protocol 판본 여부를 CONTROL이 심사한다.
- 역할별 최대 시간 또는 응답 기한을 넘겼다고 다른 역할이 대신 보거나 condition-aware operator가 판정하지 않는다.

## 5. 모든 AI 지원 호출 장부

### 5.1 포함 범위

시험과 관련해 외부 모델 또는 model-backed tool을 부른 모든 행위를 센다.

- protocol·authoring·revision 지원
- source/tradition/B/task/oracle 작업 지원
- leakage·quality review 지원
- package·redaction·QC 지원
- transport·calibration·executor·retry
- AI judge 또는 disagreement 보조
- 통계·보고·독립 review 지원
- orchestration, retrieval, embedding, search 또는 tool 안의 model call

interactive subscription, cached call, bundled credit, 실패 호출과 사람이 버린 출력도 호출 수와 token·시간에서 제외하지 않는다. 현금 증분이 0이면 `cash_increment = 0`으로 기록하되 실제 사용량과 subscription 배분 가정을 남긴다.

### 5.2 수량식

```text
Q_executor = N_instances × K_conditions × R_sessions

Q_total_max = Q_protocol_support
            + Q_authoring_support
            + Q_audit_quality_support
            + Q_packaging_redaction_support
            + Q_calibration
            + Q_executor
            + Q_retry_max
            + Q_adjudication_support
            + Q_analysis_review_support
            + Q_model_backed_tools
```

각 범주는 기본 0이 아니다. 사용하지 않기로 명시하고 0으로 동결하거나, 최대 호출 수를 정한다. prompt를 여러 과제로 묶어 fresh-session 원칙을 우회하지 않는다.

각 호출은 역할, 목적, 공급자, 모델 ID·판본, service tier, input/cached/output/tool usage, 시작·종료, retry 사유, 현금 단가 근거와 condition 노출 범위를 기록한다. 이 기록 형식의 구현은 미래 gate 사항이며 현재 schema를 만들지 않는다.

### 5.3 token과 현금

호출별 최악 예산은 공통 wrapper, task, condition context, tool context와 output ceiling을 구분한다. B와 D는 허용오차 안에서 context 자원을 맞춘다.

실행 시점에만 공식 공급자 정보로 다음을 채운다.

- 입력·cached input·출력·tool·storage의 단가
- model, tier, 확인일, 통화, 세금과 환율 가정
- subscription·credit의 배분 규칙
- 사람별 보상 최대액과 기타 고정비

```text
C_cash_max = C_all_AI_calls_max
           + C_human_compensation_max
           + C_tools_storage_max
           + C_other_approved_max
```

평균 출력이 아니라 최대 출력, 모든 허용 retry, model-backed tool 상한과 dispute adjudication 최악값을 사용한다. 현재 문서는 가격을 조회하거나 금액을 제안하지 않는다.

## 6. stop-before-authoring 계산 순서

1. A/D pilot인지 A/B/D confirmatory인지 질문과 조건 수를 고정한다.
2. measurement plan의 `Δ`, harm·blinding margin, cluster-aware power와 최소 independent family 수를 고정한다.
3. 실제 13명 또는 14명 이상을 역할에 배정하고 conflict를 확인한다.
4. 사람별 compensation, 능동·대기·calendar 상한과 absence plan을 숫자로 받는다.
5. 모든 AI 지원 범주의 `Q_max`, token, tool과 retry 상한을 계산한다.
6. 실제 모델·tier와 공식 가격을 확인한다.
7. 최악 현금, 사람시간, calendar, 호출, token을 계산한다.
8. 사용자가 `B_cash`, `B_active_time`, `B_wait_time`, `B_calendar`, `B_calls`, `B_token`을 명시 승인한다.
9. 계산서·담당자·가격 근거·가정의 version과 hash를 고정한다.
10. 그 뒤에만 별도 `MATERIAL AUTHORING OPEN` gate를 요청할 수 있다.

다음 중 하나면 authoring 0건을 유지한다.

- cluster-aware power의 family 수가 어느 상한과도 양립하지 않음
- 필수 distinct people, compensation 또는 availability가 없음
- 모든 AI support call 범주가 계산에 포함되지 않음
- 단일 인증 `selected_representation_ref`가 없음
- B, 위해 family, fresh session, redaction·blinding 또는 safety monitor를 제거해야만 예산이 맞음
- 가격·모델 판본을 실행 시점에 확인할 수 없음

비용 축소 순서는 선택적 C 제거, 선택적 AI judge 제거, 비필수 AI 지원 제거, 결과와 무관한 반복 재검토, 질문 범위 축소다. B, independent family 수, 위해 guardrail, role isolation 또는 fresh session을 지워 confirmatory 비용을 맞추지 않는다.

## 7. Stage와 gate

### Gate V2-G0 — `E0 EFFECT TEST DESIGN V0.2 REVIEW`

필요:

- v0.2 Markdown과 sidecar의 hash 일치
- v0.1 보존 확인
- 새 독립 hostile read-only verdict
- B-01·M-01~M-07 각각의 `PASS/FAIL/UNCLEAR`

열 수 있는 것: CONTROL 통합 적합성 검토만. 이 문서 작성으로 G0가 통과된 것은 아니다.

### Gate V2-G1 — `E0 SINGLE REPRESENTATION INTERFACE READY`

필요:

- 정확히 하나의 versioned·hashed·승인된 `selected_representation_ref`
- fallback이면 먼저 같은 참조 지위를 획득했다는 독립 기록
- visibility, citation, resource, limitations 참조
- 참조 변경 시 전면 re-authoring 규칙 승인

실패 시: authoring 금지. `단순 fallback` 문구로 우회할 수 없다.

### Gate V2-G2 — `E0 STAFFING AND CEILING APPROVED`

필요:

- Stage에 필요한 13명 또는 14명 이상과 conflict audit
- 사람별 compensation·시간·availability·absence plan
- cluster-aware N과 모든 AI 지원 호출을 포함한 최악 장부
- 모델·공식 가격·현금·시간·calendar·call·token 상한의 사용자 승인

실패 시: 자료 작성 0건 유지.

### Gate V2-G3 — `E0 MATERIAL AUTHORING OPEN`

필요:

- 사용자가 현재 thread에서 이 정확한 gate를 명시 개방
- V2-G0~G2 통과
- 역할별 입력 allowlist, 출력 소유권과 repo 밖 oracle 경계

이 gate는 미래 합성 authoring만 열며 code·모델 실행·채점을 열지 않는다.

### Gate V2-G4 — `E0 PREFLIGHT AND CALIBRATION OPEN`

필요:

- 모든 자료와 참조 hash
- 두 독립 leakage audit과 B-quality/relevance 승인
- redaction·condition-guess 계획과 판정 가능성 계획
- safety block·limited unblinding 계획
- 최악 비용 재계산

이 gate도 effectiveness 실행을 열지 않는다.

### Gate V2-G5 — `E0 A-D PILOT EXECUTION OPEN`

필요:

- A/D pilot 사전등록과 독립 review
- pilot 전용 13명 availability 재확인
- 모델·가격·자원 상한 재확인
- condition-blind adjudication, redaction/QC, safety monitor 준비

통과 결과: A/B/D 비용 산정 검토 여부뿐.

### Gate V2-G6 — `E0 A-B-D CONFIRMATORY EXECUTION OPEN`

필요:

- pilot advance; effect pass가 아님
- B의 이중 quality·relevance 승인
- 14명 이상 staffing과 absence plan
- family-cluster power, `Δ`, harm·blinding margins, Bonferroni rule 동결
- 새 worst-case 예산과 사용자 승인
- 결과를 보지 않은 independent review

### Gate V2-G7 — `E0 OPTIONAL C OR TRANSFER OPEN`

C/D, 네 조건 동시 실행, 다른 모델, retrieval 비교와 새 task-family 모집단은 각각 별도 질문·power·staffing·budget·사전등록을 요구한다. 앞 단계의 결과를 자동 재사용하지 않는다.

## 8. block release와 safety 비용

- 실행은 사전 크기의 block으로 계획하고 각 block 사이에 redaction, blind critical clearance와 staffing availability 시간을 배정한다.
- critical 후보가 나오면 새 호출을 즉시 멈추므로 남은 호출은 `unused`, 이미 발생한 호출·사람시간은 실제 비용으로 기록한다.
- safety monitor의 최소 unblinding, blind resolver와 독립 adverse review의 최악 시간을 예산에 넣는다.
- confirmed critical은 condition과 무관하게 전체 stop이다. D label은 귀속 기록에만 사용한다.
- 중단 뒤 favorable condition이나 family만 실행하지 않는다.

## 9. rollback

| 신호 | 즉시 조치 | 롤백 |
|---|---|---|
| 입력·참조 hash 불일치 | 의존 작업 중단 | V2-G0/G1 |
| 표현 참조 공백·복수·fallback 우회 | authoring 금지 | 단일 artifact의 새 독립 승인 |
| staffing·보상·availability 미달 | block 금지 | V2-G2 |
| 미장부 AI call 또는 비용 상한 초과 | 새 호출 중단 | ceiling 재승인; 결과와 결합 금지 |
| near-copy 또는 B 품질 실패 | family/package 격리 | 결과 전 새 authoring 판본 |
| raw cue·redaction 비대칭·blinding breach | confirmatory pass 금지 | 새 redaction/자료 판본과 review |
| adjudication 모호성 | 실행 금지 또는 block 무효 | oracle·판정 규칙 새 판본 |
| model drift·shared state | block 중단 | 동일 환경 새 block |
| confirmed critical | 전체 실행 중단 | package 격리와 adverse review |
| power와 상한 불일치 | confirmatory 금지 | scope 축소 새 설계 또는 defer |

오염·중단·invalid 결과를 깨끗한 표본과 이어 붙이지 않는다. 결과를 본 뒤 threshold, family, N, retry, condition, redaction 또는 staffing 규칙을 유리하게 바꾸면 새 탐색 판본일 뿐 confirmatory 연속성이 없다.

## 10. 현재 status와 unresolved feasibility

이 계획은 다음을 보여주지 않았다.

- 13명/14명 staffing을 실제로 구할 수 있음
- compensation·calendar·비용이 사용자 상한 안임
- family-cluster power가 경제적으로 가능함
- redaction 뒤 blinding guardrail을 통과할 수 있음
- B quality와 무관성을 동시에 만족할 수 있음

이 항목들은 숨은 약속이 아니라 미래 stop 조건이다. v0.2 설계 심사를 통과하더라도 실제 값이 채워질 때까지 authoring, 구현, 실행과 효과·경제성 주장은 닫혀 있다.
