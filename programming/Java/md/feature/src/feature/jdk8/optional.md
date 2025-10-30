# Optional

Optional 是一个容器类，用于包装可能为 null 的对象，核心目的是避免空指针异常（NullPointerException），同时让代码更清晰地表达 “值可能不存在” 的语义。

## 典型使用场景 1 替代方法返回 null

传统方法返回 null 容易导致空指针，用 Optional 明确告知调用者 “值可能不存在”：

```java
// 传统方法（风险：返回 null 无提示）
public String getUserName() {
    return null; // 调用者可能忘记判空
}

// 优化后：用 Optional 包装返回值
public Optional<String> getUserName() {
    return Optional.ofNullable(null); // 明确告知“可能为空”
}

// 调用者必须显式处理空值
Optional<String> nameOpt = getUserName();
nameOpt.ifPresent(System.out::println);
```

## 典型使用场景 2 链式处理对象属性（避免多层判空）

```java
// 传统写法（繁琐且易漏判空）
String city = null;
if (user != null) {
    Address address = user.getAddress();
    if (address != null) {
        city = address.getCity();
    }
}

// Optional 链式写法（简洁）
String cityOpt = Optional.ofNullable(user)
    .map(User::getAddress) // 若 user 为 null，返回空 Optional
    .map(Address::getCity) // 若 address 为 null，返回空 Optional
    .orElse("未知城市"); // 最终默认值
```
