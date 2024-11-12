# 基本使用

### 1. 下载

[graalvm](https://www.graalvm.org/downloads/)

### 2. 解压

### 3. 安装 xcode

```sh
xcode-select --install
```

### 4. 创建 HelloWorld.java

```java
public class HelloWorld {
  public static void main(String[] args) {
    System.out.println("Hello, World!");
  }
}
```

### 5. 编译

```sh
graalvm-jdk-21.0.5+9.1/Contents/Home/bin/javac HelloWorld.java
```

### 6. 生成可执行文件

```sh
graalvm-jdk-21.0.5+9.1/Contents/Home/bin/native-image HelloWorld
```

### 7. 运行

```sh
./helloworld
```
