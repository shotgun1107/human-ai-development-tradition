# 인간–AI 공동 개발 전통

**AI 개발 경험을 재사용 가능한 규칙과 테스트로 남기고, 다음 작업에서 다시 검증하기 위한 연구·개발 프로젝트입니다.**

세션이나 모델이 바뀔 때 실패 원인과 의사결정 근거가 사라지는 문제를 다룹니다. 대화 로그를 쌓는 대신 **출처 → 적용 조건 → 작업 자산 → 적용 결과 → 수정·철회**를 연결하는 외부 기억 체계를 설계하고, 이를 확인할 공개 입력용 하네스를 개발했습니다.

> 현재 범위는 **설계 및 S0 준비 구성요소**입니다. 중앙 시스템 전체, 실제 S0/E0 실험, 서비스 운영, 생산성·비용 개선, 모델 간 경험 전이를 구현·검증한 결과는 아닙니다.

## 프로젝트 한눈에 보기

| 항목 | 내용 |
| --- | --- |
| 문제 | AI가 이전 작업의 판단·실패·검증 조건을 이어받지 못하는 문제 |
| 접근 | 조건과 근거가 연결된 외부 기억, 단계별 검증, 사람의 승인과 철회 |
| 실제 산출물 | 설계 기준선, 공개 입력 검증 CLI, runtime·assembly 개발 소스, 시험·감사 기록 |
| 주요 기술 | Python 3.12, JSON Schema, PowerShell, C++/Win32, Git, MkDocs |
| 개발 방식 | 사람의 목적·제약·승인 아래 AI 보조 구현·시험·문서화와 분리된 검토 |
| 현재 단계 | `central-system-v2.1-s0-preparation` |

## 무엇을 만들었나

### 1. 공개 입력 검증 CLI

공개 연습자료의 무결성, JSON 형식과 결정적 변환 결과를 확인합니다. 변경된 manifest를 handler 실행 전에 거부하도록 보정했습니다.

- [현재 CLI 소스](s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1/implementation/s0_i0/)
- [실행 환경·명령과 검증 기록](s0-lab/audit-remediation/a07-public-cli-readiness-v0.1/README.md)
- [검증 범위에 대한 최종 판정](s0-lab/audit-remediation/a07-public-cli-readiness-v0.1/CONTROL-DISPOSITION.md)

### 2. runtime·assembly 개발 소스

runtime 구성과 공개 조립 경계의 감사 지적을 보정하고, 서로 겹치는 수정이 빠지지 않도록 전체 소스 묶음으로 통합했습니다.

- [runtime 개발 소스 20개](s0-lab/audit-remediation/a06-runtime-source-integration-v0.1/implementation/) — 프로필 구성, 경로 검사, native 파일 목록 보정
- [assembly 개발 소스 27개](s0-lab/audit-remediation/a08-public-assembly-source-integration-v0.1/implementation/) — 파일 접근 경계와 Windows 스트림 검사 보정

두 소스 묶음의 수용은 **개발 입력과 제한된 검증에 대한 판단**입니다. 하나의 native/live 실행 묶음으로 인증됐다는 뜻은 아닙니다.

### 3. 재사용 가능한 경험을 위한 설계

외부 기억에 무엇을 남길지뿐 아니라 언제 적용하지 말아야 하는지, 잘못된 규칙을 어떻게 철회할지까지 설계했습니다.

- [목적과 설계 원칙](docs/tradition/purpose-and-philosophy.md)
- [중앙 시스템 v2.1 준비 기준선](docs/tradition/central-system-v2-1-s0-preparation-baseline.md)
- [연구·설계 문서 지도](docs/tradition/README.md)

질문 계약 v0.14는 공개 설계 기준선으로 채택됐고, E0 v0.4는 설계 검토를 통과했습니다. 두 결과 모두 실제 실험이나 효과 검증은 아닙니다.

## 확인한 결과와 남은 한계

아래는 **2026-09-29에 기록된 검사**입니다. 이번 저장소 정리는 해당 시험을 다시 실행하거나 결과 범위를 넓히지 않았습니다.

| 대상 | 기록된 결과 | 해석 범위 |
| --- | --- | --- |
| 공개 CLI | `integrity`, `schema-check`, `verify` 및 `pip check` 각각 exit 0 | 해당 Windows 호스트와 준비된 의존성의 공개 입력 점검 |
| 공개 입력 | 90개 파일, 11개 schema, 8개 package 바이트 비교 확인 | S0 실행·점수·AI 성능 측정 아님 |
| runtime 소스 통합 | 소스 검사 24개/하위 사례 205개, 프로필 검사 59개 통과 | 실제 native lifecycle·전체 환경 인증 아님 |
| assembly 소스 통합 | 검사 77개/하위 사례 485개 통과 | 실제 Windows 전체 리허설·보안 완전성 증명 아님 |

[감사 수정·유지보수 마감 근거](docs/maintenance/MAINTENANCE-CLOSEOUT-2026-09-29.md)와 각 묶음의 `CONTROL-DISPOSITION.md`에 수용 범위가 기록돼 있습니다. 날짜가 있는 README의 `REVIEW PENDING`은 그 문서가 동결된 당시 상태이며, 뒤에 작성된 판정과 구분합니다.

현재 미검증 범위는 중앙 시스템·Project Brain 통합, 전체 Windows 리허설, S0/E0 실행, 운영 안전성, 경제적 효과와 모델 간 전이입니다. 기록된 테스트 수를 생산성 향상률이나 사업 성과로 바꾸지 않습니다.

## 공개 CLI 시작하기

아래 안내는 **Windows x64 / Python 3.12**용입니다. 가상환경은 Git에 포함되지 않습니다. 저장소 루트에서 실행하며, 새 PC의 동작은 별도 확인이 필요합니다.

### 환경 준비

```powershell
py -3.12 -m venv .venv-public
& '.\.venv-public\Scripts\python.exe' -I -B -X utf8 -m pip --isolated install --require-hashes --only-binary=:all: --index-url https://pypi.org/simple -r '.\s0-lab\audit-remediation\a07-public-cli-readiness-v0.1\requirements.lock.txt'
```

이미 준비된 환경을 사용한다면 설치를 반복할 필요는 없습니다. lock 파일은 검증 당시 Windows 의존성의 버전과 wheel 해시를 고정합니다.

### 공개 입력 확인

```powershell
& '.\.venv-public\Scripts\python.exe' -I -B -X utf8 -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path.cwd() / 's0-lab/audit-remediation/a04-i0-cli-authentication-v0.1/implementation')); from s0_i0.cli import main; raise SystemExit(main(['verify']))"
```

같은 진입점에서 `verify`를 `integrity` 또는 `schema-check`로 바꾸면 각 검사를 따로 확인할 수 있습니다. 이 세 명령은 공개 준비 자료를 읽는 CLI이며, 새 fixture·oracle·S0 실행을 만들지 않습니다. 위 상대경로 표기는 기존 진입점에 맞춘 안내이고 이번 문서 정리에서 새로 실행 검증한 명령은 아닙니다. 당시 실제 명령과 전체 출력은 [A07 기록](s0-lab/audit-remediation/a07-public-cli-readiness-v0.1/README.md)에 있습니다.

## 읽는 순서

1. 이 README — 목적, 실제 구현, 검증과 한계
2. [개발 참여 규약](CONTRIBUTING.md) — 작업·브랜치·커밋·문서 규칙
3. [프로젝트 문서 안내](DOCUMENT-GUIDE.md) — 현재 소스와 과거 근거의 위치
4. [현재 연구 작업 원장](s0-lab/control/CURRENT-WORK-LEDGER.md) — 개별 판정과 남은 선행조건
5. [공개 조립 workstream](s0-lab/control/workstreams/public-end-to-end-assembly-rehearsal.md) — 전체 실행 경로의 의존 관계

AI 작업 지침은 [AGENTS.md](AGENTS.md), 작업별 상태 기록은 `.ai/tasks/`에 있습니다. 문서 링크와 Git 존재 자체가 연구 자료의 접근·실행 권한을 부여하지는 않습니다.

## 이력과 보존

현재 안내와 원래 실험·검토 근거를 구분합니다. 과거 판정, 실패 기록, 동결 파일과 해시는 원문으로 보존하며 최신 상태처럼 다시 쓰지 않습니다. 커밋 제목 정리는 파일 내용·작성자·개발 날짜를 바꾸지 않는 Git 이력 정리입니다. 원래 커밋과 별도 작업의 복구 지점은 `archive/` 태그에 보관합니다.
