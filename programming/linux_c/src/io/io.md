# 文件 I/O

所有执行 I/O 操作的系统调用都以文件描述符, 一个非负整数(通常是小整数), 来指代打开的文件。文件描述符用以表示所有类型的已打开文件, 包括管道 (pipe)、FIFO、socket、终端、 设备和普通文件。每个进程的文件描述符互不影响。

每个进程按照惯例会至少有三个打开的文件描述符: 0, 1 和 2。文件描述符 0 是标准输入(stdin), 文件描述符 1 是标准输出(stdout), 而文件描述符 2 是标准错误(stderr)。`<unistd.h>` 提供了预处理器宏: `STDIN_FILENO`,  `STDOUT_FILENO` 和 `STDERR_FILENO`, 以取代对以上整数的直接引用。

文件 I/O 操作的 4 个主要系统调用:

- `fd = open(pathname, flags, mode)` 函数打开 pathname 所标识的文件, 并返回文件描述符, 用以在后续函数调用中指代打开的文件。flags 参数指定文件的打开方式: 只读、只写亦或是读写方式等。mode 参数则指定了由 `open()` 调用创建文件的访问权限, 如果 open()函数并未创建文件, 那么可以省略 mode 参数
- `numread = read(fd, buffer, count)` 调用从 fd 所指代的打开文件中读取至多 count 字节的数据, 并存储到 buffer 中。`read()` 调用的返回值为实际读取到的字节数。如果再无字节可读, 则返回值为 0
- `numwritten = write(fd, buffer, count)` 调用从 buffer 中读取多达 count 字节的数据写入由 fd 所指代的已打开文件中。`write()` 调用的返回值为实际写入文件中的字节数, 有可能小于 count
- `status = close(fd)` 在所有输入/输出操作完成后, 调用 `close()` 释放文件描述符 fd 以及与之相关的内核资源

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

#ifndef BUF_SIZE
#define BUF_SIZE 1024
#endif

void io_demo() {
    char buf[BUF_SIZE];

    // 打开文件
    int inputFd = open("/demo/a.txt", O_RDONLY);
    if (inputFd == -1) {
        perror("input error");
        return;
    }
    int openFlags = O_CREAT | O_WRONLY | O_TRUNC;
    // 文件访问权限: rw-rw-rw-
    mode_t filePerms = S_IRUSR | S_IWUSR |
                       S_IRGRP | S_IWGRP |
                       S_IROTH | S_IWOTH;
    int outputFd = open("/demo/b.txt", openFlags, filePerms);
    if (outputFd == -1) {
        perror("output error");
        return;
    }

    // 读写文件
    ssize_t numRead;
    while ((numRead = read(inputFd, buf, BUF_SIZE)) > 0) {
        if (write(outputFd, buf, numRead) != numRead) {
            printf("couldn't write whole buffer\n");
            return;
        }
    }
    if (numRead == -1) {
        perror("read error");
        return;
    }

    // 关闭文件
    if (close(inputFd) == -1) {
        perror("close input error");
        return;
    }
    if (close(outputFd) == -1) {
        perror("close output error");
        return;
    }

}
```
