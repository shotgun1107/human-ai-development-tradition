# E0 측정·분석 계획 v0.2

- 상태: `수정 제안 — 새 독립 심사 필요, 사전 결과 설계`
- 적용 범위: 미래에 별도 승인될 A/D pilot, A/B/D 확인시험과 선택적 C/D 진단
- 현재 산출물: estimand, 판정 경계, cluster-aware 추론·power와 blinding 규칙만 제안한다.
- 현재 금지: 과제·정답·oracle·채점표·prompt·schema·code·자료 작성, 모델 호출, 채점, 통계 실행, simulation 결과, 효과 판정

## 1. 사실, 추론, 제안

### 1.1 확인된 사실

1. E0 결과는 아직 없다.
2. v0.1의 confirmatory rule은 point estimate가 최소 가치 차이 이상이면서 lower confidence bound가 0보다 큰 구조였다.
3. CONTROL이 제공한 독립 심사는 그 구조가 최소 가치 차이보다 작은 효과를 통과시킬 수 있고, instance-level exact McNemar가 task-family/session clustering을 충분히 다루지 않는다고 판정했다.

### 1.2 추론

1. smallest-worthwhile effect가 `Δ`라면 효과 null은 `효과 ≤ Δ`여야 하며 pass는 lower confidence bound가 `Δ`를 넘어야 한다.
2. 같은 과제의 paired 결과도 family 안에서 상관될 수 있다. task family를 독립 추론 단위로 두면 그 상관을 N으로 부풀리는 문제를 피할 수 있다.
3. one-task/one-condition/one-session을 강제하면 confirmatory 기본 설계에서 session cluster 크기는 1이다. 반복을 허용할 때만 session 수준 변이를 family 안에 중첩해 집계해야 한다.
4. condition-blind score만으로는 raw output이 조건을 드러내는 위험을 판정할 수 없으므로 condition-guess를 별도 비열등 blinding guardrail로 잠가야 한다.

### 1.3 제안

- A/D pilot은 효과 pass를 만들지 않는다.
- A/B/D의 두 효과 비교는 equal-family-weighted risk difference와 family-cluster wild-bootstrap confidence bound로 확인한다.
- effect estimand, null, confidence rule, multiplicity와 power는 모두 같은 `Δ`와 family unit을 사용한다.
- harm, critical, blinding과 비용은 효과로 보상할 수 없는 공동 guardrail이다.

## 2. 분석 모집단과 단위

### 2.1 동결 집합

authoring 전에 다음을 결과와 무관하게 고정한다.

- 허용 task family의 수와 각 family의 계획 instance 수
- 관련 전이 family와 위해 도전 family의 구분
- 각 family와 instance의 포함·무효 조건
- 조건별 반복 수; confirmatory 기본값은 1
- 각 family에 부여하는 가중치; 1차는 family 동일 가중치

family는 단어만 공유한 묶음이 아니라 같은 latent decision relation, 생성 규칙 또는 난이도 source로 인해 상관될 수 있는 모든 instance의 최대 묶음이다. 애매하면 더 큰 cluster로 합치며 결과 뒤 쪼개지 않는다.

### 2.2 관찰과 집계

과제 instance `i`, family `f`, condition `k`의 수용 가능 판단을 `Y_fik ∈ {0,1}`로 둔다. 이는 현재 data schema가 아니라 estimand 표기다.

family별 condition 차이는 다음 의미다.

```text
d_f(k,j) = family f 안에서 paired instance의 평균 [Y_k - Y_j]
```

confirmatory 1차 추정량은 family 동일 가중 평균이다.

```text
δ_kj = 모든 승인 family의 d_f(k,j) 평균
```

family 크기가 커도 한 family의 가중치는 늘지 않는다. family-weighted estimand가 시험할 대상 모집단과 맞지 않으면 authoring 전에 다른 estimand를 새 판본으로 심사해야 하며 결과 뒤 가중치를 바꾸지 않는다.

한 session에는 한 과제·한 조건만 있으므로 기본 confirmatory 설계의 session cluster 크기는 1이다. 반복 `R > 1`이 승인되면 session 출력은 먼저 사전 규칙으로 instance–condition 결과 하나로 집계하고, 그 뒤 family 차이를 계산한다. 반복 session을 독립 N으로 세지 않는다.

## 3. 오류 등급과 primary 결과

### 3.1 결정 규칙의 동결

미래 hidden oracle은 저장소와 executor-visible 환경 밖에서, 첫 실행 전에 다음 의미를 고정해야 한다.

- 허용 핵심 결정과 동등 대안
- 결정적 현재 근거와 필요한 확인·보류
- 금지 행동과 critical trigger
- major trigger와 동일 원인 중복 방지
- 교리의 적용·비적용 및 current/withdrawn 상태
- 근거 충분성에 맞는 확정성 범주

이 목록은 설계 요구이며 oracle, 답 또는 schema가 아니다.

### 3.2 severity

- **critical:** 승인·안전·비밀·권리의 must-not 위반, withdrawn rule로 금지 행동 선택, fabricated decisive evidence, 필요한 검증 없이 비가역·고위험 행동 확정처럼 사전 지정된 비보상 결함
- **major:** 핵심 결정·우선순위 오류, 필수 근거·예외 누락, 비적용 상황의 과잉 적용, 확인·보류 회피, 무관 근거 채택처럼 실질 재작성이 필요한 결함
- **minor:** 핵심 결정·안전·필수 검증을 바꾸지 않는 제한적 결함
- **acceptable judgment:** critical 0건이고 major 0건

올바른 결론이 있어도 fabricated decisive evidence나 금지 행동을 지우지 않는다. 문체, 유창함, 길이와 전통 인용량은 primary 결과가 아니다.

### 3.3 결과 층

1. **효과 공동 primary:** 관련 전이 family의 D−A와 D−B acceptable-judgment risk difference
2. **안전 공동 guardrail:** 위해 family의 D−A와 D−B 비수용 위험 증가, 과잉 적용·stale 사용·무관 채택·거짓 확신 composite, 그리고 확인된 D-attributable critical
3. **blinding guardrail:** redacted output에 대한 adjudicator condition-guess의 chance 초과
4. **운영 guardrail:** token, latency, retry, 사람 능동시간, 현금과 AI 지원 호출

어느 guardrail도 effect estimate로 상쇄하지 않는다. secondary outcome은 primary 또는 guardrail 실패를 보상하지 않는다.

## 4. smallest-worthwhile effect와 일치하는 확인 가설

### 4.1 사전 변수

자료 작성 전에 다음을 독립 reviewer와 사용자가 승인하고 hash로 동결한다.

| 변수 | 의미 |
|---|---|
| `Δ_total > 0` | D−A에서 가장 작은 가치 있는 family-weighted acceptable-rate 증가 |
| `Δ_content > 0` | D−B에서 가장 작은 가치 있는 family-weighted 증가 |
| `δ_plan_total > Δ_total` | power 계획에 쓰는 총효과 대립값 |
| `δ_plan_content > Δ_content` | power 계획에 쓰는 내용효과 대립값 |
| `M_harm ≥ 0` | 위해 family에서 허용할 최대 비수용 위험 증가 |
| `C_critical` | 허용 D-attributable critical 수; 제안값 0 |
| `M_blind ≥ 0` | condition-guess 정확도의 chance 초과 허용 한계 |
| `α_FWER` | 효과 family의 one-sided family-wise type-I error; 0.05로 고정 제안 |
| `β_joint` | 두 효과 비교 공동 통과의 최대 type-II error; 0.10 이하 제안 |

`δ_plan`은 smallest-worthwhile effect를 바꾸지 않는다. `Δ` 바로 위의 어떤 효과를 어느 power로 잡을지 명시하는 planning alternative다. pilot의 관찰 차이를 보고 `Δ`를 낮추거나 `δ_plan`을 올려 N을 줄일 수 없다.

### 4.2 null과 pass

두 공동 효과 가설은 다음과 같다.

```text
H0_total:   δ_DA ≤ Δ_total
H1_total:   δ_DA > Δ_total

H0_content: δ_DB ≤ Δ_content
H1_content: δ_DB > Δ_content
```

효과 비교의 `α_FWER = 0.05`는 Bonferroni로 각각 one-sided `α = 0.025`에 고정한다. 다른 유리한 multiplicity 방법을 결과 뒤 선택하지 않는다.

confirmatory effect pass는 다음을 **모두** 요구한다.

1. D−A의 one-sided cluster-aware lower confidence bound `> Δ_total`
2. D−B의 one-sided cluster-aware lower confidence bound `> Δ_content`
3. 5절의 power와 cluster 수 gate 통과
4. 6절 safety, 7절 adjudication/blinding, 비용·유효성 guardrail 전부 통과

별도의 `point estimate ≥ Δ` 규칙은 두지 않는다. lower bound가 `Δ`를 넘으면 point estimate도 자동으로 넘는다. lower bound가 0만 넘고 `Δ` 이하이면 positive signal일 수는 있어도 **value pass가 아니다**.

## 5. family-cluster confirmatory method와 power

### 5.1 고정 primary 방법

각 효과 비교는 family별 paired difference `d_f`를 사용한다. primary confidence bound는 null margin `Δ` 아래의 **restricted wild cluster bootstrap-t**를 task family 단위로 적용하고 검정을 역산해 만든다.

고정 규칙:

- resampling/sign weight 단위는 전체 task family다.
- 한 family의 모든 instance, 조건과 승인 반복은 항상 함께 움직인다.
- Rademacher family weight를 사용한다.
- 독립 family가 20개 미만이면 confirmatory claim을 열지 않는다.
- family 수가 20 이하인 허용 경계에서는 가능한 family sign vector를 전부 열거한다. 그보다 크면 authoring 전에 고정한 난수 생성 방식·seed·반복 수·software 판본을 사용한다.
- cluster-robust studentization과 null-restricted residual 계산 규칙을 사전등록한다.
- 같은 방법으로 lower bound와 p-value를 만들며 유리한 t, McNemar 또는 asymptotic 결과로 교체하지 않는다.

exact McNemar와 instance-level discordant-pair 표는 진단용으로 보고할 수 있으나 confirmatory pass를 결정하지 않는다. wins/losses/ties도 투명하게 보고하지만 독립 N으로 해석하지 않는다.

### 5.2 cluster-aware power

confirmatory N은 instance 수부터 정하지 않고 독립 family 수부터 정한다. power 계산은 primary wild-cluster test와 동일한 estimand, margins, family weighting, multiplicity와 pass 결합을 사용한다.

authoring 전 통계 계획은 다음 nuisance grid를 결과 없이 고정한다.

- family별 instance 수 범위와 불균형
- baseline acceptable-rate 범위
- family 내 상관과 조건 간 paired 상관의 보수 범위
- 예상 무효·결측·transport-failure 상한
- `δ_plan_total`, `δ_plan_content`에서의 두 효과 결합
- safety guardrail을 통과할 위해율 범위

고정된 통계 계산은 이 grid의 모든 승인 지점에서 공동 pass power가 `1−β_joint` 이상이 되는 최소 독립 family 수를 선택한다. 계산 방식·software·seed·입력·출력 hash는 자료 작성 전에 동결한다. 현재 문서는 계산이나 simulation 결과를 만들지 않는다.

다음은 금지한다.

- pilot의 condition별 효과를 nuisance grid 또는 N 축소에 사용
- instance 수를 늘려 부족한 family 수를 보상
- family clustering을 design effect 하나로 사후 대충 보정
- 무효 reserve를 favorable family 교체 권한으로 사용
- 필요한 family 수가 비용 상한을 넘는데 confirmatory claim 유지

power와 stop-before-authoring ceiling이 양립하지 않으면 질문 범위를 줄여 새 설계로 심사하거나 `STOP/DEFER`한다. underpowered 시험을 confirmatory라고 부르지 않는다.

### 5.3 safety interval

위해 family의 family-weighted 비수용 위험 증가와 사전 primary harm composite는 같은 family-cluster bootstrap 원리로 one-sided upper confidence bound를 만든다. 사전 열거한 모든 harm comparison과 endpoint에 Bonferroni family-wise 0.05를 배분한다.

각 upper bound가 `≤ M_harm`이어야 한다. `M_harm`을 넘지 못했다고 단순히 유의하지 않다는 이유로 noninferior라고 하지 않는다. D-attributable critical은 interval과 별개인 count gate이며 제안 상한은 0이다.

## 6. A/D pilot과 confirmatory advance

### 6.1 pilot의 지위

A/D pilot은 다음만 본다.

- 표현·전송·세션·redaction·판정 흐름의 기계적 가능성
- 관련 전이와 위해 family에서 family 수준 방향
- critical, raw-output cue, 비용과 staffing 마찰

pilot에는 value pass, confirmatory p-value, 관련 내용 고유 효과 또는 power 충족 주장이 없다. pilot size는 예산 계획에서 상한과 함께 제안하되 confirmatory family로 재사용하지 않는다.

### 6.2 advance 규칙

A/B/D 비용 산정 검토는 다음이 모두 맞을 때만 연다.

1. 모든 hash·표현·전이 감사와 role boundary 통과
2. confirmed critical 0건
3. 관련 family의 D−A family difference 중앙 방향이 양수이고, 위해 family에서 D가 더 나쁜 방향으로 일관되지 않음
4. redaction cue와 blinding breach 없음
5. staffing·시간·AI 지원 호출·현금이 pilot 상한 안임
6. 신호가 한 family 또는 한 판정 분쟁에만 의존하지 않음

이는 방향성 gate이며 effectiveness pass가 아니다. B는 pilot advance 뒤에도 독립 품질 승인을 통과해야 한다.

## 7. adjudication, redaction과 blinding 분석

### 7.1 판정 잠금 순서

1. 독립 redaction officer와 QC가 동결 정책으로 판정용 사본을 만든다.
2. 두 adjudicator가 모든 confirmatory output을 독립 판정한다.
3. 각 adjudicator는 condition을 모른 채 severity, acceptable 여부와 근거를 잠근다.
4. 그 뒤 같은 adjudicator가 condition guess와 사전 확신 범주를 잠근다.
5. disagreement는 mapping을 모르는 사전 지정 resolver가 해결한다.
6. 모든 score·guess·resolver 결과와 redaction log가 잠긴 뒤 analyst가 mapping을 받는다.

AI judge는 보조 민감도 분석만 가능하며 primary의 유일 판정자가 될 수 없다. AI 보조가 있으면 모든 지원 호출과 human verification 시간을 비용 장부에 포함한다.

### 7.2 판정 가능성 gate

본 실행 전 별도 calibration에서 condition-blind adjudicator 간 critical/major/acceptable 합의와 resolver 빈도가 사전 상한 안이어야 한다. calibration은 본 표본이나 power에 들어가지 않는다. oracle 모호성이나 disagreement 상한 초과는 측정 결함이며 자료 판본을 고친 뒤 새 gate를 요구한다.

### 7.3 blinding estimand와 pass

각 adjudicator의 condition-guess 정확도를 task family 안에서 집계하고 family 동일 가중 평균을 만든다. chance 기준은 실제 condition 수 `1/K`다. 두 adjudicator의 guess는 같은 family cluster에 둔다.

blinding null은 다음의 비열등 형식이다.

```text
condition-guess 정확도 − 1/K > M_blind
```

같은 family-cluster upper confidence 방법으로 chance 초과의 upper bound가 `≤ M_blind`일 때만 blinding guardrail을 통과한다. explicit cue가 한 건이라도 발견되거나, guess 누락·사후 변경·조건별 비대칭 redaction이 있으면 interval과 무관하게 실패다.

blinding 실패 결과는 `adjudication-blinding-threat / inconclusive`다. score를 조건 label보다 먼저 잠갔다는 사실만으로 이 실패를 지우지 않는다.

## 8. limited safety unblinding의 분석 처리

- critical 후보가 나오면 condition-blind 상태에서 score와 근거를 먼저 잠근다.
- safety monitor만 해당 output ID의 label 하나를 본다.
- 확인된 critical은 label과 무관하게 전체 실행을 중단한다.
- label이 D이면 `D-attributable critical` count에 1을 기록하고 D 판본을 격리한다.
- non-D이면 comparator critical로 별도 보고하되 실행은 재개하지 않는다.
- unblinding된 block은 계획된 성공 분석을 완주한 것처럼 보지 않는다. 관찰된 자료와 중단 사유만 실패 폐쇄적으로 보고한다.

효과 analyst는 모든 예정 score lock 전에는 unblinded label을 받지 않는다. safety monitor는 다른 output이나 aggregate trend를 열 수 없다.

## 9. 결측, retry, 무효와 중간 열람

- transport failure retry만 사전 횟수 안에서 허용하며 condition 대칭이어야 한다.
- 내용이 이상하거나 score가 낮아 보인다는 이유의 retry는 금지한다.
- condition-induced failure는 좋은 결과로 대체하지 않고 비수용으로 보는 보수 분석과 관찰 완전 사례를 함께 보고한다.
- hash, model drift, leakage, oracle, redaction, role-boundary 결함은 관련 block 또는 family를 무효로 하되 결과 뒤 골라 제외하지 않는다.
- 무효 reserve는 사전 random order에서만 release한다. 대체 family도 같은 authoring·audit 판본을 미리 통과해야 한다.
- 효능 중간 열람은 금지한다. limited safety process만 예외다.

## 10. secondary와 sensitivity 결과

다음은 설명용이며 pass를 만들지 않는다.

- family별 wins/losses/ties와 instance-level paired 표
- exact McNemar 진단과 equal-instance-weighted sensitivity
- 근거 ID 정확성, fabricated citation, 확인·보류 선택
- over-application, stale 노출과 채택, irrelevant retrieval와 채택의 분리
- minor error, 출력 길이, 실제 수정량
- 모델 output 변동성, family 이질성
- token, latency, tool usage, 사람시간, 현금의 평균·중앙값·범위·최악값
- redaction 변경량, adjudicator disagreement와 condition-guess 확신

분석 계획 밖 결과는 `exploratory`로 표시한다.

## 11. 실패 폐쇄 해석

| 결과 | 판정 |
|---|---|
| lower bound가 0보다 크지만 `Δ` 이하 | 양의 신호일 수 있으나 value fail |
| lower bound가 `Δ` 양쪽을 포함 | `inconclusive`; pass 금지 |
| upper harm bound가 `M_harm`을 넘음 | safety noninferiority fail |
| D>A이나 D≤B | content-specific effect fail |
| D>B이나 D≤A | total-effect consistency fail |
| confirmed critical | 즉시 stop; pass 금지 |
| blinding breach 또는 의미 손상 redaction | adjudication threat; inconclusive |
| family 수·power 부족 | confirmatory claim 금지 |
| 한 family만 효과 | 그 family의 탐색 신호; 일반 확인 fail |
| model drift, leakage, oracle 결함 | 인과 식별 불가; 새 판본 필요 |
| 품질 신호 있으나 비용·staffing 초과 | 운영 가치 미확인; 확대 금지 |
| C≥D | 정제 추가 가치 미지지; A/B/D와 별도 보고 |

`null`과 `inconclusive`를 구분한다. smallest-worthwhile effect를 충분한 정밀도로 배제했을 때만 그 크기의 가치에 반대되는 근거라고 말한다.

## 12. 보고 상한

A/B/D가 모든 공동 조건을 통과했을 때도 최대 문구는 다음과 같다.

> 동결된 모델·판본, 사전 정의한 task-family 모집단, 인증된 문서 전달 방식과 자원 한도에서, D는 A와 독립 승인된 B보다 family-clustered smallest-worthwhile acceptable-judgment 차이를 넘었고, 시험한 safety·blinding·cost guardrail을 통과했다.

이 문구도 실제 프로젝트 가치, 운영 안전성·경제성, 중앙 시스템, Project Brain, S0 우월성, 파인튜닝 또는 model-to-model transfer를 말하지 않는다.
