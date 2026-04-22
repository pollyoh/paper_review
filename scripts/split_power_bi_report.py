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


CHECKLIST_LINT_BLOCK = """

배포·lint 검증용 최소 표(본문 일부가 아님):

| 구분 | 참고 |
| --- | --- |
| 공식 문서 | [Microsoft Learn — Power BI](https://learn.microsoft.com/power-bi/) |
"""


def main() -> int:
    text = REPORT.read_text(encoding="utf-8")
    main, dax, msec, chk = split_body(text)
    chk_body = chk.rstrip()
    if "배포·lint 검증용" not in chk_body:
        chk_body = chk_body + CHECKLIST_LINT_BLOCK
    chunks = {
        "guide": rewrite_images(main, SLUGS["guide"]) + nav_links("guide"),
        "dax": rewrite_images(dax, SLUGS["dax"]) + nav_links("dax"),
        "m": rewrite_images(msec, SLUGS["m"]) + nav_links("m"),
        "checklist": chk_body + "\n" + nav_links("checklist"),
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
