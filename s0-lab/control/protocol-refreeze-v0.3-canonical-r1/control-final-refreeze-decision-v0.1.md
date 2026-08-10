# S0 공개 프로토콜 v0.3 canonical-r1 CONTROL 최종 재동결 결정 v0.1

- `status`: `CONTROL-FINAL-REFREEZE-APPROVED`
- `current_gate`: `S0 V0.14 PUBLIC PROTOCOL V0.3 CANONICAL R1 CONTROL FINAL REFREEZE DECISION OPEN`
- `decided_at`: `2026-08-10 Asia/Seoul`
- `decision_role`: `S0 CONTROL`
- `decision_kind`: 공개 문서 바이트 판본의 최종 재동결
- `semantic_protocol_version`: `0.3`
- `canonical_document_revision`: `canonical-r1`
- `decision_input_commit`: `e32df2b64b8cb4427e0084b05c6be88d74896c3c`
- `decision_input_tree`: `54077ea6ec7108b47d89baeffe4a7c9a6bff8ca0`
- `reviewed_candidate_commit`: `114e8a9260a724288f72d270b4e04453780f6e8a`
- `reviewed_candidate_tree`: `2a1f6ada61a9518e256b20a9af39d1ad09a07d03`

## 1. CONTROL 결정

CONTROL은 다음 결정을 내린다.

1. `s0-protocol-v0.3-canonical-r1.md`와 그 same-basename sidecar를 S0 공개
   프로토콜 v0.3의 **최종 재동결된 canonical 문서 판본**으로 승인한다.
2. 프로토콜의 의미 버전은 계속 `0.3`이다. `canonical-r1`은 규칙의 새
   의미 버전이 아니라 문서 바이트 형식의 revision 이름이다.
3. 이 문서와 sidecar 한 쌍은 별도 freeze record를 중복 생성하지 않고도
   canonical-r1 최종 재동결을 선언하는 권위 있는 CONTROL 결정 기록이다.
4. predecessor인 `s0-protocol-v0.3.md`, 그 sidecar, 기존 freeze record와
   이들을 입력으로 사용한 역사 기록은 수정하거나 소급 대체하지 않는다.
5. 기존 I0, I1, SM0, SM1, F0-PUBLIC, F0-SEALED 및 public-practice 소비자의
   해시 결박은 자동으로 canonical-r1으로 이동하지 않는다.
6. 이 결정 이후 새로 여는 공개 설계·심사 gate에서 프로토콜 v0.3의 현재
   canonical 바이트 문서가 필요하면 canonical-r1 pair를 사용한다. 다만
   역사 재현이나 기존 결박 감사처럼 predecessor가 명시된 범위는 그대로
   predecessor를 사용한다.

**최종 판정: `APPROVE-FINAL-REFREEZE`**

## 2. Git 계보와 변경 범위

| 항목 | commit | tree |
|---|---|---|
| canonical-r1 후보의 parent | `21a63127b01559670cff8f3b494f642091fd9f79` | `02de94ed9fe76a5e8c3175da1a227981ed71739e` |
| canonical-r1 후보 | `114e8a9260a724288f72d270b4e04453780f6e8a` | `2a1f6ada61a9518e256b20a9af39d1ad09a07d03` |
| 독립 제한 재심사 결과 | `e32df2b64b8cb4427e0084b05c6be88d74896c3c` | `54077ea6ec7108b47d89baeffe4a7c9a6bff8ca0` |

계보 감사에서 다음을 확인했다.

- candidate parent에서 candidate까지의 tracked diff는 canonical protocol,
  refreeze candidate record, limited-rereview brief의 세 pair, 정확히 6개
  공개 파일 추가뿐이다.
- candidate에서 review commit까지의 tracked diff는 독립 제한 재심사 pair,
  정확히 2개 공개 파일 추가뿐이다.
- predecessor protocol pair와 freeze record는 위 두 diff에서 변경되지 않았다.
- 제한 재심사 출력은 독립 검토자가 산출한 정확한 바이트와 SHA-256을 CONTROL이
  지정 경로에 보존한 뒤 공식 validator로 다시 검증한 기록이다. 검토자의 최초
  직접 쓰기가 작업 경로 권한 때문에 거부됐다는 사실도 역사 기록에 남긴다.

## 3. 최종 재동결 입력

아래 표의 `sidecar SHA-256`은 sidecar 안에 적힌 artifact hash가 아니라
sidecar 파일 자체의 SHA-256이다.

| 입력 pair | artifact/Markdown SHA-256 | sidecar 파일 SHA-256 |
|---|---|---|
| predecessor protocol v0.3 | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | `ffcd795bb94f78f69b404cb49955130c3bf4ae4fff12b026a1b3584cbd391963` |
| canonical-r1 protocol | `6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60` | `88d8bcaf7e2b9c14fe71a267cbc19c4a21c4c003187348a3cf6dc323e618a3f3` |
| refreeze candidate record | `d9b1179a8337410800756a77acbcef763abf2a751efe0bd4d7d8338b0dd9705d` | `06700485c0cc9be616ab11860261a5ec3873421d5f4e99f53064b5ef7c9ed725` |
| limited-rereview brief | `c34c2f5e36c735b24ee29aaad6bfb092f19d343a27b5981339f8e1a998de12e5` | `94014e2dfb14525b8d31c7e05516279676fc1d49e513564a545554fb9a6eaceb` |
| independent limited rereview | `e10813ad559e9ea66f3c197a0a9b99649d4d68e9f5b475eee1a8395dd796dbaf` | `d47178efc71641a34c7a1fcbcfbc0a580491a26393c4c62316c30074de1d7da5` |

모든 지정 artifact와 sidecar의 실제 SHA-256은 공급된 값과 일치했다.

## 4. canonicalization 증거

CONTROL이 수용한 사실은 다음과 같다.

- 인증된 validator의 SelfTest 11개 사례가 모두 `PASS`였다.
- predecessor의 형식 실패를 다시 재현했다. UTF-8, BOM 없음, final LF와
  sidecar record/hash는 통과했지만 3–6행의 terminal ASCII space 때문에
  `TRAILING_WHITESPACE_ABSENT`가 실패했다.
- canonical-r1 protocol, candidate record, rereview brief 및 independent
  rereview의 각 pair는 UTF-8, BOM 없음, final LF, terminal SP/HT 없음,
  canonical sidecar record와 artifact hash 검사를 모두 통과했다.
- predecessor와 canonical-r1 사이의 실제 문서 변경은 제목 1행과 metadata
  3–6행뿐이다.
- `## 1. 입력과 변경 경계`부터 EOF까지 두 문서의 본문은 정확히 22,964
  bytes이며 byte-for-byte 동일하다.
- 동일한 본문 slice의 SHA-256은
  `41a8c212b36aa023747425e12ca28f800af71f228e001d5f20bb3c2ddae86b0b`이다.
- canonical-r1은 23,378 bytes이고, 3–6행은 CommonMark의 backslash-newline
  hard break를 사용해 표시 의도를 보존하면서 terminal space를 제거했다.

이 증거는 문서 형식 수리와 본문 비회귀를 지지한다. 프로토콜의 실효성,
구현 정확성 또는 S0 효과를 증명하지는 않는다.

## 5. 독립 제한 재심사 수용

독립 제한 재심사는 canonicalization과 비회귀라는 좁은 범위에서 다음을
보고했다.

- `BLOCKING`: 0건
- `MAJOR`: 0건
- `MINOR`: 0건
- 총 finding: 0건
- 판정: `PASS-FOR-CONTROL-FINAL-REFREEZE-CONSIDERATION-ONLY`

CONTROL은 이 결과를 최종 재동결 결정의 독립 근거로 수용한다. 이 수용은
reviewer가 최종 재동결 권한을 행사했다는 뜻이 아니다. 최종 승인 책임은
이 결정의 CONTROL에 있다.

## 6. 유지되는 역사 기록과 미완료 심사

이전 trust-root/role-isolation v0.3 독립 심사의 `INVALID-REVIEW` 판정은
삭제하거나 합격으로 고쳐 쓰지 않는다. 당시 허용 입력인 predecessor
protocol이 canonical validator를 통과하지 못했으므로 심사가 성립하지
않았다는 역사적 사실로 유지한다.

따라서 그 심사에서 수행되지 않은 다음 작업도 여전히 미완료다.

- v0.1 + v0.2 + v0.3 trust-root/role-isolation 유효 구성의 full reconstruction
- `TRI2-M01` observable import outcome 수리의 독립 판단
- `TRI2-m01` order-eight vector provenance 수리의 독립 판단
- 전체 hostile tabletop cases와 비보상 판정

canonical-r1 최종 재동결은 위 본심사를 대신하거나 그 결과를 미리 정하지
않는다.

## 7. 비이행과 닫힌 gate

이번 결정으로 허용되지 않는 것은 다음과 같다.

- 기존 소비자와 역사 문서의 predecessor hash를 일괄 교체하는 작업
- downstream manifest, registry, fixture 또는 실행 입력의 자동 migration
- trust-root/role-isolation v0.3 전체 설계 통과 주장
- VM, sandbox, account, network, ACL, vault, signer, store 또는 ledger 구축
- 키·anchor·registry·signature·cryptographic vector 생성이나 실행
- sealed material, hidden oracle, fixture, bank, label 또는 condition map 작성
- provider/model session, executor, judge, scoring 또는 통계 실행
- E0 또는 S0 실행
- 중앙 시스템이나 Project Brain 연동 구현
- 운영 안전성, 경제성 또는 모델 간 전이가 검증됐다는 주장

기존 I0, I1, SM0, SM1, F0-PUBLIC, F0-SEALED와 public-practice의 hash 결박을
바꾸려면 각각 별도의 영향 분석, version 결정, 재동결과 독립 검토가 필요하다.

## 8. 다음 최대 gate

이 결정 다음에 열 수 있는 최대 범위는 다음 하나다.

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION INDEPENDENT REREVIEW BRIEF REVISION OPEN`

그 gate의 범위는 canonical-r1 pair, 이 최종 재동결 결정 pair와 독립 제한
재심사 pair를 허용 입력으로 명시하도록 full-review brief와 authenticated
handoff 기준을 수정·동결하는 데 한정한다. trust-root/role-isolation full
independent rereview 자체는 자동으로 열리지 않으며 별도의 정확한 사용자
승인이 필요하다.

downstream migration, 구현, protected material, provider/model session,
E0와 S0 gate는 계속 닫혀 있다.
