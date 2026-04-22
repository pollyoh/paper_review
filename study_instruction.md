# 기술 학습(studies) 보고서 작성 가이드

## 역할

- `studies`는 논문 리뷰(`reviews`)와 분리된 **도구·플랫폼·개념 학습 정리**용 콘텐츠이다.
- 사이트 경로: `/paper_review/studies/{slug}/` (저장소: `src/content/studies/{slug}.md`)

## 원본 초안

- 디렉터리: `/report/`
- 파일명: `YYYYMMDD_<설명_snake>.md` 권장. `_report_` 문자열이 포함될 수 있다(예: `20260420_power_bi_report.md`).

## 배포용 마크다운 (`src/content/studies/`)

- 슬러그: `YYYYMMDD-kebab-case-title.md` (논문 리뷰와 동일 규칙)
- **필수 frontmatter**: `title`, `date`, `description`, `tags`, `topic`
- **선택**: `sources` (`title` + `url` 목록), `originalTitle`, `authors`, `institution` (카드 두 번째·세 번째 줄용)

## 품질 (lint `content` + `studies` 기준)

- 본문에 마크다운 헤딩(`##`–`######`) **합계 10개 이상** (부록·레퍼런스는 `####`가 많을 수 있음)
- 파이프(`|`)를 사용한 **표 1개 이상**, 또는 자동 생성 부록처럼 **본문이 매우 긴** 경우(8000자 초과) 표 없이 통과할 수 있다(lint 규칙과 동일).
- 본문 어디에든 `http://` 또는 `https://` URL **1개 이상**
- 이미지를 쓰는 경우, 참조 경로의 파일이 저장소에 존재해야 한다.

## Power BI 시리즈

- 단일 원본 `report/20260420_power_bi_report.md`는 소스 오브 트루스로 유지한다.
- 사이트용 4편은 `python3 scripts/split_power_bi_report.py`로 재생성한다.
- 스크린샷은 `public/images/studies/20260420-power-bi-desktop-guide/` 등에 두고, 마크다운에서는 `` `/paper_review/images/studies/{slug}/파일명.png` `` 형식을 쓴다.
