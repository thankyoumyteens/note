# 系统调用示例

实现的功能: 通过系统调用 `exit` 退出程序, 并向 linux 返回一个状态码。在运行程序后可通过输入`echo $?`来读取状态码。

创建 `exit.s` 文件:

```x86asm
.code32
.section .data

.section .text

    .globl _start

    _start:
        # exit系统调用号是1
        # 该指令将数字1移入eax寄存器
        # movl指令有两个操作数: 源操作数和目的操作数
        # 数字1前面的$表示要使用立即数
        # 如果没有$符号, 指令将会进行直接寻址, 加载地址1中的内容
        movl $1, %eax
        # 返回给操作系统的状态码
        movl $123, %ebx
        # 执行系统调用 int代表中断, 0x80是要用到的中断号
        int $0x80
```

## 执行

```sh
# 汇编
as --32 -o exit.o exit.s
# 链接
ld -m elf_i386 -o exit exit.o
# 运行
./exit
# 验证
echo $?
```
