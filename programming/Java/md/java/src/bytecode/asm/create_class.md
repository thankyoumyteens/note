# 生成 class

生成 class 需要使用 ClassWriter。

```java
ClassWriter(final int flags)
```

flags 参数的可选值有三个:

1. 0: ASM 不会自动计算 max stacks 和 max locals, 也不会自动计算 stack map frames
2. ClassWriter.COMPUTE_MAXS: 会自动计算 max stacks 和 max locals, 但不会自动计算 stack map frames
3. ClassWriter.COMPUTE_FRAMES: 会自动计算 max stacks 和 max locals, 也会自动计算 stack map frames

## 依赖

```xml
<dependency>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm</artifactId>
    <version>9.6</version>
</dependency>
```

## 设置类的基本信息

使用 visit 方法可用设置类的基本信息:

```java
public class ClassCreator implements Opcodes {

    public byte[] create() {
        // 自动计算 max stacks 和 max locals 和 stack map frames
        ClassWriter writer = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        // 设置类的基本信息
        writer.visit(
                // 当前类使用JDK 8编译
                Opcodes.V1_8,
                // 类的访问标志
                Opcodes.ACC_PUBLIC + Opcodes.ACC_SUPER,
                // 类的内部名
                "org/example/MyDemo",
                // 泛型信息
                null,
                // 父类的内部名
                "java/lang/Object",
                // 实现的接口
                new String[]{"java/io/Serializable"}
        );
        // 设置类的构造器
        setConstructor(writer);
        // 添加字段
        addField(writer);
        // 添加方法
        addMethod(writer);
        // 标记对类的操作结束
        writer.visitEnd();
        // 获取类的字节码
        return writer.toByteArray();
    }
}
```

## 为类添加字段

使用 visitField 方法为类添加字段, visitAnnotation 方法为字段添加注解:

```java
/**
 * 为类添加字段
 */
private void addField(ClassWriter writer) {
    // 添加字段
    FieldVisitor fieldVisitor = writer.visitField(
            // 字段的访问标志
            ACC_PUBLIC,
            // 字段名
            "myField1",
            // 字段的描述符
            "I",
            // 泛型信息
            null,
            // static final字段的初始值
            null
    );
    // 设置字段的注解
    AnnotationVisitor annotationVisitor = fieldVisitor.visitAnnotation(
            // 注解的描述符
            "Ljavax/annotation/Resource;",
            // 是否在运行时可见
            true
    );
    // 设置注解的属性值
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

## 为类添加方法

使用 visitMethod 方法为类添加方法:

```java
/**
 * 为类添加方法
 */
private void addMethod(ClassWriter writer) {
    MethodVisitor methodVisitor = writer.visitMethod(
            // 方法的访问标志
            ACC_PUBLIC,
            // 方法名
            "string2int",
            // 方法描述符
            "(Ljava/lang/String;)I",
            // 泛型信息
            null,
            // 抛出的异常
            new String[]{}
    );
    // 设置方法体
    setMethodBody(methodVisitor);
    // 方法操作结束
    methodVisitor.visitEnd();
}
```

## 设置方法体

设置方法体的过程:

1. 调用 visitCode 方法标记方法体开始
2. 调用 visitXxxInsn 系列方法设置字节码指令
3. 调用 visitMaxs 方法设置最大栈深度和最大局部变量索引并标记方法体结束

```java
/**
 * 设置方法体
 */
private void setMethodBody(MethodVisitor methodVisitor) {
    // 方法体开始
    methodVisitor.visitCode();
    // 方法体内容: return Integer.parseInt(param);
    // 把参数放入栈顶
    methodVisitor.visitVarInsn(ALOAD, 1);
    // 调用Integer.parseInt方法,
    // 返回值存放到栈顶
    methodVisitor.visitMethodInsn(
            // INVOKESTATIC指令
            INVOKESTATIC,
            // 方法所在的类
            "java/lang/Integer",
            // 方法名
            "parseInt",
            // 方法描述符
            "(Ljava/lang/String;)I",
            // 是否为接口中定义的方法
            false
    );
    // 返回栈顶的值
    methodVisitor.visitInsn(IRETURN);
    // 方法体结束
    // 由于创建ClassWriter对象时使用了COMPUTE_FRAMES
    // 这里的max_stacks和max_locals设置会被忽略
    methodVisitor.visitMaxs(0, 0);
}
```

## 设置类的构造器

类的构造器`<init>()`也是使用 visitMethod 方法添加:

```java
/**
 * 设置类的构造器
 */
private void setConstructor(ClassWriter writer) {
    // 生成<init>()方法
    MethodVisitor init = writer.visitMethod(ACC_PUBLIC,
            "<init>", "()V", null, null);
    init.visitCode();
    // 调用父类构造器(必须): super();
    init.visitVarInsn(ALOAD, 0);
    init.visitMethodInsn(INVOKESPECIAL,
            "java/lang/Object", "<init>", "()V", false);
    init.visitInsn(RETURN);
    init.visitMaxs(0, 0);
    init.visitEnd();
}
```

## 使用生成的类

要实例化动态生成的类, 先要自定义一个类加载器:

```java
public class MyClassLoader extends ClassLoader {

    /**
     * 根据字节数组加载类
     *
     * @param fullClassName 类的全限定名
     * @param b             类的字节数组
     * @return class
     */
    public Class<?> load(String fullClassName, byte[] b) {
        return defineClass(fullClassName, b, 0, b.length);
    }
}
```

通过自定义类加载器加载并实例化动态生成的类:

```java
public static void main(String[] args) {
    // 创建类
    byte[] byteArray = new ClassCreator().create();
    // 使用class
    MyClassLoader classLoader = new MyClassLoader();
    Class<?> klass = classLoader.load("org.example.MyDemo", byteArray);
    // 反射调用
    try {
        Object myDemo = klass.newInstance();
        Method string2int = klass.getMethod("string2int", String.class);
        Object returnedValue = string2int.invoke(myDemo, "100");
        System.out.println((int) returnedValue);
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
}
```
