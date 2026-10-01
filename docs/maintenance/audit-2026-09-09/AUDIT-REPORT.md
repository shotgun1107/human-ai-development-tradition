# human-ai-development-tradition 독립 감사 보고서

- 감사자: 새 독립 GPT-6 Astra · Max 세션. 기존 기술 후보 역할에 참여하지 않았고 추가 에이전트를 만들지 않았다.
- 기준일: 2026-09-09. 감사 상태: **허용된 C01–C15의 조사·판정 완료. 과거 실행 증명의 일부는 자료 접근 차단으로 남는다.**
- 산출물 상태: **감사 및 수정 제안 완료 / 원본 수정 없음 / 제안한 수정의 재검증 미실행.**
- 이 보고서는 원자료를 먼저 검토한 새 판단이다. 이전 중단 감사의 보고·진단은 이후 대조했으며, 당시 테스트를 새로 실행한 것으로 세지 않았다.

## 1) 현재 프로젝트를 신뢰할 수 있는 범위와 중요한 제한

**중앙 시스템의 목적·준비 설계와 공개 오프라인 구성요소는 한정된 범위에서 재사용할 수 있다. 현재 Windows 공개 리허설은 실행 준비가 끝나지 않았다.** 프로필 결합 규약의 기존 차단에 더해, native package 재검사와 Python 파일 감시 처리에서 각각 정상 경로를 막는 결함을 확인했다. 공개 조립의 스트림 검사에는 오류를 정상 종료로 취급하는 결함도 있다.

중앙 시스템 제품, Project Brain 연결, 공식 리허설, S0, 운영 안전성, 경제적 효과, 모델 간 전이는 구현·검증 완료로 인정할 수 없다. 이 제한은 단순히 자료를 덜 읽어서 붙인 문구가 아니라 현재 명세, 실행 진입점, 기계 결과와 종료 결정을 연결한 판정이다.

| 기준 상태 | 등록 프로젝트 P | 최근 실제 작업 W |
|---|---|---|
| 절대 경로 | `C:/Users/SSAFY/Documents/ai-development-tradition` | `C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908` |
| branch | `codex/windows-build-toolchain-environment-v0.1` | `codex/runtime-profile-neutral-preloader-v05-corrected-implementation` |
| HEAD | `f4be29ff470946741ed4b39bbb90c1eef14537ed` | `5ad4632e9ceec64fff53ee26bb3557e95f817d4c` |
| tree | `40f0ec165af60037fd38363067e0479ef8b395b4` | `f8221aaa04ef529ec11f3057b53efa31d02bd86e` |
| Git common directory | P의 `.git` | `C:/Users/SSAFY/AppData/Local/Temp/rpnp04-final-clean-20260904/.git` |
| 현재 remote | origin은 `shotgun1107/human-ai-development-tradition` | remote 목록 0개. origin 조회 exit 2 |
| 상태 | staged 0, tracked unstaged 0, 미분류 untracked 1 | staged 0, tracked unstaged 2, untracked 49. 승인된 공개 범위로 50개 분류, 미분류 1개 |
| root 정책 SHA-256 | `2bb310375111974c13e6935365bbd778285f583da14cdc019d5ebb8d82ab335e` | `6bff2cef0ddd3ecef6e3f997ec34e9460dc4097c4d46cae73bb32f5ddc10966c` |

P와 W는 같은 프로젝트의 서로 다른 작업 상태다. W의 실행 명령과 Git 연결을 확인했으므로 Temp라는 이유로 무관한 복사본으로 분류하지 않았다. HEAD만으로 W의 최신 후보를 대표할 수 없다. cached remote ref를 live remote 인증으로 취급하지 않았고 네트워크 조회도 하지 않았다. [시작 기준][baseline]과 [종료 인증][final-integrity]에서 branch/HEAD/tree 및 캡처한 전체 status 바이트가 일치한다. 마지막 인증 대상 공개 파일 271개의 해시도 모두 유지됐다. 미분류 파일의 내용을 읽거나 그 내용의 불변성을 주장하지 않는다.

두 루트의 F0 보존 집계는 각각 32/11/10이다. index·worktree·HEAD-parent quiet diff는 모두 0, untracked·ignored·skip-worktree·assume-unchanged도 모두 0이었다. 내부 파일명과 내용은 입력으로 사용하지 않았다.

실제 참조를 따라 확인한 외부 루트는 다음과 같다. 아래 약칭은 뒤에서 반복 사용한다.

| 약칭 | 절대 경로 | 역할과 현재 상태 |
|---|---|---|
| R | `C:/Users/SSAFY/AppData/Local/Temp/rpnp04-81a7e8cb/final-test-correction9-v1` | 과거 recipe와 P1–P4, 생산·시험 package의 원위치. 지명된 원본 파일은 현재 접근되지 않음 |
| B | `C:/Users/SSAFY/AppData/Local/Temp/brm07-6a21dc13/runtime-final-r4` | 과거 base runtime·identity/evidence의 원위치. 지명된 파일은 현재 접근되지 않음 |
| T | `C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-test-20260908` | 현재 인증 가능한 빌드 기록·materialization 결과·파생 runtime |
| O | `C:/Users/SSAFY/AppData/Local/Temp/rpnp05-original-static-material-v01-20260908` | 한정 재구성 검사의 결과·21개 생성물 |
| A | `C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908` | 감사 결과. 이번 새 증거는 `astra-max-clean`에만 작성 |

R/B의 directory 존재와 그 안의 exact file 접근 실패를 구분했다. 삭제 시점·삭제 주체·전역 부재는 확인하지 않았다. 같은 바이트의 대체 자료를 조사해 recipe, original P4, base payload manifest와 R의 ledger/summary를 복원했지만, 원래 B의 전체 identity/evidence와 P4가 요구하는 historical runtime material까지 복구한 것은 아니다. 이 차이가 C11/C12의 잔여 차단이다.

## 2) 주요 기능이 실제로 동작하는 방식의 간결한 설명

사용자 목표는 검증한 경험을 모델 밖의 작업 자산으로 남기고, 다음 AI가 조건에 맞는 자산을 선택·재시험·적용하며 수정·철회할 수 있게 하는 것이다. [목적 헌장][purpose]과 [v2.1 설계][central]는 이 목표를 설계 가설로 구체화한다. 현재 구현은 이를 평가하기 위한 공개 준비 구성요소다.

| 기능·흐름 | 요구와 적용 기준 | 구현·실제 진입점 | 검증·완료 주장·후속 활용의 판정 |
|---|---|---|---|
| 중앙 기억·계승·철회 | 목적 헌장, v2.1, 활성 S0 준비 기준 | 경험의 구조화→조건부 자산→선별 전달→피드백→수정/철회 | 요구 구조는 확인. 중앙 제품이나 실사용 효과 구현은 확인되지 않음 |
| S0 공개 준비와 I0 | [canonical protocol v0.3-r1][protocol], [질문 계약 v0.14 통합][question-decision], I0 brief/refreeze | [integrity/schema/transform/answer CLI][i0-cli]. 일반 답안 검사는 공개 질문 투영만 사용 | 전체 I0 소스·483행 테스트를 검토. 변환의 8개 frozen package 일치·답안 형식 검사가 목적. 기술 PASS를 S0 점수로 올리지 않음. 단독 CLI의 pin 공백은 F-07 |
| I1/I2/I3와 공개 조립 v0.1 | 한 번 호출, 재시도 0, 고정 request/answer, 완료와 consumer 판정 분리 | I1 인증·canonical topology·runner, I2 lifecycle/records, I3 분류·finalizer; [controller][controller]→stub→record/receipt→observer→consumer | component 59개 행과 assembly 32개 행 인증. 상태·실패·중복·재실행·닫기 경로와 관련 테스트 검토. 기존 47 PASS는 offline 검사이며 F-02를 포함하지 않음 |
| 공개 조립 v0.2 adapter | 정확한 predecessor closure를 재검증하는 오프라인 bridge | [candidate][adapter]가 v0.3 integration→NeutralPreloader.prepare→profile/semantic/evidence를 실제 호출 | 6개 snapshot 테스트의 기존 성공 기록과 실제 호출 코드를 대조. 반환은 `candidate_only=true`, `native_api_reachable=false`, `rehearsal_pass=false`. live launch 아님 |
| Windows 빌드 환경 | 사용자 승인 표준 Build Tools 환경 | 고정 cl/link/import library를 사용하는 [build.ps1][build] | 당시 cl 19.44.35228.0/link 14.44.35228.0 기록과 현재 빌드 입력·생성 binary 3개 연결을 인증. 이번 감사에서 설치·컴파일하지 않음 |
| runtime v0.7 | 고정 CPython ZIP/wheel과 표준 publication 선택 | [materialize.py][runtime-v07]: 핀·URL·redirect·크기 검사→안전 추출→`os.rename`→inventory/probe·결과 | 소스와 750행 테스트 및 적용 명령 검토. 사용자 09-03 표준 rename 선택이 현행 기준. T 안의 과거 base 174개/24,138,847 bytes를 재인증. 과거 r4 전체 원자료는 접근 차단 |
| runtime/profile/native v0.5 | corrected implementation과 승인된 FindClose 보정 | materializer→새 runtime→[P4/P5 결합][profile]→[native preloader][native-initial]의 suspended child와 5 handles→guard bind/commit→종료 검사 | 20개 source/324,283 bytes, 빌드·225개 생성물은 [인증됨][evidence-auth]. 실제 기록은 materializer 1회 exit 0이며 preloader/guard/bootstrap lifecycle 0회. 전체 구현 PASS 아님 |
| 공식 리허설·S0·E0 | 별도 선행조건과 실행 권한, E0 v0.4 설계 | 현재 연결 실행은 미완료. [assembly live 진입점][assembly-live]은 명시적으로 거부 | E0 설계·측정·비용·response/review를 대조. E0도 설계 통합 검토 범위이며 효과·경제성·전이의 실행 결과는 없음 |

v0.5 bootstrap이 `s0_runtime_handle_guard_v0_4`를 import하는 것은 명시된 호환 ABI와 build export가 일치한다. 버전 숫자 차이만으로 잘못된 실행 대상을 판정하지 않았다. v0.3 adapter가 사용하는 schema.py와 semantic.py는 검토한 v0.5 사본과 바이트가 동일하며, 달라진 profile/preloader/evidence 경로는 따로 읽었다.

문서의 지위는 다음과 같이 적용했다. 현재 사용자 지시·각 root의 최신 AGENTS가 권한 기준이고, 목적/채택 설계와 해당 후보의 승인 보정이 기능 기준이다. CURRENT-WORK-LEDGER와 workstream은 수정 가능한 파생 색인이므로 Git·실제 결과·종료 결정을 덮지 못한다. 버전이 붙은 과거 보고와 README/HOME의 당시 지시는 역사 자료다. 오래됐다는 이유로 폐기하지 않았고, 이미 폐기 승인된 Authenticode 확장을 현재 preloader 작업과 혼동하지 않았다.

## 3) 우선순위별 발견 사항과 증거

### F-01 — native package 재검사가 변경 없는 정상 package를 거부한다

**높음 / 정적 근거로 확인 / native lifecycle 재현은 미실행.**

[최초 검사][native-initial]는 6행 manifest와 물리 파일 7개(P1–P5, runtime manifest, package manifest)를 요구한다. [ReverifyPackage][native-terminal]의 물리 목록은 P5만 빠진 6개다. 같은 root와 retained material을 다시 검사하며, commit 응답 직전과 child 종료 뒤에 호출한다. [새 판별 결과][static-results]는 실제 소스 배열을 추출해 차이가 `runtime-profile-v0.5.json` 한 개임을 확인했다.

의도적으로 P5를 제거하는 단계일 수 있다는 설명을 검토했지만, 제거·package 전환 계약이나 호출 경로가 없고 원래 exact package 보존 요구와도 맞지 않는다. 앞선 선행조건을 충족해 이 지점에 도달하면 정상 package도 `OK` 전 실패한다. 이는 false PASS가 아니라 정상 실행 거부다. 현재 lifecycle이 그 앞에서 막혔다는 사실은 이 별도 결함을 없애지 않는다.

최소 수정은 최초·재검사에 같은 7파일 계약을 적용하는 것이다. 재검증은 변경 없는 package의 commit 전/후 통과, P5 누락·변조·추가 파일의 거부, benign bind/commit/OK/exit 0, 실패 시 잔여 handle·출력 없음이다. 단순히 테스트의 기대 목록을 6개로 바꾸면 안 된다.

### F-02 — Python 파일 감시기가 실제 os.open 읽기를 잘못 거부한다

**높음 / 격리 재현 확인 / 전체 controller·native 실행은 미실행.**

[runtime_guard.py 211행][python-open]은 open audit event의 두 번째 인자를 mode 또는 flags로 간주한다. 실제 CPython 3.12.10의 `os.open` 이벤트는 `(path, None, flags)`였다. [storage.py 80행][storage-read]의 허용 파일 읽기는 `os.open(path, flags)`를 사용하므로, 올바른 읽기여도 `invalid mode`가 발생하고 boundary latch가 켜진다.

[새 진단][guard-results]은 같은 허용 파일과 설치된 원본 sentinel을 사용해 세 조건을 비교했다. pathlib 읽기는 mode `r`로 성공했고, `os.open` 읽기와 원본 `read_workspace_file` 호출은 모두 BoundaryViolation으로 실패했다. 경로·해시 오류라는 대안 설명은 같은 파일의 성공 대조군과 실패 시점으로 기각했다. 원본 쓰기·controller·native·S0 실행은 없었다.

전파는 sentinel 설치→실제 component/storage 인증 읽기→정상 경로 거부다. 기존 [controller 테스트][assembly-tests]는 component 대역을 사용하고 sentinel 테스트는 거부 사례 중심이다. 따라서 47개 offline PASS와 이 결함은 양립한다. 최소 수정은 mode가 None일 때 세 번째 정수 flags를 엄격히 판독하는 공통 분기다. 재검증은 설치된 sentinel에서 원본 storage 정상 읽기 성공, 금지 읽기·쓰기와 잘못된 이벤트 거부, 허용 pending 출력만 쓰기 가능, latch의 기존 차단 동작 보존이다.

### F-03 — historical P4와 새 runtime을 같은 manifest 바이트에 묶는 현재 규약은 막힌다

**높음 / 정적 근거로 확인 / 이미 올바르게 BLOCKED로 보고된 선행 차단.**

정확한 original P4를 이번 감사에서 해시 일치로 복원했다. P4가 요구하는 runtime manifest는 `776e01215b3b2f9edf2c28630f49e36e0c57ae1887b71251758ce398815e7ee0`이고, T의 새 219파일 manifest는 `109150a1cf280fe730dae44c77561c5f0f33a52e42d85de40429c8b07b51d774`다. [semantic.py][semantic]의 전체 P4 검사를 거친 뒤 [profile.py][profile]가 새 6행 package에도 동일한 `static_material.runtime_files_manifest.raw`를 요구한다. 현재 두 입력 조합으로 이 equality를 만족시킬 수 없다.

원본 P4만 회수하면 해결된다는 설명은 기각된다. 회수는 historical 검증 준비의 일부일 뿐 서로 다른 manifest를 동일 객체에 강제하는 규약을 고치지 않는다. equality 한 줄만 지우는 것도 반환 profile 바이트·해시의 의미를 정의하지 못한다. 원본 P4 전체 validator를 실행해 reject를 관찰했다는 뜻은 아니며, 원본 profile 자체가 무효라는 판정도 아니다.

[CONTROL 결정][composition-decision]은 이 한계를 이미 정확히 밝힌다. 최소 수정은 historical 검증용 material과 현재 runtime/P5 바인딩을 분리하고, 반환 profile/hash가 무엇을 뜻하는지 명시하는 제한된 설계·profile 수정이다. 기존 P1–P4 핀·순서·전체 검증 및 서로 다른 package 혼합 거부는 보존해야 한다. 감사 권한으로 규약을 바꾸지 않았다.

### F-04 — alternate-stream 검사 중 오류를 정상 EOF로 취급한다

**중간 / 정적 근거 및 기존 API 대역 재현 확인 / 실제 OS 오류·전체 우회 미재현.**

[win32.py 307행][stream-code]는 FindFirstStreamW 실패의 오류값은 확인하지만 FindNextStreamW의 false 반환 뒤 오류값은 읽지 않는다. 기본 stream 하나를 본 뒤 열거가 오류로 중단돼도 `names == ["::$DATA"]`이면 검사가 통과한다. FindClose 반환도 확인하지 않는다.

인증한 [기존 대조 진단][stream-results]은 EOF=38과 예상 밖 오류=5를 비교했고 둘 다 허용됐다. API 호출 대역으로 원본 함수의 제어 흐름만 검사한 결과다. 이 false 반환이 언제나 EOF일 것이라는 설명은 함수가 실패 원인을 구분하지 않는다는 근거를 해소하지 못한다.

최소 수정은 false 직후 마지막 오류를 보존해 EOF만 인정하고, 닫기 실패도 정해진 실패 경로로 보내는 것이다. preflight와 publication 양쪽에서 오류=5·기타 오류·FindClose 실패를 거부하고 정상 EOF·기존 ADS 거부를 유지하는 작은 테스트가 필요하다. 현행 live 경로가 닫혀 있으므로 실제 리허설 PASS 우회로 확대 해석하지 않는다. native v0.5의 FindClose 보정과는 다른 파일의 별도 결함이다.

### F-05 — 종료 결정과 현재 재개 위치가 mutable 상태 문서에 끝까지 연결되지 않았다

**중간 / 공개 원문·현재 파일로 확인 / 삭제 원인과 모든 위임의 독립성은 미확인.**

[현재 ledger 47행][ledger]은 재구성 검토를 `OPEN / RECONSTRUCTION-MISMATCH-UNDER-REVIEW`로, 다음 단계를 fresh review와 CONTROL 결정으로 적는다. 그러나 공개 원문에서 마지막 독립 검토는 2026-09-08 06:16:03 UTC에 한정 PASS를 반환했고, 부모는 즉시 terminal 결정을 보고했다. 06:19:50 최종 답변은 문서 담당 재개·새 배정이 슬롯 제한으로 실패해 종료 반영만 남았다고 명시한다. [공개 인계 근거][handoff]와 [검토 원문][last-review]가 이를 뒷받침한다.

또 ledger 85–95행의 과거 원본 회수 CLOSED는 당시 기록으로는 맞지만, 현재 그 exact R 경로가 열리지 않는다. 등록 P에는 W의 최신 ledger 자체가 없다. 그래서 P에서 재개하거나 ledger만 읽으면 이미 끝난 검토를 다시 요청하거나 사용 불가능한 입력을 준비됐다고 판단할 수 있다. 이는 아직 관찰하지 않은 미래 오작업의 가능성이고, 실제 확인된 전파는 종료 반영이 끊긴 지점까지다.

외부 worktree나 미커밋 상태 자체가 결함이라는 설명은 채택하지 않았다. 원본 보호와 아직 없는 Git 승인이 합리적 이유다. 마지막 검토가 조기 완료됐다는 의심도 기각했다. 실제 공개 command 기록은 21개 파일과 33개 JSON 차이, 최종 package hash를 대조했고, 두 번의 실패한 검사 명령을 바로잡은 뒤 결과를 냈다. 결과가 후속 CONTROL 판단에 사용된 연결이 확인된다.

최소 수정은 기존 ledger와 적용 workstream에 종료 verdict, 현재 W/HEAD/미커밋 후보 범위, R/B exact 입력의 현재 가용성, 새 감사의 복원 위치를 반영하는 것이다. 역사 보고·원본 핀의 일괄 수정이나 폴더 이동은 불필요하다. 새 테스트·새 reviewer를 먼저 다시 돌릴 필요도 없다. 문서 역할의 후속 승인 작업으로 내용과 canonical sidecar를 갱신한 뒤, 별도 Git 승인 절차를 따른다.

### F-06 — E0 비용식에서 Q 재시작 인건비를 중복 계산할 여지가 있다

**낮음(현재 설계 단계) / 정의 충돌 확인 / 실제 비용 오계산 미관찰.**

[운영 비용 문서 175행 이후][e0-fixed]는 `C_fixed_run`에 Q 재시작 인건비를 넣는다. [332행 이후 현금식][e0-cash]은 다시 `C_human_Qrestart`를 더한다. 서로 다른 범주의 비용이라는 설명을 검토했지만, 어느 식에서 제외되는지 명시되지 않아 같은 재시작 비용을 한 번만 계산한다는 보장이 없다.

최소 수정은 그 비용을 fixed_run 또는 별도 항목 중 한 곳에만 포함하도록 정의하고 연결된 예산표·response의 용어를 맞추는 것이다. 비용 항목별 귀속표로 같은 인건비가 정확히 한 번 합산되는지 확인하면 된다. 실제 E0·효과 분석을 실행하거나 새로운 비용 프레임워크를 만들 이유는 없다. 실행 전 계획을 확정할 때 묶어 고칠 사항이다.

### F-07 — I0 단독 CLI의 성공은 frozen manifest 인증을 포함하지 않는다

**낮음 / 원본 소스와 인증한 기존 격리 진단으로 확인 / 후속 조립에는 backstop이 있음.**

[I0 brief][i0-brief]는 frozen bundle 무결성을 요구한다. integrity/schema-check/verify는 주어진 bundle의 자체 일관성을 확인하지만 bundle manifest 자체의 고정 digest를 검사하지 않는다. [기존 진단][i0-results]은 복사본의 example에 LF 한 개를 더하고 해당 manifest 행도 바꿨을 때 세 CLI가 여전히 성공함을 보여준다. `authenticate_public_file`은 같은 변경을 frozen manifest 불일치로 거부한다.

해시 manifest는 원래 자체 일관성을 검사하는 도구라는 설명은 타당하다. 따라서 이것을 전체 인증 우회로 부르지 않는다. 문제는 단독 `verify pass`를 frozen 입력의 승인 증거로 사용할 경우의 범위 공백이다. 실제 assembly parent는 시작 시 별도로 manifest pin을 확인하므로 확인된 후속 전파는 차단된다.

최소 수정은 frozen 입력을 뜻하는 CLI 공통 진입부에 이미 있는 pin 검사를 적용하거나 결과에서 `bundle_integrity`와 `frozen_bundle_authenticated`를 명시적으로 분리하는 것이다. 재검증은 원본 통과, 내용만 변경·내용과 manifest 동시 변경 모두 frozen 인증 거부, 일반 답안 검사의 oracle 비접근 유지다. 관련 코드 수정 시 함께 처리하고 독립 보조 관문은 만들지 않는다.

### F-08 — 두 보조 helper의 거부 범위는 표현된 계약보다 좁다

**낮음 / 한정 재현 확인 / 현재 고정 package·binary 우회는 입증되지 않음. 두 수정 위치는 구분한다.**

| 위치·직접 원인 | 판별 근거와 영향 | 최소 수정·재검증 |
|---|---|---|
| [canonical.py 86행][path-helper]: PurePosixPath.parts가 `.`를 먼저 접음 | `runtime/./a.bin`, `./runtime/a.bin`, `.`를 허용; `..`, 중복 slash 등은 거부. schema/native의 별도 원문 검사와 고정 manifest가 있어 전체 경로 탈출로 이어졌다는 증거는 없음 | 원문 성분 또는 정규형 동일성을 검사. 정규 경로 통과와 dot/alias 거부를 함께 확인 |
| [source_audit.py 408행][api-helper]: 제한된 이름 패턴으로 미분류 API를 탐색 | 메모리 소스에 추가한 `MoveFileW`는 허용, `GetTempPathW`는 거부. source helper 단독의 완전성을 뜻하지 못함 | 현재 요구에 맞게 helper의 보장 범위를 좁히거나 이름 분류를 보정. 기존 object·PE import 검사와 함께 확인; 실제 OS 호출은 하지 않음 |

두 결과는 [새 정적·메모리 진단][static-results]에 있다. native의 모든 공격면이 뚫렸다는 주장이 아니며, 단독 개선을 위해 새 parser나 보안 체계를 만들 실익은 없다.

## 4) 연결된 원인과 전파 경로

| 연결 | 확인된 부분 | 추론·제한 |
|---|---|---|
| 과거 고정 profile → 현재 runtime overlay → 동일 manifest 강제 → composition BLOCKED | F-03, 현재 validator, 복원된 P4, T manifest, 기존 CONTROL 결정 | 원본 P4 전체 유효성·전체 historical validator 실행 결과는 아님 |
| 정상 package 최초 허용 → 종료 전 P5 없는 exact set → 정상 transaction 거부 | F-01의 두 배열과 호출 순서 | native lifecycle은 앞단에서 막혀 실행하지 않음 |
| controller 정상 경로의 대역 테스트 → 실제 sentinel+storage 조합 누락 → 정상 읽기 거부 | F-02 재현과 테스트 구성 | 기존 47 PASS 자체가 거짓은 아님. 보장 범위를 넓히면 잘못된 완료 판정이 됨 |
| stream 열거 실패 → 오류와 EOF 미구분 → 제한 검사 통과 | F-04 함수와 API 대역 대조 | 실제 OS 실패 발생이나 전체 consumer PASS 우회는 미확인 |
| 마지막 independent review 완료 → CONTROL terminal 결정 → 문서 역할 슬롯 실패 → ledger 미반영 | 공개 시각·실행 기록과 현재 ledger가 직접 연결됨 | 이후 새 세션의 구체적 오작업은 입증하지 않음 |
| Temp 원본 경로를 현행 준비 상태로 간주 → 재실행 입력 없음 | exact 원위치·대체 위치 조회와 일부 해시 복원 | 외부 루트 사용 자체·삭제 원인·미공개 다른 사본은 판단하지 않음 |

한 가지 근본 원인으로 모두 묶을 수 없다. F-01은 중복 목록의 불일치, F-02/F-04는 API 결과 해석, F-03은 서로 다른 시대의 바이트를 결합하는 규약, F-05는 결정의 지속 기록 문제다. 각각 다른 수정과 판별 검사가 필요하다.

역사적 위임도 호출 수로 낭비를 판정하지 않았다. v0.5 CODE→TEST의 빌드·materialization→DOCUMENTATION 보고→한정 composition review→CONTROL 차단은 실제 산출물로 연결된다. original-static TEST→21개 생성물·33개 차이→DOCUMENTATION→fresh review→종료 결정도 연결된다. FindClose 누락을 밝힌 검토와 보정은 구체적인 실행 가능성 정보를 추가했다. 반면 잘못된 작업 폴더 확인과 마지막 문서 배정 실패는 기록된 운영 지연이다. [역할 dispatch 메타데이터][role-dispatches]는 CODE/TEST/DOC/REVIEW의 별도 배정과 fresh review 설정을 뒷받침하지만, 공개적으로 읽을 수 없는 개별 프롬프트까지 확인한 것은 아니다. 전체 역사에 역할 중첩이 없었다거나 모든 위임이 필요했다고 인증하지 않는다.

## 5) 의존 순서를 고려한 최소 수정 계획과 재검증 조건

**현재 요청한 real PUBLIC end-to-end 리허설 관문은 BLOCKED다. 다음 실행을 바로 여는 것은 부적절하다.** 먼저 현행 상태를 정리한 뒤, 기존 native 권한 계약을 유지할지 사용자 목적에 맞게 범위를 줄일지 결정해야 한다. 아래는 수정 계획이며 새 관문·코드 변경·게시 승인이 아니다. 예상 시간은 이 감사에서 얻은 거친 작업 시간 범위로, 대기·승인·설치 시간은 별도다.

| 순서·성격 | 정확한 작업과 유용한 결과 | 가장 싼 대안과 한계 | 예상 최선–최악 / 중단 기준 |
|---|---|---|---|
| 1. 보조 상태 정리, F-05 | 기존 ledger/workstream에 종료 판정·W의 실제 미커밋 범위·R/B 가용성을 반영. 다음 세션이 같은 검토를 반복하지 않게 함 | 이 보고서를 수동 인계할 수 있으나 기존 mutable index가 계속 과거 지시를 가리킴 | 10–30분. 두 기존 파일의 정리로 끝내고 역사 문서 일괄 재작성은 하지 않음 |
| 2. 핵심 프로젝트 작업의 요구 결정, F-03 | 기존 native 계약을 유지한다면 historical P4 검증과 current runtime/P5의 바이트 의미를 제한적으로 분리. 이후 실행할 하나의 정합한 입력 계약을 얻음 | 단순 오프라인 공개 stub 리허설은 표준 Python/subprocess와 기존 구성요소를 활용할 수 있음. 다만 현행 5-handle native 권한·bind/commit 계약을 충족했다는 주장은 할 수 없어 범위 변경 결정이 필요 | 30–90분. 현재 목표와 재사용처를 합의하지 못하면 custom native 보강을 더 권하지 않음. 역사 원본 전체 검증 증명이 필수라면 아래 잔여 자료 확보 전 그 주장을 중단 |
| 3. 선택한 실행 경로의 핵심 수정, F-01/F-02 | package 목록과 audit event 판독의 작은 코드 수정 및 판별 회귀. 둘 다 실제 정상 경로를 막는 직접 결함 | guard를 끄거나 P5를 지우는 대안은 frozen 경계를 위반하므로 사용 불가 | 두 수정 합계 30–90분. 정상·실패 판별이 되면 종료; 다른 native 보안 설계로 확대하지 않음 |
| 4. 관련 수정에 묶을 보조 보완, F-04/F-07/F-08 | 기존 stream·pin·경로/helper의 한정된 결함과 보고 범위를 정리 | fixed pin·schema·object/PE 검사와 명시적 nonclaim을 유지하며 후순위로 둘 수 있음. stream 실패를 정상이라고 판정하는 분기는 실제 경로를 열기 전 보정 필요 | 30–90분 상한의 별도 비용 판단. 30분 초과 또는 범위 확대 시 남은 이익을 재평가하고 사용자 결정; 새 verifier framework로 확장하지 않음 |
| 5. 선택한 경로만 재검증 | 코드/명세 바이트가 바뀐 범위의 테스트→독립 검토→명시적으로 승인된 benign lifecycle→필수 platform/live 연결 순서. 앞 단계 PASS를 뒤 단계 PASS로 승격하지 않음 | 기존 해시가 유지되는 테스트·빌드 기록은 재사용. 전체 설치·다운로드·과거 mutation 반복은 기본 선택이 아님 | 정적·단위 검사는 수분–30분. 실제 lifecycle/platform 작업은 계약·입력 확정 뒤 별도 견적. 최초 실패 원인 미분리 상태에서 추측 수정 반복 금지 |
| 6. E0 계획 확정 시 보조 수정, F-06 | 재시작 인건비를 한 번만 합산하도록 식과 설명 조정 | 실행 전에 계정 귀속표를 수동 확인할 수 있음 | 10–30분. 식 일관성 확인으로 종료; E0 실행을 열지 않음 |

재사용할 수 있는 것은 기존 I0–I3·assembly/adapter의 한정된 기능, 고정 빌드 입력, 해시가 유지된 binary·payload와 한정 검증 기록이다. 아직 충족하지 못한 전이 선행조건은 profile 결합 규약, F-01/F-02, native lifecycle, 그 다음 필요한 platform·live 연결이다. R/B 증거의 잔여 공백은 과거 원본 전체 검증을 현재 권위로 사용할 때의 별도 선행조건이다. 단순히 모든 역사 nonclaim을 닫기 위한 프로젝트는 권하지 않는다.

실제 수정은 현재 감사 권한 밖이며 해당 후보 범위와 역할 분리가 필요하다. 구현 수정 시 기존 source/manifest/report 핀의 영향 범위를 계산하고 그 범위만 갱신해야 한다. Git commit/push/main 통합은 별도 승인을 따른다. 되돌림은 승인된 후보 변경만 되돌리고 인증한 과거 파일·복원 원본을 보존하는 방식이다. 원본 파일 이동·삭제·무조건적 재설치는 필요하지 않다.

## 6) 정상으로 확인된 주요 의심, 미확인 영역, 사용자 결정 사항

정상으로 설명된 중요한 의심은 다음과 같다.

- **빌드·materializer 성공을 전체 구현 성공으로 과장했는가:** 검토한 후보 보고와 기계 기록은 lifecycle 0회·전체 미완료를 명시한다. 해당 의심은 기각한다.
- **마지막 독립 검토가 구현 PASS를 줬는가:** 아니다. task `01a07f9b-deb2-74c0-97da-411b694bc608`, 공개 최종 record 210의 판정은 오직 `RECONSTRUCTION-MISMATCH`에 대한 PASS다. 부모의 종료 인용도 이 범위와 맞는다.
- **재구성 recipe의 불일치가 original P4 무효를 증명하는가:** 아니다. 복원된 [recipe 80–165행][recipe]는 원래 P4에서 시작해 dummy runtime·guard·platform 자료 등으로 값을 바꾸는 시험용 baseline을 만든다. 이 한 recipe를 기존 원본과 같다고 가정할 수 없다. 8/13 충족·33개 차이와 validator 미호출은 그 제한된 시도의 올바른 결과다. 동일 시도를 반복할 이익은 확인되지 않았다.
- **과거 자료가 모두 사라졌는가:** 아니다. T 225/225, O 21/21, T 안의 base payload 174/174와 binary 3/3을 현재 해시·크기로 인증했다. 복원된 원본 P4도 정확한 고정 해시와 일치한다.
- **guard v0.4 이름, Temp 루트, 미커밋 후보, 이전 v0.4 테스트가 그 자체로 오류인가:** 아니다. 호환 ABI·격리 작업·Git 승인 상태·버전별 이력을 고려하면 설명된다. v0.4의 과거 성공은 v0.5의 현재 성공을 대신하지 않는다.
- **I0 frozen-input 테스트가 현재 AGENTS와 다르므로 제품이 고장났는가:** 과거 동결 입력을 검사하는 테스트의 역사적 pin 차이다. 현재 환경에서 전체 회귀가 새로 성공했다고 세지 않았으며, 이를 해결하려고 frozen pin을 덮어쓰는 수정은 제안하지 않는다.

C01–C15의 종료 상태는 다음과 같다. '판정 완료'는 모든 실행이 성공했다는 뜻이 아니라 중요한 의심이 확인·정상 설명·정확한 차단 중 하나로 정리됐다는 뜻이다.

| 항목 | 검토와 최종 판정 | 남은 제한 |
|---|---|---|
| C01 중앙 목적·v2.1 | 목적 330행, brief 295행, v2.1 전체, canonical protocol 391행·refreeze/질문 계약과 후기 실행 단계 대조. 준비/제품/효과 경계 확인 | 제품 기능·효과 결과 없음 |
| C02 I0 | 전체 모듈·483행 테스트·brief와 refreeze·public pin 대조. F-07 확인; transform/answer 목적 및 oracle 비접근 경계 확인 | 기존 35 PASS/1 symlink SKIP을 새 회귀 성공으로 세지 않음 |
| C03 공개 조립 | candidate/verifier 전체 흐름과 22+17+8 테스트, I1 인증/topology/runner·I2 lifecycle·I3 classifier/finalizer 대조. F-02/F-04 확인 | 실제 Win32 publication/live consumer 미실행 |
| C04 adapter | 정확한 closure·v0.3 실제 bridge, profile/preloader/evidence와 6개 테스트·실행 기록 대조 | offline diagnostic만 인정; native 실행 없음 |
| C05 runtime v0.7 | 다운로드 권위/핀/redirect/크기/추출/rename/probe/실패·재시도·테스트 및 표준 publication 승인 대조 | B 원래 identity/evidence와 raw r4 결과의 현재 재인증은 차단 |
| C06 E0 | 설계 223행·측정 307행·비용 433행·index/response/review 대조. A/D pilot·A/B/D confirmation, 인원·blindness·중단·비용 구분 확인. F-06 | 어떤 효과 수치·실행·경제성도 생성하지 않음 |
| C07 native 데이터·제어 | 3개 C++/공통 header·build/wrapper·Python profile/evidence/semantic/bootstrap의 연결·반환·종료 검토. F-01/F-03 | lifecycle 실제 결과 없음 |
| C08 경로·경합·retained objects | root/volume/ACL/reparse/경로 교체·retained identity·rename·출력·cleanup을 허용된 설계 의무와 대조. F-04/F-08 | 실제 동시 공격·동일 사용자 hostile parent·OS 공급자 전체 신뢰·post-close 전수 probe는 검증되지 않은 영역. 누락 자체를 새 결함으로 올리지 않음 |
| C09 실행·import closure | source→build inputs/trace→3 binary→object/PE 로그→219파일 runtime→실행 인자 연결 인증 | 22/52/29 호출 감사 기록의 당시 harness는 `2c3e6d…`, 현재는 `8a2a75…`. 현재 harness로 같은 감사가 새로 PASS했다고 하지 않음. live loaded-image 전체 closure 미검증 |
| C10 실행 가능성 | composition와 정상 package 재검사, Python storage 차단을 독립 분리. current gate·prerequisite를 재구성 | 현재 감사는 lifecycle/설치/네트워크 권한이 없고 앞단도 BLOCKED. 권한 부족을 코드 부재라고 판정하지 않음 |
| C11 R 원본 접근 | exact 원위치와 production/materialization/lifecycle/mutation/native-positive 대체 참조를 확인. recipe·P1–P4·R ledger/summary의 허용 대체 자료를 인증 | P4가 선언한 `776e012…` historical runtime manifest/전체 material은 확보되지 않아 원본 전체 validator 증명은 차단 |
| C12 B runtime 접근 | 원위치·T/O 참조·공개 command의 대체 bytes를 확인. base payload manifest와 T의 174개 payload 인증 | B prepublication/runtime/status evidence의 동일 바이트 및 원래 identity 미확보. 파일별 핀과 시도는 아래 자료에 기록 |
| C13 마지막 독립 검토 | 정확한 public 최종 판정과 17개 공개 command 기록, 21개 파일·33개 차이·최종 manifest 대조를 확인. 부모 인용과 일치 | 한정 검토의 범위 밖인 original 유효성·전체 구현 acceptance는 인증하지 않음 |
| C14 역사적 위임·활용 | 주요 v0.5 구현/FindClose/composition/reconstruction chain과 사용자 정정·dispatch·산출물·후속 결정을 연결 | 모든 개별 작업의 비공개 입력·세션 전체 독립성·기여 전수는 확인 범위 밖. 기록 없는 활용을 미사용으로 단정하지 않음 |
| C15 완료·인계 | 결과를 현행 ledger/workstream·후속 CONTROL 원문과 양방향 대조. F-05와 본 수정 계획으로 종료 | 원본 문서 정리와 Git 게시 자체는 수행하지 않음 |

정확한 복원과 잔여 자료 차단은 다음처럼 구분한다.

| 자료 | 인증 결과·복원 출처 | 막힌 판단 |
|---|---|---|
| historical recipe | 16,459 bytes, `adbc21322564ed5f17d6ccfdd5c3c344eaee4b313f3555f39da232e548bdcd00`; original-static reviewer 공개 command 107, `exec-1e87cedd-3566-4b04-aeb0-6044e4373536` 출력의 shell 최종 CRLF만 제외하여 원핀 일치 | recipe가 같아도 original runtime 전체 재구성을 보장하지 않음 |
| original P1–P3 | O의 package 사본에서 원래 3개 핀과 일치 | 이 세 파일만으로 전체 bundle 유효성을 판정할 수 없음 |
| original P4 | [복원 provenance][p4-provenance]: 인증한 33개 JSON 차이를 역적용, canonical bytes 10,819와 `266087f18cb16ced698fdfc8089a6ca305aac1d5d0278b1ee4c51f23044b3e9e`가 모두 일치한 경우에만 채택 | 원본 내용 회수는 성공. 해당 profile의 모든 외부 evidence 확보·전체 validator 실행은 아님 |
| base payload manifest | 34,849 bytes, `8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798`; 부모 공개 command 31049, `exec-fade0457-9439-47a2-8980-00bae8e8d617` | T payload의 동일 bytes는 확인. B root identity는 재현하지 않음 |
| R evidence ledger/summary | 부모 공개 command 34881의 원핀으로 정확한 bytes 복원. v0.4의 당시 70 reject·positive lifecycle 등이 기록돼 있음 | 개별 raw lifecycle/mutation 파일을 현재 다시 인증한 결과로 승격하지 않음 |
| B의 남은 3 evidence | [기록 대체 탐색][base-attempts]과 [원위치 조회][external-locators]. prepublication `0281893dce01d1aa54a1ad16cd621786615340844fcec35940095768e7dda9ca`, runtime `5d6b61194b5a7f0e53aeb78ac0bdee40f6edea294adecb0f8a7462751f6e6a84`, status `c8878e9df9d8c5979517efa3a9495b8e65c640b6f2c195fff029def6c262bbc6`의 동일 bytes 미확보 | 원래 r4 identity·전체 evidence의 현재 재인증 차단. 다른 임의 폴더를 광범위 탐색하거나 새 값으로 원핀을 바꾸지 않음 |

실행·증거의 구분과 재현 위치도 명시한다. 이번 감사의 Python helper 진단은 Windows 11 build 26200의 CPython 3.12.10에서 수행했다. 작업 위치는 P, 출력은 A/astra-max-clean이다. 다음은 현재 보존된 자료로 판별 결과를 재확인할 명령이다. 첫 세 명령은 진단 driver가 실제 사용한 하위 호출이며 이미 보존한 11-byte 비민감 scratch 파일을 읽는다. 최초 driver는 scratch directory를 새로 만드는 1회용이므로 그대로 반복하면 기존 directory 때문에 중단된다. 아래 명령은 native lifecycle을 실행하지 않는다.

```powershell
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B -X utf8 'C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/guard_open_diagnostic.py' pathlib_read
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B -X utf8 'C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/guard_open_diagnostic.py' os_open_read
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B -X utf8 'C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/guard_open_diagnostic.py' original_storage_read
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -B -X utf8 'C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/recover_original_p4.py'
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -B -X utf8 'C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/static_diagnostics.py'
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -B -X utf8 'C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/final_integrity_check.py'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/control/tools/verify-text-artifacts.ps1' -SelfTest
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/control/tools/verify-text-artifacts.ps1' -Path 'C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/AUDIT-REPORT.md'
```

실제 과거 assembly 47/adapter 6 테스트 명령과 종료 0은 [기존 실행 기록][prior-runs]에 있다. 해당 소스·manifest·runtime 바이트를 다시 인증한 후 재사용했다. I0 pin 진단과 stream API 대역 진단도 기존 자료의 제한을 유지했다. 새 static 진단은 native package 목록·path helper·API helper·composition의 필요조건을 확인했고 native 실행 횟수는 0이다. T의 1,512 ms materialization은 과거 기계 결과이며 이번 실행 시간이 아니다. Canonical validator SelfTest 11개가 통과했고 최종 보고·sidecar의 결과는 [최종 형식 검사][report-check]에 저장했다.

사용자 원문은 [감사 지시][audit-request]와 [공개 권한·인계 발췌][handoff]에서 추적한다. 관련 부모 task는 `01a03b3b-8bf3-74d0-9833-a89d29ce487f`이며 허용한 73,718,135-byte 범위의 공개 사용자/assistant 메시지와 선별된 공개 command만 사용했다. 기준 해시는 `bd2a2f1c3620211aaf8c7938a0e912f2e5a916f0a0f0b55eedf082518923aedd`다. 09-02 표준 도구 우선·불필요 확장 폐기, 09-04 열린 gate의 수정 연속성, 09-08 corrected 구현·FindClose 보정 및 별도 재구성 검증을 서로 다른 적용 범위로 보존했다. 다른 작업의 무관한 원문·비공개 내용·F0·hidden oracle·자격증명은 사용하지 않았다.

사용자 결정이 필요한 것은 감사 결과를 근거로 어떤 수정 범위를 열지, 기존 custom native 권한 계약을 유지할지, 과거 identity 증명을 실제 다음 작업에 요구할지다. 누락된 자료가 필요하다면 위 exact 파일과 핀을 가진 사본만 추가하면 된다. 공개 리허설의 범위를 줄이는 선택도 가능하지만 기존 보장까지 충족한 것으로 표시하면 안 된다. 이번 감사는 어느 선택도 대신 실행하지 않았다.

종료 기준 네 가지를 충족했다: 주요 기능·고위험 연결을 실제 소스와 기록으로 검토했고, 중요한 의심을 확인·정상 설명·정확한 자료/권한 차단으로 정리했으며, 수정 위치와 판별 재검증을 연결했고, 누락 범위를 공개했다. 이는 모든 버그 부재, 전체 과거 실행 증명의 재검증, 수정 완료 또는 공식 리허설 준비 완료의 선언이 아니다.

[baseline]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/baseline-before.json
[final-integrity]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/final-integrity.json
[purpose]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/docs/tradition/purpose-and-philosophy.md:17
[central]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/docs/proposals/v2/central-tradition-system-v2-integrated-candidate-v2.1.md
[build]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/native/build.ps1:64
[assembly-live]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_verifier/harness.py:648
[native-initial]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/native/s0_neutral_preloader_v0_5.cpp:1012
[native-terminal]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/native/s0_neutral_preloader_v0_5.cpp:1132
[static-results]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/static-diagnostics.json
[python-open]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_candidate/runtime_guard.py:211
[storage-read]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_candidate/storage.py:80
[guard-results]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/guard-open-results.json
[assembly-tests]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/public-end-to-end-v0.1/tests/test_candidate.py:584
[semantic]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/s0_public_runtime_preloader/semantic.py:404
[profile]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/s0_public_runtime_preloader/profile.py:246
[composition-decision]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/v0.5-implementation-profile-composition-control-decision-v0.1.md:3
[stream-code]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_verifier/win32.py:307
[stream-results]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max/assembly-stream-probe-results.json
[ledger]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/control/CURRENT-WORK-LEDGER.md:47
[handoff]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/public-authority-and-handoff-evidence.json
[last-review]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/review-public-records.jsonl
[e0-fixed]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.4.md:175
[e0-cash]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.4.md:332
[i0-brief]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/control/i0/i0-implementation-brief.md:64
[i0-results]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max/i0-manifest-probe-results.json
[path-helper]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/s0_public_runtime_preloader/canonical.py:86
[api-helper]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/s0_public_runtime_preloader/source_audit.py:408
[role-dispatches]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/public-role-dispatches.json
[recipe]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/historical-recipe-exact.py:80
[p4-provenance]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/recovered-P4-provenance.json
[base-attempts]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/base-evidence-recovery-attempts.json
[external-locators]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/external-locator-auth.json
[prior-runs]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max/prior-execution-records.json
[report-check]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/canonical-report-check.txt
[audit-request]: C:/Users/SSAFY/.codex/attachments/1fa0dbf0-75e6-42d5-bf54-f9230d7b86af/pasted-text.txt
[protocol]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/control/s0-protocol-v0.3-canonical-r1.md:1
[question-decision]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/control/f0-public/question-contract-v0.14/control-integration-decision-v0.1.md:1
[i0-cli]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/i0/implementation/s0_i0/cli.py:1
[controller]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_candidate/controller.py:1
[adapter]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/public-end-to-end-v0.2/implementation/s0_public_assembly_integration/candidate.py:123
[runtime-v07]: C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/implementation/s0_public_build_runtime/materialize.py:475
[evidence-auth]: C:/Users/SSAFY/AppData/Local/Temp/human-ai-development-tradition-independent-audit-20260908/astra-max-clean/evidence-reauthenticated.json
