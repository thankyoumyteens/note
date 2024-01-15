# ClassWriter

ClassWriter 的构造方法:

```java
public ClassWriter(final int flags)
```

flags 参数的可选值有三个:

1. 0: ASM 不会自动计算 max stacks 和 max locals, 也不会自动计算 stack map frames
2. ClassWriter.COMPUTE_MAXS: 会自动计算 max stacks 和 max locals, 但不会自动计算 stack map frames
3. ClassWriter.COMPUTE_FRAMES: 会自动计算 max stacks 和 max locals, 也会自动计算 stack map frames
