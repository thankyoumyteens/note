# 文件操作

## 一次性读写

```java
Path path = Paths.get("/home/demo/1.txt");

// 以字节方式读取文件全部内容
byte[] bytes = Files.readAllBytes(file);
// 以字节方式一次性写入文件
Path file2 = file.resolveSibling("2.txt");
Files.write(file2, bytes);

// 以字符方式读取文件全部内容
List<String> lines = Files.readAllLines(file);
// 以字符方式一次性写入文件
Path file3 = file.resolveSibling("3.txt");
Files.write(file3, lines);
```
