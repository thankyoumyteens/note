# ASM 搭配 Java Agent 使用

Java Agent 本质就是一个带特殊入口的 jar，通过 JVM 启动参数加载：

```sh
java -javaagent:/path/to/your-agent.jar -jar app.jar
```

Agent JAR 的 MANIFEST.MF 里需要有：

```
Premain-Class: your.package.YourAgent
```

然后 JVM 启动时会调用 Agent JAR 中的：

```java
public static void premain(String agentArgs, Instrumentation inst)
```

如果支持运行时 attach，还会调用 Agent JAR 中的：

```java
public static void agentmain(String agentArgs, Instrumentation inst)
```

只要记住：拿到 Instrumentation，就有了“拦截/修改类加载”的能力。

## 在 Agent 里接入 ASM 的标准套路

核心点就是用 Instrumentation 注册一个 ClassFileTransformer，在里面用 ASM 修改字节码。

### 1. Agent 入口

```java
public class MyAgent {
  public static void premain(String agentArgs, Instrumentation inst) {
    inst.addTransformer(new MyClassFileTransformer(), true);
  }
}
```

### 2. ClassFileTransformer 里使用 ASM

```java
public class MyClassFileTransformer implements ClassFileTransformer {

  @Override
  public byte[] transform(Module module, ClassLoader loader, String className, Class<?> classBeingRedefined, ProtectionDomain protectionDomain, byte[] classfileBuffer) {

    // 1. 过滤一下不想处理的类，比如 JDK、自身 agent 等
    if (!shouldTransform(className)) {
      return null; // 返回 null = 不修改
    }

    try {
      // 2. 用 ASM 读取原始 class
      ClassReader cr = new ClassReader(classfileBuffer);
      // 3. 用 ClassWriter 接上，通常用 COMPUTE_MAXS / COMPUTE_FRAMES 省事
      ClassWriter cw = new ClassWriter(cr, ClassWriter.COMPUTE_FRAMES);
      // 4. 自定义 ClassVisitor，里面再用 MethodVisitor / AdviceAdapter 等做增强
      ClassVisitor cv = new MyClassVisitor(Opcodes.ASM9, cw);
      // 5. 触发解析+访问
      cr.accept(cv, ClassReader.EXPAND_FRAMES);
      // 6. 返回修改后的字节码
      return cw.toByteArray();
    } catch (Throwable t) {
      t.printStackTrace();
      // 出问题就别破坏类加载，返回 null 表示用原始字节码
      return null;
    }
  }
}
```
