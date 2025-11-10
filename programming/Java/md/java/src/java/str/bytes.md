# 字符串和字节数组互转

## 字符串 -> 字节数组

```java
import java.nio.charset.StandardCharsets;

String str = "Hello, Java 12! 你好";

byte[] bytes = str.getBytes(StandardCharsets.UTF_8);
```

## 字节数组 -> 字符串

```java
import java.nio.charset.StandardCharsets;

byte[] bytes = {72, 101, 108, 108, 111}; // "Hello"

String str = new String(bytes, StandardCharsets.UTF_8);
```
