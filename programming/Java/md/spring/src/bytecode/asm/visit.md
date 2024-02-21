# 设置类的基本信息

使用 visit 方法可用设置类的基本信息:

```java
public static void main(String[] args) {
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
    setConstructor(writer, "java/lang/Object");
    // 添加字段
    addField(writer);
    // 添加方法
    addMethod(writer);
    // 标记对类的操作结束
    writer.visitEnd();
    // 获取类的字节码
    byte[] byteArray = writer.toByteArray();
    // 写入到.class文件
    try (ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
         FileOutputStream fileOutputStream = new FileOutputStream("MyDemo.class")) {
        outputStream.write(byteArray);
        outputStream.writeTo(fileOutputStream);
        fileOutputStream.flush();
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
}
```
