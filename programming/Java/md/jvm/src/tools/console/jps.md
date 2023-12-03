# JPS

JVM Process Status Tool(JPS)可以列出正在运行的 JVM 进程, 并显示虚拟机执行主类(main 函数所在的类)名称以及这些进程的本地虚拟机唯一 ID(LVMID, Local Virtual Machine Identifier)。其他的 JDK 工具大多需要输入这个 LVMID 来定位 JVM 进程。

jps 命令格式:

```
jps [ options ] [ hostid ]
```

jps 常用选项:

- -q: 只输出 LVMID
- -m: 输出虚拟机主类 main 函数传入的参数
- -l: 输出主类的全名
- -v: 输出虚拟机进程启动时 JVM 参数

## 示例

```sh
$ jps -l
27640 jdk.jcmd/sun.tools.jps.Jps
```
