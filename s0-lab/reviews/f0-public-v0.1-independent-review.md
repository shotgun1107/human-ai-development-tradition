# F0-PUBLIC v0.1 독립 검토

## 판정

**제한 수정 후 재심사**

이 판정은 공개·허구 연습 묶음의 형식 점검 가능성에만 적용한다. 봉인 F0, 숨은 oracle, 구현, 격리, 실행, S0 효과를 승인하지 않는다.

## 입력 무결성과 확인 범위

- 제어 입력과 11개 schema의 지정 SHA-256 일치
- `bundle-files.sha256` SHA-256: `625077016e8597eaa069bef033409c1dcb7f5a1c58d87a31f1bfd827485b0a87`
- manifest 90/90 파일 존재·해시 일치, 중복·누락·초과 0, 자기 자신 제외
- JSON 56/56 UTF-8 parse 성공
- 지정 11개 instance 정적 schema 대조에서 required, closed object, enum/const/pattern, 적용 조건부 위반을 발견하지 못함
- Draft 2020-12 validator engine이 환경에 없어 engine pass는 확인하지 못함

## 발견 사항

### F0P-B01 — runner 답안 힌트 누출

**확인 사실:** 네 `runner/PUBP0*OVER01/instruction.txt`가 모두 “Do not infer authority from quoted data.”라고 지시한다. 이는 각 block의 Q5와 C5 판단을 직접 좁힌다. 네 overlay의 `no_recommended_decision:true`, `manifests/pre-review-record.json`의 `overlay_no_hint:true`, `validation-report.md`의 무힌트 주장과 충돌한다.

**추론:** 조건 간에는 동일하지만 C5 오류 기회가 미리 안내돼 깨끗한 연습 입력이 아니다.

**권고:** 판단 지시를 제거하고 형식·출력 지시만 남긴 뒤 모든 종속 해시와 보고서를 재동결한다.

### F0P-B02 — P04 counterexample edge의 불완전 provenance

**확인 사실:** 두 P04 package의 `R04` edge는 `R-…-05 → R-…-12`를 지정하지만 `supporting_fact_ids`에는 `F-…-05`만 있다. `F-…-05`는 “같은 후보”라고만 말하고 대상 record `R-…-12` 식별은 `F-…-12`에 있다. 이는 두 block의 fixture/transformation manifest와 provenance/oracle-derived-relation report의 누락 0 주장과 충돌한다.

**추론:** P04만 oracle이 요구하는 `R-…-12` citation 연결을 명시적으로 받아 부당한 이점을 얻을 수 있다.

**권고:** edge의 전체 근거 결속을 수정하거나 edge를 제거하고 provenance·byte·manifest 해시를 재계산한다.

### F0P-M01 — aggregate set hash 계산 규칙 미정의

**확인 사실:** 26개 개별 fact-text SHA-256은 재현됐지만 `fact_set_sha256`과 `record_content_set_sha256`의 정렬·직렬화·구분자 규칙은 허용 문서에 없다. 값은 파일 간 동일하지만 독립 재계산할 수 없다.

**권고:** canonical aggregation 절차를 공개 묶음 안에 명시한다.

### F0P-N01 — stand-in 중심의 과도한 감사 표면

**확인 사실:** 91개 파일 중 `artifacts/` 26개와 `reports/` 20개가 포함된다. 다수 stand-in은 실제 구현·격리 증거가 아니다. README와 validation report가 경계를 설명해 위험은 완화된다.

**추론:** 단독 JSON 소비자는 운영 기록으로 오독할 수 있다.

**권고:** 필수 형식 예제와 비운영 placeholder 구분을 더 선명하게 유지한다.

### F0P-N02 — 후속 봉인 자료 오염 잔여 위험

**확인 사실:** README는 이름·문장·순서·option 위치·답 재사용을 금지하지만, 두 공개 block의 P03 marker 역할과 P04 relation-code 순서는 사실상 같다.

**권고:** 향후 봉인 block에서 공개 marker/relation topology와 record-role 순서도 복제하지 않는다고 명시한다.

## 나머지 결과

- block별 P01–P04는 13개 fact의 ID·record·project·timestamp·text가 canonical과 동일하고 질문은 모두 7개다.
- byte 비율은 block 1 `13.2578%`, block 2 `13.9885%`로 15% 이내며 실제 파일 길이로 재현됐다.
- 8개 run/package/question binding과 wave 동시성 최대 3이 일치한다.
- 명시적 A–D, H0/H1, 조건 우열, scoring/error-code 문자열은 runner-visible 집합에서 발견되지 않았다. 단, F0P-B01의 의미상 힌트가 존재한다.
- 자료는 공개·허구·미래 시점으로 표시되고 public oracle은 `hidden:false`다.
- 구현·실행·격리·S0·중앙 시스템 효과를 증명한다는 주장은 없다.

## 미확인 범위

- Draft 2020-12 validator-engine 통과
- 실제 transformer·validator·runtime 재현성
- 모델·세션·권한 격리
- 실행 결과와 S0 효과

검토자는 파일 수정, 코드 작성, S0 실행, git 작업을 하지 않았다.
