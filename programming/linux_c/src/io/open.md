# 打开文件

在对文件进行读写操作前，需要先打开该文件。内核为每个进程维护一个打开文件的列表，该表被称为文件表(file table)。该表由一些叫做文件描述符 (file descriptors)的非负整数进行索引。列表中的每项均包含一个打开文件的信息。打开一个文件返回一个文件描述符(fd)，而接下来的操作(读写等等)则把文件描述符作为基本参数。

文件描述符由 C 语言的 int 类型表示。每个 Linux 进程有一个打开文件数的上限。文件描述符从 0 开始，直到比上限小 1。默认的上限是 1024。负数不是合法的文件描述符，所以 -1 常常被用来表示一个函数不能返回合法文件描述符的错误。

每个进程按照惯例会至少有三个打开的文件描述符：0, 1 和 2，除非进程显式的关闭它们。文件描述符 0 是标准输入(stdin)，文件描述符 1 是标准输出(stdout)，而文件描述符 2 是标准错误(stderr)。C 标准库提供了预处理器宏：`STDIN_FILENO`， `STDOUT_FILENO` 和 `STDERR_FILENO`，以取代对以上整数的直接引用。

需要注意的是，文件描述符不仅仅用于普通文件的访问，也用于访问设备文件、管道、目录以及快速用户空间锁、FIFOs 和套接字。遵循一切皆文件的理念，任何你能读写的东西都可以用文件描述符来访问。

在一个文件能被访问之前，必须通过 `open()` 或者 `creat()` 系统调用打开它。一旦使用完毕，就应该用 `close()` 系统调用来关闭文件。

## open()

函数定义如下:

```c
#include <fcntl.h>

int open (const char *name, int flags);

int open (const char *name, int flags, mode t mode);
```

通过 `open()` 系统调用来打开一个文件并获得一个文件描述符:

```c
#include <stdio.h>
#include <fcntl.h>

void open_demo() {
    int fd;
    fd = open("/root/cpp_demo/demo.cpp", O_RDWR | O_APPEND);
    if (fd == -1) {
        printf("error\n");
        return;
    }
    printf("fd: %d\n", fd);
}
```

## open() 的 flags 参数

flags 参数必须是以下之一：

- O_RDONLY: 只读
- O_WRONLY: 只写
- O_RDWR: 读写

flags 参数可以和一个或多个其它值进行按位或运算，用以修改打开文件请求的行为, 常用的如下:

- O_APPEND: 文件将以追加模式下打开。就是说，在每次写操作之前，文件位置指针将被置于文件末尾
- O_CREAT: 当 name 指定的文件不存在时，将由内核来创建。如果文件已存在，本标志无效
- O_DIRECTORY: 如果 name 不是一个目录，open()调用将会失败
- O_EXCL: 和 O_CREAT 一起给出的时候，如果由 name 给定的文件已经存在，则 open()调用失败。用来防止文件创建时出现竞争
- O_TRUNC: 如果文件存在，且为普通文件，并允许写，将文件的长度截断为 0

## open() 的 mode 参数

当使用 O_CREAT 时, 必须设置 mode 参数。当文件创建时，mode 参数提供新建文件的权限。
