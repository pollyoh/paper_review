# 통합 디자인 스펙: 콘텐츠 분리, 품질·자동화, UX

**작성일**: 2026-04-22  
**범위**: 저장소 `paper_study` — Astro SSG + GitHub Pages 배포 사이트  
**구현 순서(고정)**: **A → D → B → C** (한 번에 하나의 기능/영역만 완료)

---

## 1. 목표

1. **논문 리뷰**와 **기술 학습 정리(studies)** 를 콘텐츠 모델·URL·발견 UX 상에서 명확히 분리한다.
2. Power BI 관련 발행물은 **사이트에 studies 4편(본문 + 부록 D·E·F)** 으로만 노출하고, 중간 산출물·임시 파일은 버전 관리에서 제외한다.
3. 보고서 품질은 **가이드 + lint 스크립트(L2)** 로 표준화한다.
4. **로컬 publish CLI + CI 게이트(S2)** 로 `report/` → `src/content/` → 빌드 전 검증을 자동화한다.
5. 메인 페이지 **탭 + 배지 + 관련 글** 등으로 발견성을 높이고, 사이트 브랜딩을 **seunghee's Archive** 로 통일한다.

---

## 2. 영역 A — 콘텐츠 모델·저장소·Power BI 분할

### 2.1 두 컬렉션 분리

| 컬렉션 | Astro 경로 | URL 패턴 | 용도 |
|--------|------------|----------|------|
| `reviews` | `src/content/reviews/*.md` | `{BASE}/reviews/{slug}/` | 학술 논문 분석 보고서 |
| `studies` | `src/content/studies/*.md` | `{BASE}/studies/{slug}/` | 도구·개념 등 기술 학습 정리 (스코프 β: 도구 + 일반 기술 개념) |

- **슬러그 규칙**: 기존 reviews와 동일 — `YYYYMMDD-kebab-case-title` (예: `20260410-alto-adaptive-lora-tuning-and-orchestration`).
- **레거시 `docs/`**: 수정하지 않는다 (`review_instruction.md` 관행 유지).

### 2.2 `studies` frontmatter 스키마

`src/content.config.ts`에 `studies` 컬렉션을 추가한다.

**필수**

- `title` (string)
- `date` (coerce date)
- `description` (string)
- `tags` (string[])
- `topic` (string) — 글의 주제 축 (예: `Power BI`). 탭/필터·관련 글에 사용.

**선택**

- `sources` — `{ title: string, url: string (URL) }[]`
- **C4 대응**: 카드에서 reviews와 동일한 두 번째·세 번째 텍스트 라인(`originalTitle`, `authors` 스타일)을 유지하기 위해 다음을 **선택 필드**로 둔다.
  - `originalTitle` (string, optional) — 예: 공식 제품명·문서 세트명
  - `authors` (string, optional) — 예: `Microsoft Learn` 등
  - `institution` (string, optional) — 필요 시만
- 값이 없으면 UI는 해당 라인을 숨기거나 `topic`만 보조 정보로 표시하는 등 일관된 폴백 규칙을 적용한다.

### 2.3 미배포·자산 정리 정책 (합의 표 그대로)

| 항목 | 처리 |
|------|------|
| `report/_generated_dax_appendix.md`, `_generated_m_appendix.md` | `.gitignore`에 추가, 저장소에서 추적 제거(재생성 가능) |
| `.tmp_*` | `.gitignore` + 작업 트리에서 삭제 |
| `scripts/__pycache__/`, `*.pyc` | `.gitignore` |
| `report/img/power_bi/*.png` | 커밋. publish 시 `public/images/studies/{slug}/`로 필요한 것만 복사 |
| `paper/Agentic_Ecosystems/` | **폴더명 유지**. PDF·이미지 커밋. 해당 논문 리뷰는 `reviews`로 배포 |
| 기타 `paper/*` 원본 | 커밋 (일관된 출처 보관) |
| `report/20260416_*_recommender_systems.md` | `reviews`로 변환·배포 |
| `report/20260420_power_bi_report.md` | 커밋 유지. 아래 2.4대로 4개 studies로 분할 발행 |
| `scripts/*.py` + 테스트 | 커밋. (선택) `scripts/README.md`로 재생성 절차 한 단락 |
| `review_instruction.md` | 변경분은 별도 커밋. D 영역에서 본격 정비 |

### 2.4 Power BI: 본문 + 부록 D·E·F → studies 4편

원본 단일 파일 `report/20260420_power_bi_report.md`는 **소스 오브 트루스**로 유지한다. 사이트용으로는 아래 4개 마크다운을 `src/content/studies/`에 둔다 (본문에서 해당 섹션 경계로 분리).

| 역할 | 제안 슬러그(날짜 접두 일치) | 본문 출처 구간(개요) |
|------|---------------------------|----------------------|
| Desktop 가이드(본문 1~12장 등) | `20260420-power-bi-desktop-guide` | `#` 시작 ~ 부록 D 직전 |
| 부록 D (DAX) | `20260420-power-bi-dax-reference` | `## 부록 D: ...` ~ 부록 E 직전 |
| 부록 E (M) | `20260420-power-bi-m-reference` | `## 부록 E: ...` ~ 부록 F 직전 |
| 부록 F (체크리스트) | `20260420-power-bi-review-checklist` | `## 부록 F: ...` ~ 파일 끝 |

- 각 파일 **상호 링크**: 본문 하단에 부록 3편 링크, 각 부록 상단에 본문·형제 부록 링크.
- 이미지: `report/img/power_bi/` 참조를 빌드용 경로 `/images/studies/{slug}/...` 로 맞춘다.
- **사이트에 단일 통합 Power BI 페이지는 두지 않는다** (요구사항: Power BI 관련 **발행은 이 4편만**).

### 2.5 라우팅

- `src/pages/reviews/[...slug].astro` 패턴을 studies에 복제하거나, 공통 레이아웃만 공유하는 `src/pages/studies/[...slug].astro` 를 추가한다.
- 상세 구현은 구현 계획 단계에서 확정.

---

## 3. 영역 D — 보고서 품질 표준화 (L2)

### 3.1 문서

- `review_instruction.md`: 마크다운 구조 오류 수정, **reviews** 작성 가이드 유지·보완.
- **신규** `study_instruction.md`(가칭): **studies** 용 작성 원칙·체크리스트·파일명 규칙.

### 3.2 Lint 스크립트 (`scripts/lint_report.py` 등)

**모드**

- 기본: 경고만 (`--strict` 시 실패로 종료, CI에서 사용).

**규칙 (합의: #1~#9 전부 + #10 간이)**

1. 파일명: reviews 소스는 `YYYYMMDD_report_<snake>.md` 패턴을 기본으로 한다. studies 소스는 `YYYYMMDD_*.md` 형태를 허용하되, 파일명에 `_report_` 문자열이 **포함될 수 있다**(예: `20260420_power_bi_report.md`). 정확한 정규식·예외는 `study_instruction.md`와 `lint_report.py`에 단일 정의한다.
2. frontmatter 필수 필드: 카테고리별로 정의된 키 존재·타입.
3. reviews 본문 상단 메타 블록(원논문/저자/소속/출처/작성일) 존재 여부.
4. 최소 `##` 헤딩 개수: reviews 7섹션 정책과 정렬, studies 최소 3개.
5. 표: reviews 3+, studies 1+ (파이프 테이블 패턴 등으로 추정).
6. mermaid: reviews 2+, studies 필수 없음.
7. 주석 블록: reviews `[주석]` 1+, studies 필수 없음.
8. 이미지 경로: 참조 파일 존재.
9. 참고문헌·URL: 마지막 섹션 등에 URL 1개 이상.
10. 간이 구문: 예) 닫히지 않은 펜스 코드블록 검사. **markdownlint 등 외부 도구 의존은 이번 범위에서 제외.**

---

## 4. 영역 B — 작성·배포 자동화 (S2)

### 4.1 로컬 CLI

- 예: `python scripts/publish.py --category reviews|studies path/to/report.md`
- **카테고리는 반드시 플래그로 지정**. 미지정 시 즉시 실패.
- 수행 순서(개략): D lint → slug·frontmatter 생성/병합 → `src/content/{reviews|studies}/` 에 쓰기 → 이미지 detect·복사·경로 rewrite → 사용자에게 `npm run build` 안내 또는 서브프로세스 호출(구현 계획에서 확정).

### 4.2 CI 게이트

- PR 및/또는 `main` push 시: `npm ci` → lint( strict ) → `npm run build` 실패 시 배포/머지 차단.
- 기존 `deploy-pages.yml`과의 관계: 배포 job 전에 검증 job을 두거나, 별도 workflow로 분리(구현 계획에서 확정).

---

## 5. 영역 C — 사이트 UX·발견성

### 5.1 브랜딩 (C3)

- 메인 헤더 제목: **seunghee's Archive**
- 부제: **논문 리뷰와 기술 학습 정리** (또는 동등 의미의 한국어 한 줄)
- `BaseLayout` 기본 `description` 등 메타도 동일 취지로 갱신.

### 5.2 메인 탭 (C1)

- 탭: **전체 / 논문 / 기술공부** (라벨은 한국어로 통일 가능).
- 상태는 URL 쿼리 등으로 공유 가능하면 좋음 (예: `?tab=studies`) — 구현 계획에서 확정.

### 5.3 카드 (C2, C4)

- **배지**: 카드에 콘텐츠 유형 표시 (논문 vs 기술공부).
- **텍스트 블록**: reviews는 기존과 동일. studies는 `originalTitle`·`authors`·`institution`이 있으면 동일 스타일로 표시, 없으면 폴백( `topic` 등).

### 5.4 관련 글 (C5)

- 리뷰·스터디 **개별 페이지 하단**에 "관련 글" 섹션.
- 우선순위: 동일 `topic` → 태그 교집합 → 최신순, 상한 3건.
- 구현은 Astro에서 컬렉션 순회 또는 빌드 시 정적 생성.

### 5.5 코드 변경 범위 (기존 가이드와의 정합)

- 과거 `review_instruction.md`에는 `src/components/`, `src/layouts/`, `src/styles/common.css`, `src/scripts/review-enhance.js` 등 **수정 금지** 문구가 있다. 본 스펙(C1~C5, studies 라우트)은 이와 **부분 충돌**한다.
- **본 스펙이 우선**한다. 구현 시 다음을 허용·갱신한다.
  - **허용**: `src/pages/index.astro`, `src/components/PaperSearch.tsx`, `src/styles/index.css`, `src/content.config.ts`, `src/pages/studies/`(신규), 리뷰 라우트 옆 레이아웃 공유 방식 등.
  - **원칙적 비터치**: 리뷰 **본문** 렌더링용 `src/styles/common.css`, `src/scripts/review-enhance.js`, `src/layouts/ReviewLayout.astro` 내부 구조는 필요 최소한만 변경(관련 글 블록 삽입 슬롯 등)한다.
- `review_instruction.md`의 "수정 금지" 절은 구현 착수 시 위 내용에 맞게 **문서를 개정**한다.

---

## 6. 데이터 흐름(요약)

```text
report/*.md  --(lint)-->  publish CLI  -->  src/content/{reviews|studies}/*.md
                                              + public/images/...
                    -->  npm run build  -->  dist/  -->  GitHub Pages
```

---

## 7. 성공 기준 (검수)

- `reviews`와 `studies`가 각각 URL·스키마·카드 표현에서 혼동 없이 구분된다.
- Power BI는 studies **4페이지**만 공개되고, `_generated_*.md`·`.tmp_*`는 추적되지 않는다.
- `Agentic_Ecosystems` 논문 리뷰가 `reviews`로 배포된다.
- 로컬에서 publish CLI 한 번으로(또는 문서화된 최소 단계로) 동일 결과를 재현할 수 있다.
- CI에서 lint(strict) + build가 통과하지 않으면 배포 파이프라인이 막힌다.
- 메인에서 탭·검색·태그·관련 글이 합의된 동작을 한다.

---

## 8. 명시적 비범위 (이번 스펙 이후)

- 논문 간 인용·반박 그래프(C6급), 다크 모드(C8), 읽기 진행 바(C7).
- studies를 URL 토픽 prefix로 재구조화 (필요 시 후속 스펙).
- 외부 preview 배포(Netlify 등).

---

## 9. 스펙 자체 점검 (요약)

- 모순: studies 스키마에 (B) `topic`+`sources`와 (C4) 선택적 `originalTitle`/`authors`를 함께 명시해 UI·lint·가이드가 한 줄로 맞도록 했다.
- Placeholder: 슬러그 4개는 구현 시 원본 헤딩과 정확히 맞춰 검증한다.
- 범위: A~C를 한 PR에 넣지 않고 **A → D → B → C** 순으로 쪼갠다.

---

## 다음 단계

구현에 들어가기 전에 이 스펙 파일을 검토해 주세요. 승인 후 **writing-plans** 스킬로 영역별 구현 계획을 작성한다.
