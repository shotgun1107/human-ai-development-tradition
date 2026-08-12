# I3 공개 import-decision 구현 v0.2 제한 수정 검증 보고서

- `date`: `2026-08-12 KST`
- `branch`: `codex/s0-i3-public-import-decision-contract-implementation-v02-bounded-revision`
- `base_commit`: `d1b79cb8a032c285202aef7d72b80121065e217d`
- `gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT IMPLEMENTATION V0.2 BOUNDED REVISION OPEN`
- `responds_to`: `I3-IIR-B01`
- `independent_review_sha256`: `ec1ecc1f9aaf9b32ca7d285d898ec5620e05a8327716a0e16eed2d01530b28ca`
- `claim_kind`: author-side bounded public model-free verification only

## 1. 수정 경계

이번 판본은 독립 심사에서 확인된 차단 결함 하나만 수정한다. v0.1 finalizer는
I2 completion event의 문법, route, class, 상태와 `H/Z`는 확인했지만, 호출자가
제공한 전역 sequence와 predecessor hash를 I2 lifecycle 검사에 전달하지 않았다.
그 결과 route-local 형식만 맞는 event가 전역 chain과 불일치해도 목적지 권한이
`available`이 될 수 있었다.

v0.2는 다음 두 공개 입력을 finalizer에 추가한다.

- `expected_sequence`
- `expected_previous_event_sha256`

event가 존재하고 append가 `persisted`일 때 기존 I2
`validate_event_global_link`를 호출한다. 두 입력이 없거나, 형식이 틀리거나,
event의 sequence/predecessor와 다르면 `no-completion-claim`으로 닫힌다. 정확한
accepted event와 정확한 전역 연결 증거와 persisted append가 모두 일치할 때만
기존 `consumed-accepted`와 목적지 권한 `available`을 반환한다.

## 2. 직접 수정한 공개 구현

- I3 finalizer의 I2 global-link 검증 재사용
- public contract 내부 판본 `0.2.0`과 finalizer 입력 목록 갱신
- package 판본 `0.2.0` 갱신
- 독립 심사 보고서 pair를 public source manifest에 추가
- sequence, predecessor, missing evidence 회귀시험 추가
- README, verifier와 인증 manifest 갱신

I2 파일, I3 분류 순서, 21/26/31 필드 문법, route mapping, `H/Z`, 매체 규칙,
닫힌 기능 경계는 변경하지 않았다.

## 3. 작성자 측 시험

공개 unit test는 다음을 포함한다.

- 기존 grammar, hash, binding, classification, finalization 전체 비회귀
- 정확한 sequence/predecessor evidence에서만 accepted authority 허용
- sequence 단독 변경 거부
- predecessor hash 단독 변경 거부
- 두 증거의 전체 또는 부분 누락 거부
- 독립 심사가 사용한 큰 sequence와 다른 predecessor event 거부
- wrong class, route, `H/Z`, state와 non-persisted append의 기존 거부 유지
- 닫힌 API의 `BLOCKED_NOT_EXECUTED` 유지

최종 공개 test method 수는 `26`개이며 실패·오류·skip은 모두 0이다. 동결
manifest 기반 I3 verifier에서 generator self-test, grammar/hash/binding,
classification, finalization, contract CLI, import audit, public-source integrity와
final stability가 모두 `PASS`였다. `CLOSED_BOUNDARIES`는
`BLOCKED_NOT_EXECUTED`를 유지했다.

별도 gap probe는 정확한 전역 link에서만 목적지 권한이 `available`이 되고,
심사에서 사용한 큰 sequence/다른 predecessor event와 증거의 전체·부분 누락이
모두 `no-completion-claim`이 되는 것을 확인했다. 기존 I2 verifier도 `38/38`
통과했고 I2 닫힌 경계는 실행되지 않았다.

## 4. 주장 제한

이 보고서는 작성자 측 공개 model-free 수정 검증이다. 실제 durable ledger,
witness, atomic append, registry authority, key/signature, VM 또는 sandbox,
provider/model, F0 내용, fixture/oracle, executor/judge, E0, S0, 중앙 시스템과
Project Brain은 구현하거나 실행하지 않았다.

최대 주장은 `I3-IIR-B01`의 공개 구현 수정 후보가 작성자 시험을 통과했다는
것뿐이다. finding closure와 CONTROL 통합 가능 여부는 fresh independent
implementation rereview가 별도로 판단해야 한다.
