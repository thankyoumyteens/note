# 初始化 uv 项目

```bash
uv init --python 3.13 agent-dev-py
cd agent-dev-py
# 安装依赖：
uv add openai anthropic pydantic-settings
```

推荐项目结构：

```text
agent-dev-py
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
└── src
    └── llm_api_demo
        ├── __init__.py
        ├── settings.py
        ├── clients.py
        └── main.py
```

创建目录结构：

```bash
mkdir -p src/llm_api_demo
touch src/llm_api_demo/__init__.py
touch src/llm_api_demo/settings.py
touch src/llm_api_demo/clients.py
touch src/llm_api_demo/main.py
```

## 修改 pyproject.toml

重点是锁定 Python 版本范围：

```toml
requires-python = ">=3.13,<3.14"
```

原因是：这样可以避免 uv 在未来自动帮你跑到 3.14 / 3.15 后出现依赖行为变化。

在文件末尾追加：

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/llm_api_demo"]
```

否则 uv run 时可能找不到 src 下的包。

## 修改 `.gitignore`

```gitignore
.env
.venv
__pycache__/
*.pyc
```

## 完整调用链

```text
                    ┌──────────────┐
                    │    main.py   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  LlmRouter   │
                    └──────┬───────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
       OpenAI SDK     OpenAI SDK    Anthropic SDK
             │             │             │
             │             │             │
             ▼             ▼             ▼
           OpenAI       DeepSeek       Claude
         Responses      Chat API      Messages API
```
