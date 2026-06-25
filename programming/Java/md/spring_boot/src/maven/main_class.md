# 指定主类

核心功能：

- 把 你的代码 + 依赖 jar 全部打进一个可运行的 JAR 里（胖包 / uber-jar）
- 可以对依赖里的类做：
  - 重定位（relocation）：改包名防冲突，例如把 com.google.common 改成 shadow.com.google.common
  - 合并某些资源文件（比如 META-INF/services/\*）
  - 修改 MANIFEST（比如指定 Main-Class）

## 把依赖打进 jar 包

只需要引入 maven-shade-plugin 即可：

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-shade-plugin</artifactId>
            <version>3.5.0</version>
            <executions>
                <execution>
                    <phase>package</phase>
                    <goals>
                        <goal>shade</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

默认情况下，maven-shade-plugin 会把：

- 当前模块自己的 classes
- 以及它的 依赖 JAR（compile / runtime scope）
- 一起合并成一个大 JAR（uber-jar）。

也就是说：不需要你逐个手动列出依赖，只要是 Maven 解析到的、属于这个模块的依赖（非 provided / 非 test），它都会打进去。

## 只打部分依赖/排除某些依赖

可以通过 `<artifactSet>` 来控制，比如：

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-shade-plugin</artifactId>
            <version>3.5.0</version>
            <executions>
                <execution>
                    <phase>package</phase>
                    <goals>
                        <goal>shade</goal>
                    </goals>
                    <configuration>
                        <!-- 只想要特定 groupId 的依赖，或者排除某几类 -->
                        <artifactSet>
                            <!-- 只包含这些依赖 -->
                            <includes>
                                <include>com.google.guava:guava</include>
                            </includes>
                            <!-- 要排除这些依赖 -->
                            <excludes>
                                <!-- 比如排除日志实现，避免跟宿主冲突 -->
                                <exclude>ch.qos.logback:logback-classic</exclude>
                                <exclude>org.slf4j:slf4j-log4j12</exclude>
                            </excludes>
                        </artifactSet>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

## 指定主类/agent 入口类

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-shade-plugin</artifactId>
            <version>3.5.0</version>
            <executions>
                <execution>
                    <phase>package</phase>
                    <goals>
                        <goal>shade</goal>
                    </goals>
                    <configuration>
                        <transformers>
                            <transformer
                                    implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                <!-- 指定主类 -->
                                <mainClass>com.example.App</mainClass>
                                <!-- java agent 相关配置 -->
                                <manifestEntries>
                                    <!-- 启动时使用 -javaagent:xxx.jar 的入口类 -->
                                    <Premain-Class>com.example.agent.MyAgent</Premain-Class>
                                    <!-- 运行中通过 Attach API 动态加载 agent 时的入口类 -->
                                    <Agent-Class>com.example.agent.MyAgent</Agent-Class>
                                    <!-- 是否允许通过 Instrumentation.redefineClasses 重定义已加载类 -->
                                    <Can-Redefine-Classes>true</Can-Redefine-Classes>
                                    <!-- 是否允许通过 retransformClasses 重新转换已加载类 -->
                                    <Can-Retransform-Classes>true</Can-Retransform-Classes>
                                    <!-- 是否允许给 native 方法设置前缀，用于 JVMTI 配合等高级玩法 -->
                                    <Can-Set-Native-Method-Prefix>true</Can-Set-Native-Method-Prefix>
                                </manifestEntries>
                            </transformer>
                        </transformers>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

## 包名重定位

背景问题：如果你的 Agent 里用到了一个库（比如 Guava），目标应用里也用另一个版本的 Guava，

- 不重定位就共享同一个类加载器里的 `com.google.common.*`，版本冲突、NoSuchMethod、ClassNotFound 一堆坑。
- 通过 relocation，把你的依赖改名为 `shadow.com.google.common.*`，从此两边各玩各的，互不干扰。

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-shade-plugin</artifactId>
            <version>3.5.0</version>
            <executions>
                <execution>
                    <phase>package</phase>
                    <goals>
                        <goal>shade</goal>
                    </goals>
                    <configuration>
                        <relocations>
                            <relocation>
                                <!-- 注意这里是包名，而不是groupId -->
                                <pattern>com.google.common</pattern>
                                <!--
                                 打包后，会自动把代码中所有 import 的 com.google.common 包
                                 改成 shadow.com.google.common
                                -->
                                <shadedPattern>shadow.com.google.common</shadedPattern>
                            </relocation>
                        </relocations>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```
