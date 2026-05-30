# 管理依赖

`uv` 管理依赖主要靠这几个文件和命令：

```text
pyproject.toml  记录“项目需要什么依赖”
uv.lock         记录“最终解析出来的精确版本”
.venv/          项目的虚拟环境，实际安装包的地方
```

官方文档的说法是：`uv add` / `uv remove` 用来修改项目依赖，也可以直接编辑 `pyproject.toml`；`lock` 是把依赖解析成 lockfile，`sync` 是把 lockfile 里的包安装到项目环境。([Astral Docs][1])

## 1. 添加依赖

比如添加 `requests`：

```bash
uv add requests
```

添加指定版本范围：

```bash
uv add "requests>=2.32"
```

添加多个：

```bash
uv add requests httpx pydantic
```

执行后，uv 会更新：

```text
pyproject.toml
uv.lock
.venv/
```

也就是：声明依赖、锁定精确版本、安装到虚拟环境。

## 2. 添加开发依赖

比如测试、格式化、lint 工具：

```bash
uv add --dev pytest ruff mypy
```

这类依赖通常用于开发环境，不是你的应用运行时必须依赖。

## 3. 删除依赖

```bash
uv remove requests
```

删除开发依赖：

```bash
uv remove --dev pytest
```

删除后 uv 会同步更新 `pyproject.toml` 和 `uv.lock`。

## 4. 同步依赖

别人 clone 你的项目后，通常执行：

```bash
uv sync
```

它会根据 `uv.lock` 创建/更新 `.venv`，让本地环境和锁文件一致。

常见流程：

```bash
git clone xxx
cd my-project
uv sync
uv run python main.py
```

## 5. 运行时自动同步

很多时候你不需要手动 `uv sync`，因为：

```bash
uv run python main.py
```

会在运行前检查项目环境是否和 `uv.lock` 一致，不一致时会自动同步。

所以日常可以直接：

```bash
uv run python main.py
```

## 6. 更新依赖

如果你想升级 lockfile 里的依赖版本：

```bash
uv lock --upgrade
```

如果只想升级某个包：

```bash
uv lock --upgrade-package requests
```

然后同步：

```bash
uv sync
```

也可以直接重新 add 一个版本约束：

```bash
uv add "requests>=2.32,<3"
```

## 7. 安装生产依赖，不装开发依赖

部署时如果不想安装 dev 依赖，可以用：

```bash
uv sync --no-dev
```

开发环境则直接：

```bash
uv sync
```
