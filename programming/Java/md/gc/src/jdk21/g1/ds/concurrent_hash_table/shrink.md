# 缩容

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline bool ConcurrentHashTable<CONFIG, F>::
shrink(Thread *thread, size_t size_limit_log2) {
    size_t tmp = size_limit_log2 == 0 ? _log2_start_size : size_limit_log2;
    bool ret = internal_shrink(thread, tmp);
    return ret;
}

template<typename CONFIG, MEMFLAGS F>
inline bool ConcurrentHashTable<CONFIG, F>::
internal_shrink(Thread *thread, size_t log2_size) {
    // 分配一块新内存, 用_new_table指向
    if (!internal_shrink_prolog(thread, log2_size)) {
        assert(_resize_lock_owner != thread, "Re-size lock held");
        return false;
    }
    assert(_resize_lock_owner == thread, "Should be locked by me");
    internal_shrink_range(thread, 0, _new_table->_size);
    internal_shrink_epilog(thread);
    assert(_resize_lock_owner != thread, "Re-size lock held");
    return true;
}
```

## 分配一块新内存

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline bool ConcurrentHashTable<CONFIG, F>::
internal_shrink_prolog(Thread *thread, size_t log2_size) {
    if (!try_resize_lock(thread)) {
        return false;
    }
    assert(_resize_lock_owner == thread, "Re-size lock not held");
    if (_table->_log2_size == _log2_start_size ||
        _table->_log2_size <= log2_size) {
        // 本函数只缩容
        unlock_resize_lock(thread);
        return false;
    }
    // 创建临时table, 缩小为原来的二分之一
    _new_table = new InternalTable(_table->_log2_size - 1);
    return true;
}
```

## 把原来的数据复制到新内存

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline void ConcurrentHashTable<CONFIG, F>::
internal_shrink_range(Thread *thread, size_t start, size_t stop) {
    for (size_t bucket_it = start; bucket_it < stop; bucket_it++) {
        // [0, 1, 2, 3, 4, 5, 6, 7]
        //  ⭣           ⭣
        //  x            x
        //  x            x

        // [0, 1, 2, 3]
        //  ⭣
        //  x
        //  x
        //  x
        //  x

        size_t even_hash_index = bucket_it; // High bit 0
        size_t odd_hash_index = bucket_it + _new_table->_size; // High bit 1

        Bucket *b_old_even = _table->get_bucket(even_hash_index);
        Bucket *b_old_odd = _table->get_bucket(odd_hash_index);

        b_old_even->lock();
        b_old_odd->lock();

        _new_table->get_buckets()[bucket_it] = *b_old_even;

        // 把b_old_odd追加到bucket_it对应的bucket中
        _new_table->get_bucket(bucket_it)->
                release_assign_last_node_next(*(b_old_odd->first_ptr()));

        b_old_even->redirect();
        b_old_odd->redirect();

        write_synchonize_on_visible_epoch(thread);

        _new_table->get_bucket(bucket_it)->unlock();

        DEBUG_ONLY(b_old_even->release_assign_node_ptr(b_old_even->first_ptr(),
                                                       (Node *) POISON_PTR);)
        DEBUG_ONLY(b_old_odd->release_assign_node_ptr(b_old_odd->first_ptr(),
                                                      (Node *) POISON_PTR);)
    }
}

template<typename CONFIG, MEMFLAGS F>
inline void ConcurrentHashTable<CONFIG, F>::
Bucket::release_assign_last_node_next(
        typename ConcurrentHashTable<CONFIG, F>::Node *node) {
    assert(is_locked(), "Must be locked.");
    Node *const volatile *ret = first_ptr();
    while (clear_state(*ret) != nullptr) {
        ret = clear_state(*ret)->next_ptr();
    }
    // 把b_old_odd追加到bucket后面
    release_assign_node_ptr(ret, node);
}
```

## 发布新内存并清理旧内存

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline void ConcurrentHashTable<CONFIG, F>::
internal_shrink_epilog(Thread *thread) {
    assert(_resize_lock_owner == thread, "Re-size lock not held");

    InternalTable *old_table = set_table_from_new();
    _size_limit_reached = false;
    unlock_resize_lock(thread);
#ifdef ASSERT
    for (size_t i = 0; i < old_table->_size; i++) {
        assert(old_table->get_bucket(i++)->first() == POISON_PTR,
               "No poison found");
    }
#endif
    delete old_table;
}
```
