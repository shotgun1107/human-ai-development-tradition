# I2 공개 trust-root 및 역할 격리 구현 후보

이 디렉터리는 동결된 S0 v0.14 공개 설계의 기계 판독 가능 후속 후보만
구현한다. S0 실행, 실제 격리 환경, 키 생성, 원장·증인 제공자, 모델 호출,
E0 효과시험 또는 중앙 시스템 구현이 아니다.

## 구현 범위

- `S0-SIGNER-IMPORT-ADMISSION-2`의 정확한 21행 ASCII/LF codec
- `S0-SIGNER-IMPORT-OUTCOME-1`의 정확한 26행 codec, body hash와 2,048-byte
  raw-medium 분류
- `S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1`의 완전한 31행 codec
- 예약 `R`, 승인 고정 `A`, 대기 `P`, 완료 `C`의 route-local 수명주기
- 별도 원장·증인 관측값에 대한 global sequence/predecessor 검사
- 동결된 `TRI2-VEC-02` 네 행과 세 공개 증거 hash의 exact binding

전역 원장 연결 검사는 route-local 검사와 분리되어 있다. 호출자는 각 사건에
대해 `validate_event_global_link`를 통과시키고, 같은 사건 묶음에 대해
`validate_import_route`도 통과시켜야 한다. 어느 한쪽만으로 완료 권한이 생기지
않는다.

## 권한 경계

codec은 ASCII/LF 형식과 공개 결박을 검사할 뿐, 원장·증인·TCB·호스트를
신뢰할 수 있게 만들지 않는다. `classify_outcome_medium`은 이미 인증된
입장 승인 기록과 외부 host/anti-replay 일치 관측을 입력으로 받는다. 실제
매체 부착, 부팅, 종료, 내구성 있는 append와 cleanup은 구현하지 않는다.

`bind_frozen_tri2_vec_02`는 동결된 문서 hash와 정확한 네 행만 결박한다.
곡선 연산이나 암호 검증을 재실행하지 않으며, 철회된 `TRI2-VEC-01`을 받지
않는다.

## 현재 검증 상태

Python 3.12 표준 라이브러리로 모듈 import와 syntax 검사를 수행할 수 있다.
합성 단위시험 입력은 별도의 공개 unit-sentinel 게이트가 열리기 전에는 만들지
않는다. 따라서 현재 구현 후보는 단위시험 통과를 주장하지 않는다.

```powershell
$env:PYTHONPATH = 's0-lab/i2/implementation'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -c "import s0_i2; print(s0_i2.__version__)"
```

## 계속 닫힌 범위

봉인 자료, 실제 fixture, hidden oracle, protected material, API 키, provider,
모델 세션, 키·서명 생성, platform provisioning, acceptance 실행, E0와 S0는
이 후보에 포함되지 않는다. 운영 안전성, 경제성, A-D 공정성 또는 모델 간
전이 효과도 증명하지 않는다.
