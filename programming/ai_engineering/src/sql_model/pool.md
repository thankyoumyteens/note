# 数据库连接池

SQLModel 底层使用的 SQLAlchemy 自带了成熟的连接池管理机制。

在创建 engine 时，可以通过参数调整连接池的行为。常用的参数包括 pool_size（核心池大小）和 max_overflow（允许临时突破的大小）。

```py
from sqlmodel import create_engine

sqlite_url = "postgresql://user:password@localhost/dbname"

# 配置连接池
engine = create_engine(
    sqlite_url,
    # 保持在池中的最小连接数
    pool_size=10,
    # 在 pool_size 满载后，允许额外创建的临时连接数
    max_overflow=20,
    pool_size=10,
    # 等待获取连接的最长时间，超时抛出异常
    pool_timeout=30,
    # 连接在池中被回收前的空闲秒数（防止数据库端主动断开导致的“连接失效”）
    pool_recycle=3600,
    # 每次检出连接时是否先测试其有效性（虽然有微小性能损耗，但更稳健）
    pool_pre_ping=True
)
```
