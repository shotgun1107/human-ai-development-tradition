# F0-PUBLIC v0.1 최종 제한 재심사

## 판정

**현재 F0-PUBLIC 동결 가능**

이 판정은 공개 schema-practice 묶음에만 적용한다. 구현·격리·실행·S0 효과 승인이 아니다.

## 이전 발견 사항 재판정

### F0P-B01 — 충분

- 네 runner instruction에서 판단 힌트가 제거됐다.
- 모두 288 bytes이며 동일 SHA를 사용한다.
- 기존 힌트 문구, H0/H1, 선호, scoring/error 힌트 검색 결과는 0건이다.
- overlay와 run binding이 새 instruction SHA와 일치한다.

### F0P-B02 — 충분

- 두 P04 `R04` edge가 각각 `F-…-05`, `F-…-12`를 모두 근거로 가진다.
- package hash·byte, fixture·transformation·provenance 보고서의 support count `10`, unsupported/oracle-derived count `0`이 일치한다.

### F0P-M01 — 충분

- README와 두 fact manifest에 TAB/LF, ordinal sorting, UTF-8 no-BOM, no-trailing-LF 규칙이 공개됐다.
- 작성자가 첫 수정 초안의 재현 불가능한 `record_content_set` 값을 발견해 수정했다.
- 독립 재계산 결과:
  - block 1: `1e3d1371bb74e48536c692eee6606f714d43f9d181a48e1c890b9682c9ff2a0b`
  - block 2: `a96a8c2421d2a9da946b8da806f79e8629786594870aca1d8c168236879ee22d`
- 두 값, fact-set hash, 26개 normalized-text hash가 모두 일치했고 이전 잘못된 값은 허용된 90개 파일에서 발견되지 않았다.

### F0P-N01 — 충분

91개 파일 구조는 유지되지만 README와 validation report가 placeholder, affirmative example field, schema constant를 운영 증거로 해석할 수 없다고 명확히 제한한다.

### F0P-N02 — 충분

P03 marker topology, P04 relation topology·순서, record-role 순서의 재사용과 경미한 이름 변경까지 명시적으로 금지한다.

## 회귀 검증

- 제어 입력·이전 review·수정 manifest SHA 모두 일치
- manifest 90/90 존재·해시 일치, 중복·누락·초과·self-entry 0
- JSON 56/56 parse 성공
- 양 block의 P01–P04 fact가 canonical과 일치
- byte 상한: block 1 `13.4676%`, block 2 `14.2098%`
- 8개 run의 package·question·instruction binding 일치
- common/pre-review의 overlay·fixture·package hash 집합 일치
- 새 runner 의미 힌트 없음

## 남은 한계

Draft 2020-12 validator engine을 사용할 수 없어 engine validation은 수행하지 못했다. 판정은 기존 정적 schema 검토와 수정 필드의 정적 회귀 확인에 근거한다. 실제 validator engine 검증은 I0의 선행 확인 항목으로 남긴다.

검토자는 파일 수정, 구현, S0 실행, git 작업, subagent 사용을 하지 않았다.
