# E0 독립 심사 brief v0.1

- 심사 종류: `hostile read-only design review`
- 심사 대상: E0 전통 효과시험 설계 패키지 v0.1
- 제안 라벨: `E0`는 아직 동결된 공식 단계가 아니다.
- 심사 권한: 설계의 CONTROL 통합 검토 적합성만 판정
- 권한 없음: 자료·oracle·코드·prompt·runner 작성, 모델 실행, 채점, gate 개방, 효과 주장

## 1. 심사 목적

이 심사는 설계를 좋게 설명하는 것이 아니라 다음 반증 질문에 답한다.

> 이 설계를 그대로 사전 고정하고 미래의 별도 승인 아래 수행했을 때, 정제된 전통 내용의 효과를 추가 token, 일반 조언, 원본 기록, 모델 변화, prompt 차이, 평가자 재량과 구분할 수 있으며, 동시에 음의 전이와 비용 폭증을 숨기지 않는가?

리뷰어는 “문서가 자세하다”를 품질 증거로 세지 않는다. 가장 작은 시험이 실제로 falsifiable한지, 긍정 결과에 허용되는 주장 상한이 충분히 낮은지, 부정·혼합 결과가 실패 폐쇄적으로 끝나는지를 공격적으로 본다.

## 2. 독립성과 읽기 전용 경계

리뷰어는 다음을 하지 않는다.

- 설계자를 대신해 누락 절을 작성하거나 수치·과제·정답을 채움
- 저장소를 폭넓게 검색하거나 과거 제안·심사·실행 결과를 읽음
- S0 질문 계약 초안, S0 자료, 봉인 자료, 숨은 oracle을 요청함
- 실제 고객·개인·비밀·과거 프로젝트 내용을 예로 들거나 입력으로 사용함
- 조건 자료·task family item·executor prompt·judge prompt·schema·코드를 생성함
- 특정 S0 표현 후보, 특히 D를 이미 선택됐다고 가정함
- 결과가 없는 상태에서 효과·안전·경제성·전이를 판정함

읽기 전용 심사 결과는 별도 review 경로에 둘 수 있으나, 이 brief 자체는 리뷰어에게 저장소 수정 권한을 주지 않는다.

## 3. 최대 입력 추천

리뷰어에게 주는 **최대 입력 packet**은 아래로 제한한다. 더 많은 저장소 맥락은 독립성을 높이지 않고 과거 답·S0 초안·미검증 결과에 끌릴 위험을 키운다.

### 3.1 E0 대상 패키지

1. `docs/tradition/e0-effect-test/README.md`와 sidecar
2. `docs/tradition/e0-effect-test/e0-effect-test-design-v0.1.md`와 sidecar
3. `docs/tradition/e0-effect-test/e0-measurement-and-analysis-plan-v0.1.md`와 sidecar
4. `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.1.md`와 sidecar
5. `docs/tradition/e0-effect-test/e0-independent-review-brief-v0.1.md`와 sidecar

### 3.2 허용 기준선

1. `AGENTS.md`
2. `docs/tradition/s0-e0-boundary-and-parallel-work.md`와 그 `.sha256`
3. `docs/tradition/purpose-and-philosophy.md`
4. `docs/tradition/central-system-v2-common-baseline.md`와 그 `.sha256`
5. `docs/tradition/roadmap-and-evaluation.md`

### 3.3 명시적 제외

- `s0-lab/**`
- S0 질문 계약 draft/review, S0 candidate, executor 결과
- sealed material, hidden answer/oracle, condition mapping
- 실제 또는 합성 fixture, future prompt, code, tool output
- repository history, 다른 proposal/review, 실제 과거 프로젝트 자료
- web research와 현재 API 가격 조사

해시가 맞지 않거나 입력 packet이 최대 범위를 넘으면 심사를 시작하지 않고 `INPUT-BOUNDARY-FAIL`을 낸다. 리뷰 중 더 많은 자료가 필요해 보이면 무엇을 왜 필요한지 CONTROL에 질문할 수 있지만 직접 읽지 않는다.

## 4. 심사 방식

각 rubric 항목에 `PASS / FAIL / UNCLEAR`와 근거 위치를 기록한다. 문구 개선과 인과 결함을 구분하고, 결함마다 다음을 적는다.

- severity: `blocking / major / minor`
- 실패하는 인과 또는 운영 주장
- 현재 문서의 근거 위치
- 최소 수정 방향; 완성 문구나 자료는 작성하지 않음
- 재심사가 필요한 파일과 범위

`UNCLEAR`가 통과로 계산되지 않는다. blocking 항목 하나라도 있으면 전체 통과가 아니다.

## 5. hostile rubric

### 5.1 상태·경계·비주장

- E0가 제안 라벨로만 취급되고 공식 phase나 완료된 시험처럼 쓰이지 않는가?
- S0, 중앙 시스템, Project Brain, 운영 안전성, 경제성, 모델 간 전승의 구현·검증을 주장하지 않는가?
- 설계와 미래 자료 작성·구현·실행 gate가 분리됐는가?
- 초기 방식이 외부 문서 주입/검색이며 모델 학습·파인튜닝으로 오표현되지 않는가?
- 실제 고객·개인·비밀·과거 프로젝트 자료가 완전히 배제됐는가?

### 5.2 좁고 반증 가능한 인과 질문

- intervention, comparator, outcome, unit, setting이 결과 전에 고정 가능한가?
- mechanical correctness가 causal effectiveness와 분리됐는가?
- A–D가 package total effect만 말한다는 제한이 일관적인가?
- D–B가 관련 내용과 token/format/generic advice를 구분하도록 B가 충분히 강한가?
- C가 정제 우위 질문에만 필요하며 최소 시험을 불필요하게 부풀리지 않는가?
- 네 조건을 모두 쓰는 조건과 쓰지 않는 조건이 결정 규칙으로 설명되는가?

### 5.3 표면 변화와 답 누출

- 원천 경험과 후속 과제가 문장·식별자·값이 아니라 잠재 결정 관계만 공유하는가?
- D가 후속 답이나 near-copy를 포함하면 가족 전체를 격리하는가?
- task/oracle author가 최종 D를 보지 않고 curator가 future task/oracle을 보지 않는가?
- leakage auditor가 결과 전에 두 쪽을 비교하는가?
- 현재 task가 전통 없이도 자족적이어서 D가 독점 사실을 주입하지 않는가?
- 추상 예가 future candidate item으로 전용되지 않도록 금지했는가?

### 5.4 음의 전이와 stale doctrine

- 관련 전이뿐 아니라 비적용 유사성, 경계·불충분 정보, stale/withdrawn, 무관 검색 층이 있는가?
- over-application, stale use, irrelevant retrieval, false confidence, verification avoidance, cost inflation을 각각 관찰하는가?
- withdrawn 항목의 “필터 실패”와 “노출 뒤 현재 규칙으로 채택”을 구분하는가?
- 관련 과제의 이득이 critical adverse transfer를 보상하지 못하게 했는가?
- 위해 신호가 나오면 남은 실행을 중단하고 오염된 표본을 재사용하지 않는가?

### 5.5 fresh session과 model control

- 한 과제–한 조건–한 fresh session 원칙이 분명한가?
- 같은 대화에서 A 뒤 D를 주는 carryover가 금지됐는가?
- fixture/curator/adjudicator 대화가 executor로 fork되지 않는가?
- 모델 ID·snapshot·추론·sampling·도구·wrapper·시간창이 고정·보고되는가?
- model drift가 생기면 결과를 이어 붙이지 않는가?
- 한 모델 안의 효과와 모델 업그레이드·모델 간 전승이 분리되는가?

### 5.6 결과와 오류 논리

- critical, major, minor의 관찰 기준이 미래 oracle에 결정적으로 고정 가능한가?
- fabricated decisive evidence나 withdrawn doctrine 사용이 정답 결론 뒤에 숨지 않는가?
- primary outcome이 문체·유창함·교리 인용량이 아니라 수용 가능한 판단인가?
- 효과와 안전이 공동 비보상 결과인가?
- secondary outcome이 primary 실패를 보상하지 않는가?
- 사람 adjudicator가 condition blind이며 AI judge가 유일 판정자가 아닌가?
- oracle 모호성 또는 judge 불일치가 측정 결함으로 닫히는가?

### 5.7 짝지음·순서·통계

- 같은 과제를 조건별 독립 세션에 배정해 paired unit을 보존하는가?
- 반복 호출을 독립 N으로 부풀리지 않는가?
- condition order가 family/time block 안에서 균형 무작위화되는가?
- paired binary result에 exact method를 제안하는가?
- `Δ_total`, `Δ_content`, `M_harm`, 비용 상한이 결과·자료 작성 전에 고정되는가?
- 파일럿이 effect pass를 만들지 않는가?
- confirmatory N이 smallest worthwhile effect, harm margin, power, clustering, invalid reserve에서 계산되는가?
- multiplicity와 one-sided error budget을 사전에 통제하는가?
- null과 imprecise inconclusive를 구분하는가?

### 5.8 token·prompt·raw-history confound

- A–D input-length 차이의 해석 제한이 보고 상한까지 유지되는가?
- B가 token, 구조, generic guidance, source-density를 맞추면서 latent pattern에는 무관한가?
- 공통 prompt·tool·output envelope가 모든 조건에서 같은가?
- C의 truncation·selection이 결과와 무관하게 사전 고정되는가?
- 사후 token 공변량 보정만으로 content confound를 해결했다고 하지 않는가?

### 5.9 비용과 한 사람 운영성

- 8 paired task, A/D, 16 executor call 파일럿이 feasibility 선별로만 쓰이는가?
- confirmatory call 수가 `N × K × R`로 투명한가?
- AI judge와 C가 기본 비용에 몰래 포함되지 않는가?
- 사람 authoring, leakage audit, adjudication, analysis 시간이 모두 장부에 있는가?
- current API price를 발명하지 않고 실행 시점 공식 가격을 요구하는가?
- worst-case output·retry·tool 비용을 자료 작성 전에 승인하는가?
- 상한을 맞추려고 B, 위해 층, fresh session을 제거하지 않는가?
- power와 상한이 양립하지 않으면 exploratory 강등 또는 중단하는가?

### 5.10 역할·비밀·결과 잠금

- worktree가 secret boundary로 오해되지 않는가?
- hidden oracle이 repo·executor-visible worktree/session 밖에 있는가?
- condition mapping과 output이 adjudication 뒤까지 분리되는가?
- analyst가 locked scores 뒤에 mapping을 받는가?
- 결과를 본 뒤 task, threshold, exclusion, retry를 바꾸지 않는가?
- 한 사람이 여러 역할을 맡을 때 최소 비겸임과 노출 순서가 있는가?

### 5.11 주장 사다리

- mechanical pass, A/D pilot, A/B/D confirmation, optional C/D, multi-model replication이 서로 다른 주장만 지지하는가?
- A/B/D pass도 특정 모델·과제군·전달 방식으로 제한되는가?
- 실제 프로젝트, 안전, 경제성, 중앙 시스템, Project Brain, 파인튜닝, model-to-model transfer가 명시적으로 제외되는가?
- null/mixed/adverse 결과가 `inconclusive`, scope reduction, fail, stop 중 하나로 닫히는가?

## 6. 비보상 blocking failures

다음 중 하나라도 있으면 다른 장점이나 문서 완성도로 보상할 수 없다.

1. frozen baseline hash 불일치 또는 허용 입력 밖 자료 사용
2. E0를 공식·완료 phase로 표현하거나 존재하지 않는 결과 주장
3. S0가 D 또는 특정 표현을 선택했다고 가정하거나 `selected_representation_ref` 없이 자료·실행 진행 허용
4. A–D 파일럿만으로 관련 전통 내용의 효과를 confirmatory pass 처리
5. D가 후속 답·near-copy·독점 해결 사실을 포함할 수 있는 구조
6. curator와 task/oracle author의 결과 전 정보 격리 부재
7. 관련 전이만 있고 비적용·stale/withdrawn 위해 시험이 없음
8. critical adverse transfer가 품질·속도 점수로 상쇄됨
9. 같은 세션의 조건 crossover, executor의 다른 조건·oracle 접근, 또는 fixture-author thread의 executor 전환
10. 조건 간 model/prompt/tool/resource 차이를 전통 효과로 셈
11. condition-aware 또는 사후 재량 adjudication이 primary verdict를 결정
12. 결과 뒤 threshold, N, exclusion, retry, task, condition을 유리하게 변경 가능
13. 사람시간·최악 token·현금 상한을 자료 작성 뒤에 승인
14. 필요한 power가 budget과 양립하지 않는데 confirmatory claim 유지
15. 실제 고객·개인·비밀·과거 프로젝트 자료 사용
16. hidden oracle을 repository 또는 executor-visible worktree/session에 저장
17. 문서 주입·검색 효과를 model learning, fine-tuning 또는 model-to-model transfer로 주장
18. pass를 중앙 시스템·Project Brain·실제 운영 안전·경제성 검증으로 확대

## 7. 조건 수에 대한 필수 판정

리뷰어는 단순히 “네 조건이 더 완전하다”고 하지 말고 다음 verdict를 각각 낸다.

1. **A/D 파일럿:** 가장 작은 falsifiable total-package test로 충분한가? 아니라면 최소 추가 조건과 이유는 무엇인가?
2. **B 필요성:** 관련 내용의 고유 효과를 주장하기 전에 필수인가? B의 형식·관련성 통제가 실제로 가능한가?
3. **C 필요성:** 현재 결정에 정제 우위가 필요한가, 아니면 비용만 늘리는가?
4. **네 조건 동시 실행:** 세 인과 질문을 함께 답할 가치가 표본 분산·비용보다 큰가?

권장 기본 판정은 `A/D = pilot only`, `A/B/D = content confirmation`, `C = optional curation diagnostic`이다. 리뷰어는 이를 뒤집을 수 있지만 어떤 인과 질문과 비용을 바꾸는지 명시해야 한다.

## 8. 필수 심사 산출

심사 보고는 다음 순서와 내용을 가져야 한다.

1. 읽은 파일과 SHA-256, 입력 경계 준수 확인
2. 전체 blocking finding 목록; 없으면 `none`
3. rubric 각 절의 `PASS / FAIL / UNCLEAR`
4. A/D, B, C, 네 조건에 대한 별도 verdict
5. primary outcome·critical/major·deterministic adjudication verdict
6. threshold·paired analysis·power rule verdict
7. fresh-session·model-version·prompt/token confound verdict
8. adverse transfer·stale/withdrawn·cost inflation verdict
9. stop-before-authoring 예산·gate·rollback verdict
10. 허용 주장과 금지 주장 상한 verdict
11. 재심사에 필요한 최소 수정 목록
12. 다음 review의 최대 입력 추천; 기본값은 이 brief 3절을 넘지 않음
13. 최종 verdict 하나

리뷰어는 fixture, oracle, 코드, prompt 또는 handoff를 산출하지 않는다.

## 9. 최종 verdict

다음 중 하나만 선택한다.

### `PASS-FOR-CONTROL-INTEGRATION-ONLY`

- blocking failure 0건
- 모든 핵심 rubric이 PASS
- UNCLEAR는 minor 표현에만 있고 인과·위해·비용·gate를 바꾸지 않음
- 의미: CONTROL이 S0/E0 경계와 설계 연결을 검토할 수 있음
- 의미하지 않음: 자료 작성, 구현, 실행 또는 E0 효과 승인

### `REVISE-AND-REVIEW`

- 고칠 수 있는 blocking/major/UNCLEAR가 하나 이상 있음
- 리뷰어는 최소 수정 범위와 재심사 파일을 지정
- 수정본은 새 버전·해시로 만들며 현재 판본을 조용히 덮지 않음

### `STOP-DESIGN`

- 답 누출 없는 전이 과제를 만들 수 없는 구조
- 역할·비밀 경계를 지킬 수 없음
- smallest worthwhile effect를 검출할 power가 비용 상한과 구조적으로 양립하지 않음
- 위해를 비보상으로 측정할 수 없음
- 인과 질문이 문서 주입 외의 model/tool change와 분리 불가능함

입력 hash 또는 범위가 잘못된 경우에는 위 세 verdict 전에 `INPUT-BOUNDARY-FAIL`로 멈춘다.

## 10. 다음 gate 추천의 상한

이 v0.1 설계에 대한 최선의 긍정 판정도 다음을 넘지 않는다.

> `E0 EFFECT TEST DESIGN REVIEW` 통과 후보로 CONTROL 통합 검토에 보낸다.

리뷰어가 자료 작성 gate를 직접 열거나, S0 결과를 채우거나, 예산을 승인하거나, runner 구현·모델 실행을 권고해서는 안 된다. CONTROL 통합 검토 뒤에도 `selected_representation_ref`, stop-before-authoring ceiling, 역할 격리, 사용자 명시 승인 중 하나라도 없으면 다음 단계는 보류다.
