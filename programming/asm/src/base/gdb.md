# GDB 常用命令

## 在可执行文件中包含调试信息

```sh
as --gstabs maximum.s -o maximum.o
ld maximum.o -o maximum
```

## 运行调试器

保证源代码也在当前目录下:

```sh
gdb 程序名
```

## 运行程序

要运行程序，输入 `run` 即可。

## 设置断点

设置断点必须在运行程序之前进行。执行 `run` 命令之前，可以使用 `break` 命令设置断点。

例如，要在第 10 行设置断点，可以执行命令 `break 10`。

然后，程序到达第 10 行时就会停止运行，并打印出当前行和指令。

接着，就可以从该断点开始单步运行程序，并检查寄存器和内存的内容。

```
(gdb) break 10
Breakpoint 1 at 0x4000b0: file maximum.s, line 10.
(gdb) run
Starting program: /root/asm_practice/maximum

Breakpoint 1, _start () at maximum.s:10
10              movl $0, %edi
(gdb)
```

当处理函数时，也可以在函数名上设置断点: `break 函数名`。这会使调试器在函数调用和函数设置后立即中断(会跳过 `%esp`入栈和·%esp· 复制)。

## 单步调试

- `stepi`: 执行每一行代码, 相当于 IDE 中的 `Step Into`
- `nexti`: 跳过整个函数, 相当于 IDE 中的 `Step Over`

## 查看寄存器的值

- `info register`: 以十六进制显示所有寄存器的值
- `print/ $eax`: 以十六进制显示 `%eax` 寄存器的值
- `print/d $eax`: 以十进制显示 `%eax` 寄存器的值
