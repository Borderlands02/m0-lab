"""Day 2 判分：按 README 的 7 条清洗规则处理。

标准答案（我用同一套规则手算过，别去猜，去核对你的逻辑）：
  原始 11 条 → 清洗后 9 条，丢弃 1 条（A-1005），去重 1 条（第二个 A-1002），总额 361.10
"""
from pathlib import Path

import pytest

from src.report import clean, find_data_files, load_records

DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def raw():
    records, _ = load_records(find_data_files(DATA))
    return records


@pytest.fixture(scope="module")
def result(raw):
    return clean(raw)


@pytest.fixture()
def by_id(result):
    cleaned, _ = result
    return {r["order_id"]: r for r in cleaned}


def test_counts(result):
    cleaned, stats = result
    assert len(cleaned) == 9
    assert stats["dropped"] == 1
    assert stats["duplicates"] == 1


def test_schema_and_types(result, by_id):
    cleaned, _ = result
    for r in cleaned:
        assert set(r) == {"order_id", "user", "amount", "date"}
        assert isinstance(r["amount"], float)
    assert by_id["A-1001"]["amount"] == 25.0        # 字符串 "25.00" → 25.0，且不等于 qty*price


def test_total_amount(result):
    cleaned, _ = result
    assert sum(r["amount"] for r in cleaned) == pytest.approx(361.10, abs=1e-6)


def test_amount_fallback_and_unknown_user(by_id):
    assert by_id["A-1003"]["amount"] == pytest.approx(16.5)   # amount 为 null → qty*price
    assert by_id["A-1003"]["user"] == "unknown"               # user 为 null
    assert by_id["B-2004"]["amount"] == pytest.approx(6.0)


def test_dates(by_id):
    assert by_id["A-1001"]["date"] == "2026-06-01"   # 带时间的取前 10 位
    assert by_id["A-1002"]["date"] == "2026-06-02"   # ISO 格式同样取前 10 位
    assert by_id["B-2004"]["date"] is None           # "bad-date" 解析不出来


def test_duplicated_order_keeps_first(by_id):
    assert "A-1002" in by_id                          # 只留一条
    assert "A-1005" not in by_id                      # amount/qty/price 凑不出来 → 丢弃


def test_input_not_mutated(raw):
    """清洗必须产出新列表，不能把传进来的原始记录改掉。"""
    clean(raw)
    a1001 = [r for r in raw if r["order_id"] == "A-1001"][0]
    assert a1001["amount"] == "25.00"
    assert set(a1001) == {"order_id", "user", "qty", "price", "amount", "created_at"}
