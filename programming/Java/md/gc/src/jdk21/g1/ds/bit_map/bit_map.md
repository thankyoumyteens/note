# 位图

抽象基类 BitMap 用于表示无符号整数数组的位图操作(只提供操作, 不存储数据)。BitMap 的底层存储空间分配由子类负责处理, BitMap 本身不会分配或释放底层存储空间。

BitMap 使用数组存储数据, 数组的每个元素是 bm_word_t(64 位)类, 所以数组的每个元素可以存放 64 个位图中的位。

```cpp
// --- src/hotspot/share/utilities/bitMap.hpp --- //

class BitMap {
public:
    // 索引类型
    typedef size_t idx_t;
    // 数组元素的类型
    typedef uintptr_t bm_word_t;
private:
    // 数组的首地址
    bm_word_t *_map;
    // 位图的大小(单位: 比特)
    idx_t _size;

protected:
    bm_word_t *map() { return _map; }

    static idx_t raw_to_words_align_down(idx_t bit) {
        // 一个bm_word_t中存放64个位
        // 所以bit为0~63的位保存在数组(_map)的0号元素中,
        // 64～127的位保存在数组的1号元素中,
        // 以此类推

        // LogBitsPerWord = 6
        // bit把bit除以64得到数组对应元素的索引
        return bit >> LogBitsPerWord;
    }

    bm_word_t *word_addr(idx_t bit) {
        // bit 是BitMap的位
        // map() 返回数组的首地址
        // 首地址+偏移量 定位到bit所在的数组元素(指向该元素的指针)
        // 比如 bit=20, bit/64=0, 定位到_map[0]
        // 比如 bit=65, bit/64=1, 定位到_map[1]
        return map() + to_words_align_down(bit);
    }

    static bm_word_t bit_mask(idx_t bit) {
        // 把bm_word_t长度的数值中, 第bit位设为1, 其他位设为0
        return (bm_word_t) 1 << bit_in_word(bit);
    }

public:
    // 判断index是否在位图中
    bool at(idx_t index) const {
        // 确保索引不越界
        verify_index(index);

        // index在位图中值为1, 则返回true
        return (*word_addr(index) & bit_mask(index)) != 0;
    }
};
```

## 设置 bit 位的值

```cpp
// --- src/hotspot/share/utilities/bitMap.inline.hpp --- //

// 设置bit位的值(多线程并行)
inline bool BitMap::par_set_bit(idx_t bit, atomic_memory_order memory_order) {
    verify_index(bit);
    // 定位到bit所在的数组元素
    volatile bm_word_t *const addr = word_addr(bit);
    // 把bm_word_t长度的数值中, 第bit位设为1, 其他位设为0
    const bm_word_t mask = bit_mask(bit);
    // 获取修改前的值
    bm_word_t old_val = load_word_ordered(addr, memory_order);

    do {
        // 把bit所在的位改为1, 得到新值
        const bm_word_t new_val = old_val | mask;
        // 如果新值和旧值相同, 说明其他线程已经修改过该位, 返回false
        if (new_val == old_val) {
            return false;
        }
        // 使用CAS操作, 把addr指向的值改为new_val
        const bm_word_t cur_val = Atomic::cmpxchg(addr, old_val, new_val, memory_order);
        // 如果cur_val和old_val相同, 说明CAS操作成功, 返回true
        if (cur_val == old_val) {
            return true;
        }
        // 如果cur_val和old_val不同, 说明addr指向的值已经被其他线程修改过, 需要重新获取旧值, 重新尝试
        old_val = cur_val;
    } while (true);
}

inline const BitMap::bm_word_t
BitMap::load_word_ordered(const volatile bm_word_t *const addr, atomic_memory_order memory_order) {
    if (memory_order == memory_order_relaxed || memory_order == memory_order_release) {
        return Atomic::load(addr);
    } else {
        assert(memory_order == memory_order_acq_rel ||
               memory_order == memory_order_acquire ||
               memory_order == memory_order_conservative,
               "unexpected memory ordering");
        return Atomic::load_acquire(addr);
    }
}
```
