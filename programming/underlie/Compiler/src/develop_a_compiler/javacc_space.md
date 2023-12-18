# 扫描空白字符

空白符和注释在扫描时不需要生成 token, 要跳过 token, 可以使用 SKIP 命令或 SPECIAL_TOKEN 命令。

SKIP 命令和 SPECIAL_TOKEN 命令的区别在于是否保存跳过的 token。使用 SKIP 命令无法访问跳过的字符串，使用 SPECIAL_TOKEN 命令可以在后面获取到跳过的字符串。

```java
// 跳过空白字符
SPECIAL_TOKEN: { <SPACES: ([" ", "\t", "\n", "\r", "\f"])+> }
```
