# 使用

```java
ClassReader classReader = new ClassReader(classFileBuffer);
// 用于生成新类
ClassWriter classWriter = new ClassWriter(ClassWriter.COMPUTE_MAXS);

ClassEditor classEditor = new ClassEditor(Opcodes.ASM9, classWriter);
// 读取并修改class
classReader.accept(classEditor, ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES);

// 新类的字节码
byte[] new_content = classWriter.toByteArray();
```
