# 创建动态链接库

首先进行汇编：

```sh
as write-record.s -o write-record.o
as read-record.s -o read-record.o
```

接下来，将它们链接为一个库，而不是一个程序：

```sh
ld -shared write-record.o read-record.o -o librecord.so
```

这条命令将生成一个名为 `librecord.so` 的库。现在，这个文件可用于多个程序。如果我们需要更新它包含的函数，只需更新这个文件，而不必担心那些使用它的程序。

链接到这个库：

```sh
as write-records.s -o write-records
ld -L.-dynamic-linker /1ib/1d-1inux.so.2 -o write-records -lrecord write-records.o
```

`-lrecord` 告诉链接器在 `librecord.so` 文件中搜索函数。

现在 write-records 程序已经生成了，但却无法运行，会报错找不到 `librecord.so`。

这是因为动态连接器默认情况下只搜索 `/lib`, `/usr/lib` 和在 `/etc/1d.so.conf` 中列出的目录下搜索库。

为了运行此程序，你需要将库移动到其中某个目录下，或执行以下命令：

```sh
LD_LIBRARY_PATH=.
export LD_LIBRARY_PATH
```
