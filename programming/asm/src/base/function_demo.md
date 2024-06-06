# 函数示例

实现的功能: 计算 2^3 + 5^2 = ?。

创建 `power.s` 文件:

```x86asm
.code32
.section .data

.section .text
    .globl _start
    _start:
        # 计算2^3
        # 参数逆序入栈
        pushl $3
        pushl $2
        # 调用函数
        call power
        # 函数调用完成, 从栈中移除两个参数
        addl $8, %esp
        # 保存2^3的计算结果
        pushl %eax

        # 同理, 计算5^2
        pushl $2
        pushl $5
        call power
        addl $8, %esp
        # 把2^3的计算取出到ebx中
        popl %ebx
        # 5^2的计算结果在eax中
        # 两个结果相加
        addl %eax, %ebx
        # 执行系统调用exit
        movl $1, %eax
        int $0x80

    # power函数
    .type power, @function
    power:
        # 保存_start的基址指针ebp
        pushl %ebp
        # 设置ebp为power函数的栈底,
        # 用来定位参数和局部变量
        movl %esp, %ebp

        # 为局部变量分配栈空间
        subl $4, %esp

        ####################################
        # 此时的栈空间:
        #
        # 指数 <--- 12(ebp)
        # 底数 <--- 8(ebp)
        # 返回地址 <--- 4(%ebp)
        # _start的ebp <--- (%ebp)
        # 局部变量 <--- -4(%ebp)和(%esp)
        ####################################

        # 取出参数1
        movl 8(%ebp), %ebx
        # 取出参数2
        movl 12(%ebp), %ecx

        # 先把底数存储到局部变量
        movl %ebx, -4(%ebp)
        # 循环相乘,
        # 指数从n次方减到1次方时跳出循环
        power_loop_start:
            cmpl $1, %ecx
            je end_power
            # 取出底数
            # 因为计算操作只能使用寄存器
            movl -4(%ebp), %eax
            # 相乘
            imull %ebx, %eax
            # 把结果存回局部变量
            movl %eax, -4(%ebp)

            # 指数递减
            decl %ecx
            # 下一轮循环
            jmp power_loop_start

        end_power:
            # 返回值放入eax
            movl -4(%ebp), %eax
            # 移除当前函数的栈帧
            movl %ebp, %esp
            # 恢复调用方_start的基址指针ebp
            popl %ebp
            # 返回
            ret
```

## 执行

```sh
# 汇编
as --32 power.s -o power.o
# 链接
ld -melf_i386 power.o -o power
# 运行
./power
# 验证
echo $?
```
