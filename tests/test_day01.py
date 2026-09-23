"""Day 1 判分：把 data/ 里的 JSON 原样读出来，坏文件跳过并说明原因。

跑法：python -m pytest tests/test_day01.py -v
这些数字来自 README 的规格，是**要求**，不是提示你写死。
"""
from pathlib import Path

from src.report import find_data_files, load_records

DATA = Path(__file__).resolve().parents[1] / "data"


def test_only_json_files_and_sorted():
    names = [p.name for p in find_data_files(DATA)]
    assert names == ["broken.json", "orders_2026-06.json", "orders_2026-07.json", "orders_2026-08.json"]


def test_load_returns_11_raw_records():
    records, skipped = load_records(find_data_files(DATA))
    assert len(records) == 11
    assert all("order_id" in r for r in records)


def test_day1_does_not_clean():
    """第 1 步不许顺手清洗：脏值必须还在原样里。"""
    records, _ = load_records(find_data_files(DATA))
    a1001 = [r for r in records if r["order_id"] == "A-1001"][0]
    assert a1001["amount"] == "25.00"          # 还是字符串
    assert any(r.get("amount") is None for r in records)      # A-1003
    assert any("amount" not in r for r in records)            # A-1005 根本没有这个键


def test_two_files_skipped_and_reported(capsys):
    records, skipped = load_records(find_data_files(DATA))
    assert sorted(skipped) == ["broken.json", "orders_2026-08.json"]
    printed = capsys.readouterr().out
    assert "broken.json" in printed and "orders_2026-08.json" in printed


def test_order_of_paths_does_not_matter():
    records, skipped = load_records(list(reversed(find_data_files(DATA))))
    assert len(records) == 11 and len(skipped) == 2
