# 并发哈希表

ConcurrentHashTable 是一个并发的哈希表(数组+链表实现), 其读操作是无需等待的, 插入操作采用 CAS 机制。每个桶(Bucket)的删除操作是互斥的。

VALUE 是保存在每个节点(Node)内部的类型, CONFIG 包含了哈希方法和分配方法。

对于获取和插入操作, 需要提供一个回调函数(CALLBACK_FUNC)和查找函数(LOOKUP_FUNC)。

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.hpp --- //

template<typename CONFIG, MEMFLAGS F>
class ConcurrentHashTable : public CHeapObj<F> {
    typedef typename CONFIG::Value VALUE;
private:

    // 存储数据的节点
    class Node {
    private:
        // 指向下一个节点
        Node *volatile _next;
        // 实际存储数据
        VALUE _value;
    };

    // 用来实现节点的并发访问
    class Bucket {
    private:
        // _first指针的最低两位用来存储自旋锁的状态信息, 分别是未加锁、加锁、重定向三种状态
        Node *volatile _first;

        // 最低两位 00 表示未加锁
        // 最低两位 01 表示加锁
        static const uintptr_t STATE_LOCK_BIT = 0x1;
        // 最低两位 10 表示重定向
        static const uintptr_t STATE_REDIRECT_BIT = 0x2;
        // 最低两位的掩码
        static const uintptr_t STATE_MASK = 0x3;
    };

    // 哈希表
    class InternalTable : public CHeapObj<F> {
    private:
        // Bucket数组
        Bucket *_buckets;
    };

    // 哈希表
    InternalTable *_table;
    // 扩容时的临时表
    InternalTable *_new_table;

    Mutex *_resize_lock;
    // 为了能够在调整大小(resize)以及其他批量操作中避免使用写同步(write_synchronize 函数)
    // _invisible_epoch 用于跟踪哈希表的某个版本是否曾被访问过
    // _invisible_epoch 只能由 _resize_lock 的持有者使用
    volatile Thread *_invisible_epoch;
};
```
