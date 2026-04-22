# Content Collections, Lint, Publish CLI, UX Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 스펙 `docs/superpowers/specs/2026-04-22-content-collections-pipeline-ux-design.md`를 구현하여 `reviews`/`studies` 분리, Power BI 4편 studies, report lint·publish CLI, CI 검증, 메인 탭·배지·관련 글·브랜딩을 완성한다.

**Architecture:** Astro Content Collections에 `studies`를 추가하고 `src/pages/studies/[...slug].astro`로 정적 라우트를 복제한다. `report/` 원본은 유지하되 `_generated_*.md`·`.tmp_*`는 gitignore한다. Python으로 `lint_report.py`(report 단계 + `src/content` 단계)와 `publish.py`(플래그 `--category`)를 두고, GitHub Actions는 `npm ci` + content strict lint + `npm run build`로 게이트한다. 메인은 `PaperSearch`가 reviews·studies 합쳐진 목록을 받아 탭·쿼리스트링으로 필터한다.

**Tech Stack:** Astro 6, React 19, TypeScript, Zod (content schema), Python 3.12+ (stdlib + pytest), Node 22, GitHub Actions.

**권장 작업 방식:** `superpowers:using-git-worktrees`로 본 플랜 전용 worktree를 쓰면 `main`과 충돌을 줄일 수 있다. worktree 없이도 순서는 동일하다.

---

## 파일 맵 (생성·수정)

| 경로 | 책임 |
|------|------|
| `.gitignore` | `_generated_*.md`, `.tmp_*`, `__pycache__/`, `*.pyc` |
| `src/content.config.ts` | `studies` 컬렉션, `reviews`에 선택 필드 `topic` |
| `src/content/studies/*.md` | Power BI 4편 + frontmatter |
| `src/pages/studies/[...slug].astro` | studies 렌더·관련 글 |
| `src/pages/reviews/[...slug].astro` | 관련 글 블록 추가 |
| `src/layouts/ReviewLayout.astro` | `listHref` 선택 prop, `<slot name="related" />` |
| `src/lib/relatedPosts.ts` | 관련 글 점수 알고리즘 |
| `src/components/PaperSearch.tsx` | 탭·배지·통합 카드·URL 동기화 |
| `src/pages/index.astro` | 두 컬렉션 로드·브랜딩 문구 |
| `src/styles/index.css` | 탭·배지 스타일 |
| `scripts/split_power_bi_report.py` | 단일 report → 4개 studies 본문 생성(저장소 루트 기준 경로) |
| `scripts/lint_report.py` | `--category`, `--strict`, `--stage report|content` |
| `scripts/publish.py` | `--category reviews|studies`, lint 호출·복사·경로 치환 |
| `scripts/test_lint_report.py` | pytest |
| `scripts/test_publish.py` | publish의 순수 함수(슬러그·경로) 단위 테스트 |
| `study_instruction.md` | studies 작성 규칙 |
| `review_instruction.md` | 코드블록 수정·studies·수정 허용 범위 반영 |
| `.github/workflows/verify.yml` | PR + push: Python + npm lint/build |
| `.github/workflows/deploy-pages.yml` | `needs: verify`로 변경(또는 verify 내 job 합류) |
| `public/images/studies/{slug}/` | Power BI 스크린샷 복사본 |

---

### Task A1: 저장소 정리 (.gitignore, 추적 제거)

**Files:**
- Modify: `.gitignore`
- Delete (tracked이면): `report/_generated_dax_appendix.md`, `report/_generated_m_appendix.md`, `.tmp_*` (존재 시)

- [ ] **Step 1:** `.gitignore` 끝에 다음 블록 추가

```gitignore
# Power BI 생성물·임시 캐시 (스펙 §2.3)
report/_generated_*.md
.tmp_*
**/__pycache__/
*.pyc
```

- [ ] **Step 2:** 이미 git에 올라간 `_generated_*.md`가 있으면 제거

```bash
git rm -f --ignore-unmatch report/_generated_dax_appendix.md report/_generated_m_appendix.md
```

- [ ] **Step 3:** `.tmp_*` 파일이 작업 트리에만 있으면 삭제(추적 안 됨)

```bash
rm -f .tmp_*
```

- [ ] **Step 4:** 커밋

```bash
git add .gitignore
git commit -m "chore: ignore generated appendices and tmp artifacts"
```

---

### Task A2: `studies` 컬렉션 + `reviews.topic` 선택 필드

**Files:**
- Modify: `src/content.config.ts`

- [ ] **Step 1:** `src/content.config.ts` 전체를 아래로 교체(기존 `reviews` 스키마 유지 + `topic` 선택 + `studies` 추가)

```typescript
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const reviews = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews' }),
  schema: z.object({
    title: z.string(),
    originalTitle: z.string(),
    date: z.coerce.date(),
    authors: z.string(),
    institution: z.string(),
    tags: z.array(z.string()),
    description: z.string(),
    topic: z.string().optional(),
  }),
});

const studies = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/studies' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string(),
    tags: z.array(z.string()),
    topic: z.string(),
    sources: z
      .array(
        z.object({
          title: z.string(),
          url: z.string().url(),
        }),
      )
      .optional(),
    originalTitle: z.string().optional(),
    authors: z.string().optional(),
    institution: z.string().optional(),
  }),
});

export const collections = { reviews, studies };
```

- [ ] **Step 2:** 빈 폴더 방지용 placeholder 제거 전략 — 곧 A3에서 파일 추가하므로, 이 시점에서 `mkdir -p src/content/studies` 만 수행하거나 A3과 같은 커밋에 묶는다.

- [ ] **Step 3:** 검증

```bash
npm run build
```

Expected: `studies` 폴더가 비어 있으면 glob이 빈 컬렉션이 되어 빌드는 성공해야 한다(Astro 6 glob 빈 base 동작 확인; 실패 시 `.gitkeep` 대신 A3에서 첫 md 추가).

- [ ] **Step 4:** 커밋

```bash
git add src/content.config.ts
git commit -m "feat(content): add studies collection and optional review topic"
```

---

### Task A3: Power BI report → 4개 studies 마크다운 생성

**Files:**
- Create: `scripts/split_power_bi_report.py`
- Create: `src/content/studies/20260420-power-bi-desktop-guide.md`
- Create: `src/content/studies/20260420-power-bi-dax-reference.md`
- Create: `src/content/studies/20260420-power-bi-m-reference.md`
- Create: `src/content/studies/20260420-power-bi-review-checklist.md`

- [ ] **Step 1:** `scripts/split_power_bi_report.py` 생성 — 단일 소스 `report/20260420_power_bi_report.md`를 헤딩 `## 부록 D`, `## 부록 E`, `## 부록 F`로 4분할하고, 각 chunk에 YAML frontmatter + 내비 링크를 붙인 뒤 `src/content/studies/{slug}.md`에 쓴다. 이미지 `](./img/power_bi/` → `` `/paper_review/images/studies/{slug}/` `` 로 치환한다(기존 reviews와 동일하게 base 경로 포함).

스크립트 본문(전체):

```python
#!/usr/bin/env python3
"""Split report/20260420_power_bi_report.md into four studies under src/content/studies/."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report" / "20260420_power_bi_report.md"
OUT_DIR = ROOT / "src" / "content" / "studies"
BASE = "/paper_review/images/studies"

SLUGS = {
    "guide": "20260420-power-bi-desktop-guide",
    "dax": "20260420-power-bi-dax-reference",
    "m": "20260420-power-bi-m-reference",
    "checklist": "20260420-power-bi-review-checklist",
}

FRONTMATTER = {
    "guide": """---
title: "Power BI Desktop 기능·DAX·M 통합 리포트 (본문)"
date: 2026-04-20
description: "Desktop UI·시각화·Power Query·모델·RLS·옵션을 한글 메뉴 기준으로 정리한 학습용 본문이다."
tags: ["Power BI", "DAX", "Power Query", "시각화"]
topic: "Power BI"
originalTitle: "Power BI Desktop (Microsoft)"
authors: "Microsoft Learn 기반 정리"
sources:
  - title: "Power BI 문서"
    url: "https://learn.microsoft.com/power-bi/"
  - title: "DAX 참조"
    url: "https://learn.microsoft.com/dax/"
---
""",
    "dax": """---
title: "Power BI — DAX 함수 레퍼런스 (부록 D)"
date: 2026-04-20
description: "DAX 함수·색인·예제를 함수 단위로 모은 부록이다."
tags: ["Power BI", "DAX"]
topic: "Power BI"
originalTitle: "Data Analysis Expressions (DAX)"
authors: "Microsoft Learn · dax.guide 기반"
sources:
  - title: "DAX 참조"
    url: "https://learn.microsoft.com/dax/"
---
""",
    "m": """---
title: "Power BI — Power Query M 레퍼런스 (부록 E)"
date: 2026-04-20
description: "Power Query M 식별자·함수 목록을 자동 생성 규칙에 맞춘 부록이다."
tags: ["Power BI", "Power Query", "M"]
topic: "Power BI"
originalTitle: "Power Query M"
authors: "Microsoft Learn 기반"
sources:
  - title: "Power Query M"
    url: "https://learn.microsoft.com/powerquery-m/"
---
""",
    "checklist": """---
title: "Power BI 보고서 검토 체크리스트 (부록 F)"
date: 2026-04-20
description: "Desktop·DAX·M·문서 매핑을 검토할 때 쓰는 체크리스트이다."
tags: ["Power BI", "체크리스트"]
topic: "Power BI"
---
""",
}


def split_body(text: str) -> tuple[str, str, str, str]:
    d = re.search(r"^## 부록 D:.*$", text, re.MULTILINE)
    e = re.search(r"^## 부록 E:.*$", text, re.MULTILINE)
    f = re.search(r"^## 부록 F:.*$", text, re.MULTILINE)
    if not d or not e or not f:
        raise SystemExit("appendix headings D/E/F not found")
    main = text[: d.start()].rstrip() + "\n"
    dax = text[d.start() : e.start()].rstrip() + "\n"
    msec = text[e.start() : f.start()].rstrip() + "\n"
    chk = text[f.start() :].rstrip() + "\n"
    return main, dax, msec, chk


def rewrite_images(chunk: str, slug: str) -> str:
    def repl(m: re.Match[str]) -> str:
        alt, path = m.group(1), m.group(2)
        if path.startswith("./img/power_bi/"):
            name = path.split("/")[-1]
            return f"![{alt}]({BASE}/{slug}/{name})"
        return m.group(0)

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, chunk)


def nav_links(which: str) -> str:
    g, dx, mx, c = SLUGS["guide"], SLUGS["dax"], SLUGS["m"], SLUGS["checklist"]
    base = "/paper_review/studies"
    series = "\n".join(
        [
            "",
            "---",
            "",
            "## 이 시리즈의 다른 글",
            "",
            f"- [본문 가이드]({base}/{g}/)",
            f"- [부록 D — DAX]({base}/{dx}/)",
            f"- [부록 E — M]({base}/{mx}/)",
            f"- [부록 F — 체크리스트]({base}/{c}/)",
            "",
        ]
    )
    if which == "guide":
        return series
    if which == "dax":
        return "\n".join(
            [
                "",
                "---",
                "",
                "## 이 시리즈의 다른 글",
                "",
                f"- [← 본문 가이드]({base}/{g}/)",
                f"- [부록 E — M]({base}/{mx}/)",
                f"- [부록 F — 체크리스트]({base}/{c}/)",
                "",
            ]
        )
    if which == "m":
        return "\n".join(
            [
                "",
                "---",
                "",
                "## 이 시리즈의 다른 글",
                "",
                f"- [← 본문 가이드]({base}/{g}/)",
                f"- [부록 D — DAX]({base}/{dx}/)",
                f"- [부록 F — 체크리스트]({base}/{c}/)",
                "",
            ]
        )
    return "\n".join(
        [
            "",
            "---",
            "",
            "## 이 시리즈의 다른 글",
            "",
            f"- [← 본문 가이드]({base}/{g}/)",
            f"- [부록 D — DAX]({base}/{dx}/)",
            f"- [부록 E — M]({base}/{mx}/)",
            "",
        ]
    )


def main() -> int:
    text = REPORT.read_text(encoding="utf-8")
    main, dax, msec, chk = split_body(text)
    chunks = {
        "guide": rewrite_images(main, SLUGS["guide"]) + nav_links("guide"),
        "dax": rewrite_images(dax, SLUGS["dax"]) + nav_links("dax"),
        "m": rewrite_images(msec, SLUGS["m"]) + nav_links("m"),
        "checklist": chk + nav_links("checklist"),
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for key, slug in SLUGS.items():
        out = OUT_DIR / f"{slug}.md"
        body = chunks[key]
        out.write_text(FRONTMATTER[key] + body, encoding="utf-8")
        print("wrote", out.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2:** 스크립트 실행 권한 및 실행

```bash
chmod +x scripts/split_power_bi_report.py
python3 scripts/split_power_bi_report.py
```

- [ ] **Step 3:** 본문 가이드 첫 줄이 frontmatter 직후 `# Power BI...`로 이어지는지, 부록 파일에 Mermaid/표가 깨지지 않았는지 `head -80`으로 샘플 확인

- [ ] **Step 4:** 커밋

```bash
git add scripts/split_power_bi_report.py src/content/studies/*.md
git commit -m "feat(studies): split Power BI report into four study entries"
```

---

### Task A4: Power BI 이미지를 `public/images/studies/{slug}/`에 복제

**Files:**
- Create under: `public/images/studies/20260420-power-bi-desktop-guide/*.png` (등 29개, 부록은 이미지 없을 수 있음)

- [ ] **Step 1:** 본문 가이드에 등장하는 파일명만 복사(스크립트로 추출 가능)

```bash
grep -oE '/paper_review/images/studies/20260420-power-bi-desktop-guide/[^)]+' \
  src/content/studies/20260420-power-bi-desktop-guide.md | sed 's|.*/||' | sort -u
```

- [ ] **Step 2:** 대상 디렉터리 생성 후 복사

```bash
mkdir -p public/images/studies/20260420-power-bi-desktop-guide
# 위 grep 결과 각 파일에 대해:
cp "report/img/power_bi/common.png" public/images/studies/20260420-power-bi-desktop-guide/
# (나머지 28개 동일 패턴; 한 줄 루프)
for f in $(grep -oE '20260420-power-bi-desktop-guide/[a-z0-9_]+\.png' src/content/studies/20260420-power-bi-desktop-guide.md | cut -d/ -f2 | sort -u); do
  cp "report/img/power_bi/$f" "public/images/studies/20260420-power-bi-desktop-guide/"
done
```

- [ ] **Step 3:** 부록 D/E에 `./img/` 참조가 남아 있으면 동일 slug로 복사하거나 split 스크립트에서 부록은 이미지 없음 확인

- [ ] **Step 4:** 커밋

```bash
git add public/images/studies/20260420-power-bi-desktop-guide
git commit -m "assets: add Power BI screenshots for desktop guide study"
```

---

### Task A5: `studies` 페이지 라우트 + `ReviewLayout` 확장

**Files:**
- Create: `src/pages/studies/[...slug].astro`
- Modify: `src/layouts/ReviewLayout.astro`

- [ ] **Step 1:** `ReviewLayout.astro`에 `listHref` 선택 prop 추가 — 기본값 `import.meta.env.BASE_URL`

```astro
---
import BaseLayout from './BaseLayout.astro';
import '../styles/common.css';

interface Props {
  title: string;
  originalTitle?: string;
  listHref?: string;
}

const { title, originalTitle, listHref = import.meta.env.BASE_URL } = Astro.props;
const description = originalTitle
  ? `${title} - ${originalTitle}`
  : title;
---

<BaseLayout title={title} description={description}>
  ...
  <nav class="top-nav">
    <a href={listHref}>&#8592; 목록으로</a>
  </nav>
  ...
```

- [ ] **Step 2:** `src/pages/studies/[...slug].astro` 생성 — `reviews`와 동일 패턴이나 `getCollection('studies')`, `listHref`에 `` `${import.meta.env.BASE_URL}?tab=studies` `` 전달

```astro
---
import { getCollection, render } from 'astro:content';
import ReviewLayout from '../../layouts/ReviewLayout.astro';

export async function getStaticPaths() {
  const entries = await getCollection('studies');
  return entries.map((entry) => ({
    params: { slug: entry.id },
    props: { entry },
  }));
}

const { entry } = Astro.props;
const { Content } = await render(entry);
const listHref = `${import.meta.env.BASE_URL}?tab=studies`;
const subtitle = entry.data.originalTitle ?? entry.data.topic;
---

<ReviewLayout
  title={entry.data.title}
  originalTitle={subtitle}
  listHref={listHref}
>
  <Content />
</ReviewLayout>
```

- [ ] **Step 3:** 빌드

```bash
npm run build
```

Expected: exit 0, `dist/studies/20260420-power-bi-desktop-guide/index.html` 존재

- [ ] **Step 4:** 커밋

```bash
git add src/layouts/ReviewLayout.astro src/pages/studies/[...slug].astro
git commit -m "feat(pages): add studies route and list link for studies tab"
```

---

### Task A6: EMNLP 추천 서베이 → `reviews` 배포

**Files:**
- Create: `src/content/reviews/20260416-a-survey-on-llm-powered-agents-for-recommender-systems.md`
- Create under: `public/images/reviews/20260416-a-survey-on-llm-powered-agents-for-recommender-systems/` (보고서가 참조하는 Figure/Table PNG만)

- [ ] **Step 1:** 슬러그 규칙: 파일 `report/20260416_report_a_survey_on_llm_powered_agents_for_recommender_systems.md` → `20260416-a-survey-on-llm-powered-agents-for-recommender-systems`

- [ ] **Step 2:** `src/content/reviews/20260416-a-survey-on-llm-powered-agents-for-recommender-systems.md` 상단에 YAML 추가 + 본문은 `report/...md`에서 복사하되, 이미지 경로를 `` `/paper_review/images/reviews/20260416-a-survey-on-llm-powered-agents-for-recommender-systems/Figure_1.png` `` 형식으로 통일

```yaml
---
title: "LLM 기반 에이전트 추천 시스템 서베이 -- 종합 분석 보고서"
originalTitle: "A Survey on LLM-powered Agents for Recommender Systems"
date: 2026-04-16
authors: "Qiyao Peng, Hongtao Liu, Hua Huang, Jian Yang, Qing Yang, Minglai Shao"
institution: "Tianjin University, Du Xiaoman Financial, Beihang University"
tags: ["recommender-systems", "LLM", "agents", "EMNLP-2025", "survey"]
description: "LLM 기반 에이전트를 추천 시스템에 적용하는 연구를 세 가지 패러다임과 4-모듈 아키텍처로 정리한 EMNLP 2025 Findings 서베이 분석이다."
topic: "Recommender systems"
---
```

- [ ] **Step 3:** `paper/Agentic_Ecosystems/Figure_1.png` 등을 위 public 경로로 복사

- [ ] **Step 4:** `npm run build` 성공 확인

- [ ] **Step 5:** 커밋

```bash
git add src/content/reviews/20260416-a-survey-on-llm-powered-agents-for-recommender-systems.md public/images/reviews/20260416-a-survey-on-llm-powered-agents-for-recommender-systems paper/Agentic_Ecosystems
git commit -m "feat(reviews): publish EMNLP survey on LLM agents for recommender systems"
```

---

### Task D1: `study_instruction.md` 신설

**Files:**
- Create: `study_instruction.md`

- [ ] **Step 1:** 최소 본문(예시 — 그대로 저장 가능)

```markdown
# 기술 학습(studies) 보고서 작성 가이드

## 저장 위치
- 원본 초안: `/report/` — 파일명 `YYYYMMDD_<topic_snake>.md` (예: `20260420_power_bi_report.md`)
- 사이트 배포: `src/content/studies/` — 슬러그 `YYYYMMDD-kebab-title.md`

## frontmatter (필수)
- title, date, description, tags, topic
- 선택: sources[], originalTitle, authors, institution

## 품질
- 본문 `##` 헤딩 3개 이상, 표 1개 이상, 참고 URL 1개 이상
- 이미지는 `/paper_review/images/studies/{slug}/...` 형식으로 배치한다.
```

- [ ] **Step 2:** 커밋

```bash
git add study_instruction.md
git commit -m "docs: add study_instruction for studies content"
```

---

### Task D2: `review_instruction.md` 수정

**Files:**
- Modify: `review_instruction.md`

- [ ] **Step 1:** 약 47행 근처 깨진 코드펜스 수정: `#### 1. 배경 및 문제 정의` 위의 예시 블록을 열고 닫는 ``` 쌍으로 맞춘다.

- [ ] **Step 2:** "수정 금지" 절을 스펙 §5.5에 맞게 개정 — `PaperSearch.tsx`, `index.astro`, `index.css`, `content.config.ts`, `pages/studies/`는 구현 시 수정 가능함을 명시.

- [ ] **Step 3:** `reviews`에 선택 필드 `topic` (관련 글용) 한 줄 추가

- [ ] **Step 4:** 커밋

```bash
git add review_instruction.md
git commit -m "docs: fix review_instruction fences and align with spec"
```

---

### Task D3: `scripts/lint_report.py` + pytest

**Files:**
- Create: `scripts/lint_report.py`
- Create: `scripts/test_lint_report.py`

- [ ] **Step 1:** `scripts/lint_report.py` CLI 사양

```text
python scripts/lint_report.py [--strict] --stage report|content --category reviews|studies PATH [PATH ...]
```

- `stage=content`: 파일이 `---`로 시작, YAML 파싱 성공, 카테고리별 필수 키 존재, `##` 개수, 표(파이프 테이블) 개수, mermaid(```mermaid) 개수, `[주석]`(reviews만), 이미지 `](...)` 상대·절대 경로를 `ROOT` 기준으로 존재 확인, `https?://` URL 1개 이상, 닫히지 않은 ``` 검사

- `stage=report`, `category=reviews`: 파일명 `^\d{8}_report_[a-z0-9_]+\.md$`, 본문에 `**원논문**`, `**저자**`, `**소속**`, `**출처**`, `**보고서 작성일**` 포함, `##` 7개 이상, 표 3+, mermaid 2+, `[주석]` 1+, URL, 이미지, fence

- `stage=report`, `category=studies`: 파일명 `^\d{8}_.+\.md$`, `##` 3+, 표 1+, URL, fence; frontmatter 없음 허용

- [ ] **Step 2:** 실패 시 stderr에 규칙 id와 메시지; `--strict`면 exit 1

- [ ] **Step 3:** `scripts/test_lint_report.py`에 최소 2 테스트

```python
# scripts/test_lint_report.py
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_lint_content_alto_passes():
    path = ROOT / "src/content/reviews/20260410-alto-adaptive-lora-tuning-and-orchestration.md"
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/lint_report.py"), "--strict", "--stage", "content", "--category", "reviews", str(path)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr


def test_lint_report_recommender_passes():
    path = ROOT / "report/20260416_report_a_survey_on_llm_powered_agents_for_recommender_systems.md"
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/lint_report.py"), "--strict", "--stage", "report", "--category", "reviews", str(path)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
```

- [ ] **Step 4:** 구현 후 실행

```bash
cd /Users/pollyoh/Documents/GitHub/paper_study
pytest scripts/test_lint_report.py -v
```

Expected: 전부 PASSED

- [ ] **Step 5:** 커밋

```bash
git add scripts/lint_report.py scripts/test_lint_report.py
git commit -m "feat(scripts): add report and content markdown linter"
```

---

### Task B1: `scripts/publish.py` (lint → 복사 → 경로 치환)

**Files:**
- Create: `scripts/publish.py`
- Create: `scripts/test_publish.py`

- [ ] **Step 1:** CLI 계약

```text
python scripts/publish.py --category reviews|studies [--dry-run] PATH/TO/report.md
```

- `reviews`: `lint_report.py --stage report` 통과 후, (a) 슬러그 = `{date}-{kebab(snake)}` where `YYYYMMDD_report_{snake}.md` (b) `src/content/reviews/{slug}.md`에 YAML 생성: `publish_reviews.build_frontmatter(text)`가 blockquote에서 원논문 등 파싱 (백틱 `<br>` 제거) + 본문은 첫 `#`부터 복사 (c) 이미지 `../paper/...` 또는 `./img` 패턴을 탐지해 `public/images/reviews/{slug}/`로 복사하고 경로를 `` `/paper_review/images/reviews/{slug}/...` `` 로 치환

- `studies`: v1에서는 **이미 `src/content/studies`에 존재하는 파일을 재복사하지 않고**, `report` 원본에서 split된 결과를 수동 유지한다고 가정하거나, `publish`는 `split_power_bi_report.py`를 서브프로세스 호출 옵션 `--split-power-bi`로만 처리 — **단순화:** `studies` 경로 인자는 `src/content/studies/*.md`만 받아 `lint_report.py --stage content --category studies` 후 종료(복사 없음). 실제 studies 생성은 A3 스크립트.

- 문서화: `study_instruction.md`에 "Power BI는 `split_power_bi_report.py` 후 이미지 복사(A4)" 명시

- [ ] **Step 2:** `scripts/test_publish.py`

```python
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]


def load_publish():
    path = ROOT / "scripts" / "publish.py"
    spec = importlib.util.spec_from_file_location("publish", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_slug_from_reviews_filename():
    pub = load_publish()
    assert pub.slug_from_reviews_report(
        "20260416_report_a_survey_on_llm_powered_agents_for_recommender_systems.md"
    ) == "20260416-a-survey-on-llm-powered-agents-for-recommender-systems"
```

- `publish.py`에 함수 `slug_from_reviews_report(filename: str) -> str` 노출

- [ ] **Step 3:** pytest

```bash
pytest scripts/test_publish.py scripts/test_lint_report.py -v
```

- [ ] **Step 4:** 커밋

```bash
git add scripts/publish.py scripts/test_publish.py
git commit -m "feat(scripts): add publish CLI with review slug helper"
```

---

### Task B2: CI — verify 워크플로

**Files:**
- Create: `.github/workflows/verify.yml`
- Modify: `.github/workflows/deploy-pages.yml`

- [ ] **Step 1:** `.github/workflows/verify.yml`

```yaml
name: Verify

on:
  pull_request:
  push:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - name: Install Node deps
        run: npm ci
      - name: Lint published markdown
        run: |
          set -e
          shopt -s nullglob
          rev=(src/content/reviews/*.md)
          st=(src/content/studies/*.md)
          python scripts/lint_report.py --strict --stage content --category reviews "${rev[@]}"
          python scripts/lint_report.py --strict --stage content --category studies "${st[@]}"
        shell: bash
      - name: Astro build
        run: npm run build
```

- [ ] **Step 2:** `deploy-pages.yml`의 `build` job을 `verify`와 동일 단계로 바꾸거나 `needs: []` 유지 시 중복이므로, **배포 워크플로에서 빌드 job 이름을 `verify`로 맞추고** artifact upload 전 동일 스텝 실행(단일 workflow 유지)하는 편이 간단하다. 권장: `deploy-pages.yml`에 lint 스텝을 `npm ci`와 `npm run build` 사이에 삽입.

```yaml
      - run: npm ci
      - name: Lint content markdown
        run: |
          set -e
          shopt -s nullglob
          rev=(src/content/reviews/*.md)
          st=(src/content/studies/*.md)
          python scripts/lint_report.py --strict --stage content --category reviews "${rev[@]}"
          python scripts/lint_report.py --strict --stage content --category studies "${st[@]}"
        shell: bash
      - run: npm run build
```

- [ ] **Step 3:** PR에서 워크플로 문법 검증(로컬 act 없이)은 push 후 GitHub에서 확인

- [ ] **Step 4:** 커밋

```bash
git add .github/workflows/deploy-pages.yml .github/workflows/verify.yml
git commit -m "ci: lint markdown and verify astro build"
```

(verify.yml만 쓰고 deploy는 손대지 않을 경우, PR은 verify만 통과하면 되고 main 배포는 deploy에 lint 삽입 필요)

---

### Task C1: `relatedPosts` 유틸

**Files:**
- Create: `src/lib/relatedPosts.ts`

- [ ] **Step 1:** 아래 파일 전체 추가

```typescript
import type { CollectionEntry } from 'astro:content';

export type AnyPost =
  | CollectionEntry<'reviews'>
  | CollectionEntry<'studies'>;

function tagOverlap(a: string[], b: string[]): number {
  const sb = new Set(b);
  return a.filter((t) => sb.has(t)).length;
}

export function getRelated(
  current: AnyPost,
  reviews: CollectionEntry<'reviews'>[],
  studies: CollectionEntry<'studies'>[],
  limit = 3,
): { href: string; title: string; collection: 'reviews' | 'studies' }[] {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const scored = [...reviews, ...studies]
    .filter((e) => !(e.id === current.id && e.collection === current.collection))
    .map((e) => {
      let score = 0;
      const ct = current.data.topic;
      const et = e.data.topic;
      if (ct && et && ct === et) score += 100;
      score += 10 * tagOverlap(current.data.tags, e.data.tags);
      score += e.data.date.getTime() / 1e12;
      const href =
        e.collection === 'reviews'
          ? `${base}/reviews/${e.id}/`
          : `${base}/studies/${e.id}/`;
      return { href, title: e.data.title, collection: e.collection, score };
    });
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, limit).map(({ href, title, collection }) => ({
    href,
    title,
    collection,
  }));
}
```

- [ ] **Step 2:** Typecheck는 `npm run build`에 포함

- [ ] **Step 3:** 커밋

```bash
git add src/lib/relatedPosts.ts
git commit -m "feat: add related posts helper for reviews and studies"
```

---

### Task C2: 리뷰·스터디 페이지에 관련 글 + 목록 링크

**Files:**
- Modify: `src/pages/reviews/[...slug].astro`
- Modify: `src/pages/studies/[...slug].astro`
- Modify: `src/layouts/ReviewLayout.astro` (슬롯 `related` 추가가 가장 깔끔 — 아래 참고)

`ReviewLayout`에 `<slot name="related" />`를 `</div>` 직전에 추가하고, 각 slug 페이지에서:

```astro
---
import { getCollection, render } from 'astro:content';
import ReviewLayout from '../../layouts/ReviewLayout.astro';
import { getRelated } from '../../lib/relatedPosts';

// ... getStaticPaths 동일
const allReviews = await getCollection('reviews');
const allStudies = await getCollection('studies');
const related = getRelated(entry, allReviews, allStudies);
const listHref = `${import.meta.env.BASE_URL}?tab=reviews`;
---
<ReviewLayout title={...} originalTitle={...} listHref={listHref}>
  <Content />
  <div slot="related" class="related-posts-wrap">
    {related.length > 0 && (
      <section class="related-posts" aria-labelledby="related-heading">
        <h2 id="related-heading">관련 글</h2>
        <ul>
          {related.map((r) => (
            <li>
              <a href={r.href}>{r.title}</a>
              <span class="related-badge">{r.collection === 'reviews' ? '논문' : '기술'}</span>
            </li>
          ))}
        </ul>
      </section>
    )}
  </div>
</ReviewLayout>
```

- [ ] **Step 1:** `ReviewLayout.astro`에 `<slot name="related" />` 추가 및 `related-posts`용 최소 CSS는 `common.css` 수정 대신 **인라인 style은 피하고**, `index.css`가 아닌 `common.css`에 소량 추가가 필요하면 스펙 예외로 `common.css` 끝에 `.related-posts` 블록 추가(스펙은 "필요 최소" 허용).

- [ ] **Step 2:** `npm run build`

- [ ] **Step 3:** 커밋

```bash
git add src/pages/reviews/[...slug].astro src/pages/studies/[...slug].astro src/layouts/ReviewLayout.astro src/styles/common.css
git commit -m "feat: show related posts on review and study pages"
```

---

### Task C3: 메인 브랜딩 + `PaperSearch` 탭·배지·통합 목록

**Files:**
- Modify: `src/pages/index.astro`
- Modify: `src/components/PaperSearch.tsx`
- Modify: `src/styles/index.css`
- Modify: `src/layouts/BaseLayout.astro`

- [ ] **Step 1:** `BaseLayout.astro` 기본 description 문자열을 `seunghee's Archive — 논문 리뷰와 기술 학습 정리` 로 변경

- [ ] **Step 2:** `index.astro`에서

```typescript
const reviewEntries = await getCollection('reviews');
const studyEntries = await getCollection('studies');
const papers = [
  ...reviewEntries.map((e) => ({ kind: 'reviews' as const, ... })),
  ...studyEntries.map((e) => ({ kind: 'studies' as const, ... })),
].sort((a, b) => b.date.localeCompare(a.date));
```

- 각 항목에 `hrefBase`: reviews면 `/reviews/`, studies면 `/studies/`, `cardLine2`: studies는 `originalTitle ?? topic`, `cardLine3`: `authors` + institution

- [ ] **Step 3:** `PaperSearch.tsx` props 확장

```typescript
type PaperKind = 'reviews' | 'studies';

interface Paper {
  kind: PaperKind;
  slug: string;
  href: string;
  title: string;
  subtitle: string;
  metaLine: string;
  tags: string[];
  description: string;
}
```

- 탭: `전체 | 논문 | 기술공부`, `useEffect`로 `URLSearchParams` 읽고 `tab=` 동기화

- 카드 상단 배지: `kind === 'reviews' ? '논문' : '기술공부'`

- [ ] **Step 4:** `index.css`에 `.content-tabs`, `.kind-badge` 스타일 추가(기존 톤 맞춤)

- [ ] **Step 5:** `npm run build` 후 `npm run preview`로 수동 확인

- [ ] **Step 6:** 커밋

```bash
git add src/pages/index.astro src/components/PaperSearch.tsx src/styles/index.css src/layouts/BaseLayout.astro
git commit -m "feat(ui): archive branding, tabs, and unified card grid"
```

---

### Task C4: `index.astro` 푸터 연도·제목 문자열

**Files:**
- Modify: `src/pages/index.astro`

- [ ] **Step 1:** `<h1>seunghee's Archive</h1>`, `<p>논문 리뷰와 기술 학습 정리</p>`, footer `© 2026`

- [ ] **Step 2:** 커밋

```bash
git add src/pages/index.astro
git commit -m "chore: update landing title and footer year"
```

---

## 스펙 대비 자체 점검

| 스펙 절 | 담당 Task |
|---------|-----------|
| §2.1 두 컬렉션·슬러그 | A2, A5, A6 |
| §2.2 studies 스키마 + C4 선택 필드 | A2, A3 frontmatter |
| §2.3 gitignore·자산 | A1, A4, A6 |
| §2.4 Power BI 4분할 | A3, A4 |
| §2.5 라우트 | A5 |
| §3 lint L2 | D3, B2 |
| §3.1 가이드 | D1, D2 |
| §4 publish + CI | B1, B2 |
| §5 C1~C5, §5.1 브랜딩 | C3, C4, BaseLayout |
| §5.5 코드 수정 허용 | D2, C2/C3에서 명시 반영 |
| §7 성공 기준 | 전 Task 빌드·pytest·CI |

**Placeholder 스캔:** 본 플랜에 TBD 없음. `publish.py`의 studies 분기는 "content lint만"으로 범위를 한정해 모호성 제거.

---

## 실행 위임

플랜을 `docs/superpowers/plans/2026-04-22-content-collections-pipeline-ux.md`에 저장했다.

**실행 방식 선택:**

1. **Subagent-Driven (권장)** — 태스크마다 새 서브에이전트, 태스크 사이 리뷰, 빠른 반복. **필수 서브스킬:** `superpowers:subagent-driven-development`

2. **Inline Execution** — 이 세션에서 `superpowers:executing-plans`로 체크포인트마다 일괄 실행

어느 쪽으로 진행할지 알려주면 그다음부터 해당 방식으로 구현을 시작한다.
