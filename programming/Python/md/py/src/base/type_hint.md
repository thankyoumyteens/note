# Type Hint

Type Hint（类型提示）是 Python 3.5 + 引入的语法特性，用于在代码中显式标注变量、函数参数、返回值的数据类型。它不影响代码的运行（Python 仍是动态类型语言），核心作用是提升代码可读性、帮助开发者规避类型错误，并支持静态类型检查工具（如 mypy）自动检测潜在问题。

## 变量的类型提示

直接在变量名后加 `: 类型`，标注变量期望的数据类型。

基础类型:

```py
name: str = "Alice"       # 字符串类型
age: int = 25             # 整数类型
score: float = 98.5       # 浮点数类型
is_student: bool = True   # 布尔类型
```

容器类型(需从 typing 导入对应工具类，Python 3.9+可直接用内置容器):

```py
from typing import List, Dict, Tuple

# 列表：元素均为int
numbers: List[int] = [1, 2, 3]
# Python 3.9+ 简化写法：
numbers: list[int] = [1, 2, 3]

# 字典：key为str，value为int
student_scores: Dict[str, int] = {"Alice": 95, "Bob": 88}
# Python 3.9+ 简化写法：
student_scores: dict[str, int] = {"Alice": 95}

# 元组：固定位置的类型（第一个元素str，第二个int）
person: Tuple[str, int] = ("Alice", 25)
# Python 3.9+ 简化写法：
person: tuple[str, int] = ("Alice", 25)
```

## 函数的类型提示

- 函数参数：在参数名后加 `: 类型`，标注参数的期望类型
- 函数返回值：在函数定义后加 `-> 类型`，标注函数的返回值类型

```py
# 函数：接收两个int，返回int
def add(a: int, b: int) -> int:
    return a + b
```

## 可选类型

变量 / 参数可以是指定类型，也可以是 None，需从 typing 导入 Optional。

```py
rom typing import Optional

# 可选类型：age可以是int，也可以是None
age: Optional[int] = None  # 合法
age = 25                   # 也合法
```

## 任意类型

类型不确定（不推荐滥用，会失去类型提示的意义），需从 typing 导入 Any。

```py
from typing import Any

# 任意类型：data可以是任何类型
def process_data(data: Any) -> None:
    print(f"Processing: {data}")

process_data(123)    # 合法
process_data("abc")  # 合法
process_data([1,2])  # 合法
```

## 泛型

Python 内置的容器类型（list、dict、tuple、set 等）本质是泛型，可用 Type Hint 明确其元素 / 键值的类型。

```py
# ------------------- Python 3.9+ 示例（推荐，更简洁） -------------------
# 列表：元素均为str
str_list: list[str] = ["apple", "banana"]
# 列表：元素均为int
int_list: list[int] = [1, 2, 3]

# 字典：key为str，value为float
score_dict: dict[str, float] = {"Alice": 95.5, "Bob": 88.0}

# 元组：固定位置类型（第一个str，第二个int，第三个bool）
person: tuple[str, int, bool] = ("Alice", 25, True)

# 集合：元素均为int
num_set: set[int] = {1, 2, 3, 4}


# ------------------- Python 3.5-3.8 示例（需导入typing） -------------------
from typing import List, Dict, Tuple, Set

str_list: List[str] = ["apple", "banana"]
int_list: List[int] = [1, 2, 3]
score_dict: Dict[str, float] = {"Alice": 95.5, "Bob": 88.0}
person: Tuple[str, int, bool] = ("Alice", 25, True)
num_set: Set[int] = {1, 2, 3, 4}
```
