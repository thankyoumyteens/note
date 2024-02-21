# 设置字段的注解

visitAnnotation 方法为字段添加注解:

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
    // 设置字段的注解
    AnnotationVisitor annotationVisitor = fieldVisitor.visitAnnotation(
            // 注解的描述符
            "Ljavax/annotation/Resource;",
            // 是否在运行时可见
            true
    );
    // 设置@Resource注解的value字段: @Resource(value = "f1")
    annotationVisitor.visit(
            // 注解的属性名
            "value",
            // 注解的属性值
            "f1"
    );
    // 注解操作结束
    annotationVisitor.visitEnd();
    // 字段操作结束
    fieldVisitor.visitEnd();
}
```
