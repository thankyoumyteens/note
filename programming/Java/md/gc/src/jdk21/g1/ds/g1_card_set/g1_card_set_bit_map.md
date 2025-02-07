# 位图模式容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.hpp --- //

class G1CardSetBitMap : public G1CardSetContainer {
    // 位图中值是1的位的个数
    size_t _num_bits_set;
    // 数组中每个元素包含64个位
    BitMap::bm_word_t _bits[1];
};
```

## 添加

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

inline G1AddCardResult G1CardSetBitMap::add(uint card_idx, size_t threshold, size_t size_in_bits) {
    // BitMapView是BitMap的一个实现类, 操作基本和BitMap一样
    BitMapView bm(_bits, size_in_bits);
    if (_num_bits_set >= threshold) {
        // 如果已经达到阈值, 且卡片索引不在位图中, 则返回Overflow
        return bm.at(card_idx) ? Found : Overflow;
    }
    // 把卡片索引设为1
    // 如果卡片索引已经存在, 则par_set_bit返回false
    if (bm.par_set_bit(card_idx)) {
        Atomic::inc(&_num_bits_set, memory_order_relaxed);
        return Added;
    }
    return Found;
}
```
