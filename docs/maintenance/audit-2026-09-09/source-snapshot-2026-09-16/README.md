# 2026-09-09 감사 대상 공개 파일 9개 — 보존 복구 사본

> **CONTROL/보존 복구용 자료. 현재 실행 환경이나 새 독립 검토·실험 역할의 기본 입력이 아니다.**
> 복구일: 2026-09-16. 사용자가 누락된 9개 파일의 보존 복구 진행을 승인했다.
> 원문을 고치거나 현재 작업 경로에 통합하지 않고 별도 사본으로 보존한다.

## 범위와 동일성 기준

감사가 직접 참조했고 현재 등록 프로젝트와 로컬 Git 참조 이력에서 찾지 못한 9개 파일만 대상으로 했다. 총 221,462바이트다. 각 파일의 전체 본문을 당시 공개 도구 출력에서 추출하고, **당시 SHA-256 및 바이트 수가 모두 일치한 경우에만 복구 성공으로 판정**한다.

| 복구 파일 | 원래 bytes | 당시 SHA-256 |
|---|---:|---|
| [build.ps1](./build.ps1) | 10,361 | `415dfc99d1a6dfec2bfb618dd2b8648cdc4d85d6051bdaa997e0209cde877a5e` |
| [s0_neutral_preloader_v0_5.cpp](./s0_neutral_preloader_v0_5.cpp) | 81,162 | `6230ef69d5b4b175968f7576b43aeb5ae15fa3646c59778f84b5c3877c0ef9ec` |
| [semantic.py](./semantic.py) | 21,529 | `1bea3a04282c7d5b6f930ed51b95dbcea87f14f417b04bdee4fb4fbe93c0037d` |
| [profile.py](./profile.py) | 14,641 | `c5c1f6c6c937e45b9da246b24783134570a48923501757ab4683173a5367fe89` |
| [v0.5-implementation-profile-composition-control-decision-v0.1.md](./v0.5-implementation-profile-composition-control-decision-v0.1.md) | 4,260 | `1981ec369027d08308a22c936f76b8a5906bee0a7d7ee8c596ecab85438e5d20` |
| [CURRENT-WORK-LEDGER.md](./CURRENT-WORK-LEDGER.md) | 21,845 | `952d3cf2ace2662f43c7c1dba4c302e3475e28ba1eaed42dc4c4795ea91c213a` |
| [canonical.py](./canonical.py) | 5,835 | `f73112b1bf55708d68d1e3823d768f1e9083f44760945ca7d2eb3d4fdf75aad4` |
| [source_audit.py](./source_audit.py) | 24,041 | `c5cc9edb2e290f9ec0be74e944bf515b0c398f9bd08e379a701a8582951aac99` |
| [materialize.py](./materialize.py) | 37,788 | `17c2cf9032998fe9653a5f6b8535eb76e4f15693e8b834ca60d10755bfa430f7` |

[source-files.sha256](./source-files.sha256)은 위 9개 원문만을 대상으로 한다. 두 역사 Markdown의 sidecar는 당시 본문 해시와 원래 파일명으로 다시 작성했다. 삭제된 sidecar 자체를 회수했다는 뜻은 아니다. 이 README는 현재 작성한 보존 설명이며 역사 원문의 일부가 아니다.

## 복구 출처와 방법

- 감사 보고서: [AUDIT-REPORT.md](../AUDIT-REPORT.md), SHA-256 `c77704a38f6ed8a81ccee36a12d2066fee8ccfd054d293cfb932ca8eec260eba`.
- 감사 작업: **프로젝트 전체 감사 — Astra Max 재검토**, ID `01a083e9-bc25-7d40-a70f-a794100e24c7`.
- 당시 작업 루트: `C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908`.
- 당시 HEAD: `5ad4632e9ceec64fff53ee26bb3557e95f817d4c`. 이 커밋만으로 당시 미커밋 후보 전체가 보존되는 것은 아니며 현재 등록 프로젝트의 object database에서는 찾지 못했다.
- 정확히 지정한 원본 로그: `C:/Users/SSAFY/.codex/sessions/2026/09/09/rollout-2026-09-09T11-05-28-01a083e9-bc25-7d40-a70f-a794100e24c7.jsonl`.
- 앱의 출력 길이 제한으로 잘린 부분은 위 한 로그의 공개 도구 출력에서, 정확한 원래 파일 경로와 당시 해시가 일치하는 출력만 선택해 회수했다. 로그 전체·비공개 추론·무관한 작업 출력은 이 폴더에 복사하지 않았다.
- 공개 출력의 줄 번호를 제거하고 같은 파일의 번호별 줄을 합쳤다. 중복 구간은 일치 여부를 확인하고, 잘린 마지막 줄은 해당 원본 출력의 온전한 줄로 대체했다. 추측 코드·유사 버전·새 구현으로 빈 부분을 채우지 않았다.
- 추출한 코드를 import·실행·컴파일하거나 과거 실행 명령을 재실행하지 않았다. 저장 후 표준 SHA-256 및 파일 크기로 동일성을 확인하고, 두 Markdown과 sidecar는 기존 canonical text-artifact 도구로 검사한다.

## 원래 경로와 선별 근거

파일명은 그대로 두되 이 보존 폴더에 평탄화했다. 기존 실행 경로와 혼동하지 않고 Windows 경로 길이를 제한하기 위한 것이다. 원래 상대 경로는 아래에 보존한다.

### build.ps1

- 원래 상대 경로: `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/native/build.ps1`
- 감사의 공개 command ID: `exec-8b4e373b-edc5-4e7b-91ac-6047095c219a`.
- 원본 로그에서 추가 회수한 공개 도구 출력 call ID: 없음(앱에서 반환된 공개 출력으로 전체 본문 확보).

### s0_neutral_preloader_v0_5.cpp

- 원래 상대 경로: `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/native/s0_neutral_preloader_v0_5.cpp`
- 감사의 공개 command ID: `exec-289d6921-418e-4d3d-96de-66f950ae2d78`, `exec-833b5a12-c57f-4018-b535-3a592ac88702`, `exec-741a6578-5abb-477d-b37a-2e66652674e1`, `exec-e862a606-7864-40fc-97f0-efc14e0e025e`, `exec-b872e8dd-7162-4b96-84f4-8558cfd15c67`.
- 원본 로그에서 추가 회수한 공개 도구 출력 call ID: `call_41wycaufNxFuXVmLmHAv4JWZ`, `call_Om8SrqMJrRspuhMmaToKtQYt`, `call_aPk9EMAo11IKKEFNI9teTyPx`.

### semantic.py

- 원래 상대 경로: `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/s0_public_runtime_preloader/semantic.py`
- 감사의 공개 command ID: `exec-24a4233c-cd5b-45b6-aad6-d492676c6047`, `exec-846868a7-47cf-4730-a383-057eb567bc93`.
- 원본 로그에서 추가 회수한 공개 도구 출력 call ID: 없음(앱에서 반환된 공개 출력으로 전체 본문 확보).

### profile.py

- 원래 상대 경로: `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/s0_public_runtime_preloader/profile.py`
- 감사의 공개 command ID: `exec-a8b94f85-fcd5-484d-99de-2f1bfe52a3a2`.
- 원본 로그에서 추가 회수한 공개 도구 출력 call ID: 없음(앱에서 반환된 공개 출력으로 전체 본문 확보).

### v0.5-implementation-profile-composition-control-decision-v0.1.md

- 원래 상대 경로: `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/v0.5-implementation-profile-composition-control-decision-v0.1.md`
- 감사의 공개 command ID: `exec-93ba5ce9-2df9-4aa0-89ec-ca3a2ec49437`.
- 원본 로그에서 추가 회수한 공개 도구 출력 call ID: 없음(앱에서 반환된 공개 출력으로 전체 본문 확보).

### CURRENT-WORK-LEDGER.md

- 원래 상대 경로: `s0-lab/control/CURRENT-WORK-LEDGER.md`
- 감사의 공개 command ID: `exec-4f2d3c11-a193-4ce3-ad15-df8cff5f45d4`, `exec-688a57ac-52b6-41b7-9b9a-b76df59c7c03`, `exec-148e9457-6603-45ae-b04c-3a7a93767b2c`.
- 원본 로그에서 추가 회수한 공개 도구 출력 call ID: `call_GRWnHCO9i5A3cVekpoif82XG`, `call_uXlGqf21iKiyjIlUsQJFcw1t`.

### canonical.py

- 원래 상대 경로: `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/s0_public_runtime_preloader/canonical.py`
- 감사의 공개 command ID: `exec-ce61e785-8cce-4389-9610-1978cef77ed0`.
- 원본 로그에서 추가 회수한 공개 도구 출력 call ID: 없음(앱에서 반환된 공개 출력으로 전체 본문 확보).

### source_audit.py

- 원래 상대 경로: `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/s0_public_runtime_preloader/source_audit.py`
- 감사의 공개 command ID: `exec-0e6448da-ca25-41b9-955f-3a139144f5d2`, `exec-7f756de0-82e9-4b55-88c8-c680ed0a4f38`.
- 원본 로그에서 추가 회수한 공개 도구 출력 call ID: 없음(앱에서 반환된 공개 출력으로 전체 본문 확보).

### materialize.py

- 원래 상대 경로: `s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/implementation/s0_public_build_runtime/materialize.py`
- 감사의 공개 command ID: `exec-12fad1c5-78a5-43de-9409-1dc8a61e2ff9`, `exec-c4cca638-74dc-4405-a074-0c3bb56c71dd`, `exec-c719596d-e3f2-41a6-91fc-55a728106ccb`.
- 원본 로그에서 추가 회수한 공개 도구 출력 call ID: `call_wiOrzOlMOlxCOgF4H0f7bSvJ`.

## 사용 제한과 남은 공백

1. **9개 원문의 보존 복구이지 최신 작업본 전체 복구가 아니다.** 전체 구현 20개 파일, 의존성, 빌드 결과, 219개 runtime 파일, 당시 증거·키·외부 입력을 모두 확보한 것이 아니다.
2. `CURRENT-WORK-LEDGER.md`는 감사 당시의 오래된 상태까지 포함한 역사 원문이다. 이름이 CURRENT여도 현재 작업 지시로 적용하지 않는다. 감사의 F-05 지적이 이번 원문 복구로 수정된 것은 아니다.
3. 코드의 감사 지적(F-01/F-03/F-08 등)은 수정하지 않았다. 바이트 일치는 올바른 동작·검증 통과·실제 실행 준비 완료를 뜻하지 않는다.
4. 원문의 경로·링크·선행조건은 그대로 남겼다. 이 폴더에서 build.ps1이나 Python 파일을 바로 실행하지 않는다. 현재 코드·설정·작업 원장에 자동 통합하지 않는다.
5. R/B의 과거 identity·외부 증거 공백, native lifecycle 미실행, S0/E0·중앙 시스템 효과 미검증은 그대로다.
6. 원본 Temp 폴더가 없어진 원인·주체를 이번 복구로 확정하지 않는다. 다른 백업·다른 PC·원격 사본의 전역 부재도 주장하지 않는다.
7. 후속 구현·시험·독립 검토는 새 세션의 정확한 허용 입력과 게이트를 따른다. 이 사본이나 과거 판정을 새 독립 역할에 자동 전달하지 않는다.
8. 이번 작업은 일반 보존 복구다. 새 후보 구현·독립 심사·실험을 수행한 것이 아니며, 기존 보호 자료·미분류 항목은 변경하지 않는다. commit·push·기존 경로 덮어쓰기는 수행하지 않는다.
