# S0 SM0 schema·manifest 형식 동결 기록

> 동결일: 2026-08-06  
> 책임: S0 CONTROL  
> 상태: **SM0 독립 비평·제한 재비평 완료 — 후속 7개 형식 설계 기준선**

## 동결 대상

| 파일 | SHA-256 |
|---|---|
| `answer.schema.json` | `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` |
| `common-manifest.schema.json` | `a539022d937672a99c605c12980f10d89a956a40c1e8523cb02f774d280ccc8a` |
| `condition-overlay-manifest.schema.json` | `a239c1ffa7e4b9ae3c963e7ddbf55c4cabf1f05353032cd11d9d35b842086e7a` |
| `fixture-manifest.schema.json` | `846071f069b1cbc040ef89e176caa1698dfb13fce6c6848505a60523fd8f9c80` |
| `sm0-schema-manifest-design.md` | `d3841d46baff6c6e8353ea31e4f83b80c9f48e4c2855012d6c5b6a027a391292` |
| `sm0-schema-manifest-independent-review.md` | `a8383c4f9b246e4e50402ee186d46fdceb59515238521d9aac4070e2765287d3` |
| `sm0-schema-manifest-final-limited-rereview.md` | `2eb25a9099e4c94e6bba490721774afb0d6434a5291d5392e159e85ec15099c4` |

최종 판정은 `현재 SM0 동결 가능`이며 최초 비평의 B01–B03, M01–M02, N01–N02는 모두 `충분 반영`이다.

## 동결 의미

- 위 파일은 해당 해시에서 변경하지 않는다. 수정이 필요하면 새 판본과 새 비평을 만든다.
- 다음에 열 수 있는 최대 범위는 question/options, transformation, neutral answer-validation, access, run, scoring, pre-review-record의 **형식 설계·비평**이다.
- 실제 manifest, prompt, fixture, oracle, scoring 내용, validator, 변환기, runner, A–D 실행은 만들거나 시작하지 않는다.
- 후속 형식이 모두 통과해도 I0·F0는 별도 게이트 판단 전까지 닫힌다.

## 확인하지 않은 것

- 실제 instance와 교차 검사 결과
- 실제 세션·모델·로컬 권한 대칭
- 실제 fixture·oracle·scoring의 정확성
- 구현·S0 실행·효과·경제성·Project Brain 연결
