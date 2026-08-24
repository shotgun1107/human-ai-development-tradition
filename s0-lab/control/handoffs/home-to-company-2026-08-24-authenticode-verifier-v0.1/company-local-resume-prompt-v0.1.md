# Company-PC resume prompt: Authenticode verifier v0.1

Use the following prompt in the existing company CONTROL session. Replace the
two angle-bracket final-handoff values with the exact values from the home
CONTROL completion report.

```text
당신은 human-ai-development-tradition 프로젝트를 회사 PC에서 이어받는 기존 CONTROL 세션이다.

과거 대화 기억은 보조 정보로만 사용하고, 현재 Git 상태·최신 AGENTS.md·인증된 저장소 기록을 정본으로 삼아라. 새 clone이나 기초 설치를 처음부터 반복하지 마라.

repository:
https://github.com/shotgun1107/human-ai-development-tradition.git

home→company handoff branch:
codex/home-to-company-handoff-20260824-authenticode-v01

exact final handoff commit:
<FINAL_HANDOFF_COMMIT_FROM_HOME_CONTROL_REPORT>

exact final handoff tree:
<FINAL_HANDOFF_TREE_FROM_HOME_CONTROL_REPORT>

required payload commit and final-tip sole parent:
9b32090c06ab8f8c38f9540f07c04ee3b785a364

payload tree:
90ec2aa376cf9532d54a240619442b3a9ee823b9

payload parent:
2709a46faf5502e96c24bc7731e201398042b6b6

handoff 시점 origin/main:
39263f431a82649ddc0bbd3545ed6d95b0780adc

이번 첫 작업은 회사 기존 작업을 보존하면서 exact final handoff tip을 동기화·인증하고 상태를 보고하는 것뿐이다. 구현, 테스트 재실행, 하위 에이전트, 문서 수정, commit, push, PR, main 병합 또는 다음 기술 gate를 시작하지 마라.

fetch 전에 기존 회사 저장소의 path, origin, branch, HEAD/tree/parent, upstream, tracked/staged/unstaged 상태, untracked/ignored aggregate, stash, local-only commit, refs와 worktrees를 읽기 전용으로 확인하라.

dirty 작업, stash, local-only commit 또는 충돌 가능한 별도 worktree가 있으면 기존 worktree를 switch, reset, clean, stash, rebase, merge, cherry-pick, prune하거나 덮어쓰지 마라. exact handoff commit은 별도 clean detached worktree에 배치하라. 기존 저장소가 완전히 clean한 경우에만 exact branch를 fetch하고 pinned commit을 materialize하라. unpinned git pull은 사용하지 마라.

F0 세 경로는 Git 동기화 대상이지만 AI 입력은 default-deny다.

- s0-lab/control/f0-sealed/**
- s0-lab/f0-sealed-staging/**
- s0-lab/reviews/f0-sealed/**

내용과 내부 filename을 열거나 검색하거나 출력하지 마라. aggregate 32/11/10과 quiet/anomaly 상태만 확인한다.

fetch 후 다음을 검증하라.

- live remote handoff tip = <FINAL_HANDOFF_COMMIT_FROM_HOME_CONTROL_REPORT>
- final tree = <FINAL_HANDOFF_TREE_FROM_HOME_CONTROL_REPORT>
- final sole parent = 9b32090c06ab8f8c38f9540f07c04ee3b785a364
- payload tree = 90ec2aa376cf9532d54a240619442b3a9ee823b9
- payload parent와 origin/main이 final tip의 조상
- implementation branch `codex/s0-windows-authenticode-verifier-v01`의 remote tip = 9b32090c06ab8f8c38f9540f07c04ee3b785a364
- local/remote commit과 tree 일치
- worktree/index clean
- F0 aggregate 32/11/10, payload parent 대비 변경 0

동기화 후 최신 AGENTS.md를 완독하고 canonical validator SelfTest를 실행하라. 다음 PUBLIC 파일과 sidecar/manifest를 인증·완독하라.

1. s0-lab/control/handoffs/home-to-company-2026-08-24-authenticode-verifier-v0.1/current-state-handoff-v0.1.md
2. s0-lab/control/handoffs/home-to-company-2026-08-24-authenticode-verifier-v0.1/company-local-resume-prompt-v0.1.md
3. s0-lab/assembly-rehearsal/windows-authenticode-verifier-v0.1/verification/implementation-files.sha256
4. s0-lab/assembly-rehearsal/windows-authenticode-verifier-v0.1/verification/verification-files.sha256
5. s0-lab/assembly-rehearsal/windows-authenticode-verifier-v0.1/verification/public-windows-authenticode-verifier-implementation-candidate-report-v0.1.md 및 sidecar

기대 SHA-256:

- implementation manifest: 11e2f27fc4993f8b60bca17852f2112fb1d20c901b7044572deb325147cafc6f
- verification manifest: 5f70306946c4ac70f314abe373f7b415e785a845fcca1e77f34a8e8748e81ebc
- implementation report: 2f4473274e7a9b575fc0c848f4806d0b56c6b6218aa5b9aac6250343c585f54c

과거·현재·미래 순으로 짧게 보고하라.

- 과거: v0.2 trust-profile review가 3 BLOCKING으로 종료됨
- 현재: 실제 verifier candidate가 구현됐고 PUBLIC synthetic 13/13 및 authenticated snapshot 검증을 통과했지만 독립 code/security review와 live native 실행은 없음
- 미래: 다음 후보 gate는 아래 독립 구현 검수이나 이번 동기화 프롬프트에서는 열지 않음

S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE VERIFIER IMPLEMENTATION V0.1 INDEPENDENT CODE AND SECURITY REVIEW OPEN

보고 후 멈춰라.
```

