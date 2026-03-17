# 列表推导式

在 Java 中，当我们需要对一个集合进行遍历、过滤和转换时，通常会面临两种选择：写冗长的 for 循环，或者使用 Stream API。Python 的列表推导式直接将这些操作压缩成了一行极其易读的代码。

## 核心公式：解构列表推导式

你可以把列表推导式看作是倒装的 for 循环和 if 判断。

```py
[ <转换表达式(map)>  for  <集合中的元素>  in  <集合(stream)>  if  <过滤条件(filter)> ]
```

## 场景实战：Java Stream vs Python 推导式

### 场景 A：纯转换操作（等价于 Java 的 map）

需求： 将一个字符串列表全部转换为大写。

Java Stream:

```java
List<String> names = Arrays.asList("apple", "banana", "cherry");
List<String> upperNames = names.stream()
                               .map(String::toUpperCase)
                               .collect(Collectors.toList());
```

Python 列表推导式:

```py
names = ["apple", "banana", "cherry"]
upper_names = [name.upper() for name in names]
```

解析： 这里没有 if，直接把 `for name in names` 拿到的 name 交给前面的 `name.upper()` 处理，并自动塞进新的 `[]` 里。

### 场景 B：过滤 + 转换（等价于 filter + map）

需求： 找出列表中大于 5 的数字，并将它们乘以 10。

Java Stream:

```java
List<Integer> nums = Arrays.asList(2, 6, 4, 8, 3);
List<Integer> result = nums.stream()
                           .filter(n -> n > 5)
                           .map(n -> n * 10)
                           .collect(Collectors.toList());
```

Python 列表推导式:

```py
nums = [2, 6, 4, 8, 3]
result = [n * 10 for n in nums if n > 5]
```

解析： 执行顺序其实是：先跑 for 遍历，接着过 if 过滤，最后交给最前面的 `n * 10` 进行转换。

### 场景 C：带 if-else 的转换（等价于 map 里的三元运算符）

注意，这是一个容易踩坑的地方！ 如果你的逻辑是“满足条件则转换，不满足则保留（或做另一种转换）”，此时 if-else 不再是过滤器（filter），而是属于转换逻辑（map），它需要放在最前面。

需求： 偶数乘以 2，奇数保持不变。

Java Stream:

```java
// 使用三元运算符 n % 2 == 0 ? n * 2 : n
List<Integer> result = nums.stream()
                           .map(n -> n % 2 == 0 ? n * 2 : n)
                           .collect(Collectors.toList());
```

Python 列表推导式:

```py
nums = [1, 2, 3, 4]
# Python 的三元运算符写法是： [值1] if [条件] else [值2]
result = [n * 2 if n % 2 == 0 else n for n in nums]
```

## 字典推导式 (Dict Comprehension)

既然列表可以用推导式，字典（HashMap）也可以！这在 Java 中通常需要极其繁琐的 `Collectors.toMap()` 才能搞定。

```py
# 将列表转为字典：{"apple": 5, "banana": 6}
words = ["apple", "banana"]
word_lengths = {word: len(word) for word in words}
```

## 小心内存爆炸！改用“生成器” (类似 Java Stream 的懒加载)

ava 的 Stream 是 **惰性求值（Lazy Evaluation）** 的，不到最后一步 `collect()` 是不会真正运算的。
但 Python 的列表推导式 `[...]` 是 **立即求值（Eager Evaluation）** 的，如果你的列表有一千万条数据，它会瞬间把内存撑爆。

解决方案： 把中括号 `[]` 换成小括号 `()`，它就会变成一个“生成器（Generator）”，拥有和 Java Stream 一样的懒加载特性，每次只在内存中处理一个元素。

```py
# 列表推导式：一次性把 100 万个数字放入内存
heavy_list = [n * 2 for n in range(1000000)]

# 生成器表达式：懒加载，几乎不占内存 (推荐用于大数据处理)
lazy_gen = (n * 2 for n in range(1000000))

# 需要用的时候再拿出来
for num in lazy_gen:
    # 逐个处理...
    pass
```
