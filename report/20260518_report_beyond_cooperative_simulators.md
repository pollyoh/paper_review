# Beyond Cooperative Simulators: 협조적 사용자 시뮬레이터를 넘어선 현실적 페르소나 생성 — 종합 분석 보고서

> **원논문**: *Beyond Cooperative Simulators: Generating Realistic User Personas for Robust Evaluation of LLM Agents* `<br>`
> **저자**: Harshita Chopra, Kshitish Ghate, Aylin Caliskan, Tadayoshi Kohno, Chirag Shah, Natasha Jaques `<br>`
> **소속**: University of Washington (Seattle), Georgetown University (Washington, DC)`<br>`
> **출처**: arXiv:2605.12894v1 [cs.CL] (2026), Github: https://github.com/harshita-chopra/persona-policies  `<br>`
> **보고서 작성일**: 2026-05-18

---

## 목차

1. [배경 및 문제 정의](#1-배경-및-문제-정의)
2. [선행 연구 및 기술적 계보](#2-선행-연구-및-기술적-계보)
3. [문제 정식화와 전체 아키텍처](#3-문제-정식화와-전체-아키텍처)
4. [핵심 방법론 (수식·알고리즘 수준)](#4-핵심-방법론-수식알고리즘-수준)
5. [실험 설정 및 결과](#5-실험-설정-및-결과)
6. [관련 스토리, 실제 영향, 학계 반응](#6-관련-스토리-실제-영향-학계-반응)
7. [한계·결론 및 참고문헌](#7-한계결론-및-참고문헌)

---

## 1. 배경 및 문제 정의

> **TL;DR**: LLM 에이전트 벤치마크는 “협조적·균질한” 사용자 시뮬레이터에 의존해 성능이 과대평가된다. 본 논문은 **Persona Policies(PPol)** 로 시뮬레이터 프롬프트에 붙는 **역할극 정책**을 진화적 프로그램 탐색으로 자동 발견하고, 인간 유사도와 행동 다양성을 동시에 최적화해 Sim2Real 격차를 줄인다. τ²-bench에서 fitness 33–62%p 개선, 블라인드 평가에서 인간 판정률 80.4%, PPol 기반 SFT로 OOD 견고성 +17%를 보고한다.

### 1.1 왜 “협조적 시뮬레이터”가 문제인가

대화형 LLM 에이전트는 고객 지원·예약·기술 지원처럼 **다턴·목표 지향** 환경에서 평가된다. 실제 사용자는 정보를 한꺼번에 주지 않고, 모호하게 말하며, 에이전트의 가정에 반박하고, 인내심과 협조 수준이 제각각이다. 그러나 현재 널리 쓰이는 **LLM 사용자 시뮬레이터**는 기저 모델의 기본 성향을 그대로 반영해 **지나치게 협조적(cooperative)**, 일관되며, 요청 정보를 즉시 제공하는 경향이 강하다.

| 현상          | 협조적 시뮬레이터                 | 실제 사용자                      |
| ------------- | --------------------------------- | -------------------------------- |
| 정보 공개     | 필요한 식별자·사실을 빠르게 제공 | 단계적·선택적 공개, 재질문 필요 |
| 상호작용      | 정중·명확·에이전트 지시 수용    | 반박, 불확실성, 감정·조급함     |
| 다양성        | 프로필을 바꿔도 언어 패턴이 유사  | 동일 과제라도 궤적이 크게 다름   |
| 벤치마크 함의 | 에이전트 성공률**과대평가** | 배포 후 실패·불만 증가          |

> **[주석] Sim2Real 격차(Simulation-to-Reality gap)란?**
>
> 로봇·자율주행에서 “시뮬레이터에서 잘 되면 현실에서도 잘 될 것”이라 기대하지만, 현실의 마찰·노이즈·분포 차이로 성능이 떨어지는 현상을 Sim2Real gap이라 한다. Zhou et al. (2026)은 **에이전트 과제**에서도 동일한 격차가 존재함을 τ-bench/τ²-bench 인간 대화 451명 규모로 정량화했다. LLM 시뮬레이터는 “쉬운 모드(easy mode)”를 만들어 에이전트가 인간 대비 과도하게 높은 점수를 받는다. PPol은 이 격차를 **사용자 측 분포**를 인간 궤적에 맞추는 방향으로 줄이려 한다.

### 1.2 연구 목표와 기여

논문은 **과제(goal)·사실·보상은 고정**한 채, 사용자 시뮬레이터 시스템 프롬프트에 덧붙이는 **Persona Policy** $P_\pi$만 제어한다. 핵심 기여는 다음 세 가지다.

1. **PPol**: 기존 벤치마크 시뮬레이터 위에 얹는 plug-and-play 제어층.
2. **진화적 프로그램 탐색**: 수동 페르소나 설계 대신, Python 페르소나 생성기 $G$를 OpenEvolve로 변이·선택.
3. **엔드투엔드 검증**: 행동 지문(behavioral fingerprint) 기반 지표, 블라인드 인간 평가, PPol 증강 SFT로 견고성까지 연결.

### 1.3 평가 환경: τ²-bench

실험은 **τ²-bench**(Barres et al., 2025)의 **retail·airline** 도메인에서 수행된다. τ²-bench는 에이전트와 사용자가 **공유 환경의 도구**를 모두 사용할 수 있는 **이중 제어(dual-control)** 벤치마크로, 단순히 “사용자가 텍스트로 정보만 넘겨주는” 설정보다 현실에 가깝다. PPol은 τ²-bench의 기본 사용자 시뮬레이터에 정책 문자열을 **연결(concatenate)** 하는 방식으로 동작한다.

> **[주석] τ²-bench와 τ-bench의 차이**
>
> **τ-bench**: 정책 제약이 있는 고객 서비스 대화, 에이전트 중심 도구 사용. **τ²-bench**: 사용자도 환경 도구를 쓰는 Dec-POMDP 형태로 확장되어, **조율(coordination)** 과 **의사소통** 오류를 분리 분석할 수 있다. Sierra Research가 [tau2-bench](https://github.com/sierra-research/tau2-bench)로 공개했으며, 에이전트 리더보드에서 상위 모델도 dual-control 전환 시 성능이 크게 하락한다는 점이 산업·학계에서 “도구만 잘 쓰는 에이전트”의 한계로 인용된다.

---

## 2. 선행 연구 및 기술적 계보

### 2.1 기술 발전 타임라인

```mermaid
timeline
    title 사용자 시뮬레이션·에이전트 평가 계보
    2018 : PersonaChat — 고정 프로필 기반 대화 개인화
    2024 : MINT / τ-bench — 다턴·도구·정책 제약 벤치마크
    2025 : τ²-bench / SimulatorArena — dual-control·시뮬레이터 신뢰성 논쟁
    2025 : He et al. τ-trait — 비협조 프롬프트 스트레스 테스트
    2026 : Zhou Sim2Real — 19차원 행동 지문·USI 지표
    2026 : PPol (본 논문) — 진화적 생성기 + coverage·MAP-Elites
```

### 2.2 선행 연구 비교

아래 표는 PPol 논문이 직접 인용·대비하는 선행 연구를 **원문 메타데이터·기여·PPol과의 관계**까지 포함해 정리한 것이다. 벤치마크·평가 축(표 A)과 페르소나·사용자 시뮬레이션 축(표 B)으로 나눈다.

#### 표 A. 벤치마크·시뮬레이터 평가·Sim2Real

| 원논문 제목                                                                                               | 저자 (연도)                                                                                                                               | 학회·저널                                                                                          | arXiv                                       | 핵심 아이디어                                                                                     | 주요 기여                                                                                                                                 | PPol과의 관계                                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| *τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment*                            | Victor Barres, Hao Dong, Shreyas Ray, Xiaoqi Si, Karthik Narasimhan (2025)                                                                | arXiv preprint (Sierra Research; 벤치마크 공개)                                                     | [2506.07982](https://arxiv.org/abs/2506.07982) | 에이전트뿐 아니라**사용자도 공유 환경의 도구**를 쓰는 이중 제어(Dec-POMDP) 대화 평가        | Telecom dual-control 도메인, 합성 과제 생성기, 환경 결합 사용자 시뮬레이터, 추론 vs 조율 오류 분리                                        | PPol의**실험 플랫폼·롤아웃 스택**; 기본 τ² 사용자 시뮬레이터가 PPol이 교정하는 **협조적 baseline**                                                                                                                 |
| *SimulatorArena: Are User Simulators Reliable Proxies for Multi-Turn Evaluation of AI Assistants?*      | Yiran Dou, Mike Galley, Baolin Peng, Chris Kedzie, Wenqi Cai, Alan Ritter, Chris Quirk, Wenhan Xue, Jianfeng Gao (2025)                   | **EMNLP 2025** (Main)                                                                         | [2510.05444](https://arxiv.org/abs/2510.05444) | 다턴 AI 어시스턴트 평가에서**사용자 시뮬레이터가 인간 대리인이 될 수 있는지** 체계 검증     | 909개 인간–LLM 대화, 18개 어시스턴트 벤치마크;**프로필 조건부** 시뮬레이터가 인간 판단과 Spearman ρ≈0.7 정렬                     | PPol의**문제 제기(시뮬레이터 가정)** 와 정합; Dou는 “조건부로는 신뢰 가능”을 보이고, PPol은 “**τ² 기본 사용자는 여전히 비현실적으로 협조적**”임을 지문·블라인드 실험으로 보완                                  |
| *Mind the Sim2Real Gap in User Simulation for Agentic Tasks*                                            | Xuhui Zhou, Wen Sun, Qian Ma, Yufei Xie, Jing Liu, Wenhao Du, Sean Welleck, Yiming Yang, Graham Neubig, Shang-Ting Wu, Maarten Sap (2026) | arXiv preprint (CMU 등)                                                                             | [2603.11245](https://arxiv.org/abs/2603.11245) | 에이전트 과제에서 LLM 사용자 시뮬레이터와**실제 인간(451명)** 간 Sim2Real gap 정량화        | 31개 시뮬레이터, τ-bench 프로토콜;**4차원·19특징 행동 지문**, User-Sim Index(USI); “easy mode”·과도한 협조·균일한 피드백 입증 | PPol의**지문 정의·판별기·Dice($D_1$–$D_4$)·인간 말뭉치 $\mathcal{H}$** 의 직접적 선행; PPol은 동일 지표 체계 위에서 **생성기를 진화해 gap을 줄이는 방법**을 제안                                            |
| *Lost in Simulation: LLM-Simulated Users are Unreliable Proxies for Human Users in Agentic Evaluations* | Preethi Seshadri, Samuel Cahyawijaya, Ayobami Odumakinde, Shivalika Singh, Sarah Goldfarb-Tarrant (2026)                                  | **ICLR 2026** workshop (Algorithmic Fairness Across Alignment Procedures and Agentic Systems) | [2601.17087](https://arxiv.org/abs/2601.17087) | 시뮬레이터 기반 에이전트 평가가**인간을 대체하지 못함**을 다인종·다방언 사용자 연구로 입증 | 사용자 LLM 교체 시 성공률 최대 9%p 변동; AAVE·인도 영어 등에서**체계적 과소/과대평가**; 시뮬레이터의 과한 질문·정중함             | PPol의**반론·한계 맥락**: 지문 정렬만으로 “인간 proxy”가 완전해지지 않음을 상기; PPol은 τ²·소수 도메인 인간 데이터에 **특화 교정**이며, Seshadri가 강조한 **인구·언어 대표성**은 PPol이 다루지 않은 공백 |
| *MINT: Evaluating LLMs in Multi-Turn Interaction with Tools and Language Feedback*                      | Xingyao Wang, Zihan Wang, Jiateng Liu, Yangyi Chen, Lifan Yuan, Hao Peng, Heng Ji (2024)                                                  | **ICLR 2024**                                                                                 | [2309.10691](https://arxiv.org/abs/2309.10691) | 도구 사용과**자연어 피드백**이 있는 다턴 상호작용에서 LLM 평가                              | 반복적 도구 호출·피드백 루프 벤치마크; 정적 프롬프트 평가의 한계 지적                                                                    | PPol이 속한**“에이전트 = 다턴·도구·환경”** 평가 패러다임의 초기 축; MINT는 사용자 시뮬 다양성보다**에이전트 도구 능력**에 초점—PPol은 같은 패러다임에서 **사용자 측 분포**를 문제 삼음                           |

#### 표 B. 페르소나·사용자 시뮬레이션·비협조 행동

| 원논문 제목                                                                                         | 저자 (연도)                                                                                                                                  | 학회·저널                             | arXiv                                       | 핵심 아이디어                                                                         | 주요 기여                                                                           | PPol과의 관계                                                                                                                                                                                                                                        |
| --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| *Personalizing Dialogue Agents: I have a dog, do you have pets too?*                              | Saizheng Zhang, Emily Dinan, Jack Urbanek, Arthur Szlam, Douwe Kiela, Jason Weston (2018)                                                    | **ACL 2018** (Long Papers)       | [1801.07243](https://arxiv.org/abs/1801.07243) | 대화 에이전트에**지속적 페르소나(프로필 문장)** 를 조건으로 개인화              | PersonaChat 데이터셋(16만+ 발화); 프로필 조건 시**더 구체·일관된** 잡담      | PPol의**페르소나 조건화 선행**; Zhang은 정적 프로필·잡담이고, PPol은 **과제 목표 고정 + 턴 단위 역할극 지침**·행동 축 $D$로 “어떻게 말할지”를 제어                                                                                 |
| *Scaling Synthetic Data Creation with 1,000,000,000 Personas*                                     | Tao Ge, Xin Chan, Xiao Wang, Dian Yu, Haitao Mi, Dong Yu (2024)                                                                              | arXiv preprint (Microsoft 등)          | [2406.20094](https://arxiv.org/abs/2406.20094) | **10억 규모** 합성 페르소나로 데이터·응답 다양화                               | 대규모 페르소나 샘플링 파이프라인; 정적 선호·일반 시나리오 합성                    | PPol과**스케일 vs 충실도** 대비: Ge는 프로필 **다양성·데이터량**, PPol은 **τ² 다턴·도구 롤아웃**에서 인간 지문에 맞는 **상호작용 행동**을 진화 탐색                                                                      |
| *Persona Generators: Generating Diverse Synthetic Personas at Scale*                              | Daniele Paglieri, Luke Cross, William A. Cunningham, Joel Z. Leibo, Alexander Sasha Vezhnevets (2026)                                        | arXiv preprint                         | [2602.03545](https://arxiv.org/abs/2602.03545) | **페르소나 생성기를 진화**시켜 인구 커버리지 극대화                             | 자동 persona generator evolution; 정적 선호·일반 시나리오에서**다양성** 강조 | PPol과**가장 가까운 방법론적 사촌**: 둘 다 “생성기 진화”이나, Paglieri는 **정적 응답·커버리지**, PPol은 **에이전트–사용자 롤아웃·인간-likeness·Chamfer coverage·MAP-Elites**로 **과제 보존 다턴 평가**에 특화         |
| *Know You First and Be You Better: Modeling Human-Like User Simulators via Implicit Profiles*     | Kevin Wang, Xinyue Li, Shuo Yang, Li Zhou, Fei Jiang, Hongli Li (2025)                                                                       | **ACL 2025** (Long Papers)       | [2502.18968](https://arxiv.org/abs/2502.18968) | 인간–기계 대화에서**암묵적 사용자 프로필**을 추론해 시뮬레이터 학습            | USP 프레임워크, LMSYS-USP 데이터, SFT+RL cycle consistency                          | PPol과**상보**: Wang은 **프로필 추론·모델 파인튜닝**으로 시뮬레이터 자체를 바꾸고, PPol은 **기존 τ² 시뮬레이터에 프롬프트 부록(Persona Policy)** 만 추가하는 plug-and-play; USP 프로필 + PPol 역할극 **결합** 가능        |
| *Impulsive Users Confuse AI Agents: High-Fidelity Simulations of Human Traits for Testing Agents* | Michael He, Anik Kumar, Tyler Mackey, Meghana Rajeev, J. Zico Kolter, Nazneen Rajani (2025)                                                  | arXiv preprint                         | [2510.04491](https://arxiv.org/abs/2510.04491) | **τ-trait** 프롬프트로 조급·회의·혼란 등 인간 특성을 시뮬레이터에 주입       | 비협조 사용자로**헤드라인 성공률 대폭 하락** 입증; 에이전트 스트레스 테스트   | PPol**평가·훈련 연결점**: He는 **수동 trait perturbation**, PPol은 인간 $\mathcal{H}$에 맞춰 trait·축을 **자동 발견**; PPol SFT는 τ-trait 4종(Skeptical, Incoherent, Impatient, Confusion) OOD에서 **+17%** 견고성 입증 |
| *Non-Collaborative User Simulators for Tool Agents*                                               | Jeonghoon Shim, Wonjae Song, Chaehyeon Jin, Seungbeen Kook, Yong Jo (2026)                                                                   | **ICLR 2026**                    | [2509.23124](https://arxiv.org/abs/2509.23124) | 도구 에이전트용**비협조 사용자** 시뮬레이터(불가 요청, 산만, 조급, 불완전 발화) | MultiWOZ·τ-bench에서 SOTA 에이전트**성능 급락**; NCUser 오픈소스 프레임워크 | He와 유사하게**수동 행동 카테고리**; PPol은 **Chamfer coverage**로 “비협조만”이 아니라 **인간 분포 전체**를 덮도록 설계—Shim의 4류는 PPol 진화 축의 **부분집합**이 될 수 있음                                             |
| *Reliable LLM-based User Simulator for Task-oriented Dialogue Systems*                            | Ivan Sekulic, Silvia Terragni, Victor Guimaraes, Nghia Khau, Bruna Guedes, Modestas Filipavicius, Andre Ferreira Manso, Roland Mathis (2024) | **ACL 2024 Workshop** (SCI-CHAT) | [2402.13374](https://arxiv.org/abs/2402.13374) | 과제 지향 대화에서**검증기·파인튜닝**으로 신뢰할 수 있는 LLM 사용자 시뮬레이터 | 실제 대화 기반 미세조정, verifier로 궤적 품질 관리                                  | PPol과**목표 공유(신뢰성)** 이나 수단 상이: Sekulic는 **모델 가중치** 갱신, PPol은 **프롬프트·생성기 코드** 진화—둘 다 “협조적 기본 시뮬레이터” 한계를 넘으려 함                                                               |
| *DuetSim: Building User Simulator with Dual Large Language Models for Task-oriented Dialogues*    | Xixin Luo, Zhihao Tang, Jian Wang, Xixin Zhang (2024)                                                                                        | **LREC-COLING 2024**             | [2405.13028](https://arxiv.org/abs/2405.13028) | **듀얼 LLM**으로 사용자·검증 역할 분리해 과제 지향 시뮬레이션                  | 질문 패턴·일관성 개선; 이중 모델로 환각·비현실 발화 완화                          | PPol은**단일 사용자 LLM + 외부 지문·판별기**로 품질 관리; DuetSim의 “검증 LLM” 역할이 PPol에서는 **19-D fingerprint + RF discriminator + Reflection**으로 대체됨                                                                      |

> **표 읽기 요약**: PPol은 (1) Zhou의 **측정 체계**, (2) Barres의 **τ² 롤아웃 환경**, (3) Paglieri/He/Shim 계열의 **다양·비협조 사용자** 니즈, (4) Dou/Seshadri의 **시뮬레이터 신뢰성 경고**를 한 프레임에 통합한다. 차별점은 **인간 궤적에 대한 2목적 진화(program search)** 와 **과제 보존 Persona Policy**다.

### 2.3 PPol이 왜 “진화적 탐색(OpenEvolve)”을 쓰는가

이 절은 **Figure 1 상단의 Evolutionary Coding Agent**가 실제로 무엇을 하는지, 그리고 §2.2의 Paglieri·He처럼 “페르소나를 다양하게 만든다”는 목표를 PPol이 **어떤 메커니즘**으로 달성하는지 연결하기 위해 둔다. 여기서 말하는 “검색”은 **웹 검색·문헌 검색이 아니다**. 수학 최적화에서 말하는 **search(탐색)**: “더 나은 페르소나 **생성기 프로그램** $G$를 여러 후보 중에서 찾는 과정”이다.

#### 무엇을 최적화하는가

PPol이 바꾸려는 것은 LLM 가중치가 아니라, 디스크에 있는 **Python 파일**(`initial_generator.py` → 진화하며 수정됨)이다. 그 안에는 다음이 함께 들어 있다.

- 행동 축 목록 `DIVERSITY_AXES` ($D$)
- population/roleplay용 **프롬프트 문자열**
- `generate_personas_detailed(c, D, N)` **제어 로직**

즉 **유전자형(genotype) = 생성기 소스 코드 전체**이고, **표현형(phenotype) = 그 코드를 실행했을 때 나오는 $N$개 Persona Policy와 대화 궤적**이다. fitness $\mathcal{M}(G;\mathcal{T})$는 phenotype(롤아웃 결과)을 τ²에서 돌려 측정한다.

아래는 논문 부록 **Listing 1** 전체이다. 

> **[주석] initial_generator.py — PPol 시드 생성기 전문 (논문 Appendix C.1, Listing 1)**
>
> OpenEvolve가 **변이·선택하는 대상**이 되는 Python 파일이다. 아래 코드를 펼치면 논문 부록과 동일한 구조를 볼 수 있다.
>
> | 파일 내 구성                   | 역할                                                     | 진화 시 수정 예                               |
> | ------------------------------ | -------------------------------------------------------- | --------------------------------------------- |
> | `DIVERSITY_AXES`             | 행동 축$D$ (이름·정의·true/false 연기 문구)          | 축 추가·삭제 (`incremental_disclosure` 등) |
> | `POPULATION_*`               | Stage 1:$N$명 archetype + `axis_placement` JSON 생성 | “첫 턴에 식별자 금지” 등 지시 추가          |
> | `ROLEPLAY_*`                 | Stage 2: 150–250단어 `expanded_instruction` 생성      | 턴 단위 말투·감정 규칙 구체화                |
> | `generate_personas_detailed` | $G(c,D,N)$ 공개 진입점                                 | 호출 순서·병렬화·검증 로직                  |
>
> **인자**: `c` = 과제 컨텍스트(기본 페르소나+지시), `axes` = $D$, `n` = $N$. 반환값 각 원소의 `expanded_instruction`이 사용자 시뮬레이터 프롬프트에 **덧붙는** Persona Policy $P_\pi$가 된다.
>
> ```python
> """
> This is evolution/initial_generator.py PROGRAM — Source code of function generate_personas_detailed(c, D, N):
>
>   c — Task context: user scenario (base persona + given instructions).
>   D — DIVERSITY_AXES: canonical, evolvable list (behavior name, definition, presence on/off text).
>   N — Number of personas to generate.
> """
>
> from typing import Any, Dict, List
> from persona_policies.evolution._generator_utils import generate_population, expand_personas_parallel
>
> # List of common behaviors observed in real humans.
> # Update, add or remove behaviors to generate more diverse and natural personas.
>
> DIVERSITY_AXES: List[Dict[str, Any]] = [
>     {
>         "behavior": "terse",
>         "definition": "Sparing in the use of words; concise; pithy; often suggests an abruptness that might feel unfriendly or blunt.",
>         "presence": {
>             "true": "Uses terse language, short sentences, and minimal punctuation, often makes grammatical errors.",
>             "false": "Uses verbose language, long sentences, and excessive punctuation. Unnecessary words, phrases, or emojis.",
>         },
>     },
>     {
>         "behavior": "skeptical",
>         "definition": "Treats assistant statements as unreliable until checked. Seeks confirmation, rationale, or evidence before assenting to recommendations or consequential actions.",
>         "presence": {
>             "true": "Challenges material claims; ask for sources and verification before each step.",
>             "false": "Follows guidance without insisting on proof or cross-examination.",
>         },
>     },
>     {
>         "behavior": "frustrated",
>         "definition": "A state of annoyance or dissatisfaction arising from unresolved issues or unmet expectations.",
>         "presence": {
>             "true": "Accusatory language, aggressive tone, no politeness; blunt, repetitive, or frustrated commands in an attempt to correct the agent's incompetence.",
>             "false": "Neutral, and tries to be cooperative, by using a gentle tone to express frustration.",
>         },
>     },
>     {
>         "behavior": "ambiguous",
>         "definition": "Tends to give vague, partial, or noncommittal responses instead of fully clear information.",
>         "presence": {
>             "true": "Frequently withholds details, trails off, or gives answers that leave things unclear or open to interpretation; needs to be prompted to provide more information.",
>             "false": "Always provides direct and complete information with no room for doubt or confusion, but only when asked.",
>         },
>     },
> ]
>
> # Stage 1: Population generation — jointly generate N persona descriptions with axis placements.
> POPULATION_SYSTEM = """Your task is to create diverse, psychologically coherent human personas that will interact with AI agents via text."""
>
> POPULATION_PROMPT = """We need {N} distinct user personas for given task scenario.
>
> ## Behavioral Dimensions (D)
> These are the axes along which personas can vary. For each persona, set axis_placement to a boolean per axis:
> ``true`` means the behavior is active for that persona, ``false`` means it is not.
>
> {axes_description}
>
> ## Task context c (Base Persona Scenario)
> {task_context}
>
> ## Requirements
> - Generate exactly {N} personas that are plausible humans in this situation.
> - Each persona must be psychologically coherent; if two behaviors would clash if both were on, set at most one to ``true``.
> - Maximize DIVERSITY across the {N} personas. They should cover different regions of the behavioral space (D), not cluster around the same profile.
> - Each persona needs a short "who they are" description (2-3 sentences) grounded in a real person's life situation — describe the PERSON, not the configuration.
>
> Respond with ONLY valid JSON: one array of exactly {N} objects. Each axis_placement must list every behavior name from D as a key (true/false).
> [
>   {{
>     "persona_id": "short_snake_case_name",
>     "description": "2-3 sentence description of who this person is",
>     "axis_placement": {{
>       "<behavior_name>": true,
>       "<behavior_name>": false
>     }},
>     "reasoning": "one sentence on why these placements work together for this person"
>   }}
> ]"""
>
> # Stage 2: Roleplay expansion — expand each member into roleplay instructions for the task.
> ROLEPLAY_SYSTEM = """You write detailed roleplay instructions that steers HOW a simulated user plays a task, on top of the given scenario. The persona must feel like a real human, not a script."""
>
> ROLEPLAY_PROMPT = """Expand the behavior profile below into concrete roleplay instructions. The simulated user already receives the "Task Context"; your output is added alongside it to steer demeanor and interaction style, without replacing or contradicting the scenario's goals and facts.
> Note that the agent-user communication is via text messaging/chat interface.
>
> ## Task Context (Base Persona Scenario)
> {task_context}
>
> ## Behavior profile to superimpose
> Name: {persona_id}
> Description: {description}
> Active behavioral traits:
> {active_traits}
>
> ## Instructions
> Write a detailed roleplay instruction (150-250 words) that tells the user simulator HOW to play this persona in this specific task. The instruction should:
> 1. GROUND the persona in this specific Task Context and behavior profile.
> 2. Specify concrete communication patterns: linguistics, vocabulary, emotional markers, how they respond to agent requests.
> 3. Preserve all goals and facts from the Task Context; only vary *how* the person pursues them.
> 4. Do NOT break the character — no mention of "simulation", "benchmark", or "AI".
>
> Respond with ONLY the roleplay instruction text:"""
>
>
> def generate_personas_detailed(c: str, axes: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
>     """G(c, D, N) — public entrypoint. expanded_instruction of each persona is fed to the user simulator."""
>     population = generate_population(
>         system_prompt=POPULATION_SYSTEM,
>         prompt_template=POPULATION_PROMPT,
>         task_context=c,
>         axes=axes,
>         n=n,
>     )
>     expanded_instructions = expand_personas_parallel(
>         system_prompt=ROLEPLAY_SYSTEM,
>         prompt_template=ROLEPLAY_PROMPT,
>         archetypes=[member for member in population if isinstance(member, dict)],
>         task_context=c,
>         axes=axes,
>     )
>     personas: List[Dict[str, Any]] = []
>     for i, member in enumerate(population):
>         if not isinstance(member, dict):
>             continue
>         expanded_instruction = expanded_instructions[i] if i < len(expanded_instructions) else ""
>         personas.append(
>             {
>                 "persona_id": member.get("persona_id"),
>                 "description": member.get("description"),
>                 "axis_placement": dict(member.get("axis_placement") or {}),
>                 "reasoning": member.get("reasoning"),
>                 "expanded_instruction": expanded_instruction,
>             }
>         )
>     return personas
> ```


> **[주석] AlphaEvolve / OpenEvolve란? (PPol과의 관계만)**
>
> Google DeepMind **AlphaEvolve**는 “수학·시스템 코드를 **자동으로 고치며** 성능을 올리는” 내부 연구 라인이다. **OpenEvolve**([GitHub](https://github.com/algorithmicsuperintelligence/openevolve))는 같은 **진화 루프 + LLM 코드 편집** 아이디어의 오픈소스 구현이다. PPol 논문은 이 위에 **도메인 전용 evaluator**(τ² 롤아웃, 지문, $\mathcal{M}$, Reflection)만 얹어 쓴다.

#### 한 세대(iteration)에서 실제로 일어나는 일 (구체적)

아래는 §3.4 Algorithm 1을 **구현 관점**으로 풀어 쓴 것이다.

```mermaid
sequenceDiagram
    participant OE as OpenEvolve 스케줄러
    participant LLM as Gemini 3 Flash (변이 LLM)
    participant G as Python 생성기 G
    participant Tau as τ²-bench 롤아웃
    participant Ev as Evaluator (지문·M)

    OE->>G: 현재 프로그램 + 아카이브 상위 개체 로드
    G->>Tau: 5 tasks × N personas 롤아웃
    Tau->>Ev: 대화 궤적
    Ev-->>OE: M, P̄(human), B̄_cover, Reflection 텍스트
    OE->>LLM: (1) 소스 코드 (2) fitness 수치 (3) Reflection (4) 변이 지침
    LLM-->>OE: 수정된 initial_generator.py (축 추가·프롬프트 문장 변경 등)
    OE->>OE: MAP-Elites bin에 등록·엘리트 갱신
```

1. **평가**: 현재 $G$를 import해 $\Pi_t = G(c_t,D,N)$ 실행 → 각 $P_\pi$로 사용자 시뮬레이터 프롬프트에 붙임 → 에이전트와 τ² 대화 → $\mathbf{f}(\tau)$ → $\mathcal{M}$.
2. **Reflection**(별도 LLM 호출): human-likeness 최고/최저 궤적 발췌 + 지문을 읽고 “왜 협조적으로 sounded는지” 등 **자연어 비평** 생성 (Figure 2(C) 스타일).
3. **변이**: **변이 LLM**이 `initial_generator.py`를 입력으로 받아, 예를 들어
   - `DIVERSITY_AXES`에 `incremental_disclosure` 축 추가,
   - `POPULATION_PROMPT`에 “첫 턴에 주문번호를 쓰지 말 것” 문장 삽입,
   - population JSON 스키마 검증 로직 수정
     같은 **의미 있는 편집**을 제안한다. (랜덤 비트 변경이 아님.)
4. **선택·다양성**: 수정된 $G'$의 $(\bar{P}, \bar{B}_{\mathrm{cover}})$ 좌표로 MAP-Elites bin을 정하고, bin마다 $\mathcal{M}$ 최고 프로그램만 남긴다.

수동으로 하면: 축 정의·프롬프트·샘플링 규칙을 사람이 trial-and-error해야 하고, §5.1의 **PPol-Initial / DP Personas**처럼 coverage가 잘 안 오른다. **탐색 공간이 “자연어+코드”로 너무 크기 때문**에, 논문은 OpenEvolve로 이 공간을 자동 탐색한다.

#### MAP-Elites를 같이 쓰는 이유

단일 $\mathcal{M}$ 최대화만 하면 “판별기만 속이는” 한 가지 어색한 스타일로 수렴할 수 있다. MAP-Elites([arXiv:1504.04909](https://arxiv.org/abs/1504.04909))는 $(\bar{P}(\mathrm{human}), \bar{B}_{\mathrm{cover}})$ 평면을 격자로 나누고 **각 칸마다 최고 $G$** 를 보관한다. 그래서 “인간 같지만 조급한 타입”과 “인간 같지만 정보를 숨기는 타입”처럼 **서로 다른 고득점 생성기**가 아카이브에 동시에 남는다. 이는 PPol의 coverage 목표 $\bar{B}_{\mathrm{cover}}$와 직접 맞물린다.

---

## 3. 문제 정식화와 전체 아키텍처

### 3.1 기호와 제약

- 과제 $t$: 시나리오 + 사용자 목표 (벤치마크 고정).
- 사용자 컨텍스트 $c_t$: 기본 페르소나, 지시, 사용자에게 알려진 사실.
- 기본 시스템 프롬프트 $s_{\mathrm{base}}(t)$.
- **Persona policy** $P_\pi$: 자연어 부록. 최종 사용자 프롬프트: $s_{\mathrm{base}}(t) \oplus P_\pi$ ($\oplus$는 문자열 연결).
- **행동 축 목록** $D$: 각 축은 이름, 정의, `true`/`false` 시 연기 지침(playbook)을 가진 딕셔너리. **진화 대상**이므로 축 자체가 추가·삭제·수정될 수 있다.
- 페르소나 수 $N$: 커리큘럼으로 $5 \to 8 \to 10$ 증가.

**불변 조건**: 목표, 비공개 사실, 환경 상태, 과제 성공 판정 규칙은 변경하지 않는다. 변하는 것은 **말하는 방식**뿐이다.

### 3.2 PPol 전체 루프

![PPol 진화 루프 개요](../paper/Beyond_Cooperative_simulators/Figure_1.png)

> **Figure 1**: 왼쪽 하단 **Evolvable Program $G$**가 행동 축 $D$·프롬프트·`generate_PersonaPolicies` 코드를 보유한다. 중앙 **Task Rollouts**에서 $N$개 페르소나 정책이 고정 에이전트와 채팅하며 궤적 $\mathcal{T}$를 생성한다. 오른쪽 **Evaluator**가 인간 참조 $\mathcal{H}$와 비교해 $\bar{P}(\mathrm{human})$, $\bar{B}_{\mathrm{cover}}$, fitness $\mathcal{M}$을 계산하고 **Reflection** 텍스트를 만든다. 상단 **Evolutionary Coding Agent**가 OpenEvolve로 $G$를 변이하며 `max_iter`까지 반복한다. 화살표는 “생성 → 롤아웃 → 채점 → 변이” 순환을 나타낸다.

```mermaid
flowchart TB
    subgraph evolve [진화 루프 OpenEvolve]
        G[Evolvable Program G<br/>axes D + prompts + code]
        G --> Gen[Population + Expansion]
        Gen --> Roll[τ² agent-user rollouts]
        Roll --> FP[19-D behavioral fingerprints]
        FP --> Met[HL + Coverage → M]
        Met --> Ref[Reflection LLM]
        Ref --> Mut[Mutate G]
        Mut --> G
    end
    H[(Human reference H)] --> Met
    Arch[MAP-Elites archive] --> Met
```

### 3.3 2단계 페르소나 생성 (Population → Expansion)

```mermaid
sequenceDiagram
    participant G as Generator G
    participant LLM as Frontier LLM
    participant Sim as User Simulator
    participant Ag as Fixed Agent

    G->>LLM: Stage 1 Population (joint N members)
    Note over LLM: JSON: persona_id, description,<br/>axis_placement ∈ {0,1}^|D|
    LLM-->>G: N archetypes
    par Stage 2 Expansion
        G->>LLM: Expand member i with active playbooks
        LLM-->>G: P_π^(i) roleplay instructions
    end
    G->>Sim: s_base(t) ⊕ P_π^(i)
    Sim->>Ag: multi-turn dialogue + tools
    Ag-->>G: trajectory τ^(i)
```

**Stage 1 (Population generation)**: $c_t$와 전체 $D$를 조건으로 **$N$명을 한 번에** 제안해, 이산 행동 공간에서 **조인트 샘플링**으로 다양성을 확보한다.

**Stage 2 (Persona expansion)**: 각 멤버별로 150–250단어 **역할극 지침** $P_{\pi,t}^{(i)}$를 병렬 생성한다. “주문번호를 첫 메시지에 넣지 말 것”, “한 번에 한 필드만 답할 것” 같은 **턴 단위 규칙**이 진화 후반에 두드러진다.

![발견된 행동 축·페르소나·Reflection 예시](../paper/Beyond_Cooperative_simulators/Figure_2.png)

> **Figure 2**: **(A)** 진화로 발견된 행동 축 예(`temperament`, `information_velocity`, `narrative_bias` 등). 각 축은 JSON 형태로 정의·true/false 연기 문구를 가진다. **(B)** 생성된 페르소나(hesitant procrastinator, no-nonsense executive 등). **(C)** Reflection이 지적하는 대표 실패—**과도한 협조(Overly Cooperative Behavior)**, 페르소나 이탈, 부자연스러운 완벽한 데이터 제공. 이 피드백이 다음 코드 변이의 방향을 제시한다.

---

## 4. 핵심 방법론 (수식·알고리즘 수준)

### 4.1 페르소나 생성 함수

과제 $t$에 대해:

$$
\Pi_t = \left\{ P_{\pi,t}^{(i)} \right\}_{i=1}^{N}, \qquad \Pi_t = G(c_t, D, N)
$$

각 $i$에 대해 기록 $r_t^{(i)} = (\mathbf{a}_t^{(i)}, P_{\pi,t}^{(i)})$, $\mathbf{a}_t^{(i)} \in \{0,1\}^{|D|}$는 축 활성화 벡터다.

### 4.2 행동 지문 (19차원)

완료 궤적 $\tau$의 **사용자 턴만**으로 $\mathbf{f}(\tau) \in \mathbb{R}^{19}$를 계산한다. Zhou et al. (2026)의 4차원 taxonomy를 따른다.

| 차원                      | 특징 수 | 대표 특징                                                              |
| ------------------------- | ------- | ---------------------------------------------------------------------- |
| D1 Communication Style    | 8       | words_per_turn, politeness_rate, verbosity_cv, identity_confusion_rate |
| D2 Information Disclosure | 3       | front_loading_ratio, identifiers_per_turn, opening_length              |
| D3 Clarification Behavior | 5       | uncertainty_rate, pushback_rate, clarification_question_rate           |
| D4 Error Reaction         | 3       | emotional_expression_rate, accusatory_rate, strategy_pivot_rate        |

LIWC2015·NRC 감성 어휘와 정규식 패턴(“please”, “that’s not right”, “ugh” 등)을 사용한다. **해석 가능성**과 **인간 데이터 정렬**을 동시에 노린 설계다.

> **[주석] 왜 Random Forest 판별기인가?**

| 고차원 딥 임베딩       | 19차원 regex/LIWC 지문          |
| ---------------------- | ------------------------------- |
| 표현력 높음            | 축별 실패 원인 분석 가능        |
| 인간 정렬 검증 어려움  | Zhou taxonomy·Dice와 직접 연결 |
| adversarial drift 위험 | 해석 가능한 fitness 신호        |

논문은 ROC-AUC 0.94–1.00 수준으로 **기본 τ² 시뮬레이터 vs 인간**을 거의 완벽 분리한다(Appendix E). PPol은 이 판별기를 **고정**한 채 생성기만 진화시켜, “인간처럼 보이는 지문”을 향해 이동한다.

### 4.3 Human-likeness

인간 말뭉치 $\mathcal{H}$와 기본 시뮬레이터 궤적로 Random Forest를 학습한다. 에피소드 $e$의 지문 $\mathbf{f}_e$에 대해 $p_{\mathrm{RF}}(\mathrm{human} \mid \mathbf{f}_e)$를 출력한다.

미니배치 $\mathcal{T}$에서 생성기 $G$의 롤아웃 집합 $\mathcal{B}(G;\mathcal{T})$에 대해:

$$
\bar{P}_{G,\mathcal{T}}(\mathrm{human}) = \frac{1}{|\mathcal{B}(G;\mathcal{T})|} \sum_{e \in \mathcal{B}(G;\mathcal{T})} p_{\mathrm{RF}}(\mathrm{human} \mid \mathbf{f}_e)
$$

### 4.4 Behavioral coverage (양방향 Chamfer)

과제 $t$에서 $N$개 페르소나 지문 집합 $\mathcal{F}_t(G)$, 인간 학습 분할 $\mathcal{H}_{\mathrm{train}}$:

$$
\mathrm{err}(\mathcal{F}_t, \mathcal{H}_{\mathrm{train}}) =
\frac{1}{|\mathcal{H}_{\mathrm{train}}|} \sum_{h \in \mathcal{H}_{\mathrm{train}}} \min_{\mathbf{f} \in \mathcal{F}_t} \|h - \mathbf{f}\|_2
+
\frac{1}{|\mathcal{F}_t|} \sum_{\mathbf{f} \in \mathcal{F}_t} \min_{h \in \mathcal{H}_{\mathrm{train}}} \|h - \mathbf{f}\|_2
$$

> **[주석] Chamfer 거리의 직관**

**첫 항**: 모든 “실제 인간” 점 근처에 최소 하나의 시뮬레이터 페르소나가 있어야 한다 → **인간 행동 분포를 덮음(coverage)**. **둘째 항**: 각 페르소나가 인간 지원 집합 근처에 있어야 한다 → **비현실적 이상치 페르소나**를 벌점. $d_{\mathrm{ref}}$는 $\mathcal{H}_{\mathrm{train}}$ 내 평균 쌍별 거리로 스케일 정규화한다.

$$
B_{\mathrm{cover}}(\mathcal{F}_t, \mathcal{H}_{\mathrm{train}}) =
\max\left\{ 0,\, 1 - \min\left(1,\, \frac{\mathrm{err}}{2\, d_{\mathrm{ref}}} \right) \right\}
$$

$$
\bar{B}_{\mathrm{cover}}(G;\mathcal{T}) = \frac{1}{|\mathcal{T}|} \sum_{t \in \mathcal{T}} B_{\mathrm{cover}}(\mathcal{F}_t(G), \mathcal{H}_{\mathrm{train}})
$$

### 4.5 결합 fitness

판별기만 최대화하면 **분포 밖 adversarial 행동**으로 과적합할 수 있다. coverage가 **인간 구름(human cloud) 위**에 머물도록 기하학적 정규화를 한다.

$$
\mathcal{M}(G;\mathcal{T}) = \lambda_h \, \bar{P}_{G,\mathcal{T}}(\mathrm{human}) + \lambda_b \, \bar{B}_{\mathrm{cover}}(G;\mathcal{T}), \qquad \lambda_h + \lambda_b = 1
$$

커리큘럼에 따라 $N$이 커질수록 $\lambda_b$를 키우고 $\lambda_h = 1 - \lambda_b$로 설정한다. 초기에는 소수 $N$으로 **인간 유사도**에 집중, 후반에는 **다양성 압력**을 강화한다.

### 4.6 알고리즘 의사코드

```
Algorithm 1: PPol Evolutionary Search (OpenEvolve + MAP-Elites)
Input: task pool T_train, human corpus H, initial program G_0, max_iter
Output: best generator G*

Initialize archive A with MAP-Elites bins over (P̄(human), B̄_cover)
G ← G_0
for iter = 1 .. max_iter do
    Sample minibatch T ⊂ T_train (|T| = 5)
    Set N, λ_h, λ_b from curriculum
    Reload module G; for each t ∈ T:
        Π_t ← G(c_t, D, N)           // population + expansion
        for each P_π in Π_t:
            τ ← Rollout(agent_fixed, user = s_base(t) ⊕ P_π)
            f ← Fingerprint(τ)       // 19-D
    Compute P̄(human), B̄_cover, M(G; T)
    reflection ← Reflect(best/worst trajectories by p_RF)
    G' ← LLM_Mutate(G, reflection, fitness)   // edit D, prompts, code
    Insert G' into A; keep elite per bin
end for
G* ← argmax validation M averaged over N ∈ {5,8,10}
```

**Reflection-guided mutation**: 상·하위 궤적의 대화 발췌, 19-D 지문, $p_{\mathrm{RF}}$를 Reflection LLM(Gemini 3 Flash)에 넣어 300단어 이내 비평을 생성하고, OpenEvolve 변이 프롬프트에 첨부한다.

### 4.7 베이스라인

| 방법           | 설명                                                                                |
| -------------- | ----------------------------------------------------------------------------------- |
| Base-simulator | τ² 기본 사용자 시뮬레이터, 페르소나 없음                                          |
| DP Personas    | 과제당 1회 LLM 호출로$N$개 지침 생성 (2단계·축 구조 없음)                        |
| PPol-Initial   | 시드 축(terse, skeptical, frustrated, ambiguous) + 2단계 생성기,**진화 없음** |
| PPol-Evolved   | 최대 70 iter, validation$\mathcal{M}$ 최고 체크포인트                             |
| Humans (참조)  | Zhou et al. 인간 대화 지문·지표 (시뮬레이터 아님)                                  |

---

## 5. 실험 설정 및 결과

### 5.1 설정 요약

| 항목                  | 내용                                                       |
| --------------------- | ---------------------------------------------------------- |
| 도메인                | τ²-bench Retail (74 train / 40 test), Airline (30 / 20)  |
| 사용자 시뮬레이터     | DeepSeek-V3.1, Qwen3-Next-80B-A3B-Instruct, GPT-5.4-Mini   |
| 에이전트·환경        | Gemma 4 31B IT; NL 검사·도구 인터페이스 고정              |
| 진화 LLM              | Gemini 3 Flash (생성·reflection·코드 변이)               |
| Fitness 호출당 롤아웃 | $N=5,8,10$ × 5 tasks → 25/40/50 episodes               |
| 테스트                | 모든 페르소나 조건$N=10$ (Retail 최대 400 rollouts/조건) |
| 인간 평가             | Prolific 20명 → QC 후 16명, 87 대화, Retail               |

추가 지표: 차원별 **Sørensen–Dice** 정렬 $D_1$–$D_4$ 및 $\mathrm{USI}_{\mathrm{D1\text{-}D4}}$ (Zhou et al. 방식).

### 5.2 정량 결과 (대표)

**Table 1 요약 — Retail, Qwen3-Next-80B (논문 Table 1)**

| Method                  | HL$\uparrow$  | Coverage$\uparrow$ | Score$\uparrow$ | USI$_{D1\text{-}D4}$ $\uparrow$ |
| ----------------------- | --------------- | -------------------- | ----------------- | ----------------------------------- |
| Humans                  | 0.953           | 0.614                | 0.783             | 87.8%                               |
| Base-simulator          | 0.107           | 0.046                | 0.077             | 35.1%                               |
| DP Personas             | 0.291           | 0.100                | 0.196             | 37.2%                               |
| PPol: Initial           | 0.356           | 0.017                | 0.186             | 39.8%                               |
| **PPol: Evolved** | **0.784** | **0.602**      | **0.693**   | **76.5%**                     |

- Base 대비 Score **+61.6%p** (Retail/Qwen), Airline/GPT-5.4-Mini에서 **+33.1%p** 수준 개선(논문 서술).
- **진화의 역할**: DP·Initial은 Coverage가 거의 개선되지 않음 → MAP-Elites + $\lambda_b$ 커리큘럼이 **인간 분포 위를 덮는** 페르소나 집단을 만든다.
- $D_3$(clarification), $D_4$(error reaction)에서 Base 대비 **2–3배** Dice 개선 사례 다수 (협조적 시뮬레이터가 특히 약한 축).

![진화 중 fitness 및 구성요소](../paper/Beyond_Cooperative_simulators/Figure_3.png)

> **Figure 3**: **왼쪽** Combined Score — Train(검은 점선)은 미니배치마다 요동치지만, Validation $N{=}5,8,10$(빨간 계열)은 약 20 iter 이후 0.5–0.6대로 수렴하며 Baseline Val(~0.12)을 크게 상회한다. $N$이 클수록 validation이 약간 더 높고 안정적이다. **오른쪽** Train $P(\mathrm{human})$/Coverage(점선) vs Avg. Val(실선+음영) — 두 구성요소가 함께 상승하며, 후반에 coverage 가중이 커질수록 Val Coverage가 Human-likeness와 균형을 이룬다.

![PCA 행동 지문 공간](../paper/Beyond_Cooperative_simulators/Figure_4.png)

> **Figure 4**: Retail·DeepSeek-V3.1 기준 PC1(24.1% 분산)·PC2(10.8%) 투영. **초록 삼각형(인간)**은 PC1 음의 영역에 군집, **빨간 원(Base)**은 오른쪽으로 치우쳐 분산이 크다. **파란 원(PPol)**은 인간 군집과 **부분 중첩**하며, centroid(× 표시)가 Human–PPol 사이에서 Base보다 Human에 훨씬 가깝다. “협조적 시뮬레이터 클러스터”에서 “인간 지원 영역”으로의 **분포 이동**을 시각적으로 확인하는 그림이다.

### 5.3 블라인드 인간 평가

![어노테이터 Human/Bot 판정](../paper/Beyond_Cooperative_simulators/Figure_5.png)

> **Figure 5**: Y축은 어노테이터 응답 비율(%). **True human** 80.0% Human / 10.8% Bot, **Persona Policies(PPol)** **80.4%** Human / ~3.9% Bot / 15.7% Not sure, **τ² base-simulator** 46.5% Human / **46.5% Bot**. PPol은 실제 인간과 통계적으로 유사한 “인간처럼 보임” 비율을 달성하고, 기본 시뮬레이터는 동전 던지기 수준으로 Bot으로 분류된다. Welch $t=3.556$, $p=6.37\times10^{-4}$. $p_{\mathrm{RF}}$와 어노테이터 판정의 Point-Biserial $r=0.49$ ($p<0.001$)로 **19-D 지문이 인간 지각의 proxy**임을 뒷받침한다.

### 5.4 에이전트 SFT 견고성 (Section 5.5)

Gemma-4-31B 에이전트를 LoRA(rank 32)로 32 step SFT. **Default-only** vs **Default+PPol** (동일 하이퍼·데이터량).

**Retail — Task Success Rate (Table 2)**

| Training         | In-dist. Default | Skeptical | Incoherent | Impatient | Confusion       | OOD Avg         |
| ---------------- | ---------------- | --------- | ---------- | --------- | --------------- | --------------- |
| No FT            | 0.650            | 0.150     | 0.225      | 0.150     | 0.200           | 0.181           |
| Default-only SFT | 0.675            | 0.150     | 0.225      | 0.200     | 0.275           | 0.213           |
| Default+PPol SFT | **0.750**  | 0.175     | 0.225      | 0.200     | **0.400** | **0.250** |

- In-dist. **+11%p** (0.675→0.750), OOD 평균 **+17% 상대** (0.213→0.250).
- **Confusion** (+0.125)에서 가장 큰 이득 — PPol이 흔히 생성하는 “이전 턴을 다시 의심” 패턴과 정합.
- He et al. (2025) **τ-trait** 스트레스 테스트와 연결: PPol은 **학습 분포 다양화(domain randomization for language agents)** 로 해석 가능(Tobin et al., 2017).

> **[주석] Domain randomization과 PPol SFT**

로봇에서 시뮬레이터의 질감·조명·마찰을 무작위화해 실제 세계로 전이를 돕듯, PPol은 **동일 과제·다양한 말하기 방식**으로 에이전트가 협조적 사용자에 overfit되지 않게 한다. τ-trait은 **평가 시** 인위적 perturbation이고, PPol은 **시뮬레이터 자체**를 인간 분포에 가깝게 만든 뒤 학습 데이터로 쓴다는 점에서 상보적이다.

### 5.5 진화가 발견한 행동 축 (정성)

시드 축 `terse`, `ambiguous` 등에서, 성공한 프로그램은 **`incremental disclosure`**, **`bursty cadence`**, **`cognitive load`** 등 **운영 가능(operational)** 축으로 분화한다. 페르소나는 정적 캐릭터 시트가 아니라 “첫 메시지에 주문번호 금지”, “소문자·줄임말 사용” 같은 **턴 단위 규칙**이 된다. Reflection은 “과도한 협조”, “완벽한 JSON형 답변”을 반복 지적한다.

---

## 6. 관련 스토리, 실제 영향, 학계 반응

### 6.1 산업·벤치마크 현장에서의 맥락

**Sierra Research τ²-bench**는 대화형 에이전트 제품(고객 서비스 자동화) 평가의 **사실상 표준 후보**로 자리 잡고 있다. GitHub [sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench)는 dual-control·합성 과제 생성·검증 가능 보상을 제공하며, 모델 제공자들이 “도구 사용 + 사용자 조율” 능력을 홍보할 때 인용된다. 그러나 **기본 사용자 시뮬레이터가 협조적**이라는 비판은 Zhou et al. (2026), Dou et al. (2025), Seshadri et al. (2026) 등에서 반복되며, **리더보드 순위가 인간 체감 품질과 어긋날 수 있음**이 정책·제품 의사결정에서도 논의된다.

PPol은 이 맥락에서 **벤치마크를 바꾸지 않고 사용자 분포만 교정**하는 실용적 레이어를 제시한다. 코드는 [persona-policies](https://github.com/harshita-chopra/persona-policies)에 공개되어, τ² 롤아웃 파이프라인에 페르소나를 주입하는 **재현 가능 레시피**를 제공한다.

### 6.2 학계 반응: 지지와 비판 (균형)

| 입장                 | 요지                                           | 대표 근거                                                                                               |
| -------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **지지**       | 시뮬레이터를 명시적·가변 요소로 두어야 한다   | SimulatorArena: 프로필 조건부 시뮬레이터는 인간 판단과 상관; PPol은**자동 프로필 발견**으로 확장  |
| **지지**       | Sim2Real gap 정량화 필요                       | Zhou et al.: USI·19특징; PPol이 동일 지표 체계로**개선 입증**                                    |
| **비판·주의** | 시뮬레이터가 여전히 인간 대리인이 될 수 있는가 | Seshadri et al. (2026) “Lost in simulation”: 에이전트 평가에서 LLM 사용자는**unreliable proxy** |
| **비판·주의** | 고능력 LLM ≠ 충실한 사용자                    | Zhou: 일반 capability와 시뮬레이션 충실도**무상관** — PPol도 **별도 최적화** 필요함을 시사 |
| **비판·주의** | 이중 사용·편향                                | Broader Impact: 더 그럴듯한 비협조 사용자는 악용 가능; 본 실험은**양성 CS 과제**로 제한           |

논문은 Dou et al.와 **상충하지 않고 보완**한다. SimulatorArena는 “조건부로는 괜찮다”는 반면, PPol은 “**기본 τ² 사용자는 심각하게 협조적**이므로, 진화로 분포를 인간 쪽으로 끌어와야 한다”는 강한 주장을 fingerprint·인간 실험으로 뒷받침한다.

### 6.3 정책·안전 연구 연결

UW·Georgetown 공동 연구로, 저자 일원은 **Tech Policy Lab**, DARPA/AFRL 지원 문구가 있다. “시뮬레이터 정렬을 에이전트 점수와 **분리 추적**해야 한다”는 결론은, 향후 **에이전트 안전 감사**에서 “어떤 사용자 분포로 테스트했는가”를 메타데이터로 요구하는 논의와 맞닿는다. PPol의 discriminator는 **특정 도메인 인간 말뭉치**에 의존하므로, 공정성·대표성(인구·언어) 문제는 **데이터 거버넌스** 이슈로 남는다.

### 6.4 배포·제품 관점 스토리

- **고객 지원 에이전트**: 실제 고객은 조급·회의·정보 미제공이 흔함. He et al. (2025)는 τ-trait으로 **헤드라인 성공률이 크게 하락**함을 보였고, PPol은 **학습 단계**에서 유사 마찰을 넣어 OOD 성능을 회복한다.
- **벤치마크 공정성**: 모델 A/B 비교 시 **동일 PPol 세트**를 쓰지 않으면, “더 협조적인 시뮬레이터를 고른 모델”이 유리해질 수 있다 — Dou et al.가 경고한 **순위 뒤바뀜** 현상.
- **합성 데이터**: Ge et al. 스타일의 대규모 페르소나와 달리, PPol은 **과제 보존·다턴 도구 상호작용**에 특화 — “에이전트 RL/SFT용 **상호작용 다양성**” 니즈에 직접 대응.

---

## 7. 한계·결론 및 참고문헌

### 7.1 한계

1. **인간 말뭉치 의존**: 판별기·coverage·$d_{\mathrm{ref}}$ 모두 $\mathcal{H}$ 필요 — 신규 도메인에는 **수집 비용**이 따른다.
2. **19차원 regex 지문**: 해석 가능하나, 뉘앙스·문화적 맥락을 놓칠 수 있음. 학습 표현 기반 discriminator는 향후 과제.
3. **도메인·벤치마크**: Retail/Airline·τ²에 한정; Telecom dual-control 등으로의 확장은 미검증.
4. **실사용자 검증**: SFT 견고성은 **시뮬레이터 OOD**까지이며, **실제 Prolific/현장 사용자**와의 최종 A/B는 Future work.
5. **진화 비용**: fitness당 최대 50 τ² 에피소드·iter 70·OpenEvolve timeout 3600s — 산업 적용 시 **비용·재현 시드** 관리 필요.

### 7.2 결론

PPol은 “더 많은 손으로 그린 페르소나”가 아니라, **인간 행동 지문 공간에서의 위치**를 명시적 목적함수로 최적화하는 **프로그램 합성(program synthesis)** 접근이다. 협조적 기본 시뮬레이터는 에이전트 연구의 **숨은 가정(hidden default)** 이었고, PPol은 그 가정을 **측정 가능·진화 가능**하게 만든다. 에이전트가 복잡한 사회적 배포로 나아갈수록, **사용자 시뮬레이터 정렬**은 모델 capability 추적과 분리된 필수 지표가 될 가능성이 크다.

### 7.3 참고문헌 및 관련 자료

| 자료                                                  | URL                                                        |
| ----------------------------------------------------- | ---------------------------------------------------------- |
| 본 논문 (arXiv)                                       | https://arxiv.org/abs/2605.12894                           |
| HTML 전문                                             | https://arxiv.org/html/2605.12894v1                        |
| Persona Policies 코드                                 | https://github.com/harshita-chopra/persona-policies        |
| τ²-bench                                            | https://arxiv.org/abs/2506.07982                           |
| τ²-bench GitHub                                     | https://github.com/sierra-research/tau2-bench              |
| Mind the Sim2Real Gap (Zhou et al., 2026)             | https://arxiv.org/abs/2603.11245                           |
| SimulatorArena (Dou et al., 2025)                     | https://arxiv.org/abs/2510.05444                           |
| Lost in Simulation (Seshadri et al., 2026)            | https://openreview.net/forum?id=m57vJLBHxA                 |
| Impatient users / τ-trait (He et al., 2025)          | https://arxiv.org/abs/2510.04491                           |
| Non-collaborative user simulators (Shim et al., 2026) | https://openreview.net/forum?id=UAUimofy3W                 |
| OpenEvolve                                            | https://github.com/algorithmicsuperintelligence/openevolve |
| MAP-Elites                                            | https://arxiv.org/abs/1504.04909                           |
| Persona generators at scale (Paglieri et al., 2026)   | https://arxiv.org/abs/2602.03545                           |
| Domain randomization (Tobin et al., 2017)             | https://ieeexplore.ieee.org/document/8202133               |
| ACL SimulatorArena                                    | https://aclanthology.org/2025.emnlp-main.1786/             |

---

## 보고서 품질 체크리스트 (자체 점검)

| 항목                                                        | 충족          |
| ----------------------------------------------------------- | ------------- |
| 7개 섹션 포함                                               | 예            |
| 메타정보 `<br>` 줄바꿈                                    | 예            |
| 주석 제목에 내용 요약                                       | 예            |
| 수식·알고리즘 수준 방법론                                  | 예            |
| 표 3개 이상                                                 | 예 (6개 이상) |
| mermaid 2개 이상                                            | 예 (3개)      |
| 주석 블록 보충                                              | 예            |
| 웹서치 스토리                                               | 예 (§6)      |
| 참고문헌 URL                                                | 예            |
| 파일명 `20260518_report_beyond_cooperative_simulators.md` | 예            |
