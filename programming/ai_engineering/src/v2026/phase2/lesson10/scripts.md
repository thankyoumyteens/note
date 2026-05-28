# 创建命令行测试脚本

用一个最小脚本验证 Python 工具能调用 Java AI Gateway。

这个脚本只是本地测试入口，不是生产 CLI。后续如果需要，可以再升级成 argparse / typer。

#### 代码

文件：

```text
python-tools/scripts/call_chat.py
```

代码：

```python
from ai_gateway_tools.client import AiGatewayClient


def main() -> None:
    """最小命令行测试脚本。"""
    with AiGatewayClient() as client:
        result = client.chat("请用一句话解释什么是 RAG")
        print(result.model_dump_json(indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

#### 代码说明

`model_dump_json` 会把 Pydantic 对象输出为 JSON 字符串，便于查看。

### 修改 python-tools/pyproject.toml

追加下面内容

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/ai_gateway_tools"]
```

`requires = ["hatchling"]` 表示构建这个项目之前，需要先准备 hatchling。你可以把它理解成 Java 里的构建工具依赖，比如：

```
Maven / Gradle 负责打包 Java 项目
hatchling 负责打包 Python 项目
```

`build-backend = "hatchling.build"` 表示：真正负责构建项目的后端是 hatchling.build，也就是说，当 uv sync 或 uv pip install -e . 试图安装当前项目时，会调用 hatchling.build 来判断：

```
这个项目叫什么？
有哪些 Python 包？
包在哪里？
应该怎么安装？
```

`packages = ["src/ai_gateway_tools"]` 这一段是告诉 hatchling：我要打包的 Python 包在 src/ai_gateway_tools 目录下。

### 正确运行方式

```bash
cd python-tools
uv sync
uv run python scripts/call_chat.py
```
