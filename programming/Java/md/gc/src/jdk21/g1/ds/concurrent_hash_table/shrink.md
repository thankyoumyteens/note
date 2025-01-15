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
```
