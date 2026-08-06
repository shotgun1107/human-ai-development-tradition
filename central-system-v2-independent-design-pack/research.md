# 개인 AI 개발 전통을 위한 분야 횡단 조사

## 1. 조사 질문과 방법

질문은 “한 사람이 AI 개발 경험을 어떻게 신뢰할 수 있는 다음 프로젝트의 규칙으로 바꾸고, 잘못된 규칙을 어떻게 수정·폐기할 것인가?”이다. AI 에이전트에 국한하지 않고 경험 학습을 오랫동안 다뤄 온 분야를 비교했다.

자료 우선순위는 다음과 같다.

1. 공식 교리·규정·기관 지침과 원 저자의 글
2. 동료평가 논문과 학술 출판사의 서지·초록
3. 실무 조직의 공개 운영 지침
4. 보조 설명 자료

아래의 **확인된 사실**은 링크한 자료가 직접 지지하는 내용이다. **설계 추론**은 여러 분야의 원리를 이 저장소에 적용한 제안이며, 출처가 그 구체 설계를 직접 검증한 것은 아니다. 유료·접근 제한 논문은 공개된 서지와 초록 범위에서만 확인했다.

## 2. 분야별 확인된 사실

### 2.1 군사 교리, AAR, lessons learned

미 육군은 AAR을 단순 보고서가 아니라 수행을 되돌아보고 다음 수행을 개선하는 훈련 도구로 다룬다. 2025년 공개된 TC 7-0.1 소개는 AAR의 계획·준비·진행·후속조치를 다루고, 후속조치로 즉시 재훈련, SOP 개정, 교훈의 통합·공유를 든다. 즉 회고 회의가 끝이 아니라 수행 체계의 변경이 끝점이다([U.S. Army, TC 7-0.1 소개](https://www.army.mil/article/283214/tmd_publishes_training_circular_to_augment_fm_and_adp_7_0)). 미 육군 CALL은 전 구성원이 관찰의 발견자이자 사용자라는 지식 공유 문화를 목표로 밝힌다([U.S. Army Combined Arms Center, Lessons Learned](https://usacac.army.mil/Home/Lessons-Learned)).

NATO는 더 명확한 상태 구분을 제공한다. 2022년 4판 핸드북에서 lessons learned 과정은 `Plan → Observe → Analyse → Decide → Implement & Validate → Share`로 구성된다. 관찰은 개선할 문제 또는 잠재 best practice의 짧은 설명이고, remedial action은 lesson identified를 lesson learned로 바꾸기 위한 조치다. 필요한 경우 검증은 최초 문제가 성공적으로 해결됐는지 확인해야 한다. 또한 능력은 도구만이 아니라 leadership, mindset, structure, process, tools, training, information sharing으로 구성된다([NATO JALLC, Lessons Learned Handbook 4th ed.](https://nllp.jallc.nato.int/iks/sharing%20public/jallc_ll_handbook_update_-_4th_edition_final_14072022.pdf)).

확인된 함의:

- 관찰 또는 좋은 아이디어는 아직 “학습된 교훈”이 아니다.
- 조치가 구현되고 효과가 검증돼야 교훈이 제도화됐다고 할 수 있다.
- 성공 사례와 잠재 best practice도 수집 대상이다.
- 리더십·역할·공유·후속조치 없는 데이터베이스만으로는 학습 능력이 생기지 않는다.

### 2.2 SRE와 무과실 포스트모템

Google SRE는 포스트모템을 incident, 영향, 완화·해결 조치, 원인, 재발 방지 후속조치의 기록으로 정의한다. 무과실은 책임 회피가 아니라 당시 정보와 의도를 기준으로 개인 비난 대신 기여 요인과 시스템 개선에 집중하는 것이다. 사전에 postmortem trigger를 정하고, 투명하게 공유하며, 후속조치에 공식 소유권과 우선순위를 주어야 한다([Google SRE Book, Postmortem Culture](https://sre.google/sre-book/postmortem-culture/), [Google SRE incident management guide](https://sre.google/resources/practices-and-processes/incident-management-guide/)).

확인된 함의:

- 모든 사건을 같은 무게로 조사하면 비용이 과도하므로 사전 trigger와 비례성이 필요하다.
- “누가 실수했나”보다 어떤 조건·도구·절차·훈련이 그 선택을 합리적으로 보이게 했는지 묻는다.
- action item은 소유자·기한·완료 기준 없이 존재하면 학습으로 이어지지 않는다.
- 다수의 구조화 포스트모템을 모으면 반복 패턴과 투자 영역을 찾을 수 있다.

### 2.3 ADR과 결정 기억

Michael Nygard의 원 글은 ADR을 힘과 맥락에 대한 단일 결정을 기록하는 짧은 텍스트로 제안한다. 작은 모듈식 기록을 코드와 함께 버전 관리하면 결정의 동기와 장기 의도를 보존하기 쉽다는 것이 핵심이다([Michael Nygard, Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)).

확인된 함의:

- 결과만 보존하면 미래의 사람이 과거 제약과 대안을 잃는다.
- 한 레코드에 여러 결정을 섞지 않고, 상태와 대체 관계를 버전으로 남기는 편이 추적에 유리하다.
- 결정 기록은 “정답의 영구 보증”이 아니라 당시 맥락의 보존이다.

### 2.4 조직 기억과 지식 창조

Walsh와 Ungson은 조직 기억을 정보의 획득·보존·검색 과정으로 이론화하고, 기억이 사용될 뿐 아니라 오용·남용될 수 있음을 문제로 삼았다([Walsh & Ungson, 1991, *Organizational Memory*](https://doi.org/10.5465/AMR.1991.4278992)). Nonaka는 개인이 만든 지식이 암묵지와 형식지의 지속적 대화를 통해 조직에서 명료화·증폭된다는 이론을 제시했다([Nonaka, 1994, *A Dynamic Theory of Organizational Knowledge Creation*](https://doi.org/10.1287/orsc.5.1.14)).

Argyris는 single-loop learning을 주어진 목표 안의 오류 수정으로, double-loop learning을 목표·정책 자체를 의심하는 수정으로 구분했다([Argyris, 1977, *Double Loop Learning in Organizations*](https://hbr.org/1977/09/double-loop-learning-in-organizations)).

확인된 함의:

- 저장뿐 아니라 획득 품질, 검색 가능성, 적용 시점, 망각·폐기까지 설계해야 한다.
- 경험담을 명시적 규칙으로 바꾸는 과정에서 맥락 손실이 생기므로 출처와 적용 조건을 함께 보존해야 한다.
- 월간 회고는 “현재 규칙을 더 잘 지켰나”뿐 아니라 “그 규칙과 목표가 아직 옳은가”도 물어야 한다.

### 2.5 항공 안전과 자발적 보고

NASA ASRS는 자발적·기밀·비처벌적 보고와 비식별화를 통해 최전선의 근접 실패와 위험 정보를 모은다. 이름·조직명 등 식별 정보를 제거하고 시간·장소도 필요에 따라 일반화한다. 동시에 ASRS는 보고 내용을 검증하지 않으며, 따라서 데이터베이스의 서술 자체를 확인된 사실로 취급할 수 없다고 명시한다([NASA ASRS confidentiality](https://asrs.arc.nasa.gov/overview/confidentiality.html), [ASRS database caveat](https://asrs.arc.nasa.gov/search/database.html)). 고의·범죄 등 보호 제외 범위도 명확히 둔다([NASA ASRS caveats](https://asrs.arc.nasa.gov/overview/caveats.html)).

확인된 함의:

- 솔직한 수집을 위해 비난 억제와 비밀 제거가 필요하다.
- 신고 원문은 중요한 신호지만 검증된 사실과 동일하지 않다.
- 무과실은 고의적 위반이나 별도 보안·법적 절차까지 면제한다는 뜻이 아니다.

### 2.6 의료 안전과 incident learning

WHO는 incident 보고 데이터가 위해의 성격을 이해하는 데 유용하지만 데이터의 속성을 검토하고 결론을 조심스럽게 내려야 한다고 경고한다. 보고 시스템에서 지속적 위험 감소로 이어지는 “진정한 학습”은 여전히 어려운 과제다([WHO, Patient safety incident reporting and learning systems, 2020](https://www.who.int/publications/i/item/9789240010338)). NHS PSIRF는 incident response를 학습과 개선을 위한 시스템으로 두고, 법적 책임·비난·직무 적합성 판단 등과 학습 대응을 분리한다. 고의적 위해·방치는 별도 절차 대상으로 둔다([NHS England, PSIRF](https://www.england.nhs.uk/patient-safety/patient-safety-insight/incident-response-framework/), [PSIRF response standards](https://www.england.nhs.uk/long-read/patient-safety-incident-response-standards/)).

확인된 함의:

- 보고 건수는 실제 발생률의 직접 추정치가 아니다. 보고 성향·탐지 도구·관심 변화의 영향을 받는다.
- 개별 사건의 “root cause 하나”보다 시스템의 다수 기여 요인을 보는 편이 안전하다.
- 조사 독립성과 이해관계자 참여, 대응의 비례성이 필요하다.

### 2.7 case-based reasoning

Aamodt와 Plaza가 정리한 case-based reasoning의 일반 틀은 과거 사례를 검색하고(retrieve), 재사용·수정하며(reuse), 새 상황에서 시험·교정하고(revise), 검증된 경험을 다시 보존하는(retain) 순환이다([Aamodt & Plaza, 1994](https://doi.org/10.3233/AIC-1994-7104)). 이는 일반 규칙만 저장하는 대신, 어떤 맥락에서 어떤 해결이 어떤 결과를 냈는지를 함께 검색한다.

확인된 함의:

- 전통 시스템은 교리뿐 아니라 대표 사례와 반례를 함께 검색해야 한다.
- “비슷함”을 제목이나 키워드 하나로 판단하지 않고 작업 유형, 위험, 도구 버전, 제약, 검증 방식 등 차원을 사용해야 한다.
- 과거 해결을 그대로 복사하지 말고 현재 맥락에서 다시 검증해야 한다.

### 2.8 품질관리, CAPA, PDSA, 표준화

FDA의 전통적 CAPA 요구는 부적합 원인 조사, 필요한 조치 식별, 조치가 효과적이고 부작용을 만들지 않는지 검증·검증(validation/verification), 관련 정보의 관리 검토를 요구한다([21 CFR 820.100](https://www.law.cornell.edu/cfr/text/21/820.100)). IHI의 PDSA 설명은 작은 변경을 계획하고, 시험하고, 결과를 관찰하고, 배운 바에 따라 다음 행동을 정해 로컬 환경에서 효과를 학습하는 순환을 강조한다([IHI, Testing Changes](https://www.ihi.org/library/model-for-improvement/testing-changes)).

확인된 함의:

- 해결책을 배포한 것과 효과가 있는 것은 다른 상태다.
- 작은 가역 실험과 사전 측정 계획이 잘못된 규칙의 고착 비용을 줄인다.
- 의도한 지표 개선뿐 아니라 회귀·부작용도 확인해야 한다.

### 2.9 체크리스트의 효과와 한계

WHO 수술 체크리스트의 초기 8개 병원 전후 연구에서는 사망률이 1.5%에서 0.8%, 입원 합병증이 11.0%에서 7.0%로 감소했다([Haynes et al., 2009](https://doi.org/10.1056/NEJMsa0810119)). 그러나 캐나다 온타리오 101개 병원의 광범위한 도입 연구에서는 사망률과 합병증의 유의한 감소가 관찰되지 않았다([Urbach et al., 2014](https://doi.org/10.1056/NEJMsa1308261)). 연구 설계와 시행 충실도 차이 때문에 두 결과를 단순 직접 비교할 수는 없지만, 문서 도입만으로 효과를 보장할 수 없다는 경고로는 충분하다.

확인된 함의:

- 체크리스트가 있다는 지표보다 실제 사용, 맥락 적합성, 준수 품질, 결과 지표를 측정해야 한다.
- 초기 성공 한 건을 범용 교리로 곧바로 승격하지 않는다.
- 반례를 실패한 기록이 아니라 교리의 적용 경계를 찾는 자료로 취급한다.

### 2.10 검색 가능한 외부 기억과 AI 위험관리

RAG 연구는 모델 파라미터 안의 기억과 검색 가능한 비파라미터 기억을 분리하고, 외부 문서 검색을 생성에 결합했다. 원 논문 자체도 세계 지식 갱신과 출처 제시가 파라미터 기반 모델의 열린 문제임을 지적한다([Lewis et al., 2020, NeurIPS](https://papers.nips.cc/paper_files/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)). NIST AI RMF는 AI 위험을 설계·개발·사용·평가의 생애주기 전반에서 관리하는 자발적 프레임워크다([NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)).

확인된 함의:

- “매월 AI가 학습한다”는 말은 초기에는 모델 가중치 변경이 아니라 승인된 지식 기반 갱신, 검색 인덱스 갱신, 프롬프트 주입, 평가 세트 갱신을 뜻해야 한다.
- 외부 기억은 판본·출처·폐기가 보이고 되돌릴 수 있어 개인 시스템의 초기 선택으로 적합하다.
- 검색됐다는 이유로 규칙이 참이 되는 것은 아니므로, 검색 품질과 답변의 출처 일치성을 별도로 평가해야 한다.

## 3. 분야 횡단 합성: 확인된 공통 패턴

| 공통 패턴 | 군사 | SRE·안전 | 지식·품질 | 이 설계의 의미 |
|---|---|---|---|---|
| 사건과 학습의 분리 | Observation ≠ Lesson Learned | incident ≠ preventive action | case ≠ validated rule | 단계별 상태를 강제한다 |
| 행동과 검증 | Implement & Validate | action owner·backlog | CAPA effectiveness, PDSA | 적용 결과 없이는 승격하지 않는다 |
| 맥락 보존 | 임무·관찰·분석 | timeline·impact·contributing factors | ADR context, CBR case | 적용 조건과 버전을 기록한다 |
| 심리적 안전 | 참여자 self-discovery | blameless | confidential reporting | 비난과 학습 분석을 분리한다 |
| 제도화 | doctrine·SOP·training | runbook·test·monitor | checklist·standard | 산출물에 반영돼야 효력이 있다 |
| 망각과 반례 | reject/note 경로 | trigger·trend review | memory misuse, revise | 강등·폐기·대체를 정상 상태로 둔다 |

## 4. 이 저장소에 대한 설계 추론

다음은 문헌에서 직접 검증된 사실이 아니라 이 프로젝트에 대한 제안이다.

1. incident 하네스는 사건 원본으로 유지하고, 그 위에 `experience`, `lesson`, `doctrine`, `application`, `evaluation`, `review`의 별도 논리 객체를 둔다.
2. 하나의 incident가 하나의 교훈이 된다고 가정하지 않는다. 여러 사건·성공·실험이 한 교훈을 지지할 수 있고, 한 사건이 여러 후보를 낳을 수 있다.
3. 프로젝트 교리는 한 프로젝트의 맥락에서 먼저 시험한다. 범용 교리는 독립된 두 프로젝트 이상 또는 의도적으로 다른 두 조건에서 반복되고 반례 검토를 통과해야 한다.
4. 체크리스트·프롬프트·테스트·템플릿을 교리의 “실행 가능한 표현”으로 관리하고, 어떤 교리 판본에서 파생됐는지 연결한다.
5. AI는 월간 후보 군집화·중복 탐지·반례 검색·초안 작성을 담당할 수 있다. 승인, 증거 등급 상향, 교리 효력 발생, 비밀 공개 여부는 사람이 결정한다.
6. 검색 기본값은 `active`이고 현재 프로젝트 조건과 맞는 교리만 포함한다. `deprecated`, `retired`, `rejected`는 역사·반례 질의 때만 검색한다.

## 5. 근거가 특히 약하거나 미확인인 부분

- 한 사람 규모의 AI 개발 “전통” 시스템에 최적인 월간 빈도나 증거 임계값을 직접 검증한 연구는 확인하지 못했다. 월간 주기와 승격 횟수는 운영 가설이다.
- 제안한 증거 등급과 범용 승격의 “독립 두 맥락” 기준은 안전한 시작점이지 과학적으로 확정된 절대값이 아니다.
- 원천 오케스트레이터의 초기 개발·테스트 incident만으로 반복 패턴이나 전통 효과를 통계적으로 추정할 수 없다.
- B0/B1 반복 비교가 끝나지 않았으므로 B1의 비용·시간·품질 우위는 미확인이다.
- RAG를 실제 구현하거나 검색 품질을 측정하지 않았다. 초기 단계에서는 파일명·태그·명시적 링크 기반 검색부터 검증해야 한다.

## 6. 핵심 참고문헌

- NATO JALLC. *NATO Lessons Learned Handbook*, 4th ed., 2022.
- U.S. Army Training Management Directorate. *TC 7-0.1, After Action Reviews* 소개, 2025.
- Lunney, J., & Lueder, S. *Postmortem Culture: Learning from Failure*. Google SRE Book.
- Nygard, M. *Documenting Architecture Decisions*, 2011.
- Walsh, J. P., & Ungson, G. R. “Organizational Memory.” *Academy of Management Review* 16(1), 1991. DOI: 10.5465/AMR.1991.4278992.
- Nonaka, I. “A Dynamic Theory of Organizational Knowledge Creation.” *Organization Science* 5(1), 1994. DOI: 10.1287/orsc.5.1.14.
- Argyris, C. “Double Loop Learning in Organizations.” *Harvard Business Review*, 1977.
- Aamodt, A., & Plaza, E. “Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches.” *AI Communications* 7(1), 1994. DOI: 10.3233/AIC-1994-7104.
- WHO. *Patient Safety Incident Reporting and Learning Systems*, 2020.
- Haynes, A. B., et al. “A Surgical Safety Checklist to Reduce Morbidity and Mortality in a Global Population.” *NEJM* 360, 2009. DOI: 10.1056/NEJMsa0810119.
- Urbach, D. R., et al. “Introduction of Surgical Safety Checklists in Ontario, Canada.” *NEJM* 370, 2014. DOI: 10.1056/NEJMsa1308261.
- Lewis, P., et al. “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.” *NeurIPS 2020*.
