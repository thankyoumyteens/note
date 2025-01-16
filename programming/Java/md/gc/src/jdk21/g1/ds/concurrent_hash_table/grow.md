# 扩容

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline bool ConcurrentHashTable<CONFIG, F>::
grow(Thread *thread, size_t size_limit_log2) {
    size_t tmp = size_limit_log2 == 0 ? _log2_size_limit : size_limit_log2;
    return internal_grow(thread, tmp);
}

template<typename CONFIG, MEMFLAGS F>
inline bool ConcurrentHashTable<CONFIG, F>::
internal_grow(Thread *thread, size_t log2_size) {
    // 分配一块新内存, 用_new_table指向
    if (!internal_grow_prolog(thread, log2_size)) {
        assert(_resize_lock_owner != thread, "Re-size lock held");
        return false;
    }
    assert(_resize_lock_owner == thread, "Should be locked by me");
    // 把原来的数据复制到_new_table指向的新内存
    internal_grow_range(thread, 0, _table->_size);
    // 用_table指向新内存, 并清理旧内存
    internal_grow_epilog(thread);
    assert(_resize_lock_owner != thread, "Re-size lock held");
    return true;
}

template<typename CONFIG, MEMFLAGS F>
inline bool ConcurrentHashTable<CONFIG, F>::
internal_grow_prolog(Thread *thread, size_t log2_size) {
    if (is_max_size_reached()) {
        // 已经达到最大容量, 不允许继续扩容
        return false;
    }
    if (!try_resize_lock(thread)) {
        // 其它线程正在调整容量, 或者正在进行的操作不允许调整容量
        return false;
    }
    if (is_max_size_reached() || _table->_log2_size >= log2_size) {
        unlock_resize_lock(thread);
        // 本函数只扩容不缩容
        return false;
    }

    // 创建临时table, 扩容为原来的2倍
    _new_table = new InternalTable(_table->_log2_size + 1);
    // 判断是否达到最大容量
    _size_limit_reached = _new_table->_log2_size == _log2_size_limit;

    return true;
}

template<typename CONFIG, MEMFLAGS F>
inline void ConcurrentHashTable<CONFIG, F>::
internal_grow_range(Thread *thread, size_t start, size_t stop) {
    assert(stop <= _table->_size, "Outside backing array");
    assert(_new_table != nullptr, "Grow not proper setup before start");
    // even_index的最高位都是0
    // odd_index的最高位都是1
    // 比如新table长度为8
    // even_index:
    //     0 (000)
    //     1 (001)
    //     2 (010)
    //     3 (011)
    // odd_index:
    //     4 (100)
    //     5 (101)
    //     6 (110)
    //     7 (111)
    for (size_t even_index = start; even_index < stop; even_index++) {
        Bucket *bucket = _table->get_bucket(even_index);

        bucket->lock();

        // 例子:
        // _table->_size = 2, 扩容后 _new_table->_size = 4
        // _new_table: [x, x, x, x]
        // even_index = 0 时, odd_index = 2
        size_t odd_index = even_index + _table->_size;
        // 把旧table的值赋给新table
        _new_table->get_buckets()[even_index] = *bucket;
        _new_table->get_buckets()[odd_index] = *bucket;

        // 把bucket的锁转移到新table上
        // 旧table的bucket的状态改为redirect
        bucket->redirect();

        // 重新分配新table中的节点
        if (!unzip_bucket(thread, _table, _new_table, even_index, odd_index)) {
            DEBUG_ONLY(GlobalCounter::write_synchronize();)
        }

        _new_table->get_bucket(even_index)->unlock();
        _new_table->get_bucket(odd_index)->unlock();

        DEBUG_ONLY(
                bucket->release_assign_node_ptr(
                        _table->get_bucket(even_index)->first_ptr(), (Node *) POISON_PTR);
        )
    }
}
```
