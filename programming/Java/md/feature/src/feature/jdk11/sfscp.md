# 直接启动单文件 Java 源代码程序

Java 11 引入了一项便捷特性：直接启动单文件 Java 源代码程序（Single-File Source-Code Programs），无需手动编译（javac），可直接通过 java 命令运行 .java 源文件，极大简化了小型程序、脚本或工具类的开发与执行流程。

```sh
java Hello.java
```

## 适用场景

- 单文件程序：源代码仅包含一个 .java 文件（可包含多个类，但最多一个公共类，且公共类名需与文件名一致）
- 小型工具 / 脚本：如简单的命令行工具、测试代码、一次性脚本等
- 快速原型开发：无需配置构建工具（如 Maven/Gradle），快速验证代码逻辑

## 包含多个类的单文件

创建 MultiClass.java:

```java
public class MultiClass {
    public static void main(String[] args) {
        Helper helper = new Helper();
        System.out.println(helper.getMessage());
    }
}

// 非公共类（可在同一文件中）
class Helper {
    String getMessage() {
        return "Hello from Helper";
    }
}
```

运行:

```sh
java MultiClass.java
# 输出：Hello from Helper
```

## 依赖第三方库（需指定类路径）

```java
import org.apache.commons.lang3.StringUtils;

public class StringUtilsDemo {
    public static void main(String[] args) {
        System.out.println(StringUtils.capitalize("hello")); // 输出：Hello
    }
}
```

若程序依赖外部 JAR（如 commons-lang3.jar），需通过 -cp 指定类路径：

```sh
java -cp "commons-lang3.jar:." StringUtilsDemo.java
# 输出：Hello
```
