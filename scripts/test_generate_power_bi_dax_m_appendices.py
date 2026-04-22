"""Smoke tests for generate_power_bi_dax_m_appendices."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts" / "generate_power_bi_dax_m_appendices.py"
    spec = importlib.util.spec_from_file_location("gen", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_dax_display_name():
    gen = load_module()
    assert gen.dax_display_name("calculate") == "CALCULATE"
    assert gen.dax_display_name("percentile-exc") == "PERCENTILE.EXC"
    assert gen.dax_display_name("stdev-s") == "STDEV.S"


def test_m_display_name():
    gen = load_module()
    assert gen.m_display_name("table-addcolumn") == "Table.AddColumn"
    assert gen.m_display_name("list-skip") == "List.Skip"
    assert gen.m_display_name("accesscontrolkind-allow") == "AccessControlKind.Allow"


if __name__ == "__main__":
    test_dax_display_name()
    test_m_display_name()
    print("ok")
