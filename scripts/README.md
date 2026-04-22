# Scripts

- `split_power_bi_report.py` — `report/20260420_power_bi_report.md` → `src/content/studies/` 4개 파일 생성.
- `lint_report.py` — `report/` 초안 또는 `src/content/` 배포본 마크다운 검사. 저장소 루트에서 `.venv` 생성 후 `pip install -r requirements-dev.txt` 권장.
- `publish.py` — `reviews`용 `report/YYYYMMDD_report_*.md` → `src/content/reviews/` ( `--description`, `--tags` JSON 필수).

테스트: `.venv/bin/pytest scripts/test_lint_report.py scripts/test_publish.py -v`
