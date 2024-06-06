# 文件读写示例

实现的功能: 将文件中的所有字母转换为大写。

```x86asm
.code32
.section .data
    # 定义常量(.equ 类似于 #define)

    # 系统调用号
    .equ SYS_OPEN, 5
    .equ SYS_WRITE, 4
    .equ SYS_READ, 3
    .equ SYS_CLOSE, 6
    .equ SYS_EXIT, 1

    # 文件读写模式
    .equ O_RDONLY, 0
    .equ O_CREAT_WRONLY_TRUNC, 03101

    # 基本的文件描述符
    .equ STDIN, 0
    .equ STDOUT, 1
    .equ STDERR, 2

    # 系统调用中断
    .equ LINUX_SYSCALL, 0x80

    # read系统调用在读取到文件末尾时会返回0
    .equ END_OF_FILE, 0

    .equ NUMBER_ARGUMENTS, 2

.section .bss
    # 缓冲区大小
    .equ BUFFER_SIZE, 500
    # 定义缓冲区
    .lcomm BUFFER_DATA, BUFFER_SIZE

.section .text
    # 变量在栈中的位置
    .equ ST_SIZE_RESERVE, 8
    .equ ST_FD_IN, -4
    .equ ST_FD_OUT, -8
    .equ ST_ARGC, 0       # 命令行参数个数
    .equ ST_ARGV_0, 4     # 命令行参数0: 程序名
    .equ ST_ARGV_1, 8     # 命令行参数1: 输入文件名
    .equ ST_ARGV_2, 12    # 命令行参数2: 输出文件名

    .globl _start
    _start:
        # 保存调用方的基址指针ebp
        movl %esp, %ebp
        # 分配空间保存文件描述符(读+写)
        subl $ST_SIZE_RESERVE, %esp

        # 打开输入文件
        movl $SYS_OPEN, %eax    # 系统调用open
        movl ST_ARGV_1(%ebp), %ebx    # open的参数
        movl $O_RDONLY, %ecx          # 只读模式
        movl $0666, %edx              # 文件模式(不知道干什么的)
        int $LINUX_SYSCALL            # 调用open

        # 保存读取的文件描述符
        movl %eax, ST_FD_IN(%ebp)

        # 打开输出文件
        movl $SYS_OPEN, %eax
        movl ST_ARGV_2(%ebp), %ebx
        movl $O_CREAT_WRONLY_TRUNC, %ecx    # 文件不存在则创建, 存在则覆盖
        movl $0666, %edx
        int $LINUX_SYSCALL

        # 保存写入的文件描述符
        movl %eax, ST_FD_OUT(%ebp)

        # 开始读文件
```
