# 一个“增强流程”的标准写法

1. 用 `ClassReader` 读入原始 `.class`
2. 自己写一个继承 `ClassVisitor` 的类，重写 `visitMethod`
3. 在 `visitMethod` 里返回你包装过的 `MethodVisitor`
4. 在 `MethodVisitor` 里，合适的时间点插入、修改指令
5. 用 `ClassReader::accept` 方法读取 + 访问字节码
6. 用 `ClassWriter` 接收访问结果，得到新的字节数组

ASM 不会让你直接手搓二进制，而是通过一套“回调接口”来改东西:

- `ClassReader::accept(visitor, flags)`
  - 读 class 的时候，会一边读一边回调你实现的 `ClassVisitor` / `MethodVisitor`
- 你在这些回调里：
  - 可以在进入方法前、指令前/后做事
  - 可以“放行”原始指令，也可以插入新的指令
