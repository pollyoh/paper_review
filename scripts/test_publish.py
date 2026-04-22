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
