# ClassReader：读取器

作用：从字节数组 / 输入流中读入 class 文件。

你通常这样用：

```java
ClassReader cr = new ClassReader(classfileBytes);
cr.accept(visitor, flags);
```

含义是：

- 把这个 class 读一遍，然后在读到不同部分时，去调用 visitor 对应的方法。

它本身不做业务逻辑，只负责“扫描并回调”。
