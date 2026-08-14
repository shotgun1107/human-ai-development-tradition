# S0 v0.14 runtime profile and neutral preloader v0.4 rereview start prompt

Use this entire text as the CONTROL message that opens the fresh independent
rereview. Conversation history is not evidence. Git objects and the exact
externally pinned paths below are the only repository evidence.

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.4 INDEPENDENT REREVIEW OPEN`

You are a fresh independent public-design rereviewer. Perform the rereview
defined by the admitted v0.4 rereview brief. This is a read-only role. Do not
call another agent and do not use an earlier reviewer conclusion.

## Authenticated Git identity

- repository: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- authenticated source ref:
  `refs/remotes/origin/codex/home-to-company-handoff-20260813`
- authenticated source-ref tip:
  `c5227d1dd56c9633e8c52cf863d9ffba2f94c89b`
- review commit: `c5227d1dd56c9633e8c52cf863d9ffba2f94c89b`
- review tree: `f0527421a774c5c7f7823ab2ac5d165c282649f8`
- sole parent: `a44e68d2994168a87bbf63d1b9f016496b82908b`
- parent tree: `ccc418fa7ce415718f3facf39cacf62df4872263`
- payload parent: `f336995da41d201a9132246d7fffd0506f9a5a01`
- payload-parent tree: `c3c351b2dcf2fc19364a7b5248c13343ae6345dd`
- authenticated `origin/main` identity:
  `41e0b684a7cca387be6d264c4a5b63de2561fd7c`
- authenticated `origin/main` tree:
  `a14e8b9c9bc8905060cd8811e8934643e2aa4aa3`
- expected initial source state: `HEAD` exactly at the review commit in an
  isolated worktree, whether detached or attached to an exact local source
  branch, with an empty `git status --porcelain=v1`, a clean index, and no
  untracked or unclassified ignored path

The source-ref tip, review commit, local commit, and review tree must reproduce
exactly. The sole-parent relation must reproduce exactly. The payload parent
and authenticated `origin/main` identity must both be ancestors of the review
commit. Do not fetch, pull, switch, reset, clean, merge, rebase, or modify the
source while reviewing.

## Exact repository input allowlist and external SHA-256 pins

Every following line is one individually admitted file and its external
SHA-256 pin. This is a literal maximum list, not permission to list a
directory, follow an implementation-manifest row, infer a sibling, or open a
same-directory file. Access each path individually. All unlisted repository
paths are denied.

```text
7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86  AGENTS.md
b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3  s0-lab/control/tools/verify-text-artifacts.ps1

0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623  s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/implementation-files.sha256
520a237109686a17b8c075c15f1cc676a43d450716a6157bce7b48585f0c5005  s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/public-end-to-end-assembly-rehearsal-implementation-candidate-report-v0.1.md
02d6898e11eabb3313a433e37a22ae6daa2803b99accd8c0963e1980638b5053  s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/public-end-to-end-assembly-rehearsal-implementation-candidate-report-v0.1.sha256

10a9f506231a14b291df1771f08f000d7944642b21e74d8f454c483d7cf05ac6  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/assembly-rehearsal-acceptance-plan-v0.3.md
62f23f0761d18b8ac2444646d97d79b7b6d094fb9c049c80292055c58fc8a757  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/assembly-rehearsal-acceptance-plan-v0.3.sha256
d107a121b33adb3f88f391936dec7dda816ddeb0ae1d86b9f579ff5694c779aa  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/assembly-rehearsal-interface-map-v0.3.json
121a6124243407e6181f846581874fa38ded5887fa289c7f2df7221badd17ad3  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/assembly-rehearsal-interface-map-v0.3.sha256
91cc9c176e9e55640f27117199d7c78694810f7a5ba6c9699bdbbc653368fd65  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/design-package-files.sha256
f949272c789e68c01573683c1052c71ce533e3b08874f52acb7b321ca062c768  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/independent-review-brief-v0.3.md
ffb0ff435b6c35b9554aaf4704fa1d9d688cf93fd60fe7d5ddab3a5dff2d9e8b  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/independent-review-brief-v0.3.sha256
57f148c89fceb636520a3686ad0447805307ac8b3904b24d60b9c3a24c6bc99d  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/public-end-to-end-assembly-rehearsal-design-revision-v0.3.md
07736a9797d139206812d9d73a1342424b7e0ae76727abf2540bd8145d38c3db  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/public-end-to-end-assembly-rehearsal-design-revision-v0.3.sha256
52695ddaa291105f4720bf8b5fde7db09d84a427a4732b948c56d4bb35d92ea2  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/v0.2-independent-review-response-v0.1.md
712bcfdfb60ccba1d322e89efcb34f53006cef37210aa00a7609fd8ecdcddfe4  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.3/v0.2-independent-review-response-v0.1.sha256

29d484be84e7387edb7cd1f7f07b12f9ddc6f4ee172dd9fc4d7bbcace001139a  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/assembly-rehearsal-acceptance-plan-v0.4.md
4089e1d634d560cf847f6560ed03deb33460baa7f4ca24539b612c88b4922dfe  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/assembly-rehearsal-acceptance-plan-v0.4.sha256
a6a45170816fc11e76fd5e326bd0486d161738fffb4b6c2353e92d79db66f81f  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/assembly-rehearsal-interface-map-v0.4.json
2de41e81f55a863a59a85a8df8d220a39d21f6c1c183bcfd8c63007b7c2e7720  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/assembly-rehearsal-interface-map-v0.4.sha256
35535d9d2f35d18324160208bb662274539ecd76f8f263c20f243a1aa8dbf85e  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/design-package-files.sha256
3f583ef1bc79613a242c1c1c17c521987e6409e6f2cbb6c2366082e0086e77c5  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/independent-rereview-brief-v0.4.md
bcea52c03379dc72e0bd7a38ecdd35352776a0f2ce0c25a5b5c0e0a2cf1d4609  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/independent-rereview-brief-v0.4.sha256
65f673c303835a9c49c6feaf7d01115fc02be0d252a3a443f8695bb4e4136973  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/public-end-to-end-assembly-rehearsal-design-revision-v0.4.md
3e6be3b9468f79e237beba8260dc45b7ea19138e165d3c43fdb4c51ec8cf139e  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/public-end-to-end-assembly-rehearsal-design-revision-v0.4.sha256
e433e8502c2ba68ee55d987ae692cc296881f24fc6158de70186741e726dbffb  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/v0.3-independent-review-response-v0.1.md
dd0f5766ccfbb9ffff1b2311f3a2791e0761506a902895cf61e89f948eee40c3  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.4/v0.3-independent-review-response-v0.1.sha256

82c1bdcbf74ae4135b1c7b8522e261f8e5124bcde353a87adc924a2908b07e0c  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/assembly-rehearsal-acceptance-plan-v0.5.md
ec014b9a07ea8066584a813abb6c50eb26b311afa971d16b9e1015fc438e4789  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/assembly-rehearsal-acceptance-plan-v0.5.sha256
6c2f5ac03ee6cbfad406e96c5cb35ceb5f548e74f04c37e71307b155a18915a4  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/assembly-rehearsal-interface-map-v0.5.json
90e94113dc073a0c975fd0ad54260f0e1101b46e8161c8753336e15de66d84a0  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/assembly-rehearsal-interface-map-v0.5.sha256
6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/design-package-files.sha256
34b73448430d3d9978ed804829cafff630b53965e087314531e1f525380ea625  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/independent-rereview-brief-v0.5.md
a518ff1f442229f58359f6ee1dea4ceb861687559fbde4f9596e2c40c27fa314  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/independent-rereview-brief-v0.5.sha256
849e0655e7f73b78eeb039b09357c48f150c637f8cf527dec2a9990b9d240f5b  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/public-end-to-end-assembly-rehearsal-design-revision-v0.5.md
46cc46233a437e41b7c90e0f8f1ac8ed03356faa34b9361a5141af1eab6b9ab6  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/public-end-to-end-assembly-rehearsal-design-revision-v0.5.sha256
70341264ae740f05fabdf78f69bcd8fa4bbf2fe73e6ed764fcb65b4c58827c0d  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/v0.4-independent-rereview-response-v0.1.md
2c9965ad5c7753a28193967c6c00d8a277ebee4271bd2f39088e2b182f152cbd  s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/v0.4-independent-rereview-response-v0.1.sha256

13b69bfd8614ea57e49d317902e9563bd8a47eaa13a06be22065f81177b29cad  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/design-package-files.sha256
3a6bdb5aadc4d08a5b83b9902e2d4f8b967fd6e7f49d047b064de191b7a3f465  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/neutral-preloader-launch-envelope-v0.1.schema.json
d2992ee93498a3c3b1a34b21fb5ffbe09460055a6b9ebbe91924ab80353d46b7  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/neutral-preloader-launch-envelope-v0.1.schema.sha256
ab9e87d7466e9fdd2c1c84ebd13b3ee074be29994f6ef01538e4a25ff38e22d5  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.1.md
3342d2140d6c4932f7d77443bcdbf85abe6bebbbfd3c3af6437ec76adbf76b85  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.1.sha256
7bf62dc57457e289e7e2ad4328ca8ab18f1946ee790ff823e9b1e9c4bd0c6e2d  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/public-assembly-runtime-profile-neutral-preloader-design-v0.1.md
6c860ec0182350ffed1e9d3650dc4f2da83988641a84a288861a63008dd7dae9  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/public-assembly-runtime-profile-neutral-preloader-design-v0.1.sha256
a165cc9b85619b60dba44159d52509e455ef47bac5e5de916e62f00d43af7c6c  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/public-assembly-runtime-profile-neutral-preloader-independent-rereview-brief-v0.1.md
01ab84cce9819634f3b16b0f8c48a00e669b655ce7e5cf49ac6aa284e9b158dd  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/public-assembly-runtime-profile-neutral-preloader-independent-rereview-brief-v0.1.sha256
4e30264abae5e452fcd6b1ee09c0a8e7685ee34fb676fecf9acb632560146af2  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.1.json
0ecacd1c0e379892fded84bab659a4a5a62a82f0d38f8c745483a5eb756cb22a  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.1.sha256
92943a96249c312d0e2631705a667170d60d22d8e75f2571961ed1f728e934af  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/runtime-profile-v0.1.schema.json
96dd1a14ed4a1fa4c88b5f661c13e92dc1c6bb998202f88d9a23e08b864d2676  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/runtime-profile-v0.1.schema.sha256

fed4c2151f0bebcda14b84551c529ae4d9449a3f9637ce79fd7d312c50d2e68e  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/design-package-files.sha256
c5eab082c3e35f871cfac06b5f38f6e5202d061bc29ea3228e6f6db601e3b587  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.2.md
70199ae7db632699f36652d915697c8f900ebc10a91ad4d98c032aee4d09329b  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.2.sha256
72bfafac0349b1bc047ead67fef6466c5d398dcaef62cd77da256174f954a642  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/public-assembly-runtime-profile-neutral-preloader-design-revision-v0.2.md
efbcc4bb62333e3b74be3c7a09ad3d7b1ca5ca5f45463bac0789be93f8938333  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/public-assembly-runtime-profile-neutral-preloader-design-revision-v0.2.sha256
ae69c19288e46a3d41119f908037e361977f7d4d19d399b3970fbdcf166694b5  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/public-assembly-runtime-profile-neutral-preloader-independent-rereview-brief-v0.2.md
e3c4797888bcd81a7007caaee20567303180c38ea45dc7d9af60ab1575c611f7  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/public-assembly-runtime-profile-neutral-preloader-independent-rereview-brief-v0.2.sha256
8910d41472a4e87e8303f1a0086dfc3cb02479446a0f83b3f8ca261bd03d8d7d  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.2.json
962d2fdd19a6bc6a7ec5d6db546fee61f17c023231ede6fde88a95c7763287a8  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.2.sha256
e2e96940bbafc6a80987634fe794d700844dbc7d0b48e0e269922f03364fb34f  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/runtime-profile-v0.2.schema.json
dfb23ccec217e943d434850352b24c599180a8aeb454b6918c2865a9be9141af  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/runtime-profile-v0.2.schema.sha256
6ba27af855903200263e6822dae95009e906ece9766838d324ae8000e8007a74  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/v0.1-independent-rereview-response-v0.1.md
3bbef6e443787d8fa2f224ab3700bf69b12f1608a29485e5965caa5331ac2c7b  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/v0.1-independent-rereview-response-v0.1.sha256

c2ecd2931e15a99b68d3e669026342f59a42995268f8b4937ba96e63d731481b  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/design-package-files.sha256
a20d0dab51fb038ecda998dcbd8dbbd9483797b723a843e39368281e65716a13  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.3.md
fd7273c2d9eb275bd7df49318b7a5eae7cee10f09036c505d4f9be637eb6d9a0  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.3.sha256
971d15f4fe666d656973898a0aa38b92370cd4b8a89e92aaff00ecf7241e9456  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-design-revision-v0.3.md
2e151779544a0f3a270c36d1a2db0a1ac663652e23122f9751e798dc611e9cf7  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-design-revision-v0.3.sha256
7ed10a59b4259957b695b36ddf9146866db35d82694e3d3ac5858a1366f56e86  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-independent-rereview-brief-v0.3.md
119535f7439bd346882ac77f24932d837d3b0b34fece494799780fe1df9bb17f  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-independent-rereview-brief-v0.3.sha256
30d39aa73734173c0d7908bf97fb8a75d42eafca8997f464b3001ff22abbaf39  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.3.json
624b1aec1c0812c2f402e20242d40453227635282cf504188de4b3e0f0908f81  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.3.sha256
1404f4981d3d7815e98a6c5d745596f15bb8d50a296410584d03d7ccb11ce3dd  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/runtime-profile-v0.3.schema.json
0a02deb76d5f02c38c12e4afe1d3ef8581d3b816ac800546561a1adbf78216d6  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/runtime-profile-v0.3.schema.sha256
907ab773d4998b05547f6b4eaa40a99a6c8a9420a07f2ae7709f6bb7b141354b  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/v0.2-independent-rereview-response-v0.1.md
374feefb0b0edc1a383aa48d34ebba8c37f3e1bf1441134886c17fe0cdae03c5  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/v0.2-independent-rereview-response-v0.1.sha256

abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/design-package-files.sha256
d3f38fd948198fb2c6f310cab47c5852b2b4df7e806d27c686c5c9fe3fc39e2d  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.4.md
b0c07030e01754f3f27032998151c820cea097e4012fd58a92cafa452d1d66e6  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.4.sha256
ffb4d9672a2d81f6412cb57ffb8636a4af21f4733061573a535487c50cc0b352  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-design-revision-v0.4.md
370ba6c49d7908baa1ac7a7d2ca5b29faf0a0205a166bb0cd18fd1d423cdb4b2  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-design-revision-v0.4.sha256
0afcf05370782a4f31a6255f6df14c0e0a1d52fb44b681ba8218711c005f30eb  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-independent-rereview-brief-v0.4.md
48e65493711438e66c860d9ec99ba4a5ce6d4e9584ba381bc881c74559eacff7  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-independent-rereview-brief-v0.4.sha256
63b36e5b7a6f1aad8027b5794cf21221a05d8eb057f4c0c1d0350b67a12ec2a7  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.4.json
689545e36c44946c943e22ee3f9c7b99553908c110872525306ecd73e0f512dc  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.4.sha256
3cdcf7e39d39536213f5ab577970f39643b13aa542d854176c213590a16f92dd  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/runtime-profile-v0.4.schema.json
575d5c39e79003acac7a53f2bbfbfec8bddbe12909ba31f97751571ecb497c89  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/runtime-profile-v0.4.schema.sha256
7351c19f8a2238c09e08dc4b6a1760a9a27734bd1d100d6e747824503b45ba23  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.3-independent-rereview-response-v0.1.md
2d977cf450198fdaa3717a7b9e52979d7b73e7bdc8f24ea1f1c1fc360fd9695a  s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.3-independent-rereview-response-v0.1.sha256

7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137  s0-lab/reviews/assembly-rehearsal/public-end-to-end-v0.5/public-end-to-end-assembly-rehearsal-design-v0.5-independent-rereview-v0.1.md
73a252b246e9f392f1ff34433ee156fb05bdd50fa80b7bf3b64d9a69878f0597  s0-lab/reviews/assembly-rehearsal/public-end-to-end-v0.5/public-end-to-end-assembly-rehearsal-design-v0.5-independent-rereview-v0.1.sha256
e1423b6d61c95407eeb34f03ba5dacdd372fb4fbbd500c4734af8f3df424eb29  s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/public-assembly-runtime-profile-neutral-preloader-design-v0.1-independent-rereview-result-preservation-record-v0.1.md
da9042007cb9aa57ad84849ee36be6c2b65e71b93cfcd4669c60ec0bd550eb9d  s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/public-assembly-runtime-profile-neutral-preloader-design-v0.1-independent-rereview-result-preservation-record-v0.1.sha256
99896e35937f5cfce2493aeda059063e25aad58e5b64de5965042b473f1ce090  s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/v0.2-independent-rereview-result-record-v0.1.md
8cfce2e3fbf0c376f9940350a6c4abce70a0ede108e47d29c5646f18b424f736  s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/v0.2-independent-rereview-result-record-v0.1.sha256
9085e20666fdaa1246e47430993149f103c31c4e0e64652ad57d77bbed42675e  s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/v0.3-independent-rereview-result-preservation-record-v0.1.md
831cc761030c92ef46560803f8cc111429c25a462b60ede2aba08321d448f747  s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/v0.3-independent-rereview-result-preservation-record-v0.1.sha256
```

The allowlist contains exactly 98 files. The implementation manifest and
candidate report are admitted only for structural authentication and bounded
candidate-status context. Do not open, hash, or follow any implementation
manifest target. Implementation source and tests remain denied.

The three F0 path families named by root `AGENTS.md` remain content-denied.
Do not list them or inspect their contents or filenames. No F0 operation is
needed for this rereview.

## Required execution and result

1. Read root `AGENTS.md` completely.
2. Authenticate the exact Git identities and expected clean state above.
3. Reproduce all 98 external hashes before substantive reading.
4. Run the admitted canonical validator in `-SelfTest` mode before relying on
   it.
5. Complete every authentication-preflight step in the v0.4 rereview brief,
   including same-basename sidecars, duplicate-key JSON parsing, Draft
   2020-12 schema checks, exact manifest structure, and bounded structural
   authentication of the implementation manifest.
6. If and only if preflight succeeds, answer every semantic question in the
   v0.4 rereview brief with exact artifact and section/key citations.
7. Return exactly one verdict from the brief and include its required final
   statement. Return the review only in the final response to CONTROL; do not
   create a repository review file.

Do not implement, build, install dependencies, materialize a runtime profile,
create a pipe/job/process/guard/root, execute implementation tests, run a
platform probe, invoke native APIs, rehearse, access an oracle, use network,
provider, model, or prior-chat output, or commit, push, merge, publish, or
integrate.
