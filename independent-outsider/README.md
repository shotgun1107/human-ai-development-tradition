# 독립 외부 조사자 작업 구역

> 이 디렉터리의 세 단계는 완료된 역사적 설계·심사 증거다. 현재 기술
> 작업은 [작업 원장](../s0-lab/control/CURRENT-WORK-LEDGER.md)과
> [workstream 구조](../s0-lab/control/workstreams/README.md)에서 찾는다.

이 디렉터리는 중앙 인간–AI 개발 전통 시스템의 기존 연구·설계와 분리된 외부 관점을 만들기 위한 작업 구역이다.

## 운영 규칙

- 1단계 조사자는 이 디렉터리 밖의 파일을 읽거나 검색하지 않는다.
- 기존 연구, Ultra·Pro 설계, 통합 후보와 심사 결과를 보지 않는다.
- 1단계 결과와 심사 기준을 먼저 완성하고 판본과 해시를 고정한다.
- 통합 설계 후보는 고정 이후의 2단계 심사에서만 제공한다.
- 1단계는 조사와 독립 평가 기준 작성이며 시스템 설계나 구현을 하지 않는다.

## 순서

1. `phase-1-research/start-prompt.md`로 새 세션을 시작한다.
2. 결과를 `phase-1-research/independent-research-and-review-criteria.md`에 작성한다.
3. 사람이 결과를 확인한 뒤 판본과 해시를 고정한다.
4. Ultra·Pro 통합 후보가 완성되면 `phase-2-review/start-prompt.md`로 외부 심사를 수행한다.
5. v2.1 제한 수정 후보를 `phase-3-limited-rereview/start-prompt.md`의 경계로 재심사하고, [v2.1 제한 재심사 결과](./phase-3-limited-rereview/v2-1-limited-rereview.md)를 동결했다.

1단계 독립 보고서, 2단계 심사, 3단계 제한 재심사 결과가 모두 해시로
동결됐다. 이 완료는 중앙 시스템 구현이나 S0 실행을 의미하지 않는다.
