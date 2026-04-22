#!/usr/bin/env python3
"""Markdown linter for report/ drafts and src/content published posts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as e:  # pragma: no cover
    print("PyYAML required: pip install -r requirements-dev.txt", file=sys.stderr)
    raise SystemExit(2) from e

ROOT = Path(__file__).resolve().parents[1]


def err(msg: str, *, strict: bool, code: str = "error") -> None:
    print(f"{code}: {msg}", file=sys.stderr)


def strip_fenced_blocks(text: str) -> str:
    return re.sub(r"^```[\s\S]*?^```\s*", "", text, flags=re.MULTILINE)


def count_h2(text: str) -> int:
    body = strip_fenced_blocks(text)
    return len(re.findall(r"^##\s+.+$", body, flags=re.MULTILINE))


def count_heading_lines(text: str) -> int:
    """Count ## … ###### headings (fenced blocks stripped)."""
    body = strip_fenced_blocks(text)
    return len(re.findall(r"^#{2,6}\s+", body, flags=re.MULTILINE))


def count_pipe_tables(text: str) -> int:
    body = strip_fenced_blocks(text)
    lines = body.splitlines()
    tables = 0
    in_table = False
    for line in lines:
        s = line.strip()
        if s.startswith("|") and s.count("|") >= 2:
            if not in_table:
                tables += 1
                in_table = True
        else:
            in_table = False
    return tables


def count_mermaid(text: str) -> int:
    return len(re.findall(r"^```mermaid\s*$", text, flags=re.MULTILINE))


def has_url(text: str) -> bool:
    return re.search(r"https?://[^\s)>\]]+", text) is not None


def check_unclosed_fences(text: str) -> bool:
    """Return True if OK (balanced ``` fences)."""
    lines = text.splitlines()
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
    return not in_fence


def resolve_image_path(md_path: Path, url: str) -> Path | None:
    if url.startswith("http://") or url.startswith("https://"):
        return None
    if url.startswith("/paper_review/"):
        rel = url[len("/paper_review/") :]
        return ROOT / "public" / rel
    if url.startswith("/"):
        return ROOT / "public" / url.lstrip("/")
    if url.startswith("./") or (not url.startswith("/") and ".." not in url):
        return (md_path.parent / url).resolve()
    if url.startswith("../"):
        return (md_path.parent / url).resolve()
    return None


def lint_images(md_path: Path, body: str, *, strict: bool) -> int:
    issues = 0
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", body):
        raw = m.group(1).strip()
        if raw.startswith("http"):
            continue
        p = resolve_image_path(md_path, raw)
        if p is None:
            continue
        if not p.is_file():
            err(f"missing image {raw} -> {p}", strict=strict)
            issues += 1
    return issues


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    try:
        data = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"invalid YAML frontmatter: {e}") from e
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data, parts[2]


def lint_content(
    path: Path,
    text: str,
    *,
    category: str,
    strict: bool,
) -> int:
    issues = 0
    try:
        fm, body = split_frontmatter(text)
    except ValueError as e:
        err(f"{path}: {e}", strict=strict)
        return 1
    if fm is None:
        err(f"{path}: expected YAML frontmatter", strict=strict)
        return 1

    if category == "reviews":
        required = [
            "title",
            "originalTitle",
            "date",
            "authors",
            "institution",
            "tags",
            "description",
        ]
    else:
        required = ["title", "date", "description", "tags", "topic"]

    for k in required:
        if k not in fm or fm[k] in (None, "", []):
            err(f"{path}: missing or empty frontmatter key `{k}`", strict=strict)
            issues += 1

    h2 = count_h2(body)
    tables = count_pipe_tables(body)
    mermaid = count_mermaid(text)
    annotations = "[주석]" in body

    if category == "reviews":
        if h2 < 7:
            err(f"{path}: need at least 7 ## headings, found {h2}", strict=strict)
            issues += 1
        if tables < 3:
            err(f"{path}: need at least 3 pipe tables, found {tables}", strict=strict)
            issues += 1
        if mermaid < 2:
            err(f"{path}: need at least 2 ```mermaid blocks, found {mermaid}", strict=strict)
            issues += 1
        if not annotations:
            err(f"{path}: need at least one [주석] annotation", strict=strict)
            issues += 1
    else:
        hn = count_heading_lines(body)
        if hn < 10:
            err(
                f"{path}: need at least 10 markdown headings (##–######), found {hn}",
                strict=strict,
            )
            issues += 1
        if tables < 1:
            # 긴 자동 생성 부록(M 등)은 파이프 표가 없을 수 있음 — 본문 길이로 완화
            if len(body) < 8000:
                err(
                    f"{path}: need at least 1 pipe table (or body longer than 8000 chars), "
                    f"found {tables} tables, len={len(body)}",
                    strict=strict,
                )
                issues += 1

    if not has_url(body):
        err(f"{path}: need at least one http(s) URL in body", strict=strict)
        issues += 1

    issues += lint_images(path, body, strict=strict)

    if not check_unclosed_fences(text):
        err(f"{path}: unclosed ``` fence", strict=strict)
        issues += 1

    return issues


def lint_report_reviews(path: Path, text: str, *, strict: bool) -> int:
    issues = 0
    name = path.name
    if not re.match(r"^\d{8}_report_[a-z0-9_]+\.md$", name):
        err(
            f"{path}: filename should match YYYYMMDD_report_snake.md (got {name!r})",
            strict=strict,
        )
        issues += 1

    for needle in ("**원논문**", "**저자**", "**소속**", "**출처**", "**보고서 작성일**"):
        if needle not in text:
            err(f"{path}: missing meta marker {needle!r}", strict=strict)
            issues += 1

    h2 = count_h2(text)
    if h2 < 7:
        err(f"{path}: need at least 7 ## headings, found {h2}", strict=strict)
        issues += 1
    if count_pipe_tables(text) < 3:
        err(f"{path}: need at least 3 pipe tables", strict=strict)
        issues += 1
    if count_mermaid(text) < 2:
        err(f"{path}: need at least 2 ```mermaid blocks", strict=strict)
        issues += 1
    if "[주석]" not in text:
        err(f"{path}: need at least one [주석]", strict=strict)
        issues += 1
    if not has_url(text):
        err(f"{path}: need at least one http(s) URL", strict=strict)
        issues += 1
    issues += lint_images(path, text, strict=strict)
    if not check_unclosed_fences(text):
        err(f"{path}: unclosed ``` fence", strict=strict)
        issues += 1
    return issues


def lint_report_studies(path: Path, text: str, *, strict: bool) -> int:
    issues = 0
    name = path.name
    if not re.match(r"^\d{8}_.+\.md$", name):
        err(f"{path}: filename should match YYYYMMDD_*.md", strict=strict)
        issues += 1
    h2 = count_h2(text)
    if h2 < 3:
        err(f"{path}: need at least 3 ## headings, found {h2}", strict=strict)
        issues += 1
    if count_pipe_tables(text) < 1:
        err(f"{path}: need at least 1 pipe table", strict=strict)
        issues += 1
    if not has_url(text):
        err(f"{path}: need at least one http(s) URL", strict=strict)
        issues += 1
    issues += lint_images(path, text, strict=strict)
    if not check_unclosed_fences(text):
        err(f"{path}: unclosed ``` fence", strict=strict)
        issues += 1
    return issues


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--strict", action="store_true")
    p.add_argument("--stage", choices=("report", "content"), required=True)
    p.add_argument("--category", choices=("reviews", "studies"), required=True)
    p.add_argument("paths", nargs="+", type=Path)
    args = p.parse_args(argv)
    total = 0
    for path in args.paths:
        path = path.resolve()
        if not path.is_file():
            err(f"{path}: not a file", strict=args.strict)
            total += 1
            continue
        text = path.read_text(encoding="utf-8")
        if args.stage == "content":
            total += lint_content(path, text, category=args.category, strict=args.strict)
        elif args.category == "reviews":
            total += lint_report_reviews(path, text, strict=args.strict)
        else:
            total += lint_report_studies(path, text, strict=args.strict)
    if total > 0 and args.strict:
        return 1
    if total > 0:
        print(f"warn: {total} issue(s) (non-strict mode, exit 0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
