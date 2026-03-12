# 按指定条件查询

在 SQLModel 中进行条件查询主要依赖于 `select` 语句配合 `.where()` 方法。由于 SQLModel 是基于 SQLAlchemy 的，它的查询语法非常直观且支持链式操作。

### 1. 基础条件查询

使用 `==`、`!=`、`>`、`<` 等标准 Python 比较运算符。

```python
from sqlmodel import Session, select

with Session(engine) as session:
    # 查询 name 为 "Skywalker" 的用户
    statement = select(Hero).where(Hero.name == "Skywalker")
    results = session.exec(statement).all()
```

### 2. 多条件查询 (AND / OR)

- **AND (并列)**：可以连续调用 `.where()`，或者在一个 `.where()` 中传入多个条件。
- **OR (或者)**：需要从 `sqlmodel` 导入 `or_`。

```python
from sqlmodel import or_, select

# AND 条件：年龄大于 20 且 名字是 "Zoro"
statement = select(Hero).where(Hero.age > 20, Hero.name == "Zoro")

# OR 条件：名字是 "Zoro" 或者 名字是 "Luffy"
statement = select(Hero).where(or_(Hero.name == "Zoro", Hero.name == "Luffy"))
```

### 3. 模糊查询与包含 (Like / In)

- **LIKE**: 使用 `.列.like()` 或 `.列.contains()`。
- **IN**: 使用 `.列.in_()` 传入一个列表。

| 查询类型       | 代码示例                              | SQL 对应          |
| -------------- | ------------------------------------- | ----------------- |
| **模糊匹配**   | `where(Hero.name.like("%Sky%"))`      | `LIKE '%Sky%'`    |
| **包含字符串** | `where(Hero.name.contains("walker"))` | `LIKE '%walker%'` |
| **列表匹配**   | `where(Hero.id.in_([1, 2, 3]))`       | `IN (1, 2, 3)`    |
| **为空判断**   | `where(Hero.age == None)`             | `IS NULL`         |

### 4. 排序、分页与计数

在构建查询语句时，可以链式添加 `order_by`、`limit` 和 `offset`。

```python
# 按年龄降序排列，取前 5 个（分页常用）
statement = select(Hero).order_by(Hero.age.desc()).limit(5).offset(0)

# 获取总行数
from sqlmodel import func
count_statement = select(func.count()).select_from(Hero)
total = session.exec(count_statement).one()
```

### 5. 获取结果的方法

执行 `session.exec(statement)` 后，有几种获取数据的方式：

- `.all()`: 返回所有匹配记录的列表。
- `.first()`: 返回第一条记录，如果没有则返回 `None`。
- `.one()`: 返回唯一的一条记录，如果没有或有多条则报错。
- `.exec(statement).first()`: 这种链式写法是最常用的。

### 快速参考代码示例

```python
def get_heroes_by_condition():
    with Session(engine) as session:
        # 组合查询：名字包含 "a"，年龄大于 18，按 ID 排序
        statement = select(Hero).where(
            Hero.name.contains("a"),
            Hero.age > 18
        ).order_by(Hero.id)

        results = session.exec(statement).all()
        return results
```

## 多表关联（Join）查询

多表关联（Join）是数据库操作的灵魂。在 SQLModel 中，由于它完美继承了 SQLAlchemy 的 `Relationship` 机制，处理关联查询非常优雅。

以下是三种最常见的关联查询方式：

### 1. 自动关联查询 (使用 Relationship)

这是最 Pythonic 的方式。如果你在模型中定义了 `Relationship`，SQLModel 会在你访问属性时自动（或按需）加载关联数据。

```python
from sqlmodel import Session, select

with Session(engine) as session:
    # 查找名为 "Spider-Boy" 的英雄
    hero = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).first()

    # 直接访问关联的 team 属性，SQLModel 会自动处理背后的 Join
    print(f"Hero's team: {hero.team.name}")
```

### 2. 显式内连接 (Manual JOIN)

当你需要根据关联表的条件来过滤主表数据时，使用 `.join()`。

```python
# 需求：查询所有属于 "Avengers" 战队的英雄
statement = (
    select(Hero)
    .join(Team) # 默认是 INNER JOIN
    .where(Team.name == "Avengers")
)
results = session.exec(statement).all()
```

### 3. 同时查询多个模型 (返回元组)

有时你不仅需要英雄对象，还需要同时拿到团队对象。

```python
# 需求：同时获取英雄和他们对应的团队信息
statement = select(Hero, Team).where(Hero.team_id == Team.id)

results = session.exec(statement).all()
for hero, team in results:
    print(f"Hero: {hero.name}, Team: {team.name}")
```

### 4. 左外连接 (LEFT OUTER JOIN)

如果你想查询所有英雄，即使他们没有所属战队，可以使用 `isouter=True`。

```python
# 查询所有英雄及其战队（即使没有战队的英雄也会出现在结果中）
statement = select(Hero, Team).join(Team, isouter=True)

results = session.exec(statement).all()
# 对于没有战队的英雄，team 变量将为 None
```

### 关联查询进阶技巧

| 功能          | 语法示例                                        | 适用场景                                            |
| ------------- | ----------------------------------------------- | --------------------------------------------------- |
| **多级 Join** | `.join(Team).join(Base)`                        | 处理 A -> B -> C 的多层关系                         |
| **别名查询**  | `aliased(Hero)`                                 | 同一个表自己关联自己（如：经理也是员工）            |
| **提前加载**  | `select(Hero).options(selectinload(Hero.team))` | **性能优化**：一次性查出所有关联数据，避免 N+1 问题 |

## 定义关联关系

在 SQLModel 中正确定义关联关系是实现自动查询和维护数据一致性的关键。通常我们使用 **`ForeignKey`**（物理约束）和 **`Relationship`**（对象映射）配合使用。

以下是一个标准的“一对多”关系示例（一个战队 Team 有多个英雄 Hero）：

```python
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, create_engine

# 1. 定义 "一" 的一方：战队 (Team)
class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    # Relationship 定义：
    # back_populates 指向 Hero 类中定义的对应属性名
    heroes: List["Hero"] = Relationship(back_populates="team")

# 2. 定义 "多" 的一方：英雄 (Hero)
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = None

    # ForeignKey 定义：这是数据库层面的物理约束，指向 team 表的 id 列
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

    # Relationship 定义：
    # back_populates 指向 Team 类中定义的对应属性名
    team: Optional[Team] = Relationship(back_populates="heroes")
```

---

| 核心组件                    | 作用                                                                                                                                         | 数据库表现                         |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **`foreign_key="team.id"`** | **物理连接**。告知数据库这一列的值必须存在于 `team` 表的 `id` 列中。                                                                         | 在 SQL 中生成 `FOREIGN KEY` 约束。 |
| **`Relationship`**          | **逻辑连接**。这在数据库中**不存在**，它仅供 Python 代码使用，让你能通过 `hero.team` 或 `team.heroes` 像访问属性一样获取关联对象。           | 不生成 SQL 列。                    |
| **`back_populates`**        | **双向绑定**。确保你在修改其中一方时，另一方在内存中也会同步更新。例如给 `team.heroes` 添加一个英雄，该英雄的 `hero.team` 会自动变为该战队。 | N/A                                |
| **`List["Hero"]`**          | 类型注解。注意由于类定义顺序，通常需要使用**字符串引号**引起来（前向引用），以避免 Python 找不到尚未定义的类。                               | N/A                                |

#### 创建关联数据

```python
with Session(engine) as session:
    team_avengers = Team(name="Avengers", headquarters="New York")

    # 直接在创建对象时关联
    hero_ironman = Hero(name="Iron Man", secret_name="Tony Stark", team=team_avengers)

    session.add(hero_ironman)
    session.commit()
```

#### 级联查询

```python
with Session(engine) as session:
    # 查找战队，并自动获取其下所有英雄
    statement = select(Team).where(Team.name == "Avengers")
    result = session.exec(statement).first()

    for hero in result.heroes:
        print(f"战队成员: {hero.name}")
```

### 4. 常见问题：级联删除 (Cascade Delete)

如果你希望在删除战队时，自动删除其所属的所有英雄，需要在 `Relationship` 中添加 `sa_relationship_kwargs`：

```python
class Team(SQLModel, table=True):
    # ... 其他字段
    heroes: List["Hero"] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan", # 级联删除孤儿数据
        }
    )

```
