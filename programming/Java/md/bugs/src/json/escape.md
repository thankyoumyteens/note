# illegal identifier

```sh
com.alibaba.fastjson.JSONException: illegal identifier : \pos 1, line 1, column 2
```

json 字符串为:

```json
[{\"data\":\"{\\\"message\\\":\\\"aaaaaa\\\",\\\"data\\\":\\\"aaaaa,\\\",\\\"success\\\":\\\"false\\\",\\\"code\\\":400}\",\"code2\":\"123\"},{\"data\":\"{\\\"message\\\":\\\"执行成功\\\",\\\"data\\\":\\\"{\\\\\\\"code\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"data\\\\\\\":{\\\\\\\"name\\\\\\\":\\\\\\\"啊啊啊\\\\\\\",\\\\\\\"id\\\\\\\":\\\\\\\"123321\\\\\\\"},\\\\\\\"message\\\\\\\":\\\\\\\"成功\\\\\\\"}\\\",\\\"success\\\":\\\"true\\\",\\\"code\\\":\\\"200\\\"}\",\"code2\":\"123123\"}]
```

报错原因是，在 json 反序列化时存在转义字符。

解决方案: 在处理字符串之前，先将字符串去除转义 `StringEscapeUtils.unescapeJava(jsonStr)`

StringEscapeUtils 的依赖:

```xml
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-text</artifactId>
    <version>1.12.0</version>
</dependency>
```
