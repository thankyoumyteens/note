# 匹配

```java
boolean isMatch = Pattern.matches("[a-z]+\\d{3}.*", "hello123world");
```

# 查找

```java
Pattern pattern = Pattern.compile("([a-z])([0-9])");
Matcher matcher = pattern.matcher("abcde12345");
// 需要先find, 然后group才能有数据
while(matcher.find()) {
    int count = matcher.groupCount();
    for (int i = 0; i <= count; i++) {
        String ret = matcher.group(i);
        System.out.println(ret);
    }
}
```

# 替换

```java
String input = "神探狄仁&*%$杰之四大天王@bdfbdbdfdgds23532";
// 汉字的Unicode编码范围是: \u4e00-\u9fa5
input = input.replaceAll("[^\\u4e00-\\u9fa5]", "");
System.out.println(input);   // 神探狄仁杰之四大天王
```

# 分组替换

replaceAll 是一个替换字符串的方法, 正则表达式中括号表示一个分组, replaceAll 的参数 2 中可以使用$n(n 为数字)来依次引用子表达式中匹配到的分组字串

```java
String tel = "18304072984";
// 括号表示组, 被替换的部分$n表示第n组的内容
tel = tel.replaceAll("(\\d{3})\\d{4}(\\d{4})", "$1****$2");
System.out.print(tel);   // output: 183****2984
```
