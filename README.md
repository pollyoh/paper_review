# Paper Review

읽은 논문에 대한 종합 분석 보고서를 작성하고 웹 페이지로 공개하는 저장소입니다.

**Site**: https://pollyoh.github.io/paper_review/

## 구조

```
docs/                  # GitHub Pages 배포 대상
  index.html           # 랜딩 페이지 (논문 카탈로그)
  papers.json          # 논문 메타데이터 레지스트리
  css/common.css       # 공통 스타일
  js/common.js         # 공통 JS (Mermaid, TOC, 주석 접기 등)
  reviews/             # 개별 리뷰 페이지
    YYYYMMDD-slug/
      index.html
paper/                 # 원본 논문 PDF
report/                # 리뷰 보고서 원본 (md, html, pdf)
review_instruction.md  # 리뷰 작성 가이드
```

## 새 리뷰 추가 방법

1. `docs/reviews/YYYYMMDD-slug/index.html` 생성 (공통 CSS/JS 참조)
2. `docs/papers.json`에 메타데이터 항목 추가
3. `main` 브랜치에 push하면 GitHub Actions가 자동 배포

## 리뷰 목록

| 날짜 | 제목 | 원논문 |
|------|------|--------|
| 2025.04.09 | LLM 생성 피어리뷰 탐지: 종합 분석 보고서 | Detecting LLM-Generated Peer Reviews |
