from src.report import clean


def test_missing_order_id_is_not_a_duplicate():
    rows, stats = clean([{"amount": 1}, {"amount": 2}])
    assert stats["duplicates"] == 0        # 现在会红 —— 红就是证据