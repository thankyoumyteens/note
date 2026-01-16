# 在类加载的时候修改类

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

JVM 启动时会自动调用 premain 函数

```java
public class MyAgent {
    public static void premain(String args, Instrumentation inst) {
        // 注册自己实现的ClassFileTransformer
        inst.addTransformer(new MyTransformer(), true);
    }
}
```

### 3. 打包时指定入口

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
                        <!-- MANIFEST.MF 里要指定 agent 的入口类 -->
                        <Premain-Class>org.example.MyAgent</Premain-Class>
                        <Can-Redefine-Classes>true</Can-Redefine-Classes>
                        <Can-Retransform-Classes>true</Can-Retransform-Classes>
                    </manifestEntries>
                </archive>
            </configuration>
        </plugin>
        <!-- 将依赖的 jar 包打入-->
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
                                <!-- 打入依赖的 asm 包 -->
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

### 4. 使用 agent

启动时通过 JVM 参数指定 agent:

```sh
java -javaagent:/path/to/your-agent.jar -jar app.jar
```

### 5. 输出

```
do something before main method!
Hello World!
```
