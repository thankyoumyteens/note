# 初始化 uv 项目

## 为什么需要 uv？

传统 Python 环境管理常见问题：

```text
pip 慢
依赖冲突
venv 管理麻烦
requirements.txt 不稳定
不同机器复现困难
```

`uv` 是现在 Python 生态中很常用的快速包管理和环境工具。官方文档说明，uv 可以作为 `pip`、`pip-tools`、`virtualenv` 常用命令的替代方案，并提供更快的依赖解析和可复现能力。

本课程中，uv 只承担一个职责：

```text
快速创建 Python 项目环境并安装依赖
```

## 创建目录

在 `ai-gateway` 根目录执行：

```bash
mkdir -p python-tools/src
mkdir -p python-tools/data
cd python-tools
```

---

## 初始化 uv 项目

如果你还没安装 uv，先安装：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

然后检查：

```bash
uv --version
```

初始化项目：

```bash
uv init --bare
```

指定 Python 版本，例如：

```bash
uv python pin 3.12
```

添加依赖：

```bash
uv add httpx pydantic python-dotenv
```

说明：

```text
httpx：HTTP 客户端
pydantic：结构化数据校验
python-dotenv：读取 .env
```
