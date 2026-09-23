"""M0 第一项验收：扫描目录的 JSON → 清洗 → 聚合 → 导出 CSV。

规则全部写在 README.md 的「规格」一节。函数名和签名不许改，实现全部自己写。
写之前先在纸上想清楚：这个函数拿到什么、返回什么、坏输入会走到哪条分支。
"""
from __future__ import annotations
import json
from pathlib import Path


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
    for file_path in paths:
        name = file_path.name

        try:
            text = file_path.read_text(encoding="utf-8")
            data = json.loads(text)
        except json.JSONDecodeError:
            print(f"跳过文件 {name}: JSON解析失败")
            skipped.append(name)
            continue

        if not isinstance(data, list):
            print(f"跳过文件 {name}: JSON顶层不是列表")
            skipped.append(name)
            continue
        
        records.extend(data)
    return records,skipped


def clean(records: list[dict]) -> tuple[list[dict], dict]:
    """按 README 的 7 条规则清洗。

    Day 2。返回 (清洗后的记录, {"dropped": 丢弃条数, "duplicates": 重复条数})。
    每条输出固定为：{"order_id": str, "user": str, "amount": float, "date": str | None}
    原始记录不要被就地改掉（想想为什么）。
    """
    raise NotImplementedError


def aggregate(records: list[dict]) -> list[dict]:
    """按用户汇总成 [{"user": str, "orders": int, "amount": float}]。

    Day 3。排序：amount 从大到小；金额相同时按 user 字母序。
    """
    raise NotImplementedError


def write_csv(rows: list[dict], out_path: Path) -> Path:
    """写出 CSV：表头 user,orders,amount，金额保留两位小数，UTF-8。

    Day 3。out_path 的父目录可能不存在。
    """
    raise NotImplementedError


def main(data_dir: Path = Path("data"), out_path: Path = Path("out/report.csv")) -> None:
    """把上面四个函数串起来，并打印：读到多少条、跳过哪些、丢弃/重复各几条、总额多少。

    Day 3。跑法：python -m src.report
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
