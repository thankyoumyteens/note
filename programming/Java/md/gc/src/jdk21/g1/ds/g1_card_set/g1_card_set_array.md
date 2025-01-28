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
