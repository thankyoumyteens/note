# visitAnnotation 方法

visitAnnotation 方法为字段添加注解:

```java
public AnnotationVisitor visitAnnotation(String desc, boolean visible)
```

参数说明:

- desc: 注解类的描述符, 比如: Ljavax/annotation/Resource;
- visible: 注解是否运行时可见

## 用法

```java
// 首先从ClassWriter获取FieldVisitor
FieldVisitor userService = classWriter.visitField(Opcodes.ACC_PRIVATE,
                                            "userService",
                                            "Lorg/example/UserService;",
                                            null, null);

// 使用visitAnnotation方法获取AnnotationVisitor
AnnotationVisitor annotationVisitor = userService.visitAnnotation("Ljavax/annotation/Resource;", true);
// 设置@Resource注解的value字段:
// @Resource(value = "userServiceImpl")
annotationVisitor.visit("value", "userServiceImpl");
annotationVisitor.visitEnd();

userService.visitEnd();
```
