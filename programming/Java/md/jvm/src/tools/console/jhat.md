# jhat

jhat(JVM Heap Analysis Tool)命令与jmap搭配使用, 来分析jmap生成的堆转储快照。

jhat内置了一个微型的HTTP/Web服务器, 生成堆转储快照的分析结果后, 可以在浏览器中查看。

## 使用jhat分析dump文件

```
jhat eclipse.bin
Reading from eclipse.bin...
Dump file created Fri Nov 19 22:07:21 CST 2010
Snapshot read, resolving...
Resolving 1225951 objects...
Chasing references, expect 245 dots....
Eliminating duplicate references...
Snapshot resolved.
Started HTTP server on port 7000
Server is ready.
```

屏幕显示"Server is ready."的提示后, 在浏览器中输入 http://localhost:7000/ 可以看到分析结果。

分析结果默认以包为单位进行分组显示, 分析内存泄漏问题主要会使用到其中的Heap Histogram与OQL页签的功能, 前者可以找到内存中总容量最大的对象, 后者是标准的对象查询语言, 使用类似SQL的语法对内存中的对象进行查询统计。
