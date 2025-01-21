# G1CardSetHashTable

G1CardSetHashTable 内部通过 ConcurrentHashTable 实现。

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

class G1CardSetHashTableValue {
public:
    using ContainerPtr = G1CardSet::ContainerPtr;

    // 容器对应的分区的索引
    const uint _region_idx;
    uint volatile _num_occupied;
    // 容器指针
    ContainerPtr volatile _container;
};

class G1CardSetHashTableConfig : public StackObj {
public:
    using Value = G1CardSetHashTableValue;

    static uintx get_hash(Value const &value, bool *is_dead);

    static void *allocate_node(void *context, size_t size, Value const &value);

    static void free_node(void *context, void *memory, Value const &value);
};

using CardSetHash = ConcurrentHashTable<G1CardSetHashTableConfig, mtGCCardSet>;

class G1CardSetHashTable : public CHeapObj<mtGCCardSet> {
    using ContainerPtr = G1CardSet::ContainerPtr;
    using CHTScanTask = CardSetHash::ScanTask;

    G1CardSetMemoryManager *_mm;
    CardSetHash _table;
    CHTScanTask _table_scanner;
};
```
