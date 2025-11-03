# Optional 增强

Java 10 新增了 orElseThrow() 方法，进一步简化了 “当值不存在时抛出异常” 的场景，提升了代码的简洁性和可读性。

```java
Optional<String> name = Optional.empty();
// Java 8/9：值不存在时抛出指定异常
String result = name.orElseThrow(() -> new IllegalArgumentException("名称不能为空"));

// Java 10 新增了无参版本的 orElseThrow()
// 当 Optional 为空时，默认抛出 NoSuchElementException
String result = name.orElseThrow();
```
