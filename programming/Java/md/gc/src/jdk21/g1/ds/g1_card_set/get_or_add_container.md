# 获取分区对应的容器

获取分区(card_region)对应的容器, 如果不存在则新建一个

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

G1CardSetHashTableValue *G1CardSet::get_or_add_container(uint card_region, bool *should_grow_table) {
    // _table是G1CardSetHashTable
    return _table->get_or_add(card_region, should_grow_table);
}

class G1CardSetHashTable : public CHeapObj<mtGCCardSet> {
    G1CardSetHashTableValue *get_or_add(uint region_idx, bool *should_grow) {
        G1CardSetHashTableLookUp lookup(region_idx);
        G1CardSetHashTableFound found;

        if (_table.get(Thread::current(), lookup, found)) {
            // 找到了, 直接返回
            return found.value();
        }

        // 没找到, 新建并返回

        // 通过value把分区id和容器指针关联起来
        G1CardSetHashTableValue value(region_idx, G1CardSetInlinePtr());
        // 把value添加到_table中
        bool inserted = _table.insert_get(Thread::current(), lookup, value, found, should_grow);

        if (!_inserted_card && inserted) {
            Atomic::store(&_inserted_card, true);
        }

        return found.value();
    }
};
```
