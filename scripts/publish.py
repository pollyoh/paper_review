#!/usr/bin/env python3
"""Publish report/*.md into src/content (reviews). Studies: run split script separately."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def slug_from_reviews_report(filename: str) -> str:
    m = re.match(r"^(\d{8})_report_(.+)\.md$", filename)
    if not m:
        raise ValueError(f"expected YYYYMMDD_report_snake.md, got {filename!r}")
    date, snake = m.group(1), m.group(2)
    kebab = snake.replace("_", "-")
    return f"{date}-{kebab}"


def _clean_meta_value(s: str) -> str:
    s = s.replace("`", "").replace("<br>", "").strip()
    s = re.sub(r"^\*\*(.+?)\*\*:\s*", "", s)
    s = s.strip()
    if s.startswith("*") and s.endswith("*"):
        s = s[1:-1]
    return s.strip()


def extract_reviews_meta(text: str) -> dict[str, str]:
    """Parse first blockquote meta lines (report convention)."""
    out: dict[str, str] = {}
    mapping = {
        "원논문": "originalTitle",
        "저자": "authors",
        "소속": "institution",
        "출처": "venue",
        "보고서 작성일": "reportDate",
    }
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith(">"):
            continue
        inner = line.lstrip(">").strip()
        for kr, en in mapping.items():
            if inner.startswith(f"**{kr}**"):
                out[en] = _clean_meta_value(inner)
        if {"originalTitle", "authors", "institution", "reportDate"} <= out.keys():
            break
    need = {"originalTitle", "authors", "institution", "reportDate"}
    missing = need - set(out)
    if missing:
        raise ValueError(f"missing meta fields: {missing}")
    return out


def build_reviews_markdown(
    *,
    report_text: str,
    slug: str,
    title_line: str,
    description: str,
    tags: list[str],
    topic: str | None,
) -> str:
    meta = extract_reviews_meta(report_text)
    date_iso = meta["reportDate"].replace(".", "-")
    if re.match(r"^\d{4}-\d{2}-\d{2}$", meta["reportDate"]):
        date_iso = meta["reportDate"]
    fm = {
        "title": title_line.lstrip("# ").strip(),
        "originalTitle": meta["originalTitle"],
        "date": date_iso,
        "authors": meta["authors"],
        "institution": meta["institution"],
        "tags": tags,
        "description": description,
    }
    if topic:
        fm["topic"] = topic
    header = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()
    body = strip_report_header_for_body(report_text, slug)
    # LLM이 `<br>`를 인라인 코드로 감싸면 줄바꿈이 아니라 문자 그대로 보인다.
    out = f"---\n{header}\n---\n\n{body}"
    return out.replace("`<br>`", "<br>")


def strip_report_header_for_body(text: str, slug: str) -> str:
    """Remove blockquote meta block and following ---; keep # title and rest."""
    lines = text.splitlines()
    if not lines or not lines[0].startswith("#"):
        raise ValueError("expected first line to be # title")
    title = lines[0]
    i = 1
    while i < len(lines) and lines[i].strip().startswith(">"):
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].strip() == "---":
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    rest = "\n".join(lines[i:])
    base = "/paper_review/images/reviews/" + slug + "/"
    rest = re.sub(
        r"\]\(\.\./paper/[^)]+/([^)]+)\)",
        lambda m: f"]({base}{m.group(1)})",
        rest,
    )
    return title + "\n\n" + rest


def run_lint_report(args: list[str]) -> None:
    cmd = [sys.executable, str(ROOT / "scripts" / "lint_report.py"), *args]
    r = subprocess.run(cmd, cwd=str(ROOT))
    if r.returncode != 0:
        raise SystemExit(r.returncode)


def copy_review_images(body: str, slug: str, *, dry_run: bool) -> None:
    dest_dir = ROOT / "public" / "images" / "reviews" / slug
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", body):
        url = m.group(1).strip()
        if not url.startswith("/paper_review/images/reviews/"):
            continue
        rel = url.removeprefix("/paper_review/images/reviews/").lstrip("/")
        parts = rel.split("/", 1)
        if len(parts) != 2 or parts[0] != slug:
            continue
        fname = parts[1]
        src = None
        for cand in ROOT.glob(f"paper/**/{fname}"):
            if cand.is_file():
                src = cand
                break
        if src is None:
            print(f"warn: could not find source image for {fname}", file=sys.stderr)
            continue
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest_dir / fname)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Publish a reviews report to src/content/reviews.")
    p.add_argument("--category", choices=("reviews", "studies"), required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--description", type=str, help="Frontmatter description (reviews)")
    p.add_argument("--tags", type=str, help='JSON array string, e.g. \'["a","b"]\'')
    p.add_argument("--topic", type=str, default=None)
    p.add_argument("report_md", type=Path)
    args = p.parse_args(argv)

    if args.category == "studies":
        print(
            "For studies, run: python3 scripts/split_power_bi_report.py "
            "then lint content/*.md",
            file=sys.stderr,
        )
        return 2

    path = args.report_md.resolve()
    text = path.read_text(encoding="utf-8")
    run_lint_report(["--strict", "--stage", "report", "--category", "reviews", str(path)])

    slug = slug_from_reviews_report(path.name)
    title_line = text.splitlines()[0]
    if not args.description or not args.tags:
        print("--description and --tags required for reviews publish", file=sys.stderr)
        return 2
    tags = json.loads(args.tags)
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        print("--tags must be a JSON array of strings", file=sys.stderr)
        return 2

    out = build_reviews_markdown(
        report_text=text,
        slug=slug,
        title_line=title_line,
        description=args.description,
        tags=tags,
        topic=args.topic,
    )
    out_path = ROOT / "src" / "content" / "reviews" / f"{slug}.md"
    if args.dry_run:
        print(f"would write {out_path.relative_to(ROOT)}")
        return 0
    out_path.write_text(out, encoding="utf-8")
    copy_review_images(out, slug, dry_run=False)
    run_lint_report(["--strict", "--stage", "content", "--category", "reviews", str(out_path)])
    print("wrote", out_path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
