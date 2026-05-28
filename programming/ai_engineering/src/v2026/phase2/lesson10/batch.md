# 创建批量调用雏形

为后续 eval dataset 和批处理任务准备一个可复用函数。

第 7 课的 eval 脚本已经能批量调用接口，但那是脚本式写法。本课开始把批量能力沉淀到 Python 包里。

#### 代码

文件：

```text
python-tools/src/ai_gateway_tools/batch_eval.py
```

代码：

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from ai_gateway_tools.client import AiGatewayClient


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """
    读取 JSONL 文件。

    JSONL 格式：每一行是一个独立 JSON。
    """
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    """写入 JSONL 文件。"""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_chat_batch(inputs: list[str]) -> list[dict[str, Any]]:
    """
    批量调用 /api/ai/chat。

    当前只是批处理雏形。
    后续 eval、文档处理、RAG 数据准备会继续复用这种模式。
    """
    results: list[dict[str, Any]] = []

    with AiGatewayClient() as client:
        for index, text in enumerate(inputs):
            try:
                response = client.chat(text)
                results.append(
                    {
                        "index": index,
                        "input": text,
                        "success": True,
                        "answer": response.answer,
                        "error": None,
                    }
                )
            except Exception as exc:
                results.append(
                    {
                        "index": index,
                        "input": text,
                        "success": False,
                        "answer": None,
                        "error": str(exc),
                    }
                )

    return results
```

#### 代码说明

这里的核心是：

```text
单条调用失败，不影响整个批次继续执行
```

这和后续 eval、文档处理、RAG 数据准备非常重要。
