# 本地模拟

### 1. 待增强的目标类

```java
package hello;

/**
 * 待增强的目标类
 */
public class HelloService {

    public String sayHello(String name) {
        System.out.println("Business logic: sayHello(" + name + ")");
        if ("error".equalsIgnoreCase(name)) {
            throw new RuntimeException("test exception");
        }
        return "Hello, " + name;
    }

    public static void main(String[] args) throws Exception {
        HelloService service = new HelloService();
        System.out.println(service.sayHello("world"));
        System.out.println("--------------");
        try {
            service.sayHello("error");
        } catch (Exception e) {
            System.out.println("Caught in main: " + e.getMessage());
        }
    }
}
```

### 2. Java Agent 模块

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.example</groupId>
        <artifactId>maven-demo</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>agent</artifactId>
    <packaging>jar</packaging>

    <name>agent</name>
    <url>http://maven.apache.org</url>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.ow2.asm</groupId>
            <artifactId>asm</artifactId>
            <version>9.5</version>
        </dependency>
        <dependency>
            <groupId>org.ow2.asm</groupId>
            <artifactId>asm-commons</artifactId>
            <version>9.5</version>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <!-- 1. 生成带 Premain-Class 的 MANIFEST -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <archive>
                        <manifestEntries>
                            <!-- Agent 入口 -->
                            <Premain-Class>agent.MyAgent</Premain-Class>
                            <!-- 如果需要运行时重新增强，可以加上 -->
                            <Can-Redefine-Classes>true</Can-Redefine-Classes>
                            <Can-Retransform-Classes>true</Can-Retransform-Classes>
                        </manifestEntries>
                    </archive>
                </configuration>
            </plugin>
            <!-- 2. 打成 fat jar，把 ASM 也打进来 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.5.1</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                        <configuration>
                            <createDependencyReducedPom>false</createDependencyReducedPom>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

### 3. MyAgent.java

```java
package agent;

import java.lang.instrument.Instrumentation;

public class MyAgent {

    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("[Agent] premain, args: " + agentArgs);
        inst.addTransformer(new MyClassFileTransformer(), true);
    }
}
```

### 4. MyClassFileTransformer：筛选并增强

```java
package agent;

import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.ClassWriter;

import java.lang.instrument.ClassFileTransformer;
import java.security.ProtectionDomain;

import static org.objectweb.asm.Opcodes.ASM9;

public class MyClassFileTransformer implements ClassFileTransformer {

    @Override
    public byte[] transform(ClassLoader loader,
                            String className,
                            Class<?> classBeingRedefined,
                            ProtectionDomain protectionDomain,
                            byte[] classfileBuffer) {

        // 只增强 hello/HelloService
        if (!"hello/HelloService".equals(className)) {
            // 其它类不做处理
            return null;
        }

        System.out.println("[Agent] Transforming class: " + className);

        try {
            ClassReader cr = new ClassReader(classfileBuffer);
            ClassWriter cw = new ClassWriter(cr, ClassWriter.COMPUTE_MAXS | ClassWriter.COMPUTE_FRAMES);
            // 定义修改的逻辑
            ClassVisitor cv = new TraceClassVisitor(ASM9, cw);
            // 读取并修改HelloService类的字节码
            cr.accept(cv, ClassReader.EXPAND_FRAMES);
            return cw.toByteArray();
        } catch (Exception e) {
            e.printStackTrace();
            return null; // 出问题就不改字节码
        }
    }
}
```

### 5. TraceClassVisitor

```java
package agent;

import org.objectweb.asm.*;

public class TraceClassVisitor extends ClassVisitor {

    private String className;

    public TraceClassVisitor(int api, ClassVisitor classVisitor) {
        super(api, classVisitor);
    }

    @Override
    public void visit(int version,
                      int access,
                      String name,
                      String signature,
                      String superName,
                      String[] interfaces) {
        this.className = name;
        super.visit(version, access, name, signature, superName, interfaces);
    }

    @Override
    public MethodVisitor visitMethod(int access,
                                     String name,
                                     String descriptor,
                                     String signature,
                                     String[] exceptions) {

        MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);

        // 跳过构造方法和静态代码块
        if (mv == null || "<init>".equals(name) || "<clinit>".equals(name)) {
            return mv;
        }

        // 包一层我们自己的 MethodVisitor
        return new TraceMethodVisitor(api, mv, access, name, descriptor, className);
    }
}
```

### 6. TraceMethodVisitor

```java
package agent;

import org.objectweb.asm.Label;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.commons.AdviceAdapter;

public class TraceMethodVisitor extends AdviceAdapter {

    private final String methodName;
    private final String className;

    // 用于存储 startTime 的本地变量索引
    private int startTimeLocalIndex;
    // try-catch 块 label
    private Label startLabel = new Label();
    private Label endLabel = new Label();

    protected TraceMethodVisitor(int api,
                                 MethodVisitor mv,
                                 int access,
                                 String name,
                                 String descriptor,
                                 String className) {
        super(api, mv, access, name, descriptor);
        this.methodName = name;
        this.className = className;
    }

    @Override
    public void visitCode() {
        super.visitCode();
        // 标记 try 块开始
        mark(startLabel);
    }

    @Override
    protected void onMethodEnter() {
        // long start = System.currentTimeMillis();
        mv.visitMethodInsn(INVOKESTATIC,
                "java/lang/System",
                "currentTimeMillis",
                "()J",
                false);
        // 新建一个本地变量保存 start
        startTimeLocalIndex = newLocal(org.objectweb.asm.Type.LONG_TYPE);
        mv.visitVarInsn(LSTORE, startTimeLocalIndex);

        // 打印进入日志
        mv.visitFieldInsn(GETSTATIC,
                "java/lang/System",
                "out",
                "Ljava/io/PrintStream;");
        mv.visitLdcInsn("[ASM] Enter " + className + "." + methodName + "()");
        mv.visitMethodInsn(INVOKEVIRTUAL,
                "java/io/PrintStream",
                "println",
                "(Ljava/lang/String;)V",
                false);
    }

    @Override
    protected void onMethodExit(int opcode) {
        // 对正常出口（包括返回值、void 等）做耗时统计
        if (opcode == RETURN ||
                opcode == IRETURN ||
                opcode == FRETURN ||
                opcode == ARETURN ||
                opcode == LRETURN ||
                opcode == DRETURN) {

            printCostTime();
        }
        // 如果是 ATHROW，就不要在这里处理，在 visitMaxs 里统一加 catch
    }

    private void printCostTime() {
        // long end = System.currentTimeMillis();
        mv.visitMethodInsn(INVOKESTATIC,
                "java/lang/System",
                "currentTimeMillis",
                "()J",
                false);
        int endTimeIndex = newLocal(org.objectweb.asm.Type.LONG_TYPE);
        mv.visitVarInsn(LSTORE, endTimeIndex);

        // long cost = end - start;
        mv.visitVarInsn(LLOAD, endTimeIndex);
        mv.visitVarInsn(LLOAD, startTimeLocalIndex);
        mv.visitInsn(LSUB);
        int costIndex = newLocal(org.objectweb.asm.Type.LONG_TYPE);
        mv.visitVarInsn(LSTORE, costIndex);

        // System.out.println("[ASM] Exit xxx, cost = " + cost + " ms");
        mv.visitFieldInsn(GETSTATIC,
                "java/lang/System",
                "out",
                "Ljava/io/PrintStream;");
        mv.visitTypeInsn(NEW, "java/lang/StringBuilder");
        mv.visitInsn(DUP);
        mv.visitLdcInsn("[ASM] Exit " + className + "." + methodName + "(), cost = ");
        mv.visitMethodInsn(INVOKESPECIAL,
                "java/lang/StringBuilder",
                "<init>",
                "(Ljava/lang/String;)V",
                false);
        mv.visitVarInsn(LLOAD, costIndex);
        mv.visitMethodInsn(INVOKEVIRTUAL,
                "java/lang/StringBuilder",
                "append",
                "(J)Ljava/lang/StringBuilder;",
                false);
        mv.visitLdcInsn(" ms");
        mv.visitMethodInsn(INVOKEVIRTUAL,
                "java/lang/StringBuilder",
                "append",
                "(Ljava/lang/String;)Ljava/lang/StringBuilder;",
                false);
        mv.visitMethodInsn(INVOKEVIRTUAL,
                "java/lang/StringBuilder",
                "toString",
                "()Ljava/lang/String;",
                false);
        mv.visitMethodInsn(INVOKEVIRTUAL,
                "java/io/PrintStream",
                "println",
                "(Ljava/lang/String;)V",
                false);
    }

    @Override
    public void visitMaxs(int maxStack, int maxLocals) {
        // 标记 try 块结束
        mark(endLabel);

        // 新建一个 label 作为异常处理块的开始
        Label handlerLabel = new Label();
        mv.visitLabel(handlerLabel);

        // catch 块的异常对象存入一个本地变量
        int exIndex = newLocal(org.objectweb.asm.Type.getType(Throwable.class));
        mv.visitVarInsn(ASTORE, exIndex);

        // 打印异常日志
        mv.visitFieldInsn(GETSTATIC,
                "java/lang/System",
                "out",
                "Ljava/io/PrintStream;");
        mv.visitTypeInsn(NEW, "java/lang/StringBuilder");
        mv.visitInsn(DUP);
        mv.visitLdcInsn("[ASM] Exception in " + className + "." + methodName + "(): ");
        mv.visitMethodInsn(INVOKESPECIAL,
                "java/lang/StringBuilder",
                "<init>",
                "(Ljava/lang/String;)V",
                false);
        mv.visitVarInsn(ALOAD, exIndex);
        mv.visitMethodInsn(INVOKEVIRTUAL,
                "java/lang/Throwable",
                "getMessage",
                "()Ljava/lang/String;",
                false);
        mv.visitMethodInsn(INVOKEVIRTUAL,
                "java/lang/StringBuilder",
                "append",
                "(Ljava/lang/String;)Ljava/lang/StringBuilder;",
                false);
        mv.visitMethodInsn(INVOKEVIRTUAL,
                "java/lang/StringBuilder",
                "toString",
                "()Ljava/lang/String;",
                false);
        mv.visitMethodInsn(INVOKEVIRTUAL,
                "java/io/PrintStream",
                "println",
                "(Ljava/lang/String;)V",
                false);

        // 异常重新抛出，保持原语义
        mv.visitVarInsn(ALOAD, exIndex);
        mv.visitInsn(ATHROW);

        // 注册 try-catch 块：catch Throwable
        mv.visitTryCatchBlock(startLabel, endLabel, handlerLabel, "java/lang/Throwable");

        super.visitMaxs(maxStack, maxLocals);
    }
}
```

### 7. 运行这个 demo

1. 打包 agent
2. 运行

```sh
/Users/walter/jdk/jdk8u402.jdk/bin/java -javaagent:/Users/walter/IdeaProjects/maven-demo/agent/target/agent-1.0-SNAPSHOT.jar -cp /Users/walter/IdeaProjects/maven-demo/hello/target/classes hello.HelloService
```

3. 控制台预计输出类似

```
[Agent] premain, args: null
[Agent] Transforming class: hello/HelloService
[ASM] Enter hello/HelloService.main()
[ASM] Enter hello/HelloService.sayHello()
Business logic: sayHello(world)
[ASM] Exit hello/HelloService.sayHello(), cost = 0 ms
Hello, world
--------------
[ASM] Enter hello/HelloService.sayHello()
Business logic: sayHello(error)
[ASM] Exception in hello/HelloService.sayHello(): test exception
Caught in main: test exception
[ASM] Exit hello/HelloService.main(), cost = 0 ms
```
