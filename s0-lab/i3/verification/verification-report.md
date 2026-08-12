# I3 공개 import-decision implementation candidate v0.1 검증 보고서

- `date`: `2026-08-12 KST`
- `branch`: `codex/s0-i3-public-import-decision-contract-implementation-candidate`
- `base_commit`: `1472cd191b5c8a84dcab41a6107386997c75fd3c`
- `gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT IMPLEMENTATION CANDIDATE OPEN`
- `claim_kind`: author-side bounded public model-free verification only

## 1. 입력과 경계

후보는 I3 v0.2의 boundary, 네 설계 문서, zero-finding 독립 재심, CONTROL 결정,
main 통합 결정과 I2 v0.4 contract/implementation manifest를 공개 source로
고정한다. 기존 I2 파일은 수정하지 않고 exact parser, signer context,
route context와 lifecycle 분류기를 import해 재사용한다.

F0 53개 파일의 이름이나 내용을 읽지 않았다. hidden oracle, 실제 key,
protected material, 고객·개인 데이터, provider/model session과 S0 실행도 입력으로
사용하지 않았다.

## 2. 구현 결과

구현된 범위는 다음과 같다.

1. 21줄 admission의 canonical parse/serialize/hash
2. 26줄 outcome의 canonical parse/serialize/body hash/full-frame hash
3. 세 route mapping, 네 outcome tuple과 admission/outcome binding
4. 한 2,048-byte medium의 structural scan, candidate와 zero-tail 판정
5. pre-pending 2개와 pending 9개 row의 고정 우선순위
6. 단일 eager media sequence와 8개 closed status의 immutable fact set
7. canonical frame과 외부 불일치의 disagreement/`H`, 비canonical의
   disagreement/`Z`
8. 기존 I2 event와 exact route/class/hash/state를 비교하는 finalizer
9. persisted accepted completion에서만 목적지 availability 부여

분류 함수는 기존 I2의 authenticated `ImportRouteContext`를 명시적으로 받는다.
이 입력은 admission 부재 또는 손상 시에도 route와 `SRC/DST`를 추측하지 않기
위한 공개 구조 입력이다. 새 authority, store 또는 실환경 관측은 아니다.

## 3. 작성자 측 테스트

최종 manifest를 만들기 전 공개 unittest를 실행했다.

- test methods: `25`
- failures: `0`
- errors: `0`
- skips: `0`
- closed-enum Cartesian classifications: `78,732`

각 test method 안의 subtest와 deterministic loop가 admission 21필드,
outcome 26필드, 세 route, 네 tuple, identifier collision, byte/hash/binding 변이,
모든 분류 행, `H/Z`, status 변이와 finalization을 검사한다.

최초 실행에서는 두 full frame이 2,048바이트 안에 들어간다는 테스트 작성자의
잘못된 가정 때문에 test data 생성이 실패했다. 구현 결함은 아니었으며, 두 번째
schema prefix를 zero-tail 영역에 넣는 정확한 duplicate 사례로 수정했다. 이후
전체 suite가 통과했다.

## 4. 검증기 계약

`tools/verify-i3.ps1`은 다음 순서로 검증한다.

1. 외부 expected implementation-manifest SHA-256과 anchor 확인
2. 17개 I3 payload exact path/hash 확인
3. 19개 공개 source exact path/hash 확인
4. 고정된 I2 v0.4 implementation manifest와 payload 확인
5. 인증 payload만 임시 snapshot에 복사하고 재해시
6. synthetic generator self-test
7. Python `-B -S -P` unit tests
8. machine-readable contract CLI와 forbidden-import audit
9. 실행 후 I3/I2/source 원본 재해시와 snapshot 제거

최종 manifest/anchor를 만든 뒤 외부 pin으로 검증기를 다시 실행해야 한다.
검증기 자체의 bootstrap trust는 script 내부 자기검사로 만들 수 없으므로 실행
전 trusted copy 또는 외부 hash가 필요하다.

## 5. 닫힌 경계

다음은 구현하거나 실행하지 않았고 verifier도
`CLOSED_BOUNDARIES=BLOCKED_NOT_EXECUTED`로 보고해야 한다.

- durable ledger, witness, atomic append와 project-lifetime uniqueness
- 실제 registry/key/signature/anchor 권한
- hostile same-process, VM, sandbox, OS, network 또는 provider enforcement
- F0, protected fixture, hidden oracle, executor, judge, scoring과 statistics
- E0, S0, 중앙 시스템과 Project Brain

## 6. 최대 주장과 다음 단계

현재 결과는 작성자 측 공개 construction verification이다. I3 codec,
classification과 I2 completion 연결이 합성 공개 테스트를 통과했다는 것만
주장한다. 운영 보안, 실제 격리, 실험 효과 또는 S0 성공 증거가 아니다.

최대 다음 단계는 별도로 열린 fresh independent public implementation review다.
이 보고서나 작성자 테스트가 그 심사, CONTROL 결정 또는 main 통합을 자동으로
열지 않는다.
