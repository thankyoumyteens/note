# Switch 表达式

switch 表达式在 JDK 12 和 JDK 13 中都是处于预览阶段, 在 JDK 14 中成为正式版本。

## 通过 switch 赋值

原始 switch 写法:

```java
String value;
switch (exp) {
    case "a":
    case "b":
        value = "small";
        break;
    case "c":
        value = "medium";
        break;
    case "d":
    case "e":
        value = "large";
    default:
        value = "";
        break;
}
```

Switch 表达式写法:

```java
String value = switch (exp) {
    case "a", "b" -> "small";
    case "c" -> "medium";
    case "d", "e" -> "large";
    default -> "";
};
```

## 通过 switch 执行代码块

原始 switch 写法:

```java
switch (exp) {
    case "a":
    case "b":
        System.out.println("small");
        break;
    case "c":
        System.out.println("small");
        break;
    case "d":
    case "e":
        System.out.println("small");
    default:
        break;
}
```

Switch 表达式写法:

```java
switch (exp) {
    case "a", "b" -> {
        System.out.println("small");
    }
    case "c" -> {
        System.out.println("small");
    }
    case "d", "e" -> {
        System.out.println("small");
    }
    default -> {
    }
}
```
