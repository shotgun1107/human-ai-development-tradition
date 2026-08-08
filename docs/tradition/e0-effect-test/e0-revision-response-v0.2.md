# E0 효과시험 v0.2 수정 응답과 문서 지도

- 상태: `수정 제안 — 새 독립 심사 대기, 설계 전용`
- 기준선: `central-system-v2.1-s0-preparation`
- 대상: CONTROL이 제공한 E0 v0.1 독립 심사 `REVISE-AND-REVIEW`
- 효력: v0.2 심사 packet의 entry point. v0.1을 대체하거나 통과시키지 않는다.
- 현재 gate: 설계 v0.2 revision만 열렸으며 authoring·구현·실행 gate는 닫혀 있다.

## 1. 확인된 입력과 경계

이 수정 작업은 detached commit `84014378b48466c185e13cadd6b9a07549ffbaee`에서 수행했다. 허용된 same-basename sidecar가 있는 입력은 다음 hash와 일치했다.

| 입력 | 검증한 SHA-256 |
|---|---|
| `s0-e0-boundary-and-parallel-work.md` | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` |
| `central-system-v2-common-baseline.md` | `f40bd01f2957d508f55fbfc683503afbe649dfb080608d03fff2f45902f09667` |
| `e0-effect-test/README.md` | `22d2297b429ebe1ee8d62526c573ed836df5a0a8cffb9bf274fe760b4e68fd29` |
| `e0-effect-test-design-v0.1.md` | `96de9cc3bdb695e32f98daa5b1d81585669a7c42c7bc90fc98efbcbf65f60986` |
| `e0-measurement-and-analysis-plan-v0.1.md` | `bc0baf919863de6901026cc7ba6a756f00ce04c1e5ad67ae365e283f17d6545f` |
| `e0-operating-cost-and-gates-v0.1.md` | `5a847ce5c95e970c1163cbfa19bc903312bfa104ad01c5b88b0c8481b4753ab8` |
| `e0-independent-review-brief-v0.1.md` | `6bada32d807dd066ece8f971a1adc8d4039c945567e7ee345bc4be8114bd1ffa` |

`AGENTS.md`, `purpose-and-philosophy.md`, `roadmap-and-evaluation.md`도 허용 입력으로 읽었다. 그 밖의 repository history, `s0-lab/**`, sealed/private/oracle 자료, 다른 proposal/review, web과 실제 프로젝트 자료는 사용하지 않았다.

## 2. v0.1 심사 결과의 보존

CONTROL이 제공한 동결 review text의 요지는 다음과 같다.

- 전체 verdict: `REVISE-AND-REVIEW`
- blocking: fallback이 authenticated `selected_representation_ref`를 우회할 수 있음
- major: value threshold 불일치, family/session clustering 미고정, near-copy 경계의 재현성 부족, B의 실질 품질 미보장, D-attributable stop과 blind adjudication 충돌, raw-output condition cue, staffing·cost 불완전
- 조건 verdict: A/D pilot-only, B required-but-underdetermined, C optional diagnostic, four-condition simultaneous not justified by default
- primary/adjudication, statistics, cost/gates: fail

v0.1의 최대 허용 주장은 그대로다.

> E0 v0.1은 제한된 외부 문서 전달 효과를 반증 가능하게 시험하기 위한 설계 제안이며, 독립 심사는 수정과 재심사가 필요하다고 판정했다.

v0.2는 그 review를 통과했다고 선언하지 않는다. 새 independent reviewer가 이 판본을 다시 판정해야 한다.

## 3. v0.2 문서 지도

| 문서 | 역할 |
|---|---|
| `e0-effect-test-design-v0.2.md` | 조건 지위, 단일 표현 참조, transfer/B audit, safety unblinding, redaction·blinding, role boundary |
| `e0-measurement-and-analysis-plan-v0.2.md` | family-weighted estimand, `Δ` null·CI·power 정렬, cluster-aware confirmatory method, adjudication·condition-guess 분석 |
| `e0-operating-cost-and-gates-v0.2.md` | 13/14명 최소 staffing, 보상·시간·absence stop, 모든 AI 지원 호출, gate·rollback |
| `e0-independent-review-brief-v0.2.md` | 새 read-only 심사의 input packet, blocking rubric와 최종 verdict |
| `e0-revision-response-v0.2.md` | 입력, finding별 수정 추적, status와 미해결 위험 |

각 Markdown에는 같은 basename의 `.sha256` sidecar가 따라야 한다. v0.1 파일과 기존 `README.md`는 수정하지 않는다.

## 4. finding별 수정 추적

아래 `설계상 폐쇄`는 author가 의도한 수정 위치를 뜻할 뿐 reviewer의 PASS를 뜻하지 않는다.

### B-01 — fallback 우회

- 수정: protocol 판본마다 활성 `selected_representation_ref`는 정확히 하나만 허용한다.
- fallback 처리: 단순 공개 fallback도 먼저 독립 검토된 versioned·hashed artifact가 되고 그 유일 참조로 인증돼야 한다.
- stop: 공백, 복수 후보, inline 대체, hash·known limitation 누락은 authoring 전 중단이다.
- 변경 효과: 참조가 바뀌면 기존 authored material과 감사는 효력을 잃고 새 판본이 필요하다.
- 근거: design 3절, operating V2-G1.

### M-01 — estimand, null, CI, power와 smallest-worthwhile effect

- 수정: 효과 null을 `δ ≤ Δ`로 고정하고 pass를 one-sided cluster-aware lower bound `> Δ`로 고정했다.
- `lower > 0`과 `point ≥ Δ`의 분리 규칙을 제거했다.
- power 대립값 `δ_plan > Δ`를 명시하고 동일 estimand·margin·family unit·multiplicity에서 공동 power를 계산하게 했다.
- 근거: measurement 4·5절.

### M-02 — family/session clustering

- 수정: family 동일 가중 estimand를 primary로 두고 task family 전체를 resampling cluster로 하는 restricted wild cluster bootstrap-t를 고정했다.
- confirmatory 기본은 one-task/one-condition/one-session, 반복은 instance 안에서 먼저 집계, family 20개 미만은 confirmatory 금지다.
- exact McNemar는 진단으로 강등했다.
- power도 동일 cluster method와 nuisance grid를 사용한다.
- 근거: design 2.3, measurement 2·5절.

### M-03 — transfer와 near-copy 재현성

- 수정: latent-pattern 선동결, curator와 task/oracle author의 양방향 차단, 8-token overlap·일대일 decision skeleton 자동 실패와 6축 중 4축 변화의 공동 허용 규칙을 고정했다.
- 두 독립 auditor가 surface/provenance와 structural/oracle audit을 분리한다.
- oracle은 repo 밖 read-only 환경에서 필요한 의미만 보며 반출하지 않는다.
- 한 명의 FAIL/UNCLEAR/불일치도 family reject이고 사후 adjudicator 재량은 없다.
- 근거: design 4절.

### M-04 — B의 의미 품질·권위·구체성

- 수정: token 5%, count ±1, authority tier의 일대일 대응과 general-guidance 동일 목록을 포함해 authority, actionability, specificity, limitations parity를 binary rule로 고정했다.
- 두 independent reviewer가 X/Y blind 상태에서 pre-result quality equivalence와 relevance를 모두 승인한다.
- reviewer 불일치, 표면 cue 또는 B의 실질적 공백은 package fail이다.
- 근거: design 5절, operating Stage 5와 V2-G4/G6.

### M-05 — D-attributable stop과 condition blindness

- 수정: adjudicator는 D attribution을 하지 않는다. blind critical 판정이 잠긴 뒤 별도 safety monitor만 해당 output ID의 condition label 하나를 연다.
- confirmed critical은 condition과 무관하게 전체 실행을 중단한다. D label은 귀속·격리에만 쓰며 favorable continuation을 고르지 않는다.
- block clearance 전 다음 block을 release하지 않는다.
- 근거: design 6절, measurement 8절, operating 8절.

### M-06 — raw output cue와 blinding 확인

- 수정: raw output은 독립 redaction officer와 QC가 사전 정책으로 판정용 사본을 만든다.
- adjudicator는 primary score를 먼저 잠근 뒤 condition guess와 확신을 기록한다.
- family-cluster upper bound로 chance 대비 `M_blind` 비열등을 요구한다.
- explicit cue, 비대칭·의미 손상 redaction 또는 blinding breach는 confirmatory pass를 막고 `inconclusive`로 닫는다.
- 근거: design 7절, measurement 7절.

### M-07 — staffing, compensation, absence와 AI 지원 비용

- 수정: A/D pilot은 최소 13명, A/B/D confirmatory는 최소 14명의 distinct people과 금지 겸임을 제안했다.
- 사람별 compensation 방식·rate·최대 지급, 능동·대기·calendar 시간, 가용성·replacement를 authoring 전에 숫자로 승인한다.
- 결원·conflict·미승인은 authoring 또는 block release stop이다.
- protocol·authoring·audit·redaction·judge·analysis·review·model-backed tool을 포함한 모든 AI 지원 호출을 장부에 넣는다.
- 근거: operating 3~6절.

## 5. 조건별 판정의 보존

v0.2가 새 review에 요청하는 기본 판정은 다음과 같다.

| 조건 질문 | v0.2 제안 |
|---|---|
| A/D | 가장 작은 total-package pilot, effect pass 불가 |
| B | content-specific confirmation 전에 필수; quality/relevance 이중 승인 필요 |
| C | curation value가 실제 의사결정일 때만 optional diagnostic |
| four-condition simultaneous | 기본 비정당; 세 질문의 동시 가치·power·비용이 모두 사전 승인될 때만 별도 검토 |

A/D가 좋아 보여도 B를 생략해 content-specific claim을 만들 수 없다. C 결과는 A/B/D 실패를 보상하지 않는다.

## 6. 새 독립 심사가 확인해야 할 기계적 질문

1. fallback이 어떤 문구로도 단일 authenticated reference를 우회할 수 없는가?
2. `Δ`가 estimand, null, lower bound, power와 보고 문구에서 같은 의미인가?
3. family cluster가 primary와 power에서 실제 독립 단위인가? session 재사용 경로가 닫혔는가?
4. near-copy 판정의 oracle 접근, 두 auditor 불일치와 authoring chronology가 재현 가능한가?
5. B가 독립 결과 전 승인 없이는 confirmatory input이 될 수 없는가?
6. critical 후보, score lock, safety unblinding, block stop의 순서가 condition-aware adjudication을 만들지 않는가?
7. raw cue redaction과 condition-guess 실패가 pass를 막는가?
8. 최소 staffing, compensation/time, absence와 모든 AI 지원 call이 stop-before-authoring 계산에 들어가는가?
9. A/D pilot, B confirmation, optional C와 four-condition 비기본이 문서 전체에서 일관적인가?
10. 어느 경로도 S0/E0 material authoring·구현·실행 gate를 열지 않는가?

## 7. 현재 미해결 위험

설계 문구로 제거할 수 없는 다음 위험은 미래 gate에서 실패할 수 있다.

- 13명 또는 14명의 독립 인력과 보상을 현실적으로 구할 수 있는지 알 수 없다.
- family-clustered smallest-worthwhile effect에 필요한 family 수가 비용 상한과 양립할지 알 수 없다.
- D와 의미 품질이 같으면서 모든 latent pattern에 무관한 B를 만들 수 있는지 알 수 없다.
- transfer와 near-copy 경계가 실제 합성 자료에서 auditor 일치를 낼지 알 수 없다.
- 의미를 보존한 redaction 뒤 condition guess가 chance margin을 통과할지 알 수 없다.
- 단일 representation artifact가 S0 또는 fallback 절차에서 승인될지 알 수 없다.

이 위험은 `미확인`이며 통과나 구현 사실이 아니다. 하나라도 필요한 gate에서 닫히지 않으면 E0를 보류·축소하거나 중단한다.

## 8. bounded status

현재 허용 가능한 상태 문구는 다음뿐이다.

> E0 v0.2는 v0.1 독립 심사의 B-01과 M-01~M-07을 설계 수준에서 기계적으로 다루려는 새 revision proposal이며, 새 독립 read-only review를 기다린다.

현재 주장할 수 없는 것은 S0 또는 E0 통과, 자료·oracle·runner 완성, 모델 실행·채점, 중앙 시스템·Project Brain 유효성, 운영 안전성·경제성, 실제 프로젝트 효과와 모델 간 전승이다.
