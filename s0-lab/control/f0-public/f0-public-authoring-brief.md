# F0-PUBLIC authoring brief

## 1. 역할

독립 `F0-PUBLIC` 작성자는 **공개 합성 연습 묶음**만 작성한다. 이 역할은 봉인 F0 출제자, I0 구현자, executor A–D, 사전 검토자, 사후 판정자가 아니다. 이 세션을 executor 세션으로 fork하거나 재사용하지 않는다.

## 2. 목적

I0가 나중에 변환기·검증기를 구현하기 전에, 동결된 프로토콜과 11개 JSON 형식을 실제처럼 연결해 볼 수 있는 작고 완전히 공개된 연습 묶음을 제공한다. 이 묶음의 결과는 S0 점수나 중앙 시스템 효과 증거로 사용하지 않는다.

## 3. 허용 입력

아래 15개 파일만 읽을 수 있다. allowlist는 최대 범위이며 저장소를 검색하거나 다른 파일을 읽지 않는다.

| SHA-256 | 경로 |
|---|---|
| `14f1d05cca42fd4d7930cad2537bb34bcec17ebcb22630e2f004798123f7a5a2` | `AGENTS.md` |
| `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | `s0-lab/control/s0-protocol-v0.3.md` |
| `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` | `s0-lab/control/sm0/answer.schema.json` |
| `a539022d937672a99c605c12980f10d89a956a40c1e8523cb02f774d280ccc8a` | `s0-lab/control/sm0/common-manifest.schema.json` |
| `a239c1ffa7e4b9ae3c963e7ddbf55c4cabf1f05353032cd11d9d35b842086e7a` | `s0-lab/control/sm0/condition-overlay-manifest.schema.json` |
| `846071f069b1cbc040ef89e176caa1698dfb13fce6c6848505a60523fd8f9c80` | `s0-lab/control/sm0/fixture-manifest.schema.json` |
| `d3841d46baff6c6e8353ea31e4f83b80c9f48e4c2855012d6c5b6a027a391292` | `s0-lab/control/sm0/sm0-schema-manifest-design.md` |
| `5bd4c1970662b1254f73b828e7f9e6e110d9d683621e8bc6c7bd73fe4def42e0` | `s0-lab/control/sm1/question-options.schema.json` |
| `8e233cbd678c8319da1b192ddec80ac0907444d7c05802a7c110b6bf35a9d346` | `s0-lab/control/sm1/transformation-manifest.schema.json` |
| `675222967cebc312e8fe79bc45763254bd232e3f2325df6d1a4463e7d1d0066c` | `s0-lab/control/sm1/neutral-answer-validation.schema.json` |
| `3e27d1bcdb253a9065443d1d9244889dfad753c63512d89178c7ca93dee3ef4b` | `s0-lab/control/sm1/access-manifest.schema.json` |
| `ef773dcc5bc17e6924aafc6c6ab01f080e8793a6ab91c5cbf44654105e5e9f84` | `s0-lab/control/sm1/run-manifest.schema.json` |
| `2d4e3464c01ca9c220df7344cfdf76bb05021d9d4eec484007c2e21c80af082e` | `s0-lab/control/sm1/scoring.schema.json` |
| `b936fcd86a270f57d81b959682cd72a40e22a35e49013a5ee2f6a3b4c89fa23e` | `s0-lab/control/sm1/pre-review-record.schema.json` |
| `ccaad8fd9764e8bc9bea50d28e230c36bb3482a292755fc6a1e9aaea56d56bc6` | `s0-lab/control/sm1/sm1-seven-format-design.md` |

읽기 전에 15개 SHA-256을 확인한다. 하나라도 다르면 아무 산출물도 쓰지 않고 중단한다.

## 4. 허용 출력

오직 `s0-lab/public-practice/v0.1/` 아래에만 새 파일을 쓴다. 기존 파일과 다른 경로를 수정하지 않는다.

반드시 포함할 내용:

1. `README.md`: 목적, 사용법, 비증거 경계, 실제·과거 자료 미사용 선언
2. 서로 다른 실제 시험 이름·문장·정답을 쓰는 완전한 허구의 작은 canonical 사건 묶음
3. 동일 사실을 보존한 불투명 조건 `P01`–`P04`의 공개 예상 표현
4. 공개 질문·허용 선택지·예상 중립 답안·공개 oracle·공개 scoring 예제
5. SM0·SM1의 11개 JSON Schema 각각에 대응하는 최소 유효 instance 예제
6. 파일 간 참조·SHA-256·fact/record/question ID 연결을 확인하는 사람이 읽을 수 있는 `validation-report.md`
7. 자기 자신을 제외한 최종 묶음 파일을 고정하는 `bundle-files.sha256`

파일 구조와 추가 파일명은 위 요구를 분명히 충족하는 범위에서 작성자가 정한다.

## 5. 작성 규칙

- 실제 고객, 개인, 비밀, 과거 프로젝트, 브랜드, 기존 대회·외주 자료를 사용하지 않는다.
- 공개 연습의 고유명사·문장·정답 순서는 향후 봉인 block에서 재사용할 수 없다고 명시한다.
- 공개 oracle과 scoring은 이 연습 묶음 전용이며 숨은 정답이 아니다.
- 조건 표시에는 `A`–`D`, 구조 우열, `chronological`, `lineage`, `common` 같은 목표 누출 명칭을 쓰지 않고 `P01`–`P04`만 쓴다.
- 조건별 fact ID 집합과 질문 기회는 같아야 한다.
- 조건별 표현 byte 차이는 최소 표현 대비 15% 이내여야 하며 의미 없는 padding을 금지한다.
- JSON은 UTF-8, parse 가능, 대응 schema에 유효해야 한다. schema 밖 의미 제약도 `validation-report.md`에서 별도로 확인한다.
- 코드·스크립트·실행 도구를 구현하지 않는다. 읽기·정적 검증·해시 계산을 위한 기존 로컬 명령만 사용할 수 있다.
- git commit, push, branch 생성은 금지한다.

## 6. 완료 판정

작성자는 산출물을 만든 뒤 다음만 보고한다.

- 생성 파일 목록과 개수
- 허용 입력 SHA 확인 결과
- JSON parse/schema 검증 결과
- 조건별 fact 수·question 수·byte와 15% 상한 결과
- bundle manifest 검증 결과
- 남은 미검증 사항

CONTROL이 별도 독립 검토를 통과시키기 전에는 F0-PUBLIC을 완료로 간주하지 않는다.
