# 常量

使用 `.equ` 定义常量, `.equ` 类似于 c 中的 `#define`。

```x86asm
# 定义常量
.equ SYS_OPEN, 5

# 使用常量
movl $SYS_OPEN, %eax
```
