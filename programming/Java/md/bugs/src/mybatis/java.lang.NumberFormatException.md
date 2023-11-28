# Error querying database. Cause: java.lang.NumberFormatException: For input string

```xml
<if test="param.xxx!= '2'">
```

## 原因

mybatis会把单引号转成char, String和char比较, 会报错。

## 解决

使用toString()。

```xml
<if test="param.xxx!= '2'.toString()">
```

或者内层改为双引号, 外层使用单引号。

```xml
<if test='param.xxx!= "2"'>
```
