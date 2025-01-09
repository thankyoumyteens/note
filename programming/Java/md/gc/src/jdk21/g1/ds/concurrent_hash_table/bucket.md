# Bucket 操作

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

```
