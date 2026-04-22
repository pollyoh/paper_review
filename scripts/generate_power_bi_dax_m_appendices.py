#!/usr/bin/env python3
"""Generate DAX and M function appendix markdown for Power BI report.

The DAX appendix follows a teaching layout:

- D.0 Orientation: sample model, filter/row context, CALCULATE primer.
- D.1 In-depth examples for ~100 commonly used functions with sample input,
  DAX code, and expected output.
- D.2 Category index listing every remaining function (one-line description
  and Learn link) so no function from dax.guide is dropped.

The M appendix keeps its previous generated format (heuristic display names
plus Learn/PowerQuery.how links).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from dax_catalog import CATEGORY, CATEGORY_ORDER, DETAILED  # noqa: E402

DAX_SLUGS = ROOT / ".tmp_dax_sitemap.xml"
M_SLUGS = ROOT / ".tmp_pq_core_slugs.txt"
OUT_DAX = ROOT / "report" / "_generated_dax_appendix.md"
OUT_M = ROOT / "report" / "_generated_m_appendix.md"


def parse_dax_slugs() -> list[str]:
    xml = DAX_SLUGS.read_text(encoding="utf-8")
    urls = re.findall(r"<loc>(https://dax\.guide/[^<]+)</loc>", xml)
    slugs: list[str] = []
    for u in urls:
        s = u.replace("https://dax.guide/", "").strip("/")
        # dax.guide uses slug "index" for INDEX(); do not exclude site home "index" (not in sitemap as function url)
        if s.startswith("info-") or s in ("", "dax-function-reference"):
            continue
        slugs.append(s)
    return sorted(set(slugs))


def parse_m_slugs() -> list[str]:
    if not M_SLUGS.exists():
        return []
    lines = [ln.strip() for ln in M_SLUGS.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return sorted(set(lines))


def dax_learn_url(slug: str) -> str:
    return f"https://learn.microsoft.com/en-us/dax/{slug}-function-dax"


def m_learn_url(slug: str) -> str:
    return f"https://learn.microsoft.com/en-us/powerquery-m/{slug}"


def dax_display_name(slug: str) -> str:
    """Map dax.guide slug to DAX identifier (Learn URL uses same slug)."""
    parts = slug.split("-")
    return ".".join(p.upper() for p in parts)


# Longest-first subwords for M camelCase reconstruction (lowercase segments).
_M_SUBWORDS = sorted(
    {
        "allow",
        "deny",
        "binaryoccurrence",
        "binaryencoding",
        "binaryformat",
        "buffermode",
        "combiner",
        "access",
        "control",
        "kind",
        "currency",
        "culture",
        "diagnostics",
        "metadata",
        "schedule",
        "nullable",
        "sectionmember",
        "replacer",
        "splitter",
        "comparer",
        "approximatelength",
        "signedinteger",
        "unsignedinteger",
        "transformcolumntypes",
        "columnsoftype",
        "combinecolumns",
        "addindexcolumn",
        "addrankcolumn",
        "alternaterows",
        "viewfunction",
        "infercontenttype",
        "fromlist",
        "fromtext",
        "tolist",
        "totext",
        "viewerror",
        "signedinteger16",
        "signedinteger32",
        "signedinteger64",
        "unsignedinteger16",
        "unsignedinteger32",
        "unsignedinteger64",
        "7bitencodedsignedinteger",
        "7bitencodedunsignedinteger",
        "combinetextbydelimiter",
        "combinetextbyeachdelimiter",
        "combinetextbylengths",
        "combinetextbypositions",
        "combinetextbyranges",
        "witherrorcontext",
        "donothing",
        "column",
        "columns",
        "buffer",
        "combine",
        "distinct",
        "partition",
        "transform",
        "promote",
        "demote",
        "headers",
        "index",
        "rank",
        "rows",
        "table",
        "record",
        "values",
        "fields",
        "items",
        "keys",
        "names",
        "types",
        "group",
        "sort",
        "order",
        "skip",
        "select",
        "remove",
        "replace",
        "merge",
        "split",
        "first",
        "last",
        "single",
        "from",
        "text",
        "length",
        "view",
        "error",
        "null",
        "true",
        "false",
        "type",
        "list",
        "add",
        "row",
        "key",
        "name",
        "value",
        "field",
        "item",
        "range",
        "each",
        "any",
        "contains",
        "position",
        "positions",
        "delimiter",
        "ranges",
        "lengths",
        "binary",
        "format",
        "encoding",
        "occurrence",
        "optional",
        "repeating",
        "required",
        "littleendian",
        "bigendian",
        "byteorder",
        "character",
        "number",
        "tonumber",
        "fromnumber",
    },
    key=len,
    reverse=True,
)


def _m_tokenize_body(s: str) -> list[str]:
    """Greedy longest-match tokenization for lowercase concatenated body."""
    out: list[str] = []
    i = 0
    while i < len(s):
        matched = False
        for w in _M_SUBWORDS:
            if s.startswith(w, i):
                out.append(w)
                i += len(w)
                matched = True
                break
        if not matched:
            out.append(s[i:])
            break
    return [t for t in out if t]


def _pascal_from_lower(s: str) -> str:
    tokens = _m_tokenize_body(s.replace("-", ""))
    if not tokens:
        return s[:1].upper() + s[1:] if s else s
    return "".join(t[:1].upper() + t[1:] for t in tokens)


def m_display_name(slug: str) -> str:
    """Namespace + PascalCase body from hyphen slug (heuristic)."""
    parts = slug.split("-", 1)
    if len(parts) == 1:
        return _pascal_from_lower(parts[0])
    ns = _pascal_from_lower(parts[0])
    rest = parts[1].replace("-", "")
    tokens = _m_tokenize_body(rest)
    if not tokens:
        body = "".join(p[:1].upper() + p[1:] for p in parts[1].split("-") if p)
    else:
        body = "".join(t[:1].upper() + t[1:] for t in tokens)
    return f"{ns}.{body}"


_DAX_PREAMBLE = """
## 부록 D: DAX 함수 레퍼런스

이 부록은 **읽고 바로 따라 할 수 있도록** 다음 순서로 구성한다.

1. **D.0 기초 개념과 샘플 모델** — 모든 예제에서 공통으로 쓰는 테이블(`Sales`, `'Date'`, `Product`, `Customer`)과 필터·행 컨텍스트, `CALCULATE`의 역할을 설명한다.
2. **D.1 실무 중심 심층 예제** — 가장 자주 쓰이는 약 140개 함수를 **시그니처 → 의미 → 입력 → DAX 식 → 결과**로 보여 준다.
3. **D.2 카테고리별 전 함수 색인** — dax.guide 사이트맵에서 확인한 DAX 함수 전수를 카테고리별로 나눠 한 줄 설명 + Microsoft Learn·DAX Guide 링크로 정리한다. 심층 예제에 포함된 함수도 색인에 함께 실어 완결성을 유지한다.

### D.0 기초 개념과 샘플 모델

**샘플 모델(예제에서 공통 사용)**:

| 테이블 | 주요 열 | 관계 |
| --- | --- | --- |
| `Sales` | `OrderId`, `OrderDate`, `ShipDate`, `CustomerId`, `ProductId`, `Qty`, `UnitPrice`, `Amount`(= Qty×UnitPrice), `Note` | `Sales[CustomerId] → Customer[Id]`, `Sales[ProductId] → Product[Id]`, `Sales[OrderDate] → 'Date'[Date]` |
| `'Date'` | `Date`, `Year`, `Quarter`, `Month`, `MonthName`, `DayOfWeek` | 날짜 테이블로 표시 |
| `Customer` | `Id`, `Name`, `Country`, `Email` | |
| `Product` | `Id`, `Name`, `Category`, `Color`, `Cost` | |

**샘플 데이터 일부**:

```
Sales
OrderId | OrderDate   | CustomerId | ProductId | Qty | UnitPrice | Amount
1001    | 2026-01-03  | C001       | P001      | 2   | 100       | 200
1002    | 2026-01-05  | C002       | P002      |10   |  20       | 200
1003    | 2026-02-11  | C001       | P003      | 1   | 500       | 500
1004    | 2026-03-02  | C003       | P001      | 5   | 100       | 500
```

**필터 컨텍스트(Filter context)**: 보고서 시각화의 축·슬라이서·페이지 필터로 만들어지는 **WHERE 조건 모음**. 측정값이 평가될 때 이 조건으로 테이블이 먼저 걸러진다.

**행 컨텍스트(Row context)**: 계산 열과 `SUMX`·`FILTER` 같은 **행 반복 함수(iterator)** 내부에서만 존재한다. 행 하나를 가리키고, 그 행의 열 값을 식에서 직접 참조할 수 있다. 행 컨텍스트에서 다른 테이블 열을 보려면 `RELATED`가 필요하다.

**CALCULATE**: 필터 컨텍스트를 **수정하고** 식을 다시 평가한다. 인수로 주어지는 열=값 형태의 조건은 내부적으로 `FILTER(ALL(<table>), ...)`로 해석된다. `CALCULATE` 호출은 동시에 **행 컨텍스트 → 필터 컨텍스트 전환**을 수행하므로, 계산 열 내부에서 측정값을 호출하면 자동으로 `CALCULATE`로 감싸는 효과가 난다.

**VAR / RETURN**: 중간 결과를 변수에 담아 **한 번만 평가**하고 재사용한다. 가독성·성능 모두에서 권장.

```
[Profit Margin] =
VAR _sales = SUM(Sales[Amount])
VAR _cost = SUMX(Sales, Sales[Qty] * RELATED(Product[Cost]))
RETURN DIVIDE(_sales - _cost, _sales)
```

이 절의 모든 예제는 위 샘플 모델을 전제로 한다. `[측정값]` 대괄호 표기는 측정값 이름을 의미하며 테이블 참조가 생략된 형태이다.
"""


def _render_example(slug: str, ex: dict) -> list[str]:
    """Render one detailed example entry as markdown lines."""
    name = dax_display_name(slug)
    learn = dax_learn_url(slug)
    out: list[str] = [f"##### {name}", ""]
    if ex.get("sig"):
        out.append(f"- **시그니처**: `{ex['sig']}`")
    if ex.get("summary"):
        out.append(f"- **의미**: {ex['summary']}")
    if ex.get("ctx"):
        out.append(f"- **필요 컨텍스트**: {ex['ctx']}")
    if ex.get("data"):
        out.append(f"- **입력 예**: {ex['data']}")
    if ex.get("code"):
        out.append("- **DAX 식**:")
        out.append("")
        code_lines = ex["code"].splitlines() or [ex["code"]]
        out.append("    ```DAX")
        for line in code_lines:
            out.append(f"    {line}")
        out.append("    ```")
        out.append("")
    if ex.get("output"):
        out.append(f"- **결과**: {ex['output']}")
    if ex.get("note"):
        out.append(f"- **주의**: {ex['note']}")
    out.append(
        f"- **참고**: [Microsoft Learn]({learn}) · [DAX Guide](https://dax.guide/{slug}/)"
    )
    out.append("")
    return out


def _classify(slug: str) -> str:
    if slug in CATEGORY:
        return CATEGORY[slug]
    # Heuristic fallback by common prefixes
    if slug.startswith("is"):
        return "정보(Information)"
    if slug.startswith(("date", "time")):
        return "날짜·시간(Date & Time)"
    if slug.startswith("path"):
        return "부모-자식(Parent-Child)"
    if slug.startswith("rollup"):
        return "테이블(Table)"
    return "기타(Other)"


def _index_summary(slug: str) -> str:
    """Short human line for a function that lacks a detailed example."""
    name = dax_display_name(slug)
    category = _classify(slug)
    # Reuse summary from DETAILED if present
    if slug in DETAILED and DETAILED[slug].get("summary"):
        return DETAILED[slug]["summary"]
    generic = {
        "집계(Aggregation)": f"{name} 집계 함수. 숫자 열/식을 대상으로 값을 계산한다.",
        "논리(Logical)": f"{name} 논리 연산자/함수. TRUE·FALSE·BLANK 중 하나를 돌려준다.",
        "필터(Filter)": f"{name} 필터 함수. `CALCULATE` 등과 조합해 현재 컨텍스트를 수정하거나 조회한다.",
        "관계(Relationships)": f"{name} 관계 탐색 함수. 행 컨텍스트에서 연결된 테이블 값을 읽는다.",
        "테이블(Table)": f"{name} 테이블 조작 함수. 계산 테이블·계산 쿼리에서 표를 변형한다.",
        "시간 인텔리전스(Time Intelligence)": f"{name} 시간 인텔리전스 함수. 날짜 테이블이 표시되어 있어야 동작한다.",
        "날짜·시간(Date & Time)": f"{name} 날짜/시간 조작 함수. 스칼라 날짜 값을 다룬다.",
        "텍스트(Text)": f"{name} 문자열 조작 함수.",
        "수학·삼각(Math & Trig)": f"{name} 수학 또는 삼각 함수. 대부분 스칼라 숫자를 받는다.",
        "통계(Statistical)": f"{name} 통계·분포 함수. 확률·분포·적합 계산에 쓴다.",
        "정보(Information)": f"{name} 정보 함수. 값의 형식·상태·환경을 검사한다.",
        "재무(Financial)": f"{name} 재무 함수. Excel 계열 재무 공식과 동일한 모델.",
        "부모-자식(Parent-Child)": f"{name} 부모-자식 경로 함수. 관계 대신 경로 문자열로 계층을 표현한다.",
        "기타(Other)": f"{name} 함수. 세부 동작은 Learn 문서를 따른다.",
    }
    return generic.get(category, generic["기타(Other)"])


def write_dax(slugs: list[str]) -> None:
    lines: list[str] = [
        "<!-- annotation: DAX appendix generated by scripts/generate_power_bi_dax_m_appendices.py -->",
    ]
    lines.append(_DAX_PREAMBLE.rstrip())
    lines.append("")

    # ---- D.1 detailed examples, grouped by category ----
    lines.append("### D.1 실무 중심 심층 예제")
    lines.append("")
    lines.append(
        "카테고리 순서대로 가장 자주 쓰이는 함수를 **시그니처 → 의미 → 입력 → DAX 식 → 결과** 형식으로 정리했다. 예제는 D.0의 샘플 모델을 전제로 한다."
    )
    lines.append("")

    by_cat_detailed: dict[str, list[str]] = {c: [] for c in CATEGORY_ORDER}
    for slug in DETAILED:
        cat = _classify(slug)
        by_cat_detailed.setdefault(cat, []).append(slug)

    for cat in CATEGORY_ORDER:
        items = sorted(by_cat_detailed.get(cat, []), key=dax_display_name)
        if not items:
            continue
        lines.append(f"#### 분류: {cat}")
        lines.append("")
        for slug in items:
            lines.extend(_render_example(slug, DETAILED[slug]))

    # ---- D.2 category index over every slug (full coverage) ----
    lines.append("### D.2 카테고리별 전 함수 색인")
    lines.append("")
    lines.append(
        "dax.guide 사이트맵에서 확인한 DAX 함수 전수를 카테고리별로 나눠 한 줄 설명과 공식 문서 링크로 정리한다. 심층 예제가 있는 함수는 표제 옆에 **(D.1 예제 있음)**이라고 덧붙인다."
    )
    lines.append("")

    by_cat_all: dict[str, list[str]] = {c: [] for c in CATEGORY_ORDER}
    for slug in slugs:
        by_cat_all.setdefault(_classify(slug), []).append(slug)

    for cat in CATEGORY_ORDER:
        items = sorted(by_cat_all.get(cat, []), key=dax_display_name)
        if not items:
            continue
        lines.append(f"#### {cat} ({len(items)}개)")
        lines.append("")
        for slug in items:
            name = dax_display_name(slug)
            learn = dax_learn_url(slug)
            tag = " **(D.1 예제 있음)**" if slug in DETAILED else ""
            summary = _index_summary(slug)
            lines.append(
                f"- **{name}**{tag} — {summary} [Learn]({learn}) · [DAX Guide](https://dax.guide/{slug}/)"
            )
        lines.append("")

    lines.append(
        f"_총 {len(slugs)}개 DAX 함수 색인(그 중 {len(DETAILED)}개는 D.1 심층 예제를 제공)._"
    )
    lines.append("")
    OUT_DAX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_m(slugs: list[str]) -> None:
    lines: list[str] = [
        "<!-- annotation: M appendix generated by scripts/generate_power_bi_dax_m_appendices.py -->",
        "",
        "## 부록 E: Power Query M 함수 레퍼런스(자동 생성 목록)",
        "",
        "각 항목의 Learn URL은 `https://learn.microsoft.com/en-us/powerquery-m/{slug}` 형식이다. 표시명은 슬러그를 토큰 사전으로 나눈 **가독용 추정 라벨**이며, 고급 편집기에서의 정확한 식·대소문자는 Learn 페이지를 따른다.",
        "",
    ]
    for slug in slugs:
        name = m_display_name(slug)
        learn = m_learn_url(slug)
        lines.append(f"### {name}")
        lines.append("")
        lines.append(
            "- **의미**: Power Query M 엔진이 제공하는 식별자(함수·형·열거형 등)로, 쿼리 단계의 논리를 표현한다."
        )
        lines.append(
            f"- **구문 요지**: 인수·반환 형은 [Microsoft Learn]({learn})을 따른다."
        )
        lines.append(
            "- **전형적 사용**: Power Query 편집기의 리본 동작이 생성하는 M과 대응하거나, 고급 편집기에서 직접 호출한다."
        )
        lines.append(
            "- **주의**: 프라이버시 수준, 쿼리 접기, 네이티브 쿼리 전달 여부는 커넥터·단계에 따라 달라진다."
        )
        lines.append(
            f"- **참고**: [Microsoft Learn]({learn}), [PowerQuery.how](https://powerquery.how/{slug}/)"
        )
        lines.append("")
    lines.append(f"_총 {len(slugs)}개 항목._")
    OUT_M.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    slugs_dax = parse_dax_slugs()
    slugs_m = parse_m_slugs()
    if not slugs_dax:
        raise SystemExit("No DAX slugs; ensure .tmp_dax_sitemap.xml exists")
    write_dax(slugs_dax)
    if slugs_m:
        write_m(slugs_m)
    else:
        OUT_M.write_text(
            "<!-- M slugs file missing; skipped -->\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
