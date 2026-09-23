"""Day 3 判分：聚合 + 导出 CSV + 串起来。

期望的聚合结果（金额降序，同金额按用户名字母序）：
  alice 3 145.00 / bob 2 105.90 / carol 1 50.00 / erin 1 29.70 / unknown 1 16.50 / dave 1 14.00
"""
from pathlib import Path

import pytest

from src.report import aggregate, clean, find_data_files, load_records, main, write_csv

DATA = Path(__file__).resolve().parents[1] / "data"
EXPECTED = [
    ("alice", 3, 145.00),
    ("bob", 2, 105.90),
    ("carol", 1, 50.00),
    ("erin", 1, 29.70),
    ("unknown", 1, 16.50),
    ("dave", 1, 14.00),
]


@pytest.fixture(scope="module")
def cleaned():
    records, _ = load_records(find_data_files(DATA))
    rows, _ = clean(records)
    return rows


@pytest.fixture(scope="module")
def rows(cleaned):
    return aggregate(cleaned)


def test_aggregate_shape(rows):
    assert len(rows) == 6
    for r in rows:
        assert set(r) == {"user", "orders", "amount"}
        assert isinstance(r["orders"], int)


def test_aggregate_values_and_order(rows):
    got = [(r["user"], r["orders"], round(r["amount"], 2)) for r in rows]
    assert got == EXPECTED


def test_aggregate_totals_match_cleaned(rows, cleaned):
    assert sum(r["orders"] for r in rows) == len(cleaned) == 9
    assert sum(r["amount"] for r in rows) == pytest.approx(sum(r["amount"] for r in cleaned), abs=1e-6)


def test_write_csv(rows, tmp_path):
    target = tmp_path / "report.csv"
    out = write_csv(rows, target)
    assert Path(out) == target and target.exists()
    lines = target.read_text(encoding="utf-8").strip().splitlines()
    assert lines[0] == "user,orders,amount"
    assert len(lines) == 7
    assert lines[1] == "alice,3,145.00"
    assert lines[-1] == "dave,1,14.00"


def test_write_csv_creates_parent_dir(rows, tmp_path):
    target = tmp_path / "nested" / "deeper" / "report.csv"
    write_csv(rows, target)
    assert target.exists()


def test_main_end_to_end(tmp_path, capsys):
    target = tmp_path / "out" / "report.csv"
    main(data_dir=DATA, out_path=target)
    assert target.exists()
    printed = capsys.readouterr().out
    assert "361.1" in printed          # 总额要打印出来，方便人肉核对
