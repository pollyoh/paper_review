from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_publish():
    path = ROOT / "scripts" / "publish.py"
    spec = importlib.util.spec_from_file_location("_publish", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_slug_from_reviews_report() -> None:
    pub = _load_publish()
    assert (
        pub.slug_from_reviews_report(
            "20260416_report_a_survey_on_llm_powered_agents_for_recommender_systems.md",
        )
        == "20260416-a-survey-on-llm-powered-agents-for-recommender-systems"
    )


def test_build_reviews_markdown_replaces_br_backticks() -> None:
    pub = _load_publish()
    report = """# 제목

> **원논문**: *Paper* `<br>`
> **저자**: A `<br>`
> **소속**: B `<br>`
> **출처**: C `<br>`
> **보고서 작성일**: 2026-04-16

---

## 본문

줄 `<br>` 끝
"""
    out = pub.build_reviews_markdown(
        report_text=report,
        slug="20260416-test",
        title_line="# 제목",
        description="d",
        tags=["x"],
        topic=None,
    )
    assert "`<br>`" not in out
    assert "줄 <br> 끝" in out
