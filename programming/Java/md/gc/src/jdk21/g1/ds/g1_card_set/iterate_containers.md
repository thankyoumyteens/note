# 遍历容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

void G1CardSet::iterate_containers(ContainerPtrClosure *cl, bool at_safepoint) {
    // Lambda 表达式
    // [&]：表示以引用捕获的方式捕获外部作用域中的所有变量，这样在 Lambda 表达式内部可以使用外部的 cl 变量
    // (G1CardSetHashTableValue *value)：Lambda 表达式的参数，是一个指向 G1CardSetHashTableValue 对象的指针
    auto do_value =
            [&](G1CardSetHashTableValue *value) {
                cl->do_containerptr(value->_region_idx, value->_num_occupied, value->_container);
                return true;
            };

    // 遍历容器
    if (at_safepoint) {
        // 在安全点内遍历
        _table->iterate_safepoint(do_value);
    } else {
        _table->iterate(do_value);
    }
}

class G1CardSetHashTable : public CHeapObj<mtGCCardSet> {
    template<typename SCAN_FUNC>
    void iterate_safepoint(SCAN_FUNC &scan_f) {
        _table_scanner.do_safepoint_scan(scan_f);
    }
};

// --- src/hotspot/share/utilities/concurrentHashTableTasks.inline.hpp --- //

class ConcurrentHashTable<CONFIG, F>::ScanTask :
        public BucketsOperation {
    template<typename SCAN_FUNC>
    void do_safepoint_scan(SCAN_FUNC &scan_f) {
        assert(SafepointSynchronize::is_at_safepoint(),
               "must only be called in a safepoint");

        size_t start_idx = 0, stop_idx = 0;
        InternalTable *table = nullptr;

        // claim函数找出ConcurrentHashTable中下一个要扫描的区间
        while (claim(&start_idx, &stop_idx, &table)) {
            assert(table != nullptr, "precondition");
            // 遍历这个区间
            if (!this->_cht->do_scan_for_range(scan_f, start_idx, stop_idx, table)) {
                return;
            }
            table = nullptr;
        }
    }
};
```

## 找出要扫描的区间

```cpp
// --- src/hotspot/share/utilities/concurrentHashTableTasks.inline.hpp --- //

class ConcurrentHashTable<CONFIG, F>::ScanTask :
        public BucketsOperation {
    bool claim(size_t *start, size_t *stop, InternalTable **table) {
        // 找出要扫描的区间 [start, stop)
        if (this->_table_claimer.claim(start, stop)) {
            *table = this->_cht->get_table();
            return true;
        }

        // ConcurrentHashTable 在扩容/收缩时会调整大小, 大致过程如下:
        // 1. 分配一块新内存, 用 _new_table 临时指向
        // 2. 把 _table 中的数据复制到 _new_table 中
        // 3. 把 _table 指向 _new_table 的新内存
        // 4. _new_table 恢复为 nullptr

        // 如果 ConcurrentHashTable 的大小改变, 但还没执行完上面的过程,
        // 则此时 _table 指向旧内存, _new_table 指向新内存,
        // 应该从 _new_table 中选取区间
        if (!_new_table_claimer.have_work()) {
            assert(this->_cht->get_new_table() == nullptr || this->_cht->get_new_table() == POISON_PTR, "Precondition");
            return false;
        }

        *table = this->_cht->get_new_table();
        return _new_table_claimer.claim(start, stop);
    }
};

class InternalTableClaimer {
    bool claim(size_t *start, size_t *stop) {
        // _next初始为0, 假设_size为12
        // 第一次遍历: [0, 12)
        // 第二次遍历: [12, 24)
        // 第三次遍历: [24, 36)
        // ...
        if (Atomic::load(&_next) < _limit) {
            // 类似于:
            // claimed = _next;
            // _next += _size;
            size_t claimed = Atomic::fetch_then_add(&_next, _size);
            if (claimed < _limit) { // 设置要遍历的区间
                *start = claimed;
                *stop = MIN2(claimed + _size, _limit);
                return true;
            }
        }
        return false;
    }
};
```

## 遍历区间

```cpp
// --- src/hotspot/share/utilities/concurrentHashTableTasks.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
template<typename FUNC>
inline bool ConcurrentHashTable<CONFIG, F>::
do_scan_for_range(FUNC &scan_f, size_t start_idx, size_t stop_idx, InternalTable *table) {
    assert(start_idx < stop_idx, "Must be");
    assert(stop_idx <= table->_size, "Must be");

    for (size_t bucket_it = start_idx; bucket_it < stop_idx; ++bucket_it) {
        Bucket *bucket = table->get_bucket(bucket_it);
        // If bucket have a redirect the items will be in the new table.
        // We must visit them there since the new table will contain any
        // concurrent inserts done after this bucket was resized.
        // If the bucket don't have redirect flag all items is in this table.
        if (!bucket->have_redirect()) {
            // Node里value的类型是G1CardSetHashTableValue, 包含: _region_idx, _num_occupied, _container
            if (!visit_nodes(bucket, scan_f)) {
                return false;
            }
        } else {
            assert(bucket->is_locked(), "Bucket must be locked.");
        }
    }
    return true;
}

template<typename CONFIG, MEMFLAGS F>
template<typename FUNC>
inline bool ConcurrentHashTable<CONFIG, F>::
visit_nodes(Bucket *bucket, FUNC &visitor_f) {
    Node *current_node = bucket->first();
    while (current_node != nullptr) {
        Prefetch::read(current_node->next(), 0);
        // Node里value的类型是G1CardSetHashTableValue, 包含: _region_idx, _num_occupied, _container
        if (!visitor_f(current_node->value())) {
            return false;
        }
        current_node = current_node->next();
    }
    return true;
}
```
