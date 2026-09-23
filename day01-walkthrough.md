# Day 1 带读：今晚 40 分钟，切成 6 步

先说一句：**你不需要看懂整个 README，也不需要看懂三个测试文件。** 今天只碰 5 个函数名和 4 个零件。
看不懂的东西分三层，处理方式完全不同，别混在一起：

| 你看不懂的是什么 | 怎么办 | 花多久 |
|---|---|---|
| **行话**（规格、fixture、`tuple[list[dict], list[str]]`、断言） | 看下面这张翻译表，今晚不用搞懂原理 | 3 分钟 |
| **要做什么** | 看 Step 1，我翻译成人话了 | 2 分钟 |
| **怎么写** | 这才是动手的地方，Step 2 起，卡 15 分钟就贴报错问我 | 剩下的全部时间 |

## 行话翻译表（今晚只当字典用）

- `def load_records(paths: list[Path]) -> tuple[list[dict], list[str]]`
  → 读成："给它**一串文件路径**，它还我**两个列表**：一个装着记录，一个装着被跳过的文件名。" 冒号后面和箭头后面那些是类型注解，**今晚可以完全无视**，M1 再正经学。
- `Path` → 一个"文件路径"对象，比字符串好用，因为它自带 `.read_text()`、`.name`、`.glob()`。
- `raise NotImplementedError` → 骨架里插的旗子，意思是"这里该你写"。跑测试报这个错 = 正常，不是坏了。
- `assert` → 断言，"这里必须成立，否则报错"。测试就是一堆 assert。
- `fixture` / `capsys` / `tmp_path` → pytest 提供的便利工具，**今晚不用看懂**，只需要知道 `capsys` 是用来偷看你 print 了什么。
- 规格（README 里那 7 条）→ 要求清单，不是提示，不是参考，是必须照做的合同。

---

## 那行调用怎么读（以后每行都能这样拆）

`tests/test_day01.py` 第 19 行：

```python
records, skipped = load_records(find_data_files(DATA))
```

从里往外念，五个零件：

1. `DATA` —— 第 10 行定义的变量，一个指向 `data/` 的 `Path`
2. `find_data_files(DATA)` —— **先算最里面的括号**，得到一个 `list[Path]`
3. `load_records( ... )` —— 把上面那个列表原样当参数传进去
4. `records, skipped = ` —— 函数交出**两个**东西，左边写两个变量名，按顺序一人一个。这叫**解包**，等价于：
   ```python
   结果 = load_records(find_data_files(DATA))
   records = 结果[0]
   skipped = 结果[1]
   ```
5. 第 26 行还有个变体 `records, _ = ...`：`_` 是"这个我不要，但要占个位"的约定写法

签名 `-> tuple[list[dict], list[str]]` 说的就是"我交出两个列表"。**签名和调用必须配得上**，这就是为什么骨架里的签名不许改。

## 完整思维流程（每次拿到陌生任务都走这六步）

1. **找要求**：README 的规格 + 测试里的 `assert`。先读要求，再想代码——要求永远写在文件里，不在任何人口头里。
2. **找接口**：谁调用我的函数、传进来什么、要拿走什么。看测试文件顶部的 `import` 行和调用那一行就够了。
3. **最小实验**：进 REPL，喂一个真实输入，看看现在手里有什么。别在脑子里想象，让机器打给你看。
4. **写最丑能跑版**：不求优雅，只求"交出去的东西形状对"。
5. **跑测试 → 读结论行 → 找属于我的那一帧 → 改 → 存盘 → 再跑**。写三行跑一次，别憋 20 行。
6. **提交 + 三行笔记**。没有 commit，这一天等于没发生。

这六步不是天赋，是肌肉记忆，走到第十次就不用想了。

## Step 0 · 3 分钟 · 把环境跑起来

```bash
cd /d/Source/m0-lab
uv venv
source .venv/Scripts/activate
uv pip install pytest
python -c "import sys; print(sys.prefix)"
```

最后一条的输出里出现 `.venv` 就对了。
常见卡点：激活脚本没跑（`sys.prefix` 指向 `D:\Develop\Python`）、或者你用的是 PowerShell 却要写 `.venv\Scripts\activate`（不带 source）。

## Step 1 · 2 分钟 · 今天到底要做什么

一句话：**把 `data/` 里所有 JSON 的订单倒进一个大列表；有两个文件倒不进去，你要能说出它们的名字并打印出来。**

今天**不做**的事（做了反而挂测试）：不改金额、不去重、不算钱、不排序、不导出。

只需要看懂 `tests/test_day01.py` 里这 5 个函数名在要求什么：

1. `test_only_json_files_and_sorted` —— 给我 4 个文件名，按名字排好序，`readme.txt` 不算
2. `test_load_returns_11_raw_records` —— 一共 11 条记录，每条都有 `order_id`
3. `test_day1_does_not_clean` —— 别顺手清洗，脏值必须还在
4. `test_two_files_skipped_and_reported` —— 跳过 `broken.json` 和 `orders_2026-08.json`，而且要 **print 出来**
5. `test_order_of_paths_does_not_matter` —— 我把文件顺序倒过来传给你，结果条数不能变

## Step 2 · 7 分钟 · 先在解释器里玩明白，别急着写函数

打开解释器：`python`（看到 `>>>` 就进去了）。**逐行自己敲**，一行一行看输出：

```python
from pathlib import Path
import json
ps = sorted(Path("data").glob("*.json"))
[p.name for p in ps]                      # 期望：4 个文件名
json.loads(ps[1].read_text(encoding="utf-8"))      # 成功：一个列表，6 条
json.loads(ps[0].read_text(encoding="utf-8"))      # 亲眼看到它炸：JSONDecodeError
type(json.loads(ps[3].read_text(encoding="utf-8")))   # 成功，但是 dict 不是 list
exit()
```

这 7 行跑完，今天的设计就已经浮出来了：**两个文件"倒不进去"的原因不一样**——一个是解析直接抛异常，一个是解析成功但形状不对。你要分别处理这两种。
（`ps[0]` 是 broken.json，`ps[1]` 是 orders_2026-06.json，`ps[3]` 是 orders_2026-08.json。）

跑不通就别往下走，把屏幕上的红字原文发我。

## Step 3 · 8 分钟 · 写 find_data_files

把 Step 2 里那三行搬进函数，加个 `return`。写完只跑这一个用例：

```bash
python -m pytest tests/test_day01.py -k only_json -v
```

`-k` 是"只跑名字里带这个词的用例"，别每次看 18 个结果。绿了再往下。

## Step 4 · 12 分钟 · 写 load_records（今天唯一真难的地方）

你只需要 4 个零件：`read_text`、`json.loads`、`try/except json.JSONDecodeError`、`isinstance(obj, list)`。

三个提示，按顺序看，看一个试一个：

1. `json.loads` 抛异常时，你那个 `for` 循环会怎样？——这就是为什么 `try` 必须写在**循环里面**。想清楚这句，函数就对了。
2. 形状不对的那个文件怎么挡？`isinstance(obj, list)` 为假就跳过，不要试图"顺手把 `records` 取出来"（那是 Day 2 以后的事，今天会挂测试）。
3. print 什么？测试只检查 stdout 里有没有那两个文件名，所以 `print(f"skip {name}: 原因")` 就够了。

写完跑全部：`python -m pytest tests/test_day01.py -v` → 5 passed。

**自检问题**（答不上来就别收工，答上来发给我）：
- 为什么 `except` 不能写在 for 外面？
- 如果 `data/` 目录整个不存在，你的函数会崩还是返回空？哪个行为更该要？
- 我把 `orders_2026-08.json` 的顶层改成列表，你的代码需要动吗？

## Step 5 · 5 分钟 · 留下证据

```bash
git init
git add -A
git commit -m "day1: load records, skip broken and non-list files"
git log --oneline
```

然后填 `notes.md` 的 Day 1 三行。**第三行写不出来 = 今天白过**，回去把 Step 2 那 7 行再跑一遍。

---

## 今晚不许做的事

不许看 pytest 文档、不许研究类型注解和 fixture 的机制、不许碰 Day 2/Day 3、不许为了少写两行去改测试或改 `src/report.py` 的签名、不许让 AI 生成 `load_records` 的第一版（你可以写完让它挑毛病）。

视频今晚一条都不该看。你现在缺的不是概念，是"把这 4 个零件拼起来"的十分钟——拼完再回头看，会发现没一个概念需要视频。
