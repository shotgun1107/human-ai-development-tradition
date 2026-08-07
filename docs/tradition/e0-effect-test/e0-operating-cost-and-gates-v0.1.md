# E0 운영 비용·게이트 계획 v0.1

- 상태: `제안 — 독립 심사 전`
- 제안 라벨: `E0`는 공식 단계로 동결되지 않았다.
- 현재 허용: 설계·읽기 전용 심사·CONTROL 통합 검토 준비
- 현재 금지: 합성 원천·전통·대조·과제·oracle 작성, 구현, 모델 실행, 채점, 효과 주장
- 비용 원칙: 현재 API 가격을 만들어내지 않는다. 사용할 모델과 현재 공식 가격을 확인한 뒤, 자료 작성 전에 최악 비용과 사람시간을 사용자가 승인한다.

## 1. 운영 목표

가장 작은 유효 질문을 먼저 싸게 반증하고, 통과하지 못한 질문에 조건·표본·자동화를 더하지 않는다. 단계마다 다음을 분리한다.

1. **기계적 가능성:** 해시·가시성·배정·수집·판정이 계획대로 작동하는가
2. **파일럿 방향성:** D 패키지 총효과가 확인시험 비용을 정당화할 신호를 보이는가
3. **확인 인과:** 관련 내용이 무전통 및 길이·형식 일치 무관 대조보다 나은가
4. **선택 진단:** 정제가 같은 원본 기록 접근보다 추가 가치가 있는가
5. **확장:** 다른 모델·검색 방식·과제군에서도 독립 재현되는가

각 단계는 다음 단계를 자동 승인하지 않는다. 비용이 상한을 넘거나 위해·누출·측정 결함이 나타나면 앞 단계로 롤백하거나 중단한다.

## 2. 단계별 최소 계획

### Stage 0 — 설계와 독립 심사

현재 단계다.

- 모델 호출: 0
- 자료·oracle·코드: 0
- 허용 작업: 이 패키지의 적대적 읽기 전용 심사, 수정 제안, 해시 고정, CONTROL 통합 검토
- 산출 판단: 설계가 다음 의존성 검토로 갈 수 있는지뿐

이 단계의 통과는 E0 효과, S0, 구현 가능성 또는 실행 승인이 아니다.

### Stage 1 — 의존성과 stop-before-authoring 승인

아래가 모두 채워질 때만 연다.

- 유효한 `selected_representation_ref` 또는 CONTROL이 승인한 단순 공개 대체 기준선
- runner visibility, evidence citation, resource envelope, known limitations 연결
- 역할 담당과 정보 격리 계획
- 파일럿 질문, 층, 오류 정의, advance 규칙 동결
- 최대 사람시간·호출·token·현금 상한의 사용자 승인
- 실제 사용할 모델·판본과 그 시점의 공식 가격 확인

모델 호출과 자료 작성은 아직 0일 수 있다. 비용 계산 결과가 상한을 넘으면 여기서 멈춘다.

### Stage 2 — 미래 자료 작성과 기계적 preflight

이 단계는 현재 닫혀 있으며 별도 명시적 gate가 필요하다. 승인이 나더라도 원천 경험, D, A wrapper, 과제·oracle, 누출 감사 자료를 역할별로 작성하고 각각 해시 고정한다. 구현이나 실행은 별도 승인이다.

Preflight는 다음만 확인한다.

- 파일·참조·해시·판본 일치
- 조건 가시성과 길이 통계
- near-copy·답 누출 없음
- task/oracle 판정 가능성
- 무작위 순서와 익명화 계획
- 정확한 최악 호출·token·사람시간·현금 재계산

Preflight 통과는 효과가 아니다. 자료 작성 뒤 비용이 새 상한을 넘으면 실행하지 않는다.

### Stage 3 — 저비용 A/D 파일럿

측정 계획의 제안값은 다음과 같다.

- 짝지은 과제 인스턴스 `N_pilot = 8`
- 조건 `K = 2` (`A 전통 없음`, `D 정제된 전통`)
- 과제–조건당 독립 반복 `R = 1`
- executor 호출 `8 × 2 × 1 = 16`
- 세션 `16`: 호출마다 대화 이력이 없는 별도 세션
- 관련 전이와 위해 도전 층을 같은 수로 포함
- 최소 두 개의 잠재 결정 패턴 가족
- primary 판정은 사람 oracle 기반; AI judge는 기본값 0회

파일럿은 effect pass를 만들지 않는다. 기계적 유효성, D-attributable critical, 방향성, token·지연·사람 수정·현금을 확인하고 A/B/D 확인시험의 비용 산정 여부만 판정한다.

### Stage 4 — A/B/D 확인시험

파일럿 advance와 새 비용 승인이 모두 있어야 연다.

- 조건 `K = 3`
- 과제 수 `N_confirm`은 사전 최소 가치 효과·허용 위해·power 규칙으로 계산
- 반복 `R_confirm`은 모델 변동성 근거와 예산으로 사전 고정
- executor 호출은 `N_confirm × 3 × R_confirm`
- 각 과제는 모든 조건에 배정하되 매번 새 세션
- 조건 순서를 가족 안에서 균형 무작위화
- 두 사람의 blind adjudication을 기본으로 함

`N_confirm`, `R_confirm`, 비용 상한이 고정되지 않으면 자료를 추가 작성하지 않는다. 표본 수를 맞추기 위해 위해 도전 층이나 B를 제거하면 내용 효과 확인시험이 아니므로 stage를 열지 않는다.

### Stage 5 — 선택적 C 원본 기록 진단

다음 의사결정이 남을 때만 연다.

> 정제에 드는 사람시간과 유지비가 같은 과거 합성 원본을 직접 제공하는 것보다 가치가 있는가?

기존 A/B/D 실행에 C를 사후로 덧붙이면 시간·모델 drift가 생길 수 있다. C를 추가하기로 했다면 같은 동결 모델·시간 block에서 모든 필요한 비교를 다시 균형화하거나, C/D를 별도 진단 시험으로 명시한다. C는 첫 파일럿의 필수 조건이 아니다.

### Stage 6 — 모델·검색 확장

초기 확인시험이 통과한 뒤 별도 질문으로만 검토한다.

- 다른 동결 모델에서 전체 내부 비교 반복
- 결정적 문서 주입 대비 검색/keyword/hybrid 전달 비교
- 새로운 과제 가족에서 범위 재검증

이 단계 전에는 모델 간 전승, RAG 가치, 장기 운영성을 주장하지 않는다. 파인튜닝은 초기 E0 범위가 아니며 호출 예산에 포함하지 않는다.

## 3. 모델 호출과 세션 topology

### 3.1 기본식

아래 변수는 가격이 아니라 수량 계약이다.

- `N`: 짝지은 과제 인스턴스 수
- `K`: 조건 수
- `R`: 과제–조건별 독립 반복 수
- `J`: 출력당 보조 AI judge 반복 수; 기본 0
- `Q_cal`: 본 표본과 분리된 판정 calibration 또는 transport smoke 호출 수
- `Q_retry_max`: 사전 허용한 기술 실패 재시도 최대 수

계획 호출:

```text
Q_executor = N × K × R
Q_ai_judge = N × K × R × J
Q_total_max = Q_executor + Q_ai_judge + Q_cal + Q_retry_max
```

AI judge를 쓰지 않으면 `Q_ai_judge = 0`이다. 결정적 검색은 가능한 한 로컬/비모델 방식으로 두어 추가 모델 호출을 만들지 않는다. 검색 자체가 모델 호출이면 별도 조건 자원으로 계산하고 모든 관련 조건에 대칭 적용한다.

### 3.2 세션 원칙

- executor 호출 하나당 새 세션 하나를 사용한다.
- 비용을 줄이기 위해 여러 조건이나 여러 과제를 한 대화에 묶지 않는다. carryover가 생겨 인과 비교가 무효가 된다.
- fixture-author, curator, auditor, adjudicator 세션을 executor로 재사용하거나 fork하지 않는다.
- 같은 executor가 여러 호출을 수행할 수는 있으나 플랫폼 memory, cache, shared retrieval 상태를 비우거나 조건별 격리한다.
- retry는 network/transport 실패처럼 출력 내용과 무관한 사전 원인에만 허용한다. “답이 이상해 보인다”는 이유의 재호출은 금지한다.

### 3.3 token 장부

각 호출에서 다음을 분리 기록한다.

- `T_system`: 공통 system/developer wrapper token
- `T_task`: 과제 본문 token
- `T_context`: 조건별 문서 token
- `T_output_max`: 허용 출력 상한
- `T_output_actual`: 실제 출력 token
- `T_tool`: 검색·도구가 별도 과금되는 경우의 사용량

최악 입력·출력 예산:

```text
T_input_max = Σ(T_system + T_task + T_context)
T_output_budget = Q_executor × T_output_max
```

B와 D는 사전 허용오차 안에서 `T_context`를 맞춘다. A는 context가 없으므로 A/D는 총효과 비교로만 해석한다. C가 긴 경우 truncation·검색 상한을 미리 정하고 실제 잘린 양을 기록한다.

## 4. 사람 작업과 시간 장부

모델 비용만 줄이고 사람 작업을 숨기지 않는다. 다음 능동시간을 역할별로 분리한다.

| 변수 | 사람 작업 |
|---|---|
| `H_protocol` | 설계·사전등록·변경 통제 |
| `H_pattern` | 잠재 결정 패턴과 과제군 계획 |
| `H_tradition` | 합성 원천 검토와 D 정제 |
| `H_control` | B 및 선택적 C 구성·길이 감사 |
| `H_task_oracle` | 과제·숨은 oracle 작성과 판정 가능성 검토 |
| `H_leakage` | near-copy·계보·가시성 감사 |
| `H_packaging` | 해시·배정·익명화·실행 준비 |
| `H_run_ops` | 실행 감시·기술 실패 기록 |
| `H_adjudication` | blind 채점·이중 판정·불일치 해결 |
| `H_analysis` | 결과 잠금·통계·보고 |
| `H_review` | 독립 심사와 CONTROL gate 검토 |
| `H_maintenance` | 문서 상태·판본·검색 유지의 후속 시간 |

```text
H_total = Σ H_role
```

대기시간과 능동시간을 구분한다. 사용자가 직접 써야 하는 시간, 다른 사람이 필요한 시간, AI가 보조한 시간을 별도로 보고한다. 무료 노동으로 간주하지 않는다.

## 5. 현금 비용 변수

현재 문서에는 가격을 넣지 않는다. 실행 직전 공식 공급자 정보로 다음을 채운다.

- `P_in(model, tier, date)`: 입력 token 단가
- `P_cached_in(...)`: 해당하고 실제 쓰는 경우의 cached input 단가
- `P_out(...)`: 출력 token 단가
- `P_tool(...)`: 검색·도구·저장 등 별도 단가
- `P_judge(...)`: 보조 judge 모델 단가
- `P_fixed`: 승인된 기타 고정 비용
- `B_cash_pilot`, `B_cash_confirm`, `B_cash_total`: 단계별 현금 상한

최악 비용은 평균 출력이 아니라 최대 출력·허용 재시도·도구 상한으로 계산한다.

```text
C_model_max = input 최대비용 + output 최대비용 + tool 최대비용
C_judge_max = 승인된 judge 최대비용
C_cash_max = C_model_max + C_judge_max + P_fixed
```

가격 확인 출처, 확인일, 통화, 세금·환율 가정, service tier를 기록한다. 월 25만 원 같은 일반적 탐색 한도는 자동 승인액이 아니다. 이 시험의 별도 상한을 사용자가 명시적으로 승인해야 한다.

## 6. stop-before-authoring ceiling 절차

자료를 만들기 시작하면 sunk cost와 결과 유도 위험이 생긴다. 다음 순서를 지킨다.

1. 질문과 조건 수 `K`, 파일럿/확인 구분, 최소 가치 효과와 위해 기준을 먼저 정한다.
2. power 규칙으로 필요한 `N`과 `R`의 범위를 계산한다.
3. 사용할 모델·판본·tier와 현재 공식 가격을 확인한다.
4. 최대 입력·출력·도구·retry로 `Q_total_max`, token, 현금을 계산한다.
5. 위 표의 사람 작업을 role별 시간 범위와 최악값으로 추정한다.
6. 사용자가 `B_cash`, `B_human_minutes`, `B_calendar`, `B_token`, `B_calls`를 명시적으로 승인한다.
7. 계산서, 가격 확인일, 가정, 승인 범위, 해시를 동결한다.
8. 그 뒤에만 자료 작성 gate를 검토한다.

다음 중 하나면 **자료 작성 전에 중단**한다.

- 필요한 power의 최악 비용이 승인 상한을 넘음
- 사람 능동시간의 담당자·상한이 없음
- 현재 공식 가격이나 모델 판본을 확인할 수 없음
- C를 포함해야 하는 의사결정 가치가 불명확함
- 위해 도전 층과 B를 유지한 채 비용을 맞출 수 없음
- S0 연결 정보 또는 단순 대체 기준선 승인이 없음

비용을 줄일 때의 순서는 선택적 AI judge 제거, 선택적 C 제거, 반복 R 재검토, 질문 범위·가족 수 축소다. A/B/D 대칭성, 위해 도전 층, fresh-session 원칙을 제거해 비용을 맞추지 않는다. 축소로 power가 사라지면 `exploratory`로 강등하거나 보류한다.

## 7. 제안 게이트

게이트 이름은 작업용 제안이며 현재 공식 phase가 아니다.

### Gate G0 — `E0 EFFECT TEST DESIGN REVIEW`

필요:

- 다섯 설계 문서와 sidecar
- 허용 입력 해시 확인
- hostile read-only verdict
- 사실·추론·제안·비주장 구분

열 수 있는 것: CONTROL 통합 검토와 설계 수정만.

### Gate G1 — `E0 S0 INTERFACE READY`

필요:

- `selected_representation_ref` 등 연결 정보
- S0의 known limitations
- S0 결과를 전통 효과 사전 결론로 전달하지 않았다는 확인

실패 시: 임의로 D를 선택하지 않고 E0 보류 또는 단순 공개 기준선 축소안을 별도 승인.

### Gate G2 — `E0 BUDGET AND ROLE PLAN APPROVED`

필요:

- stop-before-authoring ceiling 승인
- 역할별 최대 입력과 격리
- 숨은 oracle의 저장소 밖 보관 계획
- 모델·가격·resource envelope 확인

실패 시: 자료 작성 0건 유지.

### Gate G3 — `E0 MATERIAL AUTHORING OPEN`

필요:

- 사용자에게서 이 정확한 gate의 명시적 개방
- G0–G2 통과
- 전용 경로·소유권·비공개 보관 경계

이 gate는 자료 작성만 열며 구현·실행은 열지 않는다.

### Gate G4 — `E0 IMPLEMENTATION PREFLIGHT OPEN`

필요:

- 동결 자료 해시
- 누출·판정 가능성 감사 통과
- 정확한 runner visibility와 자원 계약
- 구현 범위·검증·비밀 경계의 별도 승인

이 gate는 모델 실행을 열지 않는다.

### Gate G5 — `E0 PILOT EXECUTION OPEN`

필요:

- transport smoke와 배정 audit
- 모델 판본·가격 재확인
- 16-call 파일럿 또는 승인된 대체 크기의 최악 비용이 상한 안임
- blind adjudication 준비
- 위해 즉시 중단 권한

통과 결과: 확인시험 비용 산정 여부만.

### Gate G6 — `E0 CONFIRMATORY EXECUTION OPEN`

필요:

- 파일럿 advance 조건 통과
- A/B/D 사전등록과 exact power N
- 새 현금·사람시간 승인
- 결과를 보지 않은 독립 검토

통과 결과도 시험한 설정에 한정된 근거다. 운영 배포나 중앙 시스템 승인이 아니다.

### Gate G7 — `E0 OPTIONAL DIAGNOSTIC OR TRANSFER OPEN`

C 원본 기록, 다른 모델, 검색 방식, 새 과제군은 각각 별도 질문·예산·사전등록으로만 연다.

## 8. 중단과 rollback

| 신호 | 즉시 조치 | 롤백 지점 |
|---|---|---|
| frozen input hash 불일치 | 의존 작업 중단 | 올바른 baseline 확인 전 G0 이전 |
| S0 후보 없음·한계 과다 | 임의 표현 선택 금지 | G1 보류 또는 축소안 재심사 |
| near-copy·답 누출 | 해당 가족·관련 자료 격리 | 결과를 안 본 새 작성자로 G3 재시작 |
| oracle 모호성·판정 불일치 초과 | 실행 금지 또는 블록 무효 | task/oracle 새 판본, G3 |
| model drift·조건별 자원 불일치 | 블록 중단 | 같은 환경에서 G4/G5 재검증 |
| D-attributable critical | 남은 호출 즉시 중단 | 개입 격리, 독립 adverse review |
| 비용·token·사람시간 상한 근접 | 상한 전 중단 | 질문/조건/표본을 결과와 무관하게 재승인 |
| 파일럿 방향성 없음 | 조건 확대 금지 | D/과제 민감도 검토 또는 종료 |
| D>A이나 D≈B | 내용 효과 주장 금지 | generic/token 원인 분석, 새 설계 심사 |
| 효과 있지만 비용 guardrail 실패 | 확대 금지 | D 축소 후 새 사전시험 |
| 저장소·세션에 oracle 노출 | 관련 실행 폐기 | 새 비공개 oracle와 역할 분리부터 재시작 |

오염된 과제나 출력을 깨끗한 표본과 합치지 않는다. 수정본에는 새 버전·해시를 쓰고 어떤 결과를 본 뒤 무엇이 바뀌었는지 공개한다. 위해 중단 뒤 남은 favorable 과제만 실행하지 않는다.

## 9. S0와 병렬로 가능한 것과 기다려야 하는 것

### 지금 병렬로 가능

- 이 설계 패키지의 독립 적대적 read-only review
- reviewer 지적에 따른 설계 새 판본 제안
- 조건 필요성, 결과·위해·비용 변수의 CONTROL 검토
- 미래 역할의 충돌·최대 입력·보관 경계 기획
- 현재 가격을 넣지 않는 예산 계산 절차와 승인 양식의 의미 검토
- S0/E0 통합 gate에서 비교할 경계 체크리스트 정리

### S0 결과와 별도 gate를 기다려야 함

- `selected_representation_ref` 실제 값 채우기
- 최종 표현을 전제로 한 합성 원천·전통·B/C·과제·oracle 작성
- condition package, 검색 index, runner, 채점 도구 구현
- transport/calibration/model call
- 파일럿·확인·진단 실행과 채점
- 효과·안전·경제성·전이 판정

S0가 명확한 후보를 내지 못하면 E0가 알아서 표현을 선택하지 않는다. 설계 검토는 계속할 수 있지만 자료·구현·실행은 의존 gate가 다시 승인될 때까지 닫힌다.

## 10. 운영 결과 보고의 최소 장부

미래에 실행이 승인되면 단계별로 다음을 함께 보고한다.

- 계획·실제 과제, 조건, 반복, 호출, 재시도, 무효 수
- 입력·출력·도구 token과 최대 상한 대비 사용률
- 모델·판본·가격 출처·확인일·현금
- 역할별 능동시간과 대기시간
- 기계적 결함, 누출·oracle·판정 문제
- 효과, 위해, 비용의 서로 분리된 verdict
- 중단·rollback·새 판본 여부

문서 작성량, 호출 성공률, 교리 적용률 또는 모델 응답의 유창함은 운영 가치의 대리 통과 지표가 아니다.
