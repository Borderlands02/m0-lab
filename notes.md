# 卡点与三行笔记

每天结束时填，一天一节。**第三行写不出来，就说明这天白过了。**

## Day 1

- 关键洞察：看README文档
- 我卡在哪（具体到函数和那一次报错的原文）：find_data_files没返回值,load_records中`read_text`、`json.loads`、`try/except json.JSONDecodeError`、isinstance(obj, list)`,append(),extend(),这些都不了解.还有填入的类型不对.没有理解到每一步的原因.
- 下次出现什么信号，该想到今天这段：数据出现崩溃,格式不对时

## Day 2

- 关键洞察：
- 我卡在哪：
- 下次出现什么信号：

## Day 3

- 关键洞察：
- 我卡在哪：
- 下次出现什么信号：
- 如果让我重做一遍，我会先写哪个函数：

## 我要问的 5 个问题（自己先答，答不上来的就是明天要补的）

1. `p`、`p.name`、`str(p)` 三者的**类型**和**值**分别是什么？合同（测试）要的是哪一个？
2. `find_data_files` 少了 `return` 时，报错为什么打在**测试文件**第 14 行，而不是 `report.py` 里？
3. `try` 为什么必须写在 `for` **里面**？写在外面会出什么具体后果？
4. `except json.JSONDecodeError:` 接不住哪一种失败？（提示：如果 `read_text` 自己炸了）
5. `append` 和 `extend` 差在哪？把 `records.extend(data)` 改成 `records.append(data)`，`len(records)` 会变成几？**真跑一遍再答**。
