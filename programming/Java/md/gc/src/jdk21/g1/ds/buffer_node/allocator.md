# 分配器

```cpp
// --- src/hotspot/share/gc/shared/ptrQueue.hpp --- //

class BufferNode::Allocator {
    friend class TestSupport;

    AllocatorConfig _config;
    // 空闲链表, 依赖 AllocatorConfig 实现具体的内存分配
    FreeListAllocator _free_list;

    NONCOPYABLE(Allocator);

public:
    Allocator(const char *name, size_t buffer_size);

    ~Allocator() = default;

    size_t buffer_size() const { return _config.buffer_size(); }

    size_t free_count() const;

    // 从空闲链表获取内存，并原地构造 BufferNode
    BufferNode *allocate();

    // 析构节点并归还内存到空闲链表
    void release(BufferNode *node);
};
```

## 内存分配流程

```
用户调用 Allocator::allocate()
    |
    v
FreeListAllocator 检查空闲链表
    ├── 如果链表非空 -> 弹出节点直接返回
    └── 如果链表为空 -> 调用 AllocatorConfig::allocate() 分配新内存块
            |
            v
        AllocatorConfig 计算总大小（头部 + 缓冲区）
            |
            v
        malloc/new 分配连续内存
            |
            v
        返回内存地址，构造 BufferNode
```

```cpp
// --- src/hotspot/share/gc/shared/ptrQueue.cpp --- //

BufferNode *BufferNode::Allocator::allocate() {
    return ::new(_free_list.allocate()) BufferNode();
}

void BufferNode::Allocator::release(BufferNode *node) {
    assert(node != nullptr, "precondition");
    assert(node->next() == nullptr, "precondition");
    node->~BufferNode();
    _free_list.release(node);
}
```

## AllocatorConfig

```cpp
// --- src/hotspot/share/gc/shared/ptrQueue.hpp --- //

class BufferNode::AllocatorConfig : public FreeListConfig {
    // 每个 BufferNode 管理的缓冲区容量（单位：void* 数量）
    const size_t _buffer_size;
public:
    explicit AllocatorConfig(size_t size);

    ~AllocatorConfig() = default;

    void *allocate() override;

    void deallocate(void *node) override;

    size_t buffer_size() const { return _buffer_size; }
};

// --- src/hotspot/share/gc/shared/ptrQueue.cpp --- //

void *BufferNode::AllocatorConfig::allocate() {
    size_t byte_size = _buffer_size * sizeof(void *);
    return NEW_C_HEAP_ARRAY(char, buffer_offset() + byte_size, mtGC);
}

void BufferNode::AllocatorConfig::deallocate(void *node) {
    assert(node != nullptr, "precondition");
    FREE_C_HEAP_ARRAY(char, node);
}
```
