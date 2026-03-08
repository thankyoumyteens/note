# 把拦截器和路由抽离到单独的文件中

在真实项目中，我们通常会按功能划分文件：

```
my_project/
├── core/
│   └── exceptions.py       <-- 全局异常拦截器
├── routers/                <-- 存放所有路由模块
│   ├── __init__.py
│   └── users.py            <-- 用户相关的所有接口
└── main.py                 <-- 终极瘦身版：只负责组装和启动
```

### 1. 编写 core/exceptions.py

在这个文件里，我们完全不需要导入 FastAPI 实例（不需要 app = FastAPI()）。我们只写一个普通的异步函数。

```py
# core/exceptions.py
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# 注意：这里不再使用 @app.exception_handler 装饰器
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_errors = []

    # exc.errors() 返回的是一个包含所有错误字典的列表
    for error in exc.errors():
        # 1. 获取出错的字段路径（例如 ["body", "user", "phone"] 转换成 "body -> user -> phone"）
        # 这对于嵌套的复杂 JSON 非常有用，能精准定位是哪里的字段报错
        loc_path = " -> ".join([str(x) for x in error["loc"]])

        # 获取最底层的具体字段名，方便做特定判断
        field_name = error["loc"][-1] if error["loc"] else "未知字段"

        # 2. 获取 Pydantic 给出的错误类型和上下文
        err_type = error.get("type")
        ctx = error.get("ctx", {})  # 上下文里会有 min_length, pattern 等详细数据

        # 3. 核心翻译机：根据不同的 type 给出对应的中文提示
        if err_type == "missing":
            error_msg = "该字段是必填项，不能漏掉或为空哦！"
        elif err_type == "string_pattern_mismatch":
            # 正则匹配失败。我们可以根据具体字段名定制，也可以给出通用提示
            if "phone" in str(field_name).lower():
                error_msg = "请输入正确的11位大陆手机号码！"
            else:
                # 还可以把写在 Field 里的正则规则 (ctx['pattern']) 打印出来给用户看
                error_msg = f"格式不符合要求，需要满足规则：{ctx.get('pattern')}"
        elif err_type == "string_too_short":
            error_msg = f"字符太短啦，至少需要 {ctx.get('min_length')} 个字符"
        elif err_type == "string_too_long":
            error_msg = f"字符太长啦，最多只能输入 {ctx.get('max_length')} 个字符"
        elif err_type == "int_parsing":
            error_msg = "数据类型错误，这里必须输入一个整数！"
        elif err_type == "greater_than_equal":
            error_msg = f"数值太小了，必须大于或等于 {ctx.get('ge')}"
        else:
            # 如果遇到我们还没翻译的罕见错误，兜底返回 Pydantic 自带的英文提示
            error_msg = error.get("msg", "参数校验失败")

        custom_errors.append({
            "定位": loc_path,
            "字段": field_name,
            "提示": error_msg
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 40001,  # 你可以自定义业务状态码
            "message": "提交的数据存在问题，请检查后重试",
            "details": custom_errors
        },
    )
```

### 2. 编写 routers/users.py

```py
# routers/users.py
from fastapi import APIRouter
from pydantic import BaseModel, Field

# 1. 创建一个 APIRouter 实例
# prefix="/users"：这个路由器下所有的接口，都会自动带上 /users 前缀！
# tags=["用户管理"]：这会让你的 /docs 接口文档自动将这些接口归类到一个叫“用户管理”的折叠面板下，极其优雅。
router = APIRouter(
    prefix="/users",
    tags=["用户管理"]
)

# 定义需要用到的 Pydantic 模型
class UserSignup(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    phone_number: str = Field(pattern=r"^1[3-9]\d{9}$")
    age: int = Field(ge=18)

# 2. 使用 @router 替代之前的 @app
# 注意：因为上面写了 prefix="/users"，所以这里的 "/" 实际上代表的就是 "/users/"
@router.post("/")
def register_user(user: UserSignup):
    return {"message": f"用户 {user.username} 注册成功！"}

# 我们再顺手加一个获取用户信息的接口
# 这里的 "/{user_id}" 实际上代表的是 "/users/{user_id}"
@router.get("/{user_id}")
def get_user(user_id: int):
    return {"message": "获取成功", "user_id": user_id}
```

### 3. 在 main.py 中注册异常处理器和 Router

现在的 main.py 会变得极其清爽，只负责组装各个模块。

```py
# main.py
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

# 1. 导入我们拆分出去的模块
from core.exceptions import custom_validation_exception_handler
from routers import users  # 导入 users 路由模块

app = FastAPI(title="我的棒棒应用")

# 注册之前写的全局异常处理器
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)

# 2. 核心：将 router 挂载到 app 上
app.include_router(users.router)

# 如果以后你有商品模块，直接这样继续挂载即可：
# from routers import products
# app.include_router(products.router)
```
