# 인간–AI 공동 개발 전통

> **CONTROL/운영용 개요 — 독립 실험 입력으로 자동 사용 금지.** 새 세션이나 공개 파일이라는 이유만으로 읽기 권한이 생기지 않습니다. 독립 검토자·실행자는 root `AGENTS.md`와 해당 역할의 정확한 허용 입력 목록을 먼저 따르십시오. 이 개요와 연결 문서에는 과거 설계 선택·검증 상태가 포함됩니다.

사람과 AI가 여러 프로젝트에서 얻은 검증된 경험을 다음 AI 세대가 이어받도록 만드는 **외부 기억·작업 규칙·검증 체계** 연구 프로젝트입니다.

이 프로젝트의 목표는 사용자의 개인 성장 일지를 만드는 데 있지 않습니다. 모델과 세션이 바뀌어도 같은 실수를 줄이고, 잘 작동한 Skill·프롬프트·체크리스트·테스트·판단 근거를 검증 가능한 형태로 계승하는 것이 핵심입니다.

> 현재는 연구·기획·S0 준비 단계입니다. 중앙 시스템, Project Brain 연동, 운영 안전성, 경제성, 모델 간 전이는 아직 구현되거나 검증되지 않았습니다.

다른 PC나 새 Codex 세션에서 작업을 재개하려면 먼저 루트
[`AGENTS.md`](./AGENTS.md)의 현재 정책을 읽으십시오. 이후
[집 Codex 시작점](./HOME-CODEX-START.md)은 역사적 인수인계 맥락으로만 읽고,
현재 Git·해시·게이트를 다시 검증하십시오.

## 회사 PC에서 작업 시작

기준 폴더는 **`C:\Users\SSAFY\Documents\ai-development-tradition`** 하나입니다.
현재 남아 있는 프로젝트 소스·문서·기존 검증 도구는 이 폴더 아래에서 사용합니다.

- **현재 상태와 최종 판정:** [현재 작업 기록](./s0-lab/control/CURRENT-WORK-LEDGER.md)을 먼저 확인합니다. 2026-09-29의 소스 통합 두 묶음과 공개 실행 환경은 각각 검사·독립 검토·제한된 승인을 마쳤고, **현재 작업 폴더의 한정된 감사 수정·유지보수를 공식 마감했습니다.** 전체 Windows 실행이나 S0 완료 판정은 아닙니다.
- **짧은 결과 설명:** [감사 수정·유지보수 마감 요약](./docs/maintenance/MAINTENANCE-CLOSEOUT-2026-09-29.md). 과거 판정이나 동결 README의 `REVIEW PENDING`을 현재 지시로 사용하지 않습니다. 현재 개별 판정은 각 묶음의 나중에 작성된 `CONTROL-DISPOSITION.md`가 기록합니다.
- 공개 CLI는 **A04의 I0 소스**를 사용합니다. [A07 실행 명령](./s0-lab/audit-remediation/a07-public-cli-readiness-v0.1/README.md)과 [최종 승인](./s0-lab/audit-remediation/a07-public-cli-readiness-v0.1/CONTROL-DISPOSITION.md)을 따라 프로젝트 안의 `.venv-public`에서 사용합니다. 확인된 명령은 `integrity`, `schema-check`, `verify`이며 S0 실행이 아닙니다.
- 후속 개발용 소스는 [A06 runtime 소스 통합](./s0-lab/audit-remediation/a06-runtime-source-integration-v0.1/CONTROL-DISPOSITION.md)과 [A08 공개 조립 소스 통합](./s0-lab/audit-remediation/a08-public-assembly-source-integration-v0.1/CONTROL-DISPOSITION.md)의 `implementation/`입니다. A08은 위 CLI의 실행 경로가 아니며, 이 소스들이 새 native 실행 묶음으로 인증됐다는 뜻도 아닙니다. [Windows 공개 조립의 남은 실행 조건](./s0-lab/control/workstreams/public-end-to-end-assembly-rehearsal.md)은 별도로 유지합니다.
- E0 비용을 다룰 때는 [원래 v0.4 비용 문서](./docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.4.md)와 [승인된 비용 정정본](./s0-lab/audit-remediation/a03-cost-definition-v0.1/COST-DEFINITION-ERRATUM.md)을 함께 적용합니다. 원본만으로 중복 비용식을 다시 사용하지 않습니다.
- 용도별 위치와 외부 설치 환경: [프로젝트 문서 안내](./DOCUMENT-GUIDE.md)
- 소스·시험·도구: `s0-lab/`의 각 구성요소 안에서 `implementation/`, `tests/`, `tools/`를 사용
- 연구·설계 문서: `docs/tradition/`, `docs/proposals/`, `docs/reviews/`
- 지원서용 요약: [지원서 프로젝트 맥락](./docs/application/PROJECT-CONTEXT-FOR-APPLICATION.md)

동결 경로와 해시를 유지하기 위해 기존 소스·검증 폴더를 임의로 합치거나
평탄화하지 않았습니다. 외부의 과거 worktree를 작업 시작점으로 사용하지 않습니다.
이 경로 정리가 중앙 시스템·S0·실제 리허설의 실행 준비 완료를 뜻하지는 않습니다.

## 왜 만드는가

좋은 모델을 사용하거나 새 모델의 기본 성능이 높아져도 다음 문제가 반복됩니다.

- 새 세션이 과거 판단과 실패 이유를 모른다.
- 같은 실수와 비효율적인 AI 사용법을 프로젝트마다 다시 겪는다.
- 성공 사례는 남아도 어떤 조건에서 성공했는지 검증되지 않는다.
- 체크리스트와 Skill이 늘어나지만 실제 효과와 폐기 기준이 없다.
- 모델이 바뀌면 경험의 맥락과 근거가 함께 전달되지 않는다.

따라서 경험을 단순히 보관하는 대신 다음 순환을 만들려고 합니다.

```text
사실·사건
  → 검증된 경험
  → 교훈 후보
  → 사람 승인
  → Skill·프롬프트·체크리스트·테스트
  → 다음 프로젝트 적용
  → 효과·반례 측정
  → 유지·수정·축소·폐기
```

초기 방식은 모델 파인튜닝이 아닙니다. 검색 가능한 문서, 출처와 버전이 연결된 규칙, RAG, 프롬프트 주입, 재현 가능한 테스트처럼 사람이 검토하고 철회할 수 있는 외부 기억으로 시작합니다.

## 초기 연구·준비 경로 요약

아래 표는 초기 준비 단계의 역사적 요약입니다. 후속 공개 조립·실행 환경 작업과 2026-09-16~17 감사 수정의 현재 진행 위치는 위의 **현재 작업 기록**을 따릅니다. 아래의 구버전 대기·거부 상태를 최신 재개 지시로 사용하지 않습니다.

| 단계 | 상태 | 의미 |
|---|---|---|
| 분야 횡단 문헌 조사 | 완료 | AAR, SRE, 조직 기억, 안전사고 학습, 품질관리, 인간–AI 협업 등을 조사 |
| 중앙 시스템 v2 기획·설계 | 후보 동결 | 독립 설계·외부 심사·제한 수정 완료, 운영 효과는 미검증 |
| S0 프로토콜 v0.3 | 동결 | 합성 논리 시험의 역할·격리·중단·판정 규칙 고정 |
| SM0·SM1 데이터 형식 | 동결 | 답안과 10개 manifest/schema 형식 고정 |
| F0-PUBLIC v0.1 | 동결 | 비밀 없는 공개 합성 연습자료 작성·독립 검토 완료 |
| I0 최소 구현 | 제한 동결 | 공개 harness와 F0-PUBLIC refreeze 완료, S0·전체 시스템 검증은 아님 |
| F0-PUBLIC 질문 계약 v0.4 | 거부 | 독립 심사에서 Critical 4·Major 3, 실패 후보로 보존 |
| 질문 계약 v0.5 | 설계 대기 | 별도 경로에서 재설계해야 하며 후보 문서는 아직 없음 |
| E0 효과시험 v0.1 | 독립 심사 전 | 분리 브랜치에 설계 후보만 존재, 자료·구현·실행은 닫힘 |
| F0-SEALED 작성·S0 실행·판정 게이트 | 미착수 | 기존 53개 보존 파일은 Git 추적되지만 AI 내용 접근과 실행 권한은 닫힘 |

단계별 배경은 [S0 작업 환경](./s0-lab/README.md)과 [F0-PUBLIC 동결 기록](./s0-lab/control/f0-public/f0-public-v0.1-freeze-record.md)에 보존돼 있습니다. 각 문서의 기준일과 역할별 접근 제한을 확인합니다.

## 핵심 원칙

- 사실, 추론, 제안, 시험 결과를 구분합니다.
- 성공·실패·결정·실험·반례를 함께 다룹니다.
- 출처, 적용 조건, 금지 조건, 버전, 소유자, 재검토일을 남깁니다.
- 한 프로젝트의 경험을 곧바로 범용 규칙으로 승격하지 않습니다.
- AI가 만든 요약이나 점수는 사람 승인 전까지 효력이 없습니다.
- 개인정보·비밀·실제 고객 자료를 중앙 저장소에 복제하지 않습니다.
- 잘못된 교훈은 덮어쓰지 않고 수정·강등·폐기 이력을 남깁니다.
- worktree와 세션 분리는 편집 충돌을 줄일 뿐, 비밀정보 격리를 자동 보장하지 않습니다.

## 저장소 지도

- [`docs/tradition/`](./docs/tradition/README.md) — 목적·철학, 문헌 조사, 중앙 시스템 기획·설계, 월간 회고와 평가
- [`docs/proposals/`](./docs/proposals/) — 서로 다른 모델이 독립적으로 작성한 설계안과 통합 후보
- [`docs/reviews/`](./docs/reviews/) — 독립 비평, 재심사, 최종 판단 기록
- [`independent-outsider/`](./independent-outsider/README.md) — 기존 설계와 분리된 외부 관점의 조사·심사
- [`s0-lab/`](./s0-lab/README.md) — S0 프로토콜, 동결 schema, 공개 합성 연습자료와 검토 기록
- [`AGENTS.md`](./AGENTS.md) — 현재 구현·실행 게이트와 역할 격리 규칙

현재 상태를 확인한 뒤 연구 배경을 더 읽을 문서는 다음과 같습니다.

1. [목적과 철학](./docs/tradition/purpose-and-philosophy.md)
2. [프로젝트 전체 문서 지도](./docs/tradition/README.md)
3. [S0 자료의 버전별 안내](./s0-lab/README.md) — 과거 안내이며 현재 운영 판정은 위 작업 기록을 우선합니다.

## 문서 사이트로 보기

이 저장소는 Material for MkDocs 설정을 포함합니다. 회사 PC에서는 이미
프로젝트 안에 있는 문서 전용 가상환경을 사용합니다. 활성화나 전역 `python`
선택에 의존하지 않고 아래처럼 실행하십시오.

```powershell
Set-Location -LiteralPath 'C:\Users\SSAFY\Documents\ai-development-tradition'
& '.\.venv-docs\Scripts\python.exe' -m mkdocs serve --config-file '.\mkdocs.yml'
```

실행 후 브라우저에서 `http://127.0.0.1:8000`을 열면 주요 기획·연구 문서를 탐색할 수 있습니다.

정적 문서만 만들려면 같은 위치에서
`& '.\.venv-docs\Scripts\python.exe' -m mkdocs build --config-file '.\mkdocs.yml'`을
사용합니다. 출력은 프로젝트 내부의 `.mkdocs-site/`입니다. 기존
`requirements-docs.txt`는 문서 환경 의존성 기록이며, 회사 PC의 현재 문서
빌드는 2026-09-16에 확인했습니다. I0/I1 실행 환경과는 별개입니다.

## 현재 하지 않는 것

- 모델 파인튜닝이나 자동 자기수정
- 실제 고객·개인·비밀 자료를 사용한 시험
- 무승인 교리 배포 또는 AI 단독 최종 결정
- 중앙 시스템·Project Brain·경제적 가치가 이미 검증됐다는 주장
- 공개 연습자료를 실제 S0 결과로 사용하는 일

## 검증 경계

현재 공개 준비 경로에서는 **F0-PUBLIC v0.1과 I0 최소 harness가 제한된 범위에서 동결**됐습니다. 이후 질문 계약 URC v0.4는 독립 심사에서 거부됐으므로 v0.5를 별도 버전으로 다시 설계해야 합니다. 이는 S0 또는 중앙 시스템의 효과가 입증됐다는 뜻이 아닙니다.

병렬 경로의 E0 v0.1은 이 초기 요약 시점에 전통 효과시험의 설계 후보·독립 심사 전 상태였습니다. 이 과거 요약만으로 다음 작업을 선택하거나 자료 작성·구현·실행을 시작하지 않습니다. 현재 후속 작업은 root `AGENTS.md`, 현재 작업 기록과 해당 작업의 명시적 승인 범위를 다시 확인합니다.
