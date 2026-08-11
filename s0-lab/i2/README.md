# I2 공개 trust-root/role-isolation construction candidate v0.3

이 디렉터리는 CONTROL에 채택된 S0 v0.14 trust-root/role-isolation v0.4
공개 설계에서, 현재 인증된 공개 입력만으로 기계적으로 구현할 수 있는 최소
범위를 담는다. 결과는 공개 construction candidate이며 실제 역할 격리 환경,
신뢰 루트, 원장 또는 S0 실행 결과가 아니다.

기존 `s0-lab/i1/**`는 변경하지 않는다. I2는 I1의 동결된 공개 runtime JSON과
manifest의 정확한 SHA-256을 별도 입력으로 인증하고, 그 안의 22개 signer ID
순서 및 root를 제외한 21개 public signer 식별자만 재사용한다. 이 결박은 공개
식별자 inventory 검증일 뿐 실제 registry 권한이나 key custody가 아니다.

## 구현된 공개 범위

- `S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1`의 정확한 31필드 ASCII/LF
  `name=value` codec과 SHA-256
- 문서에 없는 자릿수 상한을 추가하지 않은 canonical unsigned decimal
- 세 import route class의 `R/A/P/C` lifecycle tuple 및 route-local predecessor,
  binding, ID 중복 검증
- 호출자가 제공한 global sequence와 predecessor hash의 구조적 검증
- 공급된 단일 trace와 multi-route set의 emitted event ID 중복 검출
- 공급된 multi-route set에서 immutable route identity의 두 번째 출현 거부
- 각 route가 소유한 `result_media_id`와 네 preallocated `R/A/P/C` ID, 총 다섯
  식별자의 route 간 단일 소유권 및 교차 충돌 검증
- 동결된 `TRI2-VEC-02`의 네 행, 순서, 공개 증거 hash에 대한 exact binding
- public contract, I1 public runtime 및 source hash에 대한 fail-closed 인증

이 검증은 공급된 bytes와 trace의 구조만 판정한다. 공급된 set 안에서 같은
immutable route identity는 정확히 한 번만 존재할 수 있고, 각 route의 결과 매체
ID와 네 event ID는 다른 route의 다섯 ID 어느 것과도 겹칠 수 없다. 따라서 같은
route의 성공·실패 이력 중복이나 result-media/result-media,
result-media/event-ID 충돌은 거부한다. 실제 project-lifetime 원장, 원자 append,
rollback-resistant witness 또는 appliance 상태를 관찰하지 않으며 그런 결과를
주장하지 않는다.

Python의 frozen dataclass와 module-private provenance marker는 신뢰된 same-process
호출자에게 제공하는 API discipline이다. 악성 same-process 코드의 introspection,
임의 object 구성 또는 메모리 변조를 막는 보안 경계가 아니다. 실제 공격자
격리는 후속 process/VM 구현 게이트에서 검증해야 한다.

## 명시적으로 차단된 경계

현재 허용된 v0.4 입력에는 `S0-SIGNER-IMPORT-ADMISSION-2`와
`S0-SIGNER-IMPORT-OUTCOME-1`의 완전한 ordered byte grammar가 없다. 따라서
I2는 두 문법을 추측해 구현하지 않고, complete import/outcome validation 요청을
명명된 `BLOCKED` 오류로 거부한다. 구조적으로 가능한 post-pending event를
만들거나 검사하는 것은 outcome frame의 의미, 유일성 또는 수용을 증명하지
않는다.

다음 기능도 이 후보에 없다.

- 실제 key 생성, Ed25519 연산, 서명·검증, anchor 또는 registry activation
- private-key custody, 실제 ledger/witness provider, atomicity 또는 durability
- VM, sandbox, OS account, ACL, network, clipboard 또는 Git 격리 집행
- provider/model session, executor, judge, scoring 또는 통계
- fixture, protected material, hidden oracle 또는 F0 내용
- E0/S0 실행, 중앙 전통 시스템 또는 Project Brain 구현

## 검증

검증기는 외부에서 고정한 lowercase implementation-manifest SHA-256을 요구한다.
먼저 공개 source manifest와 I2 exact file set을 PowerShell에서 인증하고, 인증한
bytes만 별도 임시 snapshot으로 복사한 뒤 Python 3.12 이상에서 unit tests,
contract CLI 및 forbidden-import audit을 실행한다. 마지막에는 원본 namespace를
다시 열거·해시해 실행 전후가 같은지 확인하고 snapshot을 제거한다.

검증기 script 자체는 실행 전에 trusted copy 또는 별도의 외부 SHA-256으로
인증되어야 한다. 실행 중 script의 hash를 payload manifest와 대조하는 일은 이미
실행을 시작한 bootstrap code의 신뢰 근거를 스스로 만들지 못한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File s0-lab/i2/tools/verify-i2.ps1 `
  -ExpectedManifestSha256 <64-lowercase-hex>
```

검증기의 성공은 `STATIC_INTEGRITY`, `PUBLIC_SOURCE_INPUTS`, `UNIT_TESTS`,
`CONTRACT_CLI`, `FORBIDDEN_IMPORT_AUDIT`, `FINAL_STABILITY`를 별도로 보고한다.
`CLOSED_BOUNDARIES`는 계속 `BLOCKED_NOT_EXECUTED`로 보고되어야 한다. 이
construction 검증 결과를 operational isolation, cryptographic correctness 또는
S0 성공으로 해석하면 안 된다.
