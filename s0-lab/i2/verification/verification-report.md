# I2 공개 trust-root/role-isolation construction v0.3 검증 보고서

- `date`: `2026-08-11 KST`
- `branch`: `codex/s0-trust-root-role-isolation-public-implementation-v03`
- `base_commit`: `01a1430d29d3c87e9448d9370a404e60371f721d`
- `gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.3 REVISION OPEN`
- `claim_kind`: bounded public construction verification only

## 1. 입력 경계

후보는 `spec/public-source-files.sha256`에 고정한 공개 입력 12개만 source
authentication 대상으로 사용한다. 여기에는 채택된 v0.4 설계·CONTROL 결정·
authority matrix·acceptance plan·동결 vector 결정의 Markdown/sidecar 쌍과 기존
I1 public-runtime manifest/JSON이 포함된다.

F0-SEALED 내용, hidden oracle, protected material, fixture, 실제 key, provider 또는
model session은 읽거나 생성하거나 실행하지 않았다. F0 경로는 후보 source
manifest, implementation manifest, 테스트 및 verifier 입력에 포함되지 않는다.

## 2. 구현된 검증 범위

- exact 31-line ASCII/LF import-event parse, serialize 및 SHA-256
- canonical unsigned decimal과 arbitrary-length successor
- 세 route class의 `R/A/P/C` 구조와 두 early-terminal 및 여덟 post-pending
  completion 구조
- route-local predecessor와 호출자가 공급한 global predecessor/sequence 구조
- 단일 contiguous trace의 emitted event-ID 중복 거부
- 공급된 multi-route set에서 immutable route identity의 두 번째 출현 거부
- route별 `result_media_id`와 네 preallocated `R/A/P/C` ID, 총 다섯 식별자의
  단일 소유권 및 route 간 result/result, result/event, event/event 충돌 거부
- 공급된 multi-route set 전체의 emitted event-ID 중복 거부
- I1 public runtime manifest/JSON SHA-256, 22-role 순서, root 제외 21-role 식별자
  inventory 결박
- 동결 `TRI2-VEC-02` 네 행과 공개 evidence hash의 exact binding

## 3. 명시적으로 차단된 범위

현재 인증 입력에 완전한 ordered byte grammar가 없는 import admission/outcome과
complete outcome classification은 `UnsupportedBoundaryError`로 fail closed 한다.
실제 ledger durability, project-lifetime uniqueness, atomic append, witness,
registry authority, key/signature/curve 연산, VM·sandbox·ACL·network 집행,
provider/model, executor/judge/scoring, E0/S0도 구현하거나 실행하지 않았다.

Python provenance handle은 trusted same-process API discipline이며 적대적
same-process 코드에 대한 보안 경계가 아니다.

## 4. 작성자 측 검증

최종 source와 test delta 이후 공개 `unittest` suite를 한 번 실행했다.

- tests run: `37`
- failures: `0`
- errors: `0`
- skips: `0`

회귀 표면에는 세 route class와 모든 lifecycle variant, exact byte grammar 변이,
global/route chain 오류, forged/corrupt handle, preallocated-ID 교차 재사용,
early-terminal unused-ID 재사용, 동일 route의 모순된 종료 이력, route 간
result-media/result-media 및 result-media/event-ID 충돌, 역순 입력과
early-terminal 변형, I1 source 의미 결박 및 frozen vector mutation이 포함된다.

v0.2 독립 심사에서 다음 두 major finding이 확인됐다.

1. 같은 immutable route identity의 성공·실패 또는 복수 종료 이력이 한 supplied
   set에서 함께 허용됐다.
2. aggregate validator가 result-media ID를 소유권 map에 등록하지 않아 route 간
   result/result 및 result/event 충돌이 허용됐다.

v0.3은 route identity를 set당 정확히 한 번으로 제한하고, 각 route의 result-media
ID와 네 event ID를 하나의 다섯-ID ownership map에 등록한다. 공급된 모든 route의
emitted event ID도 별도 set으로 재검사한다. 동일 이력, 모순 종료, 두 completion,
역순 충돌, early-terminal 변형을 hostile regression으로 추가했다. 이 검증은
작성자 측 보조 검증이며 독립 심사 증거가 아니다.

## 5. 최종 verifier 계약

`tools/verify-i2.ps1`은 다음 순서로 동작한다.

1. 외부 lowercase implementation-manifest SHA-256과 저장소 anchor의 일치 확인
2. I2 exact file set, plain-file/reparse/device 및 payload hash 확인
3. 공개 source manifest의 정확한 12행 allowlist와 실제 source hash 확인
4. 인증된 bytes만 임시 snapshot에 복사하고 다시 해시
5. Python `-B -S -P`, user-site 차단 상태에서 unit tests, contract CLI 및
   forbidden-import audit 실행
6. snapshot과 원본 namespace/source를 실행 후 재열거·재해시
7. 임시 snapshot 제거

검증기 자체의 bootstrap trust는 이 내부 절차가 만들지 않는다. 실행 전 trusted
copy 또는 별도 외부 hash 인증이 필요하다.

최종 manifest/anchor가 만들어진 뒤 다음 명령의 성공으로 이 exact candidate를
확인한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File s0-lab/i2/tools/verify-i2.ps1 `
  -ExpectedManifestSha256 <implementation-manifest-sha256>
```

필수 machine-readable 결과는 `STATIC_INTEGRITY=PASS`,
`PUBLIC_SOURCE_INPUTS=PASS`, `UNIT_TESTS=PASS`, `CONTRACT_CLI=PASS`,
`FORBIDDEN_IMPORT_AUDIT=PASS`, `FINAL_STABILITY=PASS`이며,
`CLOSED_BOUNDARIES=BLOCKED_NOT_EXECUTED`가 함께 유지되어야 한다.

이 보고서는 자기 자신을 포함하는 최종 manifest의 verifier 결과를
자기참조적으로 기록하지 않는다. 최종 anchor와 그 pin으로 실행한 외부 verifier
결과를 함께 사용한다.

## 6. 최대 허용 주장

최대 주장은 인증된 공개 입력에 한해 I2 v0.3의 byte codec, 구조적 lifecycle,
공급 범위 ID 충돌, I1 공개 inventory 결박 및 frozen vector binding이 model-free
construction tests를 통과했다는 것이다.

실제 trust root, role isolation, key custody, durable ledger/witness, S0 효과,
E0 효과, 중앙 시스템, Project Brain, 운영 안전성 또는 경제성은 구현·실행·
검증됐다고 주장할 수 없다. 다음 단계는 별도 공개 구현 독립 심사 게이트이며,
이 후보의 성공이 그 심사나 후속 platform 구현을 자동으로 열지 않는다.
