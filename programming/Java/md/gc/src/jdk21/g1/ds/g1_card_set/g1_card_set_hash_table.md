# G1CardSetHashTable

G1CardSetHashTable 内部通过 ConcurrentHashTable 实现。

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

using CardSetHash = ConcurrentHashTable<G1CardSetHashTableConfig, mtGCCardSet>;

class G1CardSetHashTable : public CHeapObj<mtGCCardSet> {
    using ContainerPtr = G1CardSet::ContainerPtr;
    using CHTScanTask = CardSetHash::ScanTask;

    G1CardSetMemoryManager *_mm;
    CardSetHash _table;
    CHTScanTask _table_scanner;
};
```

## G1CardSetHashTableValue

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

class G1CardSetHashTableValue {
public:
    using ContainerPtr = G1CardSet::ContainerPtr;

    // card_region的索引
    // 一个card_region中包含多个卡片索引
    // 一个分区(heap region)由多个card_region覆盖
    const uint _region_idx;
    uint volatile _num_occupied;
    // 容器指针
    ContainerPtr volatile _container;
};
```

## G1CardSetHashTableConfig

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

class G1CardSetHashTableConfig : public StackObj {
public:
    using Value = G1CardSetHashTableValue;

    static uintx get_hash(Value const &value, bool *is_dead);

    static void *allocate_node(void *context, size_t size, Value const &value);

    static void free_node(void *context, void *memory, Value const &value);
};
```
