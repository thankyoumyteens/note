# 基本用法

做一个很经典的事：给一个类的所有方法开头都插一行：System.out.println("enter method xxx");

### 1. 准备一个原始类

```java
// Demo.java
public class Demo {
    public void sayHello(String name) {
        System.out.println("Hello, " + name);
    }

    public int add(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) {
        Demo d = new Demo();
        d.sayHello("World");
        System.out.println("add result = " + d.add(1, 2));
    }
}
```

先编译：

```sh
javac Demo.java
```

### 2. 引入 ASM 依赖

这里用到 asm-commons 是为了简化插桩操作（里面有个 AdviceAdapter 很好用）。

```xml
<dependencies>
  <dependency>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm</artifactId>
    <version>9.6</version>
  </dependency>
  <dependency>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm-commons</artifactId>
    <version>9.6</version>
  </dependency>
</dependencies>
```

### 3. 写一个最简单的“方法增强器”

我们写一个类，读取已有的 Demo.class，然后在每个方法的开头插入一条打印语句，最后把新字节码写到一个新文件里，比如 DemoEnhanced.class。

核心逻辑就两个点：

1. ClassReader 把 class 文件“走一遍”，每到一个方法就触发一次 visitMethod
2. 我们用 AdviceAdapter 的 onMethodEnter() 在方法入口插入字节码

```java
// AsmSimpleDemo.java
import org.objectweb.asm.*;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

import static org.objectweb.asm.Opcodes.ASM9;

public class AsmSimpleDemo {
    public static void main(String[] args) throws IOException {
        // 1. 读取原始 Demo.class
        String className = "Demo"; // 同目录下的 Demo.class
        FileInputStream fis = new FileInputStream(className + ".class");
        byte[] originalBytes = fis.readAllBytes();
        fis.close();

        // 2. 用 ClassReader 解析字节码
        ClassReader cr = new ClassReader(originalBytes);

        // 3. 准备 ClassWriter，用于写出修改后的字节码
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);

        // 4. 自定义 ClassVisitor，用于修改类
        ClassVisitor cv = new ClassVisitor(ASM9, cw) {
            @Override
            public MethodVisitor visitMethod(int access, String name, String descriptor,
                                             String signature, String[] exceptions) {
                // 先拿到原始的 MethodVisitor
                MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);

                // main 方法也会经过这里，我们也给它插入日志（你想过滤也可以）
                if (mv == null) {
                    return null;
                }

                // 包一层我们自己的 MethodVisitor，在 onMethodEnter 时插入字节码
                return new org.objectweb.asm.commons.AdviceAdapter(ASM9, mv, access, name, descriptor) {
                    @Override
                    protected void onMethodEnter() {
                        // 在方法一开始插入：
                        // System.out.println("enter method: " + 方法名);

                        // 相当于 Java 代码：
                        // System.out.println("enter method: " + name);

                        // 生成字节码步骤：

                        // 1. 获取 System.out（静态字段）
                        visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");

                        // 2. 压入字符串常量
                        visitLdcInsn("enter method: " + name);

                        // 3. 调用 PrintStream.println(String)
                        visitMethodInsn(INVOKEVIRTUAL,
                                "java/io/PrintStream",
                                "println",
                                "(Ljava/lang/String;)V",
                                false);
                    }
                };
            }
        };

        // 5. 触发读取 + 访问（会回调上面的 ClassVisitor + MethodVisitor）
        cr.accept(cv, ClassReader.EXPAND_FRAMES);

        // 6. 拿到增强后的字节码
        byte[] modifiedBytes = cw.toByteArray();

        // 7. 写入新文件 DemoEnhanced.class
        File outFile = new File("DemoEnhanced.class");
        FileOutputStream fos = new FileOutputStream(outFile);
        fos.write(modifiedBytes);
        fos.close();

        System.out.println("修改完成，生成：" + outFile.getAbsolutePath());
    }
}
```

### 4. 生成增强后的类

```sh
javac -cp .:asm-9.6.jar:asm-commons-9.6.jar AsmSimpleDemo.java
java -cp .:asm-9.6.jar:asm-commons-9.6.jar AsmSimpleDemo
```

此时目录里会多一个：DemoEnhanced.class

### 5. 执行增强后的类

因为类名还是 Demo，但文件叫 DemoEnhanced.class，所以直接改文件名覆盖原来的并运行

```sh
mv DemoEnhanced.class Demo.class
java Demo
```

你会看到输出类似：

```
enter method: <init>
enter method: main
enter method: sayHello
Hello, World
enter method: add
add result = 3
```

说明每个方法一开始都被插入了 println。

`<init>` 就是构造方法。
