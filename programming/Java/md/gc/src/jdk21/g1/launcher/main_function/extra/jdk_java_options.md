# 环境变量 JDK_JAVA_OPTIONS

JDK_JAVA_OPTIONS 是 JDK 9+ 引入的环境变量，用于为 java 命令（包括 javac、jar 等基于 JVM 的工具）统一指定 默认 JVM 参数，无需在每次执行 `java -jar xxx.jar` 时重复写参数。

## 设置 JDK_JAVA_OPTIONS 环境变量

当前终端临时生效:

```sh
export JDK_JAVA_OPTIONS="-Xms512m -Xmx1024m -XX:+UseG1GC -Duser.language=en"
```

## 验证是否生效

设置完成后，执行任意 java 命令（如 java -version），JVM 会自动打印 JDK_JAVA_OPTIONS 中的参数:

```sh
$ java -version
Picked up JDK_JAVA_OPTIONS: -Xms512m -Xmx1024m -XX:+UseG1GC -Duser.language=en"
openjdk version "17.0.9" 2023-10-17
OpenJDK Runtime Environment Temurin-17.0.9+9 (build 17.0.9+9)
OpenJDK 64-Bit Server VM Temurin-17.0.9+9 (build 17.0.9+9, mixed mode, sharing)
```

若看到 `Picked up JDK_JAVA_OPTIONS:` 一行，说明参数已成功加载。
