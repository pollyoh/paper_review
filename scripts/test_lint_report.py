"""Tests for scripts/lint_report.py (run: .venv/bin/pytest scripts/test_lint_report.py -v)."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_lint_report():
    path = ROOT / "scripts" / "lint_report.py"
    spec = importlib.util.spec_from_file_location("_lint_report", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def test_lint_remark_math_delimiters_flags_tex_paren() -> None:
    lr = _load_lint_report()
    p = Path("x.md")
    assert lr.lint_remark_math_delimiters(r"plain \(a\) math", p, strict=False) == 1
    assert lr.lint_remark_math_delimiters(r"ok $a$ inline", p, strict=False) == 0


def test_lint_description_plaintext_flags_bold_and_backtick() -> None:
    lr = _load_lint_report()
    p = Path("x.md")
    assert lr.lint_description_plaintext({"description": "요약 문장"}, p, strict=True) == 0
    assert lr.lint_description_plaintext({"description": "bad **bold**"}, p, strict=False) == 1
    assert lr.lint_description_plaintext({"description": "bad `code`"}, p, strict=False) == 1


def test_lint_fullwidth_asterisk() -> None:
    lr = _load_lint_report()
    p = Path("x.md")
    assert lr.lint_fullwidth_asterisk("normal *emphasis*", p, strict=True) == 0
    assert lr.lint_fullwidth_asterisk("fullwidth＊＊x", p, strict=False) == 1


def test_lint_colon_space_emphasis_open() -> None:
    lr = _load_lint_report()
    p = Path("x.md")
    assert lr.lint_colon_space_emphasis_open("**레이블**: **값**", p, strict=False) == 1
    assert lr.lint_colon_space_emphasis_open("**레이블**:**값**", p, strict=True) == 0
    assert lr.lint_colon_space_emphasis_open("**A**:\n\n**B**", p, strict=True) == 0
