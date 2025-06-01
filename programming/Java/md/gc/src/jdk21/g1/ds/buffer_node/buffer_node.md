# BufferNode

BufferNode 用于管理缓冲区（buffer）并结合无锁栈（LockFreeStack）实现高效的内存分配。

整个 BufferNode 的核心秘密在于利用 C/C++ 的内存连续布局特性，将元数据（\_index 字段, \_next 字段）和实际缓冲区内存合并到同一块连续内存中。其内存结构如下：

```
[ BufferNode 头部 (_index, _next) | 实际缓冲区（动态大小） ]
```

```cpp
class BufferNode {
    size_t _index;
    BufferNode *volatile _next;
    // 伪灵活数组成员，实际用于存储缓冲区数据
    // 在 C99 中允许 flexible array member（如 int data[];），但 C++ 标准不支持, 这里通过 _buffer[1] 模拟该特性
    // _buffer[1] 作为占位符，实际通过 BufferNode::Allocator(内部使用malloc等方式)分配更大的内存，使 _buffer 扩展为动态长度数组
    void *_buffer[1];             // Pseudo flexible array member.

    BufferNode() : _index(0), _next(nullptr) {}

    ~BufferNode() {}

    // NONCOPYABLE 宏禁用拷贝构造和赋值，防止意外复制
    NONCOPYABLE(BufferNode);

    // 计算 _buffer 在 BufferNode 中的偏移量，用于地址转换
    // 转换逻辑：
    // 1. 从缓冲区找节点：buffer地址 - buffer_offset() = BufferNode头部地址
    // 2. 从节点找缓冲区：BufferNode对象的地址 + buffer_offset() = buffer起始地址
    static size_t buffer_offset() {
        // 假设 BufferNode 内存布局如下:
        // | _index (8字节) | _next (8字节) | _buffer[0] (8字节) | ...
        // 则 buffer_offset() 返回 16（即前两个成员的总大小）
        return offset_of(BufferNode, _buffer);
    }

public:
    // 返回 _next 的地址，供 LockFreeStack 操作
    static BufferNode *volatile *next_ptr(BufferNode &bn) { return &bn._next; }

    // 定义无锁栈类型，用于管理BufferNode链表
    typedef LockFreeStack<BufferNode, &next_ptr> Stack;

    BufferNode *next() const { return _next; }

    void set_next(BufferNode *n) { _next = n; }

    size_t index() const { return _index; }

    void set_index(size_t i) { _index = i; }

    // 通过缓冲区地址反推所属节点地址，并设置索引
    // 使用场景：当外部只有缓冲区地址时（例如用户释放缓冲区），需要找到对应的 BufferNode 以便将其放回空闲链表
    // 假设 buffer 地址为 0x1000, buffer_offset() 为 16, 则节点地址 = 0x1000 - 16 = 0xFF0
    static BufferNode *make_node_from_buffer(void **buffer, size_t index) {
        // buffer指针指向的是BufferNode对象中_buffer字段的地址
        // 将 buffer 指针回退到 BufferNode 对象的头部位置, 得到指向BufferNode对象的指针
        BufferNode *node = reinterpret_cast<BufferNode *>(
                // reinterpret_cast<char *>(buffer) 将 void** 类型的 buffer 转换为 char* 类型(字节指针)
                // buffer_offset() 获取 _buffer 字段在BufferNode类中的偏移量
                // 把指针向前移动到BufferNode对象的起始位置
                reinterpret_cast<char *>(buffer) - buffer_offset()
        );
        node->set_index(index);
        return node;
    }

    // 通过节点地址计算其管理的缓冲区地址
    // 使用场景：当分配一个节点时，需要将节点内的 _buffer 地址返回给用户使用
    // 假设节点地址为 0xFF0, buffer_offset() 为 16, 则缓冲区地址 = 0xFF0 + 16 = 0x1000
    // 由于节点和缓冲区是连续分配的，用户获得的 void** 可以安全地作为数组使用
    static void **make_buffer_from_node(BufferNode *node) {
        return reinterpret_cast<void **>(
                reinterpret_cast<char *>(node) + buffer_offset()
        );
    }

    class AllocatorConfig;

    class Allocator; // 用来分配无锁空闲链表
    class TestSupport;
};
```
