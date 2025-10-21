# 使用 jlink 构建镜像

jlink 能将模块及其依赖的 JDK 模块打包成一个精简的、可直接运行的 Java 运行时，不依赖系统安装的 JDK/JRE。

### 1. 整理模块 JAR 到统一目录

```bash
# 在项目根目录创建 modules 目录
mkdir -p modules

# 复制各模块的 JAR 到 modules 目录
cp calculator/target/calculator-1.0-SNAPSHOT.jar modules/
cp calculator-impl/target/calculator-impl-1.0-SNAPSHOT.jar modules/
cp ui/target/ui-1.0-SNAPSHOT.jar modules/
```

### 2. 执行 jlink 命令生成运行时镜像

`jlink` 的核心参数：

- `--module-path`：指定模块路径, 需要包含项目模块 JAR 和 JDK 自带的模块(`$JAVA_HOME/jmods` 是 JDK 的模块目录)
- `--add-modules`：指定要包含的模块, 一般是主模块，`jlink` 会自动添加主模块依赖的模块。注意: 如果使用了服务, 服务提供模块也需要手动指定
- `--output`：指定输出目录（自定义运行时的安装路径）
- `--launcher`：可选，创建一个启动脚本, 格式: `启动脚本名=模块/主类`

```bash
# 执行时需要删掉后面的注释
jlink \
  --module-path "modules:$JAVA_HOME/jmods" \  # 项目模块 + JDK 模块
  --add-modules calculator.ui \             # 主模块（自动包含依赖）
  --add-modules calculator.impl \  # 服务提供模块需要手动添加
  --output calculator-runtime \              # 输出目录
  --launcher calculator=calculator.ui/com.example.App \  # 生成启动脚本（可选）
  --strip-debug \                            # 移除调试信息（减小体积）
  --no-man-pages \                           # 不包含手册页
  --no-header-files                          # 不包含头文件
```

生成的 `calculator-runtime` 目录包含精简的 JRE 结构：

```sh
calculator-runtime/
├── bin/           # 包含启动脚本（如 calculator、java）
├── conf/          # 配置文件
├── lib/           # 运行时库（仅包含必要模块）
└── legal/         # 许可信息
```

### 3. 运行程序

```sh
./calculator-runtime/bin/calculator
```

## 通过 maven 自动执行 jlink

为避免手动执行 `jlink`，可在 `ui` 模块的 `pom.xml` 中添加 `maven-antrun-plugin`，在打包后自动调用 `jlink`：

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-antrun-plugin</artifactId>
    <version>3.1.0</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>run</goal>
            </goals>
            <configuration>
                <target>
                    <!-- 删除旧的运行时目录 -->
                    <delete dir="alculator-runtime"/>
                    <!-- 创建 modules 目录并复制 JAR -->
                    <mkdir dir="modules"/>
                    <copy file="../calculator/target/calculator-1.0-SNAPSHOT.jar" todir="modules"/>
                    <copy file="../calculator-impl/target/calculator-impl-1.0-SNAPSHOT.jar" todir="modules"/>
                    <copy file="target/ui-1.0-SNAPSHOT.jar" todir="modules"/>

                    <!-- 执行 jlink 命令 -->
                    <exec executable="jlink">
                        <arg line="--module-path 'modules:${java.home}/jmods'"/>
                        <arg line="--add-modules calculator.ui"/>
                        <arg line="--add-modules calculator.impl"/>
                        <arg line="--output calculator-runtime"/>
                        <arg line="--launcher calculator=calculator.ui/com.example.App"/>
                        <arg line="--strip-debug --no-man-pages --no-header-files"/>
                    </exec>
                </target>
            </configuration>
        </execution>
    </executions>
</plugin>
```

执行 `mvn clean package` 后，会自动在 `ui` 目录下生成 `calculator-runtime` 目录。
