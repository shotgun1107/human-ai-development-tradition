# S0 SM1 후속 7개 형식 설계 후보

> 판본: `sm1-0.2-major-fix-candidate`  
> 기준 프로토콜: `s0-protocol-v0.3.md` (`b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c`)  
> 기준 SM0: `sm0-freeze-record.md`  
> 상태: **독립 비평 전 형식 후보 — 구현·출제·실행 금지**

## 1. 목적과 범위

SM0가 공통 답안·자원·조건·fixture의 기본 양식을 동결했다. SM1은 그 양식 사이에서 빠졌던 일곱 연결 계약을 정의한다. 모두 **JSON 형식 설계**이며 실제 질문, 합성 사건, 정답, 채점표, 코드, 세션, 실행 결과는 포함하지 않는다.

## 2. 산출물

| 형식 | 해결하는 문제 | 실제 내용 포함 여부 |
|---|---|---|
| `question-options.schema.json` | 질문별 중립 option과 runner 공개/봉인 필드 분리 | 없음 |
| `transformation-manifest.schema.json` | canonical만 읽는 결정적 변환과 4개 package·provenance 기록 | 없음 |
| `neutral-answer-validation.schema.json` | 답안 형식·질문 집합·정렬·금지 노출과 M5/무효 경계 | 없음 |
| `access-manifest.schema.json` | 역할·세션별 허용 입력·출력·금지 정보·공개 시각 | 없음 |
| `run-manifest.schema.json` | 4 overlay×2 block의 정확한 8개 실행 계획 | 없음 |
| `scoring.schema.json` | primary C/M·중복 금지·oracle 결함·선택표 입력 | 없음 |
| `pre-review-record.schema.json` | 실행 전 독립 검토의 입력 해시·격리·승인/거부 기록 | 없음 |

## 3. question/options 경계

한 block의 sealed 문서는 질문, 중립 option, 인용·영향 ID 정책, primary/ancillary 분류와 scoring 참조를 가진다. 실행자는 여기서 다음 runner projection만 받는다.

- block ID와 question ID
- 질문 문장
- 중립 `OPT-*` ID와 사람이 읽을 option 문장
- 인용 필수 여부와 affected IDs 처리 규칙

평가 역할, scoring contract ID, oracle 참조, 조건 대응표, 목표 선호는 runner projection에서 제외한다. option 문장 자체에 정답 표지가 없는지는 JSON Schema가 아니라 사전 검토자가 확인한다.

question/options와 scoring은 서로의 최종 파일 해시를 요구하지 않는다. question/options는 안정적 불투명 `scoring_contract_id`만 갖고, scoring instance만 question/options의 최종 SHA-256을 단방향으로 참조한다. 이 방식으로 순환 해시를 금지한다.

질문 ID와 option ID의 필드별 고유성, runner projection hash와 실제 projection의 일치는 neutral validation policy가 검사한다.

## 4. transformation 경계

변환기는 자기 block의 canonical input과 공개 transformation schema만 읽는다. oracle, scoring, 다른 block, 네트워크에는 접근하지 않는다.

형식은 다음을 결과 전에 묶는다.

- 변환 artifact·configuration·runtime 해시와 결정성
- canonical·fact manifest·변환 schema 해시
- 불투명 package 정확히 4개
- block과 무관하게 유지되는 불투명 treatment profile ID·profile 해시 정확히 4개
- package별 입력·fact set·record 본문 set·provenance mapping 해시
- 구조 표지 수·근거 연결 수·근거 없는 표지 수 0
- fact·record 동등성, padding 없음, byte 차이 15% 이하
- provenance·fact 동등성·byte·oracle-derived 관계 검사 report 해시

같은 treatment profile은 두 block에서 같은 불투명 ID·profile 해시를 사용한다. run validation은 같은 overlay가 두 block에서 반드시 같은 profile과 결합되는지 검사한다. 실제 profile→A–D 대응표는 CONTROL 전용 영역에만 둔다.

실제 변환 코드와 package는 I0/F0 뒤에만 생길 수 있다.

## 5. 중립 답안 검사 경계

검사 정책은 다음을 결과 전에 고정한다.

- UTF-8·JSON parse·answer schema
- 정확한 질문 ID 집합과 질문당 답 하나
- 질문·record ID 정렬과 중복 금지
- 질문별 option과 affected IDs 정책
- short reason 한 줄과 `short_reason` 필드에만 적용되는 금지 노출 정책
- 답안 최대 8,192 bytes

결과 분류는 프로토콜 v0.3을 그대로 따른다.

| 사건 | 결과 |
|---|---|
| 출력 없음·UTF-8 실패·JSON parse 실패·input hash 불일치·크기 초과 | suite 무효 |
| schema 위반·질문 누락/중복·허용되지 않은 option·정렬/ID 중복 | M5 |
| short reason의 금지 정보 노출 | M6 |

validation report는 policy·input·answer뿐 아니라 실제 question projection과 answer schema의 SHA-256도 기록한다. run manifest와 같은 projection·schema를 사용했는지 교차 검사한다. decision·cited/affected IDs의 권한 오류는 M6로 돌리지 않고 scoring의 C 코드가 처리한다.

검사기 artifact·configuration·runtime 해시는 실제 구현 뒤 policy instance에 넣는다. 현재는 코드를 만들지 않는다.

## 6. access 경계

access manifest는 역할 한 명과 session slot 하나의 계약이다.

- fresh/non-fork, 대화 상속 없음, 역할 간 session 공유 없음
- 허용 입력은 path·hash·정보 등급·공개 단계로 열거
- 허용 출력은 path·파일 수·byte 상한으로 열거
- 다른 조건/다른 block/조건 대응표/가설/목표 선호/oracle/scoring/과거 결과 등 금지 정보 등급 기록
- 저장소 검색·allowlist 밖 읽기·쓰기·네트워크·subagent·외부 전송·사람 내용 개입 금지
- shell 허용 여부는 역할 policy 해시와 함께 명시하며 executor는 SM0 common profile에 의해 금지
- 입력 공개는 사전 동결 release policy와 로그 schema hash를 따른다
- protocol·schema·manifest·condition package·role/release policy·implementation artifact·run record 등 artifact 종류와 authoring/implementation/transformation/pre-review/execution/post-run 공개 단계를 구분
- 모든 role-policy 원문과 release-policy 원문 묶음의 해시를 pre-review 입력에 포함

역할별로 정확히 어떤 정보 등급이 허용되는지는 별도 role policy instance가 고정한다. schema-valid boolean만으로 실제 격리를 주장하지 않는다.

## 7. run pairing 경계

run manifest는 suite 하나의 사전 계획이다.

- block 2개, overlay 4개, 실행 8개
- 각 block에서 overlay 4개를 한 번씩 사용
- 각 block에서 package 4개를 한 번씩 사용
- block 안에서 overlay와 package 일대일 pairing
- run ID·session slot·순서 위치 고유
- 같은 overlay의 두 block을 같은 wave에 두지 않음
- 같은 overlay는 두 block에서 같은 treatment profile ID·해시에만 결합
- 동시 실행 최대 3
- 정확한 protocol+sealed input hash로 순서 seed 계산
- 한 run 재시도 금지, 전체 suite 기술 재시도 최대 1, 가장 이른 유효 suite만 사용
- attempt 1은 prior suite·run-record bundle·실패 단계·봉인 input 공개 여부·과거/현재 block input 해시를 필수로 기록
- 공개 전 실패면 같은 block만 허용하고, 공개 뒤 실패면 새 두 block 해시를 요구

JSON Schema의 `uniqueItems`는 객체 전체 중복만 막는다. 필드별 고유성과 4×2 조합은 동결 validation policy가 계산하며 pre-review record가 그 report를 참조한다.

executor 실제 task/thread ID는 사전 run manifest에 넣지 않는다. 사전에는 불투명 session slot만 고정한다. `run-manifest.schema.json#/$defs/run_record`가 사후 기록 형식을 함께 정의하며, 세션 생성 직후 봉인 input 공개 전에 실제 task ID를 slot에 결합하고 binding record를 해시한다. 이후 run record가 실제 ID·시각·입력·도구 로그·사람 개입을 묶는다. 정상 실행은 답안 hash·byte를 요구하고, 기술 실패는 답안 대신 실패 이유·로그 hash를 요구한다. 이 형식만 설계했으며 실제 record나 세션은 만들지 않는다.

## 8. scoring 경계

scoring 형식은 oracle 답 자체가 아니라 질문·관찰 사건이 어떤 primary 오류 코드로 이어지는지를 정의한다.

- C1–C7·M1–M6 각각 최소 한 criterion은 외부 validation policy가 확인
- `C*`는 critical, `M*`는 major로 schema가 강제
- 같은 질문·같은 원인의 C/M은 C만 세고 이중 계수 금지
- 독립 원인만 별도 계수, 코드별 block 최대 1
- primary 결함은 전체 suite 무효·새 게이트, ancillary 결함은 보고만
- 정확성 채점 중 조건 identity 비공개
- D 선택은 프로토콜 §9의 두 block 반복 우위만 허용
- 비용은 익명 정확성 해시 동결 뒤 결합

scoring은 question/options를 단방향 해시로 참조하며 두 문서의 순환 해시를 금지한다. 각 criterion에는 고유 question-event key가 있고, validation policy가 13개 오류 코드가 모두 등장하는지와 criterion/event key의 필드별 고유성을 검사한다.

사후 판정자는 전체 scoring 파일이 아니라 criteria·counting policy만 포함한 익명 judge projection을 받는다. D 선택 규칙·decision function·조건 identity·비용은 정확성 해시 동결 전에 보지 않는다. CONTROL과 사전 검토자는 §9 decision function artifact를 보고 프로토콜과 일치하는지 확인한다.

criterion의 oracle rule reference가 실제 oracle에 존재하고 예상 결과와 모순 없는지는 사전 검토자가 확인한다.

## 9. pre-review record 경계

사전 검토 기록은 이미 동결된 입력의 해시를 받아 승인하거나 거부한다. 따라서 fixture manifest 안에 자기 승인 hash를 넣는 순환이 없다.

검토자는 fresh/non-fork이며 executor 답안, run record, 조건 대응표, 사후 비용을 보지 않는다. 검토 입력에는 다음이 포함된다.

- schema 묶음·common·overlay 4개·fixture 2개
- question/options 2개·transformation 2개
- validation policy·report·access 묶음·모든 role/release policy 원문 묶음·run manifest·embedded run-record contract
- oracle 2개·scoring 2개·condition package 8개
- §9 decision function artifact

승인일 때 기존 의미 검사와 함께 cross-block treatment, validation↔question projection, retry 적격성, 13개 코드 coverage, decision function 일치, role/release policy 완전성, run-record contract 준비 check가 모두 true여야 한다. 거부일 때는 최소 하나가 false여야 한다. 각 check의 근거를 묶은 evidence report와 review report를 해시하며, 승인 기록은 executor 세션 생성 전에 동결된다.

## 10. JSON Schema와 외부 검사의 분업

JSON Schema가 직접 강제하는 것:

- 필수 필드·자료형·ID·SHA-256 모양
- 배열 수량 2·4·8과 고정 상한
- boolean·const·C/M severity·approve 조건
- 안전한 상대경로와 RFC 3339 모양

동결 validation policy가 계산하는 것:

- 질문·option·package·run key의 필드별 고유성
- overlay×block 정확한 8 pairing
- 두 block에서 같은 overlay↔treatment profile 결합
- 해시가 가리키는 실제 파일 일치
- fact·record·본문·질문 기회 동등성
- provenance mapping의 실제 완전성
- C1–C7·M1–M6 coverage
- attempt 1의 이전 실패·공개 상태·새 block 필요 조건
- runner projection의 금지 필드·힌트 없음

사전 독립 검토자가 판단하는 것:

- 관계가 canonical에 실제 명시됐는가
- 질문·option·overlay 문구가 특정 조건을 유리하게 하는가
- oracle·scoring이 논리적으로 모순 없는가
- 역할별 허용 정보가 목적에 맞고 누출되지 않는가

## 11. 아직 만들지 않은 것

- 실제 일곱 형식의 instance
- role policy·release log·validation report·run record·task binding record의 실제 instance 또는 구현
- 질문·option 문장, 합성 사건, oracle, scoring 내용
- 변환기·validator·runner 코드
- 실행 세션·답안·판정 결과

따라서 SM1이 통과해도 구현이나 S0 효과가 검증된 것이 아니다.

## 12. SM1 통과 조건

1. 일곱 JSON이 Draft 2020-12 구조로 문법적·정적으로 만족 가능하다.
2. runner가 보는 질문·option에 평가 역할·oracle·scoring·조건 선호가 섞이지 않는다.
3. 변환기는 canonical+공개 schema 외 정보에 접근할 수 없다.
4. 답안 검사 결과가 v0.3의 M5/M6/suite 무효 경계와 같다.
5. access가 역할·세션·입력·출력·공개 시각을 해시로 묶는다.
6. run 형식이 4×2=8 pairing과 wave·seed·재시도를 사전에 고정할 수 있다.
7. scoring이 primary C 우선·중복 금지·결함·total function을 훼손하지 않는다.
8. pre-review 승인과 거부가 순환 없이 동결 입력·report에 결합된다.
9. schema 보장, 외부 계산, 사람 의미 검토가 구분된다.
10. 실제 구현·출제·oracle·실행 관문은 계속 닫혀 있다.

통과하면 CONTROL은 다음 단계가 구현 준비인지, 추가 형식 보완인지 위험과 프로젝트 게이트를 기준으로 판단한다.
