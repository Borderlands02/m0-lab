"""Day 3 补测：金额相同时必须按用户名字母序。

真实数据里六个金额全不同，这条分支从没被走到过。
"""
from src.report import aggregate


def test_tie_break_is_alphabetical():
    records = [
        # zoe 两单 25.00 = 50.00，amy 一单 50.00，总额打平
        {"order_id": "T-1", "user": "zoe", "amount": 25.00, "date": "2026-01-01"},
        {"order_id": "T-2", "user": "zoe", "amount": 25.00, "date": "2026-01-02"},
        {"order_id": "T-3", "user": "amy", "amount": 50.00, "date": "2026-01-03"},
    ]

    rows = aggregate(records)

    assert [r["user"] for r in rows] == ["amy", "zoe"]
    assert [r["orders"] for r in rows] == [1, 2]