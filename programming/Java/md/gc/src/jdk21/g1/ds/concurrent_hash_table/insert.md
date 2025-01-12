# 新增元素

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.hpp --- //

template<typename CONFIG, MEMFLAGS F>
class ConcurrentHashTable : public CHeapObj<F> {
    // 新增成功返回true, 如果找到重复数据则调用FOUND_FUNC函数
    template<typename LOOKUP_FUNC, typename FOUND_FUNC>
    bool insert_get(Thread *thread, LOOKUP_FUNC &lookup_f, VALUE &value, FOUND_FUNC &foundf,
                    bool *grow_hint = nullptr, bool *clean_hint = nullptr) {
        return internal_insert_get(thread, lookup_f, value, foundf, grow_hint, clean_hint);
    }
};

// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //
template<typename CONFIG, MEMFLAGS F>
template<typename LOOKUP_FUNC, typename FOUND_FUNC>
inline bool ConcurrentHashTable<CONFIG, F>::
internal_insert_get(Thread *thread, LOOKUP_FUNC &lookup_f, const VALUE &value,
                    FOUND_FUNC &foundf, bool *grow_hint, bool *clean_hint) {
    bool ret = false;
    bool clean = false;
    bool locked;
    size_t loops = 0;
    size_t i = 0;
    uintx hash = lookup_f.get_hash();
    // 创建节点
    Node *new_node = Node::create_node(_context, value, nullptr);

    while (true) {
        {
            // 进入RCU读临界区
            ScopedCS cs(thread, this);
            Bucket *bucket = get_bucket(hash);
            Node *first_at_start = bucket->first();
            // 根据LOOKUP_FUNC查找节点
            Node *old = get_node(bucket, lookup_f, &clean, &loops);
            if (old == nullptr) {
                // 没找到重复节点
                // 把新节点插入链表头
                new_node->set_next(first_at_start);
                // bucket->first指向新的头节点(CAS操作)
                // 另外, 如果bucket已上锁, 则不能修改, 返回false
                if (bucket->cas_first(new_node, first_at_start)) {
                    foundf(new_node->value());
                    JFR_ONLY(safe_stats_add();)
                    new_node = nullptr;
                    ret = true;
                    // 退出RCU读临界区
                    break;
                }
                // CAS失败, 等下次循环重试
                locked = bucket->is_locked();
            } else {
                // 节点已存在, 调用FOUND_FUNC
                foundf(old->value());
                // 退出RCU读临界区
                break;
            }
            // 退出RCU读临界区
        }
        i++;
        if (locked) {
            // 让出处理器
            os::naked_yield();
        } else {
            // 自旋
            // return 0;
            SpinPause();
        }
    }

    if (new_node != nullptr) {
        // 把新节点插入链表头后new_node会被设为nullptr
        // 如果它不是nullptr, 就表示节点已存在, 则释放new_node的内存
        Node::destroy_node(_context, new_node);
    } else if (i == 0 && clean) {
        // 没有线程竞争时, 进行清理工作

        // 根据哈希值获取bucket数组中的元素, 并把找到的bucket加锁, 清理完成前避免这个bucket被修改
        Bucket *bucket = get_bucket_locked(thread, lookup_f.get_hash());
        // 清理bucket中无效的数据
        delete_in_bucket(thread, bucket, lookup_f);
        // 解锁
        bucket->unlock();
        clean = false;
    }

    if (grow_hint != nullptr) {
        *grow_hint = loops > _grow_hint;
    }

    if (clean_hint != nullptr) {
        *clean_hint = clean;
    }

    return ret;
}
```
