# 卡片索引集合

卡片索引集合(G1CardSet)内部通过 G1CardSetHashTable 实现, G1 通过这些卡片索引来构建和维护记忆集。

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.hpp --- //

class G1CardSet : public CHeapObj<mtGCCardSet> {
public:
    using ContainerPtr = void *;
    // 内联指针卡片模式
    static const uintptr_t ContainerInlinePtr = 0x0;
    // 卡片数组模式
    static const uintptr_t ContainerArrayOfCards = 0x1;
    // 位图模式
    static const uintptr_t ContainerBitMap = 0x2;
    // Howl 模式
    static const uintptr_t ContainerHowl = 0x3;

private:
    // 管理G1CardSet的内存
    G1CardSetMemoryManager *_mm;
    G1CardSetConfiguration *_config;

    // 实际保存数据
    G1CardSetHashTable *_table;

    // G1CardSet中卡片的总数
    size_t _num_occupied;
};
```

ContainerPtr 用来表示 card set container 的类型(一个 container 对应一个分区, G1CardSet 包含许多 container), 它在最低有效位(LSBs)中对一种类型进行编码，以此来区分不同的容器类型及状态。

- `0...00000` free(空闲状态): 这个容器是空的
- `1...11111` full(已满状态): 对应区域内的卡片都已经被包含在这个容器之中了，是一种完全填满的状态
- `X...XXX00` inline-ptr-cards(内联指针卡片模式): 将卡片索引直接嵌入到指针内部，适合卡片数量较少的情况
- `X...XXX01` array of cards(卡片数组模式): 容器是由连续的卡片索引组成的数组来表示的
- `X...XXX10` bitmap(位图模式): 容器使用位图来确定给定的卡片索引是否属于这个 G1CardSet
- `X...XXX11` howl(Howl 模式): 这是一种特殊的容器，它内部包含一个 ContainerPtr 的数组, 并且每个 ContainerPtr 被限制在原始范围的一个子范围内

容器的指针最初是以内联容器的形式开始的，随着更多卡片被添加进来，它会按照一定顺序进行"粗化"(Coarsening), 也就是改变其表示形式以适应更多卡片的管理需求。具体粗化顺序: ContainerInlinePtr -> ContainerArrayOfCards -> ContainerHowl -> Full。

Howl 容器本质上是容器的数组，其中的每个条目最初是 Free(空闲)状态, 在 ContainerHowl 内部的容器进一步粗化按照以下顺序进行: Free -> ContainerInlinePtr -> ContainerArrayOfCards -> ContainerBitMap -> Full。
