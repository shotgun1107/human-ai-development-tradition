# S0 SM1 후속 7개 형식 독립 비평

> 비평일: 2026-08-06  
> 역할: 허용 입력만 본 read-only 독립 비평자  
> 범위: SM1 최초 후보 7개 JSON Schema와 설계 문서  
> 비범위: 실제 질문·fixture·oracle·scoring instance·변환기·validator·runner·run의 존재 확인 또는 평가

## 1. 입력 무결성과 범위

지정된 10개 본문의 SHA-256과 세 `.sha256` 기록은 모두 일치했다. 허용 목록 밖 파일은 읽거나 검색하지 않았고 파일도 수정하지 않았다.

7개 schema는 모두 JSON으로 파싱됐으며 각 파일만 따로 보면 Draft 2020-12 instance를 만들 수 있었다. 아래 판정은 실제 해시 일치와 7개 형식의 교차 계약까지 함께 고려한 결과다.

## 2. 최종 판정

**중대한 수정 후 재비평**

중심 차단 결함은 두 가지다.

1. question/options가 scoring instance 해시를 요구하고 scoring이 question/options instance 해시를 요구해 실용적으로 만족할 수 없는 순환 해시가 생겼다.
2. 두 봉인 block에서 같은 표현 treatment가 반복됐음을 고정하는 불투명 profile 결합이 없어 H1-D의 two-block 반복 우위를 같은 조건의 반복으로 해석할 수 없다.

따라서 최초 후보는 SM1 동결이나 I0·F0 개방에 사용할 수 없다.

## 3. 파일별 판정

| 파일 | 판정 | 핵심 이유 |
|---|---|---|
| `question-options.schema.json` | 실패 | scoring과 순환 해시, runner 제외 필드명 불일치 |
| `transformation-manifest.schema.json` | 부분 | block 내부 provenance는 있으나 block 간 동일 treatment profile 연결 부재 |
| `neutral-answer-validation.schema.json` | 부분 | question projection hash 결합 부족, M6 검사 필드 범위 불명확 |
| `access-manifest.schema.json` | 부분 | 역할별 필수 금지·artifact 종류·authoring/implementation/transformation 공개 단계 부족 |
| `run-manifest.schema.json` | 실패 | 같은 overlay가 두 block의 같은 treatment인지 고정하지 못하며 retry attempt의 이전 실패 연결 부족 |
| `scoring.schema.json` | 실패 | 순환 해시, 13 code coverage·decision function 사전 검토 계약 부족 |
| `pre-review-record.schema.json` | 부분 | approve/reject 논리는 맞지만 핵심 교차 check와 실행 전 동결 const 부족 |
| `sm1-seven-format-design.md` | 부분 | 분업·게이트 방향은 좋으나 위 결함을 완결된 계약처럼 취급 |

## 4. 차단 발견

### SM1-B01. question/options와 scoring의 순환 SHA-256

question/options의 질문이 scoring instance hash를 요구하고 scoring이 question/options instance hash를 요구한다. 실제 최종 파일 해시까지 검증하려면 암호학적 고정점을 찾아야 하므로 실용적인 instance 묶음을 만들 수 없다.

최소 수정:

- question/options에서 scoring instance hash를 제거한다.
- 안정적 불투명 scoring contract ID만 남긴다.
- 실제 파일 hash는 scoring→question/options의 한 방향으로만 둔다.
- runner 제외 필드명도 실제 필드명과 일치시킨다.

### SM1-B02. 두 block의 동일 treatment 반복이 고정되지 않음

transformation output과 run pairing에는 두 block에서 동일한 표현 구조임을 나타내는 안정적 불투명 profile ID가 없다. 따라서 같은 overlay가 block-1에서 한 구조, block-2에서 다른 구조와 연결돼도 배제하지 못한다.

최소 수정:

- package마다 불투명 `treatment_profile_id`와 profile hash를 둔다.
- 네 profile이 각 block에 정확히 한 번 등장하게 한다.
- 같은 overlay는 두 block에서 같은 profile과만 결합한다.
- pre-review에 cross-block treatment binding check를 추가한다.

## 5. 중대 발견

### SM1-M01. validation report와 질문 기준선 결합 부족

validation report가 실제 사용한 `question_projection_sha256`과 `answer_schema_sha256`을 기록하지 않아 exact question·option 검사의 기준 파일을 재구성할 수 없다.

### SM1-M02. M6 검사 범위 불명확

프로토콜 M6은 `short_reason`의 금지 정보 노출이다. 일반 forbidden disclosure로 두면 decision·cited/affected ID의 권한 오류를 M6로 잘못 분류해 C1과 충돌할 수 있다.

### SM1-M03. retry attempt의 이전 실패·공개 상태 결합 부족

attempt 1은 이전 suite ID·실패 로그·실패 단계·봉인 input 공개 여부·새 block 필요 여부를 필수로 가져야 한다. 공개 뒤 실패라면 새 두 block hash가 이전과 달라야 한다.

### SM1-M04. access artifact 종류와 release 단계 부족

condition package, role/release policy, transformation, implementation artifact, run manifest·record 등 artifact 종류와 fixture authoring·implementation·transformation 공개 단계를 구별해야 한다. 모든 role/release policy 원문 묶음도 pre-review 입력에 포함해야 한다.

### SM1-M05. 13 code coverage와 decision function 검증 부족

criteria `minItems: 13`은 C1–C7·M1–M6이 각각 한 번 이상 존재함을 보장하지 않는다. criterion ID·question-event key·primary code의 필드별 고유성과 13개 code coverage를 외부 검사·pre-review check로 고정해야 한다. §9 decision function artifact도 pre-review 입력에 포함해야 한다.

### SM1-M06. pre-review 승인 check 부족

다음을 승인 필수 check로 추가해야 한다.

- cross-block treatment binding
- validation report↔question projection 결합
- retry eligibility
- 13 code coverage
- decision function↔protocol §9 일치
- role/release policy bundle 완전성
- run-record contract 준비
- executor 생성 전 승인 기록 동결

각 check의 근거 report hash도 필요하다.

## 6. 경미 발견

### SM1-N01. runner 제외 필드명 불일치

runner projection의 `scoring_ref`와 실제 sealed 필드 `scoring_ref_sha256`이 다르다. B01 수정과 함께 안정적 contract ID 명칭으로 통일한다.

### SM1-N02. date-time 보장 표현

pattern은 RFC 3339 외형을 제한하지만 실제 달력 의미까지 단독 보증하지 않는다. 동결 validator가 format assertion을 활성화하고, 문서 표현은 `RFC 3339 모양+format assertion`으로 한정해야 한다.

## 7. 게이트

문서상 구현·출제·실행 게이트는 닫혀 있다. 실제 코드·fixture·oracle·run이 생성됐다는 증거는 보지 않았다. 위 결함을 수정한 새 해시와 제한 재비평 전에는 SM1을 동결하거나 I0·F0를 열어서는 안 된다.
