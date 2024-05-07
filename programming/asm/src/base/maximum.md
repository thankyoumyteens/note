# 查找最大值

创建 `maximum.s` 文件:

```
# 目的：本程序寻找一组数据项中的最大值
#
# 变量：寄存器有以下用途：
#
# %edi -保存正在检测的数据项索引
# %ebx -当前已经找到的最大数据项
# %eax -当前数据项
#
# 使用以下内存位置：
#
# data_items - 包含数据项
#              0表示数据结束
#

.section .data
    data_items:
        # 可以看成是long数组(一个.long的长度是4字节)
        # 把0看作是数组结束的标志
        .long 3,1,2,4,7,6,5,10,9,0

.section .text

    .globl _start

    _start:
        # 从0开始遍历
        movl $0, %edi
        # 取出第一项
        movl data_items(, %edi, 4), %eax
        # 由于这是第一项，%eax就是最大值
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

## 汇编

```sh
as maximum.s -o maximum.o
```

## 链接

```sh
ld maximum.o -o maximum
```

## 运行

```sh
./maximum
```

## 验证

```sh
echo $?
```
