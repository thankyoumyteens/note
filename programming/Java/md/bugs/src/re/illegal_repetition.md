# Illegal repetition

匹配 json 写成了:

```java
String p = "{\"code\":200,\"msg\":\"(.+?)\"\\}";
```

`{` 是正则表达式中的特殊字符，要匹配 `{`，需要转义后使用:

```java
String p = "\\{\"code\":200,\"msg\":\"(.+?)\"\\}";
```
