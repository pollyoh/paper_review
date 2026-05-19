# [2026 세미나] Beyond Cooperative Simulators: Generating Realistic User Personas for Robust Evaluation of LLM Agents

> **자료 원본**: *Beyond Cooperative Simulators: Generating Realistic User Personas for Robust Evaluation of LLM Agents*
> **저자**: Harshita Chopra, Kshitish Ghate, Aylin Caliskan, Tadayoshi Kohno, Chirag Shah, Natasha Jaques
> **소속**: University of Washington (Seattle), Georgetown University (Washington, DC)
> **출처**: arXiv:2605.12894v1 [cs.CL] (2026)
> **발표일**: 2026-05-19

---

# 목차

1. [연구 배경 및 목적](#1-연구-배경-및-목적)
2. [방법론 설명](#2-방법론-설명)
3. [실험 결과](#3-실험-결과)
4. [결론](#4-결론)

---

# 1. 연구 배경 및 목적

## 풀고자 하는 문제

대화형 LLM 에이전트의 현재 벤치마크 평가 방식에 **근본적 결함**이 존재함을 지적함.

고객 지원·예약·기술 지원 등 다턴(multi-turn) 목표 지향 환경에서 에이전트를 평가할 때, 상대방 역할을 담당하는 **LLM 사용자 시뮬레이터가 지나치게 협조적**임을 확인함. 현실의 사용자는 정보를 단계적으로 공개하고, 모호하게 말하며, 에이전트의 가정에 반박하는 반면, 시뮬레이터는 필요한 정보를 즉시·완벽하게 제공하는 경향을 보임.

| 현상          | 협조적 시뮬레이터                 | 실제 사용자                      |
| ------------- | --------------------------------- | -------------------------------- |
| 정보 공개     | 식별자·사실을 빠르게 일괄 제공   | 단계적·선택적 공개, 재질문 필요 |
| 상호작용      | 정중·명확·에이전트 지시 수용    | 반박, 불확실성, 감정·조급함     |
| 다양성        | 프로필을 바꿔도 언어 패턴이 유사  | 동일 과제라도 궤적이 크게 다름   |
| 벤치마크 함의 | 에이전트 성공률**과대평가** | 배포 후 실패·불만 증가          |

이로 인해 **Sim2Real 격차(Simulation-to-Reality gap)** 가 발생하며, 리더보드 상위 모델도 실제 사용자 대상 배포 시 성능이 크게 하락함을 보임.

## 연구를 수행한 이유

Zhou et al. (2026)이 τ-bench 기반 451명 인간 대화 연구에서 LLM 시뮬레이터가 인간 대비 "easy mode"를 만든다는 점을 정량화함. 그러나 격차를 **측정**하는 데 그쳤고, 격차를 **해소**하는 방법론은 제시되지 않음.

본 연구는 격차를 해소하기 위해:

1. 시뮬레이터 분포를 인간 궤적 분포에 정렬하는 **자동화된 방법** 개발이 필요하다고 판단함
2. 수동으로 페르소나를 설계하는 방식은 인간 행동의 다양성을 충분히 포착하지 못함을 인식함
3. 벤치마크 환경·에이전트를 바꾸지 않고도 적용 가능한 **plug-and-play 레이어**가 필요하다고 보임

## 배경 모델 설명 (Preliminaries)

**τ²-bench (Barres et al., 2025)**
에이전트와 사용자가 공유 환경의 도구를 함께 사용하는 이중 제어(Dec-POMDP) 벤치마크. 단순히 텍스트로 정보만 교환하는 설정보다 현실에 가까움. PPol의 실험 플랫폼으로 활용됨.

**19차원 행동 지문 (Zhou et al., 2026)**
인간 대화 궤적을 4개 taxonomy, 19개 스칼라 특징으로 수치화한 체계.

| Taxonomy                  | 특징 수 | 대표 특징                                     |
| ------------------------- | ------- | --------------------------------------------- |
| D1 Communication Style    | 8       | words_per_turn, politeness_rate, verbosity_cv |
| D2 Information Disclosure | 3       | front_loading_ratio, identifiers_per_turn     |
| D3 Clarification Behavior | 5       | uncertainty_rate, pushback_rate               |
| D4 Error Reaction         | 3       | emotional_expression_rate, accusatory_rate    |

**Random Forest 판별기**
인간 궤적($y=1$)과 기본 시뮬레이터 롤아웃($y=0$)을 19차원 지문 기준으로 구분함. 진화 전 1회 학습하여 고정하고, 진화 중 fitness proxy로 사용함. 도메인·백엔드별 ROC-AUC 0.94–1.00 달성을 확인함.

## 연구 목적

**Persona Policies(PPol)** 를 제안함. 사용자 시뮬레이터 시스템 프롬프트에 덧붙이는 역할극 정책(  $P_\pi$   )을 **진화적 프로그램 탐색(OpenEvolve)**으로 자동 발견하고, 인간 유사도와 행동 다양성을 동시에 최적화하여 Sim2Real 격차를 줄임을 목표로 함.

핵심 기여 3가지:

1. **PPol**: 기존 벤치마크 시뮬레이터 위에 얹는 plug-and-play 페르소나 제어층
2. **진화적 프로그램 탐색**: 수동 설계 대신 Python 페르소나 생성기 $G$를 자동 변이·선택
3. **엔드투엔드 검증**: 행동 지문 기반 지표·블라인드 인간 평가·PPol 증강 SFT 견고성 연결

---

# 2. 방법론 설명

## 전체 아키텍처

PPol의 핵심 설계 원칙: 과제(goal)·사실·보상은 고정하고, 사용자 시뮬레이터 프롬프트에 덧붙이는 **Persona Policy $P_\pi$만 제어**함.

```
[고정] 과제 t, 목표, 환경, 성공 판정
         │
         ▼
[진화] 프로그램 G  ──생성──▶  Persona Policy P_π  ──연결──▶  사용자 시뮬레이터
         ▲                              │
         │                              ▼
         └──── 채점·Reflection ◀──  대화 궤적 τ (에이전트는 고정)
```

최종 사용자 프롬프트:

$$
\text{시뮬레이터 프롬프트} = s_{\mathrm{base}}(t) \;\oplus\; P_{\pi,t}^{(i)}
$$

![PPol 진화 루프 개요](../paper/Beyond_Cooperative_simulators/Figure_1.png)

**Figure 1**: Evolvable Program $G$가 행동 축 $D$·프롬프트·생성 코드를 보유함. Task Rollouts에서 $N$개 페르소나 정책이 고정 에이전트와 대화하며 궤적을 생성함. Evaluator가 인간 참조 $\mathcal{H}$와 비교해 fitness를 계산하고 Reflection 텍스트를 생성함. Evolutionary Coding Agent가 OpenEvolve로 $G$를 변이하며 반복함.

## PPol 진화 루프

한 iteration에서 7단계 순서로 동작함:

| 단계 | 구성 요소                 | 하는 일                                                  |
| ---- | ------------------------- | -------------------------------------------------------- |
| ①   | Evolvable Program$G$    | 행동 축·프롬프트·코드 보유                             |
| ②   | Population + Expansion    | $N$개 페르소나 정책 생성                               |
| ③   | Task Rollouts             | τ²에서 다턴 대화·도구 호출 실행                       |
| ④   | 19-D fingerprint          | 사용자 턴 통계적 지문 추출                               |
| ⑤   | Evaluator                 | Human-likeness + Coverage → fitness$\mathcal{M}$ 계산 |
| ⑥   | Reflection                | 실패 패턴 분석, 다음 변이 힌트 생성                      |
| ⑦   | Evolutionary Coding Agent | OpenEvolve로 코드·축·프롬프트 수정                     |

**MAP-Elites archive**: 단일 fitness 최대화 대신, 행동 지형상 서로 다른 $G$ 후보를 보관하여 탐색이 한 축에 몰리지 않도록 함. $(\bar{P}(\mathrm{human}), \bar{B}_{\mathrm{cover}})$ 격자 기준으로 bin별 최고 프로그램만 유지함.

## 2단계 페르소나 생성

$G$는 한 과제에 대해 $N$개의 서로 다른 Persona Policy를 **두 번의 LLM 호출**로 생성함.

**Stage 1 — Population generation (골격 $N$명)**

- 행동 축 $D$와 과제 컨텍스트 $c_t$를 조건으로 $N$명을 한 번에 생성
- 각 페르소나마다 축 활성화 벡터 $\mathbf{a}_t^{(i)} \in \{0,1\}^{|D|}$ 결정
- 조인트 샘플링으로 "한 과제 안에서 서로 다른 $N$ 방향" 확보

**Stage 2 — Persona expansion (연기 지침 $P_\pi$)**

- Stage 1 결과 각 멤버에 대해 150–250단어 역할극 지침 생성 ($N$명 병렬 처리)
- 활성화된 축의 playbook 문구를 조합하여 턴 단위 규칙으로 구체화
- 예: "주문번호를 첫 메시지에 넣지 말 것", "한 번에 한 필드만 답할 것"

![발견된 행동 축·페르소나·Reflection 예시](../paper/Beyond_Cooperative_simulators/Figure_2.png)

**Figure 2**: **(A)** 진화로 발견된 행동 축 (`temperament`, `information_velocity`, `narrative_bias` 등). **(B)** 생성된 페르소나 (hesitant procrastinator, no-nonsense executive 등). **(C)** Reflection이 지적하는 대표 실패—과도한 협조, 페르소나 이탈, 부자연스러운 완벽한 데이터 제공.

## 평가 지표

PPol은 **진화 fitness**($\mathcal{M}$)와 **결과 보고**($D_1$–$D_4$, USI)에 Zhou et al. (2026)의 **19차원 행동 지문(behavioral fingerprint)** 체계를 공통으로 사용함.

### 19-D 행동 지문과 $D_1$–$D_4$ taxonomy

완료 궤적 $\tau$(agent–user 다턴 대화)의 **사용자 턴만** 정규식·턴 통계·LIWC/NRC로 19개 스칼라를 추출해 $\mathbf{f}(\tau) \in \mathbb{R}^{19}$를 만듦. 19개 특징은 **4개 taxonomy**로 묶어 해석함 ($8+3+5+3=19$).

| Taxonomy | # | 측정 대상 | 대표 특징 | 협조적 시뮬 vs 인간 (직관) |
|----------|---|-----------|-----------|---------------------------|
| **$D_1$** Communication Style | 8 | 말하기 방식·길이·정중함 | `words_per_turn`, `politeness_rate`, `verbosity_cv` | 시뮬: 장황·과도하게 정중 |
| **$D_2$** Information Disclosure | 3 | 정보를 **언제·얼마나** 주는지 | `front_loading_ratio`, `identifiers_per_turn` | 시뮬: 식별자·사실을 **앞턴에 몰아** 제공 |
| **$D_3$** Clarification Behavior | 5 | 불확실성·**반박**·재질문 | `uncertainty_rate`, `pushback_rate`, `clarification_question_rate` | 시뮬: pushback·진짜 불확실성 **부족** |
| **$D_4$** Error Reaction | 3 | 에이전트 오류에 대한 반응 | `emotional_expression_rate`, `accusatory_rate`, `strategy_pivot_rate` | 시뮬: 감정·비난 대신 **조용히 방향 전환** |

**Human-likeness ($\bar{P}$)**
각 롤아웃을 19차원 지문으로 압축한 후 Random Forest가 '인간 클래스' 확률 산출, 미니배치 전체 평균:

$$
\bar{P}_{G,\mathcal{T}}(\mathrm{human}) = \frac{1}{|\mathcal{B}(G;\mathcal{T})|} \sum_{e \in \mathcal{B}(G;\mathcal{T})} p_{\mathrm{RF}}(\mathrm{human} \mid \mathbf{f}_e)
$$

- RF는 진화 **전 1회** 학습 후 **고정**: 양성 = $\mathcal{H}$ 인간 지문, 음성 = **기본 τ² 시뮬** 지문 (PPol 롤아웃은 학습에 미포함)
- 도메인(retail/airline)·시뮬 백엔드마다 별도 RF; 19축은 학습 전 표준화
- $\mathcal{B}(G;\mathcal{T})$: 미니배치 $\mathcal{T}$의 모든 과제×$N$명 롤아웃 에피소드 집합

**Behavioral Coverage ($\bar{B}_{\mathrm{cover}}$)**

> **$\mathrm{err}$와 $\bar{B}_{\mathrm{cover}}$는 동치가 아님.** $\mathrm{err}$는 **원시 Chamfer 거리**(작을수록 좋음), $\bar{B}_{\mathrm{cover}}$는 이를 $[0,1]$로 **정규화한 점수**(클수록 좋음). Table 1의 **Coverage** 열은 $\bar{B}_{\mathrm{cover}}$.

**입력 집합**
- $\mathcal{F}_t = \{\mathbf{f}^{(1)},\ldots,\mathbf{f}^{(N)}\}$: 과제 $t$에서 $G$가 뽑은 $N$명 페르소나의 롤아웃 지문 (과제마다 **시뮬 쪽만** 바뀜)
- $\mathcal{H}_{\mathrm{train}}$: Zhou et al. **인간** 대화에서 추출한 지문 풀 (도메인 전체, **과제와 무관·고정**)

**1단계 — Chamfer 오차 $\mathrm{err}$** (양방향, $\mathbb{R}^{19}$ 유클리드 거리):

$$
\mathrm{err}(\mathcal{F}_t, \mathcal{H}_{\mathrm{train}}) = \underbrace{\frac{1}{|\mathcal{H}_{\mathrm{train}}|} \sum_{h \in \mathcal{H}_{\mathrm{train}}} \min_{\mathbf{f} \in \mathcal{F}_t} \|h - \mathbf{f}\|_2}_{\text{항 A: 인간 → 시뮬 (모든 인간 유형 근처에 페르소나 ≥1)}} + \underbrace{\frac{1}{|\mathcal{F}_t|} \sum_{\mathbf{f} \in \mathcal{F}_t} \min_{h \in \mathcal{H}_{\mathrm{train}}} \|h - \mathbf{f}\|_2}_{\text{항 B: 시뮬 → 인간 (각 페르소나가 인간 구름 위)}}
$$

- **항 A만** 쓰면: $N$명이 인간 구름 **한쪽**에만 몰려도 일부 인간만 커버하면 됨
- **항 B만** 쓰면: 인간과 **멀리** 떨어진 이상치 지문(RF 허점)도 허용될 수 있음
- **A+B**: 인간 **전체**를 덮으면서, 각 페르소나는 **실제 인간 근처**에 있어야 함

**2단계 — 참조 스케일 $d_{\mathrm{ref}}$** (사전 계산·고정):

$$
d_{\mathrm{ref}} = \frac{1}{\binom{|\mathcal{H}_{\mathrm{train}}|}{2}} \sum_{\substack{h_i, h_j \in \mathcal{H}_{\mathrm{train}} \\ i < j}} \|h_i - h_j\|_2
$$

$\mathcal{H}_{\mathrm{train}}$에서 뽑은 **서로 다른 지문 쌍** $\binom{|\mathcal{H}_{\mathrm{train}}|}{2}$개 거리의 평균 — “인간들이 19-D 지문 공간에서 얼마나 퍼져 있는가”의 전형적 스케일.

**3단계 — 과제별 coverage 점수 $B_{\mathrm{cover}} \in [0,1]$** ($\mathrm{err}$ → 점수 변환):

$$
B_{\mathrm{cover}}(\mathcal{F}_t, \mathcal{H}_{\mathrm{train}}) = \max\left\{ 0,\, 1 - \min\left(1,\, \frac{\mathrm{err}}{2\, d_{\mathrm{ref}}} \right) \right\}
$$

| $\mathrm{err}$ | $B_{\mathrm{cover}}$ (대략) |
|----------------|-----------------------------|
| $0$ | $1.0$ (완벽) |
| $d_{\mathrm{ref}}$ | $0.5$ |
| $\geq 2\, d_{\mathrm{ref}}$ | $0.0$ |

분모의 **2**는 $\mathrm{err}$가 항 A+B **합**이므로, 한쪽 항 스케일($\sim d_{\mathrm{ref}}$)과 맞추기 위한 정규화(논문 §3.3).

**4단계 — 미니배치 평균 $\bar{B}_{\mathrm{cover}}$**:

$$
\bar{B}_{\mathrm{cover}}(G;\mathcal{T}) = \frac{1}{|\mathcal{T}|} \sum_{t \in \mathcal{T}} B_{\mathrm{cover}}(\mathcal{F}_t(G), \mathcal{H}_{\mathrm{train}})
$$

진화 iteration마다 과제 미니배치 $\mathcal{T}$(예: 5개)를 샘플 → **과제마다** 위 1–3단계 → 평균. Table 1 **Coverage** = test set에서의 $\bar{B}_{\mathrm{cover}}$.

**결합 Fitness ($\mathcal{M}$)**
판별기 단독 최대화 시 adversarial 과적합 방지를 위해 두 지표를 가중합:

$$
\mathcal{M}(G;\mathcal{T}) = \lambda_h \, \bar{P}_{G,\mathcal{T}}(\mathrm{human}) + \lambda_b \, \bar{B}_{\mathrm{cover}}(G;\mathcal{T})
$$

커리큘럼에서 $N$이 $5 \to 8 \to 10$으로 증가할수록 $\lambda_b$를 높여 다양성 압력 강화함.

### $D_1$–$D_4$ Dice 및 USI (Zhou et al. 방식, 보고용)

진화 **fitness $\mathcal{M}$에는 직접 들어가지 않고**, Table 1 등에서 “인간 대비 **어느 행동 축**에서 가까워졌는지” 해석하기 위한 **보고 지표**임.

각 taxonomy $D_k$에 속하는 특징들의 **평균 프로필**을 시뮬레이터·인간($\mathcal{H}$) 각각 구한 뒤, 특징 $m$마다 Sørensen–Dice 계수로 정렬도를 측정함:

$$
\mathrm{Dice}_m = \frac{2 \cdot \min(M_m,\, H_m)}{M_m + H_m} \times 100
$$

- $M_m$: 시뮬레이터 측 특징 $m$ 평균, $H_m$: 인간 측 평균
- 100에 가까울수록 해당 특징이 **인간과 정렬**
- **$D_k$ 점수** = 그 축에 속한 특징들의 Dice **평균** (예: $D_3$ = clarification 5개 특징 평균)

**USI$_{D1\text{-}D4}$** (User-Sim Index, 4차원 집계):

$$
\mathrm{USI}_{D1\text{-}D4} = \frac{1}{4}\left(D_1 + D_2 + D_3 + D_4\right)
$$

Zhou et al. 전체 USI(6축, 설문·ECE 포함)와 달리, PPol Table 1의 USI$_{D1\text{-}D4}$는 **행동 4축 Dice만** 평균한 값(%). Humans ≈ 87.8%, Base ≈ 35.1%, PPol-Evolved ≈ 76.5% (Retail/Qwen).

| 지표 | 역할 | PPol 진화에 사용 |
|------|------|------------------|
| $\bar{P}$, $\bar{B}_{\mathrm{cover}}$, $\mathcal{M}$ | 생성기 $G$ **선택·진화** | ✅ fitness |
| $D_1$–$D_4$, USI$_{D1\text{-}D4}$ | 축별 **정렬도 보고·해석** | ❌ (사후 분석) |

PPol-Evolved는 Base 대비 **$D_3$(clarification), $D_4$(error reaction)** 에서 Dice 개선이 특히 큼(2–3배) — 협조적 시뮬레이터가 약했던 **반박·오류 반응** 축을 인간 쪽으로 끌어올렸다는 뜻.

---

# 3. 실험 결과

## 데이터셋

**τ²-bench** (Barres et al., 2025):

- **Retail**: 74 train / 40 test 과제
- **Airline**: 30 train / 20 test 과제
- 사용자도 공유 환경 도구를 쓰는 이중 제어(Dec-POMDP) 구조

**인간 참조 말뭉치 $\mathcal{H}$** (Zhou et al., 2026):

- Prolific 기반 실제 사용자 대화 451명 규모
- 19차원 행동 지문 추출 후 RF 학습 및 coverage 기준으로 사용

**인간 평가**: Prolific 20명 모집 → QC 후 16명 어노테이터, 87개 대화, Retail 도메인

## 비교 모델

| 방법                   | 설명                                                                                |
| ---------------------- | ----------------------------------------------------------------------------------- |
| Base-simulator         | τ² 기본 사용자 시뮬레이터, 페르소나 없음                                          |
| DP Personas            | 과제당 1회 LLM 호출로$N$개 지침 생성 (2단계·축 구조 없음)                        |
| PPol-Initial           | 시드 축(terse, skeptical, frustrated, ambiguous) + 2단계 생성기,**진화 없음** |
| **PPol-Evolved** | 최대 70 iter 진화, validation$\mathcal{M}$ 최고 체크포인트                        |
| Humans (참조)          | Zhou et al. 인간 대화 지문·지표 (시뮬레이터 아님)                                  |

## 평가 지표 (Table 1 요약)

§2.3에서 정의한 지표를 Table 1 열로 요약함:

- **HL**: $\bar{P}(\mathrm{human})$ — RF 인간 유사도 ($\uparrow$)
- **Coverage**: $\bar{B}_{\mathrm{cover}}$ — $\mathrm{err}$를 $d_{\mathrm{ref}}$로 정규화한 $[0,1]$ 점수 ($\uparrow$). **≠ raw Chamfer $\mathrm{err}$**
- **Score**: $\mathcal{M} = \lambda_h \bar{P} + \lambda_b \bar{B}_{\mathrm{cover}}$ — **진화 fitness** ($\uparrow$)
- **USI$_{D1\text{-}D4}$**: $D_1$–$D_4$ taxonomy별 Dice 평균 → 4축 평균 (%) — **보고용**, Zhou 행동 4축 정렬도 ($\uparrow$)

## 정량 결과

**Table 1 — Retail, Qwen3-Next-80B**

| Method                  | HL$\uparrow$  | Coverage$\uparrow$ | Score$\uparrow$ | USI$_{D1\text{-}D4}$ $\uparrow$ |
| ----------------------- | --------------- | -------------------- | ----------------- | ----------------------------------- |
| Humans                  | 0.953           | 0.614                | 0.783             | 87.8%                               |
| Base-simulator          | 0.107           | 0.046                | 0.077             | 35.1%                               |
| DP Personas             | 0.291           | 0.100                | 0.196             | 37.2%                               |
| PPol: Initial           | 0.356           | 0.017                | 0.186             | 39.8%                               |
| **PPol: Evolved** | **0.784** | **0.602**      | **0.693**   | **76.5%**                     |

- Base 대비 Score **+61.6%p** (Retail/Qwen), Airline/GPT-5.4-Mini에서 **+33.1%p** 개선 확인함
- DP Personas·PPol-Initial은 Coverage 개선이 미미함 → MAP-Elites + $\lambda_b$ 커리큘럼이 인간 분포를 덮는 페르소나 집단 생성에 필수적임을 보임
- $D_3$(clarification), $D_4$(error reaction)에서 Base 대비 **2–3배** Dice 개선 확인함

![진화 중 fitness 및 구성요소](../paper/Beyond_Cooperative_simulators/Figure_3.png)

**Figure 3**: **왼쪽** Combined Score — Validation $N{=}5,8,10$이 약 20 iter 이후 0.5–0.6대로 수렴하며 Baseline Val(~0.12)을 크게 상회함. **오른쪽** 두 구성요소가 함께 상승하며 후반에 coverage와 human-likeness의 균형을 이룸.

![PCA 행동 지문 공간](../paper/Beyond_Cooperative_simulators/Figure_4.png)

**Figure 4**: Retail·DeepSeek-V3.1 기준 PCA 투영. 초록 삼각형(인간)은 PC1 음의 영역에 군집, 빨간 원(Base)은 오른쪽으로 치우침. 파란 원(PPol)이 인간 군집과 부분 중첩하며 "협조적 시뮬레이터 클러스터"에서 "인간 지원 영역"으로의 분포 이동을 시각적으로 확인함.

## 블라인드 인간 평가

![어노테이터 Human/Bot 판정](../paper/Beyond_Cooperative_simulators/Figure_5.png)

**Figure 5**: PPol이 실제 인간과 통계적으로 유사한 "인간처럼 보임" 비율을 달성함.

| 조건                | Human 판정      | Bot 판정        |
| ------------------- | --------------- | --------------- |
| True human          | 80.0%           | 10.8%           |
| **PPol**      | **80.4%** | ~3.9%           |
| τ² base-simulator | 46.5%           | **46.5%** |

- Welch $t=3.556$, $p=6.37\times10^{-4}$ — PPol과 base 간 유의한 차이 확인함
- $p_{\mathrm{RF}}$와 어노테이터 판정의 Point-Biserial $r=0.49$ ($p<0.001$) — 19-D 지문이 인간 지각의 유효한 proxy임을 뒷받침함

## 에이전트 SFT 견고성

Gemma-4-31B 에이전트를 LoRA(rank 32)로 32 step SFT 후 He et al. τ-trait OOD 평가 수행함.

**Retail — Task Success Rate**

| Training                   | In-dist. Default | Skeptical | Incoherent | Impatient | Confusion       | **OOD Avg** |
| -------------------------- | ---------------- | --------- | ---------- | --------- | --------------- | ----------------- |
| No FT                      | 0.650            | 0.150     | 0.225      | 0.150     | 0.200           | 0.181             |
| Default-only SFT           | 0.675            | 0.150     | 0.225      | 0.200     | 0.275           | 0.213             |
| **Default+PPol SFT** | **0.750**  | 0.175     | 0.225      | 0.200     | **0.400** | **0.250**   |

- In-dist. **+11%p** 향상, OOD 평균 **+17% 상대** 향상 확인함
- **Confusion** 조건에서 가장 큰 이득(+0.125) — PPol이 생성하는 "이전 턴 재의심" 패턴과 정합함
- PPol SFT를 로봇의 **domain randomization**에 대응되는 "언어 에이전트용 학습 분포 다양화"로 해석 가능함

---

# 4. 결론

## 연구 결론

### 이 연구가 바꾼 것

PPol은 "더 많은 수동 제작 페르소나"가 아니라, **인간 행동 지문 공간에서의 위치**를 명시적 목적함수로 최적화하는 **프로그램 합성(program synthesis)** 접근임을 보임.

협조적 기본 시뮬레이터는 에이전트 연구의 **숨은 가정(hidden default)** 이었음. LLM 사용자 시뮬레이터는 기저 모델의 기본 성향인 "도움이 되려는 경향"을 그대로 반영해, 에이전트를 위해 정보를 미리 정리해주고, 반박 없이 따르고, 인내심 있게 기다리는 협조적 사용자를 기본값으로 설정해왔음. 이 가정이 암묵적으로 유지된 채 에이전트 성능이 측정되어왔음을 본 논문이 지적함.

PPol은 이 가정을 **측정 가능·진화 가능**한 형태로 전환한 첫 사례임. 핵심 기여를 아래와 같이 정리함:

| 기여 | 의의 |
|------|------|
| 19차원 행동 지문 + RF 판별기 | 인간-시뮬레이터 격차를 수치로 측정 가능하게 함 |
| OpenEvolve 진화 루프 | 수동 설계 없이 인간 분포에 정렬된 페르소나 자동 발견 |
| MAP-Elites 커버리지 | 한 가지 스타일 과적합 없이 인간 행동 공간 전체를 덮는 다양성 확보 |
| Reflection 기반 변이 | "왜 협조적으로 보이는가"를 언어로 진단하고 다음 세대에 반영 |
| SFT 견고성 검증 | 더 현실적 시뮬레이터가 에이전트 훈련에도 직접 이득임을 실증 |

### 정량 성과 요약

τ²-bench에서 fitness 33–62%p 개선, 블라인드 평가에서 인간 판정률 80.4%(실제 인간 80.0%와 동등), PPol 기반 SFT로 OOD 견고성 +17% 달성을 확인함.

기존 접근과의 성과 차이가 특히 두드러지는 지점은 **Coverage** 지표임. DP Personas(0.100)·PPol-Initial(0.017)은 단순히 다양한 페르소나 설명을 생성해도 인간 행동 공간을 덮지 못했고, 오직 **진화 + MAP-Elites**를 거친 PPol-Evolved(0.602)만이 인간(0.614)에 근접한 커버리지를 달성함. "다양하게 보이는 것"과 "실제로 다양한 것"이 다르다는 점을 실험적으로 보임.

### 한계

| 한계 | 설명 |
|------|------|
| 인간 말뭉치 의존 | 판별기·coverage 모두 도메인별 인간 대화 수집 필요 — 신규 도메인 적용 시 비용 발생 |
| 지문의 언어·문화 한계 | 19차원 regex 기반 지문은 뉘앙스·문화적 특수성(방언, 존댓말 체계 등) 포착에 한계 |
| 검증 도메인 제한 | Retail/Airline 2개 도메인에 한정 — 의료·금융·법률 등 고위험 도메인 미검증 |
| 진화 비용 | iter 70 × 최대 50 rollout — 소규모 팀·빠른 프로토타이핑 환경 적용 시 부담 |
| 실사용자 최종 검증 부재 | SFT 견고성은 시뮬레이터 OOD 조건까지이며, 실제 사용자 대상 A/B 테스트는 미수행 |

## 이후 개선 방향: 문화·인구통계적으로 다양한 현실적 유저 시뮬레이션으로 이동

PPol이 행동 다양성 측면의 Sim2Real gap을 줄이는 성과를 거둔 이후, "**더 다양한 유저를 더 정확하게 재현**하려는 연구"가 급증하는 흐름을 보임.

**대표 사례: NVIDIA Nemotron-Personas-Korea (2026.4)**

- **700만 개** 한국인 합성 페르소나 데이터셋 구축
- 실제 한국 통계(KOSIS, 건강보험, 이름 통계 등) 기반 **정밀 인구 분포** 반영
- 연령·지역·직업·**문화적 맥락**(존댓말, 방언, 생활 패턴)까지 고려
- 한국 사용자 최적화 AI 에이전트 개발·평가에 직접 활용 가능

**시사점**: PPol의 **행동 다양성** + NVIDIA의 **문화적·인구통계적 grounded 페르소나** → 더 현실적이고 포괄적인 사용자 시뮬레이션 시대 도래함. 두 접근의 결합이 향후 연구 방향으로 부상하고 있음.

## 회사 업무와의 연관성: 초개인화

D-Model팀의 핵심 과제인 **초개인화(hyper-personalization)** 서비스와 직접적 연결점이 존재함.

| PPol 인사이트                      | 초개인화 적용                                                                                   |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| 사용자는 협조적·균질하지 않음     | 실제 사용자의 다양한 커뮤니케이션 스타일(조급함, 모호함, 회의적)을 모델 학습 데이터에 반영 필요 |
| 행동 축($D$)으로 페르소나 구조화 | 개인화 추천·대화 시스템 평가 시 협조적 시뮬레이터에 의존하면 실제 사용자 경험과 괴리 발생 가능 |
| SFT 시 다양한 사용자 분포 주입     | 개인화 모델 학습에 PPol식 다양 페르소나 적용 시 실사용 환경 견고성 향상 기대                    |
| NVIDIA 한국인 페르소나 데이터셋    | 한국 사용자 대상 초개인화 서비스에 문화·인구통계적으로 grounded된 페르소나 데이터 활용 가능    |

협조적·단일한 시뮬레이터로 검증된 초개인화 알고리즘은 실제 사용자(다양한 나이, 디지털 리터러시, 성격)와의 상호작용에서 성능 저하가 나타날 수 있음을 인식하고, 평가 파이프라인에 PPol식 다양성 검증을 도입하는 방안을 검토할 필요가 있음.
