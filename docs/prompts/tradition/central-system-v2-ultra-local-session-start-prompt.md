# Sol Ultra 로컬 독립 설계 세션 시작 프롬프트

이 작업은 `ai-development-tradition` 저장소 안에서 수행하는 **중앙 인간–AI 개발 전통 시스템 v2의 독립 기획·설계**다. 구현하거나 코드를 작성하지 마라.

## 1. 읽어야 하는 파일

다음 파일만 순서대로 읽어라.

1. `docs/tradition/central-system-v2-common-baseline.md`
2. `docs/tradition/purpose-and-philosophy.md`
3. `docs/tradition/research.md`
4. `docs/tradition/research-human-ai-joint-tradition.md`
5. `docs/tradition/central-system-v2-design-brief.md`
6. `docs/prompts/tradition/central-system-v2-independent-design-start-prompt.md`

먼저 1번 기준선에 적힌 SHA-256과 2~6번 파일의 실제 SHA-256을 비교하라. 하나라도 다르면 설계를 시작하지 말고 불일치한 파일만 보고하라. 모두 일치하면 6번 시작 프롬프트를 작업 지시로 삼아 끝까지 수행하라.

## 2. 읽지 말아야 하는 파일

저장소를 탐색하거나 다음 자료를 읽지 마라.

- `docs/tradition/system-design.md`
- `docs/tradition/monthly-review-playbook.md`
- `docs/tradition/roadmap-and-evaluation.md`
- `docs/tradition/design-competition-brief.md`
- `docs/tradition/design-competition-baseline-v1.md`
- `docs/tradition/design-competition-baseline-v1.1.md`
- `docs/tradition/candidate-system-design-v1.md`
- `docs/proposals/` 아래의 기존 제안서
- `docs/reviews/` 아래의 모든 심사 문서
- 다른 모델의 결과물, 이전 Ultra 결과물, Claude·Codex의 평가나 대화 기록

파일 위치 확인을 위해 저장소 전체를 검색하지 마라. 위 허용 목록의 경로를 직접 열어라. 추가 자료 조사와 인터넷 검색도 하지 마라.

## 3. 독립성과 범위

- 기존 설계를 수정하거나 확장하는 작업이 아니다. 허용된 목적·연구·브리프만 근거로 제로베이스에서 설계하라.
- 중앙 시스템 전체의 목표 구조와 검증 가능한 첫 구축 범위를 분리하라.
- Project Brain의 실제 메시지·API·파일 규격은 아직 미정이다. 중앙 시스템이 필요로 하는 경계와 책임만 설계하고 실제 통신 규격을 확정하지 마라.
- 문서 기획과 시스템 설계만 수행하라. 코드, 스키마 구현, 실행 파일, 테스트 코드, 자동화 구성은 만들지 마라.
- Git 커밋·브랜치·푸시를 하지 마라.

## 4. 출력

최종 결과 하나만 다음 경로에 새 파일로 작성하라.

`docs/proposals/v2/sol-ultra-central-tradition-system-v2-independent-proposal.md`

다른 파일은 수정하지 마라. 작성 후 다음만 보고하라.

1. 입력 해시 5/5 일치 여부
2. 결과 파일 경로
3. 선택한 전체 구조의 한 문장 요약
4. 첫 구축 범위의 한 문장 요약
5. 아직 결정하지 않은 가장 중요한 사항 세 가지

