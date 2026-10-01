# 공개 감사 보정·유지보수 종료 정리

기준일: 2026-09-29 · 용도: CONTROL/관리자용 파생 기록 · 활성 기준선: `central-system-v2.1-s0-preparation`.

종료 대상으로 정리하는 범위는 **승인된 F-01–F-08 공개 소스·정의 보정, 개발용 소스 통합, 현재 PC의 공개 CLI 준비, 재개 위치와 한계의 인계**다.
A01–A08의 개별 제한 수용 판정은 모두 완료됐다. 이 보고서는 그 결과를 모은 고정 검토 대상이며, 전체 종료 검토의 PASS를 미리 선언하지 않는다.
보고서 검토와 최종 안내 반영 뒤의 **전체 CONTROL 종료 결정은 [현재 작업 원장][ledger]에 별도로 기록**한다. 원장과 [작업 흐름][workstream]이 현재 결정의 진입점이다.

**F-01의 실제 native lifecycle과 F-03의 완전한 historical/native 통합은 여전히 미완료다.** 이번 종료 범위는 이를 성공 처리하거나 원래 보안·독립성 계약을 줄이지 않는다.
S0/E0 실행·점수, 중앙 시스템 구현, Project Brain 연결, 운영 안전성, 경제성, 모델 간 전이는 이번 작업으로 입증되지 않았다.

## 완료된 작업과 증거의 시점

[2026-09-09 감사][audit]의 발견 사항을 기준으로, 9월 16–17일의 보정과 9월 29일의 실제 추가 확인을 구분한다.

| 시점·묶음 | 완료된 제한 범위 | 결과를 읽는 방법 |
| --- | --- | --- |
| 9월 16–17일 A01–A05 | open/stream 처리, native 목록·helper, 비용 중복 정의, I0 manifest 인증, profile composition 소스 보정 | 아래 개별 disposition의 당시 시험·검토 범위로 유지한다. 모두를 현재 native 실행 성공으로 합치지 않는다. |
| 9월 29일 A06 | 겹치는 F-01/F-03/F-08 변경을 보존한 전체 20파일 runtime 소스 통합 | 소스 보정 24개와 composition 59개 시험 PASS, 제한 수용. native 빌드·실행은 포함하지 않는다. |
| 9월 29일 A08 | F-02/F-04 보정을 포함한 전체 27파일 공개 assembly 소스 통합 | 77개 공개 단위·통합 회귀 PASS, 제한 수용. 기존 47개 시험 목적을 포함하며 live 진입 거부를 유지한다. |
| 9월 29일 A07 | 프로젝트 내부 `.venv-public`에서 기존 A04 CLI의 실제 의존성 실행 | `pip check`와 `integrity`, `schema-check`, `verify`를 각각 한 번 실행해 모두 exit 0. 모든 CLI 명령의 검증은 아니다. |

A06/A08의 시험 수에 하위 사례나 child 관찰을 더하지 않는다. A07의 631개 assertion은 반복 인증을 포함하므로 독립 시험 631개로 세지 않는다.
A07은 실제 jsonschema 4.26.0을 사용했다. 공개 manifest 90개 항목, 지정 schema 11개, 기존 package 8개의 메모리 생성 바이트 일치를 확인했고 `not_an_s0_run=true`였다.
A06/A07/A08의 fresh 검토는 소스 또는 설정을 먼저 평가한 뒤 증거를 읽는 순서였고, 각 disposition은 제한 범위 PASS와 발견 사항 0개를 기록한다.

## F-01–F-08 처분표

| 발견 사항 | 보정·처분 | 증거와 결정 | 남은 한계 |
| --- | --- | --- | --- |
| F-01 정상 native package 재검사 거부 | 최초·종료 목록 모두 P5를 포함한 동일 7개 항목으로 보정하고 A06에 통합 | [A02 수용][a02], [A06 수용][a06] | 변경 없는 package의 실제 bind/commit/OK/exit 및 실패 정리는 새 native 실행으로 입증되지 않았다. |
| F-02 정상 `os.open` 읽기 거부 | `None` mode와 세 번째 flags를 판독하고 delete-on-close를 먼저 차단; A08에 통합 | [A01 수용][a01], [A08 수용][a08] | 허용 읽기·pending 쓰기·latch와 실제 own-file 거부 사례의 범위다. OS sandbox나 전체 live controller 성공은 아니다. |
| F-03 과거 P4와 새 runtime의 manifest 강제 동일화 | historical 검증과 current composition의 바이트 의미·snapshot·consumer 연결을 분리하고 A06에 통합 | [A05 v0.3 수용][a05], [A06 수용][a06] | 완전한 historical positive 검증, native 경로 매핑·실행 권위는 미확인이다. F-03 전체 종료가 아니다. |
| F-04 stream 오류를 EOF로 처리 | EOF 38만 허용하고 오류를 close 전에 보존하며 `FindClose` 실패를 거부; A08에 통합 | [A01 수용][a01], [A08 수용][a08] | 36개 API 대역 관찰이다. 실제 OS ADS 오류·공격이나 native publication 성공을 입증하지 않는다. |
| F-05 종료 결정·재개 위치의 안내 단절 | 이 보고서에 현재 소스·환경·제한을 연결하고 최종 결정 경로를 원장/작업 흐름으로 지정 | [현재 원장][ledger], [작업 흐름][workstream], [README][root-readme], [문서 안내][guide] | 안내 최종 반영과 전체 종료 결정은 보고서 검토 후 CONTROL의 별도 완료 항목이다. 이 문서는 아직 일어나지 않은 반영을 완료로 세지 않는다. |
| F-06 Q 재시작 인건비 중복 가능성 | primary Q-human 중복 가산항만 제거하고 귀속·총액 보존 정의 수용 | [A03 수용][a03], [원문 v0.4][e0-cost] + [수용된 정오표][erratum] | 원문은 보존한다. 향후 비용 계산은 두 문서를 함께 적용해야 하며 실제 비용·인력 실현성·경제성을 검증한 것은 아니다. |
| F-07 I0 단독 CLI의 frozen manifest pin 공백 | 세 명령의 handler 이전에 고정 digest 검사 추가; A07에서 실제 의존성으로 실행 | [A04 수용][a04], [A07 수용][a07] | 해당 공개 입력·현재 호스트·기록된 버전의 세 명령에 한정한다. 모든 답안 기능·이식성·미래 상태를 보장하지 않는다. |
| F-08 path/API helper의 좁은 거부 범위 | 정규화 전 raw path 성분 검사와 MoveFile 계열 진단 보정; A06의 겹치는 source checker 변경과 결합 | [A02 수용][a02], [A06 수용][a06] | 제한된 이름·구문 검사다. 전체 Windows API나 interpreter/import closure의 완전성 검증은 아니다. |

동결된 README/checklist의 `REVIEW PENDING`은 당시 문서 작성 시점의 사실이다. **현재 개별 상태는 나중에 작성한 `CONTROL-DISPOSITION.md`를 읽는다.** 오래된 문구를 고치기 위해 원래 해시를 바꾸지 않았다.

## 한 작업 폴더에서 다시 시작하는 위치

작업 루트 `P`는 `C:/Users/SSAFY/Documents/ai-development-tradition`이다. 다음 경로는 모두 P 내부이며, 소스 존재와 live 실행 권위는 구분한다.

| 대상 | P 기준 정확한 위치 | 실용적 용도 |
| --- | --- | --- |
| 기존 단독 I0 CLI | `s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1/implementation/s0_i0/` | A07에서 실제 실행한 CLI 구현이다. |
| 공개 CLI 환경·명령 안내 | `.venv-public/`, `s0-lab/audit-remediation/a07-public-cli-readiness-v0.1/README.md` | real jsonschema 의존성 환경과 [세 읽기 전용 명령][a07-readme]을 제공한다. |
| 공개 assembly 개발 소스 | `s0-lab/audit-remediation/a08-public-assembly-source-integration-v0.1/implementation/` | 전체 27파일 소스 입력이다. A07 명령이 실행하는 CLI도, live 승인된 runtime도 아니다. |
| runtime 개발 소스 | `s0-lab/audit-remediation/a06-runtime-source-integration-v0.1/implementation/` | 전체 20파일 보정 합본이다. 새 native executable package의 수용 결과가 아니다. |
| 문서 환경·출력 | `.venv-docs/`, `.mkdocs-site/` | 문서용 환경·생성 사이트다. 공개 CLI 환경과 별도로 취급한다. |

A07 명령은 PowerShell의 작업 디렉터리를 P로 두고 `.venv-public/Scripts/python.exe`와 정확한 A04 경로를 사용한다. 이 세 명령으로 A06/A08을 실행하거나 승인된 native 묶음을 만들지 않는다.
A06은 A02+A05의 runtime 보정을 통합한다. A08은 원래 공개 assembly에 A01의 두 보정을 통합하며, A06의 20파일을 포함하거나 A06을 대체하지 않는다. 세 구성요소는 하나의 native/live 실행 묶음으로 수용된 적이 없다.
A06의 기존 build/runtime-authority 핀과 A08의 기존 authority root·manifest 경로는 유지됐다. 파일 복사·import·진단용 pin이 새 실행 권위를 부여하지 않는다.
base Python, Visual Studio Build Tools와 Windows SDK는 P 밖의 공용 설치 자산이다. P 안에 모든 시스템 의존성이 들어 있다는 뜻은 아니다.
CONTROL은 Python 3.12.10과 Build Tools 설치 metadata를 관찰했지만, 이를 전체 호스트·설치 트리 검증이나 새 native 실행 결과로 주장하지 않는다.
이번 작업의 새 지속 산출물과 프로젝트 환경은 P 아래에 둔다. 로컬 환경은 Git으로 다른 PC에 자동 재현되는 산출물이 아니다.

## 보존한 이력과 신뢰 범위

기준 branch는 `codex/windows-build-toolchain-environment-v0.1`, HEAD는 `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`, tree는 `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`다.
이는 저장소 기준점이다. 현재 후보 파일과 로컬 환경의 존재·동일성을 HEAD만으로 대신 확인할 수 없으며 새 clone이 이 작업 상태를 자동 포함한다고 하지 않는다.
CONTROL은 2026-09-29 06:14 UTC에 A01–A08 manifest 8개와 수록 파일 144개의 해시 일치를 재인증했다. 이는 보존 확인이며 시험 144개가 아니다.
DOCUMENTATION은 허용된 원문·판정의 고정 해시와 A06/A07/A08의 30/8/39개 manifest 항목을 인증했다. 소스·TEST·자료의 원래 핀과 원래 실패 기록을 유지한다.

| 남겨 둔 사건 | 현재 해석 |
| --- | --- |
| 9월 16일 worktree 정리의 미분류 차단 규칙 적용 누락 | [전환 영향 기록][impact]의 절차상 미준수를 유지한다. 현재 허용으로 소급 정당화하지 않는다. |
| A04 DOCUMENTATION의 허용 TEST 파일 3개 pre-hash 읽기 | 중단·교체와 나중의 해시 일치가 앞선 절차를 소급 준수로 바꾸지 않는다. |
| A05 v0.1 거부와 v0.2 TEST 실패 | 각 버전의 해시·결과를 보존한다. v0.3의 제한 수용을 이전 버전의 PASS로 적용하지 않는다. |
| A06 최초 TEST의 post-run Git 인증 오류 | Windows command-line 문자열과 audit hook의 인자 가정 차이를 진단해 TEST만 보정했다. CODE/native 실패나 없었던 실행으로 바꾸지 않는다. |
| A08 이전 DOCUMENTATION의 validator 읽기 권한 해석 문제 | 해당 역할이 보고 후 중단했고 명시적 권한을 받은 새 역할이 작성했다. 교체가 앞선 handoff를 소급 승인하지 않는다. |

A08의 copy-preflight filename filter 보정과 검토자의 무효한 최초 합동 validator 호출도 [해당 기록][a08]과 README에 남아 있다. 이후 개별 문서 검사는 통과했고 후보 TEST 실패·추가 수정 cycle로 세지 않는다.
CONTROL이 확인한 것은 지명된 W/T/O/R/B Temp root 5개의 현재 부재다. 전역 사본 부재나 삭제 원인·주체를 입증한 것은 아니다.
원문 회수·파일 해시 일치는 과거 filesystem identity, 전체 raw evidence 또는 현재 native 실행의 대체물이 아니다.

## 연구 경계·게시 상태·다음 작업

이 보고서와 root 안내·원장·사이트·로그는 CONTROL/유지보수 자료다. 링크·공개 Git·공유 폴더가 실행자나 독립 심사자의 입력 허용 범위를 늘리지 않는다.
새 세션·worktree만으로 강제 정보 격리나 오염 제거가 입증되지 않는다. 대화 fork, 요약, 검색 색인, 초기 프롬프트 등 간접 노출도 기록해야 한다.
이번 최종 검토는 원래 감사와 개별 판정을 읽는 **fresh 읽기 전용 파생 종료·주장 검토**다. 새 outcome-blind 코드·보안·연구 재감사나 모든 과거 역할의 독립성 인증이 아니다.
향후 연구 역할은 정확한 입력·해시·노출 이력·출력 범위를 따로 동결한다. 경계 위반 시 해당 역할을 멈추고 증거와 적용되는 무효·재시험 규칙을 보존한다.

CONTROL의 최근 보호 집계는 32/11/10, HEAD 대비 quiet diff 0, 보호 범위의 untracked/ignored/skip-worktree/assume-unchanged 각 0이다. 보호 파일명·내용은 출력하지 않았다.
이 보호 집계와 저장소의 미분류 상태 차단은 별개다. **opaque 미분류 Git-status 차단은 해제되지 않았다.** 이 정리는 commit/push·remote tip 확인을 수행하거나 게시 승인으로 간주하지 않는다.
로컬 작업 상태의 제한된 유지보수 종료는 게시와 구분된다. 다른 PC 인계나 Git 변경은 현행 분류·승인·보존 절차를 따른다.

최종 보고서 검토 뒤 CONTROL은 [원장][ledger]에 전체 결정과 남은 제한을 남기고 [작업 흐름][workstream]·[README][root-readme]·[문서 안내][guide]의 재개 경로를 마무리한다.
본 보고서의 바이트를 그 후 결정에 맞추어 다시 쓰지 않는다. 최종 안내에는 E0 [원문 v0.4][e0-cost]와 [A03 정오표][erratum]를 함께 연결한다.
이 제한된 유지보수가 끝나면 현재 세션의 기술 작업도 끝난다. 다음 CONTROL은 새 세션에서 최신 AGENTS·Git/worktree 상태·정확한 허용 산출물을 재인증해야 한다.
그 다음 사용자가 원하는 실제 기능 하나를 선택하고, 막힌 핵심 작업·가장 싼 표준 대안·유용한 결과·비용·중단 조건을 밝힌 뒤 해당 candidate/gate를 명시적으로 연다.
F-01/F-03의 누락된 historical/runtime 자료는 그 자료를 권위로 요구하는 작업을 막는다. 관계없는 기능까지 자동으로 막거나 모든 nonclaim을 닫는 새 보조 프로젝트를 권하지 않는다.
새 기능 구현, native/live 리허설, F0 내용, fixture/oracle, S0/E0 실행·scoring, 실제 provider/model 호출, Git 게시 권한은 이 보고서로 열리지 않는다.

[audit]: audit-2026-09-09/AUDIT-REPORT.md
[impact]: SESSION-TRANSITION-IMPACT-2026-09-16.md
[ledger]: ../../s0-lab/control/CURRENT-WORK-LEDGER.md
[workstream]: ../../s0-lab/control/workstreams/public-end-to-end-assembly-rehearsal.md
[root-readme]: ../../README.md
[guide]: ../../DOCUMENT-GUIDE.md
[a01]: ../../s0-lab/audit-remediation/a01-public-boundaries-v0.2/CONTROL-DISPOSITION.md
[a02]: ../../s0-lab/audit-remediation/a02-native-source-corrections-v0.1/CONTROL-DISPOSITION.md
[a03]: ../../s0-lab/audit-remediation/a03-cost-definition-v0.1/CONTROL-DISPOSITION.md
[a04]: ../../s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1/CONTROL-DISPOSITION.md
[a05]: ../../s0-lab/audit-remediation/a05-profile-composition-v0.3/CONTROL-DISPOSITION.md
[a06]: ../../s0-lab/audit-remediation/a06-runtime-source-integration-v0.1/CONTROL-DISPOSITION.md
[a07]: ../../s0-lab/audit-remediation/a07-public-cli-readiness-v0.1/CONTROL-DISPOSITION.md
[a08]: ../../s0-lab/audit-remediation/a08-public-assembly-source-integration-v0.1/CONTROL-DISPOSITION.md
[a07-readme]: ../../s0-lab/audit-remediation/a07-public-cli-readiness-v0.1/README.md#use-the-existing-read-only-cli
[e0-cost]: ../tradition/e0-effect-test/e0-operating-cost-and-gates-v0.4.md
[erratum]: ../../s0-lab/audit-remediation/a03-cost-definition-v0.1/COST-DEFINITION-ERRATUM.md
