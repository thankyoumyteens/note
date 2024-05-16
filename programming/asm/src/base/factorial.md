# 计算阶乘

创建 `factorial.s` 文件:

```x86asm
# 计算阶乘
# 一个数的阶乘 = 这个数 * 这个数减一的阶乘

.section .data

# 没有全局数据

.section .text
    .globl _start

    _start:
        # 把factorial函数的参数入栈
        # 计算7的阶乘
        subq $4, %rsp
        # exit 系统调用传给操作系统的值不能超过256
        # 所以算一个比较小的数的阶乘
        movl $3, (%rsp)

        # 调用函数计算阶乘
        call factorial

        # 清理入栈的参数
        addq $4, %rsp

        # 通过exit返回
        movl %eax, %ebx
        movl $1, %eax
        int $0x80

    # factorial函数
    .type factorial, @function
    factorial:
        pushq %rbp
        movq %rsp, %rbp
        # 取出参数
        movl 16(%rbp), %eax
        # 如果参数为1, 直接返回
        cmpl $1, %eax
        je end_factorial

        # 如果参数不是1
        # 递归调用factorial函数
        # 计算 参数 - 1 的阶乘
        decl %eax
        subq $4, %rsp
        movl %eax, (%rsp)
        call factorial
        # 调用函数后, eax会被覆盖成被调用函数的返回值
        # 需要重新取出参数, 并放到ebx中
        # 每次递归调用函数都会入栈rbp和返回地址
        # 所以偏移量还是16
        movl 16(%rbp), %ebx
        # 一个数的阶乘 = 这个数 * 这个数减一的阶乘
        # 相乘的结果存到eax中
        imull %ebx, %eax

        end_factorial:
            movq %rbp, %rsp
            popq %rbp
            ret
```
