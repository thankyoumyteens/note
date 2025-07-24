# For input string

```xml
<if test="param.xxx!= '2'">
```

Error querying database. Cause: java.lang.NumberFormatException: For input string

## 原因

mybatis 会把单引号转成 char, String 和 char 比较, 会报错。

## 解决

使用 toString()。

```xml
<if test="param.xxx!= '2'.toString()">
```

或者内层改为双引号, 外层使用单引号。

```xml
<if test='param.xxx!= "2"'>
```
