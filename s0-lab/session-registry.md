# S0 세션 등록부

> 기준일: 2026-08-06  
> 상태: I0 구현 후보 수용 가능, F0-PUBLIC 상위 결함으로 I0 동결 보류

| 코드 | 역할 | Codex 작업 | 환경 | 현재 게이트 | 상태 |
|---|---|---|---|---|---|
| CONTROL | 통제·최종 판단 | 현재 작업 | 기존 프로젝트 Local + detached worktree | I0 | HOLD—F0-PUBLIC 재개방 승인 대기 |
| I0-BUILD-0 | 최초 최소 구현 시도 | `/root/i0_implementation_builder` | detached worktree `c9f68f3` | I0 | DONE—안전 검토 차단, 파일 쓰기 0 |
| I0-BUILD | 최소 구현·제한 수정 | `/root/i0_implementation_builder_trusted` | detached worktree `c9f68f3` | I0 | DONE—후보 manifest `e670041...c105` |
| I0-REVIEW | 독립 코드 심사·제한 재심사 | `/root/i0_independent_reviewer` | read-only detached worktree | I0-R | DONE—구현 수용, 상위 재동결 필요 |
| F0-PUB | 공개 합성 연습자료 작성 | `/root/f0_public_author` | 격리 역할 세션·공유 작업공간 | F0-PUBLIC | REOPEN REQUIRED—관련 위반 20건 |
| S0-01 | 프로토콜·형식 비평 | `019fd506-ffac-7af3-8948-0bcba7d3c8da` | 기존 프로젝트 Local | SM1-R | DONE—SM1 동결 가능 |
| S0-02 | 최소 구현 | `019fd507-059a-72e1-b3d8-a2665100cbd1` | 기존 프로젝트 Local | I0 | READY—대기 |
| S0-03 | 봉인 출제 | `019fd507-0bfc-7121-ac5d-bf33dcf3ed37` | 기존 프로젝트 Local | F0 | READY—대기 |
| S0-04 | 판정 | `019fd507-12f5-77b2-929f-cb34d0435259` | 기존 프로젝트 Local | J0 | READY—대기 |
| S0-A | 방식 A 실행 | R0 직전에 생성 | 미정 | R0 | 미생성 |
| S0-B | 방식 B 실행 | R0 직전에 생성 | 미정 | R0 | 미생성 |
| S0-C | 방식 C 실행 | R0 직전에 생성 | 미정 | R0 | 미생성 |
| S0-D | 방식 D 실행 | R0 직전에 생성 | 미정 | R0 | 미생성 |

## 공통 준비 세션 지시

1. 루트 `AGENTS.md`와 `s0-lab/README.md`만 읽는다.
2. 자신의 게이트가 닫혀 있음을 확인한다.
3. 파일을 수정하거나 저장소를 추가 탐색하지 않는다.
4. 역할·금지 범위·시작 신호를 한 문단으로 확인하고 대기한다.

S0-02~04 준비 세션은 역할을 예약하기 위한 것이며 현재 결과 생산을 승인하지 않는다. S0-01의 완료는 schema·manifest 설계 가능 판정일 뿐 구현·출제·실행 승인이 아니다.
