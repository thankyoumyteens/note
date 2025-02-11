# 释放 \_buckets 中的容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.inline.hpp --- //

template<class ContainerPtrVisitor>
inline void G1CardSetHowl::iterate(ContainerPtrVisitor &found, uint num_card_sets) {
    for (uint i = 0; i < num_card_sets; ++i) {
        found(&_buckets[i]);
    }
}

// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

class G1ReleaseCardsets : public StackObj {
    G1CardSet *_card_set;
    using ContainerPtr = G1CardSet::ContainerPtr;

    void coarsen_to_full(ContainerPtr *container_addr) {
        while (true) {
            // container_addr指向_buckets数组中的某个元素
            ContainerPtr cur_container = Atomic::load_acquire(container_addr);
            uint cs_type = G1CardSet::container_type(cur_container);
            // 已经是FullCardSet了, 无需释放
            if (cur_container == G1CardSet::FullCardSet) {
                return;
            }

            // 把cur_container替换成FullCardSet
            ContainerPtr old_value = Atomic::cmpxchg(container_addr, cur_container, G1CardSet::FullCardSet);

            // 替换成功
            if (old_value == cur_container) {
                // 释放旧容器的空间
                _card_set->release_and_maybe_free_container(cur_container);
                return;
            }
        }
    }

public:
    explicit G1ReleaseCardsets(G1CardSet *card_set) : _card_set(card_set) {}

    void operator()(ContainerPtr *container_addr) {
        coarsen_to_full(container_addr);
    }
};
```
