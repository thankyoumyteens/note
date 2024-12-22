# ConcurrentHashTable

```cpp
// --- src/hotspot/share/utilities/concurrentHashTable.hpp --- //

template<typename CONFIG, MEMFLAGS F>
class ConcurrentHashTable : public CHeapObj<F> {
    typedef typename CONFIG::Value VALUE;
private:

    class Node {
    private:
        Node *volatile _next;
        VALUE _value;
    };

    class Bucket {
    private:
        // _first指针的最低两位用来存储自旋锁的状态信息，分别是未加锁、加锁、重定向三种状态
        Node *volatile _first;
    };

    class InternalTable : public CHeapObj<F> {
    private:
        // Bucket数组
        Bucket *_buckets;
    };

    InternalTable *_table;      // Active table.
    InternalTable *_new_table;  // Table we are resizing to.


    // Get methods return true on found item with LOOKUP_FUNC and FOUND_FUNC is
    // called.
    template<typename LOOKUP_FUNC, typename FOUND_FUNC>
    bool get(Thread *thread, LOOKUP_FUNC &lookup_f, FOUND_FUNC &foundf,
             bool *grow_hint = nullptr);

    // Returns true if the item was inserted, duplicates are found with
    // LOOKUP_FUNC then FOUND_FUNC is called.
    template<typename LOOKUP_FUNC, typename FOUND_FUNC>
    bool insert_get(Thread *thread, LOOKUP_FUNC &lookup_f, VALUE &value, FOUND_FUNC &foundf,
                    bool *grow_hint = nullptr, bool *clean_hint = nullptr) {
        return internal_insert_get(thread, lookup_f, value, foundf, grow_hint, clean_hint);
    }

    // Returns true if items was deleted matching LOOKUP_FUNC and
    // prior to destruction DELETE_FUNC is called.
    template<typename LOOKUP_FUNC, typename DELETE_FUNC>
    bool remove(Thread *thread, LOOKUP_FUNC &lookup_f, DELETE_FUNC &del_f) {
        return internal_remove(thread, lookup_f, del_f);
    }

};
```
