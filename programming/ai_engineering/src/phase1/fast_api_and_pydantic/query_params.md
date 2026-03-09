# 路径参数与查询参数

## 路径参数 (Path Parameters)

路径参数是你用来定位具体资源的。它直接嵌在 URL 的路径中。

在 FastAPI 中，定义路径参数非常直观：

1. 在 `@router.get()` 或 `@app.get()` 中用花括号 `{}` 括起来。
2. 在处理函数的参数列表中声明同名变量，并指定类型。

```py
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int):
    # 如果用户访问 /items/3，这里的 item_id 就会是整数 3
    # 如果用户访问 /items/foo，FastAPI 会自动拦截并返回 422 错误（类型错误）
    return {"item_id": item_id}
```

### 校验路径参数

对于路径参数，FastAPI 提供了一个专属的兄弟函数：Path。我们可以用它来限制 item_id 必须大于 0：

```py
from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(
        # Path 的用法和 Field 几乎一模一样
        # ge=1 表示 Greater than or Equal to 1
        item_id: int = Path(ge=1, description="商品的唯一ID，必须是正整数")
):
    return {"item_id": item_id, "status": "合法参数"}
```

## 查询参数 (Query Parameters)

查询参数通常用于过滤、排序或分页。它们跟在 URL 的 `?` 后面，多个参数用 & 连接（比如 `?q=keyword&skip=0&limit=10`）。

任何在处理函数中声明了，但没有在路径 `{}` 中出现的参数，都会被自动识别为查询参数！

```py
from fastapi import FastAPI

app = FastAPI()


@app.get("/items")
def list_items(skip: int = 0, limit: int = 10, q: str | None = None):
    # 访问 /items?skip=5&limit=20&q=phone
    # skip 和 limit 有默认值，所以是可选的。如果不传，就是 0 和 10。
    # q 的类型是 str | None（字符串或空），默认是 None，所以也是可选的。
    return {"skip": skip, "limit": limit, "search_query": q}
```

### 校验查询参数

为了对查询参数进行严格校验（比如限制搜索关键字的长度），我们需要使用 Query 函数：

```py
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/search")
def search_items(
        # 限制关键字 q 最小长度为3，最大长度为50
        q: str | None = Query(default=None, min_length=3, max_length=50, description="搜索关键字")
):
    if q:
        return {"message": f"正在搜索: {q}"}
    return {"message": "显示所有商品"}
```

## 路径参数 + 查询参数 + 请求体 混搭

```py
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()


# 1. 这是用于校验请求体 (Body) 的 Pydantic 模型
class ItemUpdate(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(gt=0)


# 2. 路由定义
@app.put("/items/{item_id}")
def update_item(
        # item_id 在路径中定义了，所以这是【路径参数】
        item_id: int = Path(ge=1, description="商品ID"),

        # send_notify 既不在路径中，也不是 Pydantic 模型，所以这是【查询参数】
        send_notify: bool = Query(default=False, description="是否发送通知"),

        # item 的类型继承自 BaseModel，所以这是【请求体 (Body) JSON 数据】
        item: ItemUpdate = None
):
    result = {"item_id": item_id, "updated_data": item.model_dump()}
    if send_notify:
        result["notification"] = "已发送更新通知！"

    return result
```
