# 在类加载的时候修改类

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
        if (className.equals("org/example/App")) {
            // 使用ASM修改App类的内容
            ClassReader classReader = new ClassReader(classFileBuffer);
            ClassWriter classWriter = new ClassWriter(ClassWriter.COMPUTE_MAXS);
            // 修改main方法的方法体
            classReader.accept(
                    new ClassVisitor(Opcodes.ASM9, classWriter) {
                        @Override
                        public MethodVisitor visitMethod(int access, String name, String descriptor, String signature, String[] exceptions) {
                            MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);
                            if (name.equals("main")) {
                                return new MethodVisitor(Opcodes.ASM9, mv) {
                                    @Override
                                    public void visitCode() {
                                        // 在main方法的方法体前面插入一行代码
                                        mv.visitFieldInsn(Opcodes.GETSTATIC, "java/lang/System", "out",
                                                "Ljava/io/PrintStream;");
                                        mv.visitLdcInsn("do something before main method!");
                                        mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL,
                                                "java/io/PrintStream", "println",
                                                "(Ljava/lang/String;)V", false);
                                        super.visitCode();
                                    }
                                };
                            }
                            // 其他方法不做修改
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

premain 方法是 java agent 的入口, 它总会在 main 函数之前执行

```java
public class MyAgent {
    public static void premain(String args, Instrumentation inst) {
        // 注册自己实现的ClassFileTransformer
        inst.addTransformer(new MyTransformer(), true);
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
                        <Premain-Class>org.example.MyAgent</Premain-Class>
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
public class App {
    public static void main(String[] args) {
        System.out.println("Hello World!");
    }
}
```

## 使用 agent

启动时设置 JVM 参数:

```
-javaagent:/刚才打的jar包路径/my-agent-1.0-SNAPSHOT.jar
```

## 输出

```
do something before main method!
Hello World!
```
