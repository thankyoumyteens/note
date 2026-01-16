# 修改已经加载的类

有时候应用已经在跑了，你想“热插”一个 Agent 进去，这就用：

- Attach API（com.sun.tools.attach）
- 目标 JVM 进程会加载你的 agent JAR，并调用 agentmain 函数

### 1. 实现 ClassFileTransformer 接口

```java
public class MyTransformer implements ClassFileTransformer {

    @Override
    public byte[] transform(Module module, ClassLoader loader, String className, Class<?> classBeingRedefined, ProtectionDomain protectionDomain, byte[] classFileBuffer) throws IllegalClassFormatException {
        // 例如: 只修改MyApp类
        if (className.equals("org/example/MyApp")) {
            // 使用ASM修改App类
            ClassReader classReader = new ClassReader(classFileBuffer);
            ClassWriter classWriter = new ClassWriter(ClassWriter.COMPUTE_MAXS);
            ClassVisitor cv = new MyClassVisitor(Opcodes.ASM9, classWriter);
            classReader.accept(cv, ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES);
            // 返回修改后的字节码
            // JVM 会加载修改后的字节码
            return classWriter.toByteArray();
        }
        // 返回 null 表示不修改字节码
        // JVM 会加载原始的字节码
        return null;
    }
}
```

### 2. 定义 Agent 的入口类

```java
public class MyAgent {
    public static void agentmain(String args, Instrumentation inst) {
        inst.addTransformer(new MyTransformer(), true);
        try {
            // 重新加载新的Bird类
            inst.retransformClasses(Class.forName("org.example.Bird"));
        } catch (UnmodifiableClassException | ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
    }
}
```

## 配置打包

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-jar-plugin</artifactId>
            <version>3.3.0</version>
            <configuration>
                <archive>
                    <!-- 自动添加 META-INF/MANIFEST.MF -->
                    <manifest>
                        <addClasspath>true</addClasspath>
                    </manifest>
                    <manifestEntries>
                        <Agent-Class>org.example.MyAgent</Agent-Class>
                        <Can-Redefine-Classes>true</Can-Redefine-Classes>
                        <Can-Retransform-Classes>true</Can-Retransform-Classes>
                    </manifestEntries>
                </archive>
            </configuration>
        </plugin>
        <!-- 将依赖的jar包打入项目-->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-shade-plugin</artifactId>
            <version>3.5.2</version>
            <executions>
                <execution>
                    <id>shade-when-package</id>
                    <phase>package</phase>
                    <goals>
                        <goal>shade</goal>
                    </goals>
                    <configuration>
                        <artifactSet>
                            <includes>
                                <include>org.ow2.asm:asm</include>
                            </includes>
                        </artifactSet>
                        <shadeSourcesContent>true</shadeSourcesContent>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

执行 mvn package

## 测试类

```java
// 要被修改的类
public class Bird {
    public static void fly() {
        System.out.println("bird want to fly...");
    }
}

public class App {
    public static void main(String[] args) throws InterruptedException {
        Bird.fly();
        while (true) {
            // 等待agent注入
            Thread.sleep(1000);
            Bird.fly();
        }
    }
}
```

## 使用 agent

编写一个类, 用于注入 agent:

```java
public class AttachDemo {

    public static void main(String[] args) throws AgentLoadException, IOException, AgentInitializationException, AttachNotSupportedException {
        // 当前正在运行的jvm
        List<VirtualMachineDescriptor> vmList = VirtualMachine.list();
        for (VirtualMachineDescriptor vm : vmList) {
            // 找到测试类所在的jvm
            if ("org.example.App".equals(vm.displayName())) {
                    // 连接目标jvm
                    VirtualMachine virtualMachine = VirtualMachine.attach(vm.id());
                    // 注入agent
                    virtualMachine.loadAgent("/刚才打的jar包路径/my-agent-1.0-SNAPSHOT.jar");
                    // 断开连接
                    virtualMachine.detach();
            }
        }
    }
}
```

## AttachDemo 类输出

```
92083 : com.intellij.idea.Main
...
93133 : org.example.App
93135 : org.example.AttachDemo
687 : com.intellij.idea.Main
...
```

## App 类输出

```
bird want to fly...
bird want to fly...
WARNING: A Java agent has been loaded dynamically (/刚才打的jar包路径/my-agent-1.0-SNAPSHOT.jar)
WARNING: If a serviceability tool is in use, please run with -XX:+EnableDynamicAgentLoading to hide this warning
WARNING: If a serviceability tool is not in use, please run with -Djdk.instrument.traceUsage for more information
WARNING: Dynamic loading of agents will be disallowed by default in a future release
bird is flying...
bird is flying...
bird is flying...
```
