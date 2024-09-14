# CPU 占用过高排查

1. 使用 top 命令找到占用 CPU 最高的 Java 进程 pid。如: 占用 CPU 最高的进程 pid 为 13731
2. 用 `ps H -eo pid,tid,%cpu | grep pid` pid 命令查看占用 CPU 最高的线程 id。假如 `ps H -eo pid,tid,%cpu | grep 13731` 看到占用 CPU 最高的那个线程 id 为 13756
3. 然后将线程 id 转换为 16 进制。13756 -> 0x35bc
4. 使用 jstack pid 查看当前 Java 程序的所有线程信息。输出到文件 `jstack 13731 > thread_stack.log`
5. jstack 命令生成的信息包含了 JVM 中所有存活的线程及其所在的 java 文件, 在输出结果中每个线程都有一个 nid(16 进制), 使用之前得到的 16 进制找到对应的 nid 即可(下面有这个线程的类)
