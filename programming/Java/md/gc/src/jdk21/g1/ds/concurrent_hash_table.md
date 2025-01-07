# ConcurrentHashTable

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

        static const uintptr_t STATE_LOCK_BIT = 0x1;
        static const uintptr_t STATE_REDIRECT_BIT = 0x2;
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

## Node 操作

```cpp
template<typename CONFIG, MEMFLAGS F>
template<typename LOOKUP_FUNC>
typename ConcurrentHashTable<CONFIG, F>::Node *
ConcurrentHashTable<CONFIG, F>::
get_node(const Bucket *const bucket, LOOKUP_FUNC &lookup_f,
         bool *have_dead, size_t *loops) const {
    size_t loop_count = 0;
    Node *node = bucket->first();
    while (node != nullptr) {
        bool is_dead = false;
        ++loop_count;
        if (lookup_f.equals(node->value(), &is_dead)) {
            break;
        }
        if (is_dead && !(*have_dead)) {
            *have_dead = true;
        }
        node = node->next();
    }
    if (loops != nullptr) {
        *loops = loop_count;
    }
    return node;
}
```

## Bucket 操作

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline typename ConcurrentHashTable<CONFIG, F>::Bucket *
ConcurrentHashTable<CONFIG, F>::
get_bucket(uintx hash) const {
    // 获取 _table
    InternalTable *table = get_table();
    // 根据哈希值获取bucket数组中的元素
    Bucket *bucket = get_bucket_in(table, hash);
    // ConcurrentHashTable 正在扩容, 需要使用 _new_table, 而不是 _table
    // 根据哈希值重新获取bucket数组中的元素
    if (bucket->have_redirect()) {
        table = get_new_table();
        bucket = get_bucket_in(table, hash);
    }
    return bucket;
}

Bucket *ConcurrentHashTable::get_bucket_in(InternalTable *table, const uintx hash) const {
    // 根据哈希值算出数组的索引
    size_t bucket_index = bucket_idx_hash(table, hash);
    return table->get_bucket(bucket_index);
}

static size_t ConcurrentHashTable::bucket_idx_hash(InternalTable *table, const uintx hash) {
    // _hash_mask 用来保证算出的索引不会落在数组外
    return ((size_t) hash) & table->_hash_mask;
}

Bucket *InternalTable::get_bucket(size_t idx) {
    return &_buckets[idx];
}
```

## RCU 读临界区

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.hpp --- //

// Scoped critical section, which also handles the invisible epochs.
// An invisible epoch/version do not need a write_synchronize().
class ScopedCS : public StackObj {
protected:
    // 读线程
    Thread *_thread;
    // 要读取的哈希表
    ConcurrentHashTable<CONFIG, F> *_cht;
    // 用于传给 critical_section_end 函数
    GlobalCounter::CSContext _cs_context;
public:
    // 进入RCU读临界区
    ScopedCS(Thread *thread, ConcurrentHashTable<CONFIG, F> *cht);

    // 退出RCU读临界区
    ~ScopedCS();
};

// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

// 进入RCU读临界区
template<typename CONFIG, MEMFLAGS F>
inline ConcurrentHashTable<CONFIG, F>::
ScopedCS::ScopedCS(Thread *thread, ConcurrentHashTable<CONFIG, F> *cht)
        : _thread(thread),
          _cht(cht),
          _cs_context(GlobalCounter::critical_section_begin(_thread)) {
    // This version is published now.
    if (Atomic::load_acquire(&_cht->_invisible_epoch) != nullptr) {
        Atomic::release_store_fence(&_cht->_invisible_epoch, (Thread *) nullptr);
    }
}

// 退出RCU读临界区
template<typename CONFIG, MEMFLAGS F>
inline ConcurrentHashTable<CONFIG, F>::
ScopedCS::~ScopedCS() {
    GlobalCounter::critical_section_end(_thread, _cs_context);
}
```

## 获取元素

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

// get 函数会使用 LOOKUP_FUNC 函数来查找指定元素
// 如果找到了元素则返回true, 并把找到的元素作为参数调用 FOUND_FUNC 函数
template<typename CONFIG, MEMFLAGS F>
template<typename LOOKUP_FUNC, typename FOUND_FUNC>
inline bool ConcurrentHashTable<CONFIG, F>::
get(Thread *thread, LOOKUP_FUNC &lookup_f, FOUND_FUNC &found_f, bool *grow_hint) {
    bool ret = false;
    // 进入RCU读临界区
    ScopedCS cs(thread, this);
    // 查找元素
    VALUE *val = internal_get(thread, lookup_f, grow_hint);
    if (val != nullptr) {
        // 找到了, 调用 FOUND_FUNC
        found_f(val);
        ret = true;
    }
    return ret;
    // 退出RCU读临界区
}

template<typename CONFIG, MEMFLAGS F>
template<typename LOOKUP_FUNC>
inline typename CONFIG::Value *ConcurrentHashTable<CONFIG, F>::
internal_get(Thread *thread, LOOKUP_FUNC &lookup_f, bool *grow_hint) {
    bool clean = false;
    size_t loops = 0;
    VALUE *ret = nullptr;

    // 根据 lookup_f.get_hash() 返回的哈希值, 从Bucket数组中获取指定的Bucket
    const Bucket *bucket = get_bucket(lookup_f.get_hash());
    // 根据 lookup_f.equals(), 找到匹配的Node
    Node *node = get_node(bucket, lookup_f, &clean, &loops);
    if (node != nullptr) {
        // 找到了
        ret = node->value();
    }
    if (grow_hint != nullptr) {
        // loops: 在Node链表中查找Node时遍历过的节点数
        // _grow_hint: 扩容的阈值
        // loops > _grow_hint 时需要扩容(增大Bucket数组的长度以减少Node链表的长度)
        *grow_hint = loops > _grow_hint;
    }

    return ret;
}
```

## 新增元素

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.hpp --- //

template<typename CONFIG, MEMFLAGS F>
class ConcurrentHashTable : public CHeapObj<F> {
    // Returns true if the item was inserted, duplicates are found with
    // LOOKUP_FUNC then FOUND_FUNC is called.
    template<typename LOOKUP_FUNC, typename FOUND_FUNC>
    bool insert_get(Thread *thread, LOOKUP_FUNC &lookup_f, VALUE &value, FOUND_FUNC &foundf,
                    bool *grow_hint = nullptr, bool *clean_hint = nullptr) {
        return internal_insert_get(thread, lookup_f, value, foundf, grow_hint, clean_hint);
    }
};
```

## 删除元素

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.hpp --- //

template<typename CONFIG, MEMFLAGS F>
class ConcurrentHashTable : public CHeapObj<F> {
    // Returns true if items was deleted matching LOOKUP_FUNC and
    // prior to destruction DELETE_FUNC is called.
    template<typename LOOKUP_FUNC, typename DELETE_FUNC>
    bool remove(Thread *thread, LOOKUP_FUNC &lookup_f, DELETE_FUNC &del_f) {
        return internal_remove(thread, lookup_f, del_f);
    }
};
```

## 扩容

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline bool ConcurrentHashTable<CONFIG, F>::
grow(Thread *thread, size_t size_limit_log2) {
    size_t tmp = size_limit_log2 == 0 ? _log2_size_limit : size_limit_log2;
    return internal_grow(thread, tmp);
}
```
