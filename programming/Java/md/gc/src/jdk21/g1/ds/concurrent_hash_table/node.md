# Node 操作

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.inline.hpp --- //

template<typename CONFIG, MEMFLAGS F>
template<typename LOOKUP_FUNC>
typename ConcurrentHashTable<CONFIG, F>::Node *
ConcurrentHashTable<CONFIG, F>::
get_node(const Bucket *const bucket, LOOKUP_FUNC &lookup_f,
         bool *have_dead, size_t *loops) const {
    // 找到节点需要的循环次数
    size_t loop_count = 0;
    // 链表头节点
    Node *node = bucket->first();
    while (node != nullptr) {
        bool is_dead = false;
        ++loop_count;
        // 判断是不是查找的目标
        if (lookup_f.equals(node->value(), &is_dead)) {
            break;
        }
        if (is_dead && !(*have_dead)) {
            // 这个节点需要清理
            *have_dead = true;
        }
        // 下一个节点
        node = node->next();
    }
    if (loops != nullptr) {
        *loops = loop_count;
    }
    return node;
}
```
