# jinfo

jinfo(Configuration Info for Java)的作用是实时查看和调整虚拟机各项参数。使用jps命令的-v参数可以查看虚拟机启动时显式指定的参数列表, 但如果想知道未被显式指定的参数的系统默认值, 就只能使用jinfo的-flag选项进行查询了(JDK 6或以上版本可以使用javaXX:+PrintFlagsFinal查看参数默认值)。jinfo还可以使用-sysprops选项把虚拟机进程的System.getProperties()的内容打印出来。可以使用-flag\[+|-\]name或者-flag name=value在运行期修改一部分运行期可写的
虚拟机参数值。

jinfo命令格式: 

```
jinfo [ option ] pid
```

## jinfo执行样例

查询CMSInitiatingOccupancyFraction参数值

```
jinfo -flag CMSInitiatingOccupancyFraction 1444
-XX:CMSInitiatingOccupancyFraction=85
```
