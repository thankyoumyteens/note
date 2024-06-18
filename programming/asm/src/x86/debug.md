# 调试示例

以 `maximum.s` 为例。

```x86asm
.section .data
    data_items:
        .long 3,1,2,4,7,6,5,10,9,0

.section .text

    .globl _start

    _start:
        movl $0, %edi
        movl data_items(, %edi, 4), %eax
        movl %eax, %ebx
        start_loop:
            cmpl $0, %eax
            je loop_exit

            # 把这行注释,
            # 让程序进入无限循环
            # incl %edi

            movl data_items(, %edi, 4), %eax
            cmpl %ebx, %eax
            jle start_loop
            movl %eax, %ebx

            jmp start_loop

        loop_exit:
            movl $1, %eax
            int $0x80
```

首先要让编译器在可执行文件中包含调试信息, 只要在 as 命令中加入 `--gstabs` 选项就能做到这点。汇编命令改为:

```sh
as --32 --gstabs -o maximum.o maximum.s
```

链接命令不变:

```sh
ld -m elf_i386 -o maximum maximum.o
```

## 运行调试器

运行调试器(保证源代码也在当前目录下):

```sh
gdb ./maximum
```

输出内容如下:

```
GNU gdb (Ubuntu 7.11.1-0ubuntu1~16.5) 7.11.1
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./maximum...done.
(gdb)
```

根据 GDB 版本的不同, 输出会略有不同。现在已经加载了程序, 但程序还未运行。调试器正在等待你的命令。

要运行程序, 输入 `run` 即可, 此时程序将不会返回, 因为它陷入了无限循环。

为了中断程序, 请按下 `CTRL + C`。程序会给出如下信息: 

```
(gdb) run
Starting program: /root/asm_practice/maximum
^C
Program received signal SIGINT, Interrupt.
start_loop () at maximum.s:22
22                  cmpl %ebx, %eax
(gdb)
```

上述信息告诉你程序被 `SIGINT` 信号中断(来自 `CTRL + C`), 而且中断时位于 `start_ loop` 中, 正在执行第 22 行。

根据你按下 `CTRL + C` 时刻的不同, 程序会停在与示例不同的行或指令上。

## 单步调试

不断输入 `stepi` 命令执行单步调试:

```
^C
Program received signal SIGINT, Interrupt.
start_loop () at maximum.s:22
22                  cmpl %ebx, %eax
(gdb) stepi
23                  jle start_loop
(gdb) stepi
14                  cmpl $0, %eax
(gdb) stepi
15                  je loop_exit
(gdb) stepi
21                  movl data_items(, %edi, 4), %eax
(gdb) stepi
22                  cmpl %ebx, %eax
(gdb) stepi
23                  jle start_loop
(gdb) stepi
14                  cmpl $0, %eax
(gdb)
```

## 查看寄存器的值

使用命令 `info register`, 这条命令将以十六进制显示所有寄存器的值:

```
(gdb) info register
rax            0x3      3
rbx            0x3      3
rcx            0x0      0
rdx            0x0      0
rsi            0x0      0
rdi            0x0      0
rbp            0x0      0x0
rsp            0x7fffffffe440   0x7fffffffe440
r8             0x0      0
r9             0x0      0
r10            0x0      0
r11            0x0      0
r12            0x0      0
r13            0x0      0
r14            0x0      0
r15            0x0      0
rip            0x4000bf 0x4000bf <start_loop>
eflags         0x246    [ PF ZF IF ]
cs             0x33     51
ss             0x2b     43
ds             0x0      0
es             0x0      0
fs             0x0      0
gs             0x0      0
k0             0x0      0
k1             0x0      0
k2             0x0      0
---Type <return> to continue, or q <return> to quit---q
Quit
(gdb)
```

如果只想显示 `%eax` 的内容, 可以执行 `print/ $eax` 来打印十六进制值, 也可以执行 `print/d $eax` 打印十进制值。注意, 在 GDB 中, 寄存器以 `$` 而不是 `%` 作为前缀:

```
(gdb) print/ $eax
$1 = 3
(gdb)
```

`%eax` 的内容是 3, 3 是要搜索的数字列表的第一个数字。如果单步执行循环几次, 就会发现在每次循环中的 `%eax` 内容都是 3。这是不应当发生的, 因为每次循环, `%eax` 的内容都应该是列表中的下一个值。

现在看一下 给 `%eax` 赋值的地方:

```x86asm
movl data_items(, %edi, 4), %eax
```

通过 `stepi` 命令 让程序执行到这行代码, 此时查看 `%edi` 的值:

```
(gdb) stepi
21                  movl data_items(, %edi, 4), %eax
(gdb) print/d $edi
$5 = 0
```

这表明 `%edi` 被设置为 0, 这就是一直加载数组第一个元素的原因。
