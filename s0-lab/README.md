# S0 작업 환경

> 상태: **F0-PUBLIC 재동결·I0 최소 공개 하네스 동결 승인, sealed F0는 닫힘**
> 구현: 공개 fixture 전용 I0 동결, manifest `f57514f...612ae`
> 공개 합성 연습자료: bundle manifest `e41ee6c...eb637`, 독립 제한 재심사 findings 0
> 봉인 시험자료·숨은 정답: 생성하지 않음  
> 실행 A–D: 생성하지 않음

## 현재 작업 묶음

```text
[S0 Control] 현재 주 세션
  ├─ [S0-01] 프로토콜 비평 준비
  ├─ [S0-02] 최소 구현 준비
  ├─ [S0-03] 봉인 출제 준비
  ├─ [S0-04] 판정 준비
  └─ [F0-PUB] 공개 합성 연습자료 작성

프로토콜·구현 동결 후 새로 생성
  ├─ [S0-A] 중앙 구조 없음 실행
  ├─ [S0-B] 프로젝트 로컬 실행
  ├─ [S0-C] 최소 공통 목록 실행
  └─ [S0-D] 최소 출처 연결 실행
```

현재 세션은 통제와 최종 판단을 맡는다. 준비 세션 4개는 서로 fork하지 않은 새 작업이며, 역할 경계 확인 뒤 대기한다. A–D 실행 세션은 사전 오염을 줄이기 위해 실제 봉인 실행 직전에 만든다.

## 현재 환경 선택

- 저장소: 기존 `ai-development-tradition` 프로젝트 사용
- 작업 위치: 현재 `codex/i0-public-harness-candidate` checkout의 repository root
- Git worktree: 현재 절대경로는 세션에서 다시 계산하며 과거 detached 경로는 증거 기록으로만 취급
- 이유: refreeze 후보 변경을 `main`과 분리하고 독립 검토 전 병합을 막음
- 지속 규칙: 루트 `AGENTS.md`
- 역할 설정: `.codex/agents/s0-*.toml`
- 상태 기록: `s0-lab/session-registry.md`

워크트리는 이후 I0·검토 작업의 편집 충돌을 줄이는 용도로만 사용한다. 숨은 정답은 worktree가 아니라 저장소 밖 사용자 통제 영역에서 전달하며, worktree 분리만으로 정보 보안이나 독립성을 주장하지 않는다.

## 게이트

| 게이트 | 상태 | 열리면 가능한 일 |
|---|---|---|
| E0 환경 준비 | 열림 | 역할·세션·허용 입력 설정 |
| P0 프로토콜 작성 | 완료 | S0 규칙·합격·중단·비용 한도 작성 |
| P1 프로토콜 비평 | 완료 | v0.3 제한 재비평 통과·해시 동결 |
| SM0 schema·manifest 설계 | 완료 | 답안 형식과 common/overlay/fixture manifest 형식 독립 비평·동결 |
| SM1 후속 형식 설계 | 완료 | question/options·transformation·validation·access·run·scoring·pre-review-record 형식 독립 비평·동결 |
| F0-PUBLIC 공개 연습 묶음 | 재동결 승인—공개 연습 전용 | B2 식별자·경로 12자 수정, 종속 해시 갱신, 19/19 schema 및 독립 재심사 통과 |
| I0 최소 구현 | 동결 승인—공개 하네스 전용 | 회귀 36개, integrity/schema-check/verify, fresh 독립 제한 재심사 통과 |
| F0 시험자료 출제 | 닫힘 | 공개·봉인 입력과 숨은 정답 작성 |
| R0 봉인 실행 | 닫힘 | 새 A–D 세션 네 개에서 실행 |
| J0 판정 | 닫힘 | 익명 결과와 숨은 정답 비교 |

사용자가 현재 세션에서 정확한 게이트를 열기 전에는 다음 역할이 선행 작업을 시작하지 않는다.

## 숨은 정답 규칙

- 이 저장소에 만들지 않는다.
- 준비 세션에는 제공하지 않는다.
- 구현 AI와 실행 A–D에는 절대로 제공하지 않는다.
- 네 실행 결과가 해시로 고정된 뒤 판정 세션에만 사용자가 전달한다.
- 같은 컴퓨터와 같은 계정이라는 한계 때문에 첫 S0는 완전한 보안 격리가 아니라 절차적 격리로 보고한다.

## 다음 동작

I0의 이전 후보는 CONTROL과 독립 검토자의 제한 재심사에서 구현 자체는 수용 가능 판정을 받았다. 이후 `F0-PUBLIC REOPEN` 게이트에서 네 B2 package stem을 `P0xB2EMBER001`에서 고정 12자 `P0xB2EMBR001`로 수정하고 모든 공개 reference와 종속 해시를 갱신했다. 현재 CONTROL 검증은 회귀 36개 중 35개 통과·symlink 1개 건너뜀, integrity/schema-check/verify exit 0, 지정·확대 오류 0, 적용 가능한 schema 19/19 통과, 공개 패키지 8/8 바이트 단위 재현이다.

Fresh non-fork 독립 제한 재심사는 Critical/Major/Minor findings 0과 `I0/F0-PUBLIC refreeze candidate acceptable for CONTROL final-freeze decision` verdict를 반환했다. CONTROL은 public bundle `e41ee6c...eb637`과 I0 manifest `f57514f...612ae`를 공개 연습 전용으로 동결 승인했다. 결정 기록은 `s0-lab/control/i0/i0-refreeze-gate-decision-v0.1.md`이며 SHA-256은 `a9863be6...2063`이다.

다음 보호 활동은 sealed F0 출제지만 아직 닫혀 있다. 별도 정확한 사용자 승인 전에는 sealed fixture, hidden oracle, executor A-D, S0 실행이나 채점을 시작하지 않는다.
