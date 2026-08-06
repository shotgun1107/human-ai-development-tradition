# Home local resume prompt

아래 내용을 집 PC의 새 Codex 작업에 그대로 전달한다.

---

당신은 `human-ai-development-tradition` 저장소의 S0 준비 작업을 이어받는
새 CONTROL 세션이다. 이전 Codex 대화나 세션 정체성을 재사용한다고
가정하지 말고, 저장소의 해시 기록과 실제 테스트 결과만 근거로 판단하라.

## 저장소와 브랜치

- repository: `https://github.com/shotgun1107/human-ai-development-tradition`
- branch: `codex/i0-public-harness-candidate`
- reviewed I0 candidate commit: `73c98f8`
- current branch HEAD may be a later handoff-only commit; verify that `73c98f8`
  remains in its history
- branch purpose: 독립 재심사를 통과한 I0 공개 하네스 후보 보존

저장소가 어느 절대경로에 clone되거나 Codex worktree가 어디에 만들어져도
괜찮다. 모든 실행 경로는 현재 repository root에서 상대적으로 계산하라.
과거 문서에 기록된 `C:/Users/SSAFY/AppData/Local/Temp/...` 경로는 당시의
증거 기록일 뿐 현재 실행 경로가 아니다. 그 기록을 새 PC 경로로
덮어쓰거나 기존 sidecar 해시를 고치지 마라.

## 현재 사실

- S0는 아직 실행되지 않았다.
- 중앙 시스템, Project Brain 연동, 운영 안전성, 경제성, 모델 간 전이는
  구현되거나 검증되지 않았다.
- 숨은 정답과 봉인 fixture는 이 저장소에 없다.
- I0 구현 후보는 독립 제한 재심사에서
  `I0 implementation acceptable but upstream refreeze required` 판정을 받았다.
- I0 candidate manifest SHA-256:
  `e67004179fc9d922b9fb6d822ac961d576f9c6ca07cd512d4508e29ca038c105`
- F0-PUBLIC v0.1의 B2 package ID/path가 세 schema의 12자 계약과 충돌한다.
  지정 검사는 4 errors, 확대 감사는 관련 20 errors를 보고한다.
- 이 상위 결함 때문에 I0는 아직 동결되지 않았고 sealed F0도 닫혀 있다.

## 첫 허용 입력

처음에는 저장소를 광범위하게 검색하지 말고 다음만 읽어라.

1. `AGENTS.md`
2. `s0-lab/README.md`
3. `s0-lab/control/i0/i0-gate-decision.md`
4. `s0-lab/reviews/i0/i0-limited-rereview-v0.1.md`
5. `s0-lab/i0/README.md`
6. `s0-lab/i0/verification/verification-report.md`
7. `s0-lab/i0/verification/implementation-files.sha256`
8. `s0-lab/public-practice/v0.1/bundle-files.sha256`

각 `.sha256` sidecar가 있는 문서는 사용 전에 검증하라. Candidate manifest는
자기 자신을 제외한 정확히 15개 파일과 일치해야 한다. Public bundle
manifest는 자기 자신을 제외한 정확히 90개 파일과 일치해야 한다. 해시나
파일 집합이 다르면 수정하지 말고 중단해 차이를 보고하라.

## 집 PC 환경 재구성

기존 외부 virtual environment는 전송되지 않았다. repository 밖의 새
위치에 Python 3.12 virtual environment를 만들고 다음 dependency만 설치하라.

```text
jsonschema[format]==4.26.0
```

설치 후 repository root를 현재 위치로 사용하고
`s0-lab/i0/implementation`을 `PYTHONPATH`에 추가한다. 테스트 중 bytecode가
저장소에 생기지 않도록 `PYTHONDONTWRITEBYTECODE=1`을 설정한다.

다음을 실행하라.

```powershell
python -m unittest discover -s s0-lab/i0/tests -v
python -m s0_i0.cli integrity
python -m s0_i0.cli schema-check
python -m s0_i0.cli verify
```

예상 결과:

- unittest: 총 36, 35 pass, symlink 권한이 없으면 1 skip
- integrity: exit 0
- schema-check: exit 1, designated 4 / broader related 20
- verify: exit 1, 상위 frozen-input 결함을 유지한 fail

`schema-check`와 `verify`의 exit 1을 환경 재현 실패로 오해하지 마라. 지정된
상위 결함을 정확히 검출한 결과다. 다른 error count, hash mismatch, extra
file, test failure가 나오면 다음 단계로 가지 말고 보고하라.

## 세션과 경로 규칙

- 과거 `/root/i0_...` 세션을 재사용하지 말고 필요한 역할은 새 세션으로 만든다.
- worktree는 편집 충돌 격리일 뿐 비밀 보안 경계라고 주장하지 않는다.
- fixture author 세션을 executor로 fork하지 않는다.
- executor A-D는 실제 R0 직전에 각각 fresh non-fork 세션으로 만들어야 한다.
- hidden oracle은 repository나 executor-visible worktree에 두지 않는다.
- 기존 frozen 문서와 해시는 집 PC 경로에 맞춘다는 이유로 수정하지 않는다.
- commit, push, merge는 사용자의 별도 지시 전에는 하지 않는다.

## 현재 세션의 종료 조건

이 첫 세션에서는 위 환경·해시·테스트 재현까지만 수행하고 다음 내용을
사용자에게 보고하라.

1. 실제 clone/worktree 경로
2. branch와 HEAD commit
3. candidate 15-file 및 public 90-file 무결성 결과
4. Python/jsonschema version
5. unittest, integrity, schema-check, verify 결과
6. 확인하지 않은 범위

그 뒤 멈춰라. F0-PUBLIC frozen 자료는 사용자가 새 대화에서 정확히
`F0-PUBLIC REOPEN`이라고 승인하기 전에는 수정하지 마라.

게이트가 열리면 권장 수정 방향은 schema를 느슨하게 확장하는 것이 아니라
네 B2 package stem을 `P0xB2EMBER001`에서 고정 12자 형식인
`P0xB2EMBR001`로 바꾸고 모든 공개 reference와 dependent hash를 다시
동결하는 것이다. 사실, 질문, 선택지, 변환 의미, expected decision,
scoring rule은 바꾸지 않는다. 수정 후 전체 적용 가능한 schema 검사,
I0 회귀, CONTROL 검증, 독립 제한 재심사를 다시 수행한다.

---
