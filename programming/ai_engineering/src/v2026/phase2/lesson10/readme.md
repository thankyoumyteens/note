# 创建 README.md

让 `python-tools/` 的用途和运行方式清晰。

辅助工具目录也需要 README，否则后续容易忘记怎么运行。

#### 代码

文件：

```text
python-tools/README.md
```

内容：

````markdown
# python-tools

Python helper tools for the Java AI Gateway project.

## Purpose

This directory is for auxiliary AI tooling:

- calling Java AI Gateway APIs
- validating responses with Pydantic
- batch processing
- eval dataset utilities
- future document parsing and RAG preparation

Python is auxiliary in this course. Java remains the main backend language.

## Setup

```bash
uv sync
```

## Run

Make sure the Java AI Gateway is running at:

```text
http://localhost:8080
```

Then run:

```bash
uv run python scripts/call_chat.py
```

Optional environment variable:

```bash
export AI_GATEWAY_BASE_URL="http://localhost:8080"
```
````

#### 代码说明

README 明确了 Python 的边界：

```text
Python 是辅助工具，不是主后端
```
