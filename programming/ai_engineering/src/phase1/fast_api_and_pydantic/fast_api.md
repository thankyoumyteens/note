# 写一个最简单的 FastAPI + Pydantic 应用

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

## 引入 Pydantic 处理数据

当客户端向服务器发送数据（例如通过 POST 请求创建用户）时，我们需要确保数据包含必填字段，且数据类型正确。这就是 Pydantic 大显身手的地方。

修改你的 main.py 文件：

```py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# 1. 定义 Pydantic 数据模型
class Item(BaseModel):
    name: str
    description: Optional[str] = None  # 可选字段，默认值为 None
    price: float
    tax: Optional[float] = None


# 2. 在路由中使用该模型
@app.post("/items")
def create_item(item: Item):
    # FastAPI 会自动将请求体中的 JSON 转换为这里的 item 对象
    # 你可以直接访问它的属性，甚至可以享受到编辑器的代码提示！
    item_dict = item.model_dump()  # 将对象转换为字典 (Pydantic v2 用法)

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict
```

当你向 /items 发送 POST 请求时，FastAPI 会读取请求体（JSON），交给 Pydantic 验证。

- 如果数据不对（比如 price 传了一个字符串 "免费"），FastAPI 会自动返回一个清晰的 422 错误提示给客户端。
- 如果数据正确，它会被转换成 Item 类的实例，你可以直接通过 item.name 来调用，非常优雅。

## 自动生成接口文档

FastAPI 会根据你的代码和 Pydantic 模型，自动生成符合 OpenAPI 标准的 API 文档。

保持你的服务器运行，在浏览器中访问：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

你会看到一个漂亮的 Swagger UI 界面。

1. 点开 POST /items/ 接口。
2. 点击右上角的 "Try it out"。
3. 在请求体框内输入 JSON 测试数据：
   ```json
   {
     "name": "机械键盘",
     "description": "青轴，带 RGB 背光",
     "price": 299.5,
     "tax": 10.5
   }
   ```
4. 点击 "Execute"。你不仅能看到请求成功，还能直接在界面上测试各种数据类型错误的拦截情况。
