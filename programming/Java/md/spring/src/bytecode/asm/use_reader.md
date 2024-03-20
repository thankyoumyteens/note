# 使用

```java
ClassReader classReader = new ClassReader(classFileBuffer);
ClassInfoVisitor classInfoVisitor = new ClassInfoVisitor();
classReader.accept(classInfoVisitor, ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES);
ClassInfo info = classInfoVisitor.classInfo;
```