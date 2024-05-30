# 查找最大值

创建 `maximum.s` 文件:

```x86asm
# 目的: 本程序寻找一组数据项中的最大值
#
# 变量: 寄存器有以下用途: 
#
# %edi -保存正在检测的数据项索引
# %ebx -当前已经找到的最大数据项
# %eax -当前数据项
#
# 使用以下内存位置: 
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

## 解释

在这个程序中数据段是有实际内容的:

```x86asm
data_items:
    .long 3,1,2,4,7,6,5,10,9,0
```

`data_items` 是一个指代其后位置的标签。接下来是一条指令, 该指令以 `.1ong` 开始。这会让汇编程序保留 14 个 `.1ong` 型位置, 依次连续排放。由于每个长整型要占用 4 字节, 因此整个列表要占用 40 字节。

`data_items` 是指第一个数字的位置。因为 `data_items` 是标签, 在程序中每当需要引用这个地址时, 就可以使用 `data_items` 符号, 而汇编程序将在汇编时会把它替换成实际的地址。例如, 指令 `movl data_items, %eax` 会将值 3 移入 `%eax`。

`movl $0, %edi`, 由于将 `%edi` 用于存放索引, 要从第一个数据项开始, 所以将 0 加载到 `%edi`。

`movl data_items(, %edi, 4), %eax`, 从 data_items 的起始位置开始, 取第一项的数字(因为 `%edi` 为 0), 每个数据占据 4 个字节, 然后将取出的数字存储到 `%eax`。这就是在汇编语言中使用索引寻址的方式。该指令的通用格式如下: 

```
偏移量(%基址寄存器, %索引寄存器, 比例因子)
```

有些项是可以被省略的, 比例因子默认为 1。最终地址为: 

```
偏移量 + %基址寄存器 + %索引寄存器 x 比例因子
```

当前 `%eax` 中的数字是 3。如果将 `%edi` 设置为 1, `%eax` 为 1, 如果 `%edi` 为 2, `%eax` 的内容为 2, 以此类推。

`movl %eax, %ebx`, 由于这是第一项, 这也就是当前为止的最大数, 将之存储在用于保存当前最大数的 `%ebx` 中。

`start_loop:`, 这个标签标记循环的起始位置。

`cmpl $0, %eax`, 比较数字 0 和存储在 `%eax` 中的数字, 比较的结果会存放到状态寄存器 `%eflags` 中

`je loop_exit` 如果刚才比较的值相等, 则跳转到 `end_1oop` 标签的位置。

如果最后加载的元素不是 0, 将执行下一条指令:

```x86asm
incl %edi
movl data_items(, %edi, 4), %eax
```

`incl` 将` %edi` 的值递增 1。接下来的 `mov1` 与之前的一样, 但是因为已经递增了 `%edi`, `%eax` 会获取列表的下一项值。

```x86asm
cmpl %ebx, %eax
jle start_loop
movl %eax, %ebx
```

将存储在 `%eax` 中的当前值与存放在 `%ebx` 中的当前最大值相比较。如果当前值小于或等于当前最大值, 那么无需处理, 只要跳转到循环起始处就好。否则, 需要记录当前值为最大值。

`jmp start_loop`, 跳转到循环开始, 继续循环。

```x86asm
loop_exit:
    movl $1, %eax
    int $0x80
```

将系统调用号(1 用于 `exit` 调用)存储在 `%eax` 中, 并将其他值存储在其他寄存器中。退出调用需要将退出状态存储在%ebx 中。由于已经将最大值置于 `%ebx` 中, 该寄存器中已经有退出状态了, 因此只要将数字 1 加载到 `%eax` 并调用内核退出即可。
