# Optional 增强

Java 11 对 Optional 类（用于优雅处理可能为 null 的值）进行了小幅但实用的增强，新增了 isEmpty() 方法，进一步完善了 Optional 的空值判断逻辑，提升了代码的可读性和直观性。

在 Java 11 之前，判断 Optional 是否为空（即不包含值）需要通过 `!isPresent()` 实现。这种写法虽然功能正确，但 `!isPresent()` 的语义不够直观。Java 11 新增的 isEmpty() 方法直接表达 “是否为空” 的含义，使代码更易读：

```java
Optional<String> name = Optional.empty();
// 直接判断为空，语义更清晰
if (name.isEmpty()) {
    System.out.println("名称为空");
}
```
