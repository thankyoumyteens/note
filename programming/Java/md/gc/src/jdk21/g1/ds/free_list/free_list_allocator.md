# FreeListAllocator

```cpp
class FreeListAllocator {
    static FreeNode *volatile *next_ptr(FreeNode &node) { return node.next_addr(); }

    typedef LockFreeStack<FreeNode, &next_ptr> Stack;

    FreeListConfig *_config;
    char _name[DEFAULT_CACHE_LINE_SIZE - sizeof(FreeListConfig *)];  // Use name as padding.

// 缓存行填充, 将高频访问的成员变量（如 _free_count、_free_list）分配到不同的缓存行，避免伪共享
#define DECLARE_PADDED_MEMBER(Id, Type, Name) \
  Type Name; DEFINE_PAD_MINUS_SIZE(Id, DEFAULT_CACHE_LINE_SIZE, sizeof(Type))
    DECLARE_PADDED_MEMBER(1, volatile size_t, _free_count);
    // Stack _free_list; 无锁空闲列表
    // LockFreeStack使用无锁操作, 减少同步开销
    DECLARE_PADDED_MEMBER(2, Stack, _free_list);
    DECLARE_PADDED_MEMBER(3, volatile bool, _transfer_lock);
#undef DECLARE_PADDED_MEMBER

    // 使用两个 PendingList（类似双缓冲机制），避免在批量转移时阻塞新的释放操作
    // 操作流程:
    // 1. 初始时 _active_pending_list = 0，释放操作写入 _pending_lists[0]
    // 2. 当触发批量转移(try_transfer_pending函数)时:
    //    1. 切换 _active_pending_list = 1，新的释放操作写入 _pending_lists[1]
    //    2. 处理 _pending_lists[0] 中的节点并清空
    // 3. 下次转移时切换回 _pending_lists[0]
    volatile uint _active_pending_list; // 当前活跃的待处理列表索引
    PendingList _pending_lists[2]; // 双缓冲待处理列表

    void delete_list(FreeNode *list);

    NONCOPYABLE(FreeListAllocator);

public:
    FreeListAllocator(const char *name, FreeListConfig *config);

    const char *name() const { return _name; }

    ~FreeListAllocator();

    size_t free_count() const;

    size_t pending_count() const;

    // 获取一个新的节点给用户使用
    // 1. 尝试从空闲列表_free_list获取节点
    // 2. 空闲列表为空，通过FreeListConfig::allocate()分配新内存
    void *allocate();

    // 回收一个节点
    // 1. 将节点添加到当前活跃的待处理列表: _pending_lists[_active_pending_list]
    // 2. 调用 try_transfer_pending() 尝试转移节点到空闲列表_free_list
    void release(void *node);

    void reset();

    // 批量转移流程:
    // 1. 切换 _active_pending_list 到下一个索引，确保转移过程中新的释放操作不受影响
    // 2. 检查是否需要触发批量转移:
    //    当 _pending_lists[old_active_list] 中的节点数量达到阈值FreeListConfig::_transfer_threshold时触发
    // 3. 尝试从 _pending_lists[old_active_list] 中获取节点并转移到空闲列表_free_list
    // 4. 返回是否成功转移
    bool try_transfer_pending();

    size_t mem_size() const {
        return sizeof(*this);
    }
};
```

## 多线程分配与释放流程

```
线程1: allocate()           -> 从 _free_list 弹出节点
线程2: release(node1)       -> 添加到 _pending_lists[0]
线程3: release(node2)       -> 添加到 _pending_lists[0]
线程4: release(node3)       -> _pending_lists[0] 计数达阈值，触发 try_transfer_pending()
       |
       v
try_transfer_pending():
   1. 切换 _active_pending_list = 1
   2. 将 _pending_lists[0] 的节点转移到 _free_list
   3. 后续 release() 操作写入 _pending_lists[1]
```

表示一组批量操作的节点集合，用于从 PendingList 到 FreeList 的转移

```cpp
struct NodeList {
    FreeNode *_head;
    FreeNode *_tail;
    size_t _entry_count;

    NodeList();

    NodeList(FreeNode *head, FreeNode *tail, size_t entry_count);
};

class PendingList {
    FreeNode *_tail;
    FreeNode *volatile _head;
    volatile size_t _count;

    NONCOPYABLE(PendingList);

public:
    PendingList();

    ~PendingList() = default;

    size_t add(FreeNode *node);

    size_t count() const;

    NodeList take_all();
};
```

## 分配与释放节点

```cpp
// --- src/hotspot/share/gc/shared/freeListAllocator.cpp --- //

void* FreeListAllocator::allocate() {
  FreeNode* node = nullptr;
  // 检查空闲节点
  if (free_count() > 0) {
    // 进入全局计数器临界区（解决ABA问题）
    GlobalCounter::CriticalSection cs(Thread::current());
    // 从空闲列表中弹出一个节点
    node = _free_list.pop();
  }

  if (node != nullptr) {
      // 清理节点, 因为这个节点在回收到_free_list之前可能已经被使用过了
    node->~FreeNode();
    // 更细空闲列表中的可用节点数
    size_t count = Atomic::sub(&_free_count, 1u);
    assert((count + 1) != 0, "_free_count underflow");
    return node;
  } else {
      // 如果没有空闲节点，从配置中分配一个新节点
    return _config->allocate();
  }
}

void FreeListAllocator::release(void* free_node) {
  assert(free_node != nullptr, "precondition");
  assert(is_aligned(free_node, sizeof(FreeNode)), "Unaligned addr " PTR_FORMAT, p2i(free_node));
  // 原地构造 FreeNode
  FreeNode* node = ::new (free_node) FreeNode();

  {
      // 进入全局计数器临界区, 确保与 allocate 操作互斥
    GlobalCounter::CriticalSection cs(Thread::current());
    // 获取当前在用的pending list索引
    uint index = Atomic::load_acquire(&_active_pending_list);
    // 添加节点到待处理列表
    size_t count = _pending_lists[index].add(node);
    // 检查是否达到转移阈值, 如果没有达到, 则直接返回, 不进行转移操作
    if (count <= _config->transfer_threshold()) return;
  }
  // 尝试批量转移
  try_transfer_pending();
}
```
