# 动态链接库的工作过程

hello 程序开始时，首先加载文件 `/lib/ld-linux.so.2`, 这是动态链接器，它会查看 hello 程序，并发现该程序需要 c 库才能运行。因此，链接器在标准目录(即 `/etc/1d.so.conf` 下以及环境变量 `LD_LIBRARY_PATH` 中的所有目录下)查找名为 `1ibc.so` 的库，然后在库中查找所需的符号(printf 和 exit)，并加载库到程序的虚拟内存。

最后，链接器以库中的 `printf` 的实际位置代替 hello 程序中的所有 `printf`。

查看程序依赖哪些库:

```sh
ldd ./hello
# 输出
# linux-gate.so.1 =>  (0xf77a5000)
# libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf75de000)
# /lib/ld-linux.so.2 (0xf77a6000)
```
