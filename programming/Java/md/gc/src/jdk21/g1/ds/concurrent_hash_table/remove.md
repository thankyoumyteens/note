# 删除元素

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
