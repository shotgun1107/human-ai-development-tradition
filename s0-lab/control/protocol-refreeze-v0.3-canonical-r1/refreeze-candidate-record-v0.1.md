# S0 프로토콜 v0.3 canonical document revision r1 재동결 후보 기록 v0.1

- `status`: `REFREEZE-CANDIDATE—CONTROL-VERIFIED`
- `gate`: `S0 V0.14 PUBLIC PROTOCOL CANONICALIZATION AND REFREEZE OPEN`
- `date`: `2026-08-10`
- `claim_kind`: 형식 수리 후보와 제한 재심사 입력만 준비됨
- `base_commit`: `21a63127b01559670cff8f3b494f642091fd9f79`
- `base_tree`: `02de94ed9fe76a5e8c3175da1a227981ed71739e`

## 1. 목적과 경계

이 기록은 동결된 `s0-protocol-v0.3.md`를 소급 수정하지 않고, 그 규칙
본문을 그대로 보존한 정규 형식 후속 문서
`s0-protocol-v0.3-canonical-r1.md`를 제한 재심사 후보로 고정한다. 의미상
프로토콜 버전과 `protocol_version` 값은 계속 `0.3`이며, `canonical-r1`은
문서 바이트 revision 이름이다.

이번 후보가 해결하려는 결함은 기존 문서 3–6행의 CommonMark two-space
hard break가 현재 canonical validator의 `TRAILING_WHITESPACE_ABSENT` 규칙과
충돌한 한 가지 형식 문제뿐이다. 프로토콜 규칙, 시험 설계, 권한, 역할,
입력, 출력, 판정, 재시도 또는 실행 게이트를 변경하지 않는다.

이 기록은 최종 재동결 승인, 기존 소비자의 자동 재결박, 구현, 시험자료,
숨은 정답, 모델 호출, E0 또는 S0 실행을 뜻하지 않는다.

## 2. 확인된 입력과 실패 증거

| 항목 | 값 |
|---|---|
| 동결 predecessor | `s0-lab/control/s0-protocol-v0.3.md` |
| predecessor SHA-256 | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| predecessor sidecar 파일 SHA-256 | `ffcd795bb94f78f69b404cb49955130c3bf4ae4fff12b026a1b3584cbd391963` |
| predecessor freeze record SHA-256 | `2a0e6c056ea60b872deb7cbba617be382d7e8ece96ddec63626681c42e6ae25a` |
| invalid review commit | `b98376d7935bc2ac1408dde296463d0cfadfae02` |
| invalid review SHA-256 | `e46dbafb983d9b235846384484f8e40d1a2c81f376b09e2be426cd559fe2bd02` |
| invalid review sidecar 파일 SHA-256 | `56f11635353e463840167ee8f2449809d3d121d9ffa2895158c17c50dd386ef9` |
| canonical validator SHA-256 | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |

기존 독립 심사는 모든 공급 SHA-256의 일치를 확인했지만 predecessor의
3–6행에 있는 후행 ASCII SP 때문에 canonical 형식 게이트에서
`INVALID-REVIEW`로 종료됐다. 따라서 trust-root/role-isolation 설계의
`TRI2-M01`과 `TRI2-m01`은 아직 본심사를 받지 않았다.

## 3. 새 후보와 정확한 변경

| 항목 | 값 |
|---|---|
| successor | `s0-lab/control/s0-protocol-v0.3-canonical-r1.md` |
| successor SHA-256 | `6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60` |
| successor byte count | `23,378` |
| 규칙 본문 시작 | `## 1. 입력과 변경 경계` |
| predecessor/successor 규칙 본문 SHA-256 | `41a8c212b36aa023747425e12ca28f800af71f228e001d5f20bb3c2ddae86b0b` |
| 규칙 본문 ordinal 비교 | `동일` |

새 판본의 변경은 제목과 제목 아래 거버넌스 메타데이터에만 한정된다.

1. 제목에 의미 버전 `v0.3`을 유지하면서 문서 revision `canonical r1`을
   명시했다.
2. 판본·기준일·상태를 새 정규 문서 후속 후보에 맞게 갱신했다.
3. 3–6행의 `SP SP` hard break를 후행 공백이 없는 `\` hard break로
   바꿔 렌더링 줄바꿈 의도를 유지했다.
4. `## 1. 입력과 변경 경계`부터 파일 끝까지는 predecessor와 UTF-8
   문자 및 바이트가 동일하다.

## 4. CONTROL 검증 사실

- validator SelfTest가 통과했다.
- predecessor는 UTF-8, BOM 없음, final LF, sidecar record와 artifact hash는
  통과하고 `TRAILING_WHITESPACE_ABSENT`만 실패한다.
- successor와 같은 이름의 sidecar는 validator의 모든 검사를 통과한다.
- successor에는 행 끝 ASCII SP 또는 HT가 없다.
- predecessor와 successor의 규칙 본문 SHA-256이 정확히 같다.
- 기존 `s0-protocol-v0.3.md`, sidecar, freeze record, 과거 비평·심사·실행
  기록은 수정하지 않았다.

위 항목은 CONTROL의 결정적 문서 검사 결과다. 독립 검토자의 판정이나
프로토콜 효과·구현 검증 결과가 아니다.

## 5. 결박과 마이그레이션 경계

구 SHA-256을 기록한 기존 문서·코드·manifest는 당시 predecessor 바이트에
대한 역사적 또는 기계적 결박으로 유지한다. 이번 후보는 그 값을 새
SHA-256으로 소급 치환하지 않는다.

특히 I0, I1, SM0, SM1, F0-PUBLIC, F0-SEALED와 public-practice 산출물은
자동으로 canonical-r1 소비자가 되지 않는다. 각 계층이 successor를 실제로
사용하려면 별도 버전, 영향 분석, 재동결과 해당 계층의 독립 검토가
필요하다. 현재 닫힌 실행·구현 게이트도 그대로 닫혀 있다.

## 6. CONTROL 판단과 남은 불확실성

CONTROL은 이 후보를 **제한 재심사에 제출 가능한 정규 형식 후속 후보**로
판단한다. 이 판단 근거는 규칙 본문 byte identity와 canonical validator
결과다.

아직 독립적으로 확인되지 않은 사항은 다음과 같다.

- 제목·메타데이터 변경이 새 판본 경계를 정확히 표현하는지
- `SP SP`에서 `\`로의 변경이 의도한 hard break만 보존하는지
- 기존 결박을 역사 기록으로 보존하고 후속 마이그레이션을 분리한 경계가
  누락 없이 실패 폐쇄적인지
- 이 후보를 최종 재동결해도 되는지

## 7. 다음 게이트

다음에 열 수 있는 최대 게이트는 다음 하나다.

`S0 V0.14 PUBLIC PROTOCOL V0.3 CANONICAL R1 LIMITED REREVIEW OPEN`

fresh 제한 재심사가 통과해도 허용되는 것은 별도 CONTROL 최종 재동결
판단뿐이다. trust-root/role-isolation v0.3 본심사 재개, 구현, 자료 제작,
provider/model 실행, E0 또는 S0 실행은 자동으로 열리지 않는다.

CONTROL 최종 재동결이 승인된 뒤에도 기존 trust-root/role-isolation v0.3
독립심사 brief는 predecessor 경로만 고정하므로, full 본심사 전에 별도
brief revision과 새 authenticated handoff가 필요하다. 이것은 기존 I0/I1,
SM 또는 F0 소비자 전체의 즉시 hash migration을 뜻하지 않는다.
