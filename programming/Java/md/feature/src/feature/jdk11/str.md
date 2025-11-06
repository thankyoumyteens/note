# String 增强

Java 11 对 String 类进行了几项实用增强，新增了多个便捷方法，简化了字符串处理中常见的操作（如去除空白、判断空白、重复字符串等），提升了代码的简洁性和可读性。

## 去除首尾空白

```java
String str = "  \u2002hello\u2003  "; // \u2002 是 Unicode 中的窄空格，\u2003 是宽空格

// trim() 只能去除 ASCII 空白（如空格、\t、\n），无法处理 Unicode 空白
System.out.println("trim: [" + str.trim() + "]"); // 输出：[ hello   ]（结尾宽空格未去除）

// strip() 支持 Unicode 空白
System.out.println("strip: [" + str.strip() + "]"); // 输出：[hello]（首尾所有空白均去除）

// 仅去除开头空白
System.out.println("stripLeading: [" + str.stripLeading() + "]"); // 输出：[hello   ]

// 仅去除结尾空白
System.out.println("stripTrailing: [" + str.stripTrailing() + "]"); // 输出：[ hello]
```

## 判断字符串是否为空白

```java
System.out.println("".isBlank()); // true（空字符串）
System.out.println("   ".isBlank()); // true（仅空格）
System.out.println("  \t\n".isBlank()); // true（包含制表符、换行符）
System.out.println("  a  ".isBlank()); // false（包含非空白字符）
System.out.println("\u2002\u2003".isBlank()); // true（Unicode 空白字符）
```

## 按行分割字符串

lines() 将字符串按换行符（\n、\r、\r\n 等）分割为多行，返回一个 `Stream<String>`，方便结合流操作处理多行文本。

```java
String multiLine = "first line\nsecond line\rthird line\r\nfourth line";

// 分割为流并遍历
multiLine.lines()
         .forEach(line -> System.out.println("Line: " + line));

// 输出：
// Line: first line
// Line: second line
// Line: third line
// Line: fourth line
```

## 重复字符串指定次数

```java
String str = "ab";

System.out.println(str.repeat(3)); // 输出：ababab（重复3次）
System.out.println("=".repeat(5)); // 输出：=====（重复5次，常用于分隔线）
System.out.println(str.repeat(0)); // 输出：""（count=0 时返回空字符串）
```
