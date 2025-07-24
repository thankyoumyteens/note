# 无锁空闲列表

通过 无锁空闲列表(Free List) + 双缓冲待处理列表 + 批量转移策略，在保证线程安全的同时，显著降低了多线程环境下的同步开销。其设计思想可广泛应用于高并发内存池、对象池等场景。

完整协作流程图:

```
           allocate()                                   release(node)
              |                                              |
              v                                              v
   +-----------------------+                         +-----------------+
   |   Free List           |                         |  Pending List   |
   | (使用LockFreeStack管理)|                         | (双缓冲设计)      |
   +-----------------------+                         +-----------------+
              | 空时调用                                      | 达到阈值时触发
              v                                              v
+-----------------------------+                   +------------------------+
| FreeListConfig::allocate()  |                   | try_transfer_pending() |
| 分配新内存并构造 Node          |                   | 批量转移到 Free List    |
+-----------------------------+                   +------------------------+
```

## 空闲列表中的节点

```cpp
struct FreeNode {
    FreeNode *volatile _next;

    FreeNode() : _next(nullptr) {}

    FreeNode *next() { return Atomic::load(&_next); }

    FreeNode *volatile *next_addr() { return &_next; }

    void set_next(FreeNode *next) { Atomic::store(&_next, next); }
};
```
