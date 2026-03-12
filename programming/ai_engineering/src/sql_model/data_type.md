# Python 数据类型与数据库数据类型的对应关系

在使用 SQLModel 时，由于它是基于 SQLAlchemy 和 Pydantic 构建的，它实际上起到了一个桥梁的作用：将 Python 的原生类型（用于数据验证）映射到数据库的列类型（用于持久化存储）。

以下是常见的 Python 数据类型与 SQL 数据库类型的对应关系表：

| Python 类型         | SQL 类型 (标准/通用)     | 说明                                                      |
| ------------------- | ------------------------ | --------------------------------------------------------- |
| `str`               | `VARCHAR` / `TEXT`       | 默认通常是 `VARCHAR`，可通过 `Field(max_length=...)` 限制 |
| `int`               | `INTEGER`                | 映射为标准整数                                            |
| `float`             | `FLOAT` / `REAL`         | 映射为浮点数                                              |
| `bool`              | `BOOLEAN`                | 映射为布尔值（某些数据库如 MySQL 会转为 `TINYINT`）       |
| `datetime.datetime` | `DATETIME` / `TIMESTAMP` | 建议在定义时明确时区处理                                  |
| `datetime.date`     | `DATE`                   | 仅存储日期                                                |
| `datetime.time`     | `TIME`                   | 仅存储时间                                                |
| `bytes`             | `BLOB` / `BYTEA`         | 用于存储二进制数据                                        |
| `decimal.Decimal`   | `NUMERIC` / `DECIMAL`    | 用于需要高精度的货币或科学计算                            |
| `uuid.UUID`         | `UUID` / `VARCHAR(36)`   | 数据库支持则用原生 UUID，否则存为字符串                   |
| `dict` / `list`     | `JSON`                   | 需要数据库支持（如 PostgreSQL, MySQL 5.7+）               |

---

在使用 SQLModel 时，你可以通过 `Field` 函数来精细控制数据库中的具体表现：

#### 1. 字符串长度限制

如果不指定长度，某些数据库（如 PostgreSQL）会默认使用 `TEXT`，而另一些可能需要长度。

```python
# 映射为 VARCHAR(255)
name: str = Field(max_length=255)
# 强制映射为 TEXT
description: str = Field(sa_column=Column(Text))
```

#### 2. 可选类型 (Optional) 与 Nullable

SQLModel 通过 Python 的类型注解自动判断字段是否可以为空：

- `name: str`: 映射为 `NOT NULL`。
- `name: Optional[str]` 或 `str | None`: 映射为 `NULL` (可为空)。

#### 3. 主键与自增

通常 Python 的 `int` 配合 `primary_key=True` 会在数据库中生成自增主键（如 `SERIAL` 或 `AUTO_INCREMENT`）。

```python
id: Optional[int] = Field(default=None, primary_key=True)

```

#### 4. 枚举类型 (Enum)

你可以使用 Python 的 `enum.Enum`，SQLModel 会将其映射为数据库的 `ENUM` 类型或字符串。

---

### Decimal 类型

在处理金钱时，**强烈建议**使用 `decimal.Decimal` 而不是 `float`，以避免浮点数计算精度丢失。
