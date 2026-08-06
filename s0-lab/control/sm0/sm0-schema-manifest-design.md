# S0 SM0 schema·manifest 설계 후보

> 판본: `sm0-0.2-limited-fix-candidate`  
> 기준 프로토콜: `s0-protocol-v0.3.md`  
> 기준 프로토콜 SHA-256: `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c`  
> 상태: **독립 비평 전 설계 후보 — 구현·출제·실행 금지**

## 1. 이번 단계의 목적

SM0는 네 가지 입력 방식이 실제 시험에서 같은 답안 형식·권한·시간·출력 기회를 받도록 **빈 양식과 검사 규칙**을 정하는 단계다. 실제 질문, 합성 사건, 숨은 정답, 채점 내용, 변환 코드, 실행 프롬프트는 만들지 않는다.

## 2. 산출물 지도

| 파일 | 역할 | 실행 데이터 포함 여부 |
|---|---|---|
| `answer.schema.json` | 모든 실행자가 작성할 중립 답안의 기본 모양 | 없음 |
| `common-manifest.schema.json` | 모델·권한·시간·출력·세션·실행 수의 공통 고정 양식 | 없음 |
| `condition-overlay-manifest.schema.json` | 불투명 조건 입력과 실행자 지시 파일의 통제용 등록 양식 | 없음 |
| `fixture-manifest.schema.json` | 봉인 block의 해시·개수·동등성·접근 경계를 기록하는 양식 | 없음 |

네 JSON은 실제 manifest가 아니라 이후 파일이 따라야 할 **형식 설계**다.

## 3. 답안 설계

실행자는 구조 이름이나 채점 코드를 쓰지 않고 다음만 답한다.

- 어떤 질문인지: `question_id`
- 선택한 결과: `decision_option_id`
- 직접 사용한 기록: `cited_record_ids`
- 영향을 받는 기록: `affected_record_ids`
- 불확실성 정도: `none|bounded|material`
- 500자 이하 한 줄 설명: `short_reason`

`decision_option_id`는 `allow`, `retire` 같은 의미를 전역으로 미리 주지 않는다. block별 질문 목록이 중립 `OPT-*` ID와 의미를 정의하고, 모든 조건에 똑같이 제공한다.

JSON Schema만으로는 질문 ID 정렬, 질문당 정확히 한 답, 질문별 허용 option, ID 배열 정렬, 금지 명칭의 의미 검사를 완전히 할 수 없다. 따라서 다음은 후속 중립 검증기가 별도로 검사하도록 manifest에 고정한다.

1. 답안의 질문 ID 집합이 동결 질문 목록과 정확히 같은가
2. 질문 ID와 record ID 배열이 오름차순이고 중복이 없는가
3. `decision_option_id`가 해당 질문에 허용된 값인가
4. `affected_record_ids`가 필요 없는 질문에서 빈 배열인가
5. `short_reason`에 조건 문자, 경로, 고유 필드명, 관계 코드, 목표 구조 명칭이 없는가

이 검증기는 아직 구현하지 않는다.

## 4. 공통 manifest 설계

공통 manifest는 8개 실행 전체에 같은 자원을 고정한다.

- 정확한 모델 ID·표시명·사고 수준
- 모델 전체 configuration 해시와 제공자 내부 판본 보장 여부·미보장 사유
- 실행마다 fresh/non-fork 세션
- 1 turn, 15분, 답안 8,192 bytes, 답안 파일 1개
- 하위 에이전트·인터넷·MCP·브라우저·외부 전송 금지
- 사람 내용 개입 0회
- 4조건×2block=8실행, 동시 실행 최대 3
- 동일 조건의 두 block을 같은 wave에 배치하지 않음
- 기술 재시도는 전체 suite 최대 1회
- 프로토콜·답안 schema·공통 지시·overlay·fixture·질문 목록의 해시
- validation policy와 validation report schema의 해시
- 아직 동결되지 않은 question/options·transformation·answer-validation·access·run·scoring·pre-review-record 형식의 해시

로컬 capability profile도 모든 실행에서 똑같이 고정한다.

- 읽기: 자신의 instruction, 자신의 input, answer schema, 자신의 question/options만 허용
- 저장소 검색과 allowlist 밖 파일 읽기 금지
- 쓰기: answer output 하나만 허용
- shell 금지
- 로컬 도구: 위 허용 파일 읽기와 answer 쓰기 기능만 허용
- 작업 디렉터리: 비어 있는 fresh 디렉터리에 읽기 전용 입력만 연결

실제 모델 ID나 실제 지시문은 아직 넣지 않는다. 이 schema는 이후 manifest 인스턴스가 빈값이나 모호한 `latest` 대신 정확한 값을 요구하도록 한다.

## 5. 조건 overlay manifest 설계

overlay manifest는 CONTROL과 사전 검토자만 보는 통제 문서다. 실행자는 manifest 자체가 아니라 다음 두 파일만 받는다.

1. `runner/<불투명 ID>/instruction.txt`
2. run manifest가 block과 조합한 `packages/<불투명 ID>/input.json`

manifest에는 A–D 문자나 `chronological`, `common`, `lineage` 같은 구조 이름을 넣지 않는다. 다음 비노출 확인을 모두 `true`로 요구하지만, boolean 자체만 믿지 않고 사전 검토자가 실제 파일을 읽어 확인해야 한다.

- 조건명·복잡도 순위 없음
- H0/H1·목표 후보 없음
- 답안 예시·오류 코드·추천 판단 없음
- 의미가 드러나는 경로 없음
- 모든 조건에 같은 질문 기회

조건과 A–D의 실제 대응표는 이 manifest 밖의 CONTROL 전용 영역에 둔다.

## 6. fixture manifest 설계

fixture manifest는 합성 block 내용 대신 해시와 개수만 기록한다.

- 합성 자료만 사용하고 실제 프로젝트·개인정보·비밀이 없다는 경계
- canonical input, fact 목록, 질문 목록, oracle, scoring의 해시
- 변환기가 canonical과 공개 변환 schema만 읽고 oracle·scoring을 읽지 않았다는 기록
- 프로토콜 v0.3이 정한 사건 구성 수량
- C1–C7·M1–M6별 질문 기회 수
- 네 불투명 입력 package의 fact·record·질문·관계·byte·가능한 token 수
- 모든 fact 집합·record ID·본문 해시·질문 기회가 같다는 검사 결과
- 가장 작은 입력 대비 byte 차이가 15% 이하이고 padding이 없다는 결과
- 구조 표지마다 `supporting_fact_id`가 있고 oracle에서 새 관계를 가져오지 않았다는 결과
- 실행 전에 동결됐다는 시각
- package별 구조 표지 수·근거 연결 수·근거 없는 표지 수 `0`·provenance mapping 해시
- 전체 provenance report와 oracle-derived 관계 검사 report 해시·발견 수 `0`
- C1–C7·M1–M6 각각 최소 한 번의 관찰 기회

`oracle_sha256`과 `scoring_sha256`은 내용이 아니라 봉인 파일을 가리키는 해시 자리뿐이다. 이 단계에서는 해당 파일을 만들지 않는다.

사전 검토 승인과 보고서 해시를 fixture manifest 안에 넣으면, 검토 전 manifest가 승인을 요구하는 순환이 생긴다. 따라서 fixture manifest를 먼저 동결하고, 별도 사전 검토 기록이 그 manifest 해시와 승인 결과를 묶는다.

## 7. 검증을 세 층으로 분리

### 7.1 JSON 형식 검사

- 네 JSON이 JSON Schema Draft 2020-12 문법의 유효한 JSON인지 확인
- 필수 필드, 자료형, 고정 상한, 불투명 ID, SHA-256 모양 검사

### 7.2 교차 파일 검사

후속 중립 검증기가 다음을 계산한다.

- 실제 파일 해시와 manifest 해시 일치
- 답안 질문·option·정렬 규칙
- 네 package의 fact·record·본문 해시·질문 기회 동일
- byte 최대 차이, padding 금지, 가능한 경우 token 계측
- package ID·runner path·input hash의 필드별 고유성
- 구조 표지 수와 supporting fact 연결 수·mapping의 일치
- 네 overlay의 지시 길이 차이 최대 15%
- 공통 모델·권한·상한이 8개 run에 동일
- fresh/non-fork 세션·접근 시각·재시도 기록

검사 규칙은 결과 전에 `validation_policy_sha256`으로 고정한다. 실제 manifest를 동결할 때는 별도 freeze record가 manifest 해시, validation policy 해시, 교차 검사 report 해시를 함께 묶는다. JSON Schema 통과만으로 `대칭 확인`이나 `동결 완료`라고 부르지 않는다.

이 검증 로직은 후속 형식 관문과 I0 대상이며 현재 만들지 않는다.

### 7.3 사람·독립 AI 검토

기계 검사는 `supporting_fact_id`가 존재하는지는 알 수 있지만 그 관계가 원문에 실제 명시됐는지는 스스로 보증하지 못한다. 사전 봉인 검토자는 다음 의미 검사를 맡는다.

- D에만 정답에 가까운 새 관계가 추가되지 않았는가
- overlay 문구가 한 조건에만 유리한 힌트를 주지 않는가
- oracle과 scoring이 서로 모순되지 않는가
- primary 오류 코드와 C 우선 규칙이 한 사건을 중복 계산하지 않는가

## 8. 의도적으로 만들지 않은 것

- 실제 common manifest와 overlay manifest
- 실제 모델 선택과 실행 프롬프트
- 공개·봉인 합성 사건
- 질문·option 실제 내용
- oracle·scoring 내용
- 변환기·검증기·runner 코드
- A–D 실행 세션과 결과

따라서 이 설계가 통과해도 S0가 구현되거나 검증된 것은 아니다.

## 9. 반드시 먼저 거칠 후속 형식 관문

SM0 네 schema가 동결돼도 I0·F0를 바로 열지 않는다. 다음 일곱 형식을 별도 단계에서 설계하고 독립 비평·동결해야 한다.

1. `question/options`: 질문별 허용 option, 빈 affected IDs, primary/ancillary 구분
2. `transformation`: canonical만 읽는 결정적 변환과 provenance report 계약
3. `neutral answer-validation`: 질문 집합·정렬·금지어·M5/무효 경계
4. `access`: 역할별 실제 경로·허용/금지 입력·공개 시각
5. `run`: overlay 4개×block 2개의 정확한 8 pairing, 한 run 한 fresh session, wave·seed·재시도
6. `scoring`: primary 오류 코드, C 우선, oracle 결함과 total decision 입력
7. `pre-review-record`: fixture manifest·교차 검사 report·승인 결과를 순환 없이 결합

run 형식은 각 block의 overlay 4개와 package 4개를 일대일로 묶고 두 block 합계 정확히 8개인지 검사해야 한다. 같은 block 안에서 package·overlay를 중복 사용할 수 없고, 한 run은 세션 하나만 가져야 한다.

위 일곱 형식이 모두 통과한 뒤에도 사용자 승인 또는 사용자가 명시적으로 위임한 자동 게이트 판단을 거쳐야 I0나 F0를 열 수 있다. 형식 해시를 참조하는 것만으로 해당 형식이 통과한 것은 아니다.

## 10. 경로·시간·검증기 규칙

- 모든 참조 경로는 workspace 상대경로만 허용한다. 선행 `/`, `..`, 빈 경로 구간을 금지한다.
- `created_at`은 validator의 `format` 설정에만 의존하지 않고 RFC 3339 모양을 pattern으로도 제한한다.
- 실제 validator 판본·설정·artifact 해시는 validation policy와 후속 run/access 형식에서 고정한다.

## 11. SM0 통과 조건

1. 네 JSON이 문법적으로 유효하다.
2. 답안 schema에 A–D 구조·위험 코드·정답 의미가 강제되지 않는다.
3. 공통 manifest가 모델·권한·시간·출력·세션·재시도 대칭을 빠뜨리지 않는다.
4. overlay manifest가 실행자에게 조건명·가설·목표 후보를 노출하지 않는다.
5. fixture manifest가 fact·record·질문·byte·관계 provenance와 변환기 접근을 검사할 자리를 가진다.
6. schema가 보증하는 것과 외부 검증기·사전 검토자가 확인할 것을 구분한다.
7. 구현·출제·oracle·실행 게이트가 계속 닫혀 있다.

통과하면 CONTROL은 **후속 일곱 형식의 설계 단계만** 다음 후보로 판단한다. 실제 구현이나 출제로 이동하려면 그 일곱 형식까지 독립 비평·동결하고 현재 프로젝트 게이트 규칙을 충족해야 한다.
