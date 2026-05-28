# 添加 Python 依赖

本课只需要三个核心依赖：

```text
httpx：调用 Java AI Gateway
pydantic：校验响应结构
python-dotenv：读取 .env 配置
```

#### 代码

进入 `python-tools/`：

```bash
cd python-tools
uv add httpx pydantic python-dotenv
```

#### 代码说明

这会更新：

```text
pyproject.toml
uv.lock
```

以后运行脚本时可以用：

```bash
uv run python scripts/call_chat.py
```

### pyproject.toml

`pyproject.toml` 是现代 Python 项目的核心配置文件。这里不用做复杂打包，只要保证依赖和 Python 版本清晰即可。

#### 代码

文件：

```text
python-tools/pyproject.toml
```

参考内容：

```toml
[project]
name = "ai-gateway-tools"
version = "0.1.0"
description = "Python helper tools for the Java AI Gateway course project"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "httpx",
    "pydantic",
    "python-dotenv",
]
```

#### 代码说明

`requires-python = ">=3.11"` 是为了避免过旧 Python 版本带来的类型语法问题。
