# 打开文件

`open()` 调用既能打开一个已存在的文件, 也能创建并打开一个新文件。

函数定义如下:

```c
#include <fcntl.h>

int open(const char *pathname, int flags, ... /* mode_t mode */);
```

如果调用成功, `open()` 将返回一文件描述符, 用于在后续函数调用中指代该文件。若发生错误,  则返回 -1, 并将 errno 置为相应的错误标志。

要打开的文件由参数 pathname 来标识。如果 pathname 是一个符号链接, 会对其进行解引用。

## open() 的 flags 参数

参数 flags 为位掩码, 用于指定文件的访问模式, flags 参数必须是以下之一: 

- O_RDONLY: 只读
- O_WRONLY: 只写
- O_RDWR: 读写

flags 参数可以和一个或多个其它值进行按位或运算 `|`, 来设置打开文件的行为, 常用的如下:

- O_APPEND: 文件将以追加模式下打开。就是说, 在每次写操作之前, 文件位置指针将被置于文件末尾
- O_CREAT: 当 name 指定的文件不存在时, 将由内核来创建。如果文件已存在, 本标志无效
- O_DIRECTORY: 如果 name 不是一个目录, open()调用将会失败
- O_EXCL: 和 O_CREAT 一起给出的时候, 如果由 name 给定的文件已经存在, 则 open()调用失败。用来防止文件创建时出现竞争
- O_TRUNC: 如果文件存在, 且为普通文件, 并允许写, 将文件的长度截断为 0

## open() 的 mode 参数

当使用 O_CREAT 时, 必须设置 mode 参数。当文件创建时, mode 参数提供新建文件的权限。
