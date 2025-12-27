# jvm.cfg 文件

jvm.cfg 是 Java 启动器（java、javaw 等）用来“映射”和“选择”JVM 类型的配置文件，决定：

- 哪些 JVM 类型可用（client / server / minimal / zero 等）
- 它们的优先级顺序
- 当你用 -client、-server、-Xmixed 等选项启动时，实际加载哪个 JVM 动态库（如 jvm.dll / libjvm.so）

## jvm.cfg 一般在哪里？

典型位置（以 JDK/JRE 安装目录为例）：

- Windows：`JAVA_HOME\jre\lib\i386\jvm.cfg` 或 `JAVA_HOME\jre\lib\amd64\jvm.cfg`
- Linux / macOS：`$JAVA_HOME/jre/lib/i386/jvm.cfg`、`$JAVA_HOME/jre/lib/amd64/jvm.cfg`、`$JAVA_HOME/lib/server/jvm.cfg` 等

不同版本和发行版路径会有差异，但都是在 JRE/JDK 的 lib 下、按架构区分。

内容类似这样（示例）：

```
-server KNOWN
-client KNOWN
-hotspot ALIASED_TO -server
-classic WARN
-native ERROR
-green ERROR
```

常见标志意义大致如下（不同版本略有差别）：

- KNOWN：表示这是一个可用的 JVM 类型，启动器会尝试加载对应的 libjvm 实现。
- ALIASED_TO：表示这是一个别名，例如 `-hotspot ALIASED_TO -server` 意味着你写 `java -hotspot` 实际等价于 `java -server`
- IGNORE：启动时如果用了这个类型，启动器会忽略它，通常用于兼容老选项而不报错。
- WARN：使用该类型会给出警告，但仍可能尝试运行或退回到默认。
- ERROR：指明这是不支持的 JVM 类型，一旦使用就会报错终止。

## 具体作用：控制 JVM 类型的解析与映射

当你在命令行启动 Java 时, Java 启动器会：

1. 读取 jvm.cfg
2. 根据你指定的 JVM 类型（-server、-client 等）在文件里查找相应条目
3. 决定：
   - 这是一个 有效的类型 吗？
   - 需要 别名映射 到其他类型吗？（ALIASED_TO）
   - 找不到或被标记为 ERROR、IGNORE 时要怎么办？

## -client / -server

在早期/某些版本的 JDK 中，同一平台可能存在多个 JVM 模式：

- client：启动更快、适合桌面应用
- server：启动慢一些，但长期运行性能更好，适合服务端

在现代很多发行版里，其实只有 server 模式，-client 可能会被标成 IGNORE 或 ALIASED_TO -server，保证老脚本不崩但实质上只跑 server。

## 会不会自己去改 jvm.cfg

一般不建议改，这属于 JDK/JRE 内部实现配置，平常调优 JVM、改 -Xmx、-Xms、GC 算法等都 不需要动它。

少数情况下，发行版厂商或嵌入式系统会改这个文件，用来：

- 移除不支持的 JVM 类型
- 把某些 JVM 名字映射到自家定制实现

## 出现 “Error: no known VMs” 等错误时

如果你看到类似错误：

```
Error: no known VMs. (check your jvm.cfg)
```

很可能是：

- jvm.cfg 文件丢失、损坏
- 里面引用的 JVM 类型在实际 jre/bin/client 或 jre/bin/server 中不存在
- 手动改过导致格式或内容异常

这时一般做法：

- 直接重装 JDK/JRE 或从同版本拷一份干净的 jvm.cfg 覆盖
- 确保环境变量 JAVA_HOME、PATH 指向的是同一套完整的 JDK/JRE
