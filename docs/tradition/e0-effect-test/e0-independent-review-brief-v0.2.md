# E0 독립 심사 brief v0.2

- 심사 종류: `hostile read-only revision review`
- 심사 대상: E0 효과시험 설계 v0.2
- 심사 목적: v0.1의 B-01과 M-01~M-07이 우회 없이 닫혔는지 독립 판정
- 권한: CONTROL 통합 검토 적합성만 판정
- 권한 없음: 자료·과제·정답·oracle·prompt·schema·code 작성, 가격 조회, 모델 호출, 채점, 통계 실행, gate 개방, 효과·안전·경제성 주장

## 1. 심사 질문

> v0.2를 결과 전에 그대로 동결한다면, 단일 표현 참조를 우회하지 않고, smallest-worthwhile effect와 family-cluster 추론을 일치시키며, near-copy·B quality·safety unblinding·raw-output blinding·staffing/cost를 재현 가능한 비보상 gate로 만들 수 있는가?

문서의 길이, 역할 수 또는 보수적 문구 자체는 PASS 근거가 아니다. reviewer는 실제 authoring·실행 경로에서 재량 우회가 남는지를 찾는다.

## 2. 입력 경계

### 2.1 최대 입력 packet

1. `AGENTS.md`
2. `docs/tradition/s0-e0-boundary-and-parallel-work.md`와 sidecar
3. `docs/tradition/purpose-and-philosophy.md`
4. `docs/tradition/central-system-v2-common-baseline.md`와 sidecar
5. `docs/tradition/roadmap-and-evaluation.md`
6. `docs/tradition/e0-effect-test/README.md`와 sidecar
7. v0.1 design, measurement, operating, independent-review brief와 각 sidecar
8. v0.2 design, measurement, operating, revision-response, independent-review brief와 각 sidecar

revision-response v0.2에 보존된 CONTROL-supplied v0.1 verdict·finding 요약을 심사 입력으로 사용한다. 다른 review record를 찾지 않는다.

### 2.2 명시적 제외

- repository history와 넓은 repository search
- `s0-lab/**`, S0 draft/candidate/output
- sealed/private 자료, hidden oracle·answer, condition mapping
- 실제 또는 합성 fixture·task·condition package
- executor/adjudicator prompt, schema, code, tool output, simulation 또는 결과
- 다른 proposal/review, 실제 고객·개인·비밀·과거 프로젝트 자료
- web, 현재 모델 가격과 공급자 조사

모든 available same-basename sidecar를 먼저 검증한다. hash 불일치, 누락 또는 최대 입력 초과는 `INPUT-BOUNDARY-FAIL`이다.

## 3. 독립성과 방식

- reviewer는 v0.2 authoring session을 상속하거나 author와 협상해 결함을 고치지 않는다.
- finding마다 `PASS / FAIL / UNCLEAR`, severity, 실패하는 주장, 근거 위치, 최소 수정 방향과 재심사 범위를 기록한다.
- `UNCLEAR`는 PASS가 아니다.
- reviewer는 실제 수치·자료·oracle·prompt·code를 대신 만들지 않는다.
- worktree 분리를 비밀 보안이나 reviewer 독립성 증거로 세지 않는다.
- v0.1 review finding마다 별도 verdict를 내고 전체 장점으로 blocking/major를 보상하지 않는다.

## 4. B-01 blocking 재심사

다음을 모두 확인한다.

- authoring 전에 활성 `selected_representation_ref`가 정확히 하나인가?
- 참조가 version, owner, SHA-256, 승인 근거, 범위, known limitations, replacement 관계를 가진 artifact인가?
- CONTROL-approved public fallback도 먼저 같은 artifact가 되고 유일 참조로 인증돼야 하는가?
- `후보 또는 fallback`, inline 설명, 임시 공개 형식, 사람 재량 같은 우회가 모두 stop인가?
- B/C/D와 A wrapper가 같은 표현 계약을 사용하는가?
- 참조 변경이 기존 authoring·audit·result의 효력을 끝내는가?
- hash·판본·한계 불일치가 authoring 전 fail인가?

하나라도 아니면 B-01은 `FAIL`이며 전체 PASS는 불가하다.

## 5. M-01 가치 임계값 재심사

- effect estimand가 family-weighted acceptable-judgment risk difference로 한 번 정의되는가?
- `Δ_total`, `Δ_content`가 smallest-worthwhile effect인가?
- null이 각각 `δ ≤ Δ`이고 pass lower bound가 `> Δ`인가?
- lower bound `> 0`과 point estimate `≥ Δ`의 v0.1 loophole이 사라졌는가?
- power alternative `δ_plan > Δ`가 same estimand·family·multiplicity에 연결되는가?
- pilot 결과로 `Δ`, `δ_plan`, N을 유리하게 바꾸지 못하는가?
- 보고 문구도 smallest-worthwhile bound를 넘었다고만 말하는가?

point와 interval이 다른 가치 질문을 말하거나 0 초과만으로 pass할 수 있으면 `FAIL`이다.

## 6. M-02 clustering 재심사

- task family가 독립 추론·resampling 단위인가?
- family 크기와 상관없이 primary는 equal-family weighting인가?
- family 정의와 합치기 규칙이 결과 전에 고정되는가?
- one-task/one-condition/one-session이 기본이고 session 반복을 독립 N으로 세지 않는가?
- primary가 family-cluster restricted wild-bootstrap test inversion인가?
- family 20개 미만 confirmatory 금지가 우회되지 않는가?
- exact McNemar/instance discordance가 진단으로만 남는가?
- power가 같은 cluster method, margins, multiplicity와 nuisance grid를 쓰는가?
- instance 수를 늘려 family 부족을 보상하지 않는가?
- power가 ceiling을 넘으면 confirmatory claim을 중단하는가?

통계 방법이 구현 가능하다는 결과는 아직 없으므로 reviewer는 문서 내부의 식별 가능성과 정합성만 판정하고 power 결과를 만들어내지 않는다.

## 7. M-03 transfer/near-copy 재심사

- latent-pattern 계약이 D와 task/oracle 작성 전 동결되는가?
- curator와 task/oracle author가 서로의 최종 자료를 보지 않는가?
- allowlist 밖 연속 8 content token, 일대일 치환, decision skeleton 복제, chronology 위반, non-self-contained task가 자동 실패인가?
- 전이 허용에 6축 중 4축 변화, 새 결정 관계 2개와 직접 재사용 불가 관계 1개가 필요한가?
- 두 독립 auditor가 결과 전에 각각 판정하는가?
- surface/provenance audit과 oracle 의미가 필요한 structural audit의 접근이 구분되는가?
- oracle은 repo/executor-visible 환경 밖 read-only이며 반출되지 않는가?
- 한 명의 FAIL/UNCLEAR, disagreement 또는 누락이 family reject인가?
- adjudicator/analyst가 사후 재량으로 reject를 뒤집을 수 없는가?
- 감사 뒤 문구 수정으로 같은 family를 살리지 않는가?

near-copy threshold의 실제 수치가 authoring 전 별도 동결 대상으로 명시돼 있지 않거나 auditor disagreement 처리에 재량이 남으면 `FAIL/UNCLEAR`다.

## 8. M-04 B 품질 재심사

- B가 D와 token 5%, count ±1, authority tier 일대일 대응, actionability, limitations와 동일 general-guidance 목록을 맞추는가?
- B가 무의미한 filler나 generic advice 제거판이 될 수 없는가?
- D-only 보편 지침을 common wrapper 또는 B parity로 옮기는가?
- 두 independent reviewer가 condition-blind X/Y로 pre-result quality equivalence를 각각 승인하는가?
- 같은 reviewer들이 별도로 B irrelevance와 D relevance를 확인하는가?
- reviewer가 author/executor/redactor/adjudicator/analyst와 분리되는가?
- FAIL/UNCLEAR/disagreement/cue가 package fail인가?
- B approval 없이는 A/B/D gate가 열리지 않는가?

semantic quality가 정량 surface match나 CONTROL 단독 재량으로 대체될 수 있으면 `FAIL`이다.

## 9. M-05 limited safety unblinding 재심사

- primary adjudicator는 condition attribution을 하지 않는가?
- critical 후보가 나오면 새 block release가 먼저 멈추는가?
- 두 blind adjudicator 또는 blind resolver가 critical을 잠근 뒤에만 mapping을 여는가?
- safety monitor만 해당 output ID 하나의 condition label을 보는가?
- 다른 output, aggregate trend, score 또는 미실행 배정은 열지 않는가?
- confirmed critical은 condition과 무관하게 전체 실행을 멈추는가?
- D label은 attribution·격리에만 쓰고 favorable continuation을 고르지 않는가?
- 모든 unblinding access가 기록되는가?
- 중단된 block의 favorable subset을 성공 분석에 넣지 않는가?

condition-aware adjudicator가 immediate D attribution을 하거나 non-D label이면 자동 재개할 수 있으면 `FAIL`이다.

## 10. M-06 redaction과 blinding 재심사

- raw output이 adjudicator에게 직접 가지 않는가?
- mapping·oracle을 모르는 redaction officer와 독립 QC가 사전 정책을 적용하는가?
- condition/package ID, wrapper echo, metadata, formatting cue가 정규화되는가?
- 결정·근거·오류 의미를 숨기는 redaction은 금지되는가?
- primary score가 condition guess보다 먼저 잠기는가?
- guess와 confidence가 mapping 전 잠기는가?
- family-cluster upper bound로 chance `1/K` 대비 `M_blind`를 검사하는가?
- explicit cue, 비대칭·의미 손상 redaction, guess 누락, blinding breach가 confirmatory pass를 막는가?
- `score를 먼저 잠갔다`는 사실만으로 blinding failure를 무시하지 않는가?

blinding check가 단순 보고용이거나 failure가 sensitivity analysis로 보상되면 `FAIL`이다.

## 11. M-07 staffing·cost 재심사

- pilot 13명, confirmatory 14명의 distinct-person minimum이 명시되는가?
- 다른 account/session/agent가 distinct human을 대신하지 않는가?
- curator, task/oracle author, B author, auditors, scheduler, redactor/QC, safety monitor, adjudicators/resolver, analyst, reviewer의 금지 겸임이 명시되는가?
- 사람별 compensation type/rate/cap, active/wait/calendar time, availability, replacement를 authoring 전에 숫자로 승인하는가?
- volunteer와 user time도 0 비용으로 사라지지 않는가?
- 필수 역할 부재·conflict·미승인이 authoring/block release stop인가?
- protocol, authoring, audit, redaction, calibration, executor, judge, analysis, review, orchestration과 model-backed tool의 모든 AI 호출이 장부에 포함되는가?
- subscription·cached·failed·discarded 호출도 usage에서 빠지지 않는가?
- worst-case retry·output·tool·dispute와 human compensation이 cash ceiling에 들어가는가?
- staffing/power/cost가 양립하지 않으면 `DEFER/STOP`인가?

최소 staffing 숫자만 있고 실제 담당자·보상·시간을 authoring 뒤 승인할 수 있으면 `FAIL`이다.

## 12. 조건 지위와 four-condition 판정

reviewer는 각각 별도 verdict를 낸다.

1. **A/D:** total-package feasibility·direction pilot로만 충분한가? effect pass가 완전히 금지됐는가?
2. **B:** content-specific confirmation 전에 필수이며 quality/relevance가 이제 결정 가능한가?
3. **C:** curation diagnostic으로만 선택되며 A/B/D를 보상하지 않는가?
4. **four-condition simultaneous:** 기본 비정당이며 세 질문의 동시 가치, cluster power, staffing와 비용이 모두 사전 승인될 때만 별도 gate인가?

권장 기본 verdict는 `A/D pilot-only`, `B required for confirmation`, `C optional diagnostic`, `four-condition not justified by default`다. 이를 뒤집으면 어떤 estimand·비용·주장을 바꾸는지 명시해야 한다.

## 13. 공통 경계와 비주장

- S0와 E0가 서로 다른 조작을 유지하는가?
- v0.2가 selected representation을 유효한 전통 효과의 사전 결론으로 쓰지 않는가?
- E0가 제안 라벨이고 공식 phase처럼 표현되지 않는가?
- 자료·oracle·prompt·schema·code·모델 실행 gate가 명시적으로 닫혀 있는가?
- 실제 고객·개인·비밀·과거 프로젝트 자료가 금지되는가?
- worktree가 secret boundary로 오표현되지 않는가?
- mechanical pass, pilot, confirmation, optional diagnostic와 multi-model 반복의 주장 상한이 분리되는가?
- 중앙 시스템, Project Brain, 운영 안전·경제성, 실제 프로젝트, 파인튜닝, model-to-model transfer 주장이 금지되는가?

## 14. 비보상 blocking failures

다음 중 하나라도 있으면 전체 PASS는 불가하다.

1. 입력 hash/range 위반 또는 v0.1 silent overwrite
2. fallback의 단일 authenticated reference 우회
3. lower bound가 `Δ`를 넘지 않아도 value pass 가능
4. instance-level 분석이 family cluster primary를 대체
5. family/session 반복을 독립 N으로 부풀림
6. near-copy 감사의 oracle 접근·불일치·chronology 재량
7. B가 surface만 맞거나 independent pre-result quality approval 없음
8. condition-aware adjudicator가 D-attributable stop을 결정
9. raw output cue, redaction 또는 condition-guess failure가 pass를 막지 않음
10. critical·harm·blinding·cost가 효과로 보상됨
11. 최소 staffing·보상·시간·absence가 authoring 전에 고정되지 않음
12. 일부 AI 지원 호출을 cost ledger 밖에 둠
13. A/D pilot을 effect pass로 사용하거나 B 없이 content claim
14. C 또는 four-condition을 자동 필수화해 power·비용을 숨김
15. hidden oracle을 repository/worktree/executor session에 둠
16. 자료·구현·실행 gate를 이 review가 직접 엶
17. 존재하지 않는 결과, 운영 가치, model learning/transfer 주장

## 15. 필수 심사 산출

1. 읽은 파일과 SHA-256, 입력 경계 verdict
2. B-01과 M-01~M-07 각각의 `PASS/FAIL/UNCLEAR`
3. 전체 blocking/major/minor finding
4. A/D, B, C, four-condition separate verdict
5. estimand/null/CI/power alignment verdict
6. family/session clustering verdict
7. transfer/near-copy와 B preapproval verdict
8. redaction/blinding과 limited safety unblinding verdict
9. minimum staffing, compensation/time, absence와 all-AI-call ledger verdict
10. S0/E0 separation과 claim ceiling verdict
11. unresolved feasibility risk
12. 재심사 최소 수정 범위와 다음 최대 input packet
13. 최종 verdict 하나

reviewer는 fixture, oracle, code, prompt, schema, model call, score, simulation result, price lookup 또는 downstream handoff를 만들지 않는다.

## 16. 최종 verdict

### `PASS-FOR-CONTROL-INTEGRATION-ONLY`

- B-01과 M-01~M-07 모두 PASS
- blocking/major 0건
- UNCLEAR는 claim, causality, safety, blinding, staffing, cost와 gate를 바꾸지 않는 minor 표현에만 있음
- 의미: CONTROL이 단일 표현 의존성과 stop-before-authoring feasibility를 검토할 수 있음
- 의미하지 않음: 자료 작성, 구현, 실행, E0 effectiveness 또는 경제성 승인

### `REVISE-AND-REVIEW`

- 고칠 수 있는 blocking/major/관련 UNCLEAR가 하나 이상 있음
- 새 version·hash와 독립 재심사를 요구

### `STOP-DESIGN`

- single-reference, transfer boundary, family-cluster power, B quality, blinding, safety 또는 staffing/cost를 구조적으로 만족할 수 없음
- smallest-worthwhile effect에 필요한 power가 승인 가능한 resource envelope와 양립하지 않음

입력 hash 또는 범위가 틀리면 위 verdict 전에 `INPUT-BOUNDARY-FAIL`로 멈춘다.

## 17. 다음 gate 추천 상한

가장 긍정적인 결과도 다음 문구를 넘지 않는다.

> E0 v0.2 설계는 CONTROL 통합 적합성 검토 후보로 보낼 수 있다.

reviewer는 `selected_representation_ref`를 채우거나 fallback을 승인하고, staffing·예산을 대신 승인하거나, authoring·implementation·pilot gate를 열 수 없다.
