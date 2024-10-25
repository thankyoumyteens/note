# 基本使用

1. [下载](https://www.graalvm.org/downloads/)
2. 解压
3. 安装 xcode: `xcode-select --install`

## 使用

1. 创建 HelloWorld.java

```java
public class HelloWorld {
  public static void main(String[] args) {
    System.out.println("Hello, World!");
  }
}
```

2. 编译

```sh
graalvm-jdk-21.0.5+9.1/Contents/Home/bin/javac HelloWorld.java
```

3. 生成可执行文件

```sh
graalvm-jdk-21.0.5+9.1/Contents/Home/bin/native-image HelloWorld
```

4. 执行

```sh
./helloworld
```
