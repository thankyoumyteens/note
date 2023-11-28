# windows中java -jar启动时, 报错java.nio.charset.MalformedInputException: Input length = 1

```sh
java -jar demo.jar
```

报错java.nio.charset.MalformedInputException: Input length = 1

## 原因

windows命令行默认GBK编码, 而nacos上的yml文件时utf-8编码, 所以导致中文无法解析。

## 解决

```sh
java -Dfile.encoding=utf-8 -jar demo.jar
```
