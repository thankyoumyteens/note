# 汇编程序结构

```x86asm
# 汇编程序示例
.section .data

.section .text

    .globl _start

    _start:
        # 在这里写汇编代码
        movl $1, %eax
        movl $123, %ebx
        int $0x80
```

说明:

- 以 `#` 号开始的内容是注释
- `.section`, 在汇编程序中, 任何以 `.` 开始的指令都不会被直接翻译成机器指令, 这些针对汇编程序本身的指令, 由于是由汇编程序处理, 实际上并不会由计算机运行。`.section` 指令将程序分成几个部分。
  - `.section .data` 命令是数据段的开始, 数据段中要列出程序数据所需的所有内存空间。由于该程序没有使用任何数据, 所以我们不需要这个段
  - `.section .text` 表示文本段开始, 文本段是存放程序指令的部分
- `.globl` 也可以写成 `.global`, 用于声明一个符号为全局的, `.global` 的作用: 
  - 设置符号的可见性, 使得符号在整个程序中都是可见的, 包括其他源文件
  - 在多个源文件组成的程序中, `.global` 允许编译器生成外部符号的引用, 这些符号可以在链接时被其他源文件中的代码访问
  - 通过 `.globl _start` 声明程序入口(类似 C 语言中的 main 函数)
- `_start:`, 定义 `_start` 标签的值。标签为汇编代码中的指令、数据定义或内存位置提供了一个标识符, 使得在代码中引用这些位置变得更加容易和清晰

## 赋值

```x86asm
movl $1, %eax
```

上面的代码可以理解成:

```c
int a = 1;
```

- `movl $1, %eax`: 把数值 1 放入 eax 寄存器

## 条件跳转

```x86asm
cmpl %ebx, %eax
jle target_label
```

上面的代码可以理解成:

```c
int r = eax - ebx;
if (r <= 0) {
  goto target_label;
}
```

- `cmpl` 是一个比较指令, 用于比较两个操作数的大小(右边的减左边的), 并将比较结果设置到状态寄存器中, 特别是标志位(flags)部分。`l` 在 `cmpl` 中代表 long, 意味着它比较的是 32 位的操作数
- `jle` 是一个条件跳转指令, 它会根据标志位的状态来决定是否跳转到指定的标签处执行。即如果前面的比较指令 `cmpl` 的结果表明 `%eax` 寄存器的值小于或等于 `%ebx` 寄存器的值, 那么就执行跳转。类似的指令还有 `je`, `jge` 等
- `target_label` 是跳转的目标标签。如果 `%eax` 小于或等于 `%ebx`, 程序将跳转到 `target_label` 处继续执行

## 无条件跳转

```x86asm
jmp target_label
```

跳转到 `target_label` 标签。

## 循环

循环 10 次:

```x86asm
# i = 0
movl $0, %edi
# 开始循环
start_loop:
    # 判断是否到达末尾 i == 10
    cmpl $10, %edi
    # 跳出循环
    je loop_exit

    # i++
    incl %edi

    # 跳转到循环开始, 执行下一轮循环
    jmp start_loop

loop_exit:
    # 退出
    movl $0, %ebx
    movl $1, %eax
    int $0x80
```

上面的代码可以理解成:

```c
int i = 0;
while(true) {
  if (i == 10) {
    break;
  }
  i = i + 1;
}
```
