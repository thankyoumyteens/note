# 遍历 howl 容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

template<class CardOrRangeVisitor>
inline void G1CardSetHowl::iterate(CardOrRangeVisitor &found, G1CardSetConfiguration *config) {
    // _buckets中的每个元素都是一个容器
    for (uint i = 0; i < config->num_buckets_in_howl(); ++i) {
        // 遍历每个bucket内的卡片索引
        iterate_cardset(_buckets[i], i, found, config);
    }
}
```
