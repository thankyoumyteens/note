# 卡片数组模式容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.hpp --- //

class G1CardSetArray : public G1CardSetContainer {
public:
    typedef uint16_t EntryDataType;
    typedef uint EntryCountType;
    using ContainerPtr = G1CardSet::ContainerPtr;
private:
    // 数组最大容量
    EntryCountType _size;
    // 数组元素个数
    EntryCountType volatile _num_entries;
    // 数组
    EntryDataType _data[2];

    // 最高位是1, 其余位是0
    static const EntryCountType LockBitMask = (EntryCountType) 1 << (sizeof(EntryCountType) * BitsPerByte - 1);
    // 最高位是0, 其余位是1
    static const EntryCountType EntryMask = LockBitMask - 1;

    // _num_entries的最高位是1则表示上锁, 最高位是0则表示没上锁
    class G1CardSetArrayLocker : public StackObj {
        // 指向_num_entries的指针
        EntryCountType volatile *_num_entries_addr;
        // 本地临时变量, 在析构函数中会替换_num_entries
        EntryCountType _local_num_entries;
    public:
        // 上锁
        // value: 指向传入的_num_entries的地址
        G1CardSetArrayLocker(EntryCountType volatile *value);

        EntryCountType num_entries() const { return _local_num_entries; }

        void inc_num_entries() {
            assert(((_local_num_entries + 1) & EntryMask) == (EntryCountType) (_local_num_entries + 1), "no overflow");
            _local_num_entries++;
        }

        // 把_num_entries的值设置成_local_num_entries, 同时解锁(因为_local_num_entries的最高位是0)
        ~G1CardSetArrayLocker() {
            Atomic::release_store(_num_entries_addr, _local_num_entries);
        }
    };
}:
```

## 添加

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

inline G1AddCardResult G1CardSetArray::add(uint card_idx) {
    assert(card_idx < (1u << (sizeof(_data[0]) * BitsPerByte)),
           "Card index %u does not fit allowed card value range.", card_idx);
    // 获取不包含锁状态(把最高位置0)的数组长度
    EntryCountType num_entries = Atomic::load_acquire(&_num_entries) & EntryMask;
    EntryCountType idx = 0;
    for (; idx < num_entries; idx++) {
        if (_data[idx] == card_idx) {
            // 要添加的卡片索引已经在数组中了
            return Found;
        }
    }

    // Since we did not find the card, lock.
    // 上锁
    G1CardSetArrayLocker x(&_num_entries);

    // Reload number of entries from the G1CardSetArrayLocker as it might have changed.
    // It already read the actual value with the necessary synchronization.
    // 在等待锁期间, 数组长度可能已经改变, 需要重新读取一次
    num_entries = x.num_entries();
    // Look if the cards added while waiting for the lock are the same as our card.
    // 如果在等待锁期间, 数组中已经添加了相同的卡片索引, 则不需要再添加了
    for (; idx < num_entries; idx++) {
        if (_data[idx] == card_idx) {
            return Found;
        }
    }

    // Check if there is space left.
    // 检查数组是否还有空间
    if (num_entries == _size) {
        return Overflow;
    }

    // 把新的卡片索引添加到数组末尾
    _data[num_entries] = card_idx;

    // 增加数组长度
    x.inc_num_entries();

    return Added;
}
```
