# 依赖注入

在 FastAPI 中，依赖注入的概念极其简单：“在执行你的业务逻辑之前，先帮我准备好我需要的东西（或者先帮我做个检查）。”

常见的应用场景包括：

1. 提取公共参数（比如每个接口都要做分页 skip 和 limit）。
2. 用户权限验证（比如检查请求头里有没有合法的 Token）。
3. 获取数据库连接（每次请求分配一个连接，请求结束自动回收）。

## 场景一：提取公共参数

假设你有两个接口：查商品列表（/items/）和查用户列表（/users/）。它们都需要支持分页功能（skip 和 limit），以及一个搜索关键字（q）。

如果不使用依赖注入，你得在每个路由函数里把这三个参数写一遍。如果有10个接口，你得写10遍。

使用依赖注入改造：

```py
from fastapi import FastAPI, Depends

app = FastAPI()


# 1. 定义一个普通的 Python 函数，这就是我们的“依赖项”
# 这里的参数定义方式，和之前写在路由里的完全一样！
def common_parameters(q: str | None = None, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}


# 2. 在路由中使用 Depends() 注入这个依赖
@app.get("/items/")
def read_items(commons: dict = Depends(common_parameters)):
    # FastAPI 会自动先去执行 common_parameters 函数，把返回的字典赋值给 commons
    return {"message": "商品列表", "params": commons}


@app.get("/users/")
def read_users(commons: dict = Depends(common_parameters)):
    # 完美复用！不需要重新写 skip, limit, q 了
    return {"message": "用户列表", "params": commons}
```

当你访问 /items/?q=phone&skip=5 时，FastAPI 会聪明地把 q 和 skip 传给 common_parameters，然后把结果交给你的路由代码。而且，这些参数依然会完美地出现在交互式文档（Swagger UI）中！

## 场景二：权限验证

假设我们有一个“修改个人资料”的接口，必须验证用户的请求头（Header）中是否携带了正确的 X-Token。

```py
from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()


# 1. 定义权限验证依赖
def verify_token(x_token: str = Header(description="用户的身份令牌")):
    # 模拟检查 token 是否合法
    if x_token != "super-secret-token":
        # 如果不合法，直接抛出 HTTP 异常，请求根本不会到达你的业务代码！
        raise HTTPException(status_code=401, detail="Token 不合法或已过期")

    # 如果合法，甚至可以返回当前用户的信息
    return {"user_name": "VIP_User", "token": x_token}


# 2. 注入验证依赖
@app.post("/profile/update")
def update_profile(current_user: dict = Depends(verify_token)):
    # 只要代码能走到这里，说明 Token 绝对是合法的！
    # 你甚至可以直接拿到依赖函数返回的用户信息
    return {"message": f"欢迎你，{current_user['user_name']}，资料修改成功！"}
```

## Router 级别依赖

如果你有一个依赖项（比如验证 Token），你希望某个 Router 下的所有接口都强制执行，而不想每个函数都写一遍 Depends()，你可以直接把它挂在 APIRouter 上！

```py
from fastapi import APIRouter, Depends


# 定义验证函数
def check_admin():
    pass  # 这里写验证逻辑...


# 在创建 Router 时，直接传入 dependencies 列表！
# 这样一来，这个 router 下的所有接口，都必须先通过 check_admin 验证
router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(check_admin)]
)


@router.get("/dashboard")
def get_dashboard():
    # 只有 admin 才能看到
    return {"data": "机密数据"}
```
