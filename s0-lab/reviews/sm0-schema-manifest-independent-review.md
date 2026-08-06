# S0 SM0 schema·manifest 독립 비평

> 비평일: 2026-08-06  
> 역할: SM0 독립 비평자  
> 범위: v0.3 다음 단계의 네 JSON Schema와 설계 문서 형식만 검토  
> 비범위: 실제 manifest 인스턴스, 구현, 공개·봉인 fixture, oracle, scoring, prompt, 변환기, run, 판정 결과의 존재 확인 또는 평가

## 1. 입력 무결성과 허용 범위

내용을 읽기 전에 지정된 7개 본문의 SHA-256을 직접 계산했다. 모두 제공값 및 지정 `.sha256` 기록과 일치했다.

| 허용 입력 | 실제 SHA-256 | 결과 |
|---|---|---|
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | 일치 |
| `s0-lab/reviews/s0-protocol-v0.3-final-limited-rereview.md` | `e395fbfb843fab490ce3bde859de4898aa753be2d89eb24d344eaf7809f03941` | 일치 |
| `s0-lab/control/sm0/answer.schema.json` | `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` | 일치 |
| `s0-lab/control/sm0/common-manifest.schema.json` | `8b4f4634e1768795785836e6d8b24732cbcead86928bfe059cda8015b3284a2e` | 일치 |
| `s0-lab/control/sm0/condition-overlay-manifest.schema.json` | `068e0d005b2a8010bff99316f09abfc236eefa224d086b556a9940b1b63ffba0` | 일치 |
| `s0-lab/control/sm0/fixture-manifest.schema.json` | `180dff22d372992bf351f184268f03e36baaffbe4f848a77baee34d23793415b` | 일치 |
| `s0-lab/control/sm0/sm0-schema-manifest-design.md` | `89cef721fcb425951dd0686b63da9f1fe0874a55cb130aab3f782e93f7e3fea0` | 일치 |

허용된 세 `.sha256` 파일도 위 값과 일치했다. 그 외 파일은 읽거나 검색하지 않았고, 실제 구현·fixture·oracle·scoring·prompt·run은 존재 여부도 확인하지 않았다.

네 JSON은 모두 JSON 문법으로 파싱됐다. 정적 검토에서 Draft 2020-12에 없는 keyword, 해소되지 않는 로컬 `$ref`, 서로 양립할 수 없는 `const`·`required` 조합은 발견하지 못했다. 따라서 각 schema는 적어도 자신이 선언한 **단일 파일의 구조 제약**을 만족하는 인스턴스를 받을 수 있다. 이는 교차 파일 사실이나 `const: true` 진술의 진실성을 검증했다는 뜻이 아니다.

## 2. 최종 판정

**제한 수정 후 SM0 동결 가능**

`answer.schema.json`과 condition overlay의 control/runner 분리는 현재 형태로 다음 단계에 사용할 수 있다. 설계 문서도 JSON Schema, 교차 파일 계산, 사람·독립 AI 의미 검토를 구분해 `const: true`를 실제 증거로 과장하지 않는다.

그러나 다음 세 항목은 SM0 형식 동결 전에 닫아야 한다.

1. common manifest가 인터넷 계열 권한은 기록하지만 로컬 파일 열람·검색·쓰기, shell·로컬 도구, 작업 디렉터리와 완전한 모델 설정을 고정하지 않는다.
2. fixture manifest가 relation provenance를 boolean 진술 하나로만 기록하고, C1–C7·M1–M6 질문 기회를 `0`으로도 허용한다.
3. 4 overlay×2 block의 정확한 8개 pairing과 외부 답안 검사, 접근·scoring·변환 규칙을 맡을 아직 없는 형식들이 다음 게이트로 명시적으로 고정되지 않았다. 현재 설계의 마지막 문장은 네 schema 동결 뒤 사용자 게이트만으로 I0/F0를 열 수 있는 것처럼 읽힐 여지가 있다.

이 결함들은 네 schema의 중심 구조를 다시 만들 필요는 없고 필드·외부 검사 계약·게이트 문구를 보완하면 된다. 따라서 `중대한 수정`이 아니라 `제한 수정` 판정이다.

## 3. 파일별 판정

| 파일 | 판정 | 판단 |
|---|---|---|
| `s0-protocol-v0.3.md` | **충분** | SM0가 보존해야 할 중립 답안, 자원 대칭, C/M, 재시험, total function과 금지 게이트를 명확히 제공한다. |
| `s0-protocol-v0.3-final-limited-rereview.md` | **충분** | schema·manifest에서 확인해야 할 항목과 구현·출제 비허용 범위를 정확히 구분한다. |
| `answer.schema.json` | **충분** | D 구조·조건명·오류 코드·정답 의미를 넣지 않고 opaque option과 record ID만 요구한다. 로컬 형식 제약은 Draft 2020-12로 일관된다. |
| `common-manifest.schema.json` | **부분** | 모델·시간·출력·세션·8 runs·동시성·wave·suite retry의 기본값은 있다. 로컬 파일·shell·도구 권한과 완전한 모델 configuration/제공자 판본 한계가 빠졌다. |
| `condition-overlay-manifest.schema.json` | **충분** | control-only manifest와 runner가 실제 받는 instruction/input을 분리하며 opaque 경로·비노출 진술과 네 overlay 해시 결합 경계를 제공한다. 실제 진실성은 사전 검토 대상으로 정직하게 남긴다. |
| `fixture-manifest.schema.json` | **부분** | canonical·sealed hash, item 수, package 4개, byte/token/fact/record/question/relation, 변환기 접근과 freeze 자리는 있다. provenance의 재계산 가능한 기록과 필수 오류 기회 하한이 부족하다. |
| `sm0-schema-manifest-design.md` | **부분** | 세 층 검증과 순환 없는 사전 검토 기록 분리는 타당하다. 다만 아직 없는 run/access/question/scoring/transformation 형식을 명시적 미통과 게이트로 열거하지 않아 마지막 단계 문구가 과도하게 읽힐 수 있다. |

`실패` 판정 파일은 없다.

## 4. 차단 발견 사항

### SM0-B01. common manifest의 권한·모델 대칭이 불완전하다

**확인 사실**

`common-manifest.schema.json`은 subagent, 인터넷, MCP, browser, 외부 전송, 사람 개입을 고정한다. 그러나 다음은 필드가 없다.

- runner가 읽을 수 있는 파일의 allowlist 또는 capability profile
- 저장소·다른 조건·oracle 경로 검색 금지
- answer 이외 파일 쓰기 금지와 출력 경로
- local shell·로컬 도구 사용 허용 여부와 allowlist
- 작업 디렉터리·환경 공유 범위
- 모델의 나머지 실행 설정을 묶는 configuration hash
- 제공자 내부 판본 동일성의 보장 가능 여부와 미보장 사유

**영향**

현재 schema를 만족하는 common manifest 두 개가 같은 `model_id`, `reasoning_effort`와 인터넷 금지를 기록하면서도 서로 다른 로컬 파일·shell 권한 또는 모델 세부 설정을 허용할 수 있다. 이는 v0.3이 요구한 권한·구성 대칭을 common manifest만으로 고정하지 못한다.

**최소 수정**

1. common manifest에 공통 `capability_profile`을 추가한다.
   - own instruction·own input·answer schema·question options만 읽기
   - repository search와 allowlist 밖 읽기 금지
   - answer 하나 외 쓰기 금지
   - shell·local tool의 금지 또는 정확한 allowlist
   - 공통 working-directory 정책
2. 실제 경로는 후속 access/run manifest가 갖더라도, common manifest는 그 schema 해시와 `same_capability_profile_all_runs: true`를 요구한다.
3. model 객체에 전체 설정을 가리키는 `configuration_sha256` 또는 닫힌 settings 객체를 추가한다.
4. 내부 backend revision을 보장할 수 있는지와, 불가능할 때 기록할 제한 설명을 필수화한다. `same_configuration_all_runs: true` 자체는 증거가 아니다.

이 수정 전에는 common manifest를 `권한 대칭 양식`으로 동결할 수 없다.

### SM0-B02. fixture provenance와 오류 기회가 약한 진술만으로 통과할 수 있다

**확인 사실**

- package는 `explicit_relation_count`와 `all_structural_markers_have_supporting_fact_id: true`만 기록한다.
- 전체 invariants는 `oracle_derived_relation_added: false`를 요구한다.
- C1–C7·M1–M6의 `opportunity_count`는 `minimum: 0`이다.

**영향**

schema-valid 인스턴스가 실제 구조 표지→fact 연결의 수·집합·해시를 남기지 않고도 `true`를 주장할 수 있다. 또한 특정 C/M 기회를 0으로 적어도 형식상 유효하므로, v0.3 §5.3의 `C1–C7·M1–M6이 중립 출력에서 관찰 가능` 조건을 누락한 봉인 block이 schema 검사를 통과할 수 있다.

**최소 수정**

1. package 또는 transformation에 다음 중립 검사 결과를 추가한다.
   - `structural_marker_count`
   - `supporting_fact_link_count`
   - `unsupported_structural_marker_count: 0`
   - provenance mapping 또는 중립 변환 report의 SHA-256
2. oracle-derived 관계도 단순 boolean 외에 검사 report hash와 발견 수 `0`을 기록한다.
3. v0.3이 모든 C/M을 관찰 가능하게 요구하므로 각 `opportunity_count`의 최소값을 `1`로 올리거나, protocol-defined 최소값을 외부 검사 계약에 명시하고 그 계약 해시를 fixture manifest가 참조하게 한다.
4. 네 package의 `package_id`, `runner_path`, `input_sha256`이 각각 유일한지 외부 검증기가 확인하도록 명시한다. `uniqueItems`는 객체 전체의 동일성만 막고 key별 중복은 막지 않는다.

관계가 canonical에 실제로 명시됐는지는 여전히 사전 봉인 검토자가 확인해야 한다. 위 수정은 사람 의미 판단을 대체하지 않고, 그 판단이 어떤 생성 결과를 대상으로 했는지 재현 가능하게 만든다.

### SM0-B03. 아직 없는 후속 형식과 I0/F0 게이트를 더 명시적으로 분리해야 한다

**확인 사실**

- overlay 설명은 미래 run manifest가 overlay와 block package를 조합한다고 한다.
- common manifest는 overlay 4개, fixture 2개, run 8개를 기록한다.
- fixture manifest 하나는 package 4개를 기록한다.
- 현재 허용 입력에는 run/access/question/scoring/transformation schema가 없다.
- 설계 문서 §8은 실제 내용·코드를 만들지 않았다고 하지만, §9 마지막 문장은 네 형식의 비평·동결과 프로젝트 게이트 뒤 구현·출제로 이동할 수 있는 것으로 읽힐 수 있다.

**판단**

현재 4 overlay×2 block=8이라는 수량은 모순이 없다. 한 overlay manifest는 조건 표현 하나, 한 fixture manifest는 block 하나의 package 4개이며, 미래 run manifest가 정확한 8개 pairing을 만드는 경계도 설명돼 있다. 문제는 그 미래 형식이 아직 없는데도 네 schema 동결이 I0/F0의 마지막 문서 조건처럼 읽힐 수 있다는 점이다.

**최소 수정**

설계 문서의 다음 게이트를 명시적으로 나눈다.

1. 현재 SM0: 네 schema 형식의 제한 수정·동결만 가능
2. 후속 형식 게이트: 최소한 question/options, transformation, neutral answer-validation, access, run, scoring, pre-review-record 형식의 설계·독립 비평·동결
3. 그 뒤에도 사용자의 별도 게이트가 있어야 I0 또는 F0 역할을 열 수 있음
4. run 형식은 각 block에서 overlay 4개와 package 4개를 일대일로 묶고, 두 block 합계 정확히 8개, package·overlay 재사용 없음, 한 run 한 session, wave와 seed 규칙을 검증해야 함

`question_manifest_sha256` 등을 참조하는 것만으로 해당 형식이 통과한 것은 아니다. 이 문구가 추가되기 전에는 이번 SM0 비평으로 I0/F0를 열 수 없다.

## 5. 중대 발견 사항

### SM0-M01. 필수 외부 검사기의 판본·해시를 동결할 자리가 부족하다

**확인 사실**

설계 문서는 질문 집합, option, 정렬, 금지어, package 동등성, overlay 길이, 8-run 대칭을 후속 중립 검증기가 계산한다고 정확히 밝힌다. 그러나 현재 common manifest에는 그 검증 규칙 또는 validator artifact의 schema·판본·해시를 기록할 필드가 없다.

**영향**

같은 답안·manifest에 서로 다른 검사기를 적용하거나 결과를 본 뒤 금지어·정렬·pairing 규칙을 바꾸어도 현재 네 schema만으로는 판본 차이를 잡지 못한다. 이는 M5와 suite 무효 경계를 후속 구현에 암묵적으로 맡긴다.

**최소 수정**

- common manifest 또는 별도 validation-policy manifest에 `validation_policy_sha256`, `validator_schema_sha256`을 요구한다.
- 실제 validator artifact가 생기는 단계에는 artifact SHA-256과 실행 환경을 추가한다.
- 질문 집합 불일치·정렬·금지어·option 오류 중 무엇이 M5이고 무엇이 suite 무효인지 v0.3·scoring과 같은 의미로 결과 전에 고정한다.

### SM0-M02. 교차 파일 동일성과 정확한 pairing은 JSON Schema가 아닌 외부 계약임을 instance 동결 조건에 연결해야 한다

**확인 사실**

- `uniqueItems`는 answer 객체의 `question_id` 고유성이나 package의 `package_id` 고유성을 보장하지 않는다.
- common의 두 fixture hash, 네 overlay hash와 fixture별 네 package 사이의 일대일 결합은 개별 schema가 계산하지 않는다.
- canonical hash와 transformation의 canonical hash가 같은지, package count가 canonical count와 같은지도 개별 schema가 비교하지 않는다.

설계 문서는 이러한 계산을 외부 검사로 돌리는 경계를 대체로 정직하게 밝힌다. 다만 실제 manifest instance가 `frozen`으로 불리기 위한 조건에 외부 검사 결과 해시가 연결돼 있지 않다.

**최소 수정**

- 각 실제 manifest instance는 중립 교차 검사 report의 해시와 검사 정책 해시를 별도 freeze record에서 참조하게 한다.
- JSON Schema 통과만으로 `동결 완료`, `대칭 확인`, `fresh 확인`이라고 부르지 않는다.
- 사전 봉인 승인 기록은 fixture manifest 밖에 유지하되 fixture manifest hash, 교차 검사 report hash와 승인 결과를 함께 묶는다.

## 6. 경미 발견 사항

### SM0-N01. Draft 2020-12의 `format`은 기본적으로 강제 검증이 아닐 수 있다

세 manifest schema의 `created_at`은 `format: date-time`을 쓴다. Draft 2020-12 기본 meta-schema에서 `format`은 annotation으로 취급될 수 있어 validator가 잘못된 날짜를 거부한다고 보장할 수 없다.

**최소 수정:** format-assertion을 지원·활성화한 validator를 검사 정책에 고정하거나, 필요한 최소 RFC 3339 형태를 `pattern`으로도 제한한다.

### SM0-N02. common의 일반 `opaque_path`는 상대경로 안전성을 강제하지 않는다

`^[A-Za-z0-9._/-]{1,240}$`는 선행 `/`, `..`, 중복 구분자를 허용한다. overlay와 package 경로는 더 엄격하지만 protocol·schema·instruction 참조는 이 일반 pattern을 쓴다.

**최소 수정:** workspace-relative 경로만 허용하고 `..`, 선행 `/`, 빈 segment를 금지하는 pattern 또는 외부 canonical-path 검사를 추가한다.

## 7. 필수 검토 항목별 결론

| 검토 항목 | 판정 | 근거 |
|---|---|---|
| 네 JSON의 Draft 2020-12 구조와 인스턴스 검증 가능성 | **충분** | 네 파일 모두 JSON 파싱에 성공했고 표준 keyword와 로컬 `$ref`가 모순 없이 구성됐다. 단, 교차 의미는 별도 검사다. |
| answer의 조건·D·오류 코드·정답 누출 | **충분** | option은 opaque ID이고 D 구조·C/M 코드·정답 enum을 포함하지 않는다. |
| 질문별 option·정확한 집합·정렬·short_reason 외부 검사 경계 | **부분** | 외부로 미룬 이유와 검사 항목은 정직하다. 검사 정책·판본·M5 경계의 해시 자리가 부족하다. |
| common의 모델·권한·시간·출력·세션·8 runs·wave·retry | **부분** | 시간·출력·세션·수량·wave·retry는 있다. 로컬 filesystem/shell/tool 권한과 전체 모델 configuration이 빠졌다. |
| overlay 4개와 block별 package 8개의 결합 | **충분—후속 형식 대기** | 4×2 구조는 모순 없고 run manifest로 pairing한다는 경계가 명시됐다. 아직 pairing을 검증한 것은 아니다. |
| overlay control-only와 runner 실제 파일 분리 | **충분** | visibility와 설계 문서가 manifest 비노출, instruction+package input만 전달하도록 분리한다. |
| fixture의 canonical·fact·record·질문·byte·token·provenance·접근·해시 | **부분** | 대부분의 hash·count·access 자리는 있다. provenance report와 필수 C/M 기회 하한이 부족하다. |
| 사전 검토 승인을 fixture manifest 밖에 둔 순환 방지 | **충분** | fixture hash를 먼저 동결하고 별도 승인 기록이 이를 참조하므로 자기참조를 피한다. |
| `const: true` attestation의 과장 여부 | **충분** | 설계 문서가 schema는 진술 형태만 검사하고 실제 파일 계산·사람 의미 검토가 별도임을 명시한다. |
| v0.3 run-valid/M5·primary C·oracle 결함·total function 보존 | **충분—후속 형식 대기** | 현 schema가 대체 규칙을 만들지 않는다. 실제 question/scoring/run 형식에서 동일 의미를 다시 확인해야 한다. |
| 아직 없는 형식과 I0/F0 게이트 | **부분** | 현재 상태는 구현·출제 금지를 말하지만, 누락 형식을 명시적 선행 게이트로 열거해 오독 여지를 제거해야 한다. |

## 8. 수정 후 동결 확인 기준

다음만 확인하면 전체 설계를 다시 비평할 필요 없이 제한 재확인으로 SM0 동결 여부를 판단할 수 있다.

1. common manifest에 로컬 capability profile, 전체 모델 configuration과 제공자 판본 한계가 추가됨
2. fixture manifest에 검증 가능한 provenance report/count와 C/M 기회 하한이 추가됨
3. 외부 validation policy·교차 검사 report를 실제 freeze와 연결할 해시 자리가 추가됨
4. future run/access/question/scoring/transformation/pre-review 형식이 미통과 상태이며 I0/F0 선행조건임을 설계 문서가 명시함
5. date-time assertion과 안전한 상대경로 규칙이 고정됨

수정 뒤에도 실제 schema·manifest 인스턴스, validator, 변환기, fixture 또는 oracle을 만들 필요는 없다.

## 9. 결론과 허용 범위

SM0는 형식 계층과 정보 분리 방향은 유지할 수 있으나, common 권한 대칭과 fixture provenance·오류 기회, 후속 형식 게이트를 보완하기 전에는 동결할 수 없다.

**최종 판정: 제한 수정 후 SM0 동결 가능**
