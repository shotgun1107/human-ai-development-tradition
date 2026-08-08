# E0 전통 효과시험 설계 v0.2

- 상태: `수정 제안 — 새 독립 심사 필요, 설계 전용`
- 제안 라벨: `E0`는 아직 동결된 공식 단계가 아니다.
- 기준선: `central-system-v2.1-s0-preparation`
- 범위: 효과시험의 인과 구조와 정보 경계만 제안한다.
- 현재 금지: 합성 원천·전통·대조·과제·정답·숨은 oracle·prompt·schema·코드 작성, 모델 호출, 채점, 실행, 효과 판정, 다음 gate 개방

## 1. 판본의 성격

### 1.1 확인된 사실

1. 저장소는 S0 준비 단계이며 S0, E0, 중앙 시스템, Project Brain 통합, 운영 안전성, 경제성, 실제 프로젝트 가치와 모델 간 전승은 구현되거나 검증되지 않았다.
2. E0 v0.1은 설계 제안이었고, CONTROL이 제공한 독립 심사는 `REVISE-AND-REVIEW`였다.
3. 그 심사는 우회 가능한 표현 fallback 한 건을 blocking으로, 효과 임계값·clustering·전이 경계·B 품질·위해 unblinding·판정 blind·인력과 비용을 major로 판정했다.
4. v0.1 파일은 보존되며 이 문서는 그 결과나 승인 상태를 바꾸지 않는다.

### 1.2 이 판본이 채택한 추론

1. A/D는 가장 싼 총패키지 신호를 볼 수 있지만 내용 특이적 효과를 확인할 수 없다.
2. 내용 특이적 확인은 독립적으로 품질이 승인된 B를 포함한 A/B/D가 필요하다.
3. C는 정제의 추가 가치가 현재 의사결정일 때만 필요한 별도 진단이다.
4. 과제 인스턴스는 task family 안에 묶이므로 confirmatory 추론과 power는 family clustering을 직접 반영해야 한다.
5. 사람이 조건을 추측할 수 있는 raw output은 조건명만 숨긴 판정과 같지 않다.
6. 엄격한 역할 격리와 이중 판정은 한 사람 운영 목표와 양립하지 않는다. 인력이 없으면 주장을 낮추는 것이 아니라 시험을 열지 않아야 한다.

### 1.3 제안

이 판본은 다음의 순서를 제안한다.

1. v0.2 패키지의 새 독립 read-only 심사
2. 단 하나의 인증된 `selected_representation_ref`와 나머지 의존성 승인
3. 인력·보상·시간·모든 AI 지원 호출을 포함한 stop-before-authoring 상한 승인
4. 별도 명시 gate가 있을 때만 미래 자료 작성
5. A/D pilot 뒤에만 A/B/D 확인시험 비용 재검토
6. C 또는 네 조건 동시 실행은 별도 진단 가치가 사전 승인된 경우에만 검토

## 2. 좁은 인과 질문과 조건 지위

### 2.1 질문

> 같은 동결 모델·판본, 공통 지시, 과제, 도구, 시간창과 출력 자원에서, 별도의 합성 경험에서 정제되고 인증된 외부 전통을 받은 fresh session은 전통을 받지 않은 session과 품질이 독립 승인된 무관 대조를 받은 session보다, 표면과 일부 결정 관계가 달라진 자족적 과제에서 수용 가능한 판단을 더 자주 내리며 위해 도전 과제에서 더 나빠지지 않는가?

초기 시험은 모델 가중치 변화가 아니라 외부 문서 전달의 조건 내 효과만 묻는다.

### 2.2 조건

| ID | 조건 | 지위 | 허용되는 질문 |
|---|---|---|---|
| A | 전통 없음 | pilot과 확인시험 필수 | D 패키지 총효과의 무전통 기준 |
| B | 품질·권위·구체성·일반 지침이 독립 승인된 무관 대조 | 내용 확인시험 필수 | 관련 내용이 형식·token·일반 조언보다 나은가 |
| C | 같은 합성 원천의 원본 기록 | 선택 진단 | 정제가 원본 접근보다 추가 가치가 있는가 |
| D | 인증된 표현 계약의 정제 전통 | 시험 개입 | 제한된 외부 전통 전달 효과 |

고정 해석은 다음과 같다.

- A/D는 **pilot-only**다. 실행 가능성, 방향성, 위해와 비용만 선별한다.
- B는 관련 내용의 효과를 확인하려면 **필수**다. B가 미결정이면 확인시험을 열지 않는다.
- C는 **optional diagnostic**이다. A/B/D 통과를 보상하거나 대체하지 않는다.
- 네 조건 동시 실행은 기본값이 아니다. 세 인과 질문을 같은 시간 block에서 답해야 할 사전 의사결정 가치와 충분한 family 수·예산이 모두 있을 때만 별도 승인한다.

### 2.3 단위

- 개입 단위는 `한 과제 인스턴스 × 한 조건 × 한 fresh session`이다.
- confirmatory 기본은 과제–조건당 1회이며, 한 session에는 한 과제와 한 조건만 둔다.
- 과제 인스턴스는 사전 동결된 task family에 중첩된다.
- confirmatory 1차 추정의 독립 단위는 task family다. family 안 인스턴스와 그 짝은 독립 N으로 부풀리지 않는다.
- 반복이 별도 승인되면 반복은 session 수준에서 과제–조건 안에 중첩하며, 사전 family 집계 규칙 없이는 표본을 늘리지 않는다.

## 3. 단일 인증 표현 참조 계약

### 3.1 우회 금지 규칙

자료 작성 전에 해당 protocol 판본에는 **정확히 하나의 활성 `selected_representation_ref`**만 존재해야 한다. 그 참조는 다음 의미를 모두 인증한 하나의 versioned artifact를 가리켜야 한다.

- 고유 판본 식별자와 소유자
- 참조 대상의 SHA-256
- 승인 근거와 승인 시각
- 적용 범위와 알려진 한계
- B/C/D와 A의 공통 wrapper에 적용할 표현 규칙
- 대체·철회 관계

S0가 선택한 후보와 CONTROL이 승인한 단순 공개 fallback은 이 규칙에서 동등하다. fallback은 예외 경로가 아니다. 먼저 독립 검토를 거친 versioned·hashed artifact가 되고, protocol의 **유일한** `selected_representation_ref`로 인증된 뒤에만 authoring 의존성을 만족한다.

다음은 모두 stop이다.

- `selected_representation_ref`가 비어 있음
- 둘 이상의 후보 또는 `후보 또는 fallback` 표현이 남아 있음
- inline 설명이나 사람 재량으로 참조를 대신함
- 참조 hash·판본·known limitations 중 하나가 없음 또는 불일치
- B만 다른 표현 계약을 사용함

참조 변경은 사소한 수정이 아니다. 기존에 작성된 조건 자료·과제·누출 감사의 효력을 끝내고 새 protocol 판본, 새 hash, 새 pre-result 감사를 요구한다. 기존 결과를 본 뒤 표현 참조를 바꿔 같은 시험을 계속할 수 없다.

### 3.2 나머지 연결점

아래 참조도 자료 작성 전에 versioned·hashed 상태로 단일화한다.

| 연결점 | 역할 |
|---|---|
| `runner_visibility_contract_ref` | 각 역할과 조건이 볼 수 있는 정보 경계 |
| `evidence_citation_contract_ref` | 근거·상태 표시의 공통 의미 |
| `resource_envelope_ref` | 모델, 생성 설정, 도구, 시간, 출력, retry 상한 |
| `known_limitations` | S0 또는 fallback이 입증하지 못한 범위 |

이 연결은 표현을 고정할 뿐 전통의 유효성이나 특정 표현의 우월성을 E0에 전달하지 않는다.

## 4. 전이와 near-copy의 재현 가능한 경계

### 4.1 작성 순서

1. 결과를 결정하는 추상 관계와 적용·비적용 경계를 나타내는 latent-pattern 계약을 D·후속 과제 작성 전에 동결한다.
2. tradition curator는 승인된 별도 합성 원천과 latent-pattern 계약만 본다. 후속 과제와 oracle은 보지 않는다.
3. task/oracle author는 latent-pattern 계약과 독립 합성 세계 규칙만 본다. 최종 D, B와 조건 출력은 보지 않는다.
4. 두 authoring 선이 각자 판본과 hash를 닫은 뒤에만 전용 auditor 환경에서 교차 검토한다.
5. 교차 검토 뒤에는 문구 수정으로 살리지 않는다. 실패 family는 폐기하고 결과를 보지 않은 새 authoring 판본으로 교체한다.

### 4.2 사전 동결할 판정 규칙

미래 authoring에는 아래 고정 binary 규칙을 그대로 적용한다. 고유 전문용어의 불가피한 공유는 authoring 전에 공개 allowlist로만 제외하며, 결과를 본 뒤 allowlist를 늘리지 않는다. 정규화는 Unicode normalization, 대소문자·공백·문장부호 통일과 단순 명명 placeholder 치환까지만 허용한다. token 판정은 `resource_envelope_ref`에 동결된 tokenizer 한 개만 사용한다.

**자동 실패:**

- 정규화 뒤 결정에 쓰이는 고유 이름·식별자·수치 tuple·선택지 순서가 하나라도 재사용됨
- allowlist 밖의 연속 8개 content token이 source와 task의 결정 관련 부분에 공통으로 나타남
- 이름 치환과 표면 재배열만으로 원천의 결론·필수 근거·예외·행동을 후속 답으로 복원할 수 있음
- 원천의 결정적 근거 집합, 우선순위, 예외 trigger와 요구 행동이 모두 일대일 대응함
- 후속 과제 작성 뒤 D가 바뀌거나, D 작성 뒤 후속 oracle이 D에 맞춰 바뀜
- 현재 과제 자체의 정보만으로 허용 답 범위를 결정할 수 없음

**전이로 허용하기 위한 공동 요구:**

- 공유하는 것은 동결 latent pattern뿐이고 구체 서술과 답 표지는 공유하지 않음
- 행위 맥락, 산출물 종류, 증거 형태, 제약 배치, 예외 메커니즘, 올바른 행동 형태의 6축 중 적어도 4축이 다름
- 후속 과제에는 원천에 없던 결정적 관계가 적어도 2개 있고, 원천의 현저한 관계 중 후속 답에 직접 재사용할 수 없는 것이 적어도 1개 있음
- A도 현재 과제만으로 풀 수 있고, D는 독점 해결 사실을 공급하지 않음

### 4.3 감사자와 oracle 접근

두 명의 독립 pre-result leakage auditor가 각각 판정한다. 둘은 author, executor, redactor, adjudicator, analyst가 될 수 없고 실행 출력·조건 결과를 보지 않는다.

- surface/provenance audit은 source, D, B, 후속 과제와 판본 계보를 보되 hidden oracle은 보지 않는다.
- structural audit은 저장소와 executor session 밖의 통제 환경에서 source, D, 후속 과제와 필요한 oracle 의미를 read-only로 본다. oracle을 복사·요약·반출하지 않는다.

두 감사 모두 모든 요구를 `PASS`해야 family가 살아남는다. 한 명의 `FAIL`, `UNCLEAR`, 누락 또는 두 판정의 불일치는 자동 family reject다. CONTROL에는 family ID, 입력 hash, 판정과 시각만 전달하며 oracle 내용은 전달하지 않는다. 사후 analyst나 adjudicator가 auditor 재량을 대신하지 않는다.

## 5. B의 실질적 품질과 독립 승인

### 5.1 B가 맞춰야 하는 것

B는 무의미한 filler나 약한 일반론이 아니다. D와 같은 `selected_representation_ref` 아래에서 다음 고정 parity rule을 만족하는, 내부적으로 유용하지만 시험 latent pattern에는 무관한 별도 합성 문서다.

- 문서 수와 최상위 구획 수는 같고, 전체 context token 차이는 D의 5% 이내
- active/superseded/withdrawn 상태 항목 수, 출처가 있는 주장 수와 citation 수는 각각 D 대비 ±1 이내
- `selected_representation_ref`가 정한 D의 각 authority/evidence tier에는 같은 tier의 B claim이 하나씩 대응하고 unmatched claim은 없음; 참조가 tier 의미를 정하지 않으면 B authoring stop
- 각 actionable rule의 modal strength, 적용 조건 수, 금지 조건 수, 요구 검증 수는 대응 rule과 각각 ±1 이내
- 반례, limitation과 version-replacement 관계의 수는 각각 D 대비 ±1 이내
- 문장 완성도, 내부 일관성, 실제로 따를 수 있는 정도
- 확인·보류·근거 확인 같은 general guidance의 의미 목록은 양쪽에 동일

D에만 유리한 보편 지침이 있으면 그 지침을 공통 wrapper로 이동하거나 B에 의미상 동등하게 둔다. B가 더 그럴듯하게 보이지만 실제로 빈 문서인 경우는 실패다.

### 5.2 이중 pre-result 승인

두 명의 독립 B-quality reviewer가 B와 D를 조건명이 아닌 무작위 X/Y로 보고, 결과·실행 순서·condition mapping 없이 각각 평가한다. 이 역할은 4.3의 auditor가 맡을 수 있지만 authoring, execution, redaction, adjudication, analysis 역할과는 겸임하지 않는다.

각 reviewer는 위 parity rule을 항목별 binary로 판정하고, 별도로 각 문서가 스스로 제시한 합성 맥락에서 내부 일관되고 실행 가능한지를 `PASS/FAIL/UNCLEAR`로 판정한다. 두 사람이 모든 항목에 `PASS`를 내야 한다. reviewer가 topic 단어를 제거한 X/Y 사본에서 어느 쪽이 D인지 맞히고 그 근거가 authority·specificity·완성도 차이라면 condition cue 실패다. `FAIL`, `UNCLEAR`, reviewer disagreement 또는 condition cue는 B package 전체 실패다.

별도의 relevance 판정에서 두 reviewer는 B가 모든 시험 latent pattern과 무관하고 D만 예정된 관계를 포함함을 확인한다. 이때 필요한 task 의미는 볼 수 있지만 결과와 출력은 보지 않는다. 품질 동등성과 무관성 중 하나라도 실패하면 확인시험을 열지 않는다.

## 6. 위해 감시와 제한적 unblinding

### 6.1 역할 분리

primary adjudicator는 끝까지 condition-blind다. `D-attributable` 여부를 primary adjudicator가 판정하지 않는다. 별도의 safety monitor 한 명만 잠긴 critical 후보에 한정해 condition mapping을 열 수 있다. safety monitor는 author, scheduler, executor, redactor, adjudicator, analyst가 될 수 없으며 효과 결과를 받지 않는다.

### 6.2 block 처리

- 실행은 사전 고정된 작은 block으로만 release한다.
- 다음 block은 이전 block의 transport 확인과 condition-blind critical clearance가 끝나기 전에는 release하지 않는다.
- adjudicator가 익명 출력에서 critical 후보를 표시하면 scheduler는 모든 새 호출을 즉시 보류한다.
- 두 명의 blind adjudicator 또는 사전 지정된 blind resolver가 critical 여부와 근거를 잠근다.
- 그 뒤 safety monitor는 해당 출력 ID 하나의 condition label만 1회 공개한다. 다른 점수·출력·미실행 배정은 열지 않는다.
- 확인된 critical은 condition과 무관하게 남은 실행 전체를 중단한다. label은 D-attributable 분류와 격리 범위 기록에만 사용하며 실행 지속을 유리하게 선택하는 데 쓰지 않는다.
- D로 확인되면 D package를 격리하고 해당 판본은 재사용하지 않는다. 다른 조건이어도 실행은 재개하지 않고 원인과 측정 적합성을 독립 심사한다.

모든 unblinding은 접근자, 시각, 출력 ID, 이유, 열린 필드와 후속 조치를 기록한다. candidate가 critical이 아니면 mapping을 열지 않는다. 이미 열린 block의 결과를 성공 분석에 부분 편입하거나 favorable family만 계속 실행하지 않는다.

## 7. raw output redaction과 blinding 확인

### 7.1 판정용 사본

raw output은 조건·실행 시스템과 분리된 보관 경계에 두고 adjudicator에게 직접 주지 않는다. 독립 redaction officer가 결과를 보지 않는 사전 정책으로 판정용 사본을 만든다.

다음 표면 cue는 의미를 바꾸지 않는 범위에서 제거·정규화한다.

- 조건명, 패키지명, 전통/대조 문서 제목과 고유 ID
- wrapper를 그대로 반복한 문구, condition slot 표지, 실행 순서와 timestamp
- 모델·tool metadata, 파일 경로, formatting fingerprint
- D/B 문서를 길게 그대로 인용한 부분의 출처 표지

핵심 결정, 근거, 확인·보류, 오류 또는 과잉 적용을 숨기는 내용 삭제는 금지한다. redaction officer는 oracle과 condition mapping을 보지 않는다. 두 번째 독립 QC가 redaction 정책 준수와 의미 보존만 확인한다.

### 7.2 condition-guess와 실패 폐쇄

adjudicator는 각 출력의 primary 판정과 근거를 먼저 잠근 뒤, 자신이 생각하는 condition과 확신 범주를 별도 기록한다. condition mapping은 모든 점수·guess가 잠긴 뒤 analyst에게 전달한다.

분석 계획은 조건 수에 따른 chance 기준, blinding 허용오차, confidence interval과 breach 규칙을 authoring 전에 고정한다. 다음 중 하나면 confirmatory pass를 낼 수 없다.

- 명시적 cue가 redaction 뒤 남음
- condition-guess가 사전 breach 기준을 넘음
- redaction이 조건별로 비대칭이거나 핵심 의미를 바꿈
- guess 또는 redaction QC가 누락됨

이 경우 결과는 `adjudication-blinding-threat / inconclusive`로 닫고, 효과가 커 보여도 pass로 보상하지 않는다. 객관적으로 기계 판정 가능한 사전 항목은 별도 민감도 결과로 보고할 수 있지만 사람 판정 실패를 대신하지 않는다.

## 8. fresh session, 모델과 자원 통제

- 각 과제–조건은 대화 이력·다른 조건·oracle·원천 기록이 없는 fresh executor session이다.
- fixture/tradition/task author, auditor, redactor, adjudicator session을 executor로 fork하거나 재사용하지 않는다.
- 같은 session 안 A→D 같은 crossover를 금지한다.
- 캐시, agent memory, retrieval state와 local files는 조건별로 격리하며 worktree를 비밀 경계라고 부르지 않는다.
- 공급자, 정확한 모델 ID와 노출 snapshot, 생성 설정, service tier, region, system/developer/task wrapper hash, 도구·network·file visibility, 시간·출력·retry 상한을 한 block에서 고정한다.
- drift, 비대칭 retry, resource 차이 또는 shared-state 오염이 있으면 block 전체를 무효로 하고 이어 붙이지 않는다.
- retry는 출력 내용과 무관한 사전 정의 transport failure에만 대칭 적용한다.

## 9. 역할 경계 요약

| 역할 | 허용되는 최대 정보 | 필수 금지 |
|---|---|---|
| CONTROL/protocol owner | 설계, hash, 승인, 잠긴 결과 | 자료·출력 작성, 사후 threshold 변경 |
| tradition curator | 합성 source, latent pattern, 표현 참조 | task/oracle/output |
| task/oracle author | latent pattern, 독립 세계 규칙, 외부 통제 oracle | 최종 D/B/output |
| B author | 표현 통계와 무관 합성 source | task/oracle/output |
| leakage/B reviewers 2명 | 4·5절의 pre-result 입력 | author/executor/adjudicator/analyst 겸임 |
| scheduler/run operator | 통과 package, 배정, resource envelope | oracle·판정·효과 결과 |
| executor | 한 조건의 한 과제와 허용 문서 | 다른 조건/source/oracle/output |
| redaction officer와 QC | raw output, 동결 redaction 정책 | mapping·oracle·score |
| adjudicator 2명과 blind resolver | redacted output, task, oracle 규칙 | mapping·D/B 원문·다른 score |
| safety monitor | 잠긴 critical ID의 최소 mapping | 일반 효과 결과·authoring·판정 |
| analyst | 모든 score/guess가 잠긴 뒤 mapping과 비용 장부 | 사후 exclusion·threshold 변경 |
| independent reviewer | 동결 공개 설계 packet | 자료/oracle/output 생성·gate 개방 |

정확한 최소 인원, 겸임 가능 범위와 absence stop은 비용·gate 계획이 정한다. role allowlist는 최대 입력이며 실제 필요한 최소만 제공한다.

## 10. 기계적 정합성과 효과의 분리

다음은 분석 자격일 뿐 성능이 아니다.

- 모든 입력·참조·실행 package의 hash 일치
- 유일한 `selected_representation_ref`
- authoring 순서, 전이/B 감사, role exposure 준수
- fresh session과 resource 대칭성
- redaction, score lock, condition-guess, limited unblinding 기록
- 계획된 모든 호출·실패·retry·무효·비용 기록

한 항목이라도 실패하면 관련 block은 confirmatory 분석 자격이 없다. 기계적 성공을 수용 가능 판단률에 더하지 않는다.

## 11. 주장 사다리

| 단계 | 최대 허용 주장 |
|---|---|
| v0.2 독립 심사 통과 | CONTROL이 설계 의존성과 비용을 검토할 수 있음 |
| 기계적 preflight | 비교를 계획대로 실행할 준비가 됨 |
| A/D pilot advance | 총패키지 신호를 A/B/D로 확인할 검토 가치가 있음 |
| A/B/D confirmatory pass | 시험한 모델·task-family 모집단·전달 방식·자원에서 관련 정제 전통 내용의 smallest-worthwhile effect를 지지하는 제한된 근거 |
| optional C/D pass | 같은 합성 source·자원에서 정제가 원본 접근보다 나았다는 제한된 근거 |
| 여러 모델의 독립 반복 | 시험한 각 모델 내부에서 제한 효과가 재현됨 |

어떤 단계도 S0 통과, 표현 후보의 일반 우월성, 중앙 시스템·Project Brain, 실제 고객·운영 프로젝트, 운영 안전성, 경제성, 파인튜닝, 장기 지속성 또는 model-to-model transfer를 입증하지 않는다.

## 12. 현재 닫힌 사항

다음은 새 독립 심사와 별도 gate 없이는 채우거나 수행하지 않는다.

- 실제 `selected_representation_ref`와 연결 artifact
- 모델·가격·인력·보상·시간·표본 수
- 합성 source, D/B/C, 과제, oracle, prompt, schema, code
- authoring, transport, executor 호출, adjudication, 분석

따라서 v0.2의 현재 지위는 **v0.1의 blocking/major 지적을 설계 수준에서 닫으려는 새 제안**이며, E0를 실행하거나 검증했다는 뜻이 아니다.
