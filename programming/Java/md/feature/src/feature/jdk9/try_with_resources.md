# try-with-resources 语句增强

try-with-resources 是 Java 7 引入的语法，用于自动关闭实现了 AutoCloseable 接口的资源（如文件流、数据库连接、网络连接等），避免手动调用 close() 方法可能导致的资源泄漏。其核心逻辑是：资源在 try 语句块执行完毕后（无论论正常结束还是异常退出），会自动调用 close() 方法。

在 Java 7/8 中，try-with-resources 要求资源必须在 try 后的括号内显式声明并初始化，否则无法自动管理。例如：

```java
// 资源必须在 try 括号内声明
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    System.out.println(br.readLine());
}
```

若资源已在外部定义（如作为方法参数传入），则无法直接用于 try-with-resources，必须在括号内重新赋值，导致冗余代码：

```java
// Java 8 中处理外部定义的资源（冗余）
public void readFile(BufferedReader br) throws IOException {
    // 必须重新声明变量并赋值，才能使用 try-with-resources
    try (BufferedReader reader = br) {
        System.out.println(reader.readLine());
    }
}
```

## Java 9 的增强：支持外部预定义资源

Java 9 取消了 “资源必须在 try 括号内声明” 的限制，允许直接使用已在外部定义且为 final 或等效 final（ effectively final）的资源变量。

```java
public void copyFile() throws IOException {
    final BufferedReader reader = new BufferedReader(new FileReader("src.txt"));
    final BufferedWriter writer = new BufferedWriter(new FileWriter("dest.txt"));

    // 同时管理多个外部资源
    try (reader; writer) {
        String line;
        while ((line = reader.readLine()) != null) {
            writer.write(line);
        }
    }
}
```

等效 final：指变量声明后未被重新赋值（即使未显式用 final 修饰）。

```java
public void processResource(InputStream is) throws IOException {
    // 外部传入的资源（未被重新赋值，等效 final）
    InputStream input = is;

    // 直接使用
    try (input) {
        input.read();
    }
}
```
