# S0 SM0 schema·manifest 최종 제한 재비평

> 비평일: 2026-08-06  
> 역할: SM0 독립 제한 재비평자  
> 범위: 최초 독립 비평의 `SM0-B01`–`B03`, `SM0-M01`–`M02`, `SM0-N01`–`N02` 수정 여부만 재확인  
> 비범위: 실제 manifest instance, 구현, fixture, oracle, scoring, prompt, validator, run의 존재 확인 또는 평가

## 1. 입력 무결성과 범위 준수

내용을 읽기 전에 지정된 여섯 본문의 SHA-256을 직접 계산했다. 모두 제공값과 일치했다.

| 허용 입력 | 실제 SHA-256 | 결과 |
|---|---|---|
| `s0-lab/reviews/sm0-schema-manifest-independent-review.md` | `a8383c4f9b246e4e50402ee186d46fdceb59515238521d9aac4070e2765287d3` | 일치 |
| `s0-lab/control/sm0/answer.schema.json` | `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` | 일치 |
| `s0-lab/control/sm0/common-manifest.schema.json` | `a539022d937672a99c605c12980f10d89a956a40c1e8523cb02f774d280ccc8a` | 일치 |
| `s0-lab/control/sm0/condition-overlay-manifest.schema.json` | `a239c1ffa7e4b9ae3c963e7ddbf55c4cabf1f05353032cd11d9d35b842086e7a` | 일치 |
| `s0-lab/control/sm0/fixture-manifest.schema.json` | `846071f069b1cbc040ef89e176caa1698dfb13fce6c6848505a60523fd8f9c80` | 일치 |
| `s0-lab/control/sm0/sm0-schema-manifest-design.md` | `d3841d46baff6c6e8353ea31e4f83b80c9f48e4c2855012d6c5b6a027a391292` | 일치 |

지정된 두 `.sha256` 기록도 위 값과 일치했다. 그 밖의 파일은 열거나 검색하지 않았고, 실제 구현·fixture·oracle·scoring·prompt·validator·run은 존재 여부도 확인하지 않았다.

네 JSON은 모두 JSON 문법으로 파싱됐고 Draft 2020-12를 선언한다. 이번 판정은 schema 구조와 문서화된 외부 검사 계약의 정적 검토 결과다. 실제 instance나 외부 검사 결과의 유효성을 확인했다는 뜻은 아니다.

## 2. 최종 판정

**현재 SM0 동결 가능**

최초 비평의 일곱 제한 수정은 모두 충분히 반영됐다. common manifest는 로컬 capability와 모델 configuration·backend 한계를 필수화했고, fixture manifest는 재계산 근거가 되는 provenance 기록과 모든 C/M 기회의 양의 하한을 요구한다. validation policy·report schema 및 후속 일곱 형식의 schema hash가 common manifest의 필수 필드가 됐으며, 설계 문서는 이 해시가 형식의 통과를 뜻하지 않는다고 명시한다.

이 판정이 허용하는 것은 현재 네 SM0 schema 형식의 동결뿐이다. 실제 manifest 작성, 구현, 출제, fixture·oracle·scoring·validator 제작, I0·F0 또는 S0 실행은 허가하지 않는다. 다음으로 열 수 있는 범위도 후속 일곱 형식의 별도 설계 단계뿐이다.

## 3. 제한 수정별 판정

| 항목 | 판정 | 결론 |
|---|---|---|
| `SM0-B01` capability·모델 대칭 | **충분 반영** | 로컬 읽기·검색·쓰기·shell·도구·작업 디렉터리와 모델 configuration·backend 보장 한계가 모두 필수화됐다. |
| `SM0-B02` provenance·오류 기회 | **충분 반영** | mapping/report/count, oracle-derived 발견 수 `0`, C1–C7·M1–M6 최소 `1`이 추가됐다. |
| `SM0-B03` 후속 형식·게이트 분리 | **충분 반영** | 후속 일곱 형식의 schema hash와 별도 설계·독립 비평·동결·사용자 게이트가 선행조건으로 닫혔다. |
| `SM0-M01` validation policy 판본 동결 | **충분 반영** | policy와 report schema hash가 필수이며 실제 validator 판본·설정·artifact는 후속 형식에서 결과 전에 고정하도록 분리됐다. |
| `SM0-M02` 교차 동일성·freeze 연결 | **충분 반영** | 필드별 고유성과 교차 동일성을 중립 검사로 계산하고 별도 freeze record가 manifest·policy·report hash를 묶도록 명시됐다. |
| `SM0-N01` date-time 강제 | **충분 반영** | 세 manifest의 `created_at`에 `format`과 RFC 3339 형태의 `pattern`이 함께 요구된다. |
| `SM0-N02` 상대경로 안전성 | **충분 반영** | common 경로가 workspace-relative 형태로 제한되고 선행 `/`, `..`, 빈 segment가 금지됐다. |

`부분 반영`, `미반영`, `잘못 반영`으로 판정한 항목은 없다.

## 4. 항목별 근거

### SM0-B01 — 충분 반영

`common-manifest.schema.json`은 `capability_profile`을 root 필수 필드로 추가하고 다음을 닫힌 객체와 `const`로 고정한다.

- 읽기는 자신의 runner instruction, input package, answer schema, question/options로 한정
- allowlist 밖 읽기 및 저장소 검색 금지
- 쓰기는 answer output 하나로 한정
- shell 금지
- 로컬 도구는 허용된 읽기·답안 쓰기 기능만 허용
- fresh 빈 작업 디렉터리와 읽기 전용 입력 연결
- 모든 run에 같은 capability profile 적용

이는 사용자가 요구한 로컬 읽기·검색·쓰기·shell·도구·작업 디렉터리를 모두 포함한다. `local_tools_allowed: true`와 `shell_allowed: false`도 충돌하지 않는다. 허용된 로컬 도구 목록에 shell이 없고 파일 읽기·답안 쓰기 기능만 있기 때문이다.

모델 객체는 `configuration_sha256`, `backend_revision_guarantee`, `same_configuration_all_runs`를 필수화한다. backend 판본을 보장할 수 있으면 판본 ID를, 보장할 수 없으면 제한 설명을 반드시 기록하는 상호 배타적 `oneOf` 구조다. 따라서 보장 가능성과 불가능성을 모두 표현할 수 있고 빈 상태로 회피할 수 없다.

`same_*: true`는 그 자체가 사실 증명은 아니다. 설계 문서가 8개 run의 공통 설정을 외부 검사하고 policy·report를 freeze record에 결합하도록 했으므로 이 attestation을 과장하지 않는다.

### SM0-B02 — 충분 반영

`fixture-manifest.schema.json`의 transformation에는 다음이 필수다.

- 전체 `provenance_report_sha256`
- oracle-derived 관계 검사 report의 SHA-256
- `oracle_derived_relation_found_count: 0`
- canonical input hash와 결정성·oracle/scoring 비접근

각 package에는 구조 표지 수, supporting fact 연결 수, 근거 없는 표지 수 `0`, provenance mapping SHA-256이 추가됐다. 따라서 이전처럼 boolean 하나만으로 provenance를 주장하지 않고, 후속 검사가 다시 계산할 대상과 결과를 식별할 수 있다.

`opportunity_count`의 `minimum`은 `1`이다. 같은 `$defs`를 C1–C7과 M1–M6 전부가 필수로 참조하므로 어느 오류 기회도 `0`으로 통과할 수 없다.

구조 표지 수와 연결 수의 실제 일치, mapping 내용의 타당성은 JSON Schema가 아니라 동결된 중립 validation policy가 계산하도록 남겼다. 이는 schema가 수행할 수 없는 교차 계산을 숨긴 것이 아니라 설계 문서 §7.2에 명시한 정직한 경계다.

### SM0-B03 — 충분 반영

common manifest의 `references.future_format_schema_sha256`은 다음 일곱 key를 모두 필수화하고 추가 key를 금지한다.

1. `question_options`
2. `transformation`
3. `neutral_answer_validation`
4. `access`
5. `run`
6. `scoring`
7. `pre_review_record`

설계 문서 §9는 이 일곱 형식을 별도 단계에서 설계하고 독립 비평·동결하기 전에는 I0·F0를 열 수 없다고 명시한다. 일곱 형식이 통과한 뒤에도 별도 사용자 승인 또는 명시적으로 위임된 게이트 판단을 요구하며, hash를 참조하는 것만으로 형식이 통과한 것이 아니라고 닫았다.

run 형식의 미래 의무도 두 block 각각에서 overlay 4개와 package 4개를 일대일 결합하고, 합계 정확히 8개 run, 같은 block 내 재사용 금지, run당 session 하나, wave·seed·재시도 검사를 요구한다. 따라서 현재 SM0가 아직 없는 run 형식을 암묵적으로 통과시키지 않는다.

### SM0-M01 — 충분 반영

common manifest는 `validation_policy_sha256`과 `validation_report_schema_sha256`을 필수로 요구한다. 설계 문서는 다음을 추가로 고정한다.

- 검사 규칙은 결과 전에 validation policy hash로 동결
- 실제 manifest의 freeze record는 manifest·policy·교차 검사 report hash를 함께 결합
- 실제 validator 판본·설정·artifact hash는 validation policy와 후속 run/access 형식에서 고정
- 현재 단계에서는 validator를 만들지 않음

이는 검사 규칙을 결과 뒤 바꾸는 틈을 형식 단계에서 닫으면서도 아직 존재하지 않는 validator를 통과했다고 주장하지 않는다.

### SM0-M02 — 충분 반영

`uniqueItems`가 객체 전체 중복만 막는 한계는 그대로지만, 설계 문서가 package ID·runner path·input hash의 **필드별 고유성**을 외부 중립 검사 항목으로 명시했다. 같은 외부 검사는 다음 교차 동일성도 계산한다.

- 실제 파일과 manifest hash의 일치
- package 간 fact·record·본문 hash·질문 기회의 동일성
- provenance mapping과 구조 표지·supporting fact count의 일치
- overlay 길이 제한
- 모델·권한·상한의 8-run 동일성
- fresh/non-fork session·접근 시각·재시도 기록

JSON Schema 통과만으로 대칭이나 동결 완료라고 부르지 않으며, 별도 freeze record가 manifest hash, validation policy hash, 교차 검사 report hash를 묶는다. 사전 검토 승인은 fixture manifest 밖의 `pre-review-record`가 fixture manifest·교차 검사 report·승인 결과를 결합하므로 자기참조 순환도 만들지 않는다.

### SM0-N01 — 충분 반영

common, overlay, fixture의 `created_at`은 모두 `format: date-time`과 RFC 3339 형태의 정규식 pattern을 함께 가진다. pattern과 `format`의 교집합에는 정상적인 timestamp가 존재하므로 만족 불가능하지 않다. 설계 문서도 실제 validator의 format 설정을 validation policy에 고정하도록 요구한다.

### SM0-N02 — 충분 반영

common의 `opaque_path`는 다음을 동시에 적용한다.

- 선행 `/` 금지
- 경로 어디서든 `..` 금지
- `//` 금지
- 각 segment를 허용 문자 한 글자 이상으로 요구

따라서 workspace-relative이면서 빈 segment가 없는 값을 표현할 수 있다. overlay의 runner 경로와 fixture package 경로는 더 좁은 고정 pattern을 사용하므로 새 일반 경로 규칙과 충돌하지 않는다.

## 5. 새 필드의 일관성과 만족 가능성

정적 검토에서 새 필드 때문에 schema-valid instance가 불가능해지는 조합은 발견하지 못했다.

| 검사 대상 | 결론 |
|---|---|
| common의 capability 상수 | shell 금지와 제한된 로컬 파일 도구 허용은 서로 다른 capability이므로 양립 가능하다. |
| backend revision `oneOf` | `guaranteed: true`와 `false` branch가 `const`로 배타적이며 각 branch에 충족 가능한 필수 문자열이 있다. |
| future format hash 객체 | 정확히 일곱 SHA-256을 요구하며 기존 reference 구조와 충돌하지 않는다. |
| fixture provenance 필드 | count·report hash·mapping hash·발견 수 `0`을 동시에 만족할 수 있다. 실제 값의 상호 일치는 외부 검사 대상이다. |
| C/M opportunity | 13개 필드 모두 `1` 이상 `64` 이하의 정수로 만족할 수 있다. |
| package 배열 | 네 개의 서로 다른 package 객체를 허용한다. key별 고유성은 동결 policy의 외부 검사 대상임이 명시됐다. |
| RFC 3339 pattern | `format: date-time`과 동시에 만족하는 값이 존재한다. |
| 상대경로 pattern | 허용 문자로 된 하나 이상의 안전한 segment를 수용한다. |

네 schema는 다른 파일을 직접 `$ref`하지 않고 해시로 식별하므로, 아직 없는 후속 형식이 JSON Schema 해소 실패를 일으키지도 않는다. 반대로 임의의 64자리 문자열이 실제 형식의 존재·승인을 증명하지 못한다는 한계는 §9의 별도 비평·동결 게이트와 freeze report 결합으로 명시돼 있다.

## 6. 필수 확인 사항별 결론

| 확인 사항 | 판정 |
|---|---|
| 모든 run의 로컬 읽기·검색·쓰기·shell·도구·작업 디렉터리 고정 | **충분** |
| model configuration hash와 backend revision 보장·한계 | **충분** |
| provenance mapping/report/count 및 oracle-derived 발견 수 `0` | **충분** |
| C1–C7·M1–M6 opportunity 각각 최소 `1` | **충분** |
| package key 고유성·교차 동일성의 policy/freeze 경계 | **충분** |
| validation policy/report schema와 후속 일곱 schema hash 요구 | **충분** |
| 후속 일곱 형식의 독립 설계·비평·동결이 I0/F0에 선행 | **충분** |
| RFC 3339 pattern과 안전한 상대경로 | **충분** |
| 새 필드의 충돌·schema 만족 불가능성 부재 | **충분** |

## 7. 동결 범위와 다음 게이트

현재 네 SM0 schema 형식은 동결할 수 있다. 다음 단계 후보는 설계 문서 §9의 후속 일곱 형식 설계뿐이다.

다음은 여전히 닫혀 있다.

- 실제 common·overlay·fixture manifest 작성
- 실제 질문·option·prompt·scoring·oracle 작성
- fixture·변환기·validator·runner 구현
- I0·F0 개방
- S0 실행과 결과 판정

이 재비평은 위 항목의 존재나 품질을 확인하지 않았으며, Project Brain·효과·운영 안전·경제 가치 또는 모델 간 전이를 구현·검증했다고 주장하지 않는다.

**최종 판정: 현재 SM0 동결 가능**
