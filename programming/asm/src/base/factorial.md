# 递归函数

实现的功能: 计算 4 的阶乘(一个数的阶乘 = 这个数 × 这个数减一的阶乘)。

创建 `factorial.s` 文件:

```x86asm
.code32
.section .data

.section .text
    .globl _start
    _start:
        # 把factorial函数的参数入栈
        pushl $4
        # 调用函数计算阶乘
        call factorial
        # 清理入栈的参数
        addl $4, %esp
        # 通过exit返回
        movl %eax, %ebx
        movl $1, %eax
        int $0x80

    # factorial函数
    .type factorial, @function
    factorial:
        pushl %ebp
        movl %esp, %ebp
        # 取出参数
        movl 8(%ebp), %eax
        # 如果参数为1, 直接返回
        cmpl $1, %eax
        je end_factorial

        # 如果参数不是1
        # 递归调用factorial函数
        # 计算 参数 - 1 的阶乘
        decl %eax
        pushl %eax
        call factorial
        # 调用函数后, eax会被覆盖成被调用函数的返回值
        # 需要重新取出参数, 并放到ebx中
        # 每次递归调用函数都会入栈ebp和返回地址
        # 所以偏移量还是8
        movl 8(%ebp), %ebx
        # 一个数的阶乘 = 这个数 * 这个数减1的阶乘
        # 相乘的结果存到eax中
        imull %ebx, %eax

        end_factorial:
            movl %ebp, %esp
            popl %ebp
            ret
```

## 执行

```sh
# 汇编
as --32 -o factorial.o factorial.s
# 链接
ld -m elf_i386 -o factorial factorial.o
# 运行
./factorial
# 验证
echo $?
```
