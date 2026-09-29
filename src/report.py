"""M0 第一项验收：扫描目录的 JSON → 清洗 → 聚合 → 导出 CSV。

规则全部写在 README.md 的「规格」一节。函数名和签名不许改，实现全部自己写。
写之前先在纸上想清楚：这个函数拿到什么、返回什么、坏输入会走到哪条分支。
"""

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime


def find_data_files(data_dir: Path) -> list[Path]:
    """返回 data_dir 下所有 .json 文件，按文件名排序。

    Day 1。注意：只要后缀是 .json 的都算，坏文件由 load_records 负责处理。
    """
    files = sorted(Path(data_dir).glob("*.json"))
    return files


def load_records(paths: list[Path]) -> tuple[list[dict], list[str]]:
    """把多个文件里的记录读成一个大列表。

    Day 1。返回 (记录列表, 被跳过的文件名列表)：
      - 顶层不是列表 → 跳过该文件；
      - JSON 解析失败 → 跳过该文件；
      - 两种跳过都要进第二个返回值，并且打印一行说明是哪种情况。
    这一步**不要**清洗，记录保持原样。
    """
    records = []
    skipped = []
    for pile_path in paths:
        name = pile_path.name
        try:
            text = pile_path.read_text(encoding="utf-8")
            data = json.loads(text)
        except json.JSONDecodeError:
            print(f"JSON解析失败,跳过{name}文件")
            skipped.append(name)
            continue
        if not isinstance(data, list):
            print(f"顶层不是列表,跳过{name}文件")
            skipped.append(name)
            continue
        records.extend(data)
    return records, skipped


def clean(records: list[dict]) -> tuple[list[dict], dict]:
    """按 README 的 7 条规则清洗。

    Day 2。返回 (清洗后的记录, {"dropped": 丢弃条数, "duplicates": 重复条数})。
    每条输出固定为：{"order_id": str, "user": str, "amount": float, "date": str | None}
    原始记录不要被就地改掉（想想为什么）。
    """
    cleaned: list[dict] = []
    stats = {"dropped": 0, "duplicates": 0}
    seen_order_ids = set()

    for r in records:
        order_id = r.get("order_id")
        if order_id is None:
            stats["dropped"] += 1
            continue
        if order_id in seen_order_ids:
            stats["duplicates"] += 1
            continue

        amount = r.get("amount")
        if amount is None:
            qty = r.get("qty")
            price = r.get("price")
            if qty is None or price is None:
                stats["dropped"] += 1
                continue
            else:
                amount = qty * price
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            stats["dropped"] += 1
            continue

        date_val = None
        created_at = r.get("created_at")  # 拿原始日期字段
        if created_at:  # 如果它存在且不为空
            date_str = str(created_at)[:10]  # 只取前10个字符
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d")  # ← 真的把结果接下来
                date_val = d.strftime("%Y-%m-%d")  # ← 从结果里格式化出字符串
            except ValueError:
                pass

        clean_item = {
            "order_id": str(order_id),  # 强转字符串
            "user": r.get("user") or "unknown",  # 没有 user 就填 unknown
            "amount": amount,
            "date": date_val,
        }
        cleaned.append(clean_item)
        seen_order_ids.add(order_id)

    return cleaned, stats


def aggregate(records: list[dict]) -> list[dict]:
    """按用户汇总成 [{"user": str, "orders": int, "amount": float}]。

    Day 3。排序：amount 从大到小；金额相同时按 user 字母序。
    """
    user_stats = {}
    rows = []
    for r in records:
        user = r["user"]
        if user not in user_stats:
            user_stats[user] = {"orders": 0, "amount": 0.0}
        user_stats[user]["orders"] += 1
        user_stats[user]["amount"] += r["amount"]
    sorted_items = sorted(
        user_stats.items(), key=lambda item: (-item[1]["amount"], item[0])
    )

    for user, stats in sorted_items:
        user_item = {"user": user, "orders": stats["orders"], "amount": stats["amount"]}
        rows.append(user_item)

    return rows


def write_csv(rows: list[dict], out_path: Path) -> Path:
    """写出 CSV：表头 user,orders,amount，金额保留两位小数，UTF-8。

    Day 3。out_path 的父目录可能不存在。
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("user,orders,amount\n", encoding="utf-8")
    with out_path.open("a", encoding="utf-8") as f:
        for r in rows:
            line = f"{r['user']},{r['orders']},{r['amount']:.2f}\n"
            f.write(line)

    return out_path


def main(
    data_dir: Path = Path("data"), out_path: Path = Path("out/report.csv")
) -> None:
    """把上面四个函数串起来，并打印：读到多少条、跳过哪些、丢弃/重复各几条、总额多少。

    Day 3。跑法：python -m src.report
    """
    files = find_data_files(data_dir)
    records, skipped = load_records(files)
    cleaned, stats = clean(records)
    rows = aggregate(cleaned)
    final_path = write_csv(rows, out_path)
    total_amount = sum(r["amount"] for r in rows)
    print(f"读取记录数: {len(records)}")
    print(f"跳过文件: {skipped}")
    print(f"丢弃条数: {stats['dropped']}")
    print(f"重复条数: {stats['duplicates']}")
    print(f"总金额: {total_amount:.2f}")
    print(f"已写出: {final_path}")


if __name__ == "__main__":
    main()
