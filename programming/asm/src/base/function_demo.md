# 函数示例

创建 `power.s` 文件:

```x86asm
# 计算2的3次方

# 数据段为空
.section .data

.section .text
    .globl _start
    _start:
        # 参数逆序入栈
        # pushq 会把8个字节入栈
        pushq $3
        pushq $2
        # 调用函数
        call power
        # 函数调用完成,
        # 从栈中移除两个参数
        addq $16, %rsp
        # 函数返回值在rax中
        # 把它保存到rbx
        movq %rax, %rbx
        # 系统调用: exit
        movq $1, %rax
        int $0x80

    # 定义power函数
    .type power, @function
    power:
        # 保存调用方的rbp
        pushq %rbp
        # 设置自己的rbp
        movq %rsp, %rbp
        # 为局部变量分配栈空间
        subq $8, %rsp
        # 把第一个参数放到rbx中
        # (需要跳过栈中调用方的rbp和返回地址两个8字节数据)
        movq 16(%rbp), %rbx
        # 把第二个参数放到rcx中
        movq 24(%rbp), %rcx

        # 先把底数存储到局部变量
        movq %rbx, -8(%rbp)
        # 循环相乘,
        # 指数从n次方减到1次方时跳出
        power_loop_start:
            cmpq $1, %rcx
            je end_power
            # 取出底数
            # 因为计算操作只能使用寄存器
            movq -8(%rbp), %rax
            # 相乘
            imulq %rbx, %rax
            # 把结果存回局部变量
            movq %rax, -8(%rbp)

            # 指数递减
            decq %rcx
            # 下一轮循环
            jmp power_loop_start

        end_power:
            # 返回值放入rax
            movq -8(%rbp), %rax
            # 移除当前函数的栈帧
            movq %rbp, %rsp
            # 恢复调用方的rbp
            popq %rbp
            # 返回
            ret
```

## 运行

```sh
as --gstabs power.s -o power.o
ld power.o -o power
gdb ./power
```
