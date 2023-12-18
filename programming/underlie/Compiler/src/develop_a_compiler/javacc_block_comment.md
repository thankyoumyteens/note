# 扫描多行注释

由于 JavaCC 会匹配尽可能长的字符串, 因此下面的写法会有问题。

```java
// 错误写法
SKIP { <"/*" (~[])* "*/"> }
```

JavaCC 会从第一个`/*`开始, 匹配到最后一个`*/`。

```cpp
/* 本应只有这一行是注释 */
int main() {
    printf("Hello, World!\n");
    return 0;
    /* 实际上会匹配到这里 */
}
```

解决方法:

```java
SKIP: { <"/*"> : IN_BLOCK_COMMENT }
<IN_BLOCK_COMMENT> SKIP: { <~[]> }
<IN_BLOCK_COMMENT> SKIP: { <"*/"> : DEFAULT }
```

IN_BLOCK_COMMENT 是自定义的扫描状态, 写法: `{ <"/*"> : IN_BLOCK_COMMENT }`, 表示匹配到 `/*` 后, 迁移到名为 IN_BLOCK_COMMENT 的状态。

扫描器在迁移到某个状态后只会运行该状态专用的词法分析规则, 要定义某状态下专用的规则, 可以在 TOKEN 等命令前加上 `<状态名>`, 比如: `<IN_BLOCK_COMMENT> SKIP`。

最后, `{ <"*/"> : DEFAULT }` 表示匹配到 `*/` 后, 迁移到 DEFAULT 状态, DEFAULT 状态是默认的状态。

这样在扫描到第一个`*/`时, 就会切换状态, 不会继续匹配后面的内容。

这样还有一个问题: 多行注释没有结束的话, 不会报错:

```cpp
int main() {
    printf("Hello, World!\n");
    return 0;
}
/* 文件末尾, 注释没有结束
```

未提示错误的原因在于使用了 3 个 SKIP 命令的规则进行扫描。像这样分成 3 个规则来使用 SKIP 命令的话，3 个规则就会分别被视为对各自的 token 的描述，因此匹配到任何一个规则都会认为扫描正常结束。

要解决这个问题可以使用 MORE 命令, 通过使用 MORE 命令，可以将一个 token 分割为由多个词法分析的规则来描述:

```java
// MORE命令把3条规则合并成一条规则
MORE: { <"/*"> : IN_BLOCK_COMMENT }
<IN_BLOCK_COMMENT> MORE: { <~[]> }
<IN_BLOCK_COMMENT> SKIP: { <BLOCK_COMMENT: "*/"> : DEFAULT }
```
