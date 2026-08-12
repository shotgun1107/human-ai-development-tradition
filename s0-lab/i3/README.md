# I3 공개 import-decision contract implementation revision candidate v0.2

이 디렉터리는 main에 통합된 S0 v0.14 I3 v0.2 설계를 공개·결정론적
Python 코드로 옮긴 최소 구현 후보다. 21줄 admission, 26줄 outcome, 입력 사실의
순서 있는 분류, 기존 I2 31줄 completion event와의 일치 판정만 구현한다.

이 결과는 실제 장치, 원장, 서명자, registry, VM, provider 또는 AI가 계약을
지킨다는 증거가 아니다. F0, hidden oracle, 실제 키, 모델 세션, E0와 S0는 읽거나
실행하지 않는다.

## 구현 범위

- `S0-SIGNER-IMPORT-ADMISSION-2`의 정확한 21필드 ASCII/LF codec과 SHA-256
- `S0-SIGNER-IMPORT-OUTCOME-1`의 정확한 26필드 codec, 1–25줄 body hash와
  전체 frame hash
- 세 import class의 고정 `SRC/DST`, 네 outcome tuple과 configuration-hash 규칙
- 정확히 2,048바이트인 한 raw medium, byte-zero frame, zero tail 검사
- `PRE-R`, `PRE-A`와 9개 pending row의 고정 우선순위
- caller-supplied media sequence에서만 count를 유도하는 immutable fact model
- canonical frame이 하나 있으면 외부 불확실성에도 `H`, 없으면 `Z`를 쓰는
  disagreement 처리
- I2 v0.4의 기존 parser, lifecycle, global-link 검증을 재사용하는 completion finalizer
- persisted exact accepted completion만 목적지 상태를 available로 만드는 결정
- 닫힌 기능을 `BLOCKED_NOT_EXECUTED`로 유지하는 명명된 경계

## 공개 인터페이스

주요 함수는 다음과 같다.

```text
parse_import_admission(bytes, signer_context=...) -> ImportAdmission
serialize_import_admission(value, signer_context=...) -> bytes
hash_import_admission(value, signer_context=...) -> HEX64

parse_import_outcome_frame(bytes, signer_context=...) -> ImportOutcome
serialize_import_outcome(value, signer_context=...) -> bytes
hash_import_outcome_frame(value, signer_context=...) -> HEX64

classify_import_attempt(
  optional_admission_bytes,
  ClassificationFactSet,
  route_context=authenticated_I2_route_context
) -> ImportClassification

finalize_import_attempt(
  ImportClassification,
  optional_I2_event_bytes,
  append_status,
  signer_context=...,
  expected_sequence=...,
  expected_previous_event_sha256=...
) -> ImportDecision
```

분류 함수의 명시적 `route_context`는 I2 v0.4가 이미 인증하는 route identity와
`SRC/DST`를 재사용한다. admission이 없거나 outcome이 망가진 경우에도 source
state와 completion ID를 추측하지 않도록 필요한 입력이다. 숨은 기본값이나 파일
검색을 추가하지 않는다. finalizer의 두 전역 연결 인자는 호출자가 제공한 I2
sequence와 predecessor evidence이며, 누락되거나 event와 불일치하면
`no-completion-claim`으로 닫힌다. 이 매핑은
`spec/import-decision-contract-v0.1.json`에 기계 판독 가능하게 고정했다.

## 안정된 오류

직접 codec·binding 작업은 `I3_BYTE_ERROR`, `I3_FIELD_ERROR`,
`I3_VALUE_ERROR`, `I3_ROUTE_ERROR`, `I3_TUPLE_ERROR`, `I3_HASH_ERROR`,
`I3_BINDING_ERROR`, `I3_INPUT_ERROR`, `I3_EVENT_ERROR`를 구분한다.

정확한 bytes가 아닌 API 객체는 input error다. 반면 canonical하지 않은 admission
또는 medium bytes는 well-typed evidence이므로 분류 함수가 disagreement, missing,
duplicate 등 고정 행으로 처리한다. finalizer의 event 불일치나 append 미확정은
권한을 주지 않는 `no-completion-claim`이다.

## 검증 범위

공개 unittest는 다음을 포함한다.

- admission 21개 및 outcome 26개 필드의 순서·존재·바이트·값 변이
- 세 route와 네 canonical outcome tuple
- 모든 pairwise `R/A/P/C/result_media_id` 충돌
- body hash, full-frame hash, admission/outcome binding
- missing/duplicate/complete-malformed/nonzero-offset/nonzero-tail 경계
- 네 tuple과 normal/unknown/not-started/abnormal 교차
- 8개 status 각각의 conflict/unavailable 변이
- phase 3 × end 4 × status `3^8`, 총 78,732 closed-enum 조합
- 모든 결과 class와 exact I2 completion event의 finalization
- persisted가 아닌 append, 잘못된 event와 닫힌 기능
- operational/network/process import 부재

테스트는 코드 안에서 생성한 공개 합성값만 사용한다. S0 정식 fixture나 F0를
만들거나 읽지 않는다.

## 검증기

검증기는 외부에서 고정한 `implementation-files.sha256`의 SHA-256을 반드시
입력받는다. 공개 source manifest와 I2 v0.4 구현 manifest를 인증하고, 인증한
payload만 임시 snapshot으로 복사한 다음 generator self-test, unit tests,
contract CLI와 import audit을 실행한다. 마지막에는 원본을 다시 해시한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File s0-lab/i3/tools/verify-i3.ps1 `
  -ExpectedManifestSha256 <implementation-files-sha256>
```

성공 시 `SYNTHETIC_GENERATOR_SELFTEST`, `STATIC_INTEGRITY`,
`PUBLIC_SOURCE_INPUTS`, `UNIT_TESTS`, `GRAMMAR_HASH_BINDING`,
`CLASSIFICATION`, `FINALIZATION`, `CONTRACT_CLI`, `FORBIDDEN_IMPORT_AUDIT`,
`FINAL_STABILITY`가 각각 `PASS`여야 한다. `CLOSED_BOUNDARIES`는
`BLOCKED_NOT_EXECUTED`로 남아야 한다.

## 닫힌 경계와 최대 주장

실제 durable ledger/witness, project-lifetime uniqueness, atomic append,
registry authority, key/signature, same-process hostile isolation, VM·sandbox·network,
provider/model, protected material, F0, fixture/oracle, executor/judge, E0/S0,
중앙 시스템과 Project Brain은 구현·실행·검증하지 않았다.

최대 주장은 인증된 공개 입력에 한해 I3의 두 codec, 순서 있는 분류와 I2 event
연결이 model-free 공개 테스트를 통과한 구현 후보라는 것이다. 독립 심사나
CONTROL/main 통합은 별도 게이트다.
