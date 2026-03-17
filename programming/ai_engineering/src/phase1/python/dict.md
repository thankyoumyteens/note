# 字典操作

在 Python 中，字典（dict）几乎是万物的基础（甚至 Python 内部的对象属性也是用字典存储的）。

对于 Java 开发者来说，你可以直接把 Python 的 dict 等同于 Java 的 HashMap。但得益于 Python 的动态特性，它的语法极其轻量，能帮你省去大量 put() 和 get() 的样板代码。

## 创建与增删改 (CRUD)

在 Python 中，你几乎不需要调用方法来做基础的增删改，一切都通过直观的符号完成。

```py
# 直接用大括号 {} 初始化
user = {
    "name": "Alice"
}

user["name"] = "Bob"           # 修改（如果键不存在就是新增）
del user["name"]               # 删除（使用 del 关键字）

has_name = "name" in user      # 判断键是否存在（极简的 in 关键字）
```

## 安全读取数据 (防止空指针/异常)

这是实际开发中最容易踩坑的地方。在 Python 中，如果你直接用 `user["age"]` 去取一个不存在的键，程序会直接抛出 KeyError 导致崩溃。

```py
# 推荐写法：使用 .get() 方法，效果完全等同于 Java 的 getOrDefault
age = user.get("age", 18)

# 如果不传第二个参数，找不到时默认返回 None (Python 的 null)
role = user.get("role")
```

## 遍历字典 (Iteration)

Python 利用其 **解包（Unpacking）** 特性，让遍历变得像读英语一样自然。

```py
user = {"name": "Alice", "age": 25, "role": "Admin"}

# 遍历键值对 (使用 .items()，类似 entrySet)
for key, value in user.items():
    print(f"{key}: {value}")

# 仅遍历键 (默认行为，或使用 .keys())
for key in user:
    print(key)

# 仅遍历值 (使用 .values())
for value in user.values():
    print(value)
```

## 合并字典 (Python 3.9+ 专属)

在 AI 开发中，我们经常需要合并配置项。比如把“默认参数”和“用户传入的参数”合并。

```py
default_config = {"model": "gpt-3.5", "temperature": 0.7}
user_config = {"temperature": 0.9, "max_tokens": 100}

# 直接用 | 符号合并！如果有冲突的键，右边的会覆盖左边的
final_config = default_config | user_config

print(final_config)
# 输出: {'model': 'gpt-3.5', 'temperature': 0.9, 'max_tokens': 100}
```

## JSON 与 Dict 的无缝转换

在调用大模型 API 时，你处理的实际上都是 JSON 数据。在 Java 中你需要 Jackson 或 Fastjson 这样的库来做映射，但在 Python 中，JSON 和 Dict 简直是亲兄弟。

```py
import json

# 1. 收到 API 返回的 JSON 字符串
json_response = '{"id": "chatcmpl-123", "choices": [{"text": "Hello!"}]}'

# 2. 一键转为 Python 字典 (解析)
data_dict = json.loads(json_response)
print(data_dict["choices"][0]["text"]) # 输出: Hello!

# 3. 把字典一键转回 JSON 字符串 (序列化)
new_json_string = json.dumps(data_dict, ensure_ascii=False)
```
