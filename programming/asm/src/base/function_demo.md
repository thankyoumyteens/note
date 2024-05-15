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

        # 由于64位系统只能使用pushq,
        # pushq 会把8个字节入栈,
        # 而实际上只需要两个4字节的栈空间,
        # 所以改成 subq + movl 实现

        # 分配8字节的栈空间
        subq $8, %rsp
        # 指数参数入栈
        movl $3, %eax
        movl %eax, 4(%rsp)
        # 底数参数入栈
        movl $2, %eax
        movl %eax, (%rsp)

        # 调用函数
        call power

        # 函数调用完成,
        # 从栈中移除两个参数
        addq $8, %rsp

        # 函数返回值在eax中
        # 把它保存到ebx
        movl %eax, %ebx
        # 系统调用: exit
        movl $1, %eax
        int $0x80

    # 定义power函数
    .type power, @function
    power:
        # 保存调用方的rbp
        pushq %rbp
        # 设置rbp为power函数的栈底,
        # 用来定位参数和局部变量
        movq %rsp, %rbp

        # 为局部变量分配栈空间
        subq $4, %rsp

        ####################################
        # 此时的栈空间:
        #
        # 底数 <--- 20(ebp)
        # 指数 <--- 16(ebp)
        # 返回地址 <--- 8(%ebp)
        # _start的rbp <--- (%rbp)
        # 局部变量 <--- -4(%rbp)和(%rsp)
        ####################################

        # 把第一个参数放到ebx中
        # (需要跳过栈中调用方的rbp和返回地址两个8字节数据)
        movl 16(%rbp), %ebx
        # 把第二个参数放到ecx中
        movl 20(%rbp), %ecx

        # 先把底数存储到局部变量
        movl %ebx, -4(%rbp)
        # 循环相乘,
        # 指数从n次方减到1次方时跳出
        power_loop_start:
            cmpl $1, %ecx
            je end_power
            # 取出底数
            # 因为计算操作只能使用寄存器
            movl -4(%rbp), %eax
            # 相乘
            imull %ebx, %eax
            # 把结果存回局部变量
            movl %eax, -4(%rbp)

            # 指数递减
            decl %ecx
            # 下一轮循环
            jmp power_loop_start

        end_power:
            # 返回值放入rax
            movl -4(%rbp), %eax
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
./power
echo $?
```
