# 接口支持私有方法

在 Java 8 中，接口已支持默认方法（default 方法） 和静态方法（static 方法），用于在接口中提供方法实现。但此时存在一个问题：若多个默认方法或静态方法需要复用一段共同逻辑，无法将这段逻辑封装为私有方法（Java 8 接口中不允许私有方法），只能将其公开为默认方法（可能被误调用）或重复编写代码（导致冗余）。

Java 9 的接口私有方法正是为解决这一问题而生：

- 允许在接口中定义 private 修饰的方法，仅接口内部的默认方法或静态方法可调用。
- 实现接口内部的代码复用，同时不暴露额外的公共 API，保持接口的简洁性和封装性。

```java
public interface DataProcessor {

    // 默认方法：处理数据（依赖校验和格式化）
    default String processData(String data) {
        if (isValid(data)) { // 调用私有实例方法
            return formatData(data); // 调用私有实例方法
        }
        throw new IllegalArgumentException("Invalid data");
    }

    // 默认方法：批量处理数据
    default List<String> processBatch(List<String> dataList) {
        return dataList.stream()
            .filter(this::isValid) // 调用私有实例方法
            .map(this::formatData) // 调用私有实例方法
            .collect(Collectors.toList());
    }

    // 静态方法：解析数据（依赖静态校验）
    static String parseData(String raw) {
        if (isStaticValid(raw)) { // 调用私有静态方法
            return raw.trim();
        }
        return "";
    }

    // 私有实例方法：校验数据（供默认方法复用）
    private boolean isValid(String data) {
        return data != null && !data.isEmpty();
    }

    // 私有实例方法：格式化数据（供默认方法复用）
    private String formatData(String data) {
        return data.toUpperCase();
    }

    // 私有静态方法：静态校验（供静态方法复用）
    private static boolean isStaticValid(String raw) {
        return raw != null && raw.length() > 2;
    }
}
```
