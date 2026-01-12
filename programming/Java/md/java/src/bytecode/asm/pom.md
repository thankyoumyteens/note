# 引入 ASM 依赖

一般来说：

- asm 核心库
- asm-commons 在 asm 核心的基础上，提供大量“常用模式的封装类”，让你写增强逻辑更舒服
- asm-util 更偏“工具 & 调试”的包，帮你打印、检查、验证字节码

```xml
<!-- Source: https://mvnrepository.com/artifact/org.ow2.asm/asm -->
<dependency>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm</artifactId>
    <version>9.9.1</version>
</dependency>
<!-- Source: https://mvnrepository.com/artifact/org.ow2.asm/asm-commons -->
<dependency>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm-commons</artifactId>
    <version>9.9.1</version>
</dependency>
<!-- Source: https://mvnrepository.com/artifact/org.ow2.asm/asm-util -->
<dependency>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm-util</artifactId>
    <version>9.9.1</version>
    <scope>test</scope> <!-- 常常只在开发/测试时用 -->
</dependency>
```
