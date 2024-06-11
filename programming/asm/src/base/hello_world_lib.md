# 使用动态链接库的 Hello World

创建 `hello.s` 文件:

```x86asm
.code32
.section .data
    firststring:
        .ascii "Hello! %s is a %s who loves the number %d\n\0"
    name:
        .ascii "Jonathan\0"
    personstring:
        .ascii "person\0"
    numberloved:
        .long 3
.section .text
    .globl _start
    _start:
        pushl numberloved    #This is the %d
        pushl $personstring  #This is the second %s
        pushl $name          #This is the first %s
        pushl $firststring   #This is the format string
        call printf

        pushl $0
        call exit
```

## 执行

```sh
# 汇编
as --32 hello.s -o hello.o
# 链接
ld -m elf_i386 -dynamic-linker /lib/ld-linux.so.2 -o hello -lc hello.o
# 运行
./hello
```

选项 `-lc` 表示链接 c 语言库。该库在 GNU/Linux 系统上的文件名为 `libc.so`。

## 链接时报错: ld: cannot find -lc

```sh
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386
sudo apt-get install multiarch-support
sudo apt-get install gcc-multilib g++-multilib
```

重新链接。
