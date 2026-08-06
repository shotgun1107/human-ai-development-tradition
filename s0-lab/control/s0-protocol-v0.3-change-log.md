# S0 프로토콜 v0.3 제한 수정 장부

> 기준 프로토콜: `s0-lab/control/s0-protocol-v0.2.md`  
> 기준 SHA-256: `748d6cb4c07cae2982a2220cd2f0c798b5ba8b0bc40082c6296fe6a9c2a7ef5a`  
> 대상 재비평: `s0-lab/reviews/s0-protocol-v0.2-limited-rereview.md`  
> 재비평 SHA-256: `8edfbc2b3c0c06729724f808a2674e8300e56f7733806cc8d8fa4346ca030184`

## 1. v0.1 지적의 현재 상태

| 비평 ID | v0.2 재비평 판정 | v0.3 상태 |
|---|---|---|
| P1-01 조건 차이 관찰 불가 | 충분 반영 | 유지 |
| P1-02 공통 JSON의 D 편향 | 충분 반영 | 유지·실제 schema 검토 대기 |
| P1-03 자원·출력 기회 미동결 | 부분 반영 | 제한 수정 반영·재비평 대기 |
| P1-04 H0·결정표 불완전 | 부분 반영 | 제한 수정 반영·재비평 대기 |
| P1-05 oracle 사전 검토 부재 | 충분 반영 | 유지·fresh/non-fork와 허용 입력 명시 강화 |
| P1-06 재시험 재량 | 부분 반영 | 제한 수정 반영·재비평 대기 |

## 2. 제한 수정 10건 반영

| 번호 | 재비평 요구 | v0.3 반영 |
|---|---|---|
| L01 | 변환기의 oracle 접근 금지와 관계 근거 추적 | 변환기 허용 입력을 canonical input·공개 변환 스키마로 한정. C 표지·D 관계에 `supporting_fact_id` 의무화. 원문에 명시되지 않은 평가 관계 추론 금지 |
| L02 | byte 15%와 padding | 15%를 무효 상한으로 한정. whitespace·빈 필드·무의미 문장 padding 금지. token 계측 가능 여부와 fact·record·질문·관계 수 병행 기록 |
| L03 | 두 block 우위 기준 통일 | D가 모든 eligible 단순 조건보다 두 block 각각에서 엄격히 나을 때만 D 유지 후보로 정의 |
| L04 | 결정표를 total function으로 작성 | `best_simple`과 네 비교 관계를 정의하고, 위에서 아래로 정확히 한 끝 상태를 반환하도록 재작성 |
| L05 | C/M 교차 계수와 valid–M5 경계 | 질문별 primary 오류 코드, C 우선, 독립 원인만 별도 계수. `run-valid`와 parse 가능한 schema 오류 M5를 분리 |
| L06 | oracle 결함과 재시도 종료 | 기술 재시도 재실패 시 새 사용자 게이트 요구. 실행 뒤 primary oracle 결함은 현 게이트 종료·전체 무효·새 사전검토와 사용자 재승인 요구 |
| L07 | 검토자·판정자 세션과 입력 분리 | F0·I0·실행 세션에서 fork하지 않은 fresh 세션, 역할별 허용·금지 입력·공개 시각·해시 기록 명시 |
| L08 | runner-facing 명칭 누출 | 모든 입력 경로를 `input.json` 형태의 불투명 경로로 통일. 조건 문자·복잡도·lineage 같은 목표 명칭을 파일명·필드명·short reason에서 금지 |
| L09 | 공개 묶음과 봉인 변환 순서 | 공개 연습 묶음 동결 뒤 I0 점검. 봉인 canonical과 oracle/scoring 분리 후 CONTROL이 oracle 없는 환경에서 변환 실행·즉시 해시 |
| L10 | 변경 장부 상태 정정 | P1-03·P1-04·P1-06을 `부분 반영—제한 수정 반영·재비평 대기`로 기록 |

## 3. 바뀌지 않은 경계

- v0.3은 구현, 공개·봉인 fixture 작성, oracle 작성, 변환기 실행, S0 실행을 허가하지 않는다.
- v0.3 제한 재비평이 통과할 때 열 수 있는 최대 범위는 `answer.schema.json`과 manifest의 설계·비평이다.
- 실제 자료, Project Brain 연결, 운영 효과, 경제성, 모델 전이는 여전히 S0 범위 밖이다.
