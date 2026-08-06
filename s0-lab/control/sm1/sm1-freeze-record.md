# S0 SM1 후속 7개 형식 동결 기록

> 동결일: 2026-08-06  
> 책임: S0 CONTROL  
> 상태: **SM1 독립 비평·중대 수정·제한 재비평 완료**

## 동결 대상

| 파일 | SHA-256 |
|---|---|
| `question-options.schema.json` | `5bd4c1970662b1254f73b828e7f9e6e110d9d683621e8bc6c7bd73fe4def42e0` |
| `transformation-manifest.schema.json` | `8e233cbd678c8319da1b192ddec80ac0907444d7c05802a7c110b6bf35a9d346` |
| `neutral-answer-validation.schema.json` | `675222967cebc312e8fe79bc45763254bd232e3f2325df6d1a4463e7d1d0066c` |
| `access-manifest.schema.json` | `3e27d1bcdb253a9065443d1d9244889dfad753c63512d89178c7ca93dee3ef4b` |
| `run-manifest.schema.json` | `ef773dcc5bc17e6924aafc6c6ab01f080e8793a6ab91c5cbf44654105e5e9f84` |
| `scoring.schema.json` | `2d4e3464c01ca9c220df7344cfdf76bb05021d9d4eec484007c2e21c80af082e` |
| `pre-review-record.schema.json` | `b936fcd86a270f57d81b959682cd72a40e22a35e49013a5ee2f6a3b4c89fa23e` |
| `sm1-seven-format-design.md` | `ccaad8fd9764e8bc9bea50d28e230c36bb3482a292755fc6a1e9aaea56d56bc6` |
| `sm1-seven-format-independent-review.md` | `6d3186cc550637ef977eb98322fa3f4a8f72abf649ce245e45e71fac57ebed81` |
| `sm1-seven-format-final-limited-rereview.md` | `7af896d3eba02ad1dbb5d6d9f255e28cc17538e920b951411898fc9121eda622` |

최초 판정은 `중대한 수정 후 재비평`, 최종 판정은 `현재 SM1 동결 가능`이다. B01–B02, M01–M06, N01–N02는 최종 재비평에서 모두 충분 반영됐다.

## 동결 의미

- question/options↔scoring 순환 해시를 금지하고 단방향 참조만 허용한다.
- 두 block에서 같은 overlay는 같은 불투명 treatment profile에만 결합한다.
- validation·access·retry·13-code coverage·decision function·20개 pre-review check가 실행 전 해시에 연결된다.
- 실제 task ID는 봉인 input 공개 전에 사전 session slot과 결합하며 정상/기술실패 run record 형식을 분리한다.

## 여전히 닫힌 범위

- 실제 schema/manifest instance와 역할별 policy
- 공개·봉인 fixture, question/options 내용, oracle·scoring 내용
- 변환기·validator·runner 구현
- executor 세션·답안·판정
- 실제 Project Brain·운영·경제성·모델 전이

다음 프로토콜 순서는 `F0 공개 연습 묶음 작성·동결 → I0 공개 묶음 기반 최소 구현 점검`이다. 그러나 저장소의 보호 규칙은 fixture 또는 code를 만들기 전에 현재 thread에서 해당 정확한 게이트를 사용자가 열도록 요구한다. 따라서 이 동결 기록 자체는 F0·I0를 열지 않는다.
