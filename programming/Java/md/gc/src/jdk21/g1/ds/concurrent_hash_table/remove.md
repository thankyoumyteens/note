# 删除元素

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.hpp --- //

template<typename CONFIG, MEMFLAGS F>
class ConcurrentHashTable : public CHeapObj<F> {
    template<typename LOOKUP_FUNC, typename DELETE_FUNC>
    bool remove(Thread *thread, LOOKUP_FUNC &lookup_f, DELETE_FUNC &del_f) {
        return internal_remove(thread, lookup_f, del_f);
    }
};

// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
template<typename LOOKUP_FUNC, typename DELETE_FUNC>
inline bool ConcurrentHashTable<CONFIG, F>::
internal_remove(Thread *thread, LOOKUP_FUNC &lookup_f, DELETE_FUNC &delete_f) {
    // 获取bucket并上锁
    Bucket *bucket = get_bucket_locked(thread, lookup_f.get_hash());
    assert(bucket->is_locked(), "Must be locked.");

    Node *const volatile *rem_n_prev = bucket->first_ptr();
    Node *rem_n = bucket->first();
    bool have_dead = false;
    // 查找节点并删除
    while (rem_n != nullptr) {
        if (lookup_f.equals(rem_n->value(), &have_dead)) {
            // 更新链表指针
            // 把 prev -> current -> next
            // 变成 prev -> next
            bucket->release_assign_node_ptr(rem_n_prev, rem_n->next());
            break;
        } else {
            rem_n_prev = rem_n->next_ptr();
            rem_n = rem_n->next();
        }
    }

    bucket->unlock();

    if (rem_n == nullptr) {
        return false;
    }
    GlobalCounter::write_synchronize();
    delete_f(rem_n->value());
    // 删除节点
    Node::destroy_node(_context, rem_n);
    JFR_ONLY(safe_stats_remove();)
    return true;
}

template<typename CONFIG, MEMFLAGS F>
inline void ConcurrentHashTable<CONFIG, F>::
Bucket::release_assign_node_ptr(
        typename ConcurrentHashTable<CONFIG, F>::Node *const volatile *dst,
        typename ConcurrentHashTable<CONFIG, F>::Node *node) const {
    assert(is_locked(), "Must be locked.");
    Node **tmp = (Node **) dst;
    // clear_set_state函数返回: 把node的旧状态清除, 并设置为dst的状态的指针
    // release_store函数将clear_set_state函数返回的新指针存储到tmp所指向的内存位置(即更新链表指针)
    // 把*tmp指针的地址替换成node指针的地址
    // 等同于把原来的*tmp节点删掉了
    Atomic::release_store(tmp, clear_set_state(node, *dst));
}

static Node *clear_set_state(Node *node, Node *state) {
    // 返回的指针: 把node的旧状态清除, 并设置为state的状态
    // 示例:
    // node: 10111001
    // state: 10101011
    // clear_state(node): 10111000
    // get_state(state): 00000011
    // 最终: 10111000 ^ 00000011 = 10111011
    return (Node *) (((uintptr_t) clear_state(node)) ^ get_state(state));
}
```
