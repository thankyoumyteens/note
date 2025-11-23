# JLI_List

JLI_List 是一个通用的动态字符串数组，主要用于在 JDK 启动器中存储和管理字符串集合。

```cpp
// --- src/java.base/share/native/libjli/jli_util.h --- //

/**
 * JLI_List_ 结构体 - JLI工具库中的动态字符串数组(char*数组)实现
 */
struct JLI_List_ {
    char **elements;    // 字符串数组，存储实际的字符串元素
    size_t size;        // 当前数组中元素的数量
    size_t capacity;    // 当前数组的容量（可容纳的最大元素数量）
};

/**
 * JLI_List - JLI_List_ 结构体的指针类型定义
 *
 * 这个 typedef 提供了一个更简洁的类型名称，用于在代码中引用 JLI_List_ 结构体指针，
 * 方便在 JDK 启动器中进行动态字符串列表的操作和传递。
 */
typedef struct JLI_List_ *JLI_List;
```
