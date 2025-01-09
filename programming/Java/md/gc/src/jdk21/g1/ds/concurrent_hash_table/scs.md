# RCU 读临界区

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
