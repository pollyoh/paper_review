#!/usr/bin/env python3
"""Download Power BI visualization screenshots from Microsoft Learn docs.

Images are fetched from the open-source MicrosoftDocs/powerbi-docs repository
so that the URLs do not expire and licensing (CC BY 4.0 for prose, MIT for
code, and all media attributed to Microsoft Learn) remains traceable. Each
file is saved to report/img/power_bi/<slug>.png and the script prints a CSV
line per image so the caller can copy the "source" row into the report.
"""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import NamedTuple

RAW_ROOT = "https://github.com/MicrosoftDocs/powerbi-docs/raw/main/powerbi-docs"
OUT_DIR = Path(__file__).resolve().parents[1] / "report" / "img" / "power_bi"


class Shot(NamedTuple):
    slug: str
    page: str
    rel: str
    title: str


SHOTS: list[Shot] = [
    Shot(
        "common",
        "power-bi-visualization-matrix-visual",
        "visuals/media/power-bi-visualization-matrix-visual/build-matrix-visual-desktop-step-1.png",
        "Build a matrix visual in Power BI",
    ),
    Shot(
        "table",
        "power-bi-visualization-tables",
        "visuals/media/power-bi-visualization-tables/power-bi-table-format.png",
        "Work with tables in Power BI reports",
    ),
    Shot(
        "matrix",
        "power-bi-visualization-matrix-visual",
        "visuals/media/power-bi-visualization-matrix-visual/build-matrix-visual-desktop-step-3.png",
        "Build a matrix visual in Power BI",
    ),
    Shot(
        "card",
        "power-bi-visualization-card",
        "visuals/media/power-bi-visualization-card-visual/build-card.png",
        "Create Card visuals in Power BI reports",
    ),
    Shot(
        "multirow_card",
        "power-bi-visualization-card",
        "visuals/media/power-bi-visualization-card-visual/multicard-layout.png",
        "Create Card visuals in Power BI reports",
    ),
    Shot(
        "line",
        "power-bi-line-chart",
        "visuals/media/power-bi-line-charts/line-chart-dynamic-series.png",
        "Line charts in Power BI",
    ),
    Shot(
        "bar_clustered",
        "power-bi-visualization-column-charts",
        "visuals/media/power-bi-visualization-column-charts/column-drill.png",
        "Column charts in Power BI",
    ),
    Shot(
        "bar_stacked",
        "power-bi-visualization-column-charts",
        "visuals/media/power-bi-visualization-column-charts/column-formatting.png",
        "Column charts in Power BI",
    ),
    Shot(
        "combo",
        "power-bi-visualization-combo-chart",
        "visuals/media/power-bi-visualization-combo-chart/power-bi-line-and-stacked-column-chart-fields.png",
        "Use a combo chart in Power BI",
    ),
    Shot(
        "scatter",
        "power-bi-visualization-scatter",
        "visuals/media/power-bi-visualization-scatter/power-bi-compare-charts.png",
        "Scatter, bubble, and dot plot charts in Power BI",
    ),
    Shot(
        "area",
        "power-bi-visualization-basic-area-chart",
        "visuals/media/power-bi-visualization-basic-area-chart/power-bi-chart-example.png",
        "Basic area chart in Power BI",
    ),
    Shot(
        "ribbon",
        "desktop-ribbon-charts",
        "visuals/media/desktop-ribbon-charts/ribbon-charts-01.png",
        "Ribbon charts in Power BI",
    ),
    Shot(
        "waterfall",
        "power-bi-visualization-waterfall-charts",
        "visuals/media/power-bi-visualization-waterfall-charts/power-bi-waterfall-chart.png",
        "Waterfall charts in Power BI",
    ),
    Shot(
        "funnel",
        "power-bi-visualization-funnel-charts",
        "visuals/media/power-bi-visualization-funnel-charts/power-bi-funnel-plain.png",
        "Funnel charts in Power BI",
    ),
    Shot(
        "pie_donut",
        "power-bi-visualization-pie-donut-chart",
        "visuals/media/pie-donut-chart/pie-donut-data-pane.png",
        "Pie and doughnut charts in Power BI",
    ),
    Shot(
        "treemap",
        "power-bi-visualization-treemaps",
        "visuals/media/power-bi-visualization-treemaps/power-bi-treemap-overview.png",
        "Create treemaps in Power BI",
    ),
    Shot(
        "map",
        "power-bi-map-tips-and-tricks",
        "visuals/media/power-bi-map-tips-and-tricks/power-bi-sent-to-bing-new.png",
        "Map tips and tricks",
    ),
    Shot(
        "filled_map",
        "power-bi-visualization-filled-maps-choropleths",
        "visuals/media/power-bi-visualization-filled-maps-choropleths/large-map.png",
        "Filled maps (choropleths)",
    ),
    Shot(
        "gauge",
        "power-bi-visualization-radial-gauge-charts",
        "visuals/media/power-bi-visualization-radial-gauge-charts/sample-gauge-chart.png",
        "Radial gauge charts in Power BI",
    ),
    Shot(
        "kpi",
        "power-bi-visualization-kpi",
        "visuals/media/power-bi-visualization-kpi/power-bi-desktop-value-trend-axis-trend.png",
        "KPI visuals in Power BI",
    ),
    Shot(
        "decomp_tree",
        "power-bi-visualization-decomposition-tree",
        "visuals/media/power-bi-visualization-decomposition-tree/tree-full.png",
        "Create and view decomposition tree visuals",
    ),
    Shot(
        "key_influencers",
        "power-bi-visualization-influencers",
        "visuals/media/power-bi-visualization-influencers/power-bi-ki-numbers-new.png",
        "Key influencers visuals",
    ),
    Shot(
        "qna",
        "power-bi-visualization-q-and-a",
        "visuals/media/power-bi-visualization-q-and-a/power-bi-sales-marketing-sample.png",
        "Create a Q&A visual",
    ),
    Shot(
        "slicer",
        "power-bi-visualization-slicers",
        "visuals/media/power-bi-visualization-slicers/power-bi-new-slicer-desktop.png",
        "Slicers in Power BI",
    ),
    Shot(
        "segment",
        "power-bi-visualization-button-slicer",
        "visuals/media/button-slicer/button-slicer-district-highlighted.png",
        "Button slicer in Power BI",
    ),
    Shot(
        "r_python",
        "service-r-visuals",
        "visuals/media/service-r-visuals/power-bi-r-visual-desktop.png",
        "Create R visuals in Power BI",
    ),
    Shot(
        "python",
        "desktop-python-visuals",
        "connect-data/media/desktop-python-visuals/python-visuals-15.png",
        "Create Python visuals in Power BI Desktop",
    ),
    Shot(
        "custom_visual",
        "power-bi-custom-visuals",
        "developer/visuals/media/power-bi-custom-visuals/power-bi-visualizations.png",
        "Visualizations in Power BI",
    ),
    Shot(
        "small_multiples",
        "power-bi-visualization-small-multiples",
        "visuals/media/power-bi-visualization-small-multiples/small-mulitple-sales-category-region.png",
        "Small multiples",
    ),
]


def download(shot: Shot) -> tuple[bool, str]:
    url = f"{RAW_ROOT}/{shot.rel}"
    ext = Path(shot.rel).suffix or ".png"
    dst = OUT_DIR / f"{shot.slug}{ext}"
    if dst.exists() and dst.stat().st_size > 1024:
        return True, f"{shot.slug},{dst.name},exists,{url}"
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605"
                    " (KHTML, like Gecko) Version/16.0 Safari/605"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
    except urllib.error.HTTPError as exc:
        return False, f"{shot.slug},{dst.name},HTTP{exc.code},{url}"
    except Exception as exc:  # noqa: BLE001
        return False, f"{shot.slug},{dst.name},ERR({exc}),{url}"
    dst.write_bytes(data)
    return True, f"{shot.slug},{dst.name},{len(data)},{url}"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    failures = 0
    print("slug,file,status,url")
    for shot in SHOTS:
        ok, line = download(shot)
        print(line)
        if not ok:
            failures += 1
    if failures:
        print(f"FAILURES: {failures}/{len(SHOTS)}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
