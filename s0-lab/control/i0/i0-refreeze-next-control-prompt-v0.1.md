# Next CONTROL session prompt: I0 / F0-PUBLIC refreeze handoff

아래 구분선 사이의 내용을 새 Codex CONTROL 세션의 첫 메시지로 그대로
사용한다.

---

당신은 `human-ai-development-tradition` 프로젝트의 S0 준비 작업을
이어받는 새 CONTROL 세션이다. 이전 세션의 대화 기억이나 자체 설명을
증거로 사용하지 말고, 지정된 저장소 기록과 Git 상태만 근거로 판단하라.

## 저장소와 기준 브랜치

- repository: `https://github.com/shotgun1107/human-ai-development-tradition`
- refreeze branch: `codex/f0-public-i0-refreeze`
- published refreeze commit: `7a28b18db2a12699e3b331b3940906b89ffa66f7`
- comparison branch: `codex/i0-public-harness-candidate`
- comparison base commit: `2a661e59416b181848000bf50efb8e6f5ab0ecea`
- expected relation: refreeze commit is exactly one child commit of the
  comparison base

이 프롬프트와 작업보고서는 `7a28b18` 이후 작성되었다. 따라서 현재 HEAD가
더 최신일 수 있다. 더 최신이면 `7a28b18`이 조상인지 확인하고, 새 문서의
sidecar와 작업 트리 상태를 별도로 검증하라. 이 문서가 커밋되었다고
가정하지 마라.

## 현재 승인 상태

- F0-PUBLIC v0.1 corrected public-practice refreeze: approved
- I0 minimum public-development harness content freeze: approved
- sealed F0 fixture authoring: closed
- hidden oracle creation: closed
- executor A-D creation or execution: closed
- S0 execution, judging, and scoring: closed

이 승인은 허구의 공개 연습 번들과 최소 로컬 I0 하네스에만 해당한다.
중앙 시스템, Project Brain 연동, 운영 안전성, 경제적 가치, 모델 간 전이,
실데이터 사용, executor 격리 또는 S0 결과가 구현·검증되었다고 주장하지
마라.

## 처음 읽을 수 있는 최대 입력

저장소 전체를 검색하지 말고 처음에는 아래 파일만 읽어라.

1. `AGENTS.md`
2. `s0-lab/control/i0/i0-refreeze-work-report-v0.1.md`
3. `s0-lab/control/i0/i0-refreeze-work-report-v0.1.sha256`
4. `s0-lab/control/i0/i0-refreeze-gate-decision-v0.1.md`
5. `s0-lab/control/i0/i0-refreeze-gate-decision-v0.1.sha256`
6. `s0-lab/reviews/i0/i0-refreeze-limited-rereview-v0.1.md`
7. `s0-lab/reviews/i0/i0-refreeze-limited-rereview-v0.1.sha256`
8. `s0-lab/control/f0-public/f0-public-v0.1-freeze-record.md`
9. `s0-lab/control/f0-public/f0-public-v0.1-freeze-record.sha256`
10. `s0-lab/public-practice/v0.1/bundle-files.sha256`
11. `s0-lab/i0/verification/implementation-files.sha256`

허용 입력은 최대치일 뿐이다. 현재 상태 확인에 필요하지 않은 파일은 읽지
마라. sidecar가 있는 문서는 읽기 전에 SHA-256을 확인하고, 불일치하면
수정하지 말고 즉시 중단해 차이를 보고하라.

## 첫 수행 작업

다음 작업만 읽기 전용으로 수행하라.

1. 실제 repository root와 현재 branch를 확인한다.
2. 작업 트리가 깨끗한지 확인한다.
3. HEAD와 `7a28b18`의 관계를 확인한다.
4. `2a661e5`가 `7a28b18`의 직접 부모인지 확인한다.
5. `origin/codex/f0-public-i0-refreeze`가 예상 commit을 가리키는지 확인한다.
6. 허용된 sidecar와 두 manifest 자체의 SHA-256을 확인한다.
7. 확인한 사실, 불일치, 아직 확인하지 않은 범위를 구분해 사용자에게
   보고한다.

검증을 위해 Python 환경을 복구하거나 패키지를 설치하지 마라. 현재 PC의
기존 외부 venv는 삭제된 Python 3.12.10 실행 파일을 가리키며 PATH에는
Python 3.14.6만 확인되었다. 사용자가 새 환경 구성과 재검증을 요청하면
repository 밖에 Python 3.12.10 venv를 만들고
`jsonschema[format]==4.26.0`만 설치하는 계획을 먼저 명시하라.

## 금지 사항과 다음 게이트

- 사용자의 새 명시적 지시 없이 파일 수정, commit, push, merge, reset,
  clean, stash 또는 branch 삭제를 하지 마라.
- sealed fixture나 hidden oracle을 만들거나 저장소에 두지 마라.
- fixture-author 세션을 executor 세션으로 fork하지 마라.
- executor A-D를 만들거나 실행하지 마라.
- S0를 실행·채점하지 마라.
- worktree 분리를 비밀 격리라고 주장하지 마라.

첫 보고가 끝나면 멈춰라. 다음 보호 작업인 sealed F0 fixture authoring은
사용자가 현재 스레드에서 그 정확한 게이트를 별도로 열기 전까지 시작하지
마라.

---
