"""Tests for scripts/lint_report.py (run: .venv/bin/pytest scripts/test_lint_report.py -v)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "lint_report.py"), *args],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )


def test_lint_content_alto_passes() -> None:
    path = ROOT / "src/content/reviews/20260410-alto-adaptive-lora-tuning-and-orchestration.md"
    r = _run(["--strict", "--stage", "content", "--category", "reviews", str(path)])
    assert r.returncode == 0, r.stderr + r.stdout


def test_lint_content_study_dax_passes() -> None:
    path = ROOT / "src/content/studies/20260420-power-bi-dax-reference.md"
    r = _run(["--strict", "--stage", "content", "--category", "studies", str(path)])
    assert r.returncode == 0, r.stderr + r.stdout


def test_lint_report_recommender_passes() -> None:
    path = ROOT / "report/20260416_report_a_survey_on_llm_powered_agents_for_recommender_systems.md"
    r = _run(["--strict", "--stage", "report", "--category", "reviews", str(path)])
    assert r.returncode == 0, r.stderr + r.stdout
