# 手写sql

虽然 SQLModel 的 ORM 功能很强大，但总有一些复杂的查询（比如开窗函数、复杂的聚合或特定数据库的优化）需要我们写原生 SQL。

由于 SQLModel 是建立在 SQLAlchemy 之上的，执行手写 SQL 非常简单。你可以使用 `text()` 函数来包装你的 SQL 字符串。

### 1. 执行原生 SELECT 查询

使用 `text()` 函数，并通过 `session.exec()` 执行。

```python
from sqlmodel import Session, text

with Session(engine) as session:
    # 1. 定义 SQL 语句（推荐使用参数绑定避免 SQL 注入）
    statement = text("SELECT * FROM hero WHERE age > :age_limit")

    # 2. 执行并传入参数
    results = session.exec(statement, params={"age_limit": 25})

    # 3. 遍历结果（结果通常是 Row 对象，类似于元组）
    for row in results:
        print(f"ID: {row.id}, Name: {row.name}")
```

### 2. 执行更新、删除或插入 (DML)

对于修改数据的操作，执行后需要调用 `session.commit()`。

```python
with Session(engine) as session:
    # 批量更新示例
    statement = text("UPDATE hero SET age = age + 1 WHERE team_id = :t_id")

    # 执行操作
    result = session.exec(statement, {"t_id": 1})

    # 提交事务
    session.commit()

    print(f"受影响的行数: {result.rowcount}")
```

### 3. 将原生 SQL 结果映射回 SQLModel 模型

如果你希望手写的 SQL 返回的结果直接变成 `Hero` 对象，可以使用 `select().from_statement()`。

```python
from sqlmodel import select

with Session(engine) as session:
    # 手写 SQL 但希望返回 Hero 对象
    raw_sql = text("SELECT * FROM hero WHERE name LIKE '%Sky%'")

    # 使用 from_statement 进行转换
    statement = select(Hero).from_statement(raw_sql)
    heroes = session.exec(statement).all()

    # 此时 hero 是标准的 Hero 模型实例
    print(heroes[0].name)
```

### 核心注意事项

| 特性                    | 说明                                                                                                       |
| ----------------------- | ---------------------------------------------------------------------------------------------------------- |
| **参数绑定**            | **永远不要**使用 Python 的 f-string 拼接 SQL，务必使用 `:name` 占位符和 `params` 字典来防止 **SQL 注入**。 |
| **结果获取**            | `session.exec()` 返回的是迭代器，可以使用 `.all()`, `.first()`, 或直接 `for` 循环。                        |
| **自动映射**            | 只有当 SQL 查询出的列名与模型字段完全一致时，`from_statement` 才能正确映射。                               |
| **执行原始 Connection** | 如果需要更底层的操作，可以通过 `session.connection()` 获取 SQLAlchemy 的 Connection 对象。                 |

### 进阶：获取字典格式的结果

有时候你不需要模型对象，只想拿一个字典列表：

```python
with Session(engine) as session:
    result = session.execute(text("SELECT name, age FROM hero"))
    # 将每一行转为字典
    dict_results = [row._asdict() for row in result]
    print(dict_results) # [{'name': 'Deadpool', 'age': 35}, ...]
```
