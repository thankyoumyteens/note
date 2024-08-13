# ArrayList

## 数组索引为什么不从 1 开始

以 int 数组为例, 内存结构如下:

```
[100(4字节)] [200(4字节)] [300(4字节)] [...]
 ⬆️
指针
```

访问索引为 2 的元素 300: `指针 + (2 * 4字节)`

如果索引从 1 开始, 访问索引为 3 的元素 300: `指针 + [(3 - 1) * 4字节)]`, 多了一步计算, 增加了 cpu 的负担

## 时间复杂度

- 随机访问: O(1)
- 无序数组查找元素: O(n)
- 有序数组二分查找元素: O(logn)
- 插入元素: O(n)
- 删除元素: O(n)

## 扩容

调用无参构造方法时容量是 0, 首次添加元素后扩容为 10, 代码:

```java
private static final int DEFAULT_CAPACITY = 10;

// 无参构造方法
public ArrayList() {
    this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
}

// 添加元素
public boolean add(E e) {
    // size默认为0
    ensureCapacityInternal(size + 1);
    elementData[size++] = e;
    return true;
}

private void ensureCapacityInternal(int minCapacity) {
    ensureExplicitCapacity(calculateCapacity(elementData, minCapacity));
}

private static int calculateCapacity(Object[] elementData, int minCapacity) {
    if (elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
        // 首次添加元素会返回10
        return Math.max(DEFAULT_CAPACITY, minCapacity);
    }
    return minCapacity;
}

private void ensureExplicitCapacity(int minCapacity) {
    modCount++;

    if (minCapacity - elementData.length > 0)
        // 扩容
        grow(minCapacity);
}
```

触发扩容的时机, 添加超出容量的元素时, 比如容量为 10, 那么添加第 11 个元素时会扩容。

每次扩容 1.5 倍, 代码:

```java
int newCapacity = oldCapacity + (oldCapacity >> 1);
```
