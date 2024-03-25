# 读取 class 内容

通过 ClassReader 进行字节码的解析。

ClassReader 可用的构造方法:

```java
public ClassReader(byte[] classFile)
public ClassReader(byte[] classFileBuffer, int classFileOffset, int classFileLength)
public ClassReader(InputStream inputStream) throws IOException
public ClassReader(String className) throws IOException
```

调用 ClassReader 的 accept 方法, 通过传入自定义的 visitor 来实现解析 class 字节码的功能。常用的 accept 方法:

```java
public void accept(ClassVisitor classVisitor, int parsingOptions)
```

- classVisitor: ClassVisitor 是抽象类, 需要传入自定义的 ClassVisitor。accept 方法中会调用 visitField/visitMethod 等方法, 通过重写这些方法, 就可用获得 class 中相应的信息
- parsingOptions 的取值:
  - 0: 读取 class 中的所有信息
  - ClassReader.SKIP_CODE: 跳过代码属性
  - ClassReader.SKIP_DEBUG: 跳过源文件、局部变量表、局部变量类型表、方法参数列表、行号
  - ClassReader.SKIP_FRAME: 跳过帧（visitFrame）, 帧是 JVM 验证类阶段使用的数据
  - ClassReader.EXPANDS_FRAMES: 扩展堆栈映射帧
