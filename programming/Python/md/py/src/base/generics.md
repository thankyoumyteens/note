# 泛型

在 Python 中，泛型（Generics） 是一种允许类、函数或数据结构在不指定具体类型的情况下定义，仅在使用时才确定具体类型的特性，核心作用是增强代码的复用性、可读性和类型安全性（配合 Type Hint 使用）。

## 泛型函数

```py
from typing import TypeVar

# 定义类型变量T（可代表任意类型）
T = TypeVar('T')

# 泛型函数：返回列表的第一个元素，类型与列表元素一致
def get_first_item(items: list[T]) -> T:
    return items[0]

# 使用时，自动匹配具体类型
nums: list[int] = [1, 2, 3]
num = get_first_item(nums)  # 类型提示为int（正确）

strs: list[str] = ["a", "b", "c"]
s = get_first_item(strs)    # 类型提示为str（正确）
```

## 泛型类

```py
from typing import TypeVar, Generic

T = TypeVar('T')

# 继承Generic[T]，声明这是一个泛型类，类型由T决定
class Stack(Generic[T]):
    def __init__(self):
        self.items: list[T] = []  # 容器内元素类型为T

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

# 实例化时指定具体类型
int_stack = Stack[int]()  # 存储int的栈
int_stack.push(10)
x = int_stack.pop()  # 类型提示为int

str_stack = Stack[str]()  # 存储str的栈
str_stack.push("hello")
y = str_stack.pop()  # 类型提示为str
```
