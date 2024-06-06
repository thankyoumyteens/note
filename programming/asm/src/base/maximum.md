# 数据类型示例

实现的功能: 查找最大值, 通过系统调用 `exit` 返回结果。

用到的寄存器:

- `%edi` 保存正在检测的数据项索引
- `%ebx` 当前已经找到的最大数据项
- `%eax` 当前数据项

数据段:

- `data_items` 数组数据, 0 表示数据结束

创建 `maximum.s` 文件:

```x86asm
.section .data

    # 定义变量
    data_items:
        # 可以看成是long数组
        # 一个.long的长度是4字节, 因此整个列表占用40字节
        # 把0看作是数组结束的标志
        .long 3,1,2,4,7,6,5,10,9,0

.section .text

    .globl _start

    _start:
        # 从0开始遍历
        movl $0, %edi
        # 取出第一项
        # 因为data_items是标签, 在程序中每当需要引用这个地址时,
        # 就可以使用data_items符号, 汇编程序将在汇编时会把它替换成实际的地址
        # 这条将3移入eax
        movl data_items(, %edi, 4), %eax
        # 由于这是第一项, %eax就是最大值
        movl %eax, %ebx
        # 开始循环
        start_loop:
            # 判断是否到达末尾(0)
            cmpl $0, %eax
            # 跳出循环
            je loop_exit

            # 遍历下一项
            incl %edi
            # 取出第i项
            movl data_items(, %edi, 4), %eax
            # 比较
            cmpl %ebx, %eax
            # 如果小于最大值, 跳转到循环开始, 执行下一轮循环
            jle start_loop
            # 如果大于最大值, 更新ebx中的最大值
            movl %eax, %ebx

            # 跳转到循环开始, 执行下一轮循环
            jmp start_loop

        loop_exit:
            # 把最大值作为程序退出代码
            movl $1, %eax
            int $0x80
```

## 执行

```sh
# 汇编
as --32 maximum.s -o maximum.o
# 链接
ld -melf_i386 maximum.o -o maximum
# 运行
./exit
# 验证
echo $?
```
