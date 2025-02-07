# Howl 模式容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.hpp --- //

class G1CardSetHowl : public G1CardSetContainer {
public:
    typedef uint EntryCountType;
    using ContainerPtr = G1CardSet::ContainerPtr;
    EntryCountType volatile _num_entries;
private:
    // ContainerPtr数组
    ContainerPtr _buckets[2];
public:
    // 根据_buckets数组的索引返回容器指针的指针
    ContainerPtr *get_container_addr(EntryCountType index) {
        return &_buckets[index];
    }
};
```
