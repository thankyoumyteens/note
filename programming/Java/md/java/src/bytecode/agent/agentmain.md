# 修改已经加载的类

## 添加依赖

```xml
<dependencies>
   <dependency>
       <groupId>org.ow2.asm</groupId>
       <artifactId>asm</artifactId>
       <version>9.6</version>
   </dependency>
</dependencies>
```

## 实现 ClassFileTransformer 接口

```java
public class MyTransformer implements ClassFileTransformer {
    @Override
    public byte[] transform(
            Module module,
            ClassLoader loader,
            String className,
            Class<?> classBeingRedefined,
            ProtectionDomain protectionDomain,
            byte[] classFileBuffer
    ) throws IllegalClassFormatException {
        if (className.equals("org/example/Bird")) {
            // 使用ASM修改App类的内容
            ClassReader classReader = new ClassReader(classFileBuffer);
            ClassWriter classWriter = new ClassWriter(ClassWriter.COMPUTE_MAXS);
            // 修改main方法的方法体
            classReader.accept(
                    new ClassVisitor(Opcodes.ASM9, classWriter) {
                        @Override
                        public MethodVisitor visitMethod(int access, String name, String descriptor, String signature, String[] exceptions) {
                            MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);
                            if (name.equals("fly")) {
                                return new MethodVisitor(Opcodes.ASM9, mv) {
                                    @Override
                                    public void visitLdcInsn(Object value) {
                                        // 替换打印的内容
                                        if (value instanceof String) {
                                            value = "bird is flying...";
                                        }
                                        super.visitLdcInsn(value);
                                    }
                                };
                            }
                            // 其他方法不做修改, 直接返回原始的MethodVisitor
                            return mv;
                        }
                    },
                    ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES
            );
            // 返回修改的class
            return classWriter.toByteArray();
        }
        // 返回null表示不修改class内容
        return null;
    }
}
```

## 定义 Agent 的入口类

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
