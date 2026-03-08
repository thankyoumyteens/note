# 使用 Pydantic 进行更复杂的数据校验

使用 Pydantic 进行更严格的数据校验，主要依赖于它的核心武器：Field 函数。Field 允许你在基础的数据类型（如 str、int）之上，附加丰富的元数据和校验规则。

让我们以一个“用户注册”的场景为例。我们需要限制用户名长度、验证手机号格式（使用正则表达式），并限制用户的年龄。

```py
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class UserSignup(BaseModel):
    # 1. 限制字符串长度：使用 min_length 和 max_length
    username: str = Field(
        min_length=3,
        max_length=15,
        # 注意：description 并不是用来定制报错信息的
        # 它的唯一作用是给 OpenAPI 文档提供说明文字
        description="用户名，长度必须在3到15个字符之间"
    )

    # 2. 正则表达式：使用 pattern (注意：Pydantic V1 中叫 regex)
    # 这里的正则表示：以1开头，第二位是3-9，后面跟着9位数字（标准的中国大陆手机号）
    phone_number: str = Field(
        pattern=r"^1[3-9]\d{9}$",
        description="11位有效的中国大陆手机号码"
    )

    # 3. 补充：数值大小限制
    # ge (Greater than or Equal): >=
    # le (Less than or Equal): <=
    # gt (Greater Than): >
    # lt (Less Than): <
    age: int = Field(
        ge=18,
        le=120,
        description="年龄，必须满18岁且小于等于120岁"
    )

    # 4. 设置默认值
    # 如果希望某个带有 Field 校验的字段是可选的，可以这样写：
    bio: str | None = Field(default=None, max_length=200, description="个人简介，最多200字")


@app.post("/users")
def register_user(user: UserSignup):
    # 如果代码能走到这里，说明 user 数据绝对是合法且安全的
    return {"message": f"用户 {user.username} 注册成功！", "data": user.model_dump()}
```

## 自定义报错信息

### 方案一：使用 @field_validator 自定义校验

与其依赖 Field(min_length=3) 自动生成的英文报错，我们可以自己写一个校验函数。只要校验不通过，我们就主动抛出一个带有中文信息的 ValueError。

```py
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class UserSignup(BaseModel):
    # 这里我们只定义类型，去掉 min_length 和 max_length
    username: str = Field(description="用户名")

    # 使用 @field_validator 装饰器，指定要校验的字段
    @field_validator('username')
    @classmethod
    def check_username_length(cls, value: str) -> str:
        if len(value) < 3 or len(value) > 15:
            # 这里抛出的 ValueError 的内容，就会变成 422 报错中的 msg
            raise ValueError('用户名长度必须在3到15个字符之间！')
        return value


@app.post("/users")
def register_user(user: UserSignup):
    return {"message": "成功", "user": user.model_dump()}
```

测试效果： 如果现在传入长度为 2 的用户名，返回的 JSON 会变成这样：

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "username"],
      "msg": "Value error, 用户名长度必须在3到15个字符之间！",
      "input": "ab"
    }
  ]
}
```

### 方案二：全局重写 FastAPI 的 422 异常拦截器（最强大，适合项目级开发）

这需要用到 FastAPI 的全局异常处理机制：

```py
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()


# --- 核心：重写全局 422 异常处理器 ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
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


# --- 下面是测试用的 Pydantic 模型和路由 ---
class UserSignup(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    phone_number: str = Field(pattern=r"^1[3-9]\d{9}$")
    age: int = Field(ge=18)
    email: str  # 没有设置默认值，所以是必填项


@app.post("/users")
def register_user(user: UserSignup):
    return {"message": "校验通过，注册成功！"}
```

测试效果： 客户端收到的报错不再是一大段英文，而是你完全自定义的中文结构：

```json
{
  "code": 40001,
  "message": "提交的数据存在问题，请检查后重试",
  "details": [
    {
      "定位": "body -> username",
      "字段": "username",
      "提示": "字符太短啦，至少需要 3 个字符"
    },
    {
      "定位": "body -> phone_number",
      "字段": "phone_number",
      "提示": "请输入正确的11位大陆手机号码！"
    },
    {
      "定位": "body -> age",
      "字段": "age",
      "提示": "数据类型错误，这里必须输入一个整数！"
    }
  ]
}
```
