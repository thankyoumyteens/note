# 获取元素

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
