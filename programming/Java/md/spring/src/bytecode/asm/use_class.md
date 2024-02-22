# 使用生成的类

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
    byte[] byteArray = writer.toByteArray();
    // 使用class
    MyClassLoader classLoader = new MyClassLoader();
    Class<?> klass = classLoader.load("org.example.MyDemo", byteArray);
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
