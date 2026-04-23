# Paper Study (seunghee's Archive)

읽은 논문 분석 보고서와 기술 학습 정리를 마크다운으로 작성하고, **Astro 정적 사이트**로 빌드해 GitHub Pages에 공개하는 저장소입니다.

**배포 사이트**: [https://pollyoh.github.io/paper_review/](https://pollyoh.github.io/paper_review/)

`astro.config.mjs`에서 `site`는 `https://pollyoh.github.io`, `base`는 `/paper_review`로 설정되어 있어, 마크다운·내부 링크·이미지 URL은 이 base와 맞출 필요가 있습니다.

## 기술 스택

- **Astro 6** (`output: 'static'`), **React** (홈 검색 UI `PaperSearch`)
- 마크다운: **remark-math** / **rehype-katex**, 코드 하이라이트에 **Mermaid** 변환 (`src/plugins/rehype-mermaid.mjs`)
- **Python 3.12**: `scripts/lint_report.py` 등 (개발 의존성은 `requirements-dev.txt`)

## 디렉터리 구조

```
src/
  content/
    reviews/          # 배포용 논문 리뷰 (YAML frontmatter + 본문)
    studies/          # 배포용 학습·레퍼런스 글 (동일)
  layouts/            # BaseLayout, ReviewLayout
  pages/              # index, reviews/[...slug], studies/[...slug]
  components/         # PaperSearch 등
  styles/
  plugins/
public/
  images/
    reviews/{slug}/   # 리뷰용 이미지 (URL은 /paper_review/images/reviews/...)
    studies/{slug}/   # studies용 이미지
report/               # 초안 보고서 (frontmatter 없음, review_instruction.md 규칙)
paper/                # 원본 논문 PDF 등
scripts/              # publish, lint, Power BI 분할 등 — 상세는 scripts/README.md
.github/workflows/
  verify.yml          # PR·main: lint + npm run build
  deploy-pages.yml    # main: 위 검증 후 dist → GitHub Pages
review_instruction.md # 리뷰 보고서(report/) 작성 가이드
study_instruction.md  # studies 콘텐츠·경로 규칙
```

루트의 `docs/`에는 예전 정적 HTML 샘플과 내부 설계 메모가 일부 남아 있으며, **현재 Pages 배포 산출물은 `npm run build` 결과인 `dist/`**입니다.

## 로컬 개발

```bash
npm ci
npm run dev      # http://localhost:4321/paper_review/ (base 경로 포함)
npm run build
npm run preview  # 빌드 결과 미리보기
```

마크다운 린트는 Python 가상환경에서 실행합니다.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/lint_report.py --help
```

CI와 동일하게 전체 콘텐츠를 검사하려면:

```bash
shopt -s nullglob
rev=(src/content/reviews/*.md)
st=(src/content/studies/*.md)
.venv/bin/python scripts/lint_report.py --strict --stage content --category reviews "${rev[@]}"
.venv/bin/python scripts/lint_report.py --strict --stage content --category studies "${st[@]}"
npm run build
```

## 콘텐츠 추가 흐름

1. **논문 리뷰**: `review_instruction.md`에 따라 `report/YYYYMMDD_report_{snake_case}.md` 초안 작성.
2. **배포본 생성**: `scripts/publish.py`로 `src/content/reviews/{YYYYMMDD-kebab}.md` 생성 및 이미지 복사·경로 정리. `--description`, `--tags`(JSON 배열)가 필요합니다. 자세한 CLI는 `python3 scripts/publish.py --help` 또는 `scripts/README.md` 참고.
3. **Studies (예: Power BI 분할)**: `scripts/split_power_bi_report.py` 등으로 `src/content/studies/`에 쓰고, `study_instruction.md`의 경로 규칙을 따릅니다.
4. `main`에 푸시하면 **Verify** 워크플로가 린트·빌드를 돌리고, **Deploy**가 통과한 빌드를 Pages에 올립니다.

스키마는 `src/content.config.ts`의 **reviews** / **studies** 컬렉션 정의를 따릅니다.

## 공개된 글 목록

### Reviews (논문)

| 날짜 | 제목 (한글) | 원논문 |
|------|-------------|--------|
| 2026-04-16 | LLM 기반 에이전트 추천 시스템 서베이 -- 종합 분석 보고서 | A Survey on LLM-powered Agents for Recommender Systems |
| 2026-04-14 | (Mis)alignment의 기술: 파인튜닝 방법이 LLM의 안전 정렬을 해제하고 복구하는 메커니즘 -- 종합 분석 보고서 | The Art of (Mis)alignment: How Fine-Tuning Methods Effectively Misalign and Realign LLMs in Post-Training |
| 2026-04-10 | ALTO: 이기종 LoRA 학습 워크로드를 위한 적응적 튜닝 및 오케스트레이션 -- 종합 분석 보고서 | ALTO: Adaptive LoRA Tuning and Orchestration for Heterogeneous LoRA Training Workloads |
| 2025-04-09 | LLM 생성 피어리뷰 탐지: 종합 분석 보고서 | Detecting LLM-Generated Peer Reviews |

### Studies

| 날짜 | 제목 |
|------|------|
| 2026-04-20 | Power BI Desktop 기능·DAX·M 통합 리포트 (본문) |
| 2026-04-20 | Power BI — DAX 함수 레퍼런스 (부록 D) |
| 2026-04-20 | Power BI — Power Query M 레퍼런스 (부록 E) |
| 2026-04-20 | Power BI 보고서 검토 체크리스트 (부록 F) |
