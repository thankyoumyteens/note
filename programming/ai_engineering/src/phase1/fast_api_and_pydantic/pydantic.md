# 引入 Pydantic 处理数据

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
