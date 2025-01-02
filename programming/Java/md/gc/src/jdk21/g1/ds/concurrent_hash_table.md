# ConcurrentHashTable

ConcurrentHashTable 是一个并发的哈希表，其读操作是无需等待的，插入操作采用 CAS 机制。每个桶(Bucket)的删除操作是互斥的。

VALUE 是保存在每个节点(Node)内部的类型，CONFIG 包含了哈希方法和分配方法。

对于获取和插入操作，需要提供一个回调函数(CALLBACK_FUNC)和查找函数(LOOKUP_FUNC)。

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
        // _first指针的最低两位用来存储自旋锁的状态信息，分别是未加锁、加锁、重定向三种状态
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
};
```

## 获取元素

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

// Get methods return true on found item with LOOKUP_FUNC and FOUND_FUNC is
// called.
template<typename CONFIG, MEMFLAGS F>
template<typename LOOKUP_FUNC, typename FOUND_FUNC>
inline bool ConcurrentHashTable<CONFIG, F>::
get(Thread *thread, LOOKUP_FUNC &lookup_f, FOUND_FUNC &found_f, bool *grow_hint) {
    bool ret = false;
    ScopedCS cs(thread, this);
    VALUE *val = internal_get(thread, lookup_f, grow_hint);
    if (val != nullptr) {
        found_f(val);
        ret = true;
    }
    return ret;
}

// Always called within critical section
template<typename CONFIG, MEMFLAGS F>
template<typename LOOKUP_FUNC>
inline typename CONFIG::Value *ConcurrentHashTable<CONFIG, F>::
internal_get(Thread *thread, LOOKUP_FUNC &lookup_f, bool *grow_hint) {
    bool clean = false;
    size_t loops = 0;
    VALUE *ret = nullptr;

    const Bucket *bucket = get_bucket(lookup_f.get_hash());
    Node *node = get_node(bucket, lookup_f, &clean, &loops);
    if (node != nullptr) {
        ret = node->value();
    }
    if (grow_hint != nullptr) {
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
