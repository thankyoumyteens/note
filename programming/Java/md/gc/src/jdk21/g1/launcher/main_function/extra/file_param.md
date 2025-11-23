# 参数文件

在 Java 中，`@file` 形式的参数文件是一种将命令行参数集中写入文件，再通过 `@文件名` 语法在执行时引用该文件的方式。它的核心作用是简化长命令行、管理复杂参数（比如大量 JVM 选项、程序参数、配置路径等），避免命令行过长或参数遗漏。

## 编写参数文件

创建一个文本文件（如 app.args），写入 JVM 参数、程序参数等

```sh
# ==================== JVM 启动参数 ====================
-Xms512m                # 初始堆内存
-Xmx1024m               # 最大堆内存
-XX:+UseG1GC            # 使用 G1 垃圾收集器
-Dspring.profiles.active=prod  # 系统属性（Spring 环境）
-Dlog.path=/var/log/app # 日志路径配置

# ==================== 程序自身参数 ====================
--server.port=8080      # 程序端口
--config.path="C:\Program Files\app\config.yml"  # 含空格的路径
--timeout=3000          # 超时时间（毫秒）
--features=cache,logger # 多值参数（逗号分隔）
```

## 执行 Java 程序时引用参数文件

通过 `java @参数文件路径 -jar 程序.jar` 语法执行

```sh
# 基础格式（参数文件与 jar 同目录）
java @app.args -jar myapp.jar

# 绝对路径引用（参数文件在其他目录）
java @/home/user/config/app.args -jar /home/user/app/myapp.jar
```
