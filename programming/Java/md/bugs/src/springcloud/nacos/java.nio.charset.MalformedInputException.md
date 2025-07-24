# Input length = 1

windows 中 java -jar 启动时

```sh
java -jar demo.jar
```

报错 java.nio.charset.MalformedInputException: Input length = 1

## 原因

windows 命令行默认 GBK 编码, 而 nacos 上的 yml 文件时 utf-8 编码, 所以导致中文无法解析。

## 解决

```sh
java -Dfile.encoding=utf-8 -jar demo.jar
```
