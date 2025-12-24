# 访问标志

类、方法、字段的修饰符会变成一堆常量（位标志）：

- 类的：ACC_PUBLIC, ACC_FINAL, ACC_INTERFACE, ACC_ABSTRACT ...
- 方法的：ACC_PUBLIC, ACC_STATIC, ACC_SYNCHRONIZED, ACC_NATIVE ...
- 字段的：ACC_PUBLIC, ACC_PRIVATE, ACC_FINAL, ACC_VOLATILE ...

例子：

```java
public static final int x;
```

它在 ASM 里访问时的 access 可能是：

```
ACC_PUBLIC | ACC_STATIC | ACC_FINAL
```
