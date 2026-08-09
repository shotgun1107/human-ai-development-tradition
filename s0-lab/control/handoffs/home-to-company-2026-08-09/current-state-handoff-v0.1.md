# 집 로컬에서 회사 CONTROL로 보내는 현재 상태 인수인계 v0.1

- 작성 기준 시각: `2026-08-09` KST
- 저장소: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- 활성 기준선: `central-system-v2.1-s0-preparation`
- 인수인계 성격: 공개 CONTROL 상태와 다음 design-only 작업의 Git 인계
- 금지 범위: 구현, VM 구성, 키 생성, protected material, sealed bank, oracle, 모델 호출, 채점, E0/S0 실행

이 문서는 집 PC의 대화 기억을 회사 PC로 전달하는 문서가 아니다. 회사
CONTROL은 실제 원격 Git 상태, 현재 회사 로컬의 작업 트리, `AGENTS.md`,
공개 문서와 SHA-256 기록을 다시 확인해야 한다. 아래 SHA는 2026-08-09
KST에 확인된 인수인계 기준점이며, 프롬프트에 맞추기 위해 원격을 되돌리거나
로컬 사용자 변경을 제거하는 데 사용하면 안 된다.

## 1. 원격 Git 기준점

2026-08-09 KST의 `git ls-remote --heads origin` 확인 결과는 다음과 같다.

| 원격 ref | 확인된 SHA |
|---|---|
| `refs/heads/main` | `93e353ac975c3cb5c948d61609fe4e43c57a0f37` |
| `refs/heads/codex/s0-trust-root-role-isolation-design-v02` | `cb4198f4475881ba5b607517fdbb4f0db6b8ce5d` |
| `refs/heads/codex/s0-trust-root-role-isolation-review-v02` | `7d251f04588babeb180b743c8f6860929997b17c` |

확인된 공개 계보는 선형이다.

```text
93e353ac  main: Approve I1 v0.2 CONTROL integration
  -> ccedcbc3  S0 trust-root/role-isolation v0.1 design
  -> 2fc32870  v0.1 independent review record
  -> cb4198f4  v0.2 design revision
  -> 7d251f04  v0.2 independent review record
```

`codex/s0-trust-root-role-isolation-review-v02`는 v0.2 설계 커밋을 직접
선행자로 가지므로 v0.2 설계와 독립 심사 기록을 모두 포함한다. 이
인수인계 브랜치는 `7d251f04...`에서 갈라졌으며, 인수인계 문서만 추가한다.
회사 CONTROL은 인수인계 브랜치의 실제 원격 HEAD를 다시 읽고
`7d251f04...`가 조상인지 확인해야 한다.

집 PC의 절대경로와 worktree 위치는 회사 PC의 현재 상태에 대한 증거가
아니다. 회사 PC에 저장소가 이미 있으면 새 clone을 만들지 않는다.

## 2. `main`에 통합된 공개 상태

### E0 v0.4 설계

- `e050fdd`: `Merge E0 v0.4 design and independent review`
- 독립 심사 판정: `PASS-FOR-CONTROL-INTEGRATION-ONLY`
- 의미: E0의 효과시험 설계와 심사 기록이 `main`에 보존됐다.
- 비의미: E0 자료, oracle, prompt, schema, runner, 모델 실행, 채점 또는
  효과 결론이 만들어지거나 승인된 것이 아니다.
- 현재 S0 순차 진행 동안 E0 후속 게이트는 닫혀 있다.

### F0-PUBLIC 질문 계약 v0.14

- `c0f4e09`: `Merge F0-PUBLIC question contract v0.14`
- 공개 질문 계약 설계와 독립 심사 및 CONTROL 통합 기록이 `main`에 있다.
- 이것은 S0 실행 성공이나 표현 구조의 효과를 뜻하지 않는다.

### I1 공개 구현 선행조건 v0.2

- `93e353a`: `Approve I1 v0.2 CONTROL integration`
- I0를 수정하지 않는 공개 successor 구조층과 제한된 공개 검증 기록이
  `main`에 통합됐다.
- 이것은 trust root, 실제 키, 역할별 VM, protected store, provider,
  executor, fixture, oracle 또는 S0 실행의 구현 승인이 아니다.

## 3. `main` 밖에서 완료된 최신 S0 설계 작업

### v0.1 설계와 독립 심사

- 설계 커밋: `ccedcbc3a6a029df76d4d612b2978370558c87fb`
- 심사 기록 커밋: `2fc328700124d6b874ddad4c82ca718a7c561d6a`
- v0.1 심사 결과: `REVISE-AND-REVIEW`
- 원래 결함: strict Ed25519 검증, 비순환 PoP/root bootstrap,
  invocation descriptor 권한, invocation uniqueness 규격의 불완전성

### v0.2 설계 수정

- 설계 커밋: `cb4198f4475881ba5b607517fdbb4f0db6b8ce5d`
- 설계 브랜치: `codex/s0-trust-root-role-isolation-design-v02`
- 주요 수정: strict Ed25519 profile, 비순환 PoP/root/activation 경로,
  unsigned TCB-bound invocation descriptor, 단일 invocation ID와 HKDF,
  ceremony/signer-media/invocation ledger와 독립 monotonic witness
- 작성자 측 QA는 독립 증거가 아니다.

### v0.2 독립 심사

- 심사 커밋: `7d251f04588babeb180b743c8f6860929997b17c`
- 심사 브랜치: `codex/s0-trust-root-role-isolation-review-v02`
- 공식 Markdown SHA-256:
  `67617db3b89e8067cd069609d0705f7b853f741acb5fc40eba4b675435327990`
- 판정: `REVISE-AND-REVIEW`
- finding: blocking 0, major 1, minor 1
- 기존 `TRI-B01`, `TRI-B02`, `TRI-M01`, `TRI-M02`는 proposal-text
  수준에서 폐쇄됐다.
- 32 role rows, 40 positions, 8 paired rows, 21 experimental signers와
  non-row root 1개, registry ID 22개, store 27개, reader 46개, edge
  64개와 A-D의 공개 설계상 기회 대칭은 유지됐다.

남은 결함은 다음 두 개다.

1. `TRI2-M01` (`major`): preactivation-context, registry-binding,
   activation-binding의 세 state-changing import가 성공했는지 거부됐는지
   호스트가 정확히 구별할 canonical outcome 경로가 없다. 종료와 ISO
   detach만으로는 성공과 실패가 같아 보인다. 각 import에 대해 bounded,
   canonical, host-observable 결과 경로와 성공·거부·crash·missing·duplicate·
   disagreement 규칙을 설계해야 한다.
2. `TRI2-m01` (`minor`): `bad_y2`와 네 order-eight encoding의 출처로
   적은 RFC 9381 section 5.4.5가 실제 값을 제공하지 않는다. 거짓 출처를
   제거하고 검증 가능한 derivation과 exact 32-byte encodings 또는 실제
   공식 primary source로 교체해야 한다.

v0.2는 CONTROL integration 고려 대상이 아니며 `main`에 병합하면 안 된다.

## 4. 현재 최대 주장

현재 공개 근거로 말할 수 있는 최대 범위는 다음과 같다.

- F0-PUBLIC 질문 계약 v0.14와 I1 공개 구조층 v0.2는 제한된 공개 범위에서
  CONTROL 통합됐다.
- E0 v0.4는 독립 심사를 통과한 설계 패키지로 `main`에 보존됐다.
- trust-root/role-isolation v0.2는 v0.1의 네 결함을 설계 문구 수준에서
  고쳤지만 새 major 1건과 minor 1건 때문에 다시 수정·심사해야 한다.

다음은 구현 또는 검증됐다고 주장하면 안 된다.

- 실제 trust root, anchor, registry, Ed25519 key 또는 서명 서비스
- 역할별 VM/sandbox/principal, network/clipboard/Git 차단
- protected store, ACL, atomic backend, ledger provider와 witness
- fixture, sealed bank, agreed label, oracle, condition map
- executor A-D, 모델 호출, 공홈 Pro 판정, 채점과 통계
- S0 또는 E0 효과
- 중앙 전통 시스템, Project Brain 통합, 운영 안전성, 경제성, 장기 전승

## 5. 회사 CONTROL이 이어서 할 일

첫 작업은 구현이 아니라 v0.3 public design successor다. 회사 CONTROL은
먼저 읽기 전용 상태 보고를 제출하고, 모든 기준선과 sidecar가 일치할 때만
다음 design-only 게이트를 이어서 수행한다.

```text
S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN
```

권장 successor 브랜치는
`codex/s0-trust-root-role-isolation-design-v03`이며, 인수인계 브랜치의
원격 HEAD에서 별도 worktree로 만든다. `main`, v0.2 설계 커밋 또는 과거
대화에서 직접 시작하지 않는다.

수정 범위는 `TRI2-M01`과 `TRI2-m01`뿐이다. v0.1/v0.2 파일과 sidecar는
수정하지 않고 v0.3 경로에 successor 문서를 만든다. 역할·store·edge 수,
A-D 공정성, closed provider/implementation/protected-material/E0/S0 게이트를
바꾸지 않는다. 독립 심사는 별도 future gate와 fresh reviewer가 필요하다.

## 6. Git, worktree와 봉인 경계

- 회사 로컬의 변경 또는 미추적 파일은 사용자 작업으로 간주한다.
- `reset --hard`, `clean`, stash, 강제 checkout, 삭제나 이동으로 숨기지 않는다.
- 회사 PC에만 있는 미추적 sealed 자료가 존재할 수 있지만 이번 공개 설계
  작업에서는 존재 여부와 Git 추적 여부를 넘어서 읽거나 검색하지 않는다.
- Git에 없는 집 대화와 회사 대화는 공식 증거가 아니다.
- worktree는 편집 충돌 격리이며 비밀 보안 경계가 아니다.
- 새 worktree에는 공개 allowlist만 제공하고 sealed/oracle 자료를 복사하지
  않는다.
- 구현, key 생성, VM 구성, acceptance test 실행, model call은 이번
  인수인계와 다음 설계 수정 게이트 모두에서 금지된다.

## 7. 인수인계 완료 조건

회사 CONTROL은 다음을 만족하면 인수를 완료한 것으로 보고한다.

1. 실제 회사 저장소 경로, origin, branch, HEAD, upstream, status와 worktree
   목록을 보고했다.
2. live remote `main`, v0.2 design, v0.2 review와 handoff branch를 다시 읽었다.
3. `7d251f04...`가 handoff branch의 조상임을 확인했다.
4. 허용된 Markdown/sidecar를 canonical validator로 인증했다.
5. 완료·후보·미구현 상태와 두 finding을 자신의 말로 구분했다.
6. dirty 또는 hash mismatch가 없으면 v0.3 설계 successor를 별도 worktree에서
   시작했다.
