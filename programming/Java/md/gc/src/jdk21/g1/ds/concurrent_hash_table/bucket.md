# Bucket 操作

## 上锁

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline bool ConcurrentHashTable<CONFIG, F>::
Bucket::trylock() {
    // 已上锁, 直接返回失败
    if (is_locked()) {
        return false;
    }
    // 上锁
    // 把first指针的低位设置为STATE_LOCK_BIT
    // STATE_LOCK_BIT = 0x1
    Node *tmp = first();
    if (Atomic::cmpxchg(&_first, tmp, set_state(tmp, STATE_LOCK_BIT)) == tmp) {
        return true;
    }
    // CAS失败
    return false;
}

template<typename CONFIG, MEMFLAGS F>
inline bool ConcurrentHashTable<CONFIG, F>::
Bucket::is_locked() const {
    return is_state(first_raw(), STATE_LOCK_BIT);
}

static bool is_state(Node *node, uintptr_t bits) {
    return (bits & (uintptr_t) node) == bits;
}

static Node *set_state(Node *n, uintptr_t bits) {
    return (Node *) (bits | (uintptr_t) n);
}
```

## 解锁

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline void ConcurrentHashTable<CONFIG, F>::
Bucket::unlock() {
    assert(is_locked(), "Must be locked.");
    assert(!have_redirect(),
           "Unlocking a bucket after it has reached terminal state.");
    Atomic::release_store(&_first, clear_state(first()));
}

static Node *clear_state(Node *node) {
    // STATE_MASK = 0x3
    // 把最低两位置为0
    return (Node *) (((uintptr_t) node) & (~(STATE_MASK)));
}
```

## 获取 bucket

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline typename ConcurrentHashTable<CONFIG, F>::Bucket *
ConcurrentHashTable<CONFIG, F>::
get_bucket(uintx hash) const {
    // 获取 _table
    InternalTable *table = get_table();
    // 根据哈希值获取bucket数组中的元素
    Bucket *bucket = get_bucket_in(table, hash);
    // ConcurrentHashTable 正在扩容, 需要使用 _new_table, 而不是 _table
    // 根据哈希值重新获取bucket数组中的元素
    if (bucket->have_redirect()) {
        table = get_new_table();
        bucket = get_bucket_in(table, hash);
    }
    return bucket;
}

template<typename CONFIG, MEMFLAGS F>
class ConcurrentHashTable : public CHeapObj<F> {
    Bucket *get_bucket_in(InternalTable *table, const uintx hash) const {
        // 根据哈希值算出数组的索引
        size_t bucket_index = bucket_idx_hash(table, hash);
        return table->get_bucket(bucket_index);
    }

    static size_t bucket_idx_hash(InternalTable *table, const uintx hash) {
        // _hash_mask 用来保证算出的索引不会落在数组外
        return ((size_t) hash) & table->_hash_mask;
    }

    class InternalTable : public CHeapObj<F> {
        Bucket *get_bucket(size_t idx) {
            return &_buckets[idx];
        }
    };
};
```

## 获取 bucket 并上锁

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
inline typename ConcurrentHashTable<CONFIG, F>::Bucket *
ConcurrentHashTable<CONFIG, F>::
get_bucket_locked(Thread *thread, const uintx hash) {
    Bucket *bucket;
    int i = 0;
    while (true) {
        {
            // 进入RCU读临界区
            ScopedCS cs(thread, this);
            // 获取bucket
            bucket = get_bucket(hash);
            // 加锁
            if (bucket->trylock()) {
                // 退出RCU读临界区
                break;
            }
            // 退出RCU读临界区
        }
        // 加锁失败, 自旋/让出处理器
        if ((++i) == SPINPAUSES_PER_YIELD) {
            os::naked_yield();
            i = 0;
        } else {
            SpinPause();
        }
    }
    return bucket;
}
```

## 清理 bucket 中无效的数据

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
template<typename LOOKUP_FUNC>
inline void ConcurrentHashTable<CONFIG, F>::
delete_in_bucket(Thread *thread, Bucket *bucket, LOOKUP_FUNC &lookup_f) {
    assert(bucket->is_locked(), "Must be locked.");

    size_t dels = 0;
    // 用来暂存那些被删除的节点
    Node *ndel[StackBufferSize];
    // 获取带状态的Node指针的指针
    Node *const volatile *rem_n_prev = bucket->first_ptr();
    // 获取不带状态的Node指针
    Node *rem_n = bucket->first();
    while (rem_n != nullptr) {
        bool is_dead = false;
        // 在equals函数中, 会判断value是否还要继续使用, 并设置is_dead的值
        lookup_f.equals(rem_n->value(), &is_dead);
        if (is_dead) {
            // 需要删除这个节点
            ndel[dels++] = rem_n;
            // 下一个节点
            Node *next_node = rem_n->next();
            // rem_n_prev也指向下一个节点
            // release_assign_node_ptr的作用: rem_n_prev = 不带状态的next_node指针 + rem_n_prev的状态
            bucket->release_assign_node_ptr(rem_n_prev, next_node);
            rem_n = next_node;
            if (dels == StackBufferSize) {
                break;
            }
        } else {
            // 保留这个节点, 继续遍历
            rem_n_prev = rem_n->next_ptr();
            rem_n = rem_n->next();
        }
    }
    // 删除节点
    if (dels > 0) {
        GlobalCounter::write_synchronize();
        for (size_t node_it = 0; node_it < dels; node_it++) {
            Node::destroy_node(_context, ndel[node_it]);
            JFR_ONLY(safe_stats_remove();)
            DEBUG_ONLY(ndel[node_it] = (Node *) POISON_PTR;)
        }
    }
}

template<typename CONFIG, MEMFLAGS F>
inline void ConcurrentHashTable<CONFIG, F>::
Bucket::release_assign_node_ptr(
        typename ConcurrentHashTable<CONFIG, F>::Node *const volatile *dst,
        typename ConcurrentHashTable<CONFIG, F>::Node *node) const {
    assert(is_locked(), "Must be locked.");
    Node **tmp = (Node **) dst;
    // clear_set_state函数返回: 把node的旧状态清除, 并设置为dst的状态的指针
    Atomic::release_store(tmp, clear_set_state(node, *dst));
}

// --- src/hotspot/share/utilities/concurrentHashTable.hpp --- //

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
