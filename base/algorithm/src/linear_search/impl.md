# 实现线性查找

```java
/**
 * 线性查找
 *
 * @param data   待查找的数组
 * @param target 目标值
 * @param <E>    数组元素的类型
 * @return 目标值在数组data中的索引，如果未找到则返回-1
 */
public static <E> int search(E[] data, E target) {
    for (int i = 0; i < data.length; i++) {
        if (data[i].equals(target)) {
            return i;
        }
    }
    return -1;
}
```
