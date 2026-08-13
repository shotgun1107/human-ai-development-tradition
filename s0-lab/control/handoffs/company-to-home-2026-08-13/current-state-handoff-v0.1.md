# 회사→집 CONTROL 동기화 인수인계 v0.1

- `date_kst`: 2026-08-13
- `repository`: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- `handoff_branch`: `codex/company-to-home-handoff-20260813`
- `handoff_payload_parent`: `a34e54b0ac8fbfa4c42ffced5dcd2ac15016f0e3`
- `handoff_payload_parent_tree`: `454186959ec5f929f25d9bd4f48be4fd3023f33f`
- `source_feature_branch`: `codex/s0-public-assembly-rehearsal-implementation-v01`
- `recorded_origin_main`: `41e0b684a7cca387be6d264c4a5b63de2561fd7c`
- `recorded_origin_main_tree`: `a14e8b9c9bc8905060cd8811e8934643e2aa4aa3`
- `runtime_preloader_v0.3_package_manifest_sha256`:
  `c2ecd2931e15a99b68d3e669026342f59a42995268f8b4937ba96e63d731481b`
- `status`: company work preserved; exact home synchronization and first report pending

## 1. 목적과 정본 원칙

이 문서는 회사 PC에서 완료한 Git-tracked 공개 작업을 집 PC로 손실 없이
전달하기 위한 동기화 정본이다. 최종 handoff commit은 이 문서 자신과 집 PC
시작 프롬프트를 포함하므로, 최종 commit과 tree는 커밋·푸시 뒤 사용자가
전달하는 값을 정본으로 사용한다.

동기화 대상은 Git이 추적하는 프로젝트 tree다. 가상환경, cache, Codex 대화
기억, OS별 설치 위치는 동일화 대상이 아니다. 반대로 이번 설계, 재심사 보존
기록, sidecar, manifest는 최종 handoff tree에 포함되어야 한다.

과거 대화는 증거가 아니다. 집 PC에서는 현재 Git 정본, 최신 root
`AGENTS.md`, 이 handoff pair, 인증된 설계 패키지만 증거로 사용한다.

## 2. 과거 — 오늘 회사에서 완료한 것

### 2.1 기준 main 인증

원격 main은 예상 commit과 일치했다.

- commit: `41e0b684a7cca387be6d264c4a5b63de2561fd7c`
- tree: `a14e8b9c9bc8905060cd8811e8934643e2aa4aa3`
- 의미: v0.5 public assembly rehearsal 설계와 main 통합 결정까지의 기준선

### 2.2 public assembly bounded implementation candidate

기능 브랜치 `da4ad3af483652bd755deff9d024a9833c177d39`에는 공개 assembly
candidate와 runtime/preloader 설계 v0.1이 추가되었다.

candidate 코드는 존재하지만 다음 이유로 공식 rehearsal 성공이나 구현 검증을
주장할 수 없다.

- 인증된 CPython, stdlib, extension, `jsonschema`, system DLL runtime profile이
  아직 실제로 materialize되지 않았다.
- live harness는 그 profile 부재 상태에서 output mutation 전에 fail-closed한다.
- native preloader, 공식 platform probe, 실제 `MoveFileExW`, provider/model,
  F0, oracle, S0 실행은 없었다.

따라서 “candidate 파일이 존재한다”와 “실제 환경에서 통과했다”는 서로 다른
사실이다.

### 2.3 runtime profile + neutral preloader v0.1과 v0.2

v0.1 독립 재심사는 세 결함을 찾았다.

1. 한 anonymous pipe의 양방향 사용;
2. 존재하지 않는 output root의 object identity를 조기 요구;
3. `maximum_processes=1`의 계산 영역 모순.

v0.2는 commit `ce62b7ef3f819e182a6f68e2a50eed6ec76d56e4`에서 이를
다음과 같이 보완했다.

- 세 개의 단방향 pipe;
- absent leaf와 created root의 단계 분리;
- preloader, job member, candidate process 계산 영역 분리;
- `COMMIT-ACKED` 후에만 live consumer 평가.

그러나 fresh v0.2 독립 재심사는 verdict `REVISE-AND-REREVIEW`, finding
`MAJOR 2 / MINOR 1`을 반환했다.

- `RPNP2-RR-001`: Python bootstrap이 네 inherited handle의 역할을 발견할
  고정된 locator가 없었다.
- `RPNP2-RR-002`: output directory를 만든 뒤 별도로 여는 사이에 object
  replacement 경쟁 구간이 있었다.
- `RPNP2-RR-003`: terminal `SPENT` 재시도와 “모든 invalid transition은
  `REJECTED`”라는 규칙이 충돌했다.

그 결과는 CONTROL 보존 기록으로 Git에 고정되었다. 이 기록은 reviewer 서명이나
승인이 아니라 독립 재심사 결과의 정규화된 보존본이다.

### 2.4 runtime profile + neutral preloader v0.3 설계 후보

commit `a34e54b0ac8fbfa4c42ffced5dcd2ac15016f0e3`은 위 세 finding을
설계 수준에서 답했다.

- inherited handle discovery:
  - 정확히 다섯 개의 고정 순서 command-line locator;
  - 숫자 locator 자체에는 authority 없음;
  - 인증된 one-use native guard가 object kind, access direction, root identity,
    preloader process binding, frame/nonce/EOF를 검증한 뒤에만 private wrapper를
    생성;
  - 성공과 실패 모두 첫 호출에서 latch 소비.
- atomic output root:
  - preloader가 retained parent handle을 `RootDirectory`로 사용;
  - 단일 `ntdll.dll!NtCreateFile` 호출이 leaf 생성과 retained root handle
    획득을 동시에 수행;
  - `FILE_CREATE`, directory/no-reparse 옵션, 고정 ABI와 status 검증;
  - pathname reopen, `CreateDirectory*`, fallback, retry 없음;
  - parent case-sensitive flag 0과 case-insensitive collision lookup으로 case
    alias 경쟁도 차단.
- terminal state:
  - nonterminal invalid transition은 `REJECTED`;
  - `SPENT` 또는 `REJECTED`에서의 재시도는 상태를 바꾸지 않고 실패.

v0.3 package manifest SHA-256은 다음과 같다.

`c2ecd2931e15a99b68d3e669026342f59a42995268f8b4937ba96e63d731481b`

회사 PC에서 완료된 검증:

- canonical text validator SelfTest: PASS;
- 모든 새 Markdown/sidecar pair: PASS;
- JSON duplicate-key rejection parse: PASS;
- Draft 2020-12 schema direct audit: PASS;
- interface/schema/design 간 locator, native call, atomic-root, state,
  package-composition 일치 검사: PASS;
- package manifest exact set/order/hash: PASS;
- 승인된 공개 변경 15개 외 미분류 변경: 0.

## 3. 현재 — 전달되는 정확한 상태

handoff payload parent는 다음 계보를 포함한다.

1. main integration 기준 `41e0b684...`;
2. public candidate와 runtime/preloader v0.1 `da4ad3af...`;
3. runtime/preloader v0.2 `ce62b7ef...`;
4. v0.2 재심사 보존과 runtime/preloader v0.3 `a34e54b0...`.

v0.3은 아직 fresh independent rereview 전이다. 다음을 완료 또는 검증된 것으로
주장하면 안 된다.

- v0.3 native guard 또는 `NtCreateFile` preloader 구현;
- 실제 runtime-profile capture/materialization;
- compiler/linker/binary/import review;
- real-Windows platform probe;
- official public assembly rehearsal;
- 실제 provider/model/network call 또는 `MoveFileExW`;
- F0 내용 접근, oracle, executor, judge, S0/E0;
- central system, Project Brain, operational safety, economic value,
  model-to-model transfer.

세 PUBLIC-GIT / AI-CONTENT-DEFAULT-DENY F0 경로군은 Git 동기화 대상으로 최종
tree에 그대로 보존된다. 그 내용과 개별 filename은 이 인수인계의 입력이 아니다.

- aggregate tracked counts: `32 / 11 / 10`
- total: `53`
- payload parent의 부모→payload parent F0 quiet diff: `0 / 0 / 0`

## 4. 집 PC 동기화 절차

### 4.1 기존 작업 보존이 우선

집의 기존 저장소에서 다음을 읽기 전용으로 먼저 확인한다.

- resolved repository path와 origin URL;
- branch, HEAD, upstream, detached 여부;
- staged, unstaged, untracked, ignored aggregate;
- stash와 local-only commit;
- worktree 목록.

origin은 반드시 아래 저장소여야 한다.

`https://github.com/shotgun1107/human-ai-development-tradition.git`

dirty 작업, stash 또는 local-only commit이 있으면 기존 worktree를 switch,
reset, clean, stash, rebase, merge하지 않는다. 기존 상태를 그대로 두고 exact
handoff tip을 별도 clean worktree에 materialize한다. 기존 저장소가 완전히
clean할 때만 그 worktree를 handoff branch로 전환할 수 있다.

### 4.2 fetch 뒤 exact pin부터 검증

보존 preflight가 통과하면 origin을 한 번 fetch한다. `git pull`은 사용하지 않는다.
사용자가 전달한 final handoff commit과 tree를 먼저 pin한 뒤 다음을 검증한다.

- live remote `codex/company-to-home-handoff-20260813` tip = exact final tip;
- final tip tree = 사용자가 전달한 exact final tree;
- final tip의 유일한 첫 부모 =
  `a34e54b0ac8fbfa4c42ffced5dcd2ac15016f0e3`;
- payload parent tree =
  `454186959ec5f929f25d9bd4f48be4fd3023f33f`;
- `41e0b684...`, `da4ad3af...`, `ce62b7ef...`, `a34e54b0...`가 final
  tip의 조상;
- exact target F0 aggregate = `32 / 11 / 10`;
- payload parent→final tip의 세 F0 quiet diff = `0 / 0 / 0`.

하나라도 다르면 움직이는 branch 이름이나 임의의 최신값을 받아들이지 말고,
public commit 및 aggregate 상태만 보고한 뒤 멈춘다.

### 4.3 materialization 뒤 확인

- local HEAD = remote exact handoff tip;
- local tree = exact handoff tree;
- status 출력 0;
- staged/unstaged quiet diff 0;
- local F0 aggregate `32 / 11 / 10`;
- skip-worktree와 assume-unchanged aggregate가 허용 상태;
- 기존 집 작업은 손실·변경 없음.

## 5. 집 PC에서 처음 인증하고 읽을 공개 정본

최신 root `AGENTS.md`를 처음부터 끝까지 먼저 읽는다. 그 뒤 canonical
text-artifact validator를 읽고 SelfTest를 실행한다. SelfTest가 PASS일 때만 다음
두 Markdown/sidecar pair를 검증하고 완독한다.

1. `s0-lab/control/handoffs/company-to-home-2026-08-13/current-state-handoff-v0.1.md`
2. `s0-lab/control/handoffs/company-to-home-2026-08-13/home-local-resume-prompt-v0.1.md`

그다음 v0.3 package manifest를 인증하고, v0.3 independent-rereview brief가
명시한 exact public allowlist만 사용한다. F0나 구현 source/test로 범위를
넓히지 않는다.

기록된 과거 validator와 설계 검사를 단순 불신 때문에 다시 수행하지 않는다.
첫 작업은 동기화·인증·상태 보고만 하고 멈춘다.

## 6. 미래 — 다음 단 하나의 후보 gate

다음 후보 gate는 아래 문구다.

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.3 INDEPENDENT REREVIEW OPEN`

이 gate는 v0.3 설계가 v0.2 finding 세 건을 실제로 닫았는지 fresh 독립 역할로
재심사하는 read-only gate다. 다음을 열지 않는다.

- 구현 또는 source 수정;
- compilation/build/runtime materialization;
- native API 또는 platform probe 실행;
- official assembly rehearsal;
- F0/oracle/executor/judge/S0;
- provider/model/network;
- commit, push, PR 또는 main integration.

집 PC 첫 동기화 프롬프트는 이 gate도 자동으로 열지 않는다. 동기화 보고 후
사용자가 위 exact gate를 별도로 입력할 때만 시작한다.

## 7. 동기화 완료 조건

- exact final handoff commit/tree가 local과 remote에서 일치;
- final tip의 first parent와 payload tree가 위 값과 일치;
- Git-tracked worktree가 clean;
- F0 aggregate `32 / 11 / 10`, payload parent→final diff `0 / 0 / 0`;
- handoff 두 Markdown/sidecar pair가 canonical validator에서 PASS;
- 기존 집 작업을 덮어쓰거나 숨기지 않음;
- 새 기술 gate, 구현, 테스트, subagent, commit, push, PR, main merge를
  시작하지 않음.

이 조건이 충족되면 오늘 회사 작업은 집 PC에 손실 없이 인계된 것이다.
