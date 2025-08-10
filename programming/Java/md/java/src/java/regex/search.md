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
