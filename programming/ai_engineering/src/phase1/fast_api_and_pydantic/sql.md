# 结合 SQLAlchemy 或 SQLModel 进行真实的数据库增删改查

### 1. 安装依赖

```sh
pip install sqlmodel
```

### 2. 新增和查询

```py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


# ==========================================
# 1. 定义数据模型 (既是 Pydantic，又是数据库表)
# ==========================================

# table=True 告诉 SQLModel：请在数据库里为我建一张真实的表
class User(SQLModel, table=True):
    # Field(primary_key=True) 设为主键，自动自增
    id: int | None = Field(default=None, primary_key=True)
    # 兼顾 Pydantic 校验和数据库索引
    username: str = Field(index=True, min_length=3, max_length=20)
    age: int = Field(ge=0, le=120)


# ==========================================
# 2. 配置数据库引擎 (Engine)
# ==========================================
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
# echo=True 会在终端打印底层的 SQL 语句，方便学习和调试
engine = create_engine(sqlite_url, echo=True)


# ==========================================
# 3. 核心：定义数据库会话的依赖注入 (Dependency)
# ==========================================
def get_session():
    # with 语句确保：哪怕业务代码报错了，Session 也会被安全地关闭，不漏水！
    with Session(engine) as session:
        yield session  # 把 session 交给路由函数去用


# ==========================================
# 4. 初始化 FastAPI 与数据库表
# ==========================================

# lifespan 用于在项目启动时自动建表
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)  # 启动时建表
    # 应用运行...
    yield
    # 关闭时的清理工作可以写在这里


app = FastAPI(lifespan=lifespan)


# ==========================================
# 5. 编写 CRUD 接口 (使用依赖注入获取 session)
# ==========================================

# 创建用户 (Create)
@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    # 这里的 user 已经是校验过格式的合法数据了
    session.add(user)  # 1. 添加到会话
    session.commit()  # 2. 提交到数据库保存
    session.refresh(user)  # 3. 刷新数据（为了获取数据库自动生成的 id）
    return user


# 查询用户列表 (Read)
@app.get("/users/", response_model=list[User])
def read_users(session: Session = Depends(get_session)):
    # select(User) 生成 SQL 查询，session.exec() 执行查询，.all() 获取全部结果
    users = session.exec(select(User)).all()
    return users


# 根据 ID 查询单个用户 (Read)
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    # session.get() 是通过主键查询的最快方式
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="哎呀，没找到这个用户！")
    return user
```

路由里 `session: Session = Depends(get_session)` 的执行过程：

1. FastAPI 接收到请求。
2. 它发现你需要 session，于是去运行 get_session。
3. get_session 打开了数据库连接（yield session），暂停自己，把连接交给你。
4. 你的业务代码（增删改查）舒舒服服地用完连接，返回结果。
5. FastAPI 回到 get_session，执行 with 块的结尾，自动安全地关闭数据库连接。你再也不用担心“忘记关数据库导致服务器崩溃”了！

### 3. 更新和删除

在代码顶部附近（定义 User 模型的地方），加上这段代码：

```py
# ==========================================
# 专门用于接收更新请求的模型
# 注意：这里 table=False（默认），因为它只是用来校验请求体，不需要在数据库建表
# ==========================================
class UserUpdate(SQLModel):
    username: str | None = Field(default=None, min_length=3, max_length=20)
    age: int | None = Field(default=None, ge=0, le=120)
```

继续在文件底部加上这两个路由函数：

```py
# ==========================================
# 6. 补全 CRUD 的最后两块拼图
# ==========================================

# 更新用户 (Update - 使用 PATCH 方法表示局部更新)
@app.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    # 1. 先从数据库里把这个用户找出来
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="哎呀，没找到这个用户，无法更新！")

    # 2. 提取出客户端真正传过来的数据（核心魔法！）
    # exclude_unset=True 的意思是：只提取用户在 JSON 里写了的字段。
    # 如果用户没传 username，那么 username 根本不会出现在这个字典里。
    update_data = user_update.model_dump(exclude_unset=True)

    # 3. 将新数据覆盖到数据库对象上
    for key, value in update_data.items():
        setattr(db_user, key, value)

    # 4. 提交并保存
    session.add(db_user)
    session.commit()
    session.refresh(db_user)  # 刷新一下，拿回最新的状态
    return db_user


# 删除用户 (Delete)
@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    # 1. 同样，先找到人
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在，可能已经被删除了？")

    # 2. 执行删除
    session.delete(db_user)
    session.commit()  # 别忘了 commit 才会真正生效！

    return {"message": f"用户 ID {user_id} 已成功注销！"}
```

1. `PATCH` vs `PUT`：
   - 在 RESTful 规范中，PUT 通常表示“全量替换”（如果你不传某个字段，它就被清空了）。
   - PATCH 表示“局部修改”（你传了什么，就改什么，没传的保持原样）。所以这里我们用 `@app.patch` 最符合实际业务语义。
2. `exclude_unset=True` 的魔法：
   - 这是 Pydantic 提供的一个超级好用的参数。如果没有它，当用户只传了 `{"age": 25}` 时，username 会变成默认的 None，这会错误地把数据库里的用户名清空！用了它，提取出来的字典就真的只有 `{"age": 25}`，非常安全。
3. `setattr` 动态赋值：
   - 这是 Python 的内置函数，相当于 `db_user.age = 25`。用循环配合 setattr，无论模型有 5 个字段还是 50 个字段，这三行代码都不用改，极具通用性！
