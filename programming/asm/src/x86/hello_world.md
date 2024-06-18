# Hello World

创建 `hello.s` 文件:

```x86asm
.code32
.section .data
    hello_world:
        .ascii "hello world\n"
    .equ hello_world_len, 12
.section .text
    .globl _start
    _start:
        movl $1, %ebx                  # stdout
        movl $hello_world, %ecx
        movl $hello_world_len, %edx
        movl $4, %eax                  # write
        int $0x80

        movl $0, %ebx
        movl $1, %eax
        int $0x80
```

## 执行

```sh
# 汇编
as --32 -o hello.o hello.s
# 链接
ld -m elf_i386 -o hello hello.o
# 运行
./hello
```
