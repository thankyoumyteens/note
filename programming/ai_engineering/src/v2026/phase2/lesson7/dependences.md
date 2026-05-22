# 安装 Python 依赖

如果你还没有 Python eval 环境，先用最小方式：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests
```

如果你已经在后面准备使用 `uv`，也可以：

```bash
uv add requests
```

当前第 7 课不强制引入完整 `python-tools/`。

## 为什么用 Python 写 eval

Java 主服务负责生产接口。

Python 适合做：

```text
批量请求接口
读取 JSONL 数据集
统计通过率
输出失败样本
快速实验
```

这符合当前路线：

```text
Java 主线
Python 辅助
```
