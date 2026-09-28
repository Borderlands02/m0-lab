# m0-lab · 第一次「没有教程，自己写」

这不是练习册，是一次判分。目标只有一个：**在没有跟任何视频的情况下，从零写出能跑、能测、能讲清的东西。**
你机器上 Python / git / uv 都装好了，环境不是问题；问题一直是「没人带的时候写不写得出来」。

## 唯一的规则：不许抄，可以查

- **可以查**：官方文档里某个函数怎么用（`pathlib.Path.read_text` 的参数、`json.loads` 抛什么异常）。
- **不可以抄**：整段实现、别人写好的同类脚本、让 AI 直接生成第一版。
- 卡住 **15 分钟**就把它记进「卡点」，继续往下推；当天结束时把卡点发我，我按面试官的方式追问。
- 测试里的数字就是**规格**，不是答案。写死返回值让它变绿 = 作弊，我会在第三天换一份新数据重判。

## 环境（第一次，5 分钟）

```bash
cd /d/Source/m0-lab
uv venv                      # 建 .venv（用你已装好的 uv 0.12）
source .venv/Scripts/activate  # Git Bash 下激活；cmd 用 .venv\Scripts\activate.bat
uv pip install pytest
python -m pytest tests/test_day01.py -v
```

第一条命令跑完，`python -c "import sys; print(sys.prefix)"` 应该指向 `.venv` 而不是 `D:\Develop\Python`。
这一步就是《规划》里 M0「环境与依赖管理」的验收，别跳过。

## 数据长什么样

`data/` 里五个文件，**脏是故意的**：

| 文件                    | 情况                                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| `orders_2026-06.json` | 6 条。`amount` 有字符串 `"25.00"`、有 `null`、有缺失；`user` 有 `null`；`A-1002` 重复出现两次；`A-1005` 既没 `amount` 也没 `qty` |
| `orders_2026-07.json` | 5 条。时间格式混用（`2026-07-01 12:00` / `2026-07-03T20:15:00` / `bad-date`）                                    |
| `orders_2026-08.json` | 顶层是 `{"note":..., "records":[...]}`，**不是列表**                                                           |
| `broken.json`         | JSON 被截断，`json.loads` 会抛 `JSONDecodeError`                                                             |
| `readme.txt`          | 不是 json，别理它                                                                                            |

## 规格（这就是你要实现的全部契约）

写在 `src/report.py` 里，函数名和签名不许改，实现全是你的。

**清洗规则（必须逐条照做，测试按这个判）**

1. 只处理 `data/*.json`，按文件名排序。
2. 顶层不是列表的文件 → 跳过；JSON 解析失败 → 跳过。两种情况都要把文件名收进 `skipped`。
3. `amount` 缺失或为 `null` → 用 `qty * price` 兜底；连 `qty`/`price` 都凑不出来 → **丢弃这条**，计数。
4. `amount` 是字符串 → 转成 `float`；已有 `amount` 时**以它为准**（哪怕和 `qty*price` 不等，`A-1001` 就是这种）。
5. `order_id` 重复 → 保留第一条，后面的算重复并计数。
6. `user` 为 `null` 或缺失 → `"unknown"`。
7. `created_at` 取前 10 个字符，能按 `%Y-%m-%d` 解析就留，不能就设为 `None`。
8. 没有 order_id 的记录 → 丢弃，计入 dropped。

## 三天怎么打

| 天     | 时间     | 做什么                                                                           | 完成判定                            |
| ----- | ------ | ----------------------------------------------------------------------------- | ------------------------------- |
| Day 1 | 40 min | `find_data_files` + `load_records`：只把记录原样读出来，坏文件跳过并打印原因                       | `pytest tests/test_day01.py` 全绿 |
| Day 2 | 40 min | `clean`：按上面 7 条规则清洗，返回 `(记录, {"dropped":n,"duplicates":n})`                   | `test_day02.py` 全绿              |
| Day 3 | 60 min | `aggregate` + `write_csv` + `main`：按用户汇总、按金额降序、导出 `out/report.csv`；补类型注解和异常处理 | `test_day03.py` 全绿 + 你自己能讲清每一行  |

每天结束做两件事（这两件比代码本身重要）：

```bash
git init            # 只有第一天需要
git add -A && git commit -m "day1: load records, skip broken files"
```

然后写三行：关键洞察 / 我卡在哪 / 下次出现什么信号该想到这段。

## 我怎么看你的结果

把这三样发我：`git log --oneline`、`pytest -v` 的输出、你卡住 15 分钟以上的那个点。
我会像面试官一样问五个问题，比如：`json.loads` 抛异常时你的 `for` 循环会发生什么？为什么 `amount` 用 `float` 不用 `Decimal`，什么时候必须换？把 `skipped` 改成返回原因字典，测试要怎么动？

答不上来的地方，就是还没过关的地方——不是回去看视频，是回去把那段重写一遍。
