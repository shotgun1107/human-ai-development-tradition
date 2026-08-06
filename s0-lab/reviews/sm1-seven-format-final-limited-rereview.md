# S0 SM1 후속 7개 형식 최종 제한 재비평

> 재비평일: 2026-08-06  
> 역할: 최초 비평을 수행한 read-only 독립 비평자  
> 범위: `SM1-B01–B02`, `SM1-M01–M06`, `SM1-N01–N02` 수정 여부  
> 비범위: 실제 instance·구현·fixture·oracle·scoring·격리·run의 존재 확인 또는 평가

## 1. 입력 무결성

지정된 9개 본문의 계산 SHA-256과 두 `.sha256` 기록은 모두 일치했다. 허용 목록 밖 파일은 읽거나 검색하지 않았고 파일도 수정하지 않았다. 7개 schema는 모두 유효한 JSON 문법으로 파싱됐다.

## 2. 최종 판정

**현재 SM1 동결 가능**

최초 비평의 10개 항목은 모두 충분히 반영됐다. 7개 schema는 개별적으로 정적 만족 가능하며, 순환 해시·cross-block treatment·validation 기준·retry 근거·access policy·13-code coverage·decision function·20개 승인 check가 사전 검토 계약에 연결됐다.

이 판정은 현재 해시의 SM1 **형식 설계**에만 적용된다. 실제 instance·구현·fixture·oracle·scoring·격리·run이 통과했다는 뜻은 아니다.

## 3. 항목별 판정

| 항목 | 판정 | 근거 |
|---|---|---|
| SM1-B01 순환 SHA-256 | 충분 반영 | question/options는 불투명 scoring contract ID만 갖고 scoring만 question/options 최종 해시를 단방향 참조 |
| SM1-B02 cross-block treatment | 충분 반영 | package에 profile ID·hash를 추가하고 run·pre-review가 두 block의 같은 overlay↔profile 결합을 검사 |
| SM1-M01 validation 기준 결합 | 충분 반영 | report가 question projection과 answer schema 해시를 포함 |
| SM1-M02 M6 범위 | 충분 반영 | 금지 노출 검사를 `short_reason` 하나에만 적용 |
| SM1-M03 retry 결합 | 충분 반영 | attempt 1이 이전 suite·record·실패 단계·공개 상태·과거/현재 block hash를 요구 |
| SM1-M04 access 정책 | 충분 반영 | artifact 종류·release 단계·role/release policy bundle과 pre-review 입력 연결 |
| SM1-M05 scoring 완결성 | 충분 반영 | 13 code coverage·event key 고유성·judge projection·decision function path/hash 추가 |
| SM1-M06 pre-review 완결성 | 충분 반영 | 20개 check·evidence hash·실행 전 freeze·embedded run-record 계약 |
| SM1-N01 제외 필드명 | 충분 반영 | `scoring_contract_id`로 통일 |
| SM1-N02 date-time 표현 | 충분 반영 | format assertion 활성화와 `RFC 3339 모양` 수준으로 설명 제한 |

## 4. 핵심 재확인

### 4.1 순환 해시 제거

question/options는 scoring의 최종 SHA-256을 보유하지 않는다. 두 파일은 안정적 `scoring_contract_id`로 연결되고, scoring instance만 question/options 최종 SHA-256을 참조한다. 따라서 최종 파일들이 서로의 해시를 요구하는 고정점 문제가 없다.

### 4.2 두 block의 동일 treatment

transformation package와 run item은 `treatment_profile_id`·`treatment_profile_sha256`을 가진다. 각 block은 profile 4개를 한 번씩 사용하고 같은 overlay는 두 block에서 같은 profile과만 결합한다. pre-review의 `cross_block_treatment_binding_valid`가 이를 승인 전에 확인한다.

### 4.3 validation과 M6

validation report는 policy·input·answer 외에 실제 question projection과 answer schema 해시를 기록한다. 금지 노출 검사는 `short_reason`만 대상으로 하므로 decision·cited/affected IDs의 권한 오류를 M6로 낮춰 C 우선 규칙을 우회할 수 없다.

### 4.4 retry와 run record

attempt 1은 이전 suite·run-record bundle·실패 단계·봉인 input 공개 여부·새 block 필요 여부·이전/현재 block hash를 요구한다. 정상 run record는 answer hash·byte를, 기술 실패 record는 실패 이유·로그 hash를 요구한다. 실제 task ID는 봉인 input 공개 전에 사전 session slot에 결합한다.

### 4.5 access와 scoring blind

access 형식은 역할·release policy 원문 묶음과 artifact 종류·공개 단계를 기록한다. 사후 판정자는 scoring의 criteria·counting policy projection만 받고 selection contract·조건 identity·비용을 정확성 동결 전에는 보지 않는다.

### 4.6 scoring과 pre-review

scoring은 C1–C7·M1–M6 모두의 존재, criterion/event key 고유성, C/M severity, C 우선·이중 계수 금지를 요구한다. §9 decision function artifact는 pre-review 입력에 포함된다.

pre-review는 기존 의미 검사와 새 교차 검사를 합친 20개 check를 모두 true로 해야 approve할 수 있다. reject는 최소 하나가 false여야 한다. evidence report와 review report를 해시하며 executor 세션 생성 전에 기록을 동결한다.

## 5. 파일별 최종 상태

| 파일 | 최종 상태 |
|---|---|
| `question-options.schema.json` | 충분 |
| `transformation-manifest.schema.json` | 충분 |
| `neutral-answer-validation.schema.json` | 충분 |
| `access-manifest.schema.json` | 충분 |
| `run-manifest.schema.json` | 충분 |
| `scoring.schema.json` | 충분 |
| `pre-review-record.schema.json` | 충분 |
| `sm1-seven-format-design.md` | 충분 |

## 6. 게이트

SM1 형식은 동결할 수 있지만 실제 role/release policy, validation report, run record, task binding record, 질문·fixture·oracle·scoring, 변환기·validator·runner, 실행 세션·답안은 이번 판정 범위 밖이다.

프로젝트의 보호 규칙에 따라 I0 구현과 F0 출제는 정확한 게이트가 별도로 열리기 전에는 시작할 수 없다.
