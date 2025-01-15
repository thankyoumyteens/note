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

```
