# 分组替换

使用 `$n`(n 为数字)来依次引用子表达式中匹配到的分组字串

```java
String tel = "18304072984";
// 括号表示组, 被替换的部分$n表示第n组的内容
tel = tel.replaceAll("(\\d{3})\\d{4}(\\d{4})", "$1****$2");
System.out.print(tel);   // output: 183****2984
```
