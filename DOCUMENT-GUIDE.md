# 프로젝트 문서 안내 및 정리 기록

> **CONTROL/유지보수용 자료 — 새 독립 검토·실험 역할의 기본 입력이 아님.** 이 문서와 연결된 파일·생성 사이트·검색 색인은 과거 판단과 상태를 전달할 수 있다. 새 세션이라는 이유만으로 전체를 읽히지 않는다. 운영 인계 담당자는 [세션 전환 영향 기록](C:/Users/SSAFY/Documents/ai-development-tradition/docs/maintenance/SESSION-TRANSITION-IMPACT-2026-09-16.md)을 확인하고, 연구 역할에는 별도 동결된 허용 입력만 제공한다.

> 정리일: 2026-09-16. 이 문서는 탐색용 색인과 파일 정리 기록이다.
> 기술 후보의 판정·동결·실행 권한을 바꾸지 않는다. 현재 운영 정책은 [AGENTS.md](C:/Users/SSAFY/Documents/ai-development-tradition/AGENTS.md)가 우선한다.

**최종 처리:** 1차 정리에서 보류했던 Documents 하위 작업 폴더 14개는 추가 확인 후 제거했고, 중복 백업 1개는 휴지통으로 보냈다. 메인 프로젝트와 Git 브랜치·커밋 이력은 유지했다. 최종 근거와 복원용 커밋은 §7을 따른다. §4·§6의 보존 기록은 추가 확인 전의 1차 처리 이력이다.

## 0. 회사 PC의 단일 작업 기준

**작업을 시작할 경로는 `C:\Users\SSAFY\Documents\ai-development-tradition`이다.** 현재 남아 있는 프로젝트 전용 소스·문서·검증 도구는 이 안에 있다. 별도 실행 프로그램이나 경로 연결용 스크립트를 새로 만들지 않고, 기존 도구를 이 루트에서 사용한다.

### 최종 폴더 구조

```text
ai-development-tradition/
├─ README.md                 작업 시작과 문서 실행 방법
├─ DOCUMENT-GUIDE.md         용도별 위치·외부 의존성·정리 기록
├─ AGENTS.md                 현재 운영·접근 규칙
├─ docs/
│  ├─ tradition/             목적·연구·설계·E0 문서 / 문서 사이트 원문
│  ├─ proposals/             설계안과 통합 후보
│  ├─ reviews/               설계 심사 기록
│  └─ application/           지원서용 프로젝트 요약
├─ s0-lab/
│  ├─ i0/ ... i3/            각 구성요소의 implementation·tests·tools·검증 기록
│  ├─ assembly-rehearsal/    공개 조립·runtime 준비 관련 버전별 자료
│  └─ control/               명세·판정·기존 공통 검사 도구
├─ independent-outsider/    독립 조사·심사 기록
├─ .codex/agents/            프로젝트 역할 설정
├─ .venv-docs/               기존 문서용 Python 가상환경
├─ .mkdocs-site/             재생성 가능한 문서 사이트 출력
├─ mkdocs.yml               문서 사이트 설정·목차
├─ requirements-docs.txt     문서 의존성 기록
└─ .git/                    원본 Git 이력·브랜치·관리 정보
```

위 구조는 일상 탐색에 필요한 주요 위치를 나타낸다. 미분류 항목이나 접근 제한된 자료의 내부 목록을 공개하는 전체 인벤토리가 아니다. `s0-lab`의 권한 제한은 그대로 유지한다.

### 바로 사용할 문서 명령

```powershell
Set-Location -LiteralPath 'C:\Users\SSAFY\Documents\ai-development-tradition'
& '.\.venv-docs\Scripts\python.exe' -m mkdocs serve --config-file '.\mkdocs.yml'
```

문서 주소는 `http://127.0.0.1:8000`이며 종료는 실행 터미널에서 Ctrl+C다. HTML 생성만 필요하면 같은 Python으로 `-m mkdocs build --config-file '.\mkdocs.yml'`을 실행한다. 출력은 루트 아래 `.mkdocs-site`에 모인다.

현재 가상환경은 실제 `sys.prefix`가 이 프로젝트의 `.venv-docs`로 잡히고, MkDocs 1.6.1 / Material 9.7.7을 제공한다. `pyvenv.cfg`의 `command`에 남은 예전 생성 위치는 역사 기록이며 현재 작업 루트가 아니다. 현재 경로의 `python.exe -m mkdocs`로 빌드 성공을 확인했다. 옛 생성 경로나 전역 Python 선택에 의존하는 실행 안내는 루트 README에서 위 방식으로 바꿨다.

기존 목차에 없던 S0·E0 경계 및 E0 v0.4 설계·측정·비용·심사 항목도 `mkdocs.yml` 메뉴에 연결했다. 버전별 원문과 동결 해시는 변경하지 않았다.

### 기존 검증 도구의 위치

| 용도 | 프로젝트 안의 위치 | 주의 |
|---|---|---|
| 공개 I0 CLI | `s0-lab/i0/implementation/s0_i0/cli.py` | 해당 README의 허용 입력과 Python 의존성 필요 |
| I1 검증 | `s0-lab/i1/tools/verify-i1.ps1` | 승인된 `ExpectedManifestSha256` 필요 |
| I2 검증 | `s0-lab/i2/tools/verify-i2.ps1` | 승인된 `ExpectedManifestSha256` 필요 |
| I3 검증 | `s0-lab/i3/tools/verify-i3.ps1` | 승인된 `ExpectedManifestSha256` 필요 |
| Markdown·sidecar 검사 | `s0-lab/control/tools/verify-text-artifacts.ps1` | 적용 대상과 SelfTest 규칙은 AGENTS를 따름 |

실행 도구를 별도 `tools` 폴더에 중복 복사하지 않았다. I1–I3는 자신의 위치에서 저장소 루트를 계산하므로 현재 경로를 유지하는 편이 기존 인증·상대경로 계약에 맞는다. 현 파일에서 즉석으로 구한 해시를 승인값 대신 넣거나, 준비 문서를 실제 S0 실행 승인으로 사용하지 않는다.

### 별도 위치를 유지하는 항목

| 항목 | 실제 위치·접근 | 이유 |
|---|---|---|
| 기본 Python 3.12.10 | `C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe` | 설치된 공유 런타임. 프로젝트 가상환경이 이 설치를 사용하므로 디렉터리만 옮기면 깨질 수 있음. 문서 작업에서는 프로젝트 내 `.venv-docs/Scripts/python.exe`를 사용 |
| Visual Studio Build Tools | `C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools` | 설치 관리되는 공용 컴파일러·라이브러리. 저장소로 복사하거나 이전하지 않음. 실제 native 빌드 시 승인된 기존 빌드 절차에서 접근 |
| Windows SDK | `C:/Program Files (x86)/Windows Kits/10` | OS·빌드 환경의 공유 의존성. 설치 위치 유지 |
| Codex 관리용 worktree | `C:/Users/SSAFY/.codex/worktrees/4874/ai-development-tradition` | 앱 관리 영역. 현재 HEAD의 조상 커밋이며 변경·ignored 파일 0개인 사본으로 확인. 이곳에만 있는 소스를 가져올 필요가 없으며 일상 작업 경로로 사용하지 않음. 이번 요청에서 앱 내부 경로를 임의로 이동하지 않음 |
| 검사 중 임시 snapshot | 운영체제의 사용자 Temp 경로 | 기존 I1–I3 검사기가 인증한 입력을 분리 실행하고 정리하는 일회용 공간. 보존 원본이나 사람이 관리할 작업 폴더가 아니므로 저장소 내부로 강제 변경하지 않음 |
| 앱 설치·작업 이력·계정 설정 | Codex의 사용자 데이터·설치 영역 | 여러 프로젝트가 공유하는 앱 자료. 소스 저장소로 수집하지 않음 |

### 확인 범위와 남은 실행 제한

- 공개 구현·시험·도구·역할 설정 260개 파일에서 절대경로와 삭제된 작업 폴더 참조를 제한적으로 검색했다. 삭제된 작업 폴더를 실행 소스 경로로 고정한 참조는 발견하지 못했다. 시험용 가상 Windows 경로는 실제 이동 대상이 아니므로 수정하지 않았다.
- 문서 가상환경의 현재 경로와 import, 기존 MkDocs 빌드 및 프로젝트 내부 HTML 생성을 확인했다. 새 launcher·runtime bridge·검증 harness는 만들지 않았다.
- 기본 Python과 문서 가상환경에는 I0/I1에 필요한 `jsonschema[format]==4.26.0`이 현재 설치돼 있지 않다. 문서 환경을 구성요소 검증 환경으로 오인하지 않는다. 이 정리에서 패키지 설치나 새 실행 환경 복구를 수행하지 않았고, I0–I3의 회귀 시험이 새로 통과했다고 주장하지 않는다.
- 9월 9일 감사의 일부 Temp 작업본·생성물은 이번 정리 전에 이미 지정 경로에서 접근되지 않았다. 존재하지 않는 파일을 모았거나 최신 native 후보를 복구했다고 보고하지 않는다. 그 후보를 재개할 때는 별도로 원본 확보와 실행 선행조건 확인이 필요하다.
- 제품 전체 실행·native lifecycle·S0·실제 효과 시험의 기존 제한은 변하지 않는다. 현재 폴더 정리와 문서 빌드 성공이 그 검증을 대신하지 않는다.

## 1. 용도별로 찾기

| 필요한 내용 | 위치 | 읽을 때의 기준 |
|---|---|---|
| 현재 운영·접근·변경 규칙 | [AGENTS.md](C:/Users/SSAFY/Documents/ai-development-tradition/AGENTS.md) | 현재 정책. 문서 정리가 구현·실험·Git 게시 승인은 아님 |
| 프로젝트의 목적과 철학 | [목적 헌장](C:/Users/SSAFY/Documents/ai-development-tradition/docs/tradition/purpose-and-philosophy.md) | 왜 만들고 무엇을 지키려는지 설명 |
| 연구·설계 문서 지도 | [문서 개요](C:/Users/SSAFY/Documents/ai-development-tradition/docs/tradition/README.md) | 문헌 조사, 초기 설계, 경쟁 설계, 현행 기준선을 구분해서 읽기 |
| 목표 중앙 시스템의 설계 | [v2.1 통합 후보](C:/Users/SSAFY/Documents/ai-development-tradition/docs/proposals/v2/central-tradition-system-v2-integrated-candidate-v2.1.md) | 목표 구조와 검증 전 가설. 제품 완성 기록이 아님 |
| S0 준비의 설계 기준선 | [S0 준비 기준선](C:/Users/SSAFY/Documents/ai-development-tradition/docs/tradition/central-system-v2-1-s0-preparation-baseline.md) | 설계 채택의 범위와 남은 검증 경계 |
| 공개 시험 준비·검증 자료의 시작점 | [S0 작업 환경](C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/README.md) | 버전별 과거 상태와 현재 운영 정책을 혼동하지 않기. 연결된 파일도 역할별 접근 제한을 따름 |
| 독립 외부 조사·심사 기록 | [독립 외부 작업 구역](C:/Users/SSAFY/Documents/ai-development-tradition/independent-outsider/README.md) | 설계와 심사 근거를 보존한 역사 자료. 새 독립 역할의 허용 입력과는 별개 |
| 지원서 작성용 프로젝트 설명 | [지원서용 프로젝트 맥락](C:/Users/SSAFY/Documents/ai-development-tradition/docs/application/PROJECT-CONTEXT-FOR-APPLICATION.md) | 다른 지원서 프로젝트에 전달할 자기완결적 요약. 본인 기여와 검증 한계를 포함 |
| 과거 PC·세션 인계 맥락 | [집 Codex 시작점](C:/Users/SSAFY/Documents/ai-development-tradition/HOME-CODEX-START.md) | 2026-08-07의 역사 기록. 현재 상태·Git 동기화 규칙의 대체물이 아님 |
| 문서 사이트 생성 설정 | [mkdocs.yml](C:/Users/SSAFY/Documents/ai-development-tradition/mkdocs.yml) | 원문은 `docs/tradition`, 생성물은 `.mkdocs-site` |

### 기존 폴더를 유지한 이유

- `docs/tradition`: 목적·문헌·설계·평가 문서. 구판도 설계 변화의 근거이므로 삭제하지 않았다.
- `docs/proposals`와 `docs/reviews`: 설계안과 심사의 관계를 보존한다. 새 폴더로 일괄 이동하면 상대 링크와 검증된 경로가 달라질 수 있다.
- `independent-outsider`: 독립 조사와 심사 단계의 원래 구조를 유지한다.
- `s0-lab`: 프로토콜·명세·공개 구현·시험·판정 기록을 원래 버전별 경로에 보존한다. 오래됐거나 실패한 후보라는 이유만으로 불필요한 자료로 분류하지 않았다.
- `docs/application`: 이번에 분리한 지원서·대외 설명용 요약 위치다. 원본 실험 자료를 복제하는 폴더가 아니다.

동결 문서·manifest·sidecar는 본문과 위치를 그대로 보존했다. 이번 정리는 미완료 기술 작업의 상태나 감사 결과를 새로 판정하지 않는다.

## 2. 이동한 파일

| 이전 위치 | 새 위치 | 이유 |
|---|---|---|
| 프로젝트 루트의 `PROJECT-CONTEXT-FOR-APPLICATION.md` | `docs/application/PROJECT-CONTEXT-FOR-APPLICATION.md` | 개발 운영 문서와 지원서용 파생 설명을 구분하기 위해 이동 |

파일 본문은 바꾸지 않았다. 이동 전·후 SHA-256: `5efeb580422d1388e076f60ea607ccb958c0bdcb542de65eb7bc358c3c2efb0d`.

위 값은 위치 이동 당시의 동일성 기록이다. 이후 2026-09-16 세션 전환 조치에서 요약 파일 맨 위에 역할별 입력 경고를 추가했으므로, 현재 파일 해시는 위 이동 당시 값과 다르다. 당시 이동의 동일성과 이후 문서 변경을 혼동하지 않는다.

이전 대화의 파일 링크는 옛 위치를 가리킬 수 있으므로, 앞으로는 위 새 링크를 사용한다. 다른 프로젝트에 이미 첨부한 사본은 변경하지 않았다.

## 3. 휴지통으로 보낸 항목

영구 삭제하지 않았으며 Windows 휴지통에서 복원할 수 있다. 휴지통을 비우지 않았으므로 디스크 공간 확보량으로 계산하지 않는다.

| 원래 절대 경로 | 확인한 상태·근거 | 처리 |
|---|---|---|
| `C:/Users/SSAFY/Documents/ai-development-tradition/.mkdocs-site` | `mkdocs.yml`의 명시적 사이트 출력 폴더. `.gitignore` 대상, Git 추적 파일 0개, 파일 68개·하위 폴더 24개·4,621,768 bytes. reparse point 0개. 확인 시 해당 프로젝트·MkDocs를 실행하는 별도 프로세스를 찾지 못함 | 재생성 가능한 문서 사이트 출력물을 휴지통으로 이동. 원문·설정·문서 빌드 환경은 유지 |
| `C:/Users/SSAFY/Documents/ai-development-tradition-worktrees` | 이 프로젝트의 2026-09-01 공개 실행 기록에 `authenticode-v05` worktree 생성 위치로 등장. 정리 직전 자식 항목 0개, 해당 경로와 하위에 현재 등록된 worktree 0개, reparse point 없음 | 사용 종료 후 남은 빈 컨테이너 폴더만 휴지통으로 이동. 내부 worktree나 소스 파일을 삭제한 것이 아님 |

작업 기록의 식별자: `exec-0cbe8c3a-9f37-42ce-b4d6-53592f735876`, 2026-09-01 03:42:42 UTC, 성공 종료. 현재 실제 비어 있음과 Git 등록 상태를 별도로 대조했다.

## 4. 1차 정리에서 보존한 항목과 이유

| 대상 | 보존 이유 |
|---|---|
| `.venv-docs` | 문서 사이트를 다시 만들 때 쓰는 기존 환경. 실행 중인 프로세스가 없다는 이유만으로 재사용 가능한 환경을 불필요한 캐시로 판단하지 않음 |
| 기존 추적 문서·소스·검증 결과·동결 파일 | 링크·해시·과거 판단에 연결된 원자료. 이번 정리에서 내용과 경로를 변경하지 않음 |
| F0 보호 자료 | 내용과 내부 파일명을 읽지 않음. 허용된 집계 확인만 수행하고 모두 보존 |
| 등록된 Documents 하위 Git worktree 14개 | 관련성은 Git 등록 정보로 확인했지만 단순 임시 생성물은 아님. 미커밋 상태가 깨끗하다는 사실만으로 각 브랜치 작업 위치의 폐기까지 확정하지 않음 |
| `ai-development-tradition-pre-main-sync-backup-20260811` | 이름상 관련 후보이지만 백업의 중복성·복구 필요성을 입증하지 못했으므로 보존. 내용은 탐색하지 않음 |
| 그 밖의 미분류 항목 | 프로젝트 귀속 또는 삭제 가능성이 불분명하므로 이름·내용을 불필요하게 노출하거나 변경하지 않음 |
| 다른 프로젝트·개인·시스템 항목 | 정리 대상에서 제외. 설치 프로그램·시스템 캐시를 이 프로젝트의 일회용 자료로 추정하지 않음 |

1차 정리에서 보류했던 Git 작업 폴더는 `C:/Users/SSAFY/Documents/` 아래 다음 14개다. 당시 worktree 등록 정보와 일치했고 각 `git status` 집계는 0개였다. 이후 추가 확인을 마쳐 아래 §7과 같이 작업 폴더만 제거했다. 브랜치와 커밋은 제거하지 않았다.

- `ai-development-tradition-authenticode-v01-independent-review`
- `ai-development-tradition-authenticode-v02-independent-rereview`
- `ai-development-tradition-authenticode-v02-revision`
- `ai-development-tradition-authenticode-v03-revision`
- `ai-development-tradition-company-handoff-20260810`
- `ai-development-tradition-e0-effect-test`
- `ai-development-tradition-h2c-authenticode-20260825`
- `ai-development-tradition-handoff-20260809`
- `ai-development-tradition-s0-isolation-review-v03`
- `ai-development-tradition-s0-isolation-v03`
- `ai-development-tradition-s0-isolation-v03-rereview-brief`
- `ai-development-tradition-s0-protocol-final-refreeze-v03-canonical-r1`
- `ai-development-tradition-s0-protocol-refreeze-v03-canonical-r1`
- `ai-development-tradition-s0-protocol-rereview-v03-canonical-r1`

## 5. 확인 범위와 확인하지 않은 것

- 프로젝트의 현재 Git 상태, root 정책, 문서 지도, MkDocs 설정, ignore 규칙, worktree 등록 정보와 이 작업의 공개 실행 기록을 확인했다.
- 현재 프로젝트 내부는 알려진 공개 문서·설정과 명시적으로 분류된 생성물 경로를 대상으로 확인했다. 미분류 항목을 모두 공개 자료로 간주해 재귀 검색하지 않았다.
- `C:/Users/SSAFY/Documents/`와 `C:/`의 직속 항목을 메타데이터 수준에서 확인하고, 이름·실행 기록·Git 연결이 있는 후보만 좁혀 조사했다. 다른 프로젝트 폴더와 C 드라이브 전체를 재귀 탐색하지 않았다.
- 이 작업의 기존 공개 CommandExecution 1,286개에서 C 드라이브 루트 직접 경로와 현재 항목을 대조했지만 추가 삭제 대상으로 귀속을 확정하지 못했다. C 루트의 미확정 항목은 보존했다. 이는 다른 곳에 관련 파일이 전혀 없다는 증명이 아니다.
- 공개 I0–I3의 지정된 구현·테스트 경로에는 별도로 정리할 ignored Python bytecode cache가 확인되지 않았다.
- 이전 감사·구현 기록의 임시 경로 다섯 곳은 현재 접근되지 않았다. 이번에 삭제한 항목으로 세지 않았다: `rpnp05-impl-20260908`, `rpnp05-impl-test-20260908`, `rpnp05-original-static-material-v01-20260908`, `human-ai-development-tradition-independent-audit-20260908`, `rpnp04-final-clean-20260904`(모두 당시 `C:/Users/SSAFY/AppData/Local/Temp/` 아래).
- 존재하지 않는 과거 worktree의 Git 등록 메타데이터를 `prune`하지 않았다. Git 변경·기록 제거는 이번에 수행하지 않았다.
- 새로운 검사 체계·실험·설치·다운로드를 만들거나 실행하지 않았다.

## 6. 1차 정리 기준 상태와 확인 결과

- branch: `codex/windows-build-toolchain-environment-v0.1`.
- HEAD: `f4be29ff470946741ed4b39bbb90c1eef14537ed`.
- tree: `40f0ec165af60037fd38363067e0479ef8b395b4`.
- 정리 시작 시 Git 상태 항목 2개 중 1개는 지원서용 요약 파일, 나머지 1개는 미분류 항목이었다. 미분류 항목은 그대로 보존했다.
- F0 세 경로 집계는 32/11/10이고, staged·unstaged quiet diff와 untracked·ignored 집계 이상은 없었다. 내용은 읽지 않았다.
- 기존 추적 파일을 수정하지 않았으며, commit·push·branch 변경·worktree 제거를 하지 않았다.
- 정리 후 문서 변경은 지원서 요약의 위치 변경과 이 안내 파일 추가뿐이다. 사이트 출력과 빈 컨테이너는 휴지통에서 복원 가능하다.

## 7. 보류 항목의 추가 확인과 최종 정리

2026-09-16 사용자 요청에 따라 사진에 나온 작업 폴더 14개와 백업 1개의 삭제 가능 여부를 추가 확인했다. §4의 해당 보류 판정은 이 결과로 대체한다.

### 확인한 사항

- 작업 폴더 14개 모두 메인 프로젝트의 동일한 Git 공통 저장소에 연결돼 있었다.
- 각 작업 폴더의 미커밋·미추적 파일, ignored 파일, skip-worktree, assume-unchanged 집계는 모두 0이었다.
- 12개의 HEAD는 현재 메인 작업 폴더의 HEAD 이력에 포함돼 있었다. 나머지 2개도 기존 로컬 브랜치 또는 원격추적 참조가 커밋을 보존하고 있었다.
- 해당 폴더를 참조하는 실행 중 프로세스를 찾지 못했고, 현재 실행 중인 하위 에이전트도 없었다. 저장된 프로젝트 목록에서도 이 14개 폴더를 직접 등록한 경로는 확인되지 않았다.
- 백업에는 보호 자료 53개만 있었으며, 파일 집합·개수 32/11/10과 각 파일의 SHA-256이 메인 보존본과 모두 일치했다. 추가·누락·다른 파일은 0개였다. 파일 내용이나 내부 파일명은 출력·검토하지 않았다.

### 실제 처리

- 작업 폴더 14개는 정확한 경로별로 `git worktree remove`를 사용해 제거했다. `--force`와 광범위 `prune`는 사용하지 않았다.
- 중복 백업 `C:/Users/SSAFY/Documents/ai-development-tradition-pre-main-sync-backup-20260811`은 Windows 휴지통으로 보냈다. 이 백업은 휴지통에서 복원할 수 있다.
- 제거한 작업 폴더는 휴지통에 보낸 것이 아니다. 기존 Git 커밋과 참조가 남아 있으므로 필요한 경우 해당 커밋의 작업 복사본을 다시 만들 수 있다. 재생성 시 현재 운영 정책과 접근 경계를 확인한다.
- 메인 프로젝트의 HEAD와 작업 상태는 제거 전후 동일했다. 로컬 브랜치·태그·원격추적 참조 전체도 제거 전후 동일했다. commit·push·fetch·브랜치 삭제는 하지 않았다.
- 다른 프로젝트 폴더와 시스템·개인 파일은 변경하지 않았다.

### 제거한 작업 폴더의 커밋 기록

아래 이름의 원래 부모 경로는 모두 `C:/Users/SSAFY/Documents/`였다. 메인 프로젝트의 `.git`은 그대로 남아 있다.

| 제거한 폴더 | 보존된 HEAD |
|---|---|
| `ai-development-tradition-authenticode-v01-independent-review` | `ade0e1636ba483b9f8e3f465421a2c47cf1f1e33` |
| `ai-development-tradition-authenticode-v02-independent-rereview` | `ad36069581816416dec5cc970962289701f51de7` |
| `ai-development-tradition-authenticode-v02-revision` | `67ed5f55b3883c1b3d897fe26bb3cc27c98ef14d` |
| `ai-development-tradition-authenticode-v03-revision` | `b441db0379f7bef4f24384a7001e2c82df2813d5` |
| `ai-development-tradition-company-handoff-20260810` | `6d21e61dada605763d808f623a754d8c598bd6fb` |
| `ai-development-tradition-e0-effect-test` | `84014378b48466c185e13cadd6b9a07549ffbaee` |
| `ai-development-tradition-h2c-authenticode-20260825` | `0f9b1b2c06bb2257db63c218f20e29237be1f81e` |
| `ai-development-tradition-handoff-20260809` | `5a7181b2c4b62c912bb0c48daf2cd6e0783fb1af` |
| `ai-development-tradition-s0-isolation-review-v03` | `b98376d7935bc2ac1408dde296463d0cfadfae02` |
| `ai-development-tradition-s0-isolation-v03` | `21a63127b01559670cff8f3b494f642091fd9f79` |
| `ai-development-tradition-s0-isolation-v03-rereview-brief` | `bd8c0ce38620df69bff39a1617b651f28613346b` |
| `ai-development-tradition-s0-protocol-final-refreeze-v03-canonical-r1` | `f49d8bd04299a38a7417c2cafe96907acca5e4e5` |
| `ai-development-tradition-s0-protocol-refreeze-v03-canonical-r1` | `114e8a9260a724288f72d270b4e04453780f6e8a` |
| `ai-development-tradition-s0-protocol-rereview-v03-canonical-r1` | `e32df2b64b8cb4427e0084b05c6be88d74896c3c` |

현재 HEAD의 조상은 아니지만 보존된 두 참조는 다음과 같다. 원격추적 참조는 현재 로컬 Git에 보존된 값이며 이번에 원격 서버를 다시 확인한 결과는 아니다.

- `refs/remotes/origin/codex/home-to-company-handoff-20260824-authenticode-v01` → `0f9b1b2c06bb2257db63c218f20e29237be1f81e`.
- `refs/heads/codex/s0-trust-root-role-isolation-review-v03` → `b98376d7935bc2ac1408dde296463d0cfadfae02`.
