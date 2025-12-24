# 认识 Java 字节码

先随便写一个简单类，比如：

```java
public class Hello {
    public int add(int a, int b) {
        return a + b;
    }
}
```

编译：

```sh
javac Hello.java
```

用 javap 看字节码：

```sh
javap -c Hello
```

你会看到类似：

```
public int add(int a, int b);
  Code:
     0: iload_1
     1: iload_2
     2: iadd
     3: ireturn
```

这几条就是字节码指令：

- iload_1：加载第 1 个整型参数
- iload_2：加载第 2 个整型参数
- iadd：做 int 加法
- ireturn：返回 int 结果

有了这个直观印象，你再去看 ASM，就知道你实际上是在操作这堆字节码指令。
