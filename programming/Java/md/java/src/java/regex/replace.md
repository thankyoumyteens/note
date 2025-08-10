# 替换

```java
String input = "神探狄仁&*%$杰之四大天王@bdfbdbdfdgds23532";
// 汉字的Unicode编码范围是: \u4e00-\u9fa5
input = input.replaceAll("[^\\u4e00-\\u9fa5]", "");
System.out.println(input);   // 神探狄仁杰之四大天王
```
