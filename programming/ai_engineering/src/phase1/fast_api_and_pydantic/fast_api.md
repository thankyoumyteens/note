# 写一个最简单的 FastAPI 应用

### 1. 环境准备与安装

首先，确保你安装了 Python 3.8 或更高版本。然后，打开终端并安装 FastAPI 和 Uvicorn（Uvicorn 是运行 FastAPI 的 ASGI 服务器）。

```sh
pip install fastapi "uvicorn[standard]"
```

安装 fastapi 时会自动安装 pydantic，因为它是 FastAPI 的核心依赖。

### 2. 创建一个名为 main.py 的文件

```py
from fastapi import FastAPI

# 创建一个 FastAPI 实例
app = FastAPI()

# 定义一个 GET 请求的路由
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

### 3. 运行

在终端中输入以下命令：

```sh
uvicorn main:app --reload
```

解释：main 是文件名，app 是 FastAPI 实例名，--reload 表示代码修改后自动重启服务器，非常适合开发阶段。

打开浏览器访问 [http://127.0.0.1:8000](http://127.0.0.1:8000)，你就能看到返回的 JSON 数据了。
