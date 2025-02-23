# 遍历数组容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

template<class CardVisitor>
void G1CardSetArray::iterate(CardVisitor &found) {
    EntryCountType num_entries = Atomic::load_acquire(&_num_entries) & EntryMask;
    for (EntryCountType idx = 0; idx < num_entries; idx++) {
        found(_data[idx]);
    }
}
```
