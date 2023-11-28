# jps

jps(JVM Process Status Tool)可以列出正在运行的虚拟机进程, 并显示虚拟机执行主类(main函数所在的类)名称以及这些进程的本地虚拟机唯一ID(LVMID, Local Virtual Machine Identifier)。其他的JDK工具大多需要输入它查询到的LVMID来确定要监控的是哪一个虚拟机进程。对于本地虚拟机进程来说, LVMID与操作系统的进程ID(PID, Process Identifier)是一致的, 使用Windows的任务管理器或者UNIX的ps命令也可以查询到虚拟机进程的LVMID, 但如果同时启动了多个虚拟机进程, 无法根据进程名称定位时, 那就必须依赖jps命令显示主类的功能才能区分了。

jps命令格式: 

```
jps [ options ] [ hostid ]
```

jps常用选项: 

- -q: 只输出LVMID
- -m: 输出虚拟机主类main函数传入的参数
- -l: 输出主类的全名
- -v: 输出虚拟机进程启动时JVM参数

## jps执行样例

```
jps -l

2388 D:\Develop\glassfish\bin\..\modules\admin-cli.jar
2764 com.sun.enterprise.glassfish.bootstrap.ASMain
3788 sun.tools.jps.Jps
```
