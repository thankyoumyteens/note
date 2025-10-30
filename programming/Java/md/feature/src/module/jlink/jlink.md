# jlink

`jlink` 的核心参数：

- `--module-path`：指定模块路径, 需要包含项目模块 JAR 和 JDK 自带的模块(`$JAVA_HOME/jmods` 是 JDK 的模块目录)
- `--add-modules`：指定要包含的模块, 一般是主模块，`jlink` 会自动添加主模块依赖的模块。注意: 如果使用了服务, 服务提供模块也需要手动指定
- `--output`：指定输出目录（自定义运行时的安装路径）
- `--launcher`：可选，创建一个启动脚本, 格式: `启动脚本名=模块/主类`

```bash
jlink \
  --module-path "modules:$JAVA_HOME/jmods" \  # 项目模块 + JDK 模块
  --add-modules calculator.ui \               # 主模块（自动包含依赖）
  --add-modules calculator.impl \             # 服务提供模块需要手动添加
  --output calculator-runtime \               # 输出目录
  --launcher calculator=calculator.ui/com.example.App \  # 生成启动脚本（可选）
  --strip-debug \                             # 移除调试信息（减小体积）
  --no-man-pages \                            # 不包含手册页
  --no-header-files                           # 不包含头文件
```

生成的 `calculator-runtime` 目录包含精简的 JRE 结构：

```sh
calculator-runtime/
├── bin/           # 包含启动脚本（如 calculator、java）
├── conf/          # 配置文件
├── lib/           # 运行时库（仅包含必要模块）
└── legal/         # 许可信息
```

可以提供多个以逗号分隔的根模块，而不是像此处使用多个 `--add-modules`, 比如:

```sh
--add-modules calculator.ui,calculator.impl
```

服务提供者模块也必须作为根模块添加。默认情况下 jlink 只会解析 requires 指定的模块, 不会解析 uses 和 provides 的依赖关系。可以使用 `--bind-services` 指示 jlink 在解析模块时考虑 uses/provides。但是，这样一来就绑定了平台模块之间的所有服务。因为 `java.base` 模块已经使用了很多(可选的)服务，所以这样做会导致重复解析更多不需要的已解析模块。
