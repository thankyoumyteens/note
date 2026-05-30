# 部署项目

## 方式 1：应用部署，推荐给 FastAPI / 脚本 / 服务

这种最常用。**不需要打 wheel 包**，直接把项目代码、`pyproject.toml`、`uv.lock` 部署到服务器，然后在服务器执行：

```bash
uv sync --no-dev --frozen
```

再运行服务：

```bash
uv run python main.py
```

或 FastAPI：

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`uv sync` 的作用是根据 `uv.lock` 同步环境；`--no-dev` 表示不安装开发依赖；`--frozen` 表示不更新 lockfile，只按已有锁文件安装，适合部署环境。

推荐部署文件：

```text
my-project/
├── pyproject.toml
├── uv.lock
├── .python-version
├── main.py
└── app/
```

不要上传：

```text
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
```

因为服务器上应该重新用 `uv sync` 构建环境。

---

## 方式 2：打包成 wheel/sdist，适合发布库或内部包

如果你的项目是一个 Python package，比如要发布到 PyPI、私有仓库，或者让别的项目安装，就用：

```bash
uv build
```

构建后会生成：

```text
dist/
├── your_project-0.1.0.tar.gz
└── your_project-0.1.0-py3-none-any.whl
```

发布到仓库：

```bash
uv publish
```

但如果你只是部署一个 Web 服务或脚本项目，一般不需要 `uv build`。

---

## Docker 部署示例

如果你要部署到服务器，最稳的是 Docker。示例 `Dockerfile`：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --no-dev --frozen

COPY . .

CMD ["uv", "run", "python", "main.py"]
```

如果是 FastAPI：

```dockerfile
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建：

```bash
docker build -t my-project:latest .
```

运行：

```bash
docker run -p 8000:8000 my-project:latest
```
