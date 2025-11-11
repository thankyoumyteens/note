# 数字格式化工具类

Java 12 对 CompactNumberFormat（用于紧凑数字格式，如 "1.2K" 表示 1200）的本地化支持进一步完善，可用于工具类中新增 “紧凑格式” 功能：

```java
// 示例：紧凑格式（如 1500 -> "1.5K"）
public static String formatCompact(Number number, Locale locale) {
    NumberFormat compactFormat = NumberFormat.getCompactNumberInstance(
        locale, NumberFormat.Style.SHORT
    );
    return compactFormat.format(number);
}
```
