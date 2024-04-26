# 守护进程

Gradle 守护进程（Gradle Daemon）是 Gradle 的一个后台进程，它在构建时为 Gradle 提供服务。从 Gradle 2.1 版本开始，守护进程成为了 Gradle 的默认组件。守护进程的主要目的是提高构建性能，通过减少构建启动时间来优化整个构建过程。

查看守护进程运行情况:

```sh
gradle --status
# 输出结果中:
# IDLE 为空闲
# BUSY 为繁忙
# STOPPED 为已关闭
```

关闭守护进程:

```sh
gradle --stop
```

守护进程默认打开，可通过修改项目根目录下的 gradle.properties 文件(没有就新建一个)关闭:

```sh
org.gradle.daemon=false
```
