# 错误处理

系统调用失败时, 会将全局整形变量 `errno` 设置为一个正值, 以标识具体的错误。程序应包含 `<errno.h>` 头文件, 该文件提供了对 `errno` 的声明, 以及一组针对各种错误编号而定义的常量。所有这些符号名都以字母 E 打头。

```c
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>

void errno_demo() {
    int fd;
    fd = open("demo.cpp", O_RDONLY);
    if (fd == -1 && errno == ENOENT) {
        printf("error: No such file or directory\n");
    }
}
```

函数 `perror()` 会打印出一条与当前 `errno` 值相对应的消息:

```c
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>

void errno_demo() {
    int fd;
    fd = open("demo.cpp", O_RDONLY);
    if (fd == -1 && errno == ENOENT) {
        // 输出 error: No such file or directory
        perror("error");
    }
}
```

函数 `strerror()` 会返回 `errno` 对应的错误字符串:

```c
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>

void errno_demo() {
    int fd;
    fd = open("demo.cpp", O_RDONLY);
    if (fd == -1 && errno == ENOENT) {
        // 输出 error: No such file or directory
        printf("error: %s\n", strerror(errno));
    }
}
```
