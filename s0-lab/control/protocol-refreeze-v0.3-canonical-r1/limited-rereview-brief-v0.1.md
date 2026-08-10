# S0 프로토콜 v0.3 canonical document revision r1 제한 재심사 brief v0.1

- `status`: 독립 제한 재심사 입력 후보
- `review_kind`: fresh public-only canonicalization rereview
- `review_scope`: v0.3 predecessor에서 canonical-r1 문서 revision으로의 형식 경계와 비회귀만 검토
- `claim_kind`: CONTROL 최종 재동결 고려 가능 여부만 판정

## 1. 독립성

검토자는 canonical-r1 프로토콜 문서, 재동결 후보 기록 또는 이 brief를 작성·조언하지
않은 fresh 세션이어야 한다. 다른 검토자 결론을 상속하거나 읽지 말고,
subagent를 사용하지 않는다.

검토자는 이전 trust-root/role-isolation v0.3 `INVALID-REVIEW`를 답안으로
읽지 않는다. 아래 predecessor 파일에 canonical validator를 직접 적용해
동일한 형식 결함을 재현한다.

별도 clean worktree를 정확한 후보 commit에 만들고 입력을 read-only로
유지한다. worktree 분리는 편집 격리일 뿐 비밀 또는 독립 정보 보안이
아니다.

## 2. 최대 허용 입력

CONTROL은 후보 commit·tree와 아래 파일의 정확한 SHA-256을 공급해야 한다.
허용 목록은 최대치이며, 그 밖의 저장소 파일을 검색하거나 읽지 않는다.

1. `s0-lab/control/tools/verify-text-artifacts.ps1`
   - SHA-256 `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3`
2. `s0-lab/control/s0-protocol-v0.3.md`
   - SHA-256 `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c`
3. `s0-lab/control/s0-protocol-v0.3.sha256`
   - 파일 SHA-256 `ffcd795bb94f78f69b404cb49955130c3bf4ae4fff12b026a1b3584cbd391963`
4. `s0-lab/control/s0-protocol-v0.3-freeze-record.md`
   - SHA-256 `2a0e6c056ea60b872deb7cbba617be382d7e8ece96ddec63626681c42e6ae25a`
5. `s0-lab/control/s0-protocol-v0.3-freeze-record.sha256`
   - 파일 SHA-256 `a7d1e0a62372bce6d493926e112cce07bb78e28b4e2bb20a3485becf9edb4806`
   - canonical record가 위 freeze-record hash와 basename을 고정해야 한다.
6. `s0-lab/control/s0-protocol-v0.3-canonical-r1.md`
   - SHA-256 `6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60`
7. `s0-lab/control/s0-protocol-v0.3-canonical-r1.sha256`
   - 파일 SHA-256 `88d8bcaf7e2b9c14fe71a267cbc19c4a21c4c003187348a3cf6dc323e618a3f3`
8. `s0-lab/control/protocol-refreeze-v0.3-canonical-r1/refreeze-candidate-record-v0.1.md`
   - SHA-256 `d9b1179a8337410800756a77acbcef763abf2a751efe0bd4d7d8338b0dd9705d`
9. 위 후보 기록의 same-basename `.sha256`
   - 파일 SHA-256 `06700485c0cc9be616ab11860261a5ec3873421d5f4e99f53064b5ef7c9ed725`
10. 이 brief와 same-basename `.sha256`
    - CONTROL이 동결 후 정확한 SHA-256을 공급한다.

sealed 자료, oracle, fixture, bank, label, condition map, executor output,
E0, 구현 코드, provider/model 출력과 unlisted 문서는 금지한다. 웹이나 외부
자료도 사용하지 않는다.

## 3. 읽기 전용 검토 경계

허용되는 실행은 SHA-256 계산, validator SelfTest와 지정 문서 검증, byte와
text diff, Git baseline·허용 diff 확인뿐이다. VM·sandbox·계정·network·key,
fixture·oracle·package·script·helper·model call 또는 acceptance harness를
만들거나 실행하지 않는다.

검토자는 지정된 review Markdown과 same-basename sidecar만 작성할 수 있다.
후보를 수정하거나 commit, push, merge, PR 또는 구현 준비를 하지 않는다.

## 4. 필수 재구성

다음을 author 기록의 결론을 신뢰하지 않고 직접 재구성한다.

1. 후보 branch가 CONTROL이 공급한 정확한 commit·tree이며 시작 status가
   clean인지 확인한다.
2. 모든 허용 입력을 읽기 전에 SHA-256으로 인증한다.
3. validator SelfTest가 통과하는지 확인한다.
4. predecessor pair의 검사 결과가 다음과 정확히 같은지 확인한다.
   - UTF-8, BOM 없음, final LF, sidecar record, artifact hash: `PASS`
   - 3–6행의 각 ASCII SP 2자 때문에 trailing whitespace와 overall: `FAIL`
   - 그 밖의 trailing SP 또는 HT: 없음
   - predecessor freeze record pair는 당시 동결을 인증하는 역사 증거이므로
     hash와 sidecar record만 확인하고 current canonical-pass 대상으로
     재해석하지 않음
5. successor pair와 후보 기록 pair, 이 brief pair가 validator의 모든
   검사를 통과하는지 확인한다.
6. predecessor와 successor의 `## 1. 입력과 변경 경계`부터 EOF까지가
   ordinal byte-identical하고 SHA-256이 모두
   `41a8c212b36aa023747425e12ca28f800af71f228e001d5f20bb3c2ddae86b0b`인지
   확인한다.
7. successor의 변경이 제목·거버넌스 메타데이터에만 있고, 3–6행의
   terminal `\`가 후행 공백 없이 hard break를 명시하는지 확인한다.
   의미상 프로토콜 버전과 본문 `protocol_version`은 계속 `0.3`이며
   `canonical-r1`이 문서 revision 이름인지 확인한다.
8. predecessor protocol, sidecar, freeze record와 모든 기존 소비자·역사
   기록이 후보 diff에서 변경되지 않았는지 확인한다.
9. 후보가 기존 I0, I1, SM0, SM1, F0 또는 public-practice 결박을 새 hash로
   자동 치환하거나 실행 권한을 부여하지 않는지 확인한다.

## 5. 필수 적대 사례

적어도 다음 변형을 문서상 추적한다.

- predecessor를 직접 덮어쓰거나 기존 freeze record를 소급 수정함
- successor 규칙 본문에서 문자, 공백, 줄바꿈 또는 순서를 하나라도 바꿈
- successor에 BOM, final LF 누락, trailing SP/HT 또는 잘못된 sidecar가 있음
- `\`가 literal text로 노출되거나 의도한 hard break를 만들지 못함
- 새 hash를 역사 기록·코드·manifest에 일괄 치환해 기존 증거를 재해석함
- 새 판본을 최종 재동결, 구현 승인 또는 S0 실행 승인으로 주장함
- 허용 목록 밖 자료나 이전 reviewer 결론에 의존함

처리되지 않거나 둘 이상으로 해석되는 사례가 하나라도 있으면 통과할 수
없다.

## 6. 비보상 통과 기준

다음 항목은 하나도 빠짐없이 충족해야 한다.

- 입력·baseline·독립성·validator SelfTest가 모두 유효함
- predecessor 결함이 정확히 재현됨
- successor와 새 제어 문서가 canonical validator를 통과함
- 규칙 본문 byte identity가 독립적으로 재현됨
- 새 판본 경계와 hard-break 치환이 형식 수리로 한정됨
- 기존 파일과 소비자 결박에 변경이 없음
- 구현·실행·최종 재동결을 주장하지 않음

한 항목의 강점으로 다른 항목의 실패를 상쇄할 수 없다.

## 7. 허용 판정

아래 우선순위를 위에서 아래로 적용해 정확히 하나만 반환한다.

1. `INVALID-REREVIEW`: reviewer 독립성·허용 입력 경계, CONTROL이 공급한
   candidate commit/tree, 입력 파일 존재·hash 또는 validator SelfTest가
   실패해 심사 자체가 성립하지 않음
2. `REVISE-AND-REREVIEW`: 심사는 유효하게 성립했지만 successor 내용,
   sidecar, exact diff, 본문 동일성, 판본·migration·claim 경계에서 finding이
   하나라도 있음
3. `PASS-FOR-CONTROL-FINAL-REFREEZE-CONSIDERATION-ONLY`: 위 두 판정에
   해당하지 않고 finding 0건이며 모든 비보상 기준 충족

통과 판정도 CONTROL 최종 재동결을 자동 승인하지 않는다.

## 8. 필수 출력

다음 두 파일만 작성한다.

- `s0-lab/reviews/protocol-refreeze-v0.3-canonical-r1/limited-rereview-v0.1.md`
- `s0-lab/reviews/protocol-refreeze-v0.3-canonical-r1/limited-rereview-v0.1.sha256`

review에는 독립성, commit·tree, 모든 입력 hash, validator 결과, exact diff,
규칙 본문 비교, 적대 사례 처리, finding, 판정, 최대 주장과 다음 gate를
기록한다. sidecar는 canonical 단일 record여야 한다.

어떤 판정도 trust-root/role-isolation 본심사, 구현, protected material,
provider/model session, E0 또는 S0 실행을 열지 않는다.

CONTROL 최종 재동결이 따로 승인되면 full trust-root/role-isolation 본심사
전에 기존 v0.3 independent-review brief를 새 canonical-r1 pair와 refreeze
증거를 허용하도록 별도 revision해야 한다. 이 제한 재심사는 그 full-review
brief revision이나 downstream 소비자 migration을 대신하지 않는다.
