# 집→회사 CONTROL 상태 인수인계 v0.1

- `date_kst`: `2026-08-12`
- `repository`: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- `handoff_branch`: `codex/home-to-company-handoff-20260812`
- `handoff_payload_parent`: `179dd6f76f2709881900a42dc32cbde8c33c33b0`
- `handoff_payload_parent_tree`: `86bd304b06180c304f0e09ae5ecd0f0d7019e25a`
- `recorded_origin_main`: `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`
- `active_baseline`: `central-system-v2.1-s0-preparation`
- `claim_kind`: public CONTROL handoff only

## 1. 목적과 정본

이 문서는 2026-08-12 집 PC에서 수행한 공개 CONTROL 작업을 회사 PC의 기존
CONTROL 작업에 넘긴다. 회사 PC는 대화 기억이나 branch 이름을 정본으로 삼지
않고, 채팅으로 전달된 exact final handoff commit/tree와 현재 Git 상태, 최신
`AGENTS.md`, 이 문서 및 sidecar를 인증해야 한다.

최종 handoff commit은 이 문서 자신을 포함하므로 그 commit과 tree는 문서 안에
자기 참조로 기록하지 않는다. 커밋·푸시 뒤 사용자가 전달하는 시작 프롬프트의
exact final values가 정본이다.

## 2. 과거 — 회사에서 받은 기준선

집 CONTROL은 회사→집 handoff branch
`codex/company-to-home-handoff-20260812`의 exact tip
`f7048e919ab0e698d78ca4ff4cc4eb31ca6f612c`를 인증해 이어받았다.

그 계보에는 다음 공개 상태가 포함돼 있었다.

- main: `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`
- I0-I3 readiness audit:
  `f44b1d51670d34c86698ede692029feb0b7cb9f4`
- readiness audit verdict:
  `READY-FOR-PUBLIC-ASSEMBLY-REHEARSAL-DESIGN`,
  `NOT-READY-FOR-SEALED-S0`
- readiness audit artifact SHA-256:
  `0ca3e51e8a566a94ed168325d18f5fe6196a132de5c4c6979c8ab7348483ffbf`

감사의 핵심 결론은 I0-I3 각 공개 부품은 승인 계보를 갖지만, 이들을 한 흐름으로
조립한 공개 model-free rehearsal이 없다는 것이었다. 새 저수준 보안 계층을 더
만들기보다 먼저 최소 공개 조립 흐름을 설계해야 했다.

## 3. 오늘 집에서 완료한 공개 작업

### 3.1 조립 rehearsal 설계 v0.1

- branch: `codex/s0-public-assembly-rehearsal-design-v01`
- commit: `49ecc05dacebf043ed8b2b479eb021018d4b4fe6`
- design artifact SHA-256:
  `67a49650219b7587f2698c869336f8a767c55a787235c379b643268a9ec2879a`

설계는 공개 `BLK-PRACTICE0002 / P01` 사례에 대해 I0 변환, I1 one-shot stub,
I0 답변 검증과 결정론적 실행 기록을 연결했다. I2/I3는 실제 signer-media import가
없는 공개 저장소 사례이므로 exact contract preflight와 명시적 non-applicable
disposition만 허용했다.

구현, rehearsal 실행, provider/model, F0 내용, executor, judge 또는 S0는 열지
않았다.

### 3.2 v0.1 독립 심사

- branch: `codex/s0-public-assembly-rehearsal-design-v01-review`
- commit: `571c8751d0abb8acfb853d402c072fdb7667bde7`
- verdict: `REVISE-AND-REVIEW`
- findings: blocking 3, major 4, minor 0
- review SHA-256:
  `9bb097acba46bfcfd6eee88ffbf0e41709f371f08fbd2226f6bdb86b615f95dd`

발견된 핵심은 I0 full-bundle traversal과 allowlist 충돌, I1 first-final API가
generic trailing frame을 볼 수 없다는 점, read-back 실패 뒤 pass-looking final이
남을 수 있다는 점, 그리고 grant/record/call-accounting/failure-class 정확성
부족이었다.

### 3.3 조립 rehearsal 설계 v0.2 수정

- branch: `codex/s0-public-assembly-rehearsal-design-v02`
- commit: `18a9562a9da48ce5743fc183c8c68c15d00cf249`
- design SHA-256:
  `70b0a29327dc73a9b5268ea6146ecfe7e82c2709c856190a531c3a338e065475`
- interface-map SHA-256:
  `31417e75f5f4e40e12fea02cbd21b4d1a0908e938f911b75f34ee773a6c50f76`
- acceptance-plan SHA-256:
  `d68d83d234a158952333a580404207b871f9dd0de1bc28870eb37e016a191edf`

v0.2에서 다음을 고정했다.

- I0가 실제 읽는 public-practice bundle manifest와 90개 공개 row 전체 allowlist
- request `7,917 bytes`, SHA-256
  `990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2`
- I1 one-row request manifest `135 bytes`, SHA-256
  `872f2bca8d2d56c9b664e37ad6092a4dd4d8750d40eb8ba99dfbad7f7c94c9f7`
- exact manifest path, request path, entry prefix, purpose와 grant identity inputs
- generic I1 trailing-frame claim을 제거하고 candidate-owned stub `close()`의
  scripted-frame exhaustion만 검증
- 성공 record 36 fields, `2,046 bytes`, SHA-256
  `bc13615933766fd84435fe4faf2d05b37a495b160f8529c699c73aec7784650e`
- pending record를 검증한 뒤 final path로 publish하는 commit discipline
- ten-state flow와 실제 stub entry에 기반한 zero/one-call accounting
- 9개 stable failure class

### 3.4 v0.2 독립 심사

- branch: `codex/s0-public-assembly-rehearsal-design-v02-review`
- commit: `179dd6f76f2709881900a42dc32cbde8c33c33b0`
- tree: `86bd304b06180c304f0e09ae5ecd0f0d7019e25a`
- verdict: `REVISE-AND-REVIEW`
- findings: blocking 0, major 4, minor 0
- review SHA-256:
  `c7b31be05274bb87442550c8a5790e4737d5da7d937d3d7e2f22f6d743bde6fd`

독립 재구성에서 request, manifest, I1 grant identity와 성공 record의 bytes/hash는
모두 일치했다. v0.1의 B-01, B-02, B-03, M-01, M-02, M-03은 proposal-text
수준에서 닫혔다.

남은 major는 다음 네 건이다.

1. `M-04`: final-path 충돌 시점, stub close/counter mismatch,
   determinism/record 검사 순서에 따라 failure class와 call count가 달라질 수 있다.
2. `M-05`: `atomic_no_replace_move`의 정확한 Windows/filesystem primitive,
   crash model과 metadata persistence 보장이 미확정이다.
3. `M-06`: cleanup 실패로 pass-valued `.pending` bytes가 남을 때 이를 성공
   증거로 거부하는 consumer/quarantine 규칙이 없다.
4. `M-07`: 성공 record가 assembly implementation manifest, reviewed successor
   design identity와 `stub_close_count=1`을 결박하지 않는다.

## 4. 현재 상태

현재 최신 공개 payload는 `179dd6f76f2709881900a42dc32cbde8c33c33b0`이다.
v0.2 설계는 상당 부분 정확해졌지만 독립 심사 verdict가 PASS가 아니므로 공개
implementation gate를 열면 안 된다.

다음 기술 작업은 네 major만 닫는 successor 설계 수정이다. 일반 보안 감사,
새 I4, controller 구현, rehearsal 실행 또는 S0 준비로 범위를 넓히지 않는다.

아직 주장하면 안 되는 것:

- public assembly controller 구현 또는 rehearsal 실행
- v0.2 설계 PASS
- F0, hidden oracle, executor, judge, scoring 또는 S0 실행
- 실제 provider/model, key, trust root, VM/sandbox 또는 role isolation
- E0, 중앙 시스템, Project Brain, 운영 안전성, 경제성 또는 장기 전승

## 5. F0와 동기화 경계

다음 세 경로군은 PUBLIC-GIT 동기화 대상이지만 AI-CONTENT-DEFAULT-DENY다.

- `s0-lab/control/f0-sealed/**`
- `s0-lab/f0-sealed-staging/**`
- `s0-lab/reviews/f0-sealed/**`

이번 집 작업은 이들의 내용이나 개별 filename을 열거나 검색하지 않았다. Git
동기화용 aggregate만 확인했다.

- tracked counts: `32 / 11 / 10`
- total: `53`
- payload parent worktree quiet diff: `0 / 0 / 0`
- untracked/ignored/skip-worktree/assume-unchanged anomalies: `0 / 0 / 0 / 0`

회사 PC도 내용을 읽지 말고 aggregate와 quiet diff만 확인한다. handoff branch는
이 53개를 변경 없이 보존해야 한다.

## 6. 회사 PC 동기화 원칙

1. 회사의 기존 저장소를 새 clone이나 덮어쓰기로 대체하지 않는다.
2. 먼저 path, origin, branch, HEAD, upstream, status, ignored aggregate, stash,
   local-only commit과 worktree를 읽기 전용으로 확인한다.
3. dirty, stash 또는 local-only commit이 있으면 기존 worktree를 움직이지 않고
   채팅의 exact handoff tip을 별도 clean worktree에 배치한다.
4. clean이면 fetch 후 움직이는 branch가 아니라 exact pinned commit을 사용한다.
5. switch/worktree materialization 전 target tree의 F0 aggregate `32/11/10`과
   parent→target quiet diff `0/0/0`을 확인한다.
6. 동기화 후 최신 `AGENTS.md`, 이 handoff pair, v0.2 design과 v0.2 review를
   sidecar로 인증해 완독한다.
7. 기록된 설계 심사를 단순 불신 때문에 다시 실행하지 않는다.

## 7. 미래 — 정확한 다음 후보 gate

다음 후보 gate는 아래 문구다.

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN REVISION OPEN`

이 gate는 M-04부터 M-07만 수정하는 successor 공개 설계를 허용한다. 회사 PC의
첫 동기화 프롬프트 자체는 이 gate를 열지 않는다. 동기화·인증 결과를 보고한 뒤
사용자의 별도 gate를 기다린다.
