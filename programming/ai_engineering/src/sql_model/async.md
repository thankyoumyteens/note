# 异步数据库查询

这个概念是现代高并发 Web 开发的核心，也是 FastAPI 之所以被称为“快”的根本原因。

#### 同步机制 (如普通的 Flask, Django + psycopg2)

当你在代码里执行 `session.exec(select(Hero))` 时，Python 会通过网卡向远端的 MySQL 发送一条网络报文。

- **物理速度差异：** CPU 执行一条指令的时间是纳秒级的，而网络传输和数据库磁盘查询的时间是毫秒级的。这就好比法拉利在等红绿灯。
- **线程休眠：** 在同步模式下，操作系统看这个线程在等网络响应，就会直接把它**挂起（Sleep）**。
- **并发瓶颈：** 服务器的线程池容量是有限的（通常 Web 服务器默认只开几十个工作线程）。一旦突发几百个并发请求，所有线程全都在等数据库，新的请求就只能在门外排队，导致用户界面疯狂转圈圈（超时）。

#### 异步机制 (FastAPI + Asyncio + aiomysql)

FastAPI 底层运行在一个叫做 **事件循环 (Event Loop)** 的引擎上（通常是 `uvicorn` 提供）。

- 当代码执行到 **`await`** `session.exec(...)` 时，那个 `await` 关键字就是一个**交出控制权**的信号。
- 它在对事件循环说：“大哥，这步要走网络 I/O，大概需要 50 毫秒，我先把它扔给操作系统后台去等，你先去执行其他代码吧。”
- 于是，事件循环立刻去接管了此时进来的第 2 个 API 请求。
- 等那 50 毫秒过去，操作系统的网卡收到了 MySQL 返回的数据，会给事件循环发个通知（回调）。事件循环就会回到刚才那个 `await` 的地方，拿着数据继续往下执行。

---

| 特性               | 同步 (Sync)                                      | 异步 (Async)                                                |
| ------------------ | ------------------------------------------------ | ----------------------------------------------------------- |
| **等待数据库时**   | 线程被冻结，啥也干不了                           | 线程被释放，去处理其他 API 请求                             |
| **内存与资源占用** | 高。需要开大量线程来应对并发，每个线程都要吃内存 | 极低。少量线程配合事件循环就能处理海量并发                  |
| **适用场景**       | 传统系统、后台管理、并发量要求不高的内部工具     | **高并发 Web API**、聊天室、微服务、大量调用外部接口的系统  |
| **代码编写**       | 简单直观                                         | 稍微复杂，必须满屏幕写 `async` 和 `await`，且不能混用同步库 |

很多人以为异步会让 **单次** 数据库查询变快。这是错的。执行一条 SQL，数据库该花 10 毫秒还是 10 毫秒。**异步提升的不是“单辆车的行驶速度”，而是“整条马路的通行吞吐量”。** 它可以让你的服务器在同样的硬件配置下，同时承受多 10 倍甚至 100 倍的并发访问量。

要使用 SQLModel 的异步功能，底层其实是依赖了 SQLAlchemy 的异步扩展。

### 1. 安装异步数据库驱动

普通的数据库驱动（如 psycopg2 或普通的 sqlite3）是同步的。你必须安装支持 asyncio 的异步驱动：

- PostgreSQL: `pip install asyncpg`
- SQLite: `pip install aiosqlite`
- MySQL: `pip install aiomysql`

### 2. 创建异步引擎 (Async Engine)

数据库 URL 的协议部分需要加上异步驱动的名称（例如 `postgresql+asyncpg://` 或 `sqlite+aiosqlite:///`）。

```py
from sqlalchemy.ext.asyncio import create_async_engine

# 示例使用异步
async_mysql_url = "mysql+aiomysql://your_username:your_password@localhost:3306/my_database?charset=utf8mb4"

# 创建异步引擎
async_engine = create_async_engine(
    async_mysql_url,
    echo=True, # 打印生成的 SQL，方便调试
    future=True # 确保使用 SQLAlchemy 2.0 风格的 API
)
```

### 3. 创建 FastAPI 异步依赖项 (Async Session)

我们需要从 `sqlmodel.ext.asyncio.session` 导入专门的 AsyncSession。注意依赖项函数现在变成了 `async def`，并且使用 `async with`。

```py
from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession

# 异步依赖项
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session
```

### 4. 编写异步 CRUD 操作

在执行查询、保存或更新时，凡是涉及网络 I/O 的地方，都需要加上 await。

```py
from fastapi import FastAPI, Depends
from sqlmodel import select

app = FastAPI()

@app.post("/heroes/")
async def create_hero(hero: Hero, session: AsyncSession = Depends(get_async_session)):
    session.add(hero)
    # 提交事务是一个 I/O 操作，需要 await
    await session.commit()
    # 刷新对象以获取数据库生成的 ID，也需要 await
    await session.refresh(hero)
    return hero

@app.get("/heroes/")
async def read_heroes(session: AsyncSession = Depends(get_async_session)):
    statement = select(Hero).where(Hero.age > 20)

    # 执行查询需要 await
    result = await session.exec(statement)

    # 获取数据列表 (注意：.all() 不是异步的，因为数据已经拿到了内存里)
    heroes = result.all()
    return heroes
```
