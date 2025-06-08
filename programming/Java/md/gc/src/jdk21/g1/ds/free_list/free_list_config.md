# FreeListConfig

```cpp
class FreeListConfig {
    // 当空闲列表中的空闲节点数量超过此阈值时，触发批量操作（如批量释放到全局内存池或批量申请新内存）
    const size_t _transfer_threshold;
protected:
    ~FreeListConfig() = default;

public:
    explicit FreeListConfig(size_t threshold = 10) : _transfer_threshold(threshold) {}

    size_t transfer_threshold() { return _transfer_threshold; }

    virtual void *allocate() = 0;

    virtual void deallocate(void *node) = 0;
};
```
