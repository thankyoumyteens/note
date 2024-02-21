# 为类添加字段

使用 visitField 方法为类添加字段:

```java
/**
 * 为类添加字段
 */
private static void addField(ClassWriter writer) {
    // 添加字段
    FieldVisitor fieldVisitor = writer.visitField(
            // 字段的访问标志
            Opcodes.ACC_PUBLIC,
            // 字段名
            "myField1",
            // 字段的描述符
            "I",
            // 泛型信息
            null,
            // static+final字段的初始值
            null
    );
    // 字段操作结束
    fieldVisitor.visitEnd();
}
```
